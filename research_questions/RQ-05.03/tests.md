# RQ-05.03 — Utility peut-elle être mesurée indépendamment du prix et de la quantité pour comparer les scénarios ?

Types : EMPIRICAL_TEST. Statut du protocole : DESIGNED_FIRST_PASS.

COUNTEREXAMPLE/EMPIRICAL_TEST : préférences et caractéristiques indépendantes du prix ; conserver produit et agent ; tester invariance aux échelles. Incompatible avec agrégat univoque : signe global changeant sous normalisations également admissibles.

Explication concurrente : Indices hédoniques et préférences ordinales ne mesurent pas automatiquement Utility Campergue.

Artefact déjà disponible (pas une nouvelle expérience exécutée ici) : `analysis/empirical/micro_electricity/two_product_results.json`.

Les tests de cohérence de verify.sh vérifient ce dossier et ses liens ; ils ne résolvent pas sa question scientifique.

## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). Le manuscrit reconnaît explicitement p109 que Utility ne dispose pas de mesure, mais propose un classement. Cela ne suffit pas à déterminer UP2/UP1 dans les rendements.

Limite: Classements invariants sous transformation croissante; rapports non invariants. WTP dépend de revenu et alternatives; qualité ignore utilité symbolique, don et erreur. Absence de procédure retrouvée n’est pas impossibilité future.

Statut actuel: AMBIGUOUS. Test proposé: Faire classer mêmes objets par mêmes agents à contextes fixés; comparer classements et service technique. Cela teste stabilité ordinale, pas échelle cardinale Campergue.

## Quatrième passe — EXP-02

Ordre/égalité/signes restent définis sous recodage croissant commun; différences et ratios numériques exigent des structures distinctes. PDF349 ne requiert pas d’origine absolue si le coefficient covarie; PDF386 exige une échelle de rapport.

Preuve formelle EVID-FOURTH-EXP-02-RQ-05.03, relation QUALIFIES. [Protocole figé](../experiments/EXP-02/protocol.md), [résultats et limites](../experiments/EXP-02/results.md). Calcul exécuté, non observation de T/Utility/Money.

Statut de la question conservé: AMBIGUOUS; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.
