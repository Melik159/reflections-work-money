# Arbre de recherche — version initiale

53 questions hors racine : 12 de niveau1 et41 de niveau2. Les familles sont des problèmes de synthèse ; elles ne reprennent pas les dix chapitres. Leur nombre résulte de41 questions opérationnelles et12 problèmes auxquels leurs réponses contribuent.

L’arbre a été écrit AVANT les dossiers. Son état initial OPEN est conservé dans history/001_initial_questions.md ; les statuts ci-dessous sont ceux de la première passe, synchronisés avec le graphe et les dossiers.

RQ-ROOT : citation du manuscrit, pages PDF2–3 ; phrase associée page3. Les autres questions sont RESEARCH_INTERPRETATION, jamais des citations inventées.

Les anciens RQ-01-01…RQ-10-01 restent dans analysis/data/research_questions.json. Les nouveaux RQ-01.01 utilisent un point et un espace de noms distinct ; aucune suppression ni réaffectation implicite.

## RQ-ROOT — The key question is therefore to understand how the increase in living standards has led to these environmental damages, or how we have moved from a subsistence society to an affluent society.

Parent : aucun ; importance : FOUNDATIONAL ; statut : OPEN.
[Dossier](RQ-ROOT/README.md)
Claims : CPC-0001, CPC-0003, CPC-0031, CPC-0120.
Chapitres : CH-01, CH-09.
Dépendances : RQ-12.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

## RQ-01 — Quel phénomène historique et environnemental faut-il expliquer ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-01/README.md)
Claims : CPC-0001, CPC-0003, CPC-0018, CPC-0029, CPC-0030, CPC-0031, CPC-0037, CPC-0042, CPC-0048, CPC-0065, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-05, CH-07, CH-09, CH-10.
Dépendances : RQ-01.01, RQ-01.02, RQ-01.03, RQ-01.04.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-01.01 — Le domaine annoncé couvre-t-il réellement les dommages environnementaux de la question racine ?

Parent : RQ-01 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-01.01/README.md)
Claims : CPC-0001, CPC-0003, CPC-0030, CPC-0031, CPC-0042, CPC-0065.
Chapitres : CH-01, CH-05, CH-10.
Dépendances : aucune prerequisite dans cette décomposition.
Testabilité : CONSISTENCY_TEST. Classification : BLOCKING, HIGH_VALUE.

### RQ-01.02 — Quels indicateurs distinguent niveau de vie, revenu réel et bien-être dans la comparaison historique ?

Parent : RQ-01 ; importance : FOUNDATIONAL ; statut : OPEN.
[Dossier](RQ-01.02/README.md)
Claims : CPC-0001, CPC-0048, CPC-0065, CPC-0127.
Chapitres : CH-01, CH-09, CH-10.
Dépendances : RQ-01.01.
Testabilité : EMPIRICAL_TEST. Classification : BLOCKING, EMPIRICAL.

### RQ-01.03 — La subsistance et l’abondance sont-elles des états mesurables, et la stabilité historique alléguée est-elle défendable ?

Parent : RQ-01 ; importance : MAJOR ; statut : OPEN.
[Dossier](RQ-01.03/README.md)
Claims : CPC-0018, CPC-0029, CPC-0037.
Chapitres : CH-01, CH-07, CH-09.
Dépendances : RQ-01.02.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, OPEN.

### RQ-01.04 — Quels dommages, territoires et horizons sont explicitement inclus ou laissés hors champ ?

Parent : RQ-01 ; importance : MAJOR ; statut : OPEN.
[Dossier](RQ-01.04/README.md)
Claims : CPC-0031, CPC-0120.
Chapitres : CH-01, CH-09.
Dépendances : RQ-01.01.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, OPEN.

## RQ-02 — Quel changement constitue une richesse nouvelle dans le périmètre retenu ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-02/README.md)
Claims : CPC-0006, CPC-0007, CPC-0009, CPC-0014, CPC-0022, CPC-0024, CPC-0030, CPC-0036, CPC-0048, CPC-0049, CPC-0065, CPC-0100.
Chapitres : CH-01, CH-02, CH-03, CH-04, CH-05, CH-06, CH-10.
Dépendances : RQ-02.01, RQ-02.02, RQ-02.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-02.01 — La richesse définie comme Money exclut-elle patrimoine, services non marchands et richesse matérielle ?

