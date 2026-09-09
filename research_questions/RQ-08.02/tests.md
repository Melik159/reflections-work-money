# RQ-08.02 — Un grand nombre de produits suffit-il à stabiliser K malgré des coefficients et compositions hétérogènes ?

Types : FORMAL_TEST, EMPIRICAL_TEST. Statut du protocole : DESIGNED_FIRST_PASS.

COUNTEREXAMPLE/FORMAL_TEST : maintenir K locaux et varier composition ; EMPIRICAL_TEST : coefficients fixés hors échantillon. Incompatible avec constance inconditionnelle : K agrégé change sans changement d’unité.

Explication concurrente : Composition sectorielle et hétérogénéité des fonctions de production expliquent des coefficients agrégés variables.

Artefact déjà disponible (pas une nouvelle expérience exécutée ici) : `analysis/empirical/micro_electricity/two_product_results.json`.

Les tests de cohérence de verify.sh vérifient ce dossier et ses liens ; ils ne résolvent pas sa question scientifique.

## Troisième passe — métrologie

Voir [dossier métrologique](metrology.md). K local peut être calibré si M et T sont indépendamment mesurés. K=PIB/énergie est estimable comme ratio de proxies, mais résiduel si recalculé pour chaque observation.

Limite: Un nombre élevé de produits ne suffit pas à stabiliser les poids. K agrégé=ΣKiTi/ΣTi requiert additivité, unités communes, même frontière et absence de double compte. Les Ti économiques restent non opérationnalisés.

Statut actuel: PARTIALLY_RESOLVED. Test proposé: Réutiliser diagnostics deux/trois produits; ajouter réplication à composition fixe: multiplier toutes quantités par le même facteur laisse K identique; composition variable le modifie.

## Quatrième passe — EXP-03

K est stable exactement lorsque la variation pondérée des Ki est nulle, à coefficients fixes. Composition fixe suffit mais n’est pas nécessaire; Ki identiques suffisent pour toute composition. Normalisation exige unité commune ou conversion explicite.

Preuve formelle EVID-FOURTH-EXP-03-RQ-08.02, relation QUALIFIES. [Protocole figé](../experiments/EXP-03/protocol.md), [résultats et limites](../experiments/EXP-03/results.md). Calcul exécuté, non observation de T/Utility/Money.

Statut de la question conservé: PARTIALLY_RESOLVED; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.
