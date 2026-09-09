# RQ-06.04 — tests de deuxième passe

Exécuté : ΔM31 versus premier ordre30 avec terme croisé1. DESIGNED_NOT_EXECUTED : choc de crédit, production/prix/distribution et horizon fixés ; dépôts seuls non discriminants.

Hypothèse/prédiction : M constant implique u=M/n, mais ne prouve pas que tout crédit satisfait cette prémisse. Variation finie du produit comprend Δn·Δu.

Variables et données : Création/destruction de Money, transfert et réévaluation ont des niveaux distincts ; les32 scénarios antérieurs restent tous conservés.

Conditions : Frontière isolée et agents identifiés ; horizon de compensation explicitement instantané ou différé ; production supplémentaire séparée de l’écriture de prêt.

Résultat incompatible ou contre-exemple : Un bilan prêt+dépôt ne comporte aucune équation imposant les prix immédiatement inverses du montant de dépôts. Cela contredit une déduction purement comptable, pas la branche conditionnelle posée par Campergue.

Explications concurrentes / domaine : Mélange quotidien des possibilités admis p18 ; épargne réserve p255/468 ; banque utile socialement même dans ce classement.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.