Parent : RQ-02 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-02.01/README.md)
Claims : CPC-0048, CPC-0065, CPC-0006, CPC-0049.
Chapitres : CH-01, CH-03, CH-10.
Dépendances : RQ-01.01.
Testabilité : CONSISTENCY_TEST. Classification : BLOCKING, HIGH_VALUE, EASY_WIN.

### RQ-02.02 — Quel critère distingue création nette, transfert, redistribution et simple réévaluation ?

Parent : RQ-02 ; importance : FOUNDATIONAL ; statut : OPEN.
[Dossier](RQ-02.02/README.md)
Claims : CPC-0007, CPC-0009, CPC-0014, CPC-0022, CPC-0024, CPC-0100.
Chapitres : CH-01, CH-02, CH-04, CH-05, CH-06.
Dépendances : RQ-02.01.
Testabilité : CONSISTENCY_TEST. Classification : BLOCKING, HIGH_VALUE.

### RQ-02.03 — Le principe selon lequel seul Work crée un changement économique est-il une définition ou une restriction réfutable ?

Parent : RQ-02 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-02.03/README.md)
Claims : CPC-0009, CPC-0022, CPC-0030, CPC-0036.
Chapitres : CH-01, CH-04, CH-05.
Dépendances : RQ-02.02, RQ-03.01.
Testabilité : FORMAL_TEST. Classification : HIGH_VALUE, FORMAL, OPEN.

## RQ-03 — Economic Work fournit-il une grandeur économique définie et mesurable ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-03/README.md)
Claims : CPC-0023, CPC-0039, CPC-0040, CPC-0041, CPC-0043, CPC-0044, CPC-0045, CPC-0051, CPC-0052, CPC-0054, CPC-0062, CPC-0063, CPC-0064, CPC-0066, CPC-0068, CPC-0094, CPC-0095, CPC-0121, CPC-0122, CPC-0123.
Chapitres : CH-03, CH-04, CH-05, CH-09, CH-10.
Dépendances : RQ-03.01, RQ-03.02, RQ-03.03, RQ-03.04.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-03.01 — Quelle distinction textuelle sépare Economic Work, labour, effort physique et travail socialement utile ?

Parent : RQ-03 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-03.01/README.md)
Claims : CPC-0040, CPC-0041, CPC-0051, CPC-0052, CPC-0064, CPC-0094, CPC-0095, CPC-0123.
Chapitres : CH-03, CH-04, CH-05, CH-10.
Dépendances : RQ-02.01.
Testabilité : CONSISTENCY_TEST. Classification : BLOCKING, HIGH_VALUE, EASY_WIN.

### RQ-03.02 — Quelles conventions réconcilient T, dT, Work restant, travail accumulé et signes ?

Parent : RQ-03 ; importance : FOUNDATIONAL ; statut : AMBIGUOUS.
[Dossier](RQ-03.02/README.md)
Claims : CPC-0023, CPC-0040, CPC-0045, CPC-0062, CPC-0063, CPC-0121.
Chapitres : CH-03, CH-05, CH-09.
Dépendances : RQ-03.01.
Testabilité : FORMAL_TEST. Classification : BLOCKING, FORMAL, OPEN.

### RQ-03.03 — Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?

Parent : RQ-03 ; importance : FOUNDATIONAL ; statut : AMBIGUOUS.
[Dossier](RQ-03.03/README.md)
Claims : CPC-0039, CPC-0043, CPC-0044, CPC-0052, CPC-0054, CPC-0066, CPC-0068.
Chapitres : CH-03, CH-04, CH-05.
Dépendances : RQ-03.01, RQ-03.02.
Testabilité : EMPIRICAL_TEST, FORMAL_TEST. Classification : BLOCKING, HIGH_VALUE, EMPIRICAL, FORMAL.

