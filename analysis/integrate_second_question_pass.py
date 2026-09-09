"""Apply reviewed records with exact old-file archives and explicit history.
No claim or original PDF is modified. Re-running after completion is read-only.
"""
import csv
import hashlib
import io
import json
import re
import shutil
from pathlib import Path
from second_pass_catalog import REVIEWS,ORDER,NEW_SOURCES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions'
ARCH=OUT/'history/second_pass_before'
READ=[207,208,210,413,414,415,422,536,537,548,553,554,255,256,257,468,471,426,427,429,108,222,307,309,180,273,43,18,68,69,112,113,138,157,163,165,217,225,275,284,459,460,522]
def write(path,text):
    if path.exists():
        if path.read_bytes()==text.encode():return
        old=ARCH/path.relative_to(ROOT);old.parent.mkdir(parents=True,exist_ok=True)
        if not old.exists():shutil.copy2(path,old)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
def dump(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def table(path,head,rows):
    s=io.StringIO();w=csv.writer(s);w.writerow(head);w.writerows(rows);write(path,s.getvalue())
def main():
    marker=OUT/'second_pass_manifest.json'
    if marker.exists():
        print('Second pass already integrated. Explicit new version required for further changes.');return
    g=json.loads((OUT/'question_graph.json').read_text());by={q['id']:q for q in g['nodes']}
    history=json.loads((OUT/'history.json').read_text())
    pages={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    normal=lambda s:' '.join(s.split())
    oldlib=json.loads((ROOT/'analysis/data/literature_map.json').read_text())['sources'];lib={s['id']:s for s in oldlib}
    new=[]
    for num,authors,year,title,url,doi,status,access in NEW_SOURCES:
        id=f'BIB-{num:04}';assert id not in lib
        s=dict(id=id,authors=authors,year=year,title=title,url=url,doi=doi,status=status,access=access,
               locator=access,verification='Targeted primary page or institutional index inspected during second pass; access extent explicit.')
        lib[id]=s;new.append(s)
    used=sorted({f'BIB-{n:04}' for r in REVIEWS.values() for n in r['bib']})
    dump(OUT/'second_pass_literature.json',dict(sources=[lib[id] for id in used],new_ids=[s['id'] for s in new],
        limitations=['Reused sources retain earlier access limitations.','Wiedmann direct page JS blocked; indexed metadata/abstract only.',
                    'NBER detailed theorems not read; comparison methodological.', 'No DOI inferred from a title.']))
    bib=''
    for s in new:
        bib+='@misc{'+s['id']+',\n  author = {'+s['authors']+'},\n  title = {'+s['title']+'},\n  year = {'+str(s['year'])+'},\n  url = {'+s['url']+'},\n'
        if s['doi']:bib+='  doi = {'+s['doi']+'},\n'
        bib+='  note = {'+s['status']+'; '+s['access']+'}\n}\n\n'
    write(ROOT/'bibliography/second_pass_research.bib',bib)
    direct=[]
    for id in ORDER:
        q=by[id];r=REVIEWS[id];oldstatus=q['status'];folder=OUT/id
        records=[]
        for i,(page,needle) in enumerate(r['sources'],1):
            t=normal(pages[page]);start=t.find(needle);assert start>=0,(id,page,needle)
            end=t.find('. ',start+len(needle));end=min(len(t),start+550) if end<0 else end+1
            # A source may contain a short complete fragment; context remains separate.
            s=dict(id=f'SOURCE-{id}-{i:02}',document='Reflections_PierreCampergue.pdf',page=page,pages=[page],
                quotation=t[start:end],context_before=t[max(0,start-240):start],context_after=t[end:end+240],
                normalization='whitespace only',classification='PRIMARY',claims=q['claims'],
                importance='Evidence for the reconstruction below; not proof of empirical truth.')
            records.append(s);direct.append(dict(question=id,**s))
        corpus=(folder/'corpus.md').read_text()+'\n## Deuxième passe — sources directement relues\n\nRecherche BM25 conservée dans second_pass_retrieval.json ; pages exactes inspectées ensuite. Couverture ciblée, non garantie exhaustive.\n\n'
        for s in records:
            corpus+='### '+s['id']+' — '+s['classification']+'\n\nSOURCE — '+s['document']+', page PDF'+str(s['page'])+' :\n\n> '+s['quotation']+'\n\nContexte avant : '+s['context_before']+'\n\nContexte après : '+s['context_after']+'\n\nClaims liés (pertinence, non équivalence phrase/claim) : '+', '.join(s['claims'])+'.\n\nImportance : '+s['importance']+'\n\nINTERPRETATION : '+r['result']+'\n\n'
        write(folder/'corpus.md',corpus)
        reconstruction='# '+id+' — reconstruction avant critique\n\nSOURCE_FORMALISM : les citations et équations restent dans corpus.md et les tables dédiées ; le texte ci-dessous est une reconstruction analytique.\n\n'
        for key in ['premises','definitions','mechanism','derivation','conditions','exceptions','result','domain']:
            title='CLAIMED_RESULT / RECONSTRUCTED_RESULT' if key=='result' else key.upper()
            reconstruction+='## '+title+'\n\n'+r[key]+'\n\n'
        reconstruction+='## INTERNAL REVIEW — après reconstruction\n\n'+r['issue']+'\n\nContre-épreuve : '+r['counter']+'\n\nPour augmenter la confiance : '+r['missing']+'\n'
        write(folder/'reconstruction.md',reconstruction)
        # Direct corpus evidence has a separate validation route from copied claim evidence.
        for i,s in enumerate(records,1):
            eid=f'EVID-SUPPORT-{id}-{i:02}'
            ev=dict(id=eid,question=id,claim=None,type='TEXTUAL',relation='SUPPORTS',source=s,direct_corpus=True,
                content=r['result'],force='STRONG for textual attribution ONLY',limit='Targeted pages, no empirical validation',interpretive=True)
            g['evidence'].append(ev);q['evidence'].append(eid)
        counterid='EVID-COUNTER-'+id+'-01'
        counter=dict(id=counterid,question=id,claim=None,type='COUNTEREXAMPLE' if id in ['RQ-03.02','RQ-08.01','RQ-08.03','RQ-08.04'] else 'LOGICAL',
            relation='QUALIFIES',source={'artifact':'research_questions/'+id+'/reconstruction.md'},
            content=r['counter'],force='STRONG' if id in ['RQ-03.02','RQ-08.01','RQ-08.03','RQ-08.04'] else 'MODERATE',
            limit=r['domain'],counter_kind='QUALIFICATION',interpretive=True)
        g['evidence'].append(counter);q['evidence'].append(counterid)
        evidence=(folder/'evidence.md').read_text()+'\n## Deuxième passe — soutien et contre-épreuve\n\n'
        for ev in g['evidence']:
            if ev['question']==id and ev['id'].startswith(('EVID-SUPPORT-','EVID-COUNTER-')):
                evidence+='### '+ev['id']+'\n\nType : '+ev['type']+' ; relation : '+ev['relation']+' ; force : '+ev['force']+'.\n\n'+ev['content']+'\n\nSource : '+(ev['source'].get('id') or ev['source'].get('artifact'))+'.\n\nLimites : '+ev['limit']+'\n\nInterprétation concurrente : '+r['exceptions']+'\n\n'
        evidence+='Qualification de la contre-preuve : QUALIFICATION, pas contradiction de la question entière.\n'
        write(folder/'evidence.md',evidence)
        q['literature']=[];lit='# '+id+' — littérature ciblée\n\n3–8 références liées au périmètre ; vérification d’existence ≠ lecture intégrale.\n\n'
        for n in r['bib']:
            s=lib[f'BIB-{n:04}'];relation='PARALLELS' if n in [13,14] else 'QUALIFIES'
            comparison=('Définitions et mesure externes, non équivalence automatique avec les concepts Campergue.' if n in [2,3,8,10,11,12,19,20] else
                        'Critère mathématique ou résultat externe pertinent ; ne démontre pas sa transposition économique.')
            b=dict(id=s['id'],relation=relation,question=id,claims=q['claims'],comparison=comparison,verification=s['status'],source=s,limit=s['access'])
            q['literature'].append(b)
            lit+=f"## {s['id']}\n\n{s['authors']} ({s['year']}). [{s['title']}]({s['url']}). DOI : {s.get('doi') or 'non renseigné'}.\n\nQuestion : {id} ; claims : {', '.join(q['claims'])}. Relation : {relation}.\n\nRésultat pertinent / portée : {s['access']}\n\nComparaison : {comparison}\n\nLimite : {s['status']} ; ne teste pas la théorie complète.\n\n"
        write(folder/'literature.md',lit)
        tests='# '+id+' — tests de deuxième passe\n\n'+r['test']+'\n\nHypothèse/prédiction : '+r['derivation']+'\n\nVariables et données : '+r['definitions']+'\n\nConditions : '+r['conditions']+'\n\nRésultat incompatible ou contre-exemple : '+r['counter']+'\n\nExplications concurrentes / domaine : '+r['exceptions']+'\n\nLes cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.\n'
        write(folder/'tests.md',tests)
        q.update(status=r['status'],confidence='MEDIUM',second_pass=True,second_pass_order=ORDER.index(id)+1,
            confidence_components=dict(zip(['TEXTUAL_CONFIDENCE','FORMAL_CONFIDENCE','EMPIRICAL_CONFIDENCE','LITERATURE_CONFIDENCE'],r['scores'])),
            conclusion=r['result'],test_design=r['test'],test_design_status='SECOND_PASS_DESIGNED_OR_FORMALLY_CHECKED',
            corpus_completeness='DIRECT_TARGETED_READING_NOT_EXHAUSTIVE',second_pass_sources=[s['id'] for s in records],
            internal_issue=r['issue'],next_evidence=r['missing'])
        readme=(folder/'README.md').read_text().replace('OPEN ; confiance LOW.',r['status']+' ; confiance MEDIUM.')
        readme+='\n## Deuxième passe\n\n[Reconstruction avant critique](reconstruction.md). '+r['result']+'\n\nPrérequis non entièrement résolus : '+', '.join(d+' ('+by[d]['status']+')' for d in q['dependencies'])+'.\n\n'+r['issue']+'\n'
        write(folder/'README.md',readme)
        conclusion='# '+id+' — conclusion de deuxième passe\n\n'
        for name,content in [('STATUS',r['status']),('WHAT_CAMPERGUE_CLAIMS',r['premises']+' '+r['mechanism']),('WHAT_IS_DERIVED',r['derivation']),
            ('WHAT_EVIDENCE_SUPPORTS',r['definitions']),('WHAT_EVIDENCE_QUALIFIES',r['exceptions']),('WHAT_EVIDENCE_CONTRADICTS',r['counter']),
            ('WHAT_REMAINS_UNKNOWN',r['missing']),('PROVISIONAL_ANSWER',r['result']),('CONFIDENCE','MEDIUM'),('SCOPE',r['domain'])]:
            conclusion+='## '+name+'\n\n'+content+'\n\n'
        for name,val in q['confidence_components'].items():conclusion+=name+' = '+val+'\n\n'
        conclusion+='Aucune moyenne de confiance. Aucun verdict global. SOURCE et MINIMAL_RECONSTRUCTION restent séparés dans les fichiers associés.\n'
        write(folder/'conclusion.md',conclusion)
        history.append(dict(version=2,action='SECOND_PASS',id=id,old_statement=q['question'],new_statement=q['question'],old_status=oldstatus,new_status=q['status'],
                            reason=r['result'],new_evidence=q['evidence'],sources=q['second_pass_sources']))
    dump(OUT/'second_pass_sources.json',direct)
    g['version']=2;dump(OUT/'question_graph.json',g);dump(OUT/'history.json',history)
    # Current dashboard, preserving the prior file in the archive.
    table(OUT/'evidence_matrix.csv',['Question','Corpus evidence','Formal evidence','Empirical evidence','External literature','Counterevidence','Tests available','Status','Confidence'],
        [(q['id'],sum(e['type']=='TEXTUAL' for e in g['evidence'] if e['question']==q['id']),
          sum(e['type'] in ['FORMAL','LOGICAL'] for e in g['evidence'] if e['question']==q['id']),
          sum(e['type']=='EMPIRICAL' for e in g['evidence'] if e['question']==q['id']),len(q['literature']),
          sum(e.get('counter_kind') is not None or e['type']=='COUNTEREXAMPLE' for e in g['evidence'] if e['question']==q['id']),q['test_design_status'],q['status'],q['confidence']) for q in g['nodes']])
    status='# Statuts actuels après deuxième passe\n\n| Question | Première passe | Deuxième passe | Statut | Confiance |\n|---|---|---|---|---|\n'
    status+='\n'.join(f"| [{q['id']}]({q['id']}/README.md) | {q['first_pass']} | {q.get('second_pass',False)} | {q['status']} | {q['confidence']} |" for q in g['nodes'])+'\n'
    write(OUT/'status.md',status)
    tree=(OUT/'questions.md').read_text()
    for id in ORDER:
        start=tree.index('### '+id+' —');end=tree.find('\n##',start+5);end=len(tree) if end<0 else end
        section=tree[start:end].replace('statut : OPEN.', 'statut : '+by[id]['status']+'.')
        tree=tree[:start]+section+tree[end:]
    write(OUT/'questions.md',tree)
    coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text());before=sum(p['examined'] for p in coverage)
    newpages=[]
    note='# Lecture dirigée — deuxième passe des questions\n\nPages directement lues : '+', '.join(map(str,sorted(READ)))+'. Les candidats RAG non retenus ne sont pas comptés. Une nouvelle note ne crée pas automatiquement un claim.\n\n'
    for page in sorted(READ):
        relevant=[id for id,r in REVIEWS.items() if page in r['pages']]
        note+='## Page PDF '+str(page)+'\n\nQuestions : '+', '.join(relevant)+'.\n\n'
        note+='\n\n'.join(REVIEWS[id]['definitions'] for id in relevant)+'\n\n'
        p=coverage[page-1]
        if not p['examined']:
            newpages.append(page);p.update(examined=True,reading_note='second_question_pass.md',reason='TARGETED_READING_SECOND_QUESTION_PASS')
    write(ROOT/'analysis/reading_notes/second_question_pass.md',note)
    dump(ROOT/'analysis/data/page_coverage.json',coverage)
    progress=json.loads((ROOT/'analysis/data/phase2_progress.json').read_text());progress['pages_examined']=sum(p['examined'] for p in coverage)
    progress['second_question_pass']='10 targeted dossiers, no global verdict';dump(ROOT/'analysis/data/phase2_progress.json',progress)
    dump(marker,dict(questions=ORDER,coverage_before=before,coverage_after=progress['pages_examined'],new_pages=newpages,read_pages=sorted(READ),
        new_claims=0,source_claim_count=127,new_bibliography=[s['id'] for s in new],literature_used=used,
        dependency_graph_changed=False,root_question_unchanged=True,archive=str(ARCH.relative_to(ROOT)),
        exhaustive_source_search=False,formal_results='research_questions/second_pass_formal_results.json'))
    print('Integrated',len(ORDER),'questions; coverage',before,'→',progress['pages_examined'])
if __name__=='__main__':main()
