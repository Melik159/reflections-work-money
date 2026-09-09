"""Versioned, one-time integration of a targeted metrology pass; no empirical fitting."""
import csv, io, json, math, shutil
from collections import Counter
from pathlib import Path
from third_pass_catalog import ROWS, REVIEWS, TARGETS, LITERATURE
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions'; MET=OUT/'operationalization'
ARCH=OUT/'history/third_pass_before'
def write(path,text):
    path=ROOT/path
    if path.exists():
        backup=ARCH/path.relative_to(ROOT)
        backup.parent.mkdir(parents=True,exist_ok=True)
        if not backup.exists():shutil.copy2(path,backup)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
def dump(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in row)+' |\n' for row in rows)
def csvwrite(path,headers,rows):
    f=io.StringIO();w=csv.writer(f);w.writerow(headers);w.writerows(rows);write(path,f.getvalue())
def main():
    if (MET/'manifest.json').exists():raise SystemExit('Already integrated; do not overwrite an existing research pass.')
    g=json.loads((OUT/'question_graph.json').read_text());byid={q['id']:q for q in g['nodes']}
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    pages={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    variables=[]
    for i,row in enumerate(ROWS,1):
        name,definition,ps,formula,unit,dim,kind,scale,status,level,proxy,assumptions=row
        deps=[qid for qid,d in REVIEWS.items() if set(ps)&set(d['pages'])]
        variables.append(dict(id=f'VAR-{i:02}',name=name,definition_by_campergue=definition,definition_is_interpretation=True,
            source_document='Reflections_PierreCampergue.pdf',pages=ps,formulas=[formula],source_unit=unit,
            dimension=dim,dimension_is_analyst_inference=True,level_or_change=kind,scale=scale,
            measurement_status=status,measurement_level=level,directly_observable=status=='DIRECTLY_OBSERVABLE',
            proxy_or_procedure=proxy,proxy_explicit=('PROXY' in proxy or status=='PROXY_ONLY'),
            necessary_data=proxy,necessary_assumptions=assumptions,ambiguities=assumptions,
            dependent_questions=deps,empirical_measurement_claimed=level>=4,
            available_data_artifact='analysis/empirical/independent_energy/results.json' if name=='energy' else None,
            maturity_scope='Target quantity, not maturity of a substitute proxy; L3 is a procedure, not collected data.'))
    dump('research_questions/operationalization/variables.json',variables)
    levels=['NOT DEFINED WELL ENOUGH','CONCEPTUALLY DEFINED','PROXY AVAILABLE','OPERATIONAL DEFINITION','INDEPENDENT MEASUREMENT AVAILABLE','REPEATED/REPLICABLE MEASUREMENT AVAILABLE']
    intro='# Carte des variables — troisième passe\n\nStatuts métrologiques provisoires, pas verdicts théoriques. Les définitions ci-dessous sont INTERPRETATION reliée aux pages; citations dans les dossiers. Une procédure L3 n’est pas une collecte réalisée. L5 énergie décrit les séries physiques archivées, pas leur équivalence à T. Alias ω/productivity et cp/complexity ne sont pas observations indépendantes.\n\n'+''.join(f'- LEVEL {i} — {s}\n' for i,s in enumerate(levels))+'\n'
    write('research_questions/operationalization/variables.md',intro+table(['ID','Variable','Statut','Niveau','Pages','Proxy ou procédure','Condition'],[(v['id'],v['name'],v['measurement_status'],v['measurement_level'],v['pages'],v['proxy_or_procedure'],v['necessary_assumptions']) for v in variables]))
    csvwrite('research_questions/operationalization/measurement_matrix.csv',['VARIABLE_ID','Variable','Status','Level','Unit','Dimension','Level_or_change','Scale','Pages','Proxy_or_procedure','Assumptions','Questions'],[(v['id'],v['name'],v['measurement_status'],v['measurement_level'],v['source_unit'],v['dimension'],v['level_or_change'],v['scale'],v['pages'],v['proxy_or_procedure'],v['necessary_assumptions'],';'.join(v['dependent_questions'])) for v in variables])
    for b in LITERATURE:b.update(status='VERIFIED',verification_scope='Selected official web entry read, not linked materials',accessed='2026-09-08')
    dump('research_questions/operationalization/measurement_literature.json',LITERATURE)
    write('research_questions/operationalization/literature.md','# Littérature métrologique ciblée\n\nIdentifiants MET-BIB stables, registre spécialisé distinct de BIB-XXXX; aucune nouvelle source inventée ni DOI inféré.\n\n'+''.join(f"## {b['id']} — {b['title']}\n\n{b['author']}; {b['year'] or 'page non datée'}. [{b['title']}]({b['url']}). VERIFIED: entrée sélectionnée, consultée le 2026-09-08.\n\n{b['role']}: {b['result']}\n\nLimite: {b['limit']}\n\n" for b in LITERATURE))
    history=json.loads((OUT/'history.json').read_text());changes=[]
    # Re-read pages in this turn; old coverage preserved. No keyword hit counted alone.
    read_pages=[108,109,189,190,191,192,200,207,385,386,387,388,389,390,391,455,559]
    coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text());before=sum(p['examined'] for p in coverage)
    newpages=[p['page'] for p in coverage if p['page'] in read_pages and not p['examined']]
    note='third_pass_metrology.md'
    write('analysis/reading_notes/'+note,'# Lecture métrologique dirigée\n\nPages relues intégralement: '+str(read_pages)+'. Nouvelles pages couvertes: '+str(newpages)+'.\n\n108–109: Utility non additive, mesure explicitement absente, classement proposé. 189–192: utilité subjective et contextuelle, Cash, agents. 200: variations de vitesses, approximation continue. 207: substitution des Forces puis intégration à constante zéro. 385–391: rendements signés, réversibilité, produit des rendements, angle imposé π/8, cas isopheles. 455: pont physique/économique conditionné à Utility. 559: K local puis stabilité agrégée alléguée.\n\nInterprétation: calculabilité conditionnelle ne fournit pas un étalon indépendant. Les cas limites de rendement exigent des conditions supplémentaires; aucune dérivée libre ne suffit à établir l’optimum contraint du manuscrit.\n')
    for p in coverage:
        if p['page'] in newpages:p.update(examined=True,reading_note=note,reason='TARGETED_METROLOGY_READING')
    dump('analysis/data/page_coverage.json',coverage)
    progress=json.loads((ROOT/'analysis/data/phase2_progress.json').read_text());progress['pages_examined']=sum(p['examined'] for p in coverage);progress['third_question_pass']='Targeted conceptual metrology; no global verdict';dump('analysis/data/phase2_progress.json',progress)
    for qid,d in REVIEWS.items():
        q=byid[qid];oldstatus=q['status'];old_evidence=list(q['evidence'])
        if qid in ['RQ-01.03','RQ-04.04']:q['status']='PARTIALLY_RESOLVED'
        q['third_pass']=True;q['measurement_variables']=[v['id'] for v in variables if qid in v['dependent_questions']]
        q['metrology_conclusion']=d['result'];q['metrology_limit']=d['limit'];q['metrology_literature']=[b['id'] for b in LITERATURE if b['id'] in (['MET-BIB-01','MET-BIB-02']+(['MET-BIB-03'] if qid in ['RQ-05.03','RQ-05.01'] else [])+(['MET-BIB-04'] if qid=='RQ-01.03' else []))]
        q['metrology_confidence']={'TEXTUAL_CONFIDENCE':'HIGH' if qid=='RQ-05.03' else 'MEDIUM','FORMAL_CONFIDENCE':'MEDIUM','EMPIRICAL_CONFIDENCE':'LOW','LITERATURE_CONFIDENCE':'MEDIUM'}
        artifact=f'research_questions/{qid}/metrology.md'
        text=f"# {qid} — Opérationnalisation\n\n## Périmètre\n\n{q['question']}\n\nLecture ciblée et réemploi des dossiers antérieurs; pas inventaire exhaustif du manuscrit. Dépendances conservées: {', '.join(q['dependencies'])}.\n\n## SOURCE_FORMALISM\n\nPages: {d['pages']}. Extraits des claims associés dans corpus.md; retour direct aux pages pour les nouvelles citations ci-dessous.\n\n## MINIMAL_RECONSTRUCTION\n\n{d['result']}\n\n## Conditions, exceptions et contre-épreuve\n\n{d['limit']}\n\n## Mesure et test\n\n{d['test']}\n\nDESIGNED_NOT_EXECUTED, sauf diagnostics formels explicitement consignés dans operationalization/formal_results.json.\n\n## Conclusion provisoire\n\n{q['status']}; confiance métrologique MEDIUM, empirique LOW. Aucune impossibilité universelle ni validation globale affirmée.\n\n## Littérature\n\n{', '.join(q['metrology_literature'])}: voir [registre métrologique](../operationalization/literature.md). Les méthodes externes ne mesurent pas automatiquement les concepts Campergue.\n"
        write(artifact,text)
        eid='EVID-METROLOGY-'+qid
        g['evidence'].append(dict(id=eid,question=qid,claim=None,type='LOGICAL',relation='QUALIFIES',source={'artifact':artifact},content=d['result'],force='MODERATE',limit=d['limit'],interpretive=True))
        q['evidence'].append(eid)
        for filename in ['README.md','evidence.md','tests.md','literature.md','conclusion.md']:
            path=OUT/qid/filename;old=path.read_text()
            if filename=='conclusion.md':old=old.replace('## STATUS\n\n'+oldstatus,'## STATUS\n\n'+q['status'])
            if filename=='README.md' and oldstatus!=q['status']:old=old.replace('\n'+oldstatus+'\n','\n'+q['status']+'\n')
            write(path.relative_to(ROOT),old+f'\n## Troisième passe — métrologie\n\nVoir [dossier métrologique](metrology.md). {d["result"]}\n\nLimite: {d["limit"]}\n\nStatut actuel: {q["status"]}. Test proposé: {d["test"]}\n')
        # Preserve old history; new event records full current evidence and scope.
        change=dict(action='THIRD_PASS',id=qid,old_status=oldstatus,new_status=q['status'],old_statement=q['question'],new_statement=q['question'],old_evidence=old_evidence,new_evidence=q['evidence'],reason=d['result'],scope='METROLOGY_ONLY',date='2026-09-08')
        history.append(change);changes.append(change)
    # Explicit p109 admission, whitespace-normalized verbatim with machine provenance.
    quote="If it's possible to measure need, the same cannot be said for Utility."
    assert quote in ' '.join(pages[109].split())
    q=byid['RQ-05.03'];eid='EVID-METROLOGY-UTILITY-P109'
    g['evidence'].append(dict(id=eid,question=q['id'],claim=None,type='TEXTUAL',direct_corpus=True,relation='SUPPORTS',source={'document':'Reflections_PierreCampergue.pdf','page':109,'quotation':quote},content='Absence de mesure explicitement reconnue, sans interdire mesure future.',force='STRONG for textual reconstruction',limit='Ne démontre pas impossibilité; classement proposé ensuite.',interpretive=True));q['evidence'].append(eid)
    history[-1:] # no history rewriting; references in new event share the evidence list.
    cp=OUT/'RQ-05.03/corpus.md'
    write(cp.relative_to(ROOT),cp.read_text()+f'\n## SOURCE-MET-109 — PRIMARY\n\n### SOURCE\n\nReflections_PierreCampergue.pdf, page PDF109.\n\n> {quote}\n\nContexte: analogie de la mesure historique de température; classement des Products proposé dans le même paragraphe.\n\n### INTERPRETATION\n\nL’absence de mesure n’est pas seulement une réserve de l’analyste: elle est reconnue ici par le manuscrit. Cela ne fournit pas de ratios cardinaux de Utility.\n')
    dump('research_questions/question_graph.json',g);dump('research_questions/history.json',history)
    qmd=(OUT/'questions.md').read_text();write('research_questions/questions.md',qmd+'\n## Passe métrologique — 2026-09-08\n\n'+table(['Question','Statut courant','Conclusion'],[(i,byid[i]['status'],REVIEWS[i]['result']) for i in TARGETS])+'\nAucun ID ou lien de dépendance changé. Les entrées ci-dessus actualisent les statuts historiques précédents.\n')
    # Update statuses in earlier table lines, preserving archive.
    qmd=(OUT/'questions.md').read_text().splitlines()
    for j,line in enumerate(qmd):
        for c in changes:
            if c['id'] in line and c['old_status']!=c['new_status']:qmd[j]=qmd[j].replace(c['old_status'],c['new_status'])
    write('research_questions/questions.md','\n'.join(qmd)+'\n')
    with (OUT/'evidence_matrix.csv').open() as f:reader=csv.DictReader(f);headers=reader.fieldnames;matrix=list(reader)
    for r in matrix:
        if r['Question'] in TARGETS:
            q=byid[r['Question']];r['Status']=q['status'];r['Tests available']='METROLOGY_DESIGNED; FORMAL_DIAGNOSTICS_AVAILABLE';r['Confidence']=q['confidence']
            if q['id']=='RQ-05.03':r['Corpus evidence']=str(int(r['Corpus evidence'])+1)
    # Separate specialist literature column: don't inflate centrally registered bibliographic count.
    headers=headers+['Metrology evidence','Measurement literature']
    for r in matrix:r['Metrology evidence']=int(r['Question'] in TARGETS);r['Measurement literature']=len(byid[r['Question']].get('metrology_literature',[]))
    csvwrite('research_questions/evidence_matrix.csv',headers,[[r[h] for h in headers] for r in matrix])
    dump('research_questions/operationalization/manifest.json',dict(status='TARGETED_PASS_COMPLETE_WITH_LIMITS',questions=TARGETS,variables=len(variables),measurement_levels=dict(Counter(v['measurement_level'] for v in variables)),pages_read=read_pages,new_pages=newpages,coverage_before=before,coverage_after=progress['pages_examined'],new_claims=0,new_literature=len(LITERATURE),status_changes=changes,global_verdict=None))
if __name__=='__main__':main()