### RQ-03.04 — La conservation ou destruction de Work est-elle une identité de bilan ou une hypothèse économique ?

Parent : RQ-03 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-03.04/README.md)
Claims : CPC-0023, CPC-0039, CPC-0043, CPC-0121, CPC-0122.
Chapitres : CH-05, CH-09.
Dépendances : RQ-03.02, RQ-03.03.
Testabilité : FORMAL_TEST. Classification : FORMAL, HIGH_VALUE.

## RQ-04 — Sous quelles conditions une transformation améliore-t-elle la productivité ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-04/README.md)
Claims : CPC-0017, CPC-0019, CPC-0032, CPC-0033, CPC-0035, CPC-0038, CPC-0052, CPC-0054, CPC-0066, CPC-0094, CPC-0096, CPC-0101, CPC-0102, CPC-0103, CPC-0104, CPC-0105, CPC-0106, CPC-0108, CPC-0110, CPC-0111, CPC-0112.
Chapitres : CH-03, CH-04, CH-05, CH-06, CH-07, CH-08, CH-09, CH-10.
Dépendances : RQ-04.01, RQ-04.02, RQ-04.03, RQ-04.04.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-04.01 — Quand accélérer une tâche constante réduit-il effectivement les intrants nécessaires par produit ?

Parent : RQ-04 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-04.01/README.md)
Claims : CPC-0017, CPC-0019, CPC-0052, CPC-0094, CPC-0110, CPC-0112.
Chapitres : CH-03, CH-04.
Dépendances : RQ-03.01.
Testabilité : EMPIRICAL_TEST. Classification : HIGH_VALUE, EMPIRICAL.

### RQ-04.02 — Le résultat +78% découle-t-il d’une hypothèse quadratique particulière plutôt que d’une loi générale mesurée ?

Parent : RQ-04 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-04.02/README.md)
Claims : CPC-0035, CPC-0096.
Chapitres : CH-04.
Dépendances : RQ-03.03, RQ-04.01.
Testabilité : FORMAL_TEST. Classification : HIGH_VALUE, FORMAL, EASY_WIN.

### RQ-04.03 — Comment machines, complexité et substitution au salarié modifient-elles les gains et leurs coûts ?

Parent : RQ-04 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-04.03/README.md)
Claims : CPC-0054, CPC-0066, CPC-0105, CPC-0106, CPC-0111.
Chapitres : CH-03, CH-04, CH-08, CH-09.
Dépendances : RQ-04.01.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

### RQ-04.04 — Quelles contraintes et conventions de signe rendent les rendements et optima des cycles définis ?

Parent : RQ-04 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-04.04/README.md)
Claims : CPC-0032, CPC-0033, CPC-0038, CPC-0101, CPC-0102, CPC-0103, CPC-0104, CPC-0108.
Chapitres : CH-05, CH-06, CH-07, CH-09, CH-10.
Dépendances : RQ-03.02, RQ-03.04.
Testabilité : FORMAL_TEST. Classification : FORMAL, HIGH_VALUE, OPEN.

## RQ-05 — Comment un gain productif se répartit-il entre coût, prix, qualité et profit ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-05/README.md)
Claims : CPC-0019, CPC-0020, CPC-0021, CPC-0034, CPC-0055, CPC-0056, CPC-0057, CPC-0058, CPC-0059, CPC-0060, CPC-0076, CPC-0077, CPC-0078, CPC-0079, CPC-0097, CPC-0098, CPC-0105, CPC-0110, CPC-0113, CPC-0124, CPC-0125.
Chapitres : CH-02, CH-03, CH-04, CH-05, CH-06, CH-09, CH-10.
Dépendances : RQ-05.01, RQ-05.02, RQ-05.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-05.01 — Quelles conditions distinguent baisse de prix, prix maintenu et gain retenu après baisse du coût ?

Parent : RQ-05 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-05.01/README.md)
Claims : CPC-0019, CPC-0020, CPC-0021, CPC-0097, CPC-0098, CPC-0105, CPC-0110.
Chapitres : CH-04, CH-09.
Dépendances : RQ-04.01.
Testabilité : EMPIRICAL_TEST. Classification : BLOCKING, HIGH_VALUE, EMPIRICAL.

