# Audit des120tests

Catégories primaires exclusives, méthode par méthode; unités de comptage = méthodes unittest, pas assertions ni modèles estimés. Les tests hybrides sont signalés.

| Catégorie | Nombre |
|---|---:|
|INTEGRITY_TEST|15|
|PROVENANCE_TEST|60|
|LOGIC_TEST|27|
|FORMAL_TEST|16|
|EMPIRICAL_REPRODUCTION_TEST|2|
|SCIENTIFIC_VALIDITY_TEST|0|

102 contrôlent principalement les artefacts et la logique du pipeline; 16 des propriétés mathématiques locales; 2 la reproduction numérique de données. Zéro test SCIENTIFIC_VALIDITY_TEST au sens étroit d'une prédiction économique indépendante et discriminante. Cela n'enlève pas la valeur scientifique des diagnostics mathématiques négatifs.

## Ce que PASS ne signifie pas

La citation peut être présente mais insuffisante; le graphe peut être acyclique sans implication valide; un statut peut être verrouillé tout en étant erroné. Les14tests de synthèse sont des contrôles d'infrastructure/provenance/logique, pas14preuves économiques.

Deux contre-épreuves réellement exécutées dans independent_checks.py, sans changer les fichiers, montrent que validate accepte SYN-01 avec une phrase erronée affirmant une neutralité causale autonome, et accepte README.md comme source de ce résultat. Il teste l'existence du chemin, non son entailment. Le rapport interne annonce déjà cette limite générale, mais la garantie « aucune conclusion sans source » doit être lue au sens structurel, non sémantique.

Les calculs énergétiques et électriques sont bien réexécutés dans verify et dans des méthodes dédiées. Plusieurs tests au nom empirique ne font cependant que comparer des drapeaux. Les reconstitutions de tableaux et le smoke test amont ne constituent pas de nouvelles observations. Le golden set RAG mesure la récupération de passages annotés, pas leur vérité ni une performance externe à la sélection de questions.

Remédiation proposée : associer des rôles de preuve à chaque lien, ajouter des cas de mauvaise source pertinente en apparence, isoler les attestations documentaires des évaluations scientifiques et conserver un holdout de retrieval. Ne pas remplacer ces contrôles utiles par un score global de justesse.

## Inventaire complet

Voir test_audit.csv pour120lignes avec fichier et numéro de ligne. Toutes les méthodes y figurent, y compris les contrôles de l'audit global et de la synthèse. Le dénombrement est comparé à la liste réellement exécutée dans baseline.json.
