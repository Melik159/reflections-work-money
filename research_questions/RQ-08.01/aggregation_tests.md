# Deux puis trois produits

Le test à deux produits existant est conservé dans `analysis/empirical/micro_electricity/two_product_results.json` et recalculé par verify.sh. La seconde expérience utilise A/B inchangés, puis C : prix5→4, quantité8→1, coefficient K=4 et contribution T par copie1. Les données sont **synthétiques**, non mesures de Campergue.

Le panier initial coûte200 puis184 aux nouveaux prix : indice0,92. La moyenne correctement pondérée des indices individuels donne0,92, leur moyenne égale0,933333. Les K locaux(0,5;2;4) donnent K agrégé72/43≈1,6744 puis44/51≈0,8627 lorsque la composition change. Cela montre la nécessité de poids, pas une inconsistance de l’addition elle-même.

**Correction de portée de la critique antérieure : p.108 dit explicitement que Utility n’est pas additive.** Le changement de signe d’une somme arbitraire de qualités était un diagnostic de mesure proposé par l’analyste ; ce n’est pas une règle d’agrégation imputable à Campergue. Aucune somme d’Utility n’est effectuée dans le test à trois produits.

Double compte : la contribution physique de la machine ne peut être comptée une seconde fois comme contribution physique intégrale de son opérateur. Il s’agit d’un contrôle de frontière proposé, pas d’un double compte effectivement mesuré dans le manuscrit.

Les potentiels locaux exigent en plus leur exactitude ; addition de fonctions d’état sur un espace produit possible si elles sont définies et si interactions/contraintes sont traitées. Un champ de vecteurs ne fournit pas cette somme. Voir RQ-08.03 et RQ-08.04.
