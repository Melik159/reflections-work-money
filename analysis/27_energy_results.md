# Résultats indépendants PIB–énergie

Source et protocole : rapport27. Fenêtre1990–2023 ; régression PIB sur énergie, pas sens causal. IC95% HAC(3) asymptotiques. Tests exécutés ; aucune interpolation. Les niveaux sont en milliards USD constants2015 par TWh.

| Expérience / modèle | Zone | N | Période | Coefficient énergie | IC95% | R² |
|---|---|---:|---|---:|---|---:|
| TEST-E1 / level | CHN | 34 | 1990–2023 | 0.4044 | [0.3615, 0.4472] | 0.9659 |
| TEST-E1 / loglog | CHN | 34 | 1990–2023 | 1.4631 | [1.3421, 1.5841] | 0.9811 |
| TEST-E1 / dlog | CHN | 33 | 1991–2023 | 0.3238 | [0.0871, 0.5604] | 0.2190 |
| TEST-E2 / per_capita_loglog | CHN | 34 | 1990–2023 | 1.5127 | [1.3670, 1.6585] | 0.9757 |
| TEST-E1 / level | DEU | 34 | 1990–2023 | -1.4667 | [-1.9856, -0.9478] | 0.5813 |
| TEST-E1 / loglog | DEU | 34 | 1990–2023 | -1.7282 | [-2.4619, -0.9945] | 0.5434 |
| TEST-E1 / dlog | DEU | 33 | 1991–2023 | 0.3310 | [0.0664, 0.5956] | 0.2224 |
| TEST-E2 / per_capita_loglog | DEU | 34 | 1990–2023 | -1.4067 | [-2.0902, -0.7233] | 0.5466 |
| TEST-E1 / level | FRA | 34 | 1990–2023 | -0.5603 | [-1.0781, -0.0424] | 0.1442 |
| TEST-E1 / loglog | FRA | 34 | 1990–2023 | -0.6624 | [-1.3205, -0.0044] | 0.1150 |
| TEST-E1 / dlog | FRA | 33 | 1991–2023 | 0.3063 | [0.0195, 0.5930] | 0.2844 |
| TEST-E2 / per_capita_loglog | FRA | 34 | 1990–2023 | -0.5804 | [-0.8561, -0.3046] | 0.3791 |
| TEST-E1 / level | IND | 34 | 1990–2023 | 0.3242 | [0.3051, 0.3432] | 0.9911 |
| TEST-E1 / loglog | IND | 34 | 1990–2023 | 1.2801 | [1.2498, 1.3105] | 0.9975 |
| TEST-E1 / dlog | IND | 33 | 1991–2023 | 0.7490 | [0.2618, 1.2363] | 0.4593 |
| TEST-E2 / per_capita_loglog | IND | 34 | 1990–2023 | 1.4121 | [1.3683, 1.4559] | 0.9949 |
| TEST-E1 / level | USA | 34 | 1990–2023 | 1.8374 | [1.0714, 2.6035] | 0.4057 |
| TEST-E1 / loglog | USA | 34 | 1990–2023 | 3.3990 | [2.2454, 4.5525] | 0.4944 |
| TEST-E1 / dlog | USA | 33 | 1991–2023 | 0.5343 | [0.3919, 0.6767] | 0.5979 |
| TEST-E2 / per_capita_loglog | USA | 34 | 1990–2023 | -1.3966 | [-1.9887, -0.8045] | 0.5144 |
| TEST-E1 / level | WLD | 34 | 1990–2023 | 0.7070 | [0.6613, 0.7527] | 0.9876 |
| TEST-E1 / loglog | WLD | 34 | 1990–2023 | 1.5349 | [1.4585, 1.6114] | 0.9918 |
| TEST-E1 / dlog | WLD | 33 | 1991–2023 | 0.8646 | [0.6202, 1.1089] | 0.7859 |
| TEST-E2 / per_capita_loglog | WLD | 34 | 1990–2023 | 2.8702 | [2.4590, 3.2813] | 0.9355 |

## E3 — Stabilité descriptive

Découpage fixé à2007 avant estimation, deux sous-échantillons de17 observations chacun. Modèle joint avec intercept et pente propres à chaque période. IC de la différence : HAC(3) du coefficient interaction. Pas de correction pour comparaisons multiples ; résultats exploratoires.

| Zone | β1990–2006 | β2007–2023 | Δβ | IC95% Δβ |
|---|---:|---:|---:|---|
| CHN | 1.4622 | 1.8342 | 0.3719 | [-0.0260, 0.7699] |
| DEU | -1.8358 | -0.5434 | 1.2924 | [-1.3839, 3.9686] |
| FRA | 1.9563 | -0.4728 | -2.4291 | [-3.0173, -1.8409] |
| IND | 1.3062 | 1.3950 | 0.0888 | [-0.0139, 0.1915] |
| USA | 2.5603 | 0.7647 | -1.7956 | [-3.9174, 0.3261] |
| WLD | 1.5867 | 1.7813 | 0.1946 | [-0.0210, 0.4101] |

### Restriction GDP=K·W à K constant

Diagnostic supplémentaire **du même E3**, sans quatrième expérience : le ratio observé devrait être stable si cette opérationnalisation forte était exacte. Sa variation n’est pas une mesure directe de K économique ; elle documente le coût empirique de cette identification.

| Zone | PIB2023/1990 | Énergie2023/1990 | (PIB/E)2023/1990 | CV(PIB/E) |
|---|---:|---:|---:|---:|
| CHN | 16.913 | 5.930 | 2.852 | 0.287 |
| DEU | 1.563 | 0.758 | 2.062 | 0.182 |
| FRA | 1.648 | 0.908 | 1.815 | 0.206 |
| IND | 7.019 | 4.706 | 1.491 | 0.138 |
| USA | 2.255 | 1.160 | 1.944 | 0.208 |
| WLD | 2.609 | 1.797 | 1.452 | 0.107 |

## Interprétation

Monde : forte association positive en niveaux et co-mouvement annuel. France/Allemagne : tendances de niveau opposées, mais co-mouvements annuels positifs. La France change de signe entre sous-périodes. La pente française globale est fragile (IC proche de zéro), pas une estimation robuste d’un effet négatif de l’énergie. Les tendances incluent chocs, mutations sectorielles et échanges internationaux.

Les associations sont non spécifiques. La version strictement constante de GDP=K·W, avec nos proxies, ne décrit pas ces trajectoires ; cela distingue une restriction particulière d’une explication standard autorisant découplage et coefficients variables. Ce n’est pas une confirmation positive du formalisme Campergue et ne rejette pas toutes ses branches. E1/E2 : ASSOCIATION ou TEMPORAL_CO_MOVEMENT ; E3 : ASSOCIATION/stabilité ; causalité et prévision hors échantillon NOT_IDENTIFIABLE / NOT_TESTED.
