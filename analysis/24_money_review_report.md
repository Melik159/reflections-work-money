# MONEY/COMPENSATION REVIEW

**QUALIFIED** — révision ciblée du 8 septembre 2026, sans verdict global.

Source : branche `research/corpus-validation`, HEAD `a697345c427fca8de0521108a17aa2b76f267654`. PDF original intact; SHA-256 vérifié par la suite de tests. Couverture progressive : **121/562** pages, contre61 avant cette passe. Recherche lexicale sur toutes les pages indexées, lecture analytique ciblée; exhaustivité absolue des scénarios non certifiée.

## SCENARIOS FOUND

**32 entrées**, de niveaux différents et non mutuellement exclusives :

- 11 régimes : stabilité; émission compensée; retrait compensé; création à n constant; destruction à n constant; émission à u constant; retrait à u constant; inflation2a1; dévaluation2a2; déflation2b1; réévaluation2b2.
- 4 configurations prix/utilité : enrichissement, déflation, inflation, appauvrissement.
- 17 applications ou limites : dénomination; redistribution; crédit; inertie; support métallique/confiance; hyperinflation; thésaurisation; change extérieur; mélanges; couplage spéculatif; variations de même signe exclues; marge sans transmission du gain; agrégation n/N; appréciation spéculative temporaire; cycle bouclé par dévaluation; cycle bouclé par Work pour les intérêts; non-neutralité réciproque entre acteurs (trois sous-cas).

Inventaire et citations : [rapport détaillé](24_money_compensation_scenarios.md), [JSON](data/money_compensation_scenarios.json).

## CLAIMS REVIEWED

41 claims antérieurs revus : KEEP34, QUALIFY6, SPLIT1, MERGE0, REWRITE0, RETRACT0. **25 claims ajoutés**, CPC-0069 à CPC-0093; total actuel93. Les formulations initiales et les raisons des changements figurent dans [le journal](data/money_claim_revision_log.json). Aucune citation initiale supprimée pour rendre artificiellement le manuscrit plus cohérent.

## PREVIOUS FINDING

> M=n.u ne démontre pas la neutralité : la compensation inverse constitue une hypothèse supplémentaire.

**STATUS : OVER_SIMPLIFIED.** Exact comme non-implication algébrique, insuffisant comme reconstruction du manuscrit.

Nouvelle formulation : Campergue distingue M global constant et variable. La compensation inverse découle conditionnellement de M constant; la création/destruction productive peut modifier u à n constant, ou s’accompagner d’un ajustement de n maintenant u constant. Redistribution, inertie, mélanges et évolutions incohérentes sont explicitement traités. La critique doit porter sur les conditions, leur sélection causale et les horizons de retour, pas sur une déduction uniforme de neutralité à partir de l’identité seule.

## ARGUMENT GRAPH

126 nœuds,138 arêtes. Branches SC-MONEY explicites, conditions conservées, raccourcis directs identité→neutralité générale retirés. Convention DEPENDS_ON uniformisée de prémisse vers dépendant et changements consignés dans [le journal du graphe](data/money_graph_revision_log.json). Aucune dépendance cyclique détectée par le test exécuté.

## LITERATURE COMPARISON

Le contraste dépôts/money institutionnel versus Cash/Money chez Campergue ne constitue pas seul une contradiction. Comparaison Banque d’Angleterre réexaminée sur le PDF primaire; traduction détaillée [ici](24_money_literature_translation.md). Les deux anciennes relations CONTRADICTS visant une neutralité générale passent à UNCLEAR avec historique. Le nouvel accès NBER est refusé403; pas de nouvelle vérification intégrale revendiquée.

Les oppositions substantielles à tester concernent la compensation nécessaire, l’exclusion bancaire des autres branches, la causalité de la confiance et le retour final exact. Aucune réfutation empirique indépendante de ces restrictions n’a été établie dans cette passe.

## REGRESSION

`./verify.sh` réellement exécuté : **PASS,32 tests réussis,0 échec,0 erreur**, dont7 nouveaux. Les contrôles empiriques existants ont aussi été réexécutés; aucun nouveau résultat causal revendiqué. FORM-002 conserve son arithmétique mais précise sa compatibilité conditionnelle avec4a.

Un premier échec venait d’un marqueur textuel trop littéral du nouveau test visuel, pas d’une source corrompue; résultat conservé dans `history/pre_money_review/initial_money_test_failure.json`. Le contrôle final vérifie aussi les directions transcrites. Deux erreurs de lecture initiale du tableau531 ont été corrigées après agrandissement, sans les imputer à l’auteur.

WARNING : couverture, bibliographie et mécanismes causaux incomplets; libellés Constant/Current, comparaison des variations absolues/relatives, Td en2a2 aux pages531/532, inflation/pouvoir d’achat24/291, agrégation n/N et horizon final restent ouverts.

## MAIN RESULT

Cash désigne le support, Money sa valeur; augmenter les unités n’est donc pas définir une richesse nouvelle.
La compensation inverse appartient à une branche où Money global est tenu constant.
La branche productive permet, elle, création ou destruction de Money et plusieurs ajustements de n/u.
Le manuscrit admet effets redistributifs, retards, anomalies, corrections et coexistence de régimes.
Il nie même expressément la neutralité des décisions entre acteurs, sans abandonner ses invariants globaux revendiqués.
Ce pluralisme ne suffit pas à démontrer ses restrictions causales, et ses généralisations fortes restent à articuler avec les cas particuliers.
Notre précédente synthèse devait donc être révisée, sans remplacer une caricature défavorable par une version artificiellement affaiblie du texte.

## Fichiers et état local

Livrables principaux : rapport24, scénariosJSON, traduction bibliographique, journaux des claims/graphe/littérature, contrôles visuels, audit de recherche, notes de lecture, scripts éditoriaux et sept tests additionnels. Claims, concepts, graphe, chapitres, questions, HYP-0007, matrice, couverture, fiches CORE concernées, README et verify.sh actualisés. États antérieurs archivés dans `analysis/history/pre_money_review/`.

Aucun push ni commit effectué. Les fichiers de recherche étaient déjà non suivis dans Git; ils le restent. Les fichiers suivis d’origine ne sont pas modifiés.
