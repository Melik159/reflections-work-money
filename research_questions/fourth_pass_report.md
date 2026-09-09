# Quatrième passe — expériences sur des relations locales

## EXPERIMENTS SELECTED

EXP-02 (opérations sur Utility), EXP-03 (conditions de stabilité de K), EXP-09 (lectures locales de T/dT). [Table complète de sélection](experiments/selection.md).

EXP-02 et EXP-03 approfondissent des diagnostics déjà exécutés; leurs résultats antérieurs étaient connus et sont explicitement déclarés dans le manifeste. Leurs nouvelles opérations ont été protocolées avant calcul. EXP-09 est un nouveau sous-problème formel promu DO_NOW; il ne remplace pas EXP-01, dont la mesure indépendante reste NEEDS_DEFINITION.

Les expériences de faibles niveaux métrologiques sont retenues ici uniquement pour les questions de cohérence mathématique explicitement demandées. Elles ne deviennent pas empiriquement testables grâce à des nombres synthétiques. EXP-09 inclut ω L3, sans prétendre collecter des mesures cette passe.

## EXPERIMENTS EXECUTED

**3/3 extensions formelles exécutées.** Protocoles figés avant calcul, empreintes SHA-256 contrôlées, aucune modification des critères après résultats. Calculs rationnels exacts avec la bibliothèque standard Python. Aucun modèle statistique nouveau, aucun nouveau jeu empirique.

Commande de reproduction spécifique:

```bash
.venv-research/bin/python analysis/run_fourth_pass.py --check
```

Le registre comporte désormais9 expériences proposées, dont les huit précédentes conservées. L’exécution du nouveau EXP-09 ne vaut pas exécution du test indépendant EXP-01.

## EXP-02

**Question:** RQ-05.03 — quelles opérations restent définies avec une Utility seulement ordinale?

**Prédiction examinée:** coexistence dans le corpus d’un classement proposé et de relations employant différences, niveaux et rapports. L’invariance est la question de recherche, pas une affirmation attribuée à Campergue selon laquelle toutes ces opérations seraient ordinales.

**Résultat:** ordre, égalité et signes de variation sont invariants sous recodage strictement croissant commun. Les différences numériques exigent une structure d’intervalle; les rapports de niveaux une échelle de rapport. La formule de différences PDF349 peut être covariante sous une transformation affine si rP change inversement avec l’unité: elle n’exige donc pas une origine absolue. Le rendement réversible PDF386 ne possède pas cette invariance aux translations.

**Statuts:** FORMALLY_SUPPORTED / FORMALLY_QUALIFIED; BLOCKED_BY_MEASUREMENT pour valeurs économiques indépendamment calibrées.

**Pouvoir discriminant:** distingue des reconstructions mathématiques, pas des explications empiriques concurrentes. **Limite:** comparabilité entre agents, contextes et usages non acquise. [Table formule par formule](experiments/EXP-02/results.md).

## EXP-03

**Question:** RQ-08.02 — quelles conditions rendent K stable?

**Prédiction examinée:** PDF559 propose qu’une agrégation de davantage de Products stabilise K. Le test reconstruit une moyenne pondérée sous additivité, unités communes et frontière consolidée; il ne suppose pas que cette règle soit entièrement établie par le texte.

**Résultat:** 9 compositions à deux produits et27 à trois produits. Avec coefficients différents, K varie respectivement sur [7/5,13/7] et [5/3,7/3]. Réplication proportionnelle et coefficients identiques conservent K. Une recomposition peut aussi le conserver: poids [1/4,1/2,1/4] puis [1/3,1/3,1/3] donnent K=2 avec les coefficients déclarés.

**Statuts:** FORMALLY_SUPPORTED pour les conditions; FORMALLY_QUALIFIED pour une généralisation sans restrictions de composition/coefficient.

**Pouvoir discriminant:** contredit la nécessité d’une composition fixe et précise les limites d’une stabilité inconditionnelle; pas test empirique du couplage final. **Limite:** Ti positifs dans le test, additivité hypothétique, aucun Money observé. [Démonstration et normalisation](experiments/EXP-03/results.md).

## EXP-09

