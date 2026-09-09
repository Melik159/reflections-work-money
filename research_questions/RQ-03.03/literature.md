# RQ-03.03 — Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?

## BIB-0002

OECD (2001). [Measuring Productivity - OECD Manual](https://www.oecd.org/content/dam/oecd/en/publications/reports/2001/07/measuring-productivity-oecd-manual_g1gh2484/9789264194519-en.pdf).

Relation : QUALIFIES ; question : RQ-03.03. Résultat pertinent : Les conventions de mesure des facteurs doivent être explicitées.

Localisation et accès : PDF pp12,116–119; printed pp11,115–118; sections 2.1 and 10 ; Institutional manual; selected passages inspected.

Vérification héritée : VERIFIED. Limite : Réutilisation ciblée du registre existant ; ce lien ne prouve pas le formalisme complet.


## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). T est dérivé des lois proposées, non mesuré indépendamment par cette dérivation. L’intégrale de FP dl n’offre une voie distincte que si FP est étalonné sans utiliser cp·dω/dt.

Limite: CIRCULAR_OPERATIONALIZATION_RISK. Calibrer cp sur T construit puis tester le même échantillon ne teste rien. Une calibration sur données indépendantes et prédiction hors échantillon pourrait tester une conséquence, pas l’échelle absolue de T.

Statut actuel: AMBIGUOUS. Test proposé: Comparer des procédés à tâche et qualité fixes; définir une indication indépendante de Force puis calibrer cp. Sans cela, test T∝ω²: NEEDS_DEFINITION.
