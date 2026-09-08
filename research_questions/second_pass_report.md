# Deuxième passe — dix questions prioritaires

## QUESTIONS REVIEWED

**10/10 dossiers traités**, ordre : RQ-03.02 → RQ-08.03 → RQ-08.01 → RQ-08.04 → RQ-06.04 → RQ-10.01 → RQ-09.03 → RQ-11.02 → RQ-11.03 → RQ-12.01. La carte préalable distingue dépendances réelles et ordre de travail. Les prérequis hors sélection ne sont pas déclarés résolus.

Chaque dossier conserve corpus et analyses antérieurs, puis ajoute citations directes SOURCE-XX, reconstruction avant critique, soutien, contre-épreuve,3–4 références ciblées, protocoles, statut et quatre composantes de confiance. Limite : **recherche ciblée, pas garantie d’avoir retrouvé tous les passages pertinents des562 pages**. Les nouveaux textes sont séparés des interprétations.

## STATUS CHANGES

| Question | Ancien | Nouveau | Résultat local |
|---|---|---|---|
| RQ-03.02 | OPEN | AMBIGUOUS | Niveaux, intégrales et réserves conciliables localement avec indices, pas un T univoque global |
| RQ-08.03 | OPEN | AMBIGUOUS | Règle du produit cohérente sous hypothèses ; absence de pertes ne prouve pas l’exactitude |
| RQ-08.01 | OPEN | PARTIALLY_RESOLVED | Additivité de certains caractères, refus explicite de sommer Utility p108 |
| RQ-08.04 | OPEN | AMBIGUOUS | Échelles et coefficients nécessaires ; substitution p554 problématique sous lecture littérale |
| RQ-06.04 | OPEN | PARTIALLY_RESOLVED | Bilans des32 scénarios conservés ; création bancaire de dépôts distincte de Money |
| RQ-10.01 | OPEN | PARTIALLY_RESOLVED | Gain à panier fixe distinct de ses usages : réserve, autres achats, dette, taxes |
| RQ-09.03 | OPEN | PARTIALLY_RESOLVED | K strict constant testable sur proxies ; pont physique/T/M toujours non identifié |
| RQ-11.02 | OPEN | PARTIALLY_RESOLVED | Réaffectation proche du rebond indirect, mais pertes techniques ≠ rebond de demande |
| RQ-11.03 | OPEN | OPEN | Pressions et ressources explicites ; empreinte marginale et fonction de dommages absentes |
| RQ-12.01 | OPEN | PARTIALLY_RESOLVED | Restrictions comparatives candidates, aucune signature globale démontrée |

Confiance globale de chaque dossier : MEDIUM, jugement de reconstruction et non probabilité de vérité. Sous-scores TEXTUAL/FORMAL/EMPIRICAL/LITERATURE dans les dossiers et le graphe, sans moyenne. Une confiance textuelle HIGH coexiste avec une confiance empirique LOW.

## CORPUS COVERAGE / NEW CLAIMS

247→**271/562**, soit24 nouvelles pages analysées.43 pages directement relues dans la sélection ; pages candidates RAG non examinées non comptées. Note : `analysis/reading_notes/second_question_pass.md`. PDF original intact. **0 nouveau claim**,127 conservés ; nouvelles précisions reliées comme preuves directes plutôt que claims artificiellement multipliés.

## LITERATURE

19 références distinctes mobilisées :17 VERIFIED et2 PARTIALLY_VERIFIED. Parmi elles7 nouvelles notices,6 VERIFIED et1 PARTIALLY_VERIFIED. Vérifier une notice ou lire un résumé n’est pas lire intégralement l’ouvrage : accès détaillés conservés. NBER reste limité ; article de Wiedmann inaccessible directement via sa page institutionnelle, métadonnées/résumé indexés seulement. Sources nouvelles : OpenStax travail-énergie et champs conservatifs, BIPM, BCE, Gillingham/Rapson/Wagner, Wiedmann et UNEP. Aucun DOI inventé. Registre de passe : `second_pass_literature.json` ; nouvelles notices BibTeX dans `bibliography/second_pass_research.bib`.

## FORMAL RESULTS

1. **Niveau/variation** : cp=2, ω3→4 donne T9→16, variation7 ; à vitesse constante variation0 n’impose pas niveau0. cp variable requiert un terme supplémentaire.
2. **Agrégation** : test à deux produits antérieur conservé et recalculé ; trois produits donnent indice pondéré0,92 versus moyenne égale0,933333. K locaux fixes donnent K agrégé72/43→44/51 par composition seule.
3. **Potentiels** : contrôle positif d(xy), intégrale1 sur deux chemins ; y·dx donne0 ou1. Des endpoints et une étiquette « sans pertes » ne suffisent pas à l’intégrabilité.
4. **Métrique** : p554 inspectée visuellement. Avec cp2,ca3,e4,a9, substitution des vitesses donne norme carrée13 versus35 dans l’expression à coefficients non carrés. Conclusion conditionnelle aux mêmes variables et absence de normalisation cachée ; aucune correction silencieuse.
5. **Money** : exemple fini ΔM31, approximation linéaire30, terme croisé1. Le différentiel n’est pas une règle exacte de grands changements finis sans terme croisé.

