# RQ-08.03 — tests de deuxième passe

Exécuté : contre-exemple y·dx et contrôle positif d(xy)=y·dx+x·dy, deux chemins donnent1. DESIGNED_NOT_EXECUTED : boucles économiques avec états et coefficients mesurés.

Hypothèse/prédiction : La règle du produit restitue le différentiel si dETM=−UP·dP+FA·dp. Une fonction d’état C2 implique les identités de Maxwell ; l’absence de pertes seule ne démontre pas l’exactitude d’une forme différentielle.

Variables et données : ETM^L=ETM+UP·P ; différentiel p415 P·dUP+FA·dp ; le rappel p427 emploie dV. Potentiel et transfert doivent être distincts.

Conditions : Coordonnées et p/V définis sans permutation ; domaine approprié ; fonctions suffisamment différentiables ; contraintes maintenues ; somme seulement de fonctions compatibles.

Résultat incompatible ou contre-exemple : Forme y·dx entre(0,0) et(1,1) : intégrales0 ou1 selon chemin, sans invoquer de variable de pertes. Nommer les endpoints ne crée pas un potentiel. Exemple analytique, pas ajustement du manuscrit.

Explications concurrentes / domaine : Un potentiel mathématique peut exister malgré une trajectoire dissipative ; c’est le transfert qui dépend alors du chemin. Ne pas imposer ce vocabulaire physique sans reconnaître la restriction économique de l’auteur.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.
