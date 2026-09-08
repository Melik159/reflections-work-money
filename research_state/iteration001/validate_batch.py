"""Read-only STRUCTURAL checks of iteration 001; no scientific adjudication.

Run from any directory with Python and PyYAML; --complete requires ten cycles.
Prints JSON to stdout and never writes to the repository.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "research_state"
TASK_FIELDS = "id priority topic question related_rq related_claims roles pages_hint data_needed status created_from expected_output".split()
DECISION_FIELDS = "id task decision finding_class claims questions sources reviewers candidate_path negative_results scientific_scope".split()
CANDIDATE_FIELDS = "target current_state proposed_state evidence counterevidence reviewers confidence reason impact".split()
EXPERIMENT_FIELDS = "id question claims hypotheses variables measurement_level dataset design competing_models prediction falsification_condition discriminating_power status".split()
DECISIONS = {"ACCEPT", "QUALIFY", "REJECT", "OPEN DISPUTE", "OPEN_DISPUTE"}
FINDINGS = set("CONFIRMS_EXISTING QUALIFIES_EXISTING NEW_CLAIM_CANDIDATE NEW_SCENARIO NEW_FORMAL_ISSUE NEW_MEASUREMENT_ISSUE NEW_EMPIRICAL_RESULT NEW_COUNTEREXAMPLE NEW_LITERATURE_PARALLEL NEW_DISCRIMINATING_PREDICTION".split())


def validate(complete=False):
    errors = []
    counts = {"cycles": 0, "tasks": 0, "experiments": 0, "manifest_entries": 0}

    def check(condition, message):
        if not condition:
            errors.append(message)
        return bool(condition)

    def read(path, loader=json.loads):
        try:
            return loader(path.read_text())
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            return None

    def fields(record, required, label):
        if not check(isinstance(record, dict), f"{label}: expected mapping"):
            return False
        for name in required:
            check(name in record, f"{label}: missing {name}")
        return True

    def local_file(value, label, under=None):
        if not check(isinstance(value, str) and bool(value), f"{label}: expected path"):
            return False
        path = (ROOT / value).resolve()
        if not check(path.is_relative_to(ROOT), f"{label}: path escapes repository"):
            return False
        if under is not None:
            check(path.is_relative_to(ROOT / under), f"{label}: outside {under}")
        return check(path.is_file(), f"{label}: missing file {value}")

    def reviewers(value, label):
        roles = {}
        if isinstance(value, dict):
            roles = value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    roles[item.get("role", "")] = item.get("path")
        for role in ("specialist", "adversarial", "evidence"):
            matching = [v for k, v in roles.items() if role in k.lower()]
            check(bool(matching), f"{label}: missing {role} review")
            for entry in matching:
                for path in entry if isinstance(entry, list) else [entry]:
                    local_file(path, f"{label}/{role}")

    claims_data = read(ROOT / "analysis/data/claims.jsonl", lambda text: [json.loads(line) for line in text.splitlines() if line.strip()])
    graph = read(ROOT / "research_questions/question_graph.json")
    claims = {x["id"] for x in claims_data or []}
    questions = {x["id"] for x in (graph or {}).get("nodes", [])}

    def links(value, known, label):
        if check(isinstance(value, list), f"{label}: expected list"):
            for item in value:
                check(isinstance(item, str) and item in known, f"{label}: unknown ID {item}")

    tasks = read(STATE / "NEXT_ACTIONS.yaml", yaml.safe_load)
    task_ids = set()
    if check(isinstance(tasks, list), "NEXT_ACTIONS: expected list"):
        for task in tasks:
            if not isinstance(task, dict):
                check(False, "NEXT_ACTIONS: entry must be mapping")
                continue
            tid = task.get("id")
            check(isinstance(tid, str), "NEXT_ACTIONS: missing string id")
            check(tid not in task_ids, f"NEXT_ACTIONS: duplicate {tid}")
            task_ids.add(tid)
            if not isinstance(tid, str) or not re.fullmatch(r"ITER001-P0-(?:0[1-9]|10)", tid):
                continue  # Historical and follow-up tasks have independent schemas.
            counts["tasks"] += 1
            fields(task, TASK_FIELDS, tid)
            check(task.get("priority") in {"P0", "P1", "P2", "P3"}, f"{tid}: invalid priority")
            links(task.get("related_claims"), claims, f"{tid}/claims")
            links(task.get("related_rq"), questions, f"{tid}/questions")
        for n in range(1, 11):
            check(f"ITER001-P0-{n:02}" in task_ids, f"Missing initial task {n:02}")

    cycle_ids = set()
    for path in sorted((STATE / "iteration001").glob("C*/decision.json")):
        counts["cycles"] += 1
        cid = path.parent.name
        check(bool(re.fullmatch(r"C(?:0[1-9]|10)", cid)), f"Unexpected cycle directory {cid}")
        cycle_ids.add(cid)
        record = read(path)
        if not fields(record, DECISION_FIELDS, cid):
            continue
        check(record.get("id") in {cid, f"ITER001-{cid}"}, f"{cid}: decision id mismatch")
        check(record.get("task") in task_ids, f"{cid}: unknown task")
        check(record.get("task") == f"ITER001-P0-{cid[1:]}", f"{cid}: task/cycle mismatch")
        check(record.get("decision") in DECISIONS, f"{cid}: invalid decision")
        finding = record.get("finding_class")
        for item in finding if isinstance(finding, list) else [finding]:
            check(isinstance(item, str) and item in FINDINGS, f"{cid}: invalid discovery class {item}")
        links(record.get("claims"), claims, f"{cid}/claims")
        links(record.get("questions"), questions, f"{cid}/questions")
        check(isinstance(record.get("negative_results"), list), f"{cid}: negative_results must be list")
        check(bool(record.get("scientific_scope")), f"{cid}: empty scientific_scope")
        reviewers(record.get("reviewers"), f"{cid}/reviewers")
        report_dir = ROOT / "agents/reports" / f"ITER001-{cid}"
        provenance_path = report_dir / "provenance.json"
        source_path = report_dir / "source_pages.txt"
        local_file(str(source_path.relative_to(ROOT)), f"{cid}/source pages")
        provenance = read(provenance_path)
        if isinstance(provenance, dict):
            check(provenance.get("task") == f"ITER001-{cid}" or
                  (provenance.get("task") == record.get("task") and provenance.get("cycle") == f"ITER001-{cid}"),
                  f"{cid}: provenance task mismatch")
            # Preparatory extraction locators do not attest later source reading.
            pages = provenance.get("pages_read_pdf", provenance.get("pages_actually_read", provenance.get("pages_hint_extracted")))
            check(isinstance(pages, list) and bool(pages) and all(isinstance(p, int) and 1 <= p <= 562 for p in pages), f"{cid}: invalid source page locators")
            if "page_text_sha256" in provenance:
                extracted = read(ROOT / "corpus/extracted/Reflections_PierreCampergue.pages.jsonl", lambda text: [json.loads(line) for line in text.splitlines() if line.strip()])
                source_pages = {str(row['page_pdf']): row['text'] for row in extracted or []}
                for page, expected in provenance["page_text_sha256"].items():
                    check(page in source_pages and hashlib.sha256(source_pages[page].encode()).hexdigest() == expected, f"{cid}: source page hash mismatch {page}")
                check(all(str(page) in provenance["page_text_sha256"] for page in pages), f"{cid}: page locator has no page hash")
            if provenance.get("source_pages_sha256") and source_path.is_file():
                check(hashlib.sha256(source_path.read_bytes()).hexdigest() == provenance["source_pages_sha256"], f"{cid}: source extract file hash mismatch")
            hashes = provenance.get("input_sha256")
            check(isinstance(hashes, dict) and bool(hashes), f"{cid}: missing provenance hashes")
            for name, expected in hashes.items() if isinstance(hashes, dict) else []:
                if local_file(name, f"{cid}/provenance input"):
                    check(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f"{cid}: provenance hash mismatch {name}")
            retrieval = provenance.get("retrieval")
            check(isinstance(retrieval, list) and bool(retrieval), f"{cid}: missing retrieval records")
            collections = set()
            for entry in retrieval if isinstance(retrieval, list) else []:
                if not fields(entry, ["collection", "query", "file"], f"{cid}/retrieval"):
                    continue
                collections.add(entry.get("collection"))
                file = entry.get("file")
                if isinstance(file, str):
                    local_file(str((report_dir / file).relative_to(ROOT)), f"{cid}/retrieval file")
            check({"SOURCE_CORPUS", "DERIVED_ANALYSIS"} <= collections, f"{cid}: missing separated retrieval collections")
        sources = record.get("sources")
        check(isinstance(sources, list) and bool(sources), f"{cid}: sources must be nonempty list")
        for source in sources if isinstance(sources, list) else []:
            value = source.get("path", source.get("url")) if isinstance(source, dict) else source
            if isinstance(value, str) and value.startswith(("https://", "http://")):
                continue  # URL presence only, not source verification.
            local_file(value, f"{cid}/source")
        candidate_path = record.get("candidate_path")
        if local_file(candidate_path, f"{cid}/candidate", "candidate_changes"):
            candidate = read(ROOT / candidate_path)
            if fields(candidate, CANDIDATE_FIELDS, f"{cid}/candidate"):
                reviewers(candidate.get("reviewers"), f"{cid}/candidate/reviewers")
                check(candidate.get("reviewers") == record.get("reviewers"), f"{cid}: candidate/decision reviewer chain differs")
                evidence = candidate.get("evidence")
                check(isinstance(evidence, list) and bool(evidence), f"{cid}: candidate evidence must list references")
                for reference in evidence if isinstance(evidence, list) else []:
                    local_file(reference, f"{cid}/candidate evidence")

    check(1 <= counts["cycles"] <= 10, "Expected 1..10 completed cycle records")
    check(cycle_ids == {f"C{n:02}" for n in range(1, counts["cycles"] + 1)}, "Cycle records must form a contiguous sequence from C01")
    if complete:
        check(cycle_ids == {f"C{n:02}" for n in range(1, 11)}, "Complete batch requires C01..C10")
        local_file("research_state/iteration_report_001.md", "final report")

    experiments = read(STATE / "EXPERIMENT_QUEUE.yaml", yaml.safe_load)
    experiment_ids = set()
    if check(isinstance(experiments, list), "EXPERIMENT_QUEUE: expected list"):
        for record in experiments:
            counts["experiments"] += 1
            if not fields(record, EXPERIMENT_FIELDS, "experiment"):
                continue
            eid = record.get("id")
            check(isinstance(eid, str) and eid not in experiment_ids, f"Invalid/duplicate experiment ID {eid}")
            experiment_ids.add(eid)
            links(record.get("claims"), claims, f"{eid}/claims")
            check(record.get("status") in {"DESIGN", "READY", "RUNNING", "COMPLETED", "BLOCKED", "REJECTED"}, f"{eid}: invalid status")

    manifest = ROOT / "closure_review/BASELINE_MANIFEST_SHA256.txt"
    try:
        for line in manifest.read_text().splitlines():
            expected, name = line.split(maxsplit=1)
            name = name.lstrip("*")
            counts["manifest_entries"] += 1
            if local_file(name, "manifest"):
                check(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f"Baseline hash mismatch: {name}")
    except (OSError, ValueError) as exc:
        errors.append(f"Manifest error: {exc}")
    return {"category": "STRUCTURAL", "scientific_evidence_established": False,
            "complete_required": complete, "status": "FAIL" if errors else "PASS",
            "counts": counts, "errors": errors,
            "limitations": "Checks presence, links, schemas, source provenance and hashes; contiguous cycle numbering and review dependency presence do not establish real-time review chronology, source meaning, review quality, independent measurement or scientific conclusions."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete", action="store_true")
    result = validate(parser.parse_args().complete)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(result["status"] != "PASS")