### RQ-05.02 — Comment concurrence, négociation, monopole et brevet répartissent-ils productivité et rente ?

Parent : RQ-05 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-05.02/README.md)
Claims : CPC-0021, CPC-0060, CPC-0113, CPC-0124, CPC-0125.
Chapitres : CH-03, CH-04, CH-06, CH-10.
Dépendances : RQ-05.01, RQ-02.02.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

### RQ-05.03 — Utility peut-elle être mesurée indépendamment du prix et de la quantité pour comparer les scénarios ?

Parent : RQ-05 ; importance : FOUNDATIONAL ; statut : AMBIGUOUS.
[Dossier](RQ-05.03/README.md)
Claims : CPC-0034, CPC-0055, CPC-0056, CPC-0057, CPC-0058, CPC-0059, CPC-0076, CPC-0077, CPC-0078, CPC-0079, CPC-0113.
Chapitres : CH-02, CH-03, CH-04, CH-05, CH-06.
Dépendances : RQ-02.01.
Testabilité : EMPIRICAL_TEST. Classification : BLOCKING, HIGH_VALUE, EMPIRICAL.

## RQ-06 — Quand les variations de Cash et de sa valeur constituent-elles une variation de Money ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-06/README.md)
Claims : CPC-0002, CPC-0005, CPC-0010, CPC-0011, CPC-0012, CPC-0013, CPC-0014, CPC-0015, CPC-0016, CPC-0025, CPC-0026, CPC-0027, CPC-0028, CPC-0041, CPC-0046, CPC-0050, CPC-0053, CPC-0069, CPC-0070, CPC-0071, CPC-0072, CPC-0073, CPC-0074, CPC-0075, CPC-0080, CPC-0081, CPC-0082, CPC-0083, CPC-0085, CPC-0086, CPC-0088, CPC-0090, CPC-0099, CPC-0107.
Chapitres : CH-01, CH-02, CH-03, CH-04, CH-07.
Dépendances : RQ-06.01, RQ-06.02, RQ-06.03, RQ-06.04.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-06.01 — Quelles unités et frontières distinguent Cash, Money, n, u et pouvoir d’achat ?

Parent : RQ-06 ; importance : FOUNDATIONAL ; statut : OPEN.
[Dossier](RQ-06.01/README.md)
Claims : CPC-0002, CPC-0010, CPC-0011, CPC-0041, CPC-0046, CPC-0050, CPC-0053.
Chapitres : CH-02, CH-03.
Dépendances : RQ-02.01.
Testabilité : CONSISTENCY_TEST. Classification : BLOCKING, HIGH_VALUE, EASY_WIN.

### RQ-06.02 — Dans quels scénarios M=n·u s’accompagne-t-il d’une compensation immédiate, différée ou absente ?

Parent : RQ-06 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-06.02/README.md)
Claims : CPC-0005, CPC-0012, CPC-0025, CPC-0026, CPC-0069, CPC-0070, CPC-0071, CPC-0072, CPC-0073, CPC-0074, CPC-0075, CPC-0080, CPC-0081, CPC-0082, CPC-0083, CPC-0086, CPC-0088, CPC-0090.
Chapitres : CH-02.
Dépendances : RQ-06.01.
Testabilité : FORMAL_TEST. Classification : BLOCKING, HIGH_VALUE, FORMAL.

### RQ-06.03 — Comment création, destruction et émission accompagnatrice se distinguent-elles sans double compter le gain ?

Parent : RQ-06 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-06.03/README.md)
Claims : CPC-0015, CPC-0016, CPC-0071, CPC-0072, CPC-0073, CPC-0099, CPC-0107.
Chapitres : CH-02, CH-04, CH-07.
Dépendances : RQ-06.01, RQ-05.01, RQ-05.03.
Testabilité : FORMAL_TEST. Classification : HIGH_VALUE, FORMAL.

