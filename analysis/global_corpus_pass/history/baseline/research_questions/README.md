# Programme de recherche navigable

État courant — troisième passe métrologique : [rapport](third_pass_report.md), [carte des variables](operationalization/README.md), [expériences proposées](operationalization/experiments.md). Dix dossiers enrichis; 26 entrées métrologiques; 272/562 pages couvertes; 127 claims inchangés. Les paragraphes de première et deuxième passe ci-dessous sont historiques. Le graphe, les statuts et la matrice actuels font foi. La littérature spécialisée MET-BIB est décomptée séparément du registre antérieur BIB.

**Deuxième passe disponible : [rapport](second_pass_report.md), [dépendances préalables](second_pass_dependency_map.md), [matrice actualisée](evidence_matrix.csv).** Dix nouveaux dossiers ciblés,271/562 pages couvertes,127 claims inchangés. Les13 dossiers de première passe restent conservés ; les chiffres historiques ci-dessous décrivent leur initialisation, non le dernier état. La matrice et le graphe version2 font foi. Les générateurs initiaux refusent d’écraser les conclusions révisées ; ne pas les employer pour régénérer rétroactivement la première passe.

Point d’entrée : [arbre des questions](questions.md), [statuts actuels](status.md), [bilan et priorités](first_pass_report.md), [graphe structuré](question_graph.json).

**53 questions hors RQ-ROOT**, dont12 problèmes de synthèse et41 sous-questions opérationnelles. Les synthèses ne sont pas douze expériences indépendantes supplémentaires. Les dix chapitres restent des classifications transversales du corpus. Les familles couvrent définition du phénomène, richesse, Work, transformation, répartition du gain, monnaie, agents, agrégation, énergie, usage, dommages et identification causale. Ce découpage rend visibles des maillons que la structure des chapitres rapproche sans nécessairement les démontrer.

La question exacte commence page PDF2 et se termine page3. La phrase associée est page3. [Dossier racine](RQ-ROOT/README.md). Les questions autres que la racine sont des **RESEARCH_INTERPRETATION**, pas des questions citées du manuscrit.

Chaque dossier contient README, corpus, evidence, literature, tests et conclusion. Les13 dossiers de première passe réutilisent et confrontent les analyses déjà réalisées ; les autres sont des dossiers d’orientation, **pas des recherches achevées**. Aucun ne revendique tous les passages pertinents des562 pages. Couverture générale inchangée247/562 : relecture ciblée, aucune page nouvelle comptabilisée.

## Naviguer dans les preuves

- [Question ↔ claim](claim_question_matrix.csv) : un lien est une pertinence analytique, pas une implication logique.
- [Tableau de preuves](evidence_matrix.csv) : TEXTUAL atteste une attribution ; FORMAL contrôle un calcul ; EMPIRICAL dépend du protocole ; COUNTEREXAMPLE précise une restriction. Compter des lignes n’est pas mesurer la force scientifique.
- Chaque evidence.md précise source, force et limite ; chaque corpus.md sépare SOURCE et INTERPRETATION.
- La littérature est reliée seulement aux13 dossiers examinés. Les mêmes références peuvent servir plusieurs questions ; elles ne deviennent pas plusieurs preuves indépendantes.
- Les protocoles des40 autres questions, dont les synthèses, restent SCOPING_ONLY. Les13 protocoles détaillés ne sont pas tous exécutables avec les données actuelles.

## Lire le graphe

`A DEPENDS_ON B` : répondre à A requiert de clarifier B ; ce sont des prérequis de recherche proposés par l’analyste, non des implications textuelles. `A PART_OF B` : A est une sous-question de B. `RQ-12.03 ANSWERS RQ-ROOT` désigne la destination de la réponse, encore OPEN. Ne pas lire ANSWERS comme une réponse déjà démontrée. L’acyclicité se vérifie par type de relation, pas sur une fusion arbitraire des flèches.

Les catégories BLOCKING, HIGH_VALUE, EASY_WIN, EMPIRICAL, FORMAL et OPEN sont des **étiquettes non exclusives**. Elles ne sont pas les statuts épistémiques. Une question PARTIALLY_RESOLVED peut rester BLOCKING et nécessiter des données.

## Versionner sans effacer

Le catalogue questions.md a été écrit **avant** les dossiers ; son état initial OPEN est conservé dans history/001_initial_questions.md. questions.md, status.md, les dossiers et question_graph.json contiennent maintenant l’état après première passe. history.json enregistre les13 transitions de statut, leurs raisons et leurs preuves ; aucun état initial n’a été effacé.

Les anciens IDs `RQ-01-01`…`RQ-10-01` restent inchangés dans `analysis/data/research_questions.json`. Les nouveaux utilisent un point (`RQ-01.01`) : aucun renommage silencieux. Ils ne remplacent pas les anciennes questions de chapitres.

Pour toute révision : archiver l’état précédent, ajouter à history.json ID, ancienne/nouvelle formulation ou statut, justification et nouvelles preuves. Conserver une question retirée avec action DEPRECATED ; une division avec SPLIT_INTO et IDs cibles. Ces actions de cycle de vie restent distinctes des statuts scientifiques. Ne jamais recycler un ID.

Les générateurs `analysis/build_research_question_tree.py` et `analysis/research_question_dossiers.py` refusent d’écraser un fichier divergent. Leur rôle est de produire la structure à partir d’un catalogue éditorial, pas de déduire automatiquement les conclusions. Une nouvelle version exige un archivage explicite ; adapter ensuite le catalogue et les dossiers ensemble.

## Reproduire les contrôles

```bash
.venv-research/bin/python analysis/verify_research_questions.py
./verify.sh
```

Le contrôleur valide les liens, citations, statuts, couverture des claims et fichiers. Les questions ouvertes produisent WARNING ; aucune obligation de résolution n’est imposée pour obtenir PASS. Les résultats micro et énergétiques antérieurs restent conservés ; aucune expérience supplémentaire n’a été lancée pour remplir l’arbre.

## Quatrième passe — expériences locales

[Rapport](fourth_pass_report.md), [protocoles et sélection](experiments/selection.md). Trois extensions formelles exécutées; quatre questions concernées, statuts conservés. Les affirmations sources ne sont pas effacées. Cadrage: définitions, constructions, relations, principes proposés, analogies, mécanismes et exemples évalués séparément; aucun verdict global.

## Cinquième passe — contribution et cadres existants

[Rapport](fifth_pass_report.md) · [matrice et comparaisons](contribution/README.md). 24 CORE, 21 entrées conceptuelles, 32 scénarios monétaires comparés; 21 questions annotées. Originalité historique et valeur empirique non établies. Définitions, sources et statuts scientifiques conservés.
