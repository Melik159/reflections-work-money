# EXP-09 — Protocole figé

## QUESTION

RQ-03.02, RQ-03.03

## CLAIMS

CPC-0040, CPC-0052, CPC-0054, CPC-0066, CPC-0068, CPC-0121

## CAMPERGUE_PREDICTION

PDF207 donne une primitive quadratique; PDF471 écrit T comme différence entre deux instants; PDF472 compense cinétique et réserve potentielle. Comparer ces usages sans imposer un sens unique à toutes les occurrences.

## ALTERNATIVE_PREDICTION

MODEL-A état E=½cpω²; MODEL-B réserve potentielle R, dR=−dE dans un bilan isolé; MODEL-C transfert sur intervalle T[a,b]=E(b)−E(a), suggéré PDF471. Réserve accumulée monotone distincte et non présumée par MODEL-B.

## VARIABLES

T, dT, cp, ω

## MEASUREMENT_LEVELS

VAR-01:L1, VAR-02:L1, VAR-03:L1, VAR-04:L3

## DATA

Sources PDF [197, 203, 207, 471, 472]; paramètres synthétiques déclarés ci-dessous. Aucun nouveau jeu empirique.

## PREPROCESSING

Aucun filtrage de données empiriques. Unités/référents déclarés; valeurs synthétiques non estimées.

## MODEL / FORMAL_TEST

cp=2; trajectoire ω=[1,3,2,1], réserve initiale100. Tester différences signées, retour au point initial, télescopage, cumul positif non signé. Comparer cp variable, ω=2 constante et cp=1→3: différentielle totale vs intégrale cpωdω. Unit change l’=s l impose cp’=cp/s² pour T invariant.

## SUCCESS_CRITERION

Chaque lecture doit conserver les relations et conventions de signe dans son domaine; pas de sélection du modèle qui semble le plus favorable.

## QUALIFICATION_CRITERION

Un même symbole recouvre état, réserve et transfert; indices explicites proposés uniquement comme MINIMAL_RECONSTRUCTION.

## CONTRADICTION_CRITERION

Interpréter la même quantité simultanément comme primitive absolue et transfert fini sans référence produit des égalités incompatibles. Modèle réserve identifiée directement à E incompatible avec conservation sauf variation nulle.

## NON_IDENTIFICATION_CRITERION

Calcul de T depuis la relation quadratique ne constitue jamais test indépendant de cette relation: REQUIRES_INDEPENDENT_T.

## LIMITATIONS

Unités économiques non calibrées; cp variable n’est pas présenté comme domaine effectivement annoncé pour toutes les intégrations. Aucun test empirique.

## NOVELTY_AND_HISTORY

Nouveau ID: sous-problème formel promu DO_NOW. EXP-01 demeure NEEDS_DEFINITION; il n’est pas renommé ni déclaré exécuté.

