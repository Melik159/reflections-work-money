"""Reconcile metrics and publish explicit incompleteness; preserves prior files."""
import collections
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'

def main():
    progress=ROOT/'analysis/data/phase2_progress.json'
    archive=OUT/'history/baseline/analysis/data/phase2_progress.json'
    if not archive.exists():
        archive.write_bytes(progress.read_bytes())
        baseline=json.loads((OUT/'baseline.json').read_text())
        baseline['artifacts'].append(dict(path='analysis/data/phase2_progress.json',size=archive.stat().st_size,
            sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),archive_note='Added before this metric was modified'))
        (OUT/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
    coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
    data=json.loads(progress.read_text());data['pages_examined']=sum(r['examined'] for r in coverage)
    data['global_consolidation_status']='GLOBAL_CORPUS_PASS_INCOMPLETE'
    data['global_consolidation_note']='90 pages relues dans cette tranche; couverture analytique cumulée300/562; pas certificat intégral.'
    progress.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    addition='\n## Consolidation globale en cours\n\n[Addendum de lecture tardive](global_corpus_addendum.md). Observations locales, pas révision certifiée sur562pages. Les évaluations précédentes sont conservées; aucune originalité ni mesure nouvelle attribuée.\n'
    for name in ['README.md','candidate_contributions.md']:
        p=ROOT/'research_questions/contribution'/name
        if addition not in p.read_text():p.write_text(p.read_text()+addition)
    manifest=json.loads((OUT/'manifest.json').read_text())
    rechecks=json.loads((OUT/'claim_rechecks.json').read_text())
    counters={kind:dict(collections.Counter(r['local_review_status'] or 'PENDING' for r in rechecks if r['criticality']==kind)) for kind in ['CORE','MAJOR']}
    text=f'''# Rapport de consolidation globale — tranche incomplète

## GLOBAL CORPUS STATUS

**GLOBAL_CORPUS_PASS_INCOMPLETE**. Ce rapport est un état de travail, pas un certificat de confrontation au manuscrit complet. La passe comparative était achevée et vérifiée avant cette tranche. Aucune synthèse finale engagée.

## PAGES

- Nouvelle vérification transversale : **90/562 SCANNED_FOR_RELEVANCE**, dont78 ANALYTICALLY_REVIEWED et12 SCANNED. Ces catégories sont emboîtées; ne pas additionner90 et78.
- DEEP_REVIEWED : **0** dans cette tranche; inspection visuelle de14 pages, sans prétendre analyser exhaustivement leurs dépendances.
- Couverture analytique cumulée historique : **272 → 300/562**, soit28 pages nouvelles.
- Pages parcourues :426–450,500–562, ainsi que20 et349 pour rapprochements. **472 pages restent à relire dans cette passe**, y compris celles analysées auparavant.
- Matrice :562 lignes, dont472 UNREVIEWED. Quatre blocs complets parcourus, trois partiels, seize non commencés. Les blocs incomplets restent REQUIRES_REVIEW.

## NEW MATERIAL

Claims canoniques nouveaux :0; total127 conservé. Candidats non encore intégrés :5 (concurrence, location/crédit, services, classement richesse/Core Law, boucle offre-prix-demande).

Claims localement qualifiés :8; source à étendre :11; confirmés localement :10. Aucun énoncé canonique remplacé; historique ancien/nouveau identique et motif de relecture dans claim_rechecks.json. Divisions réalisées :0. Un périmètre de division est proposé pour la généralisation aux services.

Scénarios nouveaux canoniques :0; branches complémentaires et exceptions enregistrées dans14 findings (pas14 nouveaux scénarios). Nouveaux concepts :0; trois notices corrigées avec historique.

Formules :40 fiches sélectionnées, dont25 FORMULA_NEW dans cet inventaire,10 FORMULA_CONFLICT,2 FORMULA_REINTERPRETED,3 FORMULA_ALREADY_COVERED. Une fiche conflit peut avoir un résultat final récupérable. Les344 occurrences automatiques de labels ne sont PAS344 formules structurantes certifiées. Inventaire exhaustif non terminé.

## QUESTIONS

Existantes53, nouvelles0, dépréciées0. Les passages structurels effectivement relus sont rattachés; dossiers supplémentaires global_consolidation.md, sans modification des statuts scientifiques. Suffisance de l'arbre sur562pages : **non encore établie**. Les exemples concurrence/location peuvent être rattachés aux questions actuelles sans multiplication artificielle.

## CORE CLAIMS

24 enregistrements de suivi. Relecture LOCALE : {counters['CORE']}.
Relecture contre CORPUS COMPLET :0/24, donc aucune confirmation intégrale annoncée.

## MAJOR CLAIMS

96 enregistrements de suivi. Relecture LOCALE : {counters['MAJOR']}.
Relecture contre CORPUS COMPLET :0/96. Un contrôle automatique de fidélité de citation n'est pas une relecture sémantique globale.

## CONCEPT CONSISTENCY

Distinctions stables localement : Cash/Money, coût/prix, création/transfert, énergie physique/Work économique. Exceptions importantes : Work accompli utilisé p501/553 malgré règle par défaut du restant; Utility rapportée au Transformer sauf stipulation contraire; champ et évolution temporelle de Utility distingués p546.

Ambiguïtés : cp/ca et unités de norme; P,A et primitives logarithmiques; ajout de N dans normalisation; richesse par respect de Core Law versus Money; exclusion des services et critère de variation Utility. Voir concept_consistency.md.

## INTERNAL COUNTEREXAMPLES

14 entrées de consolidation, typées et sourcées : exceptions, limites, oppositions apparentes et contexte. Principaux cas : profits variables et trois bénéficiaires; location refusée; spéculation exceptée de l'analogie crédit/location; thésaurisation; intermédiaires initialement efficaces; contexte des gradients Utility. Les quatre contre-exemples algébriques calculés sont des constructions de l'analyste, non des données ou exemples attribués à l'auteur.

## LATE-STAGE FINDINGS

P507 approfondit les branches de transmission; p511–522 ajoutent contraintes de ratios et de comparabilité intersupports; p523 distingue création/dépense; p529 exclut PIB avant p559; p534–540 renforcent les exclusions sectorielles; p538 borne explicitement le modèle à une transformation; p546 apporte une explication contextuelle; p560–561 revendiquent différence de concepts sans dossier historique.

## ROOT QUESTION CHAIN

Chaîne PROVISOIRE, non synthèse après lecture entière. Table :5 liens EXPLICIT,1 STRONGLY_IMPLIED,2 MISSING au niveau d'une liaison quantifiée. Une partie des sources environnementales est héritée des passes précédentes et non recomptée comme relue. Gains accessibles ne signifient ni consommation effective automatique ni dommage marginal identifié.

## CONTRIBUTION REVIEW

Aucune candidate ne reçoit de label BY_FULL_CORPUS. Trois candidates qualifiées localement; CC-03 renforce le diagnostic d'exigence métrologique, pas une nouveauté historique de l'auteur. Les quatre évaluations historiques sont conservées et reliées à l'addendum; aucune supériorité empirique établie.

## FORMAL RESULTS

Quatre contrôles nouveaux exécutés :

1. L'inverse du logarithme25-03/04 ne dérive pas le différentiel p525 à coefficients constants.
2. Mc≥Md ne donne pas dMc≥dMd.
3. g constants ne transforment pas cette inégalité en égalité sans condition additionnelle.
4. Les étapes beta imprimées ont un signe incompatible avec leurs définitions, mais les résultats finaux peuvent se déduire correctement de celles-ci.

Images contrôlées pour différencier erreur de PDF et erreur d'extraction; résultats formels locaux, aucun verdict global. Exécution reproductible : `analysis/run_global_local_checks.py --check`.

## VERIFY

Départ : ./verify.sh exécuté,94/94 PASS. Vérification après modifications : **PENDING_FINAL_EXECUTION**. Les tests ajoutés empêchent notamment qu'une matrice complète de lignes soit présentée comme lecture complète. OPEN et couverture inachevée produisent WARNING, non un faux certificat de complétude.

## MAIN CHANGES TO OUR UNDERSTANDING

1. Les exceptions coût/prix ont des destinataires nommés et des effets distributifs de signes divers.
2. Le corpus fournit une tentative explicite de résoudre gradient/constance par coordonnées.
3. Le champ micro/macro est déclaré ne pas être une relation d'agrégation.
4. Les exclusions sectorielles tardives sont plus fortes que le simple critère d'Utility.
5. La thésaurisation rend indispensable une frontière temporelle pour l'égalité PIB/création.
6. Les erreurs d'intégration, de différentiels et de saturation sont distinctes, pas une seule objection vague.
7. Certaines fautes intermédiaires n'empêchent pas la récupération indépendante du résultat final.
8. Location et emprunt demandent des comparaisons entre Utility de supports/agents différents.
9. L'indicateur de richesse par fréquence de Core Law mérite un dossier séparé avant toute mesure.
10. Les notices historiques du lexique doivent être réconciliées avec les travaux plus récents.

## REMAINING BLOCKERS

1. Relire/classer les472 pages restantes de cette passe; ce travail est non réalisé, pas déclaré inaccessible.
2. Compléter la relecture sémantique des24 CORE et96 MAJOR contre ces pages.
3. Inventorier et inspecter les formules structurantes restantes, y compris pages graphiques.
4. Vérifier les sections antérieures sur offre/demande, location et services avant atomisation des cinq candidats.
5. Formaliser les conditions minimales réparant les dérivations récupérables, séparées du texte original.
6. Confronter les53 questions à la totalité du corpus avant statut SUFFICIENT.
7. Achever la revue des quatre contributions candidates sur tout le manuscrit.
8. Vérifier les figures de cycles et conventions locales non encore examinées en profondeur.

Ces limites sont de couverture et d'analyse, pas un blocage externe inventé. Les artefacts sont préparés pour poursuivre sans recommencer la tranche achevée. Les générateurs d'initialisation refusent d'écraser les fichiers divergents : étendre le catalogue et conserver un historique de la tranche avant toute reconstruction.

## READY_FOR_SYNTHESIS

**NO**. Infrastructure contrôlable et nouveaux diagnostics exploitables, mais lecture transversale et certification des claims/formules encore incomplètes. Aucun verdict global, aucun push, PDF source intact.
'''
    target=OUT/'final_report.md'
    if target.exists():raise SystemExit('Report exists; revise explicitly with history')
    target.write_text(text)
    print('Metric reconciliation:',data['pages_examined'],'; partial report written')

if __name__=='__main__':main()
