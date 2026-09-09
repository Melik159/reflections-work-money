# Historique d’exécution

Baseline:120/120PASS. Le premier contrôle du nouveau validateur a échoué sur un chemin d’import; chemin du dépôt rendu explicite. Première exécution complète des tests unitaires:127/128, un contrôle historique exigeait encore l’égalité binaire des claims. Le contrôle vérifie désormais tous les champs antérieurs inchangés et l’historique des ajouts; aucune assertion de provenance n’a été retirée sans remplacement. Résultat initial conservé dans first_test_failure.json.

Les nouveaux contrats verrouillent un ensemble fini d’énoncés relus et leurs passages. Ils ne résolvent PAS la compréhension sémantique générale; ils rendent détectables les mutations demandées. Une nouvelle conclusion légitime exige une revue et un historique, pas une mise à jour automatique du contrat. verify.sh ne rafraîchit pas les empreintes d’entrée: seul le script explicite de remédiation le fait, en historisant chaque changement.

Les verdicts externes restent inchangés dans external_review/. Le reclassement post-remédiation de CPC-0016 est proposé pour contrôle de clôture, non nouvelle expertise externe.
