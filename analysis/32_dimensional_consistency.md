# 32 — Cohérence dimensionnelle du sous-modèle micro

Périmètre : formules déjà transcrites et sourcées dans `productive_formulas.json`, pages197–208,456,501 ; scénarios20–21 et503–506. Pas de nouvelle unité attribuée au manuscrit. Les dimensions symboliques ci-dessous sont des **inférences de l'analyste** ; elles ne constituent pas une calibration empirique.

## Grandeurs économiques

Notons ℒ une unité abstraite de tâche, τ le temps, π l'unité de prix d'un exemplaire, ℰT et ℰM les unités encore non calibrées de Work et Money. Ces lettres sont des auxiliaires de ce rapport, pas des notations ajoutées à Campergue.

| Relation | Dimensions nécessaires | Niveau / intensité | État de résolution |
|---|---|---|---|
| ω=−dl/dt, p.197 | [ω]=ℒ/τ | Vitesse locale, pas quantité produite par an automatiquement | ℒ physique/opérationnelle UNRESOLVED |
| varpi=dp/dt, p.198 | [varpi]=π/τ | Vitesse de formation du prix d'un exemplaire | Ne pas remplacer par variation annuelle du prix moyen de produits différents |
| FP=cp·dω/dt, p.201 | [cp]=ℰT·τ²/ℒ² ; [FP]=ℰT/ℒ | Force et coefficient de complexité locaux | Calibration cp UNRESOLVED |
| dT=−FP·dl ; dT=cpωdω, p.471 | [dT]=ℰT | Variation, pas stock | Convention de signe/référent à conserver ; dT=0 n'impose pas T=0 |
| T=½cpω², p.207 | [T]=ℰT | Primitive à zéro choisi ; somme possible seulement à référent commun | Comparaison au travail physique UNRESOLVED |
| dM=FA·dp ou −FA·dp selon référent, p.204/415 | [FA]=ℰM/π | Variation de Money | Les deux conventions du corpus ne doivent pas être mélangées |
| M=n·u | [u]=ℰM/[n] | n nombre d'unités, M quantité économique | π, USD nominal et ℰM ne sont pas identifiés par cette identité |
| a=−ca·varpi, p.208 | [ca]=ℰM·τ²/π² ; [a]=ℰM·τ/π | Caractéristique dynamique locale | Ni kWh/USD ni revenu réel par simple renommage |
| p=½(e·Ch)(l/T), p.501 | Avec e=cpω et T=½cpω² : p=Ch·l/ω ; [Ch]=π/τ | Prix d'un exemplaire pour tâche donnée | Le rapport l/ω est une durée ; pas le rendement thermique Btu/kWh |
| ηTM=−M/T | Rapport ℰM/ℰT | Rendement de transformation | Sans unité économique commune, pas un nombre sans dimension automatiquement |
| Q=−M/(Πηphys·Πηecon), p.456 | Si tous η sont sans dimension, M doit être exprimé dans une unité compatible avec Q | Énergie physique extensive d'un processus | Conversion économique→joules UNRESOLVED |

Si une conversion κ en joules par unité économique était requise, l'analyste devrait l'identifier indépendamment, et non lui donner arbitrairement la valeur1. Ce κ est une **condition de mesure proposée**, pas une formule citée du manuscrit. Le fait de réexprimer kWh en joules ne résout pas la conversion de Money en énergie.

## Grandeurs observées dans le cas électrique

| Symbole de travail | Mesure | Dimension et périmètre |
|---|---|---|
| h | Heat rate gaz, Btu/kWh net | Intrant énergétique par énergie électrique produite ; ratio physique intensif, hors cogénération dans sa source |
| f | Coût moyen des réceptions de gaz, USD/MMBtu | Prix d'un intrant, pas coût total de production ; échantillon distinct de h |
| c_hat=f·h/10000 | cents/kWh | 100cents/USD × 1MMBtu/10⁶Btu ; proxy faible, produit de moyennes |
| η_heat=3412/h | sans dimension | Rendement thermique approximatif sur pouvoir calorifique supérieur ; ce n'est pas ηTM |
| P | Prix résidentiel moyen, cents/kWh | Recettes/ventes, taxes comprises ; livraison au client, tous modes de génération |
| Qprod, Qsold | millions de kWh par année | Totaux de flux sur l'année, non stocks ; production et ventes ont des frontières différentes |
| CPI | Indice général BLS | Sans dimension, moyenne annuelle de12 observations mensuelles |
| P_real=P·CPI2023/CPIt | cents2023/kWh | Prix relatif au panier CPI, non à Utility constante démontrée |
| G_nom=1000·(Pprevious−Pcurrent)/100 | USD pour1000kWh | Économie nominale pour panier fixe ; positive seulement si prix baisse |
| G_real=1000·(Preal_previous−Preal_current)/100 | USD2023 pour1000kWh | Comparaison de prix déflatés, pas gain de revenu observé |
| B_nom=10000/P | kWh pour100USD courants | Budget nominal fixe ; pas revenu effectivement constant des ménages |
| B_real=10000/P_real | kWh pour100USD2023 | Budget réel conventionnel fixe |
| SAIDI | minutes d'interruption/client/an | Qualité partielle intensive ; pas Utility subjective |

3412Btu/kWh est le facteur arrondi de contenu calorifique de l'électricité de la tableA6. Il ne faut pas confondre ce facteur de conversion avec les Btu **consommés** par kWh h, plus élevés à cause des pertes. Il ne mesure pas de création économique.

## Deux erreurs dimensionnellement discrètes

**Même unité, différent objet.** P et c_hat sont tous deux en cents/kWh ; leur différence est calculable mais n'est pas une marge. Réseau, capital, autres combustibles, achats de gros, taxes, échantillons et calendriers restent différents. Une cohérence dimensionnelle n'établit pas une correspondance économique.

**Produit des moyennes ≠ moyenne des produits.** Même avec une population commune, moyenne(f)×moyenne(h) diffère généralement de moyenne(fh), et les poids peuvent différer. Ainsi c_hat n'est pas même une mesure directe du coût combustible moyen observé d'une entreprise représentative.

## Lecture du test

La régression emploie des logarithmes de ratios annuels (sans dimension). Son coefficient ne convertit pas des dollars en Economic Work. Une décomposition Δlog(c_hat)=Δlog(f)+Δlog(h) est arithmétiquement exacte pour **notre proxy construit** ; elle ne constitue pas une découverte empirique d'une loi Campergue. Une baisse de h peut refléter composition ou dispatch plutôt qu'une transformation accélérée d'une même installation.

Conclusion dimensionnelle : calculs physiques et budgétaires définissables ; unités de cp, Utility interproduits et pont T/M/énergie **UNRESOLVED**. Aucun remplacement par une unité inventée pour obtenir artificiellement un test.