**Questions:** RQ-03.02 et RQ-03.03 — compatibilités locales des notations T/dT.

**Prédiction examinée:** primitive PDF207, différence temporelle PDF471, réserve et conservation PDF472.

**Résultat:** MODEL-A état E, MODEL-B réserve R et MODEL-C transfert T[a,b] sont localement compatibles sous des conditions différentes. Sur le cycle synthétique, transfert net=0 mais cumul positif=8. À cp variable, la primitive exige le terme ½ω²dcp. Une unité commune ne rend pas identiques stock, réserve et transfert.

**Statuts:** FORMALLY_SUPPORTED localement / FORMALLY_QUALIFIED / NOT_IDENTIFIABLE pour la mesure indépendante.

**Pouvoir discriminant:** distingue des lectures locales; ne teste pas indépendamment la relation quadratique. **Limite:** aucune lecture unique imposée au corpus, aucune dissipation empirique modélisée. [Modèles comparés](experiments/EXP-09/results.md).

## FORMAL RESULTS

La précision nouvelle ne consiste pas à répéter que « les variables manquent »: elle délimite les opérations permises, les groupes de changements d’échelle et les conventions nécessaires. Les preuves analytiques accompagnent les exemples finis. Les sorties JSON portent des statuts locaux et interdisent d’étiqueter Money ou T comme observés.

## EMPIRICAL RESULTS

**Aucun nouveau résultat empirique.** Le cas électrique antérieur ne fournit toujours pas coût complet, marge et qualité appariés; il n’a pas été présenté comme un nouveau test coût/prix. **NO_NEW_ENERGY_TEST:** la restriction temporelle de K reste disponible en EXP-08, mais sa faible spécificité ne justifiait pas une nouvelle analyse cette passe.

`verify.sh` relance les contrôles numériques antérieurs; cela ne multiplie pas le nombre d’expériences nouvelles.

## NON_IDENTIFIABLE RESULTS

- REQUIRES_CARDINAL_UTILITY pour les résultats numériques concernés, avec distinction intervalle/rapport.
- REQUIRES_INDEPENDENT_T pour tester la relation quadratique et calibrer cp.
- K économique non observé; moyenne de nombres synthétiques ne calibre pas M/T.
- Money reste non mesuré; les implications de budget ou de prix ne sont pas sa mesure.

## UTILITY

Restent possibles avec un ordre contextualisé: comparer, reconnaître égalité, classer le sens d’un changement. Ne restent pas déterminées par cet ordre: amplitudes, rapports, rendements numériques et produits à coefficient fixe. Une différence pondérée peut tolérer une translation d’origine si son coefficient covarie; un ratio de niveaux ne la tolère généralement pas. Cette distinction évite de réclamer une même échelle pour toutes les relations.

## T / dT

MODEL-A: état quadratique à référence choisie. MODEL-B: réserve compensant cet état dans un bilan isolé. MODEL-C: transfert signé entre deux extrémités. Les trois descriptions ne sont ni interchangeables ni nécessairement incompatibles lorsqu’on explicite leurs objets. Identifier simultanément la réserve et l’état à la même expression variable viole le bilan retenu. Aucun modèle n’est sélectionné arbitrairement comme lecture exclusive.

## K

À Ki fixes et poids normalisés, condition nécessaire et suffisante entre deux compositions: `Σ Δwi Ki=0`. Pour invariance à toute composition positive, les Ki actifs doivent être identiques. Même composition n’est pas nécessaire à une stabilité ponctuelle et ne suffit plus si Ki changent.

La normalisation indépendante par produit peut produire un K numérique arbitraire si on additionne des unités incompatibles. Dans l’exemple, agrégation brute8/13, retour à l’unité commune2. Changement commun d’unité par7: K devient2/7; le produit physique ou économique représenté est covariant, le nombre K n’est pas invariant.

## MONEY

[Implications observables sans mesure directe](operationalization/money_observable_implications.md): branches coût/prix/marge, prix sous profit fixé, économie sur panier constant, classifications qualitatives. Les hypothèses requises et les cas où une conséquence sur dM exige encore sa mesure sont explicités. Ces résultats peuvent être compatibles avec plusieurs explications usuelles.

