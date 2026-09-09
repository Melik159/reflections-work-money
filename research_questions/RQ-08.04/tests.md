# RQ-08.04 — tests de deuxième passe

Exécuté : substitution13≠35 ; pente0,5→50 en centimes, pente normalisée identique. Le test n’autorise pas une correction silencieuse de l’équation source.

Hypothèse/prédiction : MINIMAL_RECONSTRUCTION : choisir échelles explicites l0,p0 avant norme/angle. Transformer e, a et cp,ca ensemble. Cela ajoute une métrique, non fournie comme telle par le texte.

Variables et données : Scalaire Ω=varpi/ω=−dp/dl p548 ; métrique vectorielle et transformations p553–554 ; n local versus N global p537.

Conditions : Même Product, unités fixées, métrique commune, indices pos/neg conservés ; normalisation M/N distinguée du M initial.

Résultat incompatible ou contre-exemple : Avec cp=2,ca=3,e=4,a=9, norme carrée issue des vitesses=13 ; expression e²/cp+a²/ca=35. Incompatibilité sous mêmes variables, sauf reparamétrage supplémentaire. Page554 inspectée visuellement.

Explications concurrentes / domaine : Ratio prix/tâche possède des unités ; un angle numérique change avec dollars→centimes sans renormalisation. La visualisation reste possible dans une convention donnée.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.
