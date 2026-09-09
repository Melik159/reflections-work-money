# Deuxième passe — dépendances avant analyse

Ordre retenu : RQ-03.02 → RQ-08.03 → RQ-08.01 → RQ-08.04 → RQ-06.04 → RQ-10.01 → RQ-09.03 → RQ-11.02 → RQ-11.03 → RQ-12.01.

T/dT précède les potentiels ; additivité précède le champ ; le bilan monétaire précède usage et dommage. Les contraintes directes des dix nœuds sont respectées. Les prérequis hors sélection restent visibles et ne sont pas déclarés résolus par cet ordre. RQ-12.01 est traitée en dernier conformément à sa fonction de comparaison ; cela ne transforme pas une priorité de travail en implication textuelle.

## RQ-03.02

Quelles conventions réconcilient T, dT, Work restant, travail accumulé et signes ?

Prérequis : RQ-03.01 (PARTIALLY_RESOLVED).

Dépendants directs : RQ-03, RQ-03.03, RQ-03.04, RQ-04.04, RQ-07.01, RQ-08.03.

CORE : CPC-0023, CPC-0040, CPC-0045.

MAJOR : CPC-0062, CPC-0063, CPC-0121.

Concepts : agent, energy, force, money, price, remaining, transformation, utility, work.

Chapitres : CH-03, CH-05, CH-09.

## RQ-08.03

Les potentiels locaux sont-ils des fonctions d’état intégrables et sommables sous leurs contraintes ?

Prérequis : RQ-03.02 (OPEN), RQ-03.04 (OPEN).

Dépendants directs : RQ-08.

CORE : aucun direct.

MAJOR : CPC-0004, CPC-0047, CPC-0115, CPC-0116.

Concepts : coefficient, money, price, transformation, utility.

Chapitres : CH-05, CH-08.

## RQ-08.01

Quelles unités, frontières et pondérations autorisent l’addition des contributions sans double compte ?

Prérequis : RQ-03.03 (AMBIGUOUS), RQ-06.01 (OPEN), RQ-07.01 (OPEN).

Dépendants directs : RQ-08, RQ-08.02, RQ-08.04.

CORE : aucun direct.

MAJOR : CPC-0037, CPC-0089, CPC-0111, CPC-0114, CPC-0126.

Concepts : cash, coefficient, money, price, production, productivity, purchasing, supply, transformation, unit, utility, work.

Chapitres : CH-02, CH-03, CH-07, CH-08.

## RQ-08.04

Le champ labour-prix et les normalisations locales/globales sont-ils invariants aux changements d’unités ?

Prérequis : RQ-08.01 (OPEN).

Dépendants directs : RQ-08.

CORE : aucun direct.

MAJOR : CPC-0089, CPC-0112, CPC-0116, CPC-0126.

Concepts : cash, coefficient, money, price, productivity, purchasing, transformation, unit, utility, work.

Chapitres : CH-02, CH-04, CH-08.

## RQ-06.04

Après traduction du vocabulaire, quelle restriction sur le crédit bancaire reste réellement contestable ?

Prérequis : RQ-06.02 (PARTIALLY_RESOLVED), RQ-02.02 (OPEN).

Dépendants directs : RQ-06.

CORE : aucun direct.

MAJOR : CPC-0013, CPC-0014, CPC-0050, CPC-0085.

Concepts : accounting, cash, deflation, distribution, inflation, money, purchasing, unit, wealth.

Chapitres : CH-01, CH-02, CH-03.

## RQ-10.01

Sous quelles conditions un gain de prix améliore-t-il le pouvoir d’achat réel plutôt qu’un simple indicateur nominal ?

Prérequis : RQ-05.01 (PARTIALLY_RESOLVED), RQ-05.03 (AMBIGUOUS), RQ-06.01 (OPEN).

Dépendants directs : RQ-10, RQ-10.02.

CORE : CPC-0015, CPC-0016, CPC-0053.

MAJOR : CPC-0076, CPC-0077, CPC-0078, CPC-0079.

Concepts : cash, money, price, productivity, purchasing, unit, work.

Chapitres : CH-02, CH-03, CH-04.

## RQ-09.03

GDP=K·W est-il testable indépendamment du PIB et avec des rendements, pertes et frontières explicites ?

Prérequis : RQ-09.02 (AMBIGUOUS), RQ-08.02 (PARTIALLY_RESOLVED).

Dépendants directs : RQ-09, RQ-10.03.

CORE : aucun direct.

MAJOR : CPC-0067, CPC-0108, CPC-0117, CPC-0118, CPC-0119.

Concepts : coefficient, energy, entropy, money, price, productivity, transformation, utility, work.

Chapitres : CH-08, CH-09, CH-10.

## RQ-11.02

L’usage du gain produit-il un rebond direct, indirect ou global, et dans quelles limites ?

Prérequis : RQ-10.02 (PARTIALLY_RESOLVED), RQ-09.01 (OPEN).

Dépendants directs : RQ-11, RQ-11.03.

CORE : aucun direct.

MAJOR : CPC-0084, CPC-0099, CPC-0120, CPC-0127.

Concepts : agent, cash, energy, money, price, productivity, purchasing, transformation, unit, work.

Chapitres : CH-02, CH-07, CH-09, CH-10.

## RQ-11.03

Quelle empreinte marginale attribuer aux matières, transports, énergie et externalités du panier supplémentaire ?

Prérequis : RQ-11.01 (PARTIALLY_RESOLVED), RQ-11.02 (OPEN).

Dépendants directs : RQ-11, RQ-12.03.

CORE : aucun direct.

MAJOR : CPC-0018, CPC-0031, CPC-0120, CPC-0127.

Concepts : agent, energy, environment, growth, living, money, price, work.

Chapitres : CH-01, CH-09, CH-10.

## RQ-12.01

Quelles observations départageraient Campergue des explications concurrentes à conditions comparables ?

Prérequis : RQ-03.03 (AMBIGUOUS), RQ-05.01 (PARTIALLY_RESOLVED), RQ-08.02 (PARTIALLY_RESOLVED), RQ-09.02 (AMBIGUOUS).

Dépendants directs : RQ-12, RQ-12.03.

CORE : CPC-0003.

MAJOR : CPC-0068, CPC-0117, CPC-0118, CPC-0119.

Concepts : coefficient, energy, money, price, productivity, transformation, utility, work.

Chapitres : CH-01, CH-04, CH-08, CH-09.

## Périmètres complémentaires sans renommage

RQ-06.04 reste la question du crédit : les bilans création/destruction couvrent aussi RQ-06.02/06.03. RQ-10.01 reste la question du gain réel : les usages demandés sont traités en liaison avec RQ-10.02, sans changer silencieusement son ID ni sa formulation.
