# RQ-10.01 — tests de deuxième passe

Recalcul du panel et du gain à1000kWh existants dans verify. DESIGNED_NOT_EXECUTED : suivi des budgets après baisse de prix avec épargne/dettes/usages séparés.

Hypothèse/prédiction : Gain de panier fixe Σq0(p0−p1), puis déflation séparée ; durée de vie du pneu peut modifier le coût de service sans seule baisse du prix d’achat.

Variables et données : Pouvoir d’achat usuel panier/revenu versus a=−ca·varpi ; qualité/durée d’usage versus Utility. Ne pas fusionner ces mesures.

Conditions : Même budget, service, qualité et frontière ; distinguer nominal/réel ; aucune proportion universelle d’affectation du gain.

Résultat incompatible ou contre-exemple : Le cas électrique ne mesure pas un surplus : prix réel moyen en hausse entre bornes malgré proxy de combustible en baisse. Ce n’est pas un contre-exemple à la branche à coût total/profit/qualité constants.

Explications concurrentes / domaine : Gain épargné ou reporté ; dette et taxes ; investissement du surplus seulement possibilité économique tant qu’un passage ne l’établit pas directement.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.
