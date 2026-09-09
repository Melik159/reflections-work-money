"""Infrastructure PASS and honest completeness WARNING are separate outcomes."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'

def read(name):return json.loads((OUT/name).read_text())
def validate(rows=None,manifest=None,rechecks=None,require_complete=False):
    if rows is None:
        with (OUT/'page_matrix.csv').open() as f:rows=list(csv.DictReader(f))
    manifest=read('manifest.json') if manifest is None else manifest
    rechecks=read('claim_rechecks.json') if rechecks is None else rechecks
    assert len(rows)==562 and {int(r['page']) for r in rows}==set(range(1,563)), '562 unique page rows required'
    allowed={'UNREVIEWED','SCANNED','ANALYTICALLY_REVIEWED','DEEP_REVIEWED','SCANNED_NO_STRUCTURAL_CONTENT'}
    graph=json.loads((ROOT/'research_questions/question_graph.json').read_text())
    qids={q['id'] for q in graph['nodes']}
    for q in graph['nodes']:
        if q['id']!='RQ-ROOT':assert q['parent'] in qids
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    count=Counter(r['scan_status'] for r in rows)
    scanned={int(r['page']) for r in rows if r['scan_status']!='UNREVIEWED'}
    for r in rows:
        assert r['scan_status'] in allowed and r['notes']
        if r['scan_status']=='UNREVIEWED':assert not r['questions'] and r['importance']=='PENDING'
        if r['importance']=='STRUCTURAL':assert r['questions'] and int(r['page']) in scanned
        assert set(filter(None,r['questions'].split(';')))<=qids
        assert set(filter(None,r['claims'].split(';')))<=set(claims)
        if int(r['page']) in scanned:
            start=((int(r['page'])-1)//25)*25+1;end=min(start+24,562)
            assert f"## PDF {r['page']} " in (OUT/f'blocks/p{start:03}_p{end:03}.md').read_text()
    assert manifest['pages_scanned']==len(scanned)
    assert manifest['analytical_this_pass']==count['ANALYTICALLY_REVIEWED']+count['DEEP_REVIEWED']
    assert manifest['deep_this_pass']==count['DEEP_REVIEWED']
    assert set(manifest['pending_pages'])==set(range(1,563))-scanned
    assert len(rechecks)==len(claims) and {r['id'] for r in rechecks}==set(claims)
    allowed_claim={'CONFIRMED','QUALIFIED','SPLIT_REQUIRED','MERGE_CANDIDATE','CONTRADICTED_BY_CORPUS','SOURCE_NEEDS_EXTENSION','SOURCE_EXTENDED','REQUIRES_FURTHER_REVIEW',None}
    for r in rechecks:
        assert r['local_review_status'] in allowed_claim
        assert r['global_review_status'] in allowed_claim
        assert set(r['pages_reviewed'])<=scanned
        assert r['old_statement'] and r['reason']
        assert r['new_statement']==claims[r['id']]['statement']
        assert r['source_unchanged']==claims[r['id']]['source']
        if r['full_corpus_reviewed']:assert len(scanned)==562 and r['global_review_status'] is not None
    core=[r for r in rechecks if r['criticality']=='CORE'];major=[r for r in rechecks if r['criticality']=='MAJOR']
    assert len(core)==24 and len(major)==96
    corpus={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    for finding in read('findings.json'):
        assert finding['SOURCE'] and finding['INTERPRETATION']
        s=finding['SOURCE'];assert ' '.join(s['quotation'].split()) in ' '.join(corpus[s['page']].split())
        assert set(finding['pages'])<=scanned
        assert set(finding['questions'])<=qids and set(finding['claims'])<=set(claims)
    formulas=read('formulas.json');assert len({f['id'] for f in formulas})==len(formulas)
    for f in formulas:
        assert f['page'] in scanned and f['conditions'] and f['expression']
        assert f['source_page_sha256']==hashlib.sha256(corpus[f['page']].encode()).hexdigest()
        assert f['id'] in next(r for r in rows if int(r['page'])==f['page'])['formulas'].split(';')
    assert len(read('question_rechecks.json'))==len(graph['nodes'])
    # A complete certificate requires actual review, not simply a 562-row file.
    complete=(len(scanned)==562 and manifest['formulas_exhaustive']
              and all(r['full_corpus_reviewed'] and r['global_review_status'] for r in core+major)
              and all(q['full_corpus_coverage_verified'] for q in read('question_rechecks.json')))
    if require_complete or manifest['status']=='GLOBAL_CORPUS_PASS_COMPLETE' or manifest['ready_for_synthesis']:
        assert complete, 'Full-corpus certificate not earned'
        families=read('formula_families.json');family_ids={f['id'] for f in families}
        formula_ids={f['id'] for f in formulas}
        for candidate in read('formula_candidates.json'):
            assert candidate['editorial_entry'] in formula_ids
            assert candidate['editorial_family'] in family_ids
        history=read('claim_review_history.json')
        assert {r['id'] for r in history}==set(claims)
        assert all(r['previous_review'] and r['reason'] and r['new_sources'] for r in history)
        assert {q['id'] for q in read('question_rechecks.json')}==qids
    return dict(infrastructure='PASS',scientific_status=manifest['status'],scanned=len(scanned),
        pending=562-len(scanned),core_local=sum(r['local_review_status'] is not None for r in core),
        major_local=sum(r['local_review_status'] is not None for r in major),
        core_global=sum(r['full_corpus_reviewed'] for r in core),major_global=sum(r['full_corpus_reviewed'] for r in major),
        warning=None if complete else 'GLOBAL_CORPUS_CONSOLIDATION_IN_PROGRESS')

if __name__=='__main__':
    print('GLOBAL CORPUS PASS');print(json.dumps(validate(),ensure_ascii=False,indent=2))
