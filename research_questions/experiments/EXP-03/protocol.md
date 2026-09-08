# EXP-03 — Protocole figé

## QUESTION

RQ-08.02

## CLAIMS

CPC-0044, CPC-0109, CPC-0117, CPC-0118

## CAMPERGUE_PREDICTION

PDF559 suppose que davantage de Products stabilisent K. Tester précisément quelles restrictions de composition rendent possible la stabilité; ne pas postuler stabilité ou variation universelle.

## ALTERNATIVE_PREDICTION

K agrégé est une moyenne pondérée de Ki seulement si M et T additifs et unités/frontières compatibles. Ki identiques peuvent rendre K indépendant des proportions; Ki différents permettent aussi compensations particulières.

## VARIABLES

T, Money, K

## MEASUREMENT_LEVELS

VAR-01:L1, VAR-07:L1, VAR-11:L1

## DATA

Sources PDF [202, 559]; paramètres synthétiques déclarés ci-dessous. Aucun nouveau jeu empirique.

## PREPROCESSING

Aucun filtrage de données empiriques. Unités/référents déclarés; valeurs synthétiques non estimées.

## MODEL / FORMAL_TEST

Calcul rationnel exact. Trois produits Ki=[1,2,3], Ti=[1,2,1]; toutes quantités qi dans {1,2,3}. Comparer deux et trois produits, coefficients identiques, réplication par7, changement de poids, composition [1,1,1]→[2,1,2]. Tester normalisation Ti’=siTi et Ki’=Ki/si, si=[2,3,5], avec retour à l’unité commune avant agrégation; tester changement commun d’unité.

## SUCCESS_CRITERION

Invariance sous réplication commune; invariance à toute composition positive si tous Ki égaux; condition nécessaire/suffisante pour deux compositions: somme (wi’−wi)Ki=0, sous Ki fixes et poids normalisés.

## QUALIFICATION_CRITERION

Composition variable peut préserver K par compensation; nombre de produits seul ne garantit pas convergence sans hypothèses de distribution/pondérations.

## CONTRADICTION_CRITERION

Exemple qui contredit l’affirmation inconditionnelle de stabilité par simple multiplication du nombre de produits; conclusion limitée à cette généralisation, pas aux couplages conditionnels.

## NON_IDENTIFICATION_CRITERION

Ti et Mi synthétiques ne sont pas des mesures économiques; ni loi empirique ni calibration de K.

## LIMITATIONS

Ti>0 et dénominateur non nul dans le test. Signes mixtes excluent la lecture convexe. Utility non additive jamais agrégée.

## NOVELTY_AND_HISTORY

Extension: condition analytique de stabilité, compensation avec recomposition, énumération, coefficients identiques et normalisation covariante.

