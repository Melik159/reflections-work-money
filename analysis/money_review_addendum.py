"""Additional targeted reading after broad candidate screening; explicit append only."""
import copy
import json
from pathlib import Path
from money_review import src, P
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):(ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
r=load('analysis/data/money_compensation_scenarios.json')
if len(r['scenarios'])!=28:raise SystemExit('Addendum already applied or incompatible baseline.')
rows=[
 ('SPEC_UP','Appréciation spéculative de u sans retrait de n',146,"However, it's always possible to cheat momentarily",'Sans Work, n non diminué; spéculation temporaire','Hausse des indices interprétée comme u accru; retour ultérieur obligatoire','Gain transitoire puis crise rétablissant M constant', 'Hausse puis baisse de valorisation convient; hausse fondée sur productivité quitte la condition sans Work; cours des actifs absorbent; assimiler indices boursiers à u reste indéterminé.'),
 ('INTEREST_D','Bouclage par dévaluation',344,'The equality between these two Money','Cycle Money→Work→Money avec pertes et Money dépensé supérieur à Money créé','Dévaluation présentée comme première voie pour restaurer égalité','Égalité recherchée au prix d’une distorsion','Réévaluation des montants peut boucler un compte; contrats indexés peuvent empêcher le résultat; créancier supporte une perte; unité du bilan et périmètre temporel manquent.'),
 ('INTEREST_T','Bouclage par Work supplémentaire pour les intérêts',344,'or by a Work spent in excess','Même cycle; Work dépensé supplémentaire','Seconde voie : davantage de Work, reliée aux possibilités3/4','Surplus productif pour payer les intérêts, voie dite valide','Gain productif réalisable peut financer intérêts; intérêts supérieurs au surplus ne le permettent pas; refinancement/transfert peut absorber; aucune loi empirique de rendement démontrée.'),
 ('RECIP','Non-neutralité réciproque entre acteurs',400,'AN ECONOMIC DECISION IS NEVER NEUTRAL','Consommateur et fournisseur; trois configurations aux tableaux399–400','Money gagné par un acteur associé à Work inverse; configuration opposée et état constant explicités','Décision déclarée non neutre sur Work et Money, sans identité avec neutralité monétaire agrégée','Transfert fermé peut avoir incidence opposée; création productive simultanée interdit de conclure automatiquement au jeu nul; contraintes et efforts absorbent; passage des effets individuels au total reste ouvert.')]
claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
g=load('analysis/data/argument_graph.json');chapters=load('analysis/data/research_chapters.json');ch=next(c for c in chapters if c['id']=='CH-02')
added=[]
for label,name,page,anchor,conditions,mechanism,result,limits in rows:
    s=copy.deepcopy(r['scenarios'][23]);sid=f"SC-MONEY-{len(r['scenarios'])+1:02d}";cid=f'CPC-{len(claims)+1:04d}';q=src(page,anchor)
    pos=P[page].index(q['quotation']);q.update(context_before=P[page][max(0,pos-200):pos],context_after=P[page][pos+len(q['quotation']):pos+len(q['quotation'])+200],argument_function=mechanism)
    s.update(id=sid,author_label=label,name=name,pages=[page],sources=[q],claims=[cid],initial_state=conditions,conditions=conditions,
      applied_change=name,fixed_variables=conditions,adjusted_variables=result,mechanism=mechanism,expected_result=result,exceptions=limits,
      behavioral_assumption=conditions,causal_mechanism=mechanism,derived_consequence=result,relation_to_purchasing_power=result,interpretation=mechanism,fragility=limits)
    parts=limits.split('; ');s['boundary_cases']=dict(works=parts[0],does_not_work=parts[1],other_adjustment=parts[2],indeterminate=parts[3],epistemic_status='ANALYST_HYPOTHETICAL_NOT_EMPIRICAL')
    if label=='RECIP':s['subcases']=['Money consommateur augmente / fournisseur diminue; Work inverse','Money consommateur diminue / fournisseur augmente; Work inverse','Work et Money constants pour les deux acteurs']
    c=copy.deepcopy(claims[-1]);c.update(id=cid,statement=name+' : '+result+', sous les conditions du scénario '+sid+'.',source=q,page=page,quotation=q['quotation'],depends_on=['CPC-0010'],money_scenarios=[sid],interpretation_notes='Lecture ciblée additionnelle; ne pas assimiler incidence individuelle à neutralité globale.')
    claims.append(c);r['scenarios'].append(s);ch['claims'].append(cid);added.append(cid)
    g['nodes'] += [dict(id=cid,kind='HYPOTHESIS'),dict(id=sid,kind='MONETARY_SCENARIO',conditions=conditions)]
    g['edges'] += [dict(source='CPC-0010',target=sid,relation='DEPENDS_ON',direction='premise_to_dependent',evidence=q,conditions=conditions,interpretive=True),dict(source=sid,target=cid,relation='EXEMPLIFIES',evidence=q,conditions=conditions,interpretive=True)]
    text=f'\n## Addendum — {sid} : {name}\n\nClaim : {cid}. SOURCE_TEXT page PDF {page} :\n\n> {q["quotation"]}\n\nA — Identité M=n.u inchangée. B — Conditions : {conditions}.\n\nC — Mécanisme proposé : {mechanism}.\n\nD — Conséquence revendiquée, non validée : {result}.\n\nE — Généralisation : voir périmètre du scénario; pas de neutralité générale déduite.\n\nINTERPRETATION — Cas limites hypothétiques : {limits}\n'
    with (ROOT/'analysis/24_money_compensation_scenarios.md').open('a') as f:f.write(text)
for label,pg,anchor in [('2a',57,'or the prices of Products evolve'),('4a',58,'point N°3 can be summarised'),('4b',57,'either the prices of the Products are constant'),('REDIST',147,'if their own remuneration were to be reduced'),('RECIP',380,'An economic decision acting')]:
    s=next(s for s in r['scenarios'] if s['author_label']==label);q=src(pg,anchor);q.update(context_before='',context_after='',argument_function='Formulation complémentaire à comparer au scénario, sans équivalence causale automatique.');s['sources'].append(q);s['pages']=sorted(set(s['pages']+[pg]))
    with (ROOT/'analysis/24_money_compensation_scenarios.md').open('a') as f:f.write(f'\n### Source complémentaire — {s["id"]}, page {pg}\n\n> {q["quotation"]}\n\n{q["argument_function"]}\n')
save('analysis/data/money_compensation_scenarios.json',r)
(ROOT/'analysis/data/claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
g['money_review']['scenario_ids']=[s['id'] for s in r['scenarios']];save('analysis/data/argument_graph.json',g)
ch['page_ranges'] += [[57,58],[145,147],[343,344],[379,380],[399,400]];save('analysis/data/research_chapters.json',chapters)
(ROOT/'analysis/data/claim_chapter_matrix.csv').write_text('claim_id,chapter_id\n'+''.join(f"{cid},{ch['id']}\n" for ch in chapters for cid in ch['claims']))
cs=load('analysis/data/concepts.json')
for c in cs:c['used_in_claims']=[x['id'] for x in claims if c['id'] in x['concepts']]
save('analysis/data/concepts.json',cs)
coverage=load('analysis/data/page_coverage.json');examined=[57,58,145,146,147,343,344,379,380,399,400]
for row in coverage:
    if row['page'] in examined:row.update(examined=True,reading_note='money_targeted_addendum.md',reason='TARGETED_ANALYTICAL_READING')
    row['claims']=[c['id'] for c in claims if row['page'] in c['source']['pages']]
save('analysis/data/page_coverage.json',coverage)
(ROOT/'analysis/reading_notes/money_targeted_addendum.md').write_text('# Lecture ciblée additionnelle\n\n57–58 : quatre hypothèses n/prix et réduction des cas. 145–147 : ruissellement, spéculation temporaire, chronologie et rémunérations. 343–344 : contraintes, pertes du cycle, dévaluation ou Work supplémentaire et intérêts. 379–380 : équilibre des acteurs, non-neutralité des décisions. 399–400 : trois tableaux réciproques Money/Work, effets opposés et stationnarité. Sources et interprétations dans le rapport24, addendum SC29–32.\n')
state=load('analysis/data/phase2_progress.json');state['pages_examined']=sum(x['examined'] for x in coverage);state['claims']=len(claims);save('analysis/data/phase2_progress.json',state)
summary=load('analysis/data/money_review_summary.json');summary.update(scenarios=len(r['scenarios']),new_claims=len(claims)-68,total_claims=len(claims),coverage=state['pages_examined'],graph_nodes=len(g['nodes']),graph_edges=len(g['edges']));save('analysis/data/money_review_summary.json',summary)
log=load('analysis/data/money_claim_revision_log.json');log['new_claims']+=added;log['addendum_reason']='Additional full-page reading: speculation without n withdrawal, interest closure alternatives and reciprocal non-neutrality.';save('analysis/data/money_claim_revision_log.json',log)