Ces cinq diagnostics sont synthétiques et conditionnels, pas des confirmations empiriques.

## EMPIRICAL RESULTS

Aucune collecte nouvelle ni nouvelle régression. Les expériences E1/E2/E3 indépendantes et le cas électrique antérieur sont réexécutés par verify.sh, avec comparaison des snapshots. Variation du ratio PIB/énergie : contre-épreuve à K strict constant sur les proxies retenus. Coût combustible/prix résidentiel : frontières non appariées, donc pas mesure de profit ni transmission structurelle. Nouveaux protocoles de pertes, Core Law, crédit et empreinte : **DESIGNED_NOT_EXECUTED**.

## COUNTEREVIDENCE / STRONGEST SUPPORT

Soutien le plus net : attribution textuelle de Utility non additive p108 ; référents pos/neg explicités p553 ; épargne et paiements ultérieurs p255/468 ; coexistence des scénarios monétaires p18. Ces passages permettent une reconstruction plus fidèle et réduisent le risque de caricature.

Contre-épreuves : composition variable à K locaux fixes ; dépendance d’un champ non normalisé aux unités ; intégrabilité non déduite des endpoints ; substitution p554 ; usage trop large de δQ=T·dS p113 sans réversibilité. La revue externe de rebond qualifie un backfire universel, mais ne réfute pas toutes les liaisons énergétiques de Campergue.

## STRONGEST PROBLEMS

Mesure indépendante de T/Utility/Money ; constance et unités de cp/ca ; normalisation micro/macro ; confusion possible entre vitesse physique, débit et durée de fabrication ; sélection des branches ; empreinte marginale et dommages. P112/163/165 contiennent des assertions fortes sur pertes/dommages quadratiques qui nécessitent un test propre, pas une corrélation macro.

## RQ-12.01

Table complète : `RQ-12.01/discrimination.md`.

- PURELY_DEFINITIONAL : M=n·u.
- NON_SPECIFIC : transmission à profit constant, prix maintenu, réaffectation de gain/rebond sans restriction additionnelle.
- SPECIFIC_BUT_NOT_YET_TESTABLE : Work quadratique, Core Law sous mesures indépendantes, bornes de pertes/vitesse et dommages/vitesse.
- SPECIFIC_AND_TESTABLE **sur proxies fixés seulement** : K macro strict constant face à une alternative de K variable. Cela ne mesure pas T/M complets.
- NOT_IDENTIFIED : compensation réelle du crédit sans mesure commune de u/M et horizon fixé.

Spécificité ici = restriction face aux alternatives indiquées, pas originalité historique prouvée. Trois protocoles discriminants proposés : procédé à vitesse/quantité/qualité contrôlées ; mesure indépendante de Force/Utility/complexité ; K calibré puis prédit hors échantillon. Aucun verdict global.

## RESOLVED_WITHIN_SCOPE / BLOCKING QUESTIONS REMAINING

Aucune question déclarée RESOLVED_WITHIN_SCOPE : dépendances ouvertes et portée source encore ciblée. Les16 questions BLOCKING restent non entièrement résolues. Priorités particulièrement contraignantes : RQ-03.03, RQ-05.03, RQ-06.01, RQ-08.01, RQ-09.02, RQ-10.02 et RQ-11.01.

## VERIFY

Résultat d’exécution final enregistré dans `validation/phase2_regression_results.json`. Les questions OPEN/AMBIGUOUS et la couverture partielle restent des WARNING ; seules incohérences structurelles et régressions reproductibles provoquent FAIL. Aucun résultat scientifique n’est promu pour obtenir PASS.

`./verify.sh` : **72 tests exécutés,72 PASS,0 échec,0 erreur**, dont8 contrôles nouveaux de cette passe. Les cinq diagnostics formels et les anciens résultats énergétiques/micro sont recalculés et comparés aux snapshots.

## NEXT QUESTIONS

RQ-03.03, RQ-05.03, RQ-08.02, RQ-09.02, RQ-10.02, RQ-11.01, RQ-12.02, RQ-04.04, RQ-01.03, RQ-05.01. Avant de multiplier les expériences : rendre les concepts propriétaires opérationnels et fixer les restrictions qui pourraient réellement échouer.

## Historique

États des dossiers avant modification sous `history/second_pass_before/`, transitions dans history.json, graphe version2. Aucun ID renommé, aucune dépendance modifiée silencieusement. Les compléments demandés sur Money et usages du gain renvoient aux questions adjacentes sans remplacer les intitulés originaux RQ-06.04 et RQ-10.01.
