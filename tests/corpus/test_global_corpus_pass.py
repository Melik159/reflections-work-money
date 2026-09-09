import copy
import csv
import hashlib
import json
import unittest
from pathlib import Path
from analysis.verify_global_corpus_pass import validate
from analysis.run_global_local_checks import compute,validate as validate_formal

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'analysis/global_corpus_pass'

class GlobalCorpusPassTests(unittest.TestCase):
    def test_562_rows_are_not_562_read_pages(self):
        r=validate();self.assertEqual(r['infrastructure'],'PASS')
        # Negative control remains meaningful after a genuine full scan.
        with (OUT/'page_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        rows[0].update(scan_status='UNREVIEWED',importance='PENDING',questions='')
        with self.assertRaises(AssertionError):validate(rows=rows,require_complete=True)

    def test_missing_or_duplicate_page_fails(self):
        with (OUT/'page_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        with self.assertRaises(AssertionError):validate(rows=rows[:-1])
        rows[-1]=copy.deepcopy(rows[0])
        with self.assertRaises(AssertionError):validate(rows=rows)

    def test_false_complete_certificate_fails(self):
        m=json.loads((OUT/'manifest.json').read_text());m['status']='GLOBAL_CORPUS_PASS_COMPLETE'
        m['formulas_exhaustive']=False
        with self.assertRaises(AssertionError):validate(manifest=m)

    def test_all_core_major_have_records_but_pending_is_honest(self):
        reviews=json.loads((OUT/'claim_rechecks.json').read_text())
        self.assertEqual(sum(r['criticality']=='CORE' for r in reviews),24)
        self.assertEqual(sum(r['criticality']=='MAJOR' for r in reviews),96)
        bad=copy.deepcopy(reviews);bad[0]['full_corpus_reviewed']=False;bad[0]['global_review_status']=None
        with self.assertRaises(AssertionError):validate(rechecks=bad,require_complete=True)

    def test_important_page_needs_question(self):
        with (OUT/'page_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        next(r for r in rows if r['importance']=='STRUCTURAL')['questions']=''
        with self.assertRaises(AssertionError):validate(rows=rows)

    def test_source_and_history_preserved(self):
        baseline=json.loads((OUT/'baseline.json').read_text())
        for item in baseline['artifacts']:
            archived=OUT/'history/baseline'/item['path']
            self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(),item['sha256'])
        # Remediation may add reviewed metadata, never silently alter the frozen claims.
        previous=[json.loads(l) for l in (OUT/'history/baseline/analysis/data/claims.jsonl').read_text().splitlines()]
        current_claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
        self.assertEqual(len(previous),len(current_claims))
        for old,new in zip(previous,current_claims):
            for key,value in old.items():self.assertEqual(new[key],value)
        manifest=json.loads((ROOT/'remediation/applied_changes.json').read_text())
        change=next(r for r in manifest if r['path']=='analysis/data/claims.jsonl')
        self.assertEqual(hashlib.sha256((ROOT/change['path']).read_bytes()).hexdigest(),change['new_sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'Reflections_PierreCampergue.pdf').read_bytes()).hexdigest(),baseline['pdf_sha256'])
        changes=json.loads((OUT/'concept_amendments.json').read_text())
        old={c['id']:c for c in json.loads((OUT/'history/baseline/analysis/data/concepts.json').read_text())}
        current={c['id']:c for c in json.loads((ROOT/'analysis/data/concepts.json').read_text())}
        for change in changes:
            self.assertEqual(old[change['id']][change['field']],change['old_value'])
            self.assertEqual(current[change['id']][change['field']],change['new_value'])
        for cid in old:self.assertEqual(old[cid]['quotations'],current[cid]['quotations'])

    def test_formal_diagnostics_reproduce_and_keep_scope(self):
        result=compute();validate_formal(result)
        self.assertEqual(result,json.loads((OUT/'formal_checks.json').read_text()))
        self.assertEqual(result['type'],'FORMAL_SYNTHETIC_NOT_EMPIRICAL')
        self.assertEqual(result['checks'][3]['result'],'INTERMEDIATE_CONFLICT_FINAL_LOCALLY_RECOVERABLE')

    def test_coverage_is_monotonic_and_has_notes(self):
        old=json.loads((OUT/'history/baseline/analysis/data/page_coverage.json').read_text())
        new=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
        for a,b in zip(old,new):
            if a['examined']:self.assertTrue(b['examined'])
            if b['examined'] and not a['examined']:
                self.assertTrue((ROOT/b['global_pass_note']).exists())
        concepts={c['id']:c for c in json.loads((ROOT/'analysis/data/concepts.json').read_text())}
        self.assertIn('money',concepts['cash']['distinguished_from'])
        self.assertIn('labour',concepts['work']['distinguished_from'])

    def test_complete_review_and_all_formula_occurrences_are_linked(self):
        self.assertEqual(validate(require_complete=True)['scanned'],562)
        formulas=json.loads((OUT/'formulas.json').read_text())
        ids={f['id'] for f in formulas}
        families={f['id'] for f in json.loads((OUT/'formula_families.json').read_text())}
        for item in json.loads((OUT/'formula_candidates.json').read_text()):
            self.assertIn(item['editorial_entry'],ids)
            self.assertIn(item['editorial_family'],families)

    def test_new_formula_fragments_are_source_text_not_invented_latex(self):
        corpus={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
        for f in json.loads((OUT/'formulas.json').read_text()):
            if f['transcription'].startswith('VERBATIM_EXTRACTED'):
                self.assertIn(f['expression'],corpus[f['page']])

    def test_qualifications_and_full_review_history_preserved(self):
        reviews=json.loads((OUT/'claim_rechecks.json').read_text())
        history={r['id']:r for r in json.loads((OUT/'claim_review_history.json').read_text())}
        for r in reviews:
            self.assertTrue(r['full_corpus_reviewed'])
            self.assertEqual(history[r['id']]['new_statement'],r['new_statement'])
            self.assertTrue(history[r['id']]['previous_review'])
        for archive in (OUT/'history').glob('*/archive_manifest.json'):
            for item in json.loads(archive.read_text()):
                path=archive.parent/item['path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),item['sha256'])

    def test_internal_exceptions_cannot_silently_disappear(self):
        findings=json.loads((OUT/'findings.json').read_text())
        pages={p for f in findings for p in f['pages']}
        # Transport productive, assumptions allowed, per-copy domain, gains saved,
        # patent mixed, replacement-only durations, macro K restriction.
        self.assertTrue({159,271,301,382,468,490,498,559}<=pages)
        families={f['id']:f for f in json.loads((OUT/'formula_families.json').read_text())}
        self.assertIn('seulement',families['GF-20']['conditions'])
        self.assertIn('non nulle',families['GF-26']['conditions'])
        self.assertIn('Stocks',families['GF-21']['conditions'])