### RQ-06.04 — Après traduction du vocabulaire, quelle restriction sur le crédit bancaire reste réellement contestable ?

Parent : RQ-06 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-06.04/README.md)
Claims : CPC-0013, CPC-0014, CPC-0027, CPC-0028, CPC-0050, CPC-0085.
Chapitres : CH-01, CH-02, CH-03.
Dépendances : RQ-06.02, RQ-02.02.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

## RQ-07 — Comment les interactions entre agents créent-elles ou redistribuent-elles les gains ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-07/README.md)
Claims : CPC-0007, CPC-0024, CPC-0038, CPC-0060, CPC-0061, CPC-0062, CPC-0063, CPC-0084, CPC-0087, CPC-0091, CPC-0092, CPC-0093, CPC-0100, CPC-0101, CPC-0102, CPC-0103, CPC-0104, CPC-0108, CPC-0123, CPC-0124, CPC-0125.
Chapitres : CH-01, CH-02, CH-03, CH-05, CH-06, CH-07, CH-09, CH-10.
Dépendances : RQ-07.01, RQ-07.02, RQ-07.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-07.01 — Quels bilans distinguent les rôles du producteur, salarié, consommateur, État et intermédiaire ?

Parent : RQ-07 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-07.01/README.md)
Claims : CPC-0007, CPC-0060, CPC-0061, CPC-0062, CPC-0063, CPC-0108, CPC-0123.
Chapitres : CH-01, CH-03, CH-09, CH-10.
Dépendances : RQ-02.02, RQ-03.02.
Testabilité : FORMAL_TEST. Classification : FORMAL, HIGH_VALUE.

### RQ-07.02 — Une transaction ou décision non neutre entre acteurs implique-t-elle une création globale ?

Parent : RQ-07 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-07.02/README.md)
Claims : CPC-0024, CPC-0084, CPC-0087, CPC-0093, CPC-0100, CPC-0124, CPC-0125.
Chapitres : CH-02, CH-05, CH-06, CH-10.
Dépendances : RQ-07.01, RQ-06.03.
Testabilité : FORMAL_TEST. Classification : BLOCKING, HIGH_VALUE, FORMAL.

### RQ-07.03 — Quels bouclages de crédit, intérêt et profit exigent Work supplémentaire, transfert ou dévaluation ?

Parent : RQ-07 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-07.03/README.md)
Claims : CPC-0038, CPC-0091, CPC-0092, CPC-0101, CPC-0102, CPC-0103, CPC-0104.
Chapitres : CH-02, CH-06, CH-07, CH-09, CH-10.
Dépendances : RQ-07.01, RQ-06.02, RQ-04.04.
Testabilité : FORMAL_TEST. Classification : FORMAL, HIGH_VALUE.

## RQ-08 — À quelles conditions les relations locales deviennent-elles des relations agrégées ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-08/README.md)
Claims : CPC-0004, CPC-0037, CPC-0043, CPC-0044, CPC-0047, CPC-0089, CPC-0109, CPC-0111, CPC-0112, CPC-0114, CPC-0115, CPC-0116, CPC-0117, CPC-0118, CPC-0126.
Chapitres : CH-02, CH-03, CH-04, CH-05, CH-07, CH-08, CH-09.
Dépendances : RQ-08.01, RQ-08.02, RQ-08.03, RQ-08.04.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-08.01 — Quelles unités, frontières et pondérations autorisent l’addition des contributions sans double compte ?

Parent : RQ-08 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-08.01/README.md)
Claims : CPC-0037, CPC-0089, CPC-0111, CPC-0114, CPC-0126.
Chapitres : CH-02, CH-03, CH-07, CH-08.
Dépendances : RQ-03.03, RQ-06.01, RQ-07.01.
Testabilité : FORMAL_TEST. Classification : BLOCKING, FORMAL, HIGH_VALUE.

### RQ-08.02 — Un grand nombre de produits suffit-il à stabiliser K malgré des coefficients et compositions hétérogènes ?

