# Sélection de quatrième passe

Cadrage: claims, relations, constructions et modèles locaux. Aucun verdict global. Les cas synthétiques L1/L2 ne sont pas présentés comme données empiriques. Leur sélection exceptionnelle répond aux tests formels explicitement demandés.

| EXP | Questions | Claims | Variables / niveaux | Données disponibles | Pouvoir | Coût | État / décision |
|---|---|---|---|---|---|---|---|
| EXP-01 | RQ-03.03 | CPC-0039, CPC-0043, CPC-0044, CPC-0052, CPC-0054, CPC-0066, CPC-0068 | T L1, cp L1, ω L3, Force / Forces L1 | Élevé; instrument économique absent | NOT_TESTABLE | Élevé; instrument économique absent | NEEDS_DEFINITION; non retenue |
| EXP-02 | RQ-05.03 | CPC-0034, CPC-0055, CPC-0056, CPC-0057, CPC-0058, CPC-0059, CPC-0076, CPC-0077, CPC-0078, CPC-0079, CPC-0113 | Utility L2, price L3 | Synthetic only | MEDIUM | Faible; diagnostic formel | DO_NOW; extension retenue |
| EXP-03 | RQ-08.02 | CPC-0043, CPC-0044, CPC-0109, CPC-0116, CPC-0117, CPC-0118 | K L1, T L1, Money L1 | Synthetic only | MEDIUM | Faible; formal_results.json | DO_NOW; extension retenue |
| EXP-04 | RQ-04.04 | CPC-0032, CPC-0033, CPC-0038, CPC-0101, CPC-0102, CPC-0103, CPC-0104, CPC-0108 | η L1, Utility L2 | Synthetic only | MEDIUM | Faible; formal_results.json | DO_NOW; non retenue |
| EXP-05 | RQ-09.02 | CPC-0003, CPC-0017, CPC-0039, CPC-0042, CPC-0067, CPC-0119, CPC-0122 | energy L5, useful work L3, ω L3 | Modéré; laboratoire ou usine; domaine à pré-spécifier | MEDIUM | Modéré; laboratoire ou usine; domaine à pré-spécifier | NEEDS_DATA; non retenue |
| EXP-06 | RQ-05.01 | CPC-0019, CPC-0020, CPC-0021, CPC-0097, CPC-0098, CPC-0105, CPC-0110 | cost L2, price L3, profit L3, productivity L3, Utility L2, consumer gain L2 | Élevé; données commerciales appariées | LOW | Élevé; données commerciales appariées | NEEDS_DATA; non retenue |
| EXP-07 | RQ-10.02 | CPC-0008, CPC-0084, CPC-0099, CPC-0127 | consumer gain L2, price L3, standard of living L2, environmental damage L2 | Élevé; contrefactuel et données de panel | LOW | Élevé; contrefactuel et données de panel | NEEDS_DATA; non retenue |
| EXP-08 | RQ-12.02 | CPC-0001, CPC-0009, CPC-0018, CPC-0029, CPC-0118, CPC-0120 | K L1, energy L5 | Faible; données indépendantes déjà archivées; pas de régression cette passe | LOW | Faible; données indépendantes déjà archivées; pas de régression cette passe | DO_LATER; non retenue |
| EXP-09 | RQ-03.02, RQ-03.03 | CPC-0040,0052,0054,0066,0068,0121 | T,dT,cp L1; ω L3 | passages et calcul formel | local, pas empirique | faible | nouveau sous-problème DO_NOW |

Sélection: EXP-02, EXP-03, EXP-09. EXP-04 a déjà son diagnostic de dérivée; rien à répéter. EXP-05/06/07 manquent de données appariées. EXP-08 est possible mais de faible spécificité: NO_NEW_ENERGY_TEST. Aucun nouveau test coût/prix; les données précédentes ne permettent pas marge complète ni qualité/Utility appariée. Les sorties de verify.sh sur ces anciens jeux sont des contrôles de reproduction, pas des expériences nouvelles.
