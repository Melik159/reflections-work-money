"""Append experiment evidence and preserve all previous claim/question records."""
import csv,io,json,shutil
from pathlib import Path
from prepare_fourth_pass import SPECS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions';ARCH=OUT/'history/fourth_pass_before'
def write(path,text):
    p=ROOT/path
    if p.exists():
        b=ARCH/p.relative_to(ROOT);b.parent.mkdir(parents=True,exist_ok=True)
        if not b.exists():shutil.copy2(p,b)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def dump(path,x):write(path,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    if (OUT/'experiments/fourth_pass_integration.json').exists():raise SystemExit('Already integrated; do not overwrite')
    g=json.loads((OUT/'question_graph.json').read_text());h=json.loads((OUT/'history.json').read_text());qs={q['id']:q for q in g['nodes']}
    cs={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    conclusions={
      'EXP-02':'Ordre/égalité/signes restent définis sous recodage croissant commun; différences et ratios numériques exigent des structures distinctes. PDF349 ne requiert pas d’origine absolue si le coefficient covarie; PDF386 exige une échelle de rapport.',
      'EXP-03':'K est stable exactement lorsque la variation pondérée des Ki est nulle, à coefficients fixes. Composition fixe suffit mais n’est pas nécessaire; Ki identiques suffisent pour toute composition. Normalisation exige unité commune ou conversion explicite.',
      'EXP-09':'État E, réserve R et transfert T[a,b] ont des compatibilités locales distinctes. Le transfert signé télescope; cumul positif et réserve ne sont pas la primitive. cp variable exige un terme supplémentaire; aucune mesure indépendante de T.'}
    affected={qid for s in SPECS.values() for qid in s['questions']}
    old={qid:json.loads(json.dumps(qs[qid])) for qid in affected}
    evidence_ids=[]
    for eid,s in SPECS.items():
        for qid in s['questions']:
            q=qs[qid];evid=f'EVID-FOURTH-{eid}-{qid}';evidence_ids.append(evid)
            g['evidence'].append(dict(id=evid,question=qid,claim=None,type='FORMAL',relation='QUALIFIES',source={'artifact':f'research_questions/experiments/{eid}/results.json'},content=conclusions[eid],force='STRONG for stated conditional mathematics; not empirical evidence',limit=s['limitations'],interpretive=True))
            q['evidence'].append(evid);q['fourth_pass']=True;q.setdefault('fourth_pass_experiments',[]).append(eid)
            for filename in ['evidence.md','tests.md','conclusion.md']:
                path=f'research_questions/{qid}/{filename}'
                addition=f'\n## Quatrième passe — {eid}\n\n{conclusions[eid]}\n\nPreuve formelle {evid}, relation QUALIFIES. [Protocole figé](../experiments/{eid}/protocol.md), [résultats et limites](../experiments/{eid}/results.md). Calcul exécuté, non observation de T/Utility/Money.\n\nStatut de la question conservé: {q["status"]}; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.\n'
                write(path,(ROOT/path).read_text()+addition)
    for qid in sorted(affected):
        q=qs[qid];o=old[qid]
        h.append(dict(action='FOURTH_PASS',id=qid,old_status=o['status'],new_status=q['status'],old_statement=o['question'],new_statement=q['question'],old_evidence=o['evidence'],new_evidence=q['evidence'],reason='Local formal experiment; status not automatically upgraded',experiments=q['fourth_pass_experiments'],date='2026-09-08'))
    # Add narrowly linked textual evidence only where already available in the dossiers;
    # numerical experiments do not fabricate new original claims.
    impacts=[]
    for cid in sorted({c for s in SPECS.values() for c in s['claims']}):
        action='UNCHANGED';reason='Original statement and attribution preserved; no new empirical identification.'
        if cid=='CPC-0117':action='REQUIRES_NEW_CONDITION';reason='Stability needs restrictions on coefficients/weights; product count alone insufficient in the reconstructed aggregation.'
        if cid=='CPC-0121':action='QUALIFIED';reason='Balance locally consistent when reserve, state and transfer are separated and signs fixed.'
        if cid=='CPC-0052':action='QUALIFIED';reason='State depends on speed; transfer depends on change and reference. No independent calibration.'
        impacts.append(dict(id=cid,action=action,old_statement=cs[cid]['statement'],new_statement=cs[cid]['statement'],reason=reason,source_unchanged=True,experiments=[eid for eid,s in SPECS.items() if cid in s['claims']],claim_epistemic_status_unchanged=True))
    dump('research_questions/experiments/fourth_pass_claim_impacts.json',impacts)
    dump('research_questions/question_graph.json',g);dump('research_questions/history.json',h)
    with (OUT/'evidence_matrix.csv').open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
    for row in rows:
        qid=row['Question']
        if qid in affected:
            row['Formal evidence']=str(int(row['Formal evidence'])+sum(qid in s['questions'] for s in SPECS.values()))
            row['Tests available']+='; FOURTH_PASS_EXECUTED '+','.join(qs[qid]['fourth_pass_experiments'])
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=fields);w.writeheader();w.writerows(rows);write('research_questions/evidence_matrix.csv',buf.getvalue())
    # Extend the experiment register without relabelling the blocked measurement test.
    p='research_questions/operationalization/experiments.json';exps=json.loads((ROOT/p).read_text());vs={v['id']:v for v in json.loads((OUT/'operationalization/variables.json').read_text())}
    for e in exps:
        if e['id'] in ['EXP-02','EXP-03']:e['fourth_pass_extension']={'protocol':f'research_questions/experiments/{e["id"]}/protocol.md','status':'EXECUTED_FORMAL'}
    s=SPECS['EXP-09'];exps.append(dict(id='EXP-09',question='RQ-03.02',related_questions=['RQ-03.03'],claims=s['claims'],variables=[dict(id=v,name=vs[v]['name'],measurement_level=vs[v]['measurement_level']) for v in s['variables']],data='Synthetic only; source passages',design=s['method'],prediction=s['prediction'],alternative_prediction=s['alternative'],discriminating_power='MEDIUM for local notation; NONE empirical',cost_complexity='Low',feasibility='DO_NOW',execution_status='EXECUTED_FORMAL',measurement_scope='Local formal reconstruction, not execution of EXP-01 measurement',independent_law_test=False))
    dump(p,exps)
    md='research_questions/operationalization/experiments.md';write(md,(ROOT/md).read_text()+'\n## Quatrième passe\n\nEXP-02 et EXP-03 approfondis; nouveau EXP-09 pour comparaison formelle T/dT, DO_NOW, EXECUTED_FORMAL. EXP-01 demeure NEEDS_DEFINITION. [Sélection, niveaux et raisons](../experiments/selection.md). Aucun changement des résultats antérieurs.\n')
    # Operation-level requirements are regression-tested, not inferred from a keyword.
    requirements=[
      dict(id='U-ORDER',formula='UP>UA',source_page=283,operation='ORDER',ordinal_sufficient=True,ratio_scale_required=False,condition='Common agent/context and common increasing recoding'),
      dict(id='U-DIFF',formula='M=rP(UPf−UPi)/(1−gamma)',source_page=349,operation='DIFFERENCE',ordinal_sufficient=False,ratio_scale_required=False,condition='Interval structure; rP covaries; gamma!=1'),
      dict(id='U-RATIO',formula='eta=1−UP2/UP1',source_page=386,operation='RATIO',ordinal_sufficient=False,ratio_scale_required=True,condition='Reversible case; UP1 nonzero; meaningful common origin'),
      dict(id='U-BOUND',formula='eta>=1−UP2/UP1',source_page=385,operation='RATIO',ordinal_sufficient=False,ratio_scale_required=True,condition='Keep inequality and reference/sign convention'),
      dict(id='U-LEVEL',formula='FA p=rP UP',source_page=283,operation='LEVEL_PRODUCT',ordinal_sufficient=False,ratio_scale_required=True,condition='Same multiplicative model, rP fixed across states; inverse scaling of rP under common unit conversion'),
      dict(id='U-DIFFERENTIAL',formula='P dUP',source_page=415,operation='DIFFERENTIAL',ordinal_sufficient=False,ratio_scale_required=False,condition='Numerical differentiable coordinate and covariant conjugate coefficient')]
    dump('research_questions/experiments/EXP-02/operation_requirements.json',requirements)
    bibliography=[dict(id='EXP-BIB-01',title='JCGM VIM3 1.26 Ordinal quantity',year=2012,url='https://jcgm.bipm.org/vim/en/1.26.html',status='VERIFIED',accessed='2026-09-08',role='MEASUREMENT_METHOD',experiments=['EXP-02'],scope='Entry and notes read, not all linked resources',result='Ordinal order distinct from numerical algebraic operations',limit='Does not operationalize Campergue Utility'),dict(id='BIB-0018',title='OpenStax Calculus Volume 3, 6.3 Conservative Vector Fields',url='https://openstax.org/books/calculus-volume-3/pages/6-3-conservative-vector-fields',status='VERIFIED',accessed='2026-09-08',role='MEASUREMENT_METHOD',experiments=['EXP-09'],previously_registered=True,scope='Selected section reconsulted',result='Potential and endpoint difference distinction',limit='Does not establish existence of economic potential')]
    dump('research_questions/experiments/fourth_pass_literature.json',bibliography)
    dump('research_questions/experiments/fourth_pass_integration.json',dict(experiments=list(SPECS),questions=sorted(affected),evidence_ids=evidence_ids,new_claims=0,claim_impacts=len(impacts),question_status_changes=[],coverage_before=272,coverage_after=272,new_empirical_experiments=0,new_literature=1,reused_literature=1,epistemic_scope='Claims, constructions, relations and local models only'))
    p='research_questions/README.md';write(p,(ROOT/p).read_text()+'\n## Quatrième passe — expériences locales\n\n[Rapport](fourth_pass_report.md), [protocoles et sélection](experiments/selection.md). Trois extensions formelles exécutées; quatre questions concernées, statuts conservés. Les affirmations sources ne sont pas effacées. Cadrage: définitions, constructions, relations, principes proposés, analogies, mécanismes et exemples évalués séparément; aucun verdict global.\n')
if __name__=='__main__':main()
