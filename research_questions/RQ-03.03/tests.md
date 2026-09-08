# RQ-03.03 — Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?

Types : EMPIRICAL_TEST, FORMAL_TEST. Statut du protocole : DESIGNED_FIRST_PASS.

EMPIRICAL_TEST/FORMAL_TEST : mesurer tâche, temps, coût, qualité et une force/complexité indépendamment ; prévoir ΔT avant le résultat. Incompatible : ΔT indépendant hors prédiction à conditions satisfaites. Actuellement NOT_IDENTIFIABLE.

Explication concurrente : Production standard, composition du parc et substitution capital/travail peuvent produire la même efficacité sans T.

Artefact déjà disponible (pas une nouvelle expérience exécutée ici) : `analysis/32_dimensional_consistency.md`.

Les tests de cohérence de verify.sh vérifient ce dossier et ses liens ; ils ne résolvent pas sa question scientifique.

## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). T est dérivé des lois proposées, non mesuré indépendamment par cette dérivation. L’intégrale de FP dl n’offre une voie distincte que si FP est étalonné sans utiliser cp·dω/dt.

Limite: CIRCULAR_OPERATIONALIZATION_RISK. Calibrer cp sur T construit puis tester le même échantillon ne teste rien. Une calibration sur données indépendantes et prédiction hors échantillon pourrait tester une conséquence, pas l’échelle absolue de T.

Statut actuel: AMBIGUOUS. Test proposé: Comparer des procédés à tâche et qualité fixes; définir une indication indépendante de Force puis calibrer cp. Sans cela, test T∝ω²: NEEDS_DEFINITION.

## Quatrième passe — EXP-09

État E, réserve R et transfert T[a,b] ont des compatibilités locales distinctes. Le transfert signé télescope; cumul positif et réserve ne sont pas la primitive. cp variable exige un terme supplémentaire; aucune mesure indépendante de T.

Preuve formelle EVID-FOURTH-EXP-09-RQ-03.03, relation QUALIFIES. [Protocole figé](../experiments/EXP-09/protocol.md), [résultats et limites](../experiments/EXP-09/results.md). Calcul exécuté, non observation de T/Utility/Money.

Statut de la question conservé: AMBIGUOUS; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.
