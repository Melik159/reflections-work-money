"""Comparative structure and epistemic separation, not originality certification."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions/contribution'
STATUSES={'KNOWN_EQUIVALENT','KNOWN_WITH_DIFFERENT_TERMINOLOGY','PARTIAL_PARALLEL','RECOMBINATION_OF_KNOWN_CONCEPTS','DISTINCT_DECOMPOSITION','DISTINCT_FORMAL_RESTRICTION','DISTINCT_TESTABLE_PREDICTION','POTENTIALLY_NEW_MEASUREMENT','HISTORICAL_NOVELTY_UNRESOLVED','NO_CLEAR_ADDED_VALUE'}
VALUES={'NONE','LOW','POSSIBLE','MODERATE','HIGH','UNDETERMINED'}
def validate(concepts,cores,sources):
    bysource={s['id']:s for s in sources};assert len(bysource)==len(sources)
    assert len({r['id'] for r in concepts+cores})==len(concepts)+len(cores)
    for r in concepts+cores:
        assert r['contribution_status'] in STATUSES
        assert r['sources'] and all(b in bysource for b in r['sources'])
        assert len(r['value'])==4 and set(r['value'].values())<=VALUES
        if r['originality_asserted']:
            assert r.get('historical_review_complete') and r.get('priority_evidence'),'originality needs historical evidence'
        if r['different_prediction']:assert r.get('prediction_comparison') and r.get('observable_identification')
        if r['kind']=='CONCEPT':
            assert r['campergue_definition'] and r['difference'] and r['lost_on_renaming']
            if r['contribution_status']=='KNOWN_WITH_DIFFERENT_TERMINOLOGY':assert r['substantive_difference']!='YES_IN_SPECIFIED_CONSTRUCTION'
            assert not r['empirical_contribution_established'] or r.get('empirical_evidence')
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    assert {r['id'] for r in cores}=={c for c,x in claims.items() if x['criticality']=='CORE'}
    for r in cores:assert r['source']==claims[r['id']]['source'] and r['what_campergue_claims']==claims[r['id']]['statement']
    return dict(core_compared=len(cores),concepts_compared=len(concepts),sources=len(sources),source_statuses=dict(Counter(s['status'] for s in sources)),originality_asserted=sum(r['originality_asserted'] for r in concepts+cores),status='PASS',warnings=['TARGETED_COMPARISON_NOT_EXHAUSTIVE','HISTORICAL_PRIORITY_UNRESOLVED','ANALYTICAL_VALUE_NOT_BENCHMARKED'])
def main():
    result=validate(json.loads((OUT/'concepts.json').read_text()),json.loads((OUT/'core_comparisons.json').read_text()),json.loads((OUT/'literature.json').read_text()))
    print('CONTRIBUTION REVIEW');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
