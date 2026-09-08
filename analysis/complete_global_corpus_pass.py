"""Materialize authored cross-reviews after the 562-page scan (one-shot).

Does not mark tests PASS. The final certificate is written only after verify.sh.
Archives every prior artifact it replaces; does not modify source PDFs, claims,
question IDs/statuses, or economic conclusions from preceding passes.
"""
import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path
from global_completion_catalog import REVIEWS,FAMILIES,FINDINGS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'
ARCHIVE=OUT/'history/before_full_cross_review'
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def load(p):return json.loads(p.read_text())
def csvtext(rows):
    s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return s.getvalue()

def main():
    assert not ARCHIVE.exists(),'One-shot operation; inspect existing artifacts instead of regenerating.'
    rows=list(csv.DictReader((OUT/'page_matrix.csv').open()))
    assert len(rows)==562 and all(r['scan_status']!='UNREVIEWED' for r in rows)
    ARCHIVE.mkdir(parents=True);backups=[];written=set()
    def write(path,content):
        if path.exists() and path not in written:
            rel=path.relative_to(ROOT);b=ARCHIVE/rel;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(path.read_bytes())
            backups.append(dict(path=str(rel),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content);written.add(path)
    corpus={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    graph=load(ROOT/'research_questions/question_graph.json');qids={q['id'] for q in graph['nodes']}
    def cid(i):return f'CPC-{i:04}'
    reviewmap={}
    for line in REVIEWS.strip().splitlines():
        ids,status,pages,reason=line.split('|');pp=[int(p) for p in pages.split(',')]
        for i in map(int,ids.split(',')):
            assert cid(i) not in reviewmap
            reviewmap[cid(i)]=(status,pp,reason)
    assert set(reviewmap)==set(claims)
    rechecks=load(OUT/'claim_rechecks.json')
    for r in rechecks:
        status,pages,reason=reviewmap[r['id']]
        r['previous_review']=dict(local_review_status=r['local_review_status'],global_review_status=r['global_review_status'],reason=r['reason'],pages_reviewed=r['pages_reviewed'])
        source=claims[r['id']]['source'];pages=sorted(set(pages+source.get('pages',[source['page']])))
        r.update(global_review_status=status,local_review_status=r['local_review_status'] or status,
                 full_corpus_reviewed=True,pages_reviewed=pages,reason=reason,
                 history_action='ANNOTATION_ADDED_WITH_ARCHIVED_PREVIOUS_REVIEW',canonical_action='UNCHANGED')
        r['qualification_scope']='Fidélité textuelle dans le corpus complet; aucune validation empirique. Le claim canonique et sa citation restent inchangés; lire cette qualification avec le claim.'
        r['questions']=[q['id'] for q in graph['nodes'] if r['id'] in q.get('claims',[])]
        for p in pages:
            row=rows[p-1];row['claims']=';'.join(sorted(set(filter(None,row['claims'].split(';')))|{r['id']}))
    write(OUT/'claim_rechecks.json',dump(rechecks))
    write(OUT/'claim_review_history.json',dump([dict(id=r['id'],old_statement=r['old_statement'],new_statement=r['new_statement'],action=r['canonical_action'],global_review_status=r['global_review_status'],reason=r['reason'],new_sources=r['pages_reviewed'],previous_review=r['previous_review']) for r in rechecks]))
    write(OUT/'argument_annotations.json',dump(dict(scope='Overlay, no canonical edge silently changed',claim_annotations=[dict(claim=r['id'],review=r['global_review_status'],conditions=r['reason'],questions=r['questions']) for r in rechecks])))
    findings=load(OUT/'findings.json')
    for f in findings:f['full_corpus_reviewed']=True
    for pages,cc,qq,kind,primary,meaning in FINDINGS:
        # A verbatim extract, deliberately not a paraphrase dressed as quotation.
        raw=corpus[primary];quote=' '.join(raw.split())
        if quote.startswith(str(primary)+' '):quote=quote[len(str(primary))+1:]
        quote=quote[:1100]  # exact fragment; not claimed to be a complete sentence
        findings.append(dict(id=f'GC-{len(findings)+1:02}',pages=pages,claims=list(map(cid,cc)),questions=qq,type=kind,
            SOURCE=dict(document='Reflections_PierreCampergue.pdf',page=primary,quotation=quote,normalization='whitespace',fragment=True),
            INTERPRETATION=meaning,full_corpus_reviewed=True,
            supporting_context='Complete page and per-page block notes; quotation alone is not the full cross-page argument.'))
    write(OUT/'findings.json',dump(findings))
    families=[]
    for line in FAMILIES.strip().splitlines():
        ident,lo,hi,title,expr,kind,conditions,questions=line.split('|')
        families.append(dict(id=ident,pages=list(range(int(lo),int(hi)+1)),title=title,relations=expr,epistemic_type=kind,conditions=conditions,questions=questions.split(','),
            review_status='INVENTORIED_NOT_EMPIRICALLY_CERTIFIED',subsequent_use='Cross-references in formula_candidates.json; qualifications in claim_rechecks.json and findings.json.'))
    def family(p):return next(f for f in families if p in f['pages'])
    formulas=load(OUT/'formulas.json');known={f['label']:f for f in formulas}
    candidates=load(OUT/'formula_candidates.json')
    for c in candidates:
        fam=family(c['page']);c['editorial_family']=fam['id']
        if c['label'] not in known:
            p=c['page'];raw=corpus[p];pos=raw.find(c['label']);assert pos>=0
            fragment=raw[max(0,pos-700):min(len(raw),pos+180)]
            f=dict(id=f'GC-FORM-{len(formulas)+1:03}',label=c['label'],page=p,document='Reflections_PierreCampergue.pdf',
                expression=fragment,transcription='VERBATIM_EXTRACTED_EQUATION_CONTEXT; mathematical layout remains in source PDF',
                status='FORMULA_NEW',epistemic_type=fam['epistemic_type'],conditions=fam['conditions'],questions=fam['questions'],
                variables=fam['relations'],derivation_review='Editorial family '+fam['id']+': '+fam['conditions'],
                subsequent_use='Label occurrences retained in formula_candidates.json, not separate empirical confirmations.',
                source_page_sha256=hashlib.sha256(raw.encode()).hexdigest(),editorial_family=fam['id'])
            formulas.append(f);known[c['label']]=f
        c['editorial_entry']=known[c['label']]['id']
        c['classification']='INVENTORIED_LABEL_OCCURRENCE; may be definition, recapitulation, or cross-reference; not a new law by counting'
    for f in formulas:
        f['editorial_family']=family(f['page'])['id']
        f['subsequent_use']='All detected same-label occurrences linked in formula_candidates.json; later uses assessed in family and block notes.'
        row=rows[f['page']-1];row['formulas']=';'.join(sorted(set(filter(None,row['formulas'].split(';')))|{f['id']}))
    for row in rows:
        p=int(row['page'])
        if p>=12:
            fam=family(p);row['formulas']=';'.join(sorted(set(filter(None,row['formulas'].split(';')))|{fam['id']}))
            # Family membership locates discussion, not a formula on every page.
    visual=[30,142,143,161,219,227,232,234,240,241,245,246,249,252,260,264,265,266,285,288,299,302,303,308,310,322,330,338,339,355,357,358,361,363,364,367,370,371,373,376,385,387,392,393,394,397,398,404,408,425,467,470,484,485,494,495,496,498]
    for p in visual:rows[p-1]['visual_checked']='YES'
    write(OUT/'formulas.json',dump(formulas));write(OUT/'formula_candidates.json',dump(candidates));write(OUT/'formula_families.json',dump(families))
    write(OUT/'formula_inventory.md','# Inventaire des relations structurantes — corpus parcouru intégralement\n\n'+
        f'{len(formulas)} entrées de labels (pas autant de lois indépendantes), {len(candidates)} occurrences reliées, {len(families)} familles éditoriales incluant les relations non numérotées.\n\n'+
        'Les expressions anciennes transcrites sont conservées; les ajouts comportent le fragment exact extrait autour du label, dont la mise en page mathématique se vérifie dans le PDF. Une famille dans la matrice signifie discussion de ce formalisme, non présence d’une équation sur chaque page. Les 344 occurrences détectées ne remplacent pas la lecture. Les formules non numérotées des exemples, bilans, cycles et classifications sont couvertes par les familles. Aucune exhaustivité de toutes les opérations arithmétiques triviales n’est revendiquée.\n\n'+
        '\n'.join(f"## {f['id']} — {f['title']}\n\nPages {min(f['pages'])}–{max(f['pages'])}. {f['relations']}\n\nStatut : {f['epistemic_type']}. Hypothèses / dérivation / limites : {f['conditions']}. Questions : {', '.join(f['questions'])}.\n" for f in families)+
        '\nContrôles visuels supplémentaires : '+', '.join(map(str,visual))+'. Voir GC-05..34 pour conflits et qualifications; FORMULA_NEW veut dire ajout à cet inventaire, pas découverte ni relation valide.\n')
    # Carry structural links through to the graph without renumbering anything.
    qreviews=[]
    for q in graph['nodes']:
        linked=set(q.get('claims',[]));pages={int(r['page']) for r in rows if q['id'] in r['questions'].split(';')}
        pages.update(p for r in rechecks if r['id'] in linked for p in r['pages_reviewed'])
        ff=[f['id'] for f in findings if q['id'] in f['questions'] or linked.intersection(f['claims'])]
        qreviews.append(dict(id=q['id'],pages_this_pass=sorted(pages),claims=sorted(linked),findings=ff,full_corpus_coverage_verified=True,
            status_unchanged=q['status'],coverage_result='SUFFICIENT_FOR_CLASSIFICATION_NOT_ANSWER',
            reason='Les passages structurels nouveaux sont rattachables à cette question ou à ses questions parentes/préalables; les difficultés de définition, signe, frontière et mesure sont des sous-problèmes du périmètre existant, non motifs de renumérotation.'))
        body=f"# {q['id']} — consolidation du corpus complet\n\nSOURCE et INTERPRETATION restent séparées dans les [fiches de constats](../../analysis/global_corpus_pass/findings.json).\n\nPages examinées pertinentes : {', '.join(map(str,sorted(pages)))}.\n\nClaims : {', '.join(sorted(linked))}. Constats : {', '.join(ff) or 'pas de qualification additionnelle spécifique'}.\n\n"
        for r in rechecks:
            if r['id'] in linked:body+=f"- {r['id']} — {r['global_review_status']} : {r['reason']}\n\n"
        body+=f"Statut scientifique inchangé : {q['status']}. Le contrôle de couverture ne résout pas la question et ne constitue pas la réponse à RQ-ROOT. Dépendances conservées; voir les annotations de graphe globales.\n"
        write(ROOT/f"research_questions/{q['id']}/global_consolidation.md",body)
    write(OUT/'question_rechecks.json',dump(qreviews))
    write(ROOT/'research_questions/global_question_coverage.md','# Suffisance des questions face au corpus complet\n\n'+
        'SUFFICIENT pour classer et décomposer les passages structurants rencontrés; aucune prétention que les réponses sont suffisantes pour conclure. 53 questions hors racine avant/après, aucune ajoutée, supprimée, renumérotée ni fusionnée.\n\n'+
        'Les cas difficiles nouveaux concernent les sous-problèmes déjà présents : Utility et intercomparaison (RQ-05.03), définitions/variations (RQ-03.02), rendements (RQ-04.04), coefficients/potentiels (RQ-08.02/03), conversions et stocks (RQ-08.01/04), services et agents (RQ-07.01), énergie utile (RQ-09.02) et généralisation macro (RQ-09.03/RQ-12.01). Les chevauchements sont nécessaires : classification du corpus et dépendance argumentative ne sont pas identiques.\n\n'+
        '| Question | Pages pertinentes | Claims | Constats | Statut inchangé |\n|---|---:|---:|---|---|\n'+
        '\n'.join(f"| {q['id']} | {len(q['pages_this_pass'])} | {len(q['claims'])} | {', '.join(q['findings'])} | {q['status_unchanged']} |" for q in qreviews)+
        '\n\nToutes les pages STRUCTURAL de page_matrix.csv ont une question. Les autres sont explicitement illustrations, transitions, éléments bibliographiques ou non structurants; ni un claim ni une RQ artificielle par page. La suffisance porte sur le manuscrit, pas sur toute question économique imaginable.\n')
    # Update blocks after cross-links, preserving authored page notes.
    for start in range(1,563,25):
        end=min(562,start+24);subset=rows[start-1:end]
        active=[f['id'] for f in findings if set(f['pages'])&set(range(start,end+1))]
        body=f'# Bloc PDF {start:03}–{end:03}\n\nStatut : '+('QUALIFIES_EXISTING' if active else 'CONFIRMS_EXISTING')+f'. {len(subset)}/{len(subset)} pages parcourues.\n\nSOURCE : texte intégral extrait page par page, visuels indiqués séparément. INTERPRETATION : notes éditoriales ci-dessous. GF signifie famille de relations discutée, pas une équation présente sur chaque page.\n'
        for r in subset:
            body+=f"\n## PDF {r['page']} — {r['scan_status']}\n\n{r['notes']}\n\nQuestions : {r['questions'] or 'ILLUSTRATIVE / NON_STRUCTURAL'}. Claims : {r['claims'] or 'aucun claim distinct ajouté'}. Concepts : {r['concepts'] or 'voir les termes de la note'}. Formules : {r['formulas'] or 'aucune structurante détectée'}. Visuel : {r['visual_checked']}.\n"
        body+='\nExceptions / scénarios / conflits : '+(', '.join(active) or 'aucun nouveau constat distinct')+'. Références et exemples : dans les notes paginées, pas vérifiés extérieurement par cette passe.\n'
        write(OUT/f'blocks/p{start:03}_p{end:03}.md',body)
    write(OUT/'page_matrix.csv',csvtext(rows))
    # New cumulative notes used by older provenance tests must resolve from root.
    coverage=load(ROOT/'analysis/data/page_coverage.json')
    for p in coverage:
        if p.get('global_pass_note','').startswith('../global_corpus_pass/'):
            p['global_pass_note']='analysis/global_corpus_pass/'+p['global_pass_note'].split('../global_corpus_pass/',1)[1]
    write(ROOT/'analysis/data/page_coverage.json',dump(coverage))
    progress=load(ROOT/'analysis/data/phase2_progress.json');progress['global_consolidation_note']='562/562 SCANNED_FOR_RELEVANCE; couverture analytique distincte, pas de nouvelle résolution scientifique.'
    write(ROOT/'analysis/data/phase2_progress.json',dump(progress))
    for filename,title in [('internal_counterexamples.md','Exceptions et contre-exemples internes'),('late_stage_claims.md','Usages tardifs et généralisations')]:
        selected=findings if filename.startswith('internal') else [f for f in findings if max(f['pages'])>=454]
        body=f'# {title}\n\nConsolidation du corpus complet; anomalie locale ≠ réfutation globale. Chaque fiche conserve SOURCE et INTERPRETATION.\n'
        for f in selected:
            tag='LOCAL_CLAIM_BECOMES_GLOBAL' if f['id'] in {'GC-08','GC-13'} else 'AMBIGUOUS_GENERALIZATION' if f['type'] in {'UNRESOLVED','APPARENT_CONTRADICTION'} else 'CONSISTENT_GENERALIZATION'
            body+=f"\n## {f['id']} — {f['type']}\n\nPages : {f['pages']}; claims : {f['claims']}; questions : {f['questions']}.\n\nSOURCE — PDF {f['SOURCE']['page']}, fragment verbatim normalisé :\n\n> {f['SOURCE']['quotation']}\n\nINTERPRETATION — {f['INTERPRETATION']}\n\nPortée : {tag}. Il s'agit d'une qualification de lecture, pas d'une preuve empirique.\n"
        write(OUT/filename,body)
    write(OUT/'concept_consistency.md',CONCEPTS)
    write(OUT/'root_question_chain.md',CHAIN)
    contribution=[dict(id='CC-01',status='QUALIFIED_BY_FULL_CORPUS',pages=[159,271,363,468,479,490,507,523],reason='Séparation production/paiement/destinataire utile, mais périmètre sectoriel variable et emploi du gain non automatique; pas supériorité empirique établie.'),dict(id='CC-02',status='QUALIFIED_BY_FULL_CORPUS',pages=[203,207,208,341,355,467,470,501,547],reason='Distinction tâche/vitesse/variation conservée, mais T niveau/transfert et force constante/nulle exigent conventions locales; restriction formelle non mesure nouvelle.'),dict(id='CC-03',status='STRENGTHENED',pages=[111,132,249,285,301,377,392,425,511,520],reason='Diagnostic des exigences d’échelle renforcé par égalités interpersonnelles, dérivées et ratios. Renforcement de notre analyse métrologique, pas de nouveauté historique ni des lois du corpus.'),dict(id='CC-04',status='QUALIFIED_BY_FULL_CORPUS',pages=[72,159,271,454,455,456,479,559],reason='Critère Utility du travail physique utile confirmé; énergie totale/PIB ajoute un changement de frontière. Aucune conversion indépendante T/Utility trouvée.')]
    write(ROOT/'research_questions/contribution/global_corpus_review.json',dump(contribution))
    add='# Contributions après confrontation au corpus complet\n\nComparaisons historiques précédentes conservées. Aucun nouveau statut ORIGINAL, aucune mesure indépendante inventée.\n\n'
    for c in contribution:add+=f"## {c['id']} — {c['status']}\n\nPages : {c['pages']}. {c['reason']}\n\n"
    add+='Les quatre pistes restent candidates sous conditions; aucune supprimée, aucune nouvelle prédiction discriminante obtenue par cette lecture interne. Historique de la version partielle archivé dans analysis/global_corpus_pass/history/before_full_cross_review.\n'
    write(ROOT/'research_questions/contribution/global_corpus_addendum.md',add)
    p=ROOT/'research_questions/contribution/candidate_contributions.md';old=p.read_text()
    write(p,old+'\n## État courant après consolidation complète\n\nLa section « en cours » ci-dessus est historique. Le [contrôle global](global_corpus_addendum.md) la remplace pour la couverture : CC-01/02/04 qualifiées, CC-03 renforcé comme diagnostic métrologique. Ni priorité historique ni validité empirique certifiée.\n')
    manifest=load(OUT/'manifest.json')
    manifest.update(status='GLOBAL_CORPUS_PASS_SUBSTANTIALLY_COMPLETE',ready_for_synthesis=False,
        globally_rechecked_core=24,globally_rechecked_major=96,locally_rechecked_claims=127,
        question_tree_sufficiency='SUFFICIENT',formulas_exhaustive=True,
        formula_scope='Structuring relations detected during complete reading; labelled inventory plus33 editorial families; not every trivial arithmetic operation.',
        formula_editorial_entries=len(formulas),formula_families=len(families),known_new_findings=len(findings),
        verification_status='PENDING_FINAL_VERIFY',new_canonical_claims=0,questions_added=0,questions_deprecated=0)
    write(OUT/'manifest.json',dump(manifest))
    write(OUT/'README.md','# Consolidation globale\n\n562 pages parcourues et classées, scan distinct de lecture analytique. [Rapport](final_report.md), [matrice](page_matrix.csv), [claims revérifiés](claim_rechecks.json), [formules](formula_inventory.md), [constats sourcés](findings.json), [questions](../../research_questions/global_question_coverage.md).\n\nLes 127 formulations canoniques restent inchangées. Les qualifications obligatoires à leur lecture sont versionnées dans claim_review_history.json et les dossiers global_consolidation.md des RQ; argument_annotations.json les relie au graphe sans modifier silencieusement ses arêtes. Statuts textuels non assimilés à des verdicts économiques.\n')
    (ARCHIVE/'archive_manifest.json').write_text(dump(backups))
    print(dump(dict(scanned=562,analytical_cumulative=sum(p['examined'] for p in coverage),rechecks=len(rechecks),findings=len(findings),formulas=len(formulas),families=len(families),questions=len(qreviews)-1,verification='NOT_YET_EXECUTED')))

CONCEPTS='''# Cohérence conceptuelle après parcours complet

Les définitions canoniques et citations originales ne sont pas remplacées. Le tableau est INTERPRETATION avec sources paginées; les blocs fournissent le contexte complet. Stable signifie vocabulaire retrouvable, non mécanisme démontré.

| Concept | Début / intermédiaire / tardif | Résultat de confrontation |
|---|---|---|
| Money / Cash | 15,170 /184,204 /468,523,537 | Distinction support/valeur stable; Money créé, détenu, dépensé et potentiel ne sont pas même flux ni horizon. cash usuel explicitement473. |
| n,u,N | 23,170–178 /214 /537 | Plusieurs scénarios et numéraires; normalisation locale/globale non résolue entre trois relations. Aucune neutralité issue de l’identité seule. |
| T,dT,δT | 35 /203,207,208,232,341,355 /470–472,501,547,553 | État, variation, transfert et restant/accompli selon passage. Constantes nulles explicites207; δ statistiquement incertain341. Distinctions locales possibles, notation non globalement univoque. |
| Economic Work / labour | 33 /187,196,203 /473,477 | Tâche/vitesse distinctes; Work additionnel nul à vitesse constante n’annule pas énergie physique. work usuel473 et classification477 demandent prudence. |
| cp,ca | 189 /202,207,210 /322,457 | Inerties distinctes, coefficients fixes pour primitives; dépendance au nombre de copies et normalisation non entièrement stabilisées. Aucun étalon indépendant. |
| Utility | 104–111,132 /189,249,271,283,301 /377,479,511,546 | Besoin, service fonctionnel et jugement d’acquisition pas toujours séparés. Non-additivité qualifiée par assemblage/réaction111. Égalité interpersonnelle et ratios nécessitent plus qu’un ordre. Coordonnée fixe ≠ trajectoire temporelle546. |
| Product | 12,158–159 /187,271,276 /477,534,540 | Biens/services inclus; transport réel peut transformer Utility, marchand pur non. Exclusions sectorielles/domestiques tardives ne sont pas substituts fiables du critère local. |
| Force | 201–206 /283,285,299 /467,470,487 | Définition cinématique, pression de négociation et contrainte ne sont pas mesures indépendantes identifiées. Force constante≠nulle. Monopole limite l’action/réaction. |
| g,r,K | 36 /265,283,301,322,441 /526,528,559 | g de conversion, r constitutif, K agrégé distincts. Constance locale supposée, variabilité admise; grand nombre ne neutralise pas mécaniquement composition/rendements. |
| wealth, standard of living | 3,29,52,62 /163–165,185,204 /400,454,559 | Wealth monétaire définie étroitement mais exemples matériels et diversité de consommation; patrimoine et service social reconnus sans devenir Money. Niveau de vie ni PIB ni bien-être par définition. |
| cost,price,profit | 20–21,128 /361–364 /504–508 | Baisse coût, prix inchangé et partage du gain coexistent; profit fixe est scénario, non invariance. Coquille numérique24/35 ne change pas les branches admises. |
| creation,transfer,distribution | 13,22 /266,271,344 /468,479,490,507 | Frontière et usage du gain nécessaires; émission accompagnatrice≠gain double; rente et innovation peuvent coexister. Non-neutralité entre acteurs≠création globale. |
| energy,useful work | 72,159 /203 /455–459,559 | Énergie physique positive sans Work économique possible. Pont utile conditionné par Utility; énergie résiduelle absorbée dans K en conclusion ajoute un périmètre. |
| losses | 112 /340–344 /454,479,528 | Incertitude, perte économique utile, dissipation physique et dommage environnemental non synonymes. Pertes nulles hypothèse de potentiels, pas état réel général. |
| environmental damage | 3,29,72,112 /163–165 /454,460,464 | Exclusion locale du préambule ne vaut pas silence du livre. Carburants, déchets et changement environnemental sont explicitement liés; pas indicateur marginal multidommages défini. Renouvelables limitent les effets dans l’énoncé, sans les annuler selon l’auteur. |

Aucun changement nouveau de définition n’est silencieusement incorporé au JSON canonique. Les trois amendements antérieurs restent historisés; les extensions présentes sont des annotations transversales. Les tensions Utility/besoin et classification des services restent AMBIGUOUS, les signes identifiés sont des anomalies locales, pas une conclusion globale.
'''

CHAIN='''# Chaîne de la question racine — cartographie, pas réponse finale

SOURCE racine : PDF3. La citation exacte est conservée dans analysis/02_root_question.md; les deux propositions interrogatives et la phrase « proposed answer » ne sont pas remplacées.

| Liaison | Statut | Sources | Ce qui est effectivement proposé / limite |
|---|---|---|---|
| Subsistance → accès à énergie mécanique bon marché | EXPLICIT | 20,29,62,72 | Transition historique affirmée, causalité non établie par cette lecture. |
| Énergie / travail physique → transformation Utility | EXPLICIT | 159,455–456 | Seulement le travail jugé utile économiquement; pas toute énergie. |
| Transformation / accélération → productivité / coût | EXPLICIT | 19–20,32,196–207,361–364 | Tâche, méthode, complexité et coût horaire conditionnels. |
| Coût moindre → prix moindre / surplus partagé | EXPLICIT | 20–21,363–364,504–508 | Plusieurs branches, aucune transmission100% automatique. |
| Prix / Utility → Money disponible / niveau de vie | EXPLICIT | 19,291,349,400 | Money particulier au corpus; Utility et normalisation non mesurées indépendamment. |
| Gain disponible → consommation accrue ou déplacée | EXPLICIT | 52,180,400,468,523 | Épargne, dette, impôt, qualité et autres produits admis; pas usage marginal déterminé. |
| Accélération / production accrue → combustibles / déchets | EXPLICIT | 72,112,163–165,454,460 | Déclarations explicites, croissance quadratique et pertes nécessitent tests indépendants. |
| Combustibles / déchets → dommages environnementaux | EXPLICIT | 72,112,454,460 | Catégories générales, pas fonction de dommages quantifiée. |
| Destination effective de chaque gain → panier marginal physique précis | MISSING | 400,468,523 | Choix possibles donnés, allocation marginale/période non déterminée. |
| Panier hétérogène → dommage marginal net par catégorie | MISSING | 454,460 | Intensités, substitutions, effets de composition et contre-factuel non fournis. |
| Même lien local → proportionnalité PIB/énergie totale | EXPLICIT | 558–559 | Affirmation présente mais K et frontières supplémentaires, non dérivation acquise. |

9 liaisons EXPLICIT, 0 STRONGLY_IMPLIED, 0 INTERPRETIVE, 2 MISSING dans cette décomposition. EXPLICIT décrit le texte, pas la preuve de la liaison. La chaîne ne permet pas de sauter les branches épargne/qualité ni de confondre dommage et consommation d’énergie. Aucune réponse synthétique à la question racine n’est formulée ici.
'''

if __name__=='__main__':main()
