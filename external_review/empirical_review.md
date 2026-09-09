# Revue empirique

| test | DATA_VALID | DESIGN_VALID | RESULT_REPRODUCED | INTERPRETATION_VALID |
|---|---|---|---|---|
| 30 modèles PIB–énergie archivés | Fichiers et indépendance PIB contrôlés; pas nouvel audit statistique amont | Descriptif seulement; tendances, composition, chocs et causalité inverse | YES: OLS/HAC recalculés indépendamment, tolérance1e-8 | Association/co-mouvement; NON_DISCRIMINATING, aucun pont Energy→Money observé |
| Modèle électrique N20 | Données archivées; proxy gaz ≠ coût total apparié | Diagnostic limité, pas pass-through causal | YES: coefficient,SE,R² tolérance1e-10 | NOT_IDENTIFIABLE pour marge/transmission/Money; limite interne confirmée |
| +78% | Scénario construit, pas données physiques | Arithmétique conditionnelle | YES via suite; (8/6)²−1 | Pas validation de loi empirique universelle |
| K, Utility, T/dT | Exemples synthétiques explicites | Tests formels locaux, pas échantillon économique | YES: diagnostics externes et suite | Qualifie hypothèses/échelles; ne mesure pas variables latentes |

Le premier essai du reviewer a rencontré une instabilité numérique de son inversion matricielle; correction consignée dans calculation_history.md. Les résultats finaux concordent. La circularité de la série ancienne doit être évaluée sur sa filiation, pas sur la seule apparition algébrique du PIB dans un ratio. Aucun test énergétique redondant nouveau n’a été présenté comme découverte.
