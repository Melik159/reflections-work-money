"""Versioned first comparison pass; no historical originality asserted."""
import csv,io,json,shutil
from collections import Counter
from pathlib import Path
from contribution_catalog import CONCEPTS,CORE,NEW_SOURCES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions/contribution';ARCH=ROOT/'research_questions/history/fifth_pass_before'
def write(path,text):
    p=ROOT/path
    if p.exists():
        b=ARCH/p.relative_to(ROOT);b.parent.mkdir(parents=True,exist_ok=True)
        if not b.exists():shutil.copy2(p,b)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def dump(path,x):write(path,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(str(x).replace('|','/').replace('\n',' ') for x in row)+' |\n' for row in rows)
def main():
    if (OUT/'manifest.json').exists():raise SystemExit('Comparative pass already exists; amend with history')
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    assert set(CORE)=={c for c,x in claims.items() if x['criticality']=='CORE'}
    existing={s['id']:s for s in json.loads((ROOT/'bibliography/initial_research_library.json').read_text())}
    new=[]
    for bid,author,title,year,url,status,scope,result,limit in NEW_SOURCES:
        new.append(dict(id=bid,author=author,title=title,year=year,url=url,status=status,verification_scope=scope,result=result,limit=limit,accessed='2026-09-08',primary=True))
    # Add strong accessible methods to entries otherwise only supported by inaccessible leads.
    conceptrows=[]
    for i,(term,pages,meaning,framework,similarity,diff,status,bibs) in enumerate(CONCEPTS,1):
        bibs=list(bibs)
        if term in ['consumer gain','productive creation','Money','Utility']:bibs.append('CBIB-10')
        if term in ['Economic Work','labour','cost','productivity-cost-price chain']:bibs.append('CBIB-11')
        distinct=status.startswith('DISTINCT_')
        conceptrows.append(dict(id=f'COMP-{i:02}',kind='CONCEPT',term=term,source_document='Reflections_PierreCampergue.pdf',source_pages=pages,campergue_definition=meaning,definition_is_interpretation=True,
            existing_framework=framework,similarity=similarity,difference=diff,substantive_difference='YES_IN_SPECIFIED_CONSTRUCTION' if distinct else 'PARTIAL_OR_NOT_ESTABLISHED',
            observable_consequence='Formal domain or classification differs; economic observable not independently identified' if distinct else 'No additional observable demonstrated beyond named comparator',
            different_prediction=False,prediction_status='NOT_IDENTIFIED' if distinct else 'NONE_ESTABLISHED',different_measurement=False,measurement_limit='No independent calibration or new measurement supplied',
            decision_relevance='May prevent category errors; no decision performance benchmark',historical_precedence_checked='TARGETED_COMPARATORS_ONLY',historical_novelty_status='HISTORICAL_NOVELTY_UNRESOLVED',contribution_status=status,sources=bibs,
            renaming_test='LOSS_OF_SPECIFIC_CONDITIONS_OR_FORMAL_RELATIONS' if distinct else 'LIKELY_REFORMULATION' if status in ['KNOWN_EQUIVALENT','KNOWN_WITH_DIFFERENT_TERMINOLOGY','RECOMBINATION_OF_KNOWN_CONCEPTS'] else 'PARTIAL_TRANSLATION_ONLY',
            lost_on_renaming=diff,reverse_test='The corpus reclassifies some operations; established frameworks may already separate them through other accounts or variables. No claim of a universal blind spot.',
            value=dict(CONCEPTUAL_CLARITY='MODERATE' if term in ['Cash','Money','labour','transfer','consumer gain','K'] else 'POSSIBLE',MEASUREMENT_VALUE='LOW' if distinct else 'POSSIBLE',EMPIRICAL_VALUE='UNDETERMINED',DECISION_VALUE='POSSIBLE'),originality_asserted=False,empirical_contribution_established=False))
    core=[]
    for cid,(framework,diff,status,bibs) in CORE.items():
        c=claims[cid];bibs=list(bibs)
        if cid in ['CPC-0015','CPC-0045']:bibs.append('CBIB-10')
        if cid in ['CPC-0017','CPC-0051','CPC-0052']:bibs.append('CBIB-11')
        core.append(dict(id=cid,kind='CORE_CLAIM',source=c['source'],what_campergue_claims=c['statement'],closest_existing_framework=framework,
            same='ONLY_IF_DOMAIN_AND_MEANING_MATCH' if status=='KNOWN_WITH_DIFFERENT_TERMINOLOGY' else 'NOT_EXACTLY',partly_same=True,substantively_different=status.startswith('DISTINCT_'),difference=diff,
            different_observable_consequence='Not established independently of definitions/calibration',different_prediction=False,contribution_status=status,historical_novelty_status='HISTORICAL_NOVELTY_UNRESOLVED',
            potential_usefulness=diff,sources=bibs,originality_asserted=False,value=dict(CONCEPTUAL_CLARITY='POSSIBLE',MEASUREMENT_VALUE='UNDETERMINED',EMPIRICAL_VALUE='UNDETERMINED',DECISION_VALUE='UNDETERMINED'),scope='First comparison, not exhaustive historical priority search'))
    dump('research_questions/contribution/concepts.json',conceptrows);dump('research_questions/contribution/core_comparisons.json',core)
    used={b for r in conceptrows+core for b in r['sources']}
    library=[dict(existing[b],verification_reused=True) for b in sorted(used) if b in existing]+new
    dump('research_questions/contribution/literature.json',library)
    write('research_questions/contribution/literature.md','# Registre comparatif\n\nCBIB est un registre spécialisé versionné; BIB réutilise les vérifications antérieures. VERIFIED décrit les passages spécifiés, non une lecture intégrale. Les accès403 et métadonnées seules restent PARTIALLY_VERIFIED. SNA2008 est un comparateur historique explicite, pas présenté comme dernière édition en vigueur.\n\n'+''.join(f"## {s['id']} — {s.get('title')}\n\n[{s.get('title')}]({s.get('url')}). Statut: {s.get('status',s.get('verification_status','SEE_PRIOR_REGISTRY'))}.\n\nPortée: {s.get('verification_scope','Vérification antérieure conservée dans registre BIB.')}\n\n{ s.get('result','Réemploi ciblé, voir analyses antérieures.') }\n\nLimite: {s.get('limit','Aucune priorité historique globale déduite.')}\n\n" for s in library))
    write('research_questions/contribution/concept_comparisons.md','# Comparaisons conceptuelles\n\nSens source préservé. « Distinct » signifie distinct des comparateurs nommés, pas inédit dans toute la littérature.\n\n'+''.join(f"## {r['id']} — {r['term']}\n\nSOURCE: {r['source_document']}, pages {r['source_pages']}. INTERPRETATION: {r['campergue_definition']}.\n\nCadres proches: {r['existing_framework']}. Sources: {', '.join(r['sources'])}.\n\nRecouvrement: {r['similarity']}. Différence: {r['difference']}.\n\nTest de renommage: {r['renaming_test']}; {r['lost_on_renaming']}. Test inverse: {r['reverse_test']}\n\nConséquence: {r['observable_consequence']}. Prédiction différente établie: NO. Mesure nouvelle établie: NO. Statut: {r['contribution_status']}; {r['historical_novelty_status']}.\n\nValeur: {r['value']}. Ces appréciations sont des jugements de recherche, pas des performances observées.\n\n" for r in conceptrows))
    write('research_questions/contribution/claim_comparisons.md','# Première comparaison des24 CORE\n\nChaque SOURCE est copiée du registre original, sans nouveau claim. Les statuts ci-dessous portent sur la comparaison, pas sur la véracité globale.\n\n'+''.join(f"## {r['id']}\n\n### SOURCE\n\n{r['source']['document']}, page {r['source']['page']}.\n\n> {r['source']['quotation']}\n\n### INTERPRETATION\n\nCampergue: {r['what_campergue_claims']}\n\nCadre proche: {r['closest_existing_framework']}. Sources: {', '.join(r['sources'])}.\n\nSame? {r['same']}. Partly same? YES. Différence substantielle dans la construction? {r['substantively_different']}.\n\n{r['difference']}\n\nConséquence observable différente: {r['different_observable_consequence']}. Prédiction différente établie: NO. Statut: {r['contribution_status']}; priorité: {r['historical_novelty_status']}.\n\nValeur possible: {r['potential_usefulness']}. Évaluations séparées: {r['value']}.\n\n" for r in core))
    headers=['ID','Campergue concept/claim','Source pages','Existing economic concept/model','Similarity','Difference','Is difference substantive?','Observable consequence','Different prediction?','Different measurement?','Decision relevance?','Historical precedence checked?','Current contribution status','Historical novelty status','Sources']
    buf=io.StringIO();w=csv.writer(buf);w.writerow(headers)
    for r in conceptrows:w.writerow([r['id'],r['term'],r['source_pages'],r['existing_framework'],r['similarity'],r['difference'],r['substantive_difference'],r['observable_consequence'],r['different_prediction'],r['different_measurement'],r['decision_relevance'],r['historical_precedence_checked'],r['contribution_status'],r['historical_novelty_status'],';'.join(r['sources'])])
    for r in core:w.writerow([r['id'],r['what_campergue_claims'],r['source'].get('pages',r['source']['page']),r['closest_existing_framework'],'Partial; see dossier',r['difference'],r['substantively_different'],r['different_observable_consequence'],False,False,r['potential_usefulness'],'TARGETED_COMPARATORS_ONLY',r['contribution_status'],r['historical_novelty_status'],';'.join(r['sources'])])
    write('research_questions/contribution/contribution_matrix.csv',buf.getvalue())
    dump('research_questions/contribution/manifest.json',dict(core_compared=len(core),concepts_compared=len(conceptrows),concept_status_counts=dict(Counter(r['contribution_status'] for r in conceptrows)),core_status_counts=dict(Counter(r['contribution_status'] for r in core)),novelty_unresolved_concepts=len(conceptrows),novelty_unresolved_core=len(core),library_entries=len(library),new_sources=len(new),new_verified=sum(s['status']=='VERIFIED' for s in new),new_partially_verified=sum(s['status']=='PARTIALLY_VERIFIED' for s in new),empirical_contributions_established=0,new_measurements_established=0,originality_asserted=False))
if __name__=='__main__':main()