## QUESTION STATUS CHANGES

Pas de changement artificiel: RQ-03.02, RQ-03.03, RQ-05.03 restent AMBIGUOUS; RQ-08.02 reste PARTIALLY_RESOLVED. Quatre nouveaux éléments de preuve formelle ajoutés uniquement à ces quatre dossiers. Les fichiers evidence.md, tests.md, conclusion.md et la matrice sont actualisés; dépendances inchangées.

## CLAIM STATUS CHANGES

18 claims reliés aux expériences examinés: 15 UNCHANGED; CPC-0052 et CPC-0121 QUALIFIED dans le périmètre des lectures locales; CPC-0117 REQUIRES_NEW_CONDITION pour la stabilité agrégée. Il s’agit d’un registre d’impact analytique, **pas d’une modification silencieuse des énoncés ou statuts source**. Les127 claims restent conservés, aucun nouveau claim créé. [Historique d’impact](experiments/fourth_pass_claim_impacts.json).

## NEW EVIDENCE

Quatre éléments FORMAL / QUALIFIES, trois jeux de résultats, une table machine-readable d’exigences d’échelle, protocoles et manifeste d’exécution. Les anciens dossiers modifiés sont archivés sous `history/fourth_pass_before`. Couverture analytique conservatrice inchangée272/562; aucune couverture supplémentaire revendiquée.

## LITERATURE

Une nouvelle entrée officielle ciblée: [JCGM VIM3, quantité ordinale](https://jcgm.bipm.org/vim/en/1.26.html), vérifiée, qui distingue ordre et opérations algébriques. Une source déjà enregistrée reconsultée: [OpenStax, champs conservatifs](https://openstax.org/books/calculus-volume-3/pages/6-3-conservative-vector-fields). Les ressources métrologiques antérieures sont réutilisées; pas de bibliographie ajoutée pour donner artificiellement du poids à une démonstration élémentaire. Les nouvelles déductions ne sont pas attribuées à ces références. [Registre ciblé](experiments/fourth_pass_literature.json).

## VERIFY

**PASS — 88/88 tests**, dont8 nouveaux. Le lancement direct puis `./verify.sh` ont tous deux terminé avec code de sortie0. Les empreintes des protocoles et les résultats exacts des trois extensions sont contrôlés. Aucun critère n’a été modifié après calcul.

WARNING: couverture partielle, absence de mesure indépendante de T/Utility/Money, hypothèses et bibliographie encore partielles. Ces limites scientifiques ne deviennent pas des échecs d’infrastructure et aucun résultat formel n’est présenté comme observation empirique.

## MAIN RESULTS

1. Les exigences de mesure de Utility diffèrent selon les opérations.
2. Les classifications ordinales survivent sans déterminer les rendements numériques.
3. Une formule de différences peut être compatible avec une origine arbitraire et un coefficient covariant.
4. Composition fixe suffit à stabiliser K sous coefficients fixes, mais n’est pas nécessaire.
5. Invariance à toute composition positive exige Ki identiques dans le modèle pondéré étudié.
6. Invariance économique et invariance du nombre après changement d’unité sont distinctes.
7. État, réserve, transfert et cumul positif ne sont pas une même quantité T.
8. Les diagnostics formels ne lèvent pas l’absence de mesure indépendante de T ou Money.

## NEXT

1. EXP-01: chercher une indication indépendante de Force/T avant calibration de cp.
2. RQ-05.03: déterminer quel groupe de changements d’échelle le corpus autorise pour chaque coefficient.
3. RQ-08.02: spécifier poids et frontières d’un K observable avant son test temporel.
4. EXP-08: ne promouvoir le hors-échantillon que pour une restriction explicite et des alternatives précises.
5. RQ-03.02: confronter la notation état/transfert/réserve aux autres passages, sans généraliser la compatibilité locale.
6. EXP-06: chercher un panel produit-usine-client réellement apparié.
7. RQ-04.04: expliciter le domaine contraint de l’optimum avant un nouvel approfondissement.

Le résultat porte sur des constructions et mécanismes locaux, selon le [cadrage épistémique](epistemic_policy.md); aucun verdict global n’est formulé.
