"""Structural and provenance checks; scientific OPEN remains a warning."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions/synthesis'
ALLOWED_CORE={'DEFINITIONAL','FORMALLY_DERIVED','ASSUMPTION_DEPENDENT','EMPIRICALLY_COMPATIBLE',
 'EMPIRICALLY_SUPPORTED_WITHIN_SCOPE','EMPIRICALLY_QUALIFIED','NON_DISCRIMINATING','NOT_IDENTIFIED',
 'AMBIGUOUS','CONTRADICTED_WITHIN_SCOPE'}

def load(name):return json.loads((OUT/name).read_text())

def validate(questions=None,cores=None,results=None,candidates=None,manifest=None,check_hashes=True):
    questions=load('questions.json') if questions is None else questions
    cores=load('core_claims.json') if cores is None else cores
    results=load('results.json') if results is None else results
    candidates=load('contributions.json') if candidates is None else candidates
    manifest=load('manifest.json') if manifest is None else manifest
    graph=json.loads((ROOT/'research_questions/question_graph.json').read_text())
    nodes={n['id']:n for n in graph['nodes'] if n['id']!='RQ-ROOT'}
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    rechecks={c['id']:c for c in json.loads((ROOT/'analysis/global_corpus_pass/claim_rechecks.json').read_text())}
    literature={b['id']:b for b in load('literature.json')}
    assert len(questions)==53 and {q['id'] for q in questions}==set(nodes)
    assert len(cores)==24 and {c['id'] for c in cores}=={c['id'] for c in claims.values() if c['criticality']=='CORE'}
    assert len(results)==14 and len({r['id'] for r in results})==14
    assert len(candidates)==4 and len({r['id'] for r in candidates})==4
    for item in questions+cores+results+candidates:
        assert not item.get('global_validation',False),'No global validation certificate'
        assert item['status'] and item['confidence'] in {'LOW','MEDIUM','HIGH'}
        for field in ['internal_coherence','external_compatibility','distinctive_explanation','epistemic_kind']:
            assert item[field],(item['id'],field)
        assert item.get('claims',[item.get('id')]),item['id']
        for cid in item.get('claims',[item.get('id')]):assert cid in claims,cid
        for qid in item.get('questions',[item.get('id')]):assert qid in nodes,qid
        paths=item.get('sources',item.get('source_artifacts',[]))
        assert paths,('Missing provenance',item['id'])
        for p in paths:assert (ROOT/p).is_file(),p
        for bid in item.get('literature',[]):assert bid in literature,bid
    for q in questions:
        assert q['status']==nodes[q['id']]['status'],'No silent promotion of question status'
        assert q['claims']==nodes[q['id']]['claims']
        assert q['main_corpus_answer'] and q['counterevidence'] and q['remaining_uncertainty'] and q['root_question_impact']
        assert q['epistemic_kind']=='INTERPRETATION'
    for c in cores:
        assert c['source']==claims[c['id']]['source'],'Canonical quotation must survive unchanged'
        assert c['statement']==claims[c['id']]['statement']
        assert c['global_review_status']==rechecks[c['id']]['global_review_status']
        assert c['global_qualification']==rechecks[c['id']]['reason']
        assert set(c['status'])<=ALLOWED_CORE
        assert c['literature'] and c['objections']
    for c in candidates:
        assert c['literature'] and c['source_pages'] and c['current_evidence'] and c['limit']
        assert c['historical_novelty_status']=='HISTORICAL_NOVELTY_UNRESOLVED'
        assert c['originality_asserted'] is False
        assert c['different_testable_prediction_established'] is False
        assert c['new_measurement_established'] is False
    assert manifest['global_validation'] is False
    assert manifest['questions']==53 and manifest['core_claims']==24
    assert manifest['source_root_question_pages']==[2,3]
    assert manifest['question_statuses']==dict(Counter(q['status'] for q in questions))
    assert manifest['core_classification_counts']==dict(Counter(s for c in cores for s in c['status']))
    assert manifest['classification_counts_are_nonexclusive'] is True
    assert manifest['source_sha256']=='7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827'
    assert manifest['source_sha256']==hashlib.sha256((ROOT/'Reflections_PierreCampergue.pdf').read_bytes()).hexdigest()
    assert manifest['scientific_status_changes']==[] and manifest['canonical_claim_changes']==[]
    if check_hashes:
        for record in load('input_manifest.json'):
            assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256'],('Synthesis input changed; explicit review required',record['path'])
    root_answer=(OUT/'root_question_answer.md').read_text()
    assert claims['CPC-0001']['source']['quotation'] in root_answer
    assert 'This essay should only be understood as a proposed answer to this question.' in root_answer
    assert 'CPC-0001' in root_answer and 'RQ-12.01' in root_answer
    for h in ['WHAT_CAMPERGUE_PROPOSES','WHAT_IS_WELL_RECONSTRUCTED','WHAT_IS_FORMALLY_SUPPORTED',
        'WHAT_IS_EMPIRICALLY_COMPATIBLE','WHAT_IS_EMPIRICALLY_SUPPORTED_WITHIN_SCOPE','WHAT_REMAINS_UNMEASURED',
        'WHAT_IS_AMBIGUOUS','WHAT_IS_QUALIFIED_OR_WEAKENED','WHAT_ALTERNATIVE_EXPLANATIONS_EXIST','PROVISIONAL_ANSWER','CONFIDENCE']:
        assert '## '+h in root_answer
    chain=load('root_question_chain.json')
    assert len(chain)==11 and sum('MISSING' in x['status'] for x in chain)==2
    for x in chain:
        assert x['qualification'] and x['causal_identification']=='NOT_IDENTIFIED'
        assert (ROOT/x['source']).is_file()
    with (OUT/'master_matrix.csv').open() as f:matrix=list(csv.DictReader(f))
    assert len(matrix)==95 and len({r['Item'] for r in matrix})==95
    assert {r['Item'] for r in matrix}=={r['id'] for r in questions+cores+results+candidates}
    for r in matrix:
        for k,v in r.items():assert v,('Empty master cell',r['Item'],k)
    with (OUT/'question_synthesis.csv').open() as f:qcsv=list(csv.DictReader(f))
    assert {q['id'] for q in qcsv}==set(nodes) and len(qcsv)==53
    for q,r in zip(questions,qcsv):
        for k in ['id','status','confidence','main_corpus_answer','formal_status','empirical_status']:
            assert q[k]==r[k],('CSV mismatch',q['id'],k)
    report=(OUT/'final_synthesis.md').read_text()
    assert len(re.findall(r'^## \d+\. ',report,re.M))==22
    for phrase in ['LEVEL A','LEVEL B','LEVEL C']:assert phrase in (OUT/'minimal_model.md').read_text()
    for phrase in ['the framework is globally validated','le système est globalement validé','la théorie est validée']:
        assert phrase not in report.lower()
    # Markdown local links: provenance must be navigable, not merely nonempty strings.
    for p in OUT.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('http://','https://','#')):continue
            target=target.split('#')[0]
            assert (p.parent/target).exists(),('Broken link',p.name,target)
    return dict(status='PASS',questions=53,core_claims=24,master_items=95,
       question_statuses=dict(Counter(q['status'] for q in questions)),
       warnings=['SCIENTIFIC_QUESTIONS_OPEN','MEASUREMENT_INCOMPLETE','LITERATURE_PARTIAL','CAUSAL_IDENTIFICATION_NOT_ESTABLISHED'],
       interpretation='Infrastructure and provenance check, not scientific validation.')

if __name__=='__main__':
    print('SYNTHESIS')
    print(json.dumps(validate(),ensure_ascii=False))