Parent : RQ-08 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-08.02/README.md)
Claims : CPC-0043, CPC-0044, CPC-0109, CPC-0116, CPC-0117, CPC-0118.
Chapitres : CH-05, CH-07, CH-08, CH-09.
Dépendances : RQ-08.01, RQ-05.03.
Testabilité : FORMAL_TEST, EMPIRICAL_TEST. Classification : HIGH_VALUE, FORMAL, EMPIRICAL.

### RQ-08.03 — Les potentiels locaux sont-ils des fonctions d’état intégrables et sommables sous leurs contraintes ?

Parent : RQ-08 ; importance : MAJOR ; statut : AMBIGUOUS.
[Dossier](RQ-08.03/README.md)
Claims : CPC-0004, CPC-0047, CPC-0115, CPC-0116.
Chapitres : CH-05, CH-08.
Dépendances : RQ-03.02, RQ-03.04.
Testabilité : FORMAL_TEST. Classification : FORMAL, OPEN.

### RQ-08.04 — Le champ labour-prix et les normalisations locales/globales sont-ils invariants aux changements d’unités ?

Parent : RQ-08 ; importance : CORE ; statut : AMBIGUOUS.
[Dossier](RQ-08.04/README.md)
Claims : CPC-0089, CPC-0112, CPC-0116, CPC-0126.
Chapitres : CH-02, CH-04, CH-08.
Dépendances : RQ-08.01.
Testabilité : FORMAL_TEST. Classification : FORMAL, HIGH_VALUE.

## RQ-09 — Quel pont mesurable relie énergie physique et transformation économique ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-09/README.md)
Claims : CPC-0003, CPC-0017, CPC-0018, CPC-0029, CPC-0039, CPC-0042, CPC-0067, CPC-0105, CPC-0106, CPC-0108, CPC-0117, CPC-0118, CPC-0119, CPC-0122.
Chapitres : CH-01, CH-04, CH-05, CH-08, CH-09, CH-10.
Dépendances : RQ-09.01, RQ-09.02, RQ-09.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-09.01 — L’énergie bon marché est-elle une condition nécessaire, suffisante ou seulement favorable à la productivité ?

Parent : RQ-09 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-09.01/README.md)
Claims : CPC-0017, CPC-0018, CPC-0029, CPC-0105, CPC-0106.
Chapitres : CH-01, CH-04, CH-09.
Dépendances : RQ-04.01, RQ-01.03.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

### RQ-09.02 — Quel critère et quelle conversion séparent énergie consommée, travail physique utile et Work économique ?

Parent : RQ-09 ; importance : FOUNDATIONAL ; statut : AMBIGUOUS.
[Dossier](RQ-09.02/README.md)
Claims : CPC-0003, CPC-0017, CPC-0039, CPC-0042, CPC-0067, CPC-0119, CPC-0122.
Chapitres : CH-01, CH-04, CH-05, CH-09.
Dépendances : RQ-03.03, RQ-05.03.
Testabilité : FORMAL_TEST. Classification : BLOCKING, HIGH_VALUE, FORMAL.

### RQ-09.03 — GDP=K·W est-il testable indépendamment du PIB et avec des rendements, pertes et frontières explicites ?

Parent : RQ-09 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-09.03/README.md)
Claims : CPC-0067, CPC-0108, CPC-0117, CPC-0118, CPC-0119.
Chapitres : CH-08, CH-09, CH-10.
Dépendances : RQ-09.02, RQ-08.02.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

## RQ-10 — Comment les gains disponibles deviennent-ils une abondance effectivement consommée ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-10/README.md)
Claims : CPC-0008, CPC-0015, CPC-0016, CPC-0018, CPC-0053, CPC-0065, CPC-0076, CPC-0077, CPC-0078, CPC-0079, CPC-0084, CPC-0099, CPC-0118, CPC-0127.
Chapitres : CH-01, CH-02, CH-03, CH-04, CH-07, CH-09, CH-10.
Dépendances : RQ-10.01, RQ-10.02, RQ-10.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-10.01 — Sous quelles conditions un gain de prix améliore-t-il le pouvoir d’achat réel plutôt qu’un simple indicateur nominal ?

