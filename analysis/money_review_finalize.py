"""Mechanical consistency update following the documented monetary revision."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):(ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
g=load('analysis/data/argument_graph.json')
if g.get('dependency_direction')=='premise_to_dependent':raise SystemExit('Already finalized; do not silently rebuild.')
changes=[]
for e in g['edges']:
    if e['relation']=='DEPENDS_ON' and e.get('direction')!='premise_to_dependent':
        old=dict(e);e['source'],e['target']=e['target'],e['source'];e['direction']='premise_to_dependent'
        changes.append(dict(old=old,new=dict(e),reason='Unify dependency direction with original convention.'))
removed=[e for e in g['edges'] if (e['source'],e['target']) in [('CPC-0010','CPC-0012'),('CPC-0011','CPC-0005'),('CPC-0069','CPC-0012')]]
g['edges']=[e for e in g['edges'] if e not in removed]
for e in removed:changes.append(dict(old=e,new=None,reason='Replace direct shortcut with conditional scenario.'))
claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
c=next(c for c in claims if c['id']=='CPC-0012');c['depends_on']=['CPC-0011','CPC-0005']
g['edges'].append(dict(source='CPC-0005',target='CPC-0012',relation='DEPENDS_ON',direction='premise_to_dependent',evidence=c['source'],conditions='Money global supposé constant; SC-MONEY-02',interpretive=True))
for e in g['edges']:
    if e['target'] in ['CPC-0005','CPC-0012','CPC-0013','CPC-0014']:
        e['conditions']='Sans création productive de Money, dans le scénario associé; ni neutralité instantanée ni identité suffisante.'
g['dependency_direction']='premise_to_dependent'
save('analysis/data/argument_graph.json',g);save('analysis/data/money_graph_revision_log.json',changes)
(ROOT/'analysis/data/claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
summary=load('analysis/data/money_review_summary.json');summary['graph_edges']=len(g['edges']);save('analysis/data/money_review_summary.json',summary)
qs=load('analysis/data/research_questions.json')
for q in qs:
    if q['chapter']=='CH-02':q['question']='Sous quelles conditions les scénarios compensent-ils les variations de n, et quelles autres variables s’ajustent ?'
save('analysis/data/research_questions.json',qs)
hs=load('analysis/data/hypotheses.json')
for h in hs:
    if h['id']=='HYP-0007':
        h['hypothesis']='Dans le scénario d’émission sans création productive et à l’horizon final, Campergue affirme une compensation inverse de u maintenant Money global constant.'
        h['money_scenarios']=['SC-MONEY-02','SC-MONEY-18','SC-MONEY-19']
        h['incompatible_result']='Variation finale de n.u après mesure indépendante, délai défini préalablement et contrôle des transformations productives; un effet temporaire seul ne réfute pas la proposition.'
        h['revision_note']='Conditionnalisation explicite; statut PROPOSED_NOT_EXECUTED inchangé.'
save('analysis/data/hypotheses.json',hs)
