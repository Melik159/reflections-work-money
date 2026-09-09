"""Research-tree structure only: open research is a warning, not failure."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions'
STATUS={'OPEN','PARTIALLY_RESOLVED','RESOLVED_WITHIN_SCOPE','AMBIGUOUS','CONTRADICTED','NOT_TESTABLE'}
RELATIONS={'DEPENDS_ON','PART_OF','SUPPORTS','REQUIRES','TESTS','ANSWERS'}

def validate(g):
    nodes=g['nodes'];ids=[q['id'] for q in nodes];assert len(ids)==len(set(ids)),'duplicate question ID'
    byid={q['id']:q for q in nodes};assert 'RQ-ROOT' in byid
    evidence={e['id']:e for e in g['evidence']};assert len(evidence)==len(g['evidence'])
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    chapters={c['id'] for c in json.loads((ROOT/'analysis/data/research_chapters.json').read_text())}
    for q in nodes:
        assert q['status'] in STATUS
        assert q['parent'] is None if q['id']=='RQ-ROOT' else q['parent'] in byid
        assert all(d in byid and d!=q['id'] for d in q['dependencies'])
        assert q['claims'] and all(c in claims for c in q['claims'])
        assert q['chapters'] and set(q['chapters'])<=chapters
        assert q['scope'] and q['out_of_scope'] and q['interpretive']
        assert q['evidence'] and all(e in evidence and evidence[e]['question']==q['id'] for e in q['evidence'])
        if q['status']=='RESOLVED_WITHIN_SCOPE':assert q['scope_of_resolution'] and q['evidence']
        if q['status']=='CONTRADICTED':
            assert any(evidence[e]['relation']=='CONTRADICTS' for e in q['evidence']),'contradiction needs counterevidence'
        for b in q['literature']:assert b['id']==b['source']['id'] and b['source']['url'] and b['question']==q['id']
    for e in g['evidence']:
        assert e['question'] in byid
        assert e['type'] in {'FORMAL','TEXTUAL','EMPIRICAL','HISTORICAL','LOGICAL','COUNTEREXAMPLE'}
        assert e['relation'] in {'SUPPORTS','PARTIALLY_SUPPORTS','QUALIFIES','CONTRADICTS','DOES_NOT_DECIDE'}
        assert e['force'] and e['limit']
        if e['type']=='TEXTUAL' and e.get('direct_corpus'):
            pages={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
            s=e['source'];assert s['document']=='Reflections_PierreCampergue.pdf'
            assert s['quotation'] and s['quotation'] in ' '.join(pages[s['page']].split()),'direct quotation not on source page'
        elif e['type']=='TEXTUAL':assert e['source']==claims[e['claim']]['source'],'altered or invented source'
        else:assert (ROOT/e['source']['artifact']).is_file()
    for e in g['edges']:
        assert e['source'] in byid and e['target'] in byid and e['relation'] in RELATIONS
    for relation in ['DEPENDS_ON','PART_OF']:
        seen=set();active=set();adj={id:[] for id in ids}
        for e in g['edges']:
            if e['relation']==relation:adj[e['source']].append(e['target'])
        def visit(id):
            assert id not in active,'cycle in '+relation
            if id in seen:return
            active.add(id)
            for target in adj[id]:visit(target)
            active.remove(id);seen.add(id)
        for id in ids:visit(id)
        for q in nodes:
            expected=q['dependencies'] if relation=='DEPENDS_ON' else [q['parent']] if q['parent'] else []
            assert sorted(adj[q['id']])==sorted(expected),'edge/list mismatch'
    covered={c for q in nodes if q['level']==2 for c in q['claims']}
    core={c for c in claims if claims[c]['criticality']=='CORE'}
    major={c for c in claims if claims[c]['criticality']=='MAJOR'}
    assert core<=covered,'orphan CORE claim'
    qs=[q for q in nodes if q['id']!='RQ-ROOT'];status=Counter(q['status'] for q in qs)
    return dict(status='PASS',questions=len(qs),root_count=1,level1=sum(q['level']==1 for q in qs),level2plus=sum(q['level']>=2 for q in qs),
        core_covered=len(core&covered),core_total=len(core),major_covered=len(major&covered),major_total=len(major),
        orphan_core_claims=sorted(core-covered),orphan_major_claims=sorted(major-covered),orphan_research_questions=[],
        classifications=dict(Counter(t for q in qs for t in q['classification'])),statuses=dict(status),
        with_evidence=sum(bool(q['evidence']) for q in qs),with_literature=sum(bool(q['literature']) for q in qs),
        distinct_literature=len({b['id'] for q in qs for b in q['literature']}),first_pass=sum(q['first_pass'] for q in qs),
        second_pass=sum(q.get('second_pass',False) for q in qs),resolved=status['RESOLVED_WITHIN_SCOPE'],open=status['OPEN'],warnings=['RESEARCH_IN_PROGRESS','TARGETED_CORPUS_NOT_EXHAUSTIVE','INITIAL_TEST_DESIGNS_PARTIAL'])

def main():
    g=json.loads((OUT/'question_graph.json').read_text());r=validate(g)
    print('RESEARCH QUESTION TREE')
    print(json.dumps(r,ensure_ascii=False,indent=2))
    if (OUT/'operationalization/variables.json').exists():
        variables=json.loads((OUT/'operationalization/variables.json').read_text())
        print('MEASUREMENT MAP',json.dumps(dict(third_pass=sum(q.get('third_pass',False) for q in g['nodes']),variables=len(variables),levels=dict(Counter(v['measurement_level'] for v in variables))),ensure_ascii=False))
    print('PASS: question-tree structure; WARNING: unresolved research is not an infrastructure failure')
if __name__=='__main__':main()
