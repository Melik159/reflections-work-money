# RQ-03.03 — Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?

## Why it matters

Parent : [RQ-03](../RQ-03/README.md). Ce problème précise une condition de réponse à RQ-ROOT ; ses dépendances empêchent de sauter directement du gain à ses dommages.

## Scope

Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ? Périmètre : passages et conditions référencés, sans verdict global.

## Out of scope

Validation de la théorie entière, causalité déduite d’une corrélation ou équivalence automatique des proxies.

## Related claims

CPC-0039, CPC-0043, CPC-0044, CPC-0052, CPC-0054, CPC-0066, CPC-0068

## Related concepts

cash, coefficient, complexity, energy, force, labour, money, price, product, productivity, work

## Dependencies

[RQ-03.01](../RQ-03.01/README.md), [RQ-03.02](../RQ-03.02/README.md)

## Current status

AMBIGUOUS ; confiance MEDIUM.

Première passe approfondie ciblée : oui. Complétude des passages : TARGETED_EXISTING_EVIDENCE_NOT_EXHAUSTIVE.

Chapitres transversaux : CH-03, CH-04, CH-05.

[Corpus](corpus.md) · [Preuves](evidence.md) · [Littérature](literature.md) · [Tests](tests.md) · [Conclusion](conclusion.md)

## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). T est dérivé des lois proposées, non mesuré indépendamment par cette dérivation. L’intégrale de FP dl n’offre une voie distincte que si FP est étalonné sans utiliser cp·dω/dt.

Limite: CIRCULAR_OPERATIONALIZATION_RISK. Calibrer cp sur T construit puis tester le même échantillon ne teste rien. Une calibration sur données indépendantes et prédiction hors échantillon pourrait tester une conséquence, pas l’échelle absolue de T.

Statut actuel: AMBIGUOUS. Test proposé: Comparer des procédés à tâche et qualité fixes; définir une indication indépendante de Force puis calibrer cp. Sans cela, test T∝ω²: NEEDS_DEFINITION.