Parent : RQ-10 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-10.01/README.md)
Claims : CPC-0015, CPC-0016, CPC-0053, CPC-0076, CPC-0077, CPC-0078, CPC-0079.
Chapitres : CH-02, CH-03, CH-04.
Dépendances : RQ-05.01, RQ-05.03, RQ-06.01.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

### RQ-10.02 — Quelle fraction du gain est épargnée, dépensée plus tard, consommée davantage ou affectée à la qualité ?

Parent : RQ-10 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-10.02/README.md)
Claims : CPC-0008, CPC-0084, CPC-0099, CPC-0127.
Chapitres : CH-01, CH-02, CH-07, CH-09, CH-10.
Dépendances : RQ-10.01, RQ-07.02.
Testabilité : EMPIRICAL_TEST. Classification : BLOCKING, HIGH_VALUE, EMPIRICAL.

### RQ-10.03 — L’abondance peut-elle progresser sans augmentation des flux physiques d’énergie et de matière ?

Parent : RQ-10 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-10.03/README.md)
Claims : CPC-0018, CPC-0065, CPC-0118, CPC-0127.
Chapitres : CH-01, CH-09, CH-10.
Dépendances : RQ-10.02, RQ-09.03.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE, OPEN.

## RQ-11 — Par quelles voies cette consommation produit-elle des dommages environnementaux ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-11/README.md)
Claims : CPC-0001, CPC-0018, CPC-0031, CPC-0084, CPC-0099, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-02, CH-07, CH-09, CH-10.
Dépendances : RQ-11.01, RQ-11.02, RQ-11.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-11.01 — Quels maillons sourcés relient gains productifs, flux physiques et dommages, et lesquels restent manquants ?

Parent : RQ-11 ; importance : FOUNDATIONAL ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-11.01/README.md)
Claims : CPC-0001, CPC-0018, CPC-0031, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-09, CH-10.
Dépendances : RQ-10.02, RQ-09.02, RQ-01.04.
Testabilité : EMPIRICAL_TEST. Classification : BLOCKING, HIGH_VALUE, EMPIRICAL.

### RQ-11.02 — L’usage du gain produit-il un rebond direct, indirect ou global, et dans quelles limites ?

Parent : RQ-11 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-11.02/README.md)
Claims : CPC-0084, CPC-0099, CPC-0120, CPC-0127.
Chapitres : CH-02, CH-07, CH-09, CH-10.
Dépendances : RQ-10.02, RQ-09.01.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, HIGH_VALUE.

### RQ-11.03 — Quelle empreinte marginale attribuer aux matières, transports, énergie et externalités du panier supplémentaire ?

Parent : RQ-11 ; importance : MAJOR ; statut : OPEN.
[Dossier](RQ-11.03/README.md)
Claims : CPC-0018, CPC-0031, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-09, CH-10.
Dépendances : RQ-11.01, RQ-11.02.
Testabilité : EMPIRICAL_TEST. Classification : EMPIRICAL, OPEN.

## RQ-12 — Quels maillons permettraient une explication causale spécifique de la transition ?

Parent : RQ-ROOT ; importance : CORE ; statut : OPEN.
[Dossier](RQ-12/README.md)
Claims : CPC-0001, CPC-0003, CPC-0009, CPC-0018, CPC-0029, CPC-0031, CPC-0048, CPC-0068, CPC-0117, CPC-0118, CPC-0119, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-04, CH-08, CH-09, CH-10.
Dépendances : RQ-12.01, RQ-12.02, RQ-12.03.
Testabilité : COMPARATIVE_TEST. Classification : HIGH_VALUE.

### RQ-12.01 — Quelles observations départageraient Campergue des explications concurrentes à conditions comparables ?

Parent : RQ-12 ; importance : CORE ; statut : PARTIALLY_RESOLVED.
[Dossier](RQ-12.01/README.md)
Claims : CPC-0003, CPC-0068, CPC-0117, CPC-0118, CPC-0119.
Chapitres : CH-01, CH-04, CH-08, CH-09.
Dépendances : RQ-03.03, RQ-05.01, RQ-08.02, RQ-09.02.
Testabilité : EMPIRICAL_TEST, FORMAL_TEST. Classification : HIGH_VALUE, EMPIRICAL, FORMAL.

