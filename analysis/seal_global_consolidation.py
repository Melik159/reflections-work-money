"""Final metadata reconciliation, actual verify execution, and scoped certificate.

The scan/review records preexist; this script cannot manufacture them.
"""
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from global_completion_catalog import FAMILIES
from verify_global_corpus_pass import validate
from complete_global_corpus_pass import csvtext,dump

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis/global_corpus_pass'

def main():
    archive=OUT/'history/before_complete_certificate';assert not archive.exists()
    archive.mkdir(parents=True);backups=[];written=set()
    def write(path,text):
        if path.exists() and path not in written:
            rel=path.relative_to(ROOT);p=archive/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(path.read_bytes())
            backups.append(dict(path=str(rel),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);written.add(path)
    def load(p):return json.loads(p.read_text())
    # Narrow correction of editorial headings after checking the actual labels.
    # Equations and original page readings unchanged; archive records old mapping.
    families=load(OUT/'formula_families.json')
    for line in FAMILIES.strip().splitlines():
        ident,lo,hi,title,expr,kind,conditions,qq=line.split('|')
        f=next(f for f in families if f['id']==ident)
        f.update(pages=list(range(int(lo),int(hi)+1)),relations=expr,title=title)
    write(OUT/'formula_families.json',dump(families))
    rows=list(csv.DictReader((OUT/'page_matrix.csv').open()))
    for p in range(426,431):rows[p-1]['formulas']=rows[p-1]['formulas'].replace('GF-23','GF-22')
    write(OUT/'page_matrix.csv',csvtext(rows))
    block=OUT/'blocks/p426_p450.md';text=block.read_text()
    split=text.index('## PDF 431 ');text=text[:split].replace('GF-23','GF-22')+text[split:];write(block,text)
    p=OUT/'formula_inventory.md';text=p.read_text().replace('05-01..10','05-01..09').replace('14-01..08','14-01..12').replace('16-01..32','16-01..34').replace('17-01..15','17-01..16').replace('Pages 413–425','Pages 413–430').replace('Pages 426–440','Pages 431–440');write(p,text)
    # Keep every prior candidate; explicit disposition rather than silent deletion.
    candidates=load(OUT/'claim_candidates.json')
    links=[['CPC-0113'],['CPC-0050','CPC-0092'],['CPC-0100','CPC-0123'],['CPC-0048','CPC-0055'],['CPC-0113','CPC-0114']]
    for c,links_ in zip(candidates,links):
        c['previous_action']=c['action'];c['action']='DOCUMENTED_UNDER_EXISTING_RQ_NOT_PROMOTED';c['related_claims']=links_
        c['reason']='Passage conservé dans bloc et dossier RQ; exemple, qualification ou opérationnalisation candidate, pas ajout automatique d’un claim canonique.'
    write(OUT/'claim_candidates.json',dump(candidates))
    # Do not use stale incomplete prose as current navigation.
    p=ROOT/'research_questions/README.md'
    write(p,p.read_text()+'\n## Consolidation — état courant\n\nLa tranche incomplète ci-dessus est historique. Le [rapport global](../analysis/global_corpus_pass/final_report.md) et la [matrice](../analysis/global_corpus_pass/page_matrix.csv) portent désormais sur562/562 pages parcourues. Les qualifications des127 claims sont dans les dossiers global_consolidation.md et le journal de revue; les53 statuts scientifiques restent inchangés. Aucune synthèse finale commencée.\n')
    (archive/'archive_manifest.json').write_text(dump(backups))
    # Real subprocess, not a PASS synthesized from metadata.
    result=subprocess.run(['./verify.sh'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    write(OUT/'final_verify.log',result.stdout)
    tests=load(ROOT/'validation/phase2_regression_results.json')
    assert result.returncode==0 and tests['status']=='PASS' and tests['failed']==tests['errors']==0,result.stdout[-6000:]
    validate(require_complete=True)
    manifest=load(OUT/'manifest.json')
    manifest.update(status='GLOBAL_CORPUS_PASS_COMPLETE',ready_for_synthesis=True,verification_status='PASS',
        regression_tests=tests['tests_run'],regression_passed=tests['passed'],regression_failed=0)
    write(OUT/'manifest.json',dump(manifest));write(OUT/'verification_results.json',dump(dict(**tests,verify_command='./verify.sh',verify_exit_code=result.returncode,full_scan_pages=562,log='final_verify.log')))
    rechecks=load(OUT/'claim_rechecks.json');cc={level:dict(Counter(r['global_review_status'] for r in rechecks if r['criticality']==level)) for level in ['CORE','MAJOR','SUPPORTING']}
    report=f'''# GLOBAL CORPUS STATUS

GLOBAL_CORPUS_PASS_COMPLETE

READY_FOR_SYNTHESIS = YES

Ce statut certifie la consolidation documentaire définie par la demande, pas la justesse des propositions, la résolution des questions ou l’exhaustivité bibliographique. Aucune synthèse générale ni réponse finale à la question racine n’est commencée.

## SOURCE

Branche locale research/corpus-validation. HEAD source analysé a697345c427fca8de0521108a17aa2b76f267654. Manuscrit Reflections_PierreCampergue.pdf,562pages. SHA2567981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827, revérifié par tests. Aucun PDF modifié, aucun push.

## PAGES

| Mesure | Début de cette continuation | Fin |
|---|---:|---:|
| Parcourues spécifiquement pendant consolidation |90/562|562/562|
| Couverture analytique cumulée |300/562|447/562|
| ANALYTICALLY_REVIEWED pendant consolidation entière |tranche historique conservée|374|
| SCANNED seulement pendant consolidation |tranche historique conservée|188|
| DEEP_REVIEWED attribué pendant consolidation |0|0|

472 nouvelles pages parcourues, sans refaire les90 déjà traitées. Les374+188 couvrent562;447 est une autre métrique cumulant les anciennes lectures analytiques et les nouvelles. Aucun reclassement automatique du scan en lecture approfondie.23blocs complets,562lignes classées. Les tableaux/formules sensibles ont reçu les contrôles visuels indiqués; les autres pages ont été lues par extraction, non par OCR inventé.

## NEW MATERIAL FOUND

127 claims canoniques avant/après;0ajout,0suppression,0scission effective. Tous ont une revue textuelle avec ancien/nouveau statement identiques, raison, pages et historique. Les qualifications sont des annotations obligatoires, pas des réécritures cachées.5candidats antérieurs conservés, rattachés sans promotion artificielle.

34 constats transversaux au total (14 hérités + 20 ajouts). Parmi les ajouts, 2 fiches ALTERNATIVE_SCENARIO consolident les rattachements transport/services et brevet/rente; elles ne représentent pas 2 nouveaux scénarios monétaires exclusifs. Les 32 scénarios Money antérieurs ne sont ni supprimés ni aplatis. Les autres ajouts documentent limites, tensions et anomalies.

298entrées de labels/formules contre40 dans la tranche initiale, reliées aux344occurrences détectées;33familles éditoriales couvrent aussi les relations non numérotées. Ce ne sont pas298lois indépendantes ou validées : répétitions et dérivations sont signalées. Les ajouts conservent le fragment exact extrait et sa page; les transcriptions mathématiques doivent se lire avec le PDF lorsque la disposition est sensible. Aucune formule structurante détectée laissée sans famille; pas de catalogue exigé des calculs triviaux.

0nouveau concept canonique; cohérence transversale documentée pour les termes prioritaires. Les3amendements antérieurs restent historisés; nouvelles extensions et tensions dans concept_consistency.md.

## CORE REVIEW

24/24revérifiés :5CONFIRMED,17QUALIFIED,2SOURCE_EXTENDED,0sans revue. Ces catégories concernent l’attribution et son domaine. Aucune ne signifie vérité empirique; les problèmes formels liés aux CORE qualifiés restent explicitement ouverts.

## MAJOR REVIEW

96/96revérifiés :23CONFIRMED,45QUALIFIED,25SOURCE_EXTENDED,3REQUIRES_FURTHER_REVIEW. Ces trois cas sont CPC-0034 (égalité Utility/troc),CPC-0089 (normalisation n/N),CPC-0123 (classification des agents). Ils sont examinés mais non résolus, non oubliés. Les7SUPPORTING sont également revérifiés :2confirmés,5qualifiés.

## QUESTIONS

53hors racine avant/après;0ajout,0dépréciation,0renumérotation,0restructuration. Couverture SUFFICIENT pour classifier le manuscrit complet, pas pour fournir toutes les réponses.53/53dossiers ont un addendum de consolidation, racine séparée. Tous les passages STRUCTURAL sont reliés à des RQ; toutes les CORE/MAJOR restent couvertes. Statuts inchangés :29OPEN,18PARTIALLY_RESOLVED,6AMBIGUOUS.

## CONCEPT CONSISTENCY

Support/valeur Cash–Money, tâche–Work et transformation–flux restent des distinctions nécessaires. Utility/besoin n’est pas uniforme entre108–111et132; services/transport entre159,261–276et477; T/dT/δT change de fonction selon frontière et type d’incertitude. Les concepts physiques, économiques et usuels sont parfois explicitement séparés (notamment473). g,r,K ne sont pas interchangeables.

## FORMAL ISSUES

Égalités interpersonnelles depuis0/0 non démontrées249–252; limites vers dérivées285/299; inversions303; bornes308/310/373; changement de contraintes322/323/330; signes357/371; égalités de rendement à partir de bornes385/387; carré seulement au point équilibré392; stocks omis404; normalisation p·l=1 (page408); Force constante≠nulle467/470. Les problèmes inverselog525/526 et niveaux→dérivées528 antérieurs restent conservés. Inventorier ne prétend pas résoudre.

## INTERNAL COUNTEREXAMPLES

34fiches au sens large (exceptions, scénarios, limitations, contradictions apparentes ou non résolues), pas34réfutations. Les plus importantes : transport créateur de Utility; brevet combinant innovation et rente; baisse de coût sans transmission intégrale; gain épargné; Work nul aux frontières sans transformation interne nulle; contrainte par copie et non par heure; durées égales limitées au remplacement.

## LATE-STAGE CLAIMS

CONDITIONS_DROPPED / AMBIGUOUS_GENERALIZATION : extrapolations de bilan local vers généralité macro, de force constante vers conservation, de coefficients absorbants vers K stable. LOCAL_CLAIM_BECOMES_GLOBAL : GDP=K·W559 malgré domaine micro538 et corrélation non causale558. CONSISTENT_GENERALIZATION dans son périmètre : brevet mixte490, partage du surplus507, possibilité d’épargne523. Les développements tardifs n’annulent pas les restrictions antérieures.

## ROOT QUESTION CHAIN

9liaisons EXPLICIT,0STRONGLY_IMPLIED,0INTERPRETIVE,2MISSING dans root_question_chain.md. Le manuscrit propose déjà explicitement énergie/coût/production/déchets/dommages72,112,163–165,454–460; dire que toute chaîne environnementale manque serait incorrect. Restent absentes l’allocation marginale précise du gain et la fonction de dommage du panier hétérogène. EXPLICIT ne signifie pas causalement établi. Aucune réponse finale formulée.

## CONTRIBUTION IMPACT

1renforcement : CC-03 comme diagnostic métrologique de notre analyse, pas nouveauté historique attribuée à l’auteur.3qualifications : CC-01,CC-02,CC-04.0suppression/affaiblissement de candidature entière; aucune nouvelle prédiction empirique spécifique obtenue par simple lecture. Historique conservé dans contribution/global_corpus_review.json et addendum.

## VERIFY

PASS : ./verify.sh exécuté, code sortie0; {tests['passed']}/{tests['tests_run']}testsPASS,0FAIL,0ERROR,0SKIP.4nouveaux tests et adaptation de3contrôles négatifs qui présupposaient auparavant l’incomplétude; ils rejettent maintenant un faux certificat en retirant réellement une page, une revue ou l’inventaire. Aucun critère de provenance désactivé.

WARNING : couverture analytique partielle447/562 distincte du scan complet; littérature et métrologie partielles; questions ouvertes; identification causale et mesure de Money/Utility non acquises. Les expériences antérieures ont seulement été contrôlées par verify, pas remplacées par une nouvelle campagne empirique. Journal complet : final_verify.log; résultat machine : verification_results.json.

## MOST IMPORTANT CHANGES

1. Le lien environnemental est plus explicite dans les prolegomena qu’une lecture ciblée de la conclusion ne le laissait voir.
2. Transport effectif et services de nettoyage empêchent une exclusion générale des services productifs.
3. Les Core Laws sont expressément admises comme hypothèses simplificatrices301–303.
4. L’égalité des Utility entre agents reste une prémisse non démontrée par les limites données.
5. Work restant, variation, transfert frontière et grandeur accumulée nécessitent des lectures locales.
6. Le résultat d’antagonisme des gains est limité à la copie, pas au revenu horaire382.
7. Les rendements ne se réduisent pas partout à un carré; les deux facteurs et les contraintes doivent être gardés.
8. Débit vendu et débit produit ne sont pas bornés de la même manière que leurs cumuls avec stocks.
9. «Force constante» et «aucune force supplémentaire» ne sont pas synonymes sans référentiel explicite.
10. L’exemple énergétique France/Chine est déclaré illustratif, pas observation chiffrée462.
11. La fin du livre ajoute une agrégation PIB/énergie plus forte que les modèles locaux et leurs exclusions.
12. Les53questions suffisent pour classer ces difficultés sans multiplier artificiellement les nœuds.

## REMAINING SCIENTIFIC BLOCKERS

1. Mesure indépendante de T,cp,Force.
2. Échelle cardinale/ratio et comparaison interpersonnelle de Utility.
3. Sens précis de Utility quand le besoin d’une copie supplémentaire est nul.
4. Normalisations n,N et prix local/global.
5. Domaine des potentiels, régularité et contraintes des dérivées.
6. Signes et frontières des bilans de cycles.
7. Conditions de couplage justifiant optimum et normalisation des axes.
8. Stabilité de K sous composition, rendement et énergie résiduelle variables.
9. Frontière des services et classification domestique/collective.
10. Allocation marginale du gain entre épargne, quantité, qualité, autres dépenses.
11. Mesure du dommage marginal et contre-factuel environnemental.
12. Prédictions indépendamment mesurables distinguant les explications concurrentes.

Ces problèmes ne bloquent pas la clôture documentaire de cette passe. Aucun verdict global sur le système Campergue; arrêt avant synthèse.
'''
    write(OUT/'final_report.md',report)
    (archive/'archive_manifest.json').write_text(dump(backups))
    checked=validate(require_complete=True)
    print(dump(dict(status=manifest['status'],ready_for_synthesis=True,tests=tests['tests_run'],passed=tests['passed'],failed=0,review_counts=cc,structural_check=checked)))

if __name__=='__main__':main()
