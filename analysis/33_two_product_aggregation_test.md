# 33 — Deux produits : conditions de l’agrégation

**FORMALLY_CONSISTENT ; NON_DISCRIMINATING.** Expérience entièrement synthétique, pas des données ni une calibration des variables de Campergue. Sources motivant le diagnostic : manuscrit p.210 (contributions), 406 (flux à prix commun), 441 (coefficient constitutif), 536–538 (local/global), 558–559 (entreprises et coefficient agrégé) ; analyse28 et CPC-0111/0116/0126. Les règles ci-dessous sont des hypothèses analytiques explicites, non une nouvelle loi attribuée à l’auteur.

| Produit | Prix 0→1 | Coût 0→1 | Quantité 0→1 | Points de qualité 0→1 |
|---|---:|---:|---:|---:|
| A | 10→8 | 8→6 | 10→20 | 4→5 |
| B | 20→24 | 12→14 | 3→2 | 9→8 |

Prix/coût : même monnaie par copie ; quantités : copies de chaque produit. Les points de qualité n’ont **pas** d’équivalence interproduits établie et ne mesurent pas l’Utility du manuscrit.

## Somme et normalisation

Le panier initial coûte160 puis152 aux nouveaux prix : économie8, indice de Laspeyres0,95. La moyenne des indices individuels0,8 et1,2, pondérée par les dépenses initiales100/160 et60/160, restitue exactement0,95. Leur moyenne équipondérée donne1 : **autre pondération, autre question**, pas contradiction arithmétique. Avec les quantités finales, l’indice vaut208/240=0,866667. La dépense effectivement composée passe160→208 : elle augmente malgré l’économie à panier initial fixe.

Dollars→centimes laisse les indices inchangés. Vendre B par paquets de deux (prix et coût doublés, quantité divisée par deux) conserve la dépense. Il faut transformer simultanément les grandeurs et les poids. L’agrégation avant/après normalisation est donc compatible **sous ces conditions**, pas indépendamment de toute pondération.

## Utility et coefficient

La somme des points, aux quantités initiales, passe67→74. En multipliant seulement l’échelle des points de B par100, elle passe2740→2450 : les évolutions propres à chaque produit restent identiques, le signe agrégé change. Cela montre la nécessité d’une métrique commune si l’on veut sommer ; cela ne démontre pas que Campergue autorise ce changement arbitraire.

Posons, dans des unités économiques abstraites déclarées, T par copie=(2,5), K=(0,5;2) et Mᵢ=KᵢTᵢ. Les totaux additifs donnent K₀=40/35=1,142857 puis K₁=40/50=0,8, sans modifier les K individuels. Répliquer chaque produit mille fois ne change aucun de ces rapports. Le grand nombre seul ne garantit donc pas la stabilité face à la composition. Ce contre-exemple porte sur la suffisance de cette condition, non sur toute l’analyse p.559.

**NOT_IDENTIFIABLE** : agrégat unique de Money ou d’Utility empirique, faute de calibration commune. A conserve ici un profit unitaire absolu2 ; B le voit passer8→10. Ces profits sont connus dans le jouet parce que les coûts totaux sont fournis ; ils ne légitiment pas l’usage du différentiel prix résidentiel–combustible comme marge dans le cas électrique.

Reproduction : `.venv-research/bin/python analysis/run_two_product_aggregation.py --check`. Entrées, hypothèses et résultats : `analysis/empirical/micro_electricity/two_product_results.json`.
