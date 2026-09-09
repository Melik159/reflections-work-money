# RQ-03.03 — Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?

## STATUS

AMBIGUOUS

## WHAT_CAMPERGUE_CLAIMS

CPC-0039 : Economic Work et Money sont posés comme deux formes d’énergie économique.

CPC-0043 : Le principe d’équivalence est écrit M=g.T.

CPC-0044 : La constance du coefficient g n’est pas garantie en économie.

CPC-0052 : Pour une tâche constante, Work dépend de sa vitesse d’exécution.

CPC-0054 : La complexité désigne l’inertie du produit face au changement de vitesse d’exécution de la tâche.

CPC-0066 : Les complexités du Product et de Cash ne sont pas égales malgré une notation c parfois commune.

CPC-0068 : Les relations de vitesse mesurent les évolutions sans en déterminer les causes.

Reformulations ci-dessus : INTERPRETATION ; citations exactes séparées dans corpus.md.

## WHAT_IS_DERIVED

Sous cp constant et référent fixé, intégrer cp·ω·dω donne une différence quadratique ; cela ne produit pas une observation indépendante.

## WHAT_EVIDENCE_SUPPORTS

Les extraits attestent les affirmations ; les conditions restent obligatoires.

## WHAT_EVIDENCE_QUALIFIES

Le cas électrique ne mesure ni tâche homogène ni Utility ; son efficacité thermique ne comble pas ces lacunes.

## WHAT_EVIDENCE_CONTRADICTS

Aucune contradiction globale établie. Les tensions et données non discriminantes ne sont pas converties en contradiction.

## WHAT_REMAINS_UNKNOWN

Procédure de mesure indépendante, invariance au choix d’unité de tâche et éventuel coefficient variable.

## PROVISIONAL_ANSWER

Les dimensions peuvent être exprimées symboliquement, mais aucune calibration indépendante de cp, Force et T n’est disponible dans le cas micro. Calculer T depuis ω puis vérifier la même équation serait circulaire.

## CONFIDENCE

MEDIUM


## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). T est dérivé des lois proposées, non mesuré indépendamment par cette dérivation. L’intégrale de FP dl n’offre une voie distincte que si FP est étalonné sans utiliser cp·dω/dt.

Limite: CIRCULAR_OPERATIONALIZATION_RISK. Calibrer cp sur T construit puis tester le même échantillon ne teste rien. Une calibration sur données indépendantes et prédiction hors échantillon pourrait tester une conséquence, pas l’échelle absolue de T.

Statut actuel: AMBIGUOUS. Test proposé: Comparer des procédés à tâche et qualité fixes; définir une indication indépendante de Force puis calibrer cp. Sans cela, test T∝ω²: NEEDS_DEFINITION.

## Quatrième passe — EXP-09

État E, réserve R et transfert T[a,b] ont des compatibilités locales distinctes. Le transfert signé télescope; cumul positif et réserve ne sont pas la primitive. cp variable exige un terme supplémentaire; aucune mesure indépendante de T.

Preuve formelle EVID-FOURTH-EXP-09-RQ-03.03, relation QUALIFIES. [Protocole figé](../experiments/EXP-09/protocol.md), [résultats et limites](../experiments/EXP-09/results.md). Calcul exécuté, non observation de T/Utility/Money.

Statut de la question conservé: AMBIGUOUS; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.