### RQ-12.02 — Quels mécanismes établis ou postulés sont nécessaires, suffisants ou substituables dans la transition historique ?

Parent : RQ-12 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-12.02/README.md)
Claims : CPC-0001, CPC-0009, CPC-0018, CPC-0029, CPC-0118, CPC-0120.
Chapitres : CH-01, CH-04, CH-09.
Dépendances : RQ-01.03, RQ-09.01, RQ-10.03, RQ-11.01.
Testabilité : CONSISTENCY_TEST. Classification : HIGH_VALUE, OPEN.

### RQ-12.03 — Quelle réponse limitée à la question racine résiste aux lacunes, contre-exemples et changements de périmètre ?

Parent : RQ-12 ; importance : CORE ; statut : OPEN.
[Dossier](RQ-12.03/README.md)
Claims : CPC-0001, CPC-0003, CPC-0031, CPC-0048, CPC-0120, CPC-0127.
Chapitres : CH-01, CH-09, CH-10.
Dépendances : RQ-12.01, RQ-12.02, RQ-11.03.
Testabilité : CONSISTENCY_TEST. Classification : HIGH_VALUE, OPEN.


## Passe métrologique — 2026-09-08

| Question | Statut courant | Conclusion |
|---|---|---|
| RQ-03.03 | AMBIGUOUS | T est dérivé des lois proposées, non mesuré indépendamment par cette dérivation. L’intégrale de FP dl n’offre une voie distincte que si FP est étalonné sans utiliser cp·dω/dt. |
| RQ-05.03 | AMBIGUOUS | Le manuscrit reconnaît explicitement p109 que Utility ne dispose pas de mesure, mais propose un classement. Cela ne suffit pas à déterminer UP2/UP1 dans les rendements. |
| RQ-08.02 | PARTIALLY_RESOLVED | K local peut être calibré si M et T sont indépendamment mesurés. K=PIB/énergie est estimable comme ratio de proxies, mais résiduel si recalculé pour chaque observation. |
| RQ-09.02 | AMBIGUOUS | Le pont Tused=−Wcreated est explicite et conditionné à une évolution de Utility. Ce n’est ni toute énergie consommée ni toute fatigue. |
| RQ-10.02 | PARTIALLY_RESOLVED | Consommation ailleurs, quantité/qualité et dépenses différées sont des branches, non fractions déterminées. Le bilan comptable permet de classer des flux observés, pas leur destination marginale causale. |
| RQ-11.01 | PARTIALLY_RESOLVED | Le corpus vise un ensemble de pressions et dégradations; pas un indicateur unique de dommage quantifié. Ressources, déchets, énergie et transports sont explicitement reliés aux transformations. |
| RQ-12.02 | OPEN | La recherche de signatures est ici un sous-périmètre métrologique, pas un remplacement de la question historique nécessaire/suffisant. T quadratique, optimum et conversion sont caractéristiques mais leurs variables indépendantes manquent. |
| RQ-04.04 | PARTIALLY_RESOLVED | 0.3431 et 0.5858 sont calculables lorsque les angles sont fixés à π/8. La formule de rendement seule ne sélectionne pas cette valeur comme maximum. |
| RQ-01.03 | PARTIALLY_RESOLVED | Subsistance/abondance décrivent des conditions de consommation et possibilités d’accès, sans seuil opérationnel unique retrouvé. Dépenses, quantités, temps et diversité devraient être suivis conjointement. |
| RQ-05.01 | PARTIALLY_RESOLVED | Mesurer simultanément coût complet unitaire, prix net réalisé, quantité, qualité et résultat producteur permet de distinguer branches coût/prix. Une baisse de coût seule ne détermine pas le partage. |

Aucun ID ou lien de dépendance changé. Les entrées ci-dessus actualisent les statuts historiques précédents.
