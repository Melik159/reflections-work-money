# 34 — Électricité : une chaîne microéconomique identifiable ?

**Résultat de la chaîne : NOT_IDENTIFIABLE ; spécificité : NON_DISCRIMINATING.** Le cas est un secteur national, pas un panel de producteurs et clients appariés. Il documente la faisabilité d’une enquête micro, sans remplir toutes ses conditions. Protocole31 écrit avant acquisition, sélection et amendement conservés séparément ; aucune sélection de régression suivant ses résultats.

## Sources et périmètres

États-Unis2001–2023,23 observations annuelles ; qualité2014–2023,10 observations. Les fichiers bruts, URL, tailles et SHA256 sont archivés dans `analysis/empirical/micro_electricity/source/manifest.json`. Acquisition sans clé payante : `analysis/acquire_micro_electricity.py` ; calcul ensuite entièrement hors ligne.

Les [tables EIA MER](https://www.eia.gov/totalenergy/data/monthly/) fournissent prix résidentiel9.8, coût du gaz reçu9.9, heat rateA6, production7.2b et ventes7.6. Les prix annuels publiés sont utilisés, sans moyenne mensuelle non pondérée ni interpolation. La population du coût combustible change en2002 et2013 : les transitions correspondantes sont exclues de l’unique régression, mais conservées et signalées dans les tendances. Les achats de gaz ne sont pas nécessairement sa consommation contemporaine. Voir [notes EIA9.9, page PDF13](https://www.eia.gov/totalenergy/data/monthly/pdf/sec9.pdf).

Le [heat rate](https://www.eia.gov/electricity/annual/html/epa_08_01.html) concerne des centrales électriques, excluant notamment la cogénération ; le prix vendu au ménage incorpore un autre périmètre. Le produit de deux moyennes ne restitue pas nécessairement le coût moyen pondéré des mêmes centrales. Notre coût combustible est donc un **WEAK_PROXY**, jamais coût total. Énergie primaire combustible, électricité produite et électricité livrée restent distinctes.

Le CPI général BLS CUUR0000SA0 est acquis par [API publique](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2021&endyear=2023), en trois fenêtres : moyenne des12 mois, rebasage en dollars2023. Ce déflateur général ne corrige ni qualité électrique ni revenu individuel. Tentative CSV FRED inaccessible (404), conservée dans le journal d’acquisition. Aucun manque dans les23 années des séries retenues ; pas de fiabilité avant2014 dans cette sélection.

## Mesures et résultats

| Variable | 2001 | 2023 | Interprétation |
|---|---:|---:|---|
| Prix résidentiel, cents/kWh | 8,58 | 16,00 | +86,48% nominal |
| Prix en cents2023/kWh | 14,7647 | 16,00 | +8,37% réel CPI |
| Gaz reçu, USD/MMBtu | 4,487 | 3,36 | intrant acheté, pas coût total |
| Heat rate gaz, Btu/kWh | 10051 | 7721 | −23,18% ; composition du parc possible |
| Coût combustible construit, cents/kWh | 4,5099 | 2,5943 | −42,48% ; populations non appariées |
| Production gaz, millions kWh | 554939,682 | 1699855,345 | +206,31% ; substitution du mix possible |
| Ventes résidentielles, millions kWh | 1201606,593 | 1450025,184 | +20,67% ; population et usages variables |

Ces variations sont descriptives, pas des effets de traitement. Aucune consommation totale d’énergie n’est reconstruite en multipliant un heat rate d’un sous-ensemble par la production d’un ensemble différent.

Régression unique : Δlog(prix résidentiel nominal)=α+βΔlog(coût combustible proxy)+ε. **N=20**, transitions2003–2012 et2014–2023 ; β=**0,01428**, erreur-type HAC2=0,01094, IC95% asymptotique=[−0,00716;0,03572], R²=0,03190. Bartlett/Newey-West à distances calendaires, correction N/(N−2). Ni effet causal, ni coefficient structurel de transmission : coûts omis, délais réglementaires, mix et demande non contrôlés ; intervalle asymptotique fragile avec20 points. L’absence d’association précise ne réfute pas la transmission conditionnelle de coûts totaux.

## Cinq prédictions conditionnelles et concurrents

Les formulations sont des **hypothèses de recherche dérivées**, pas des citations supplémentaires. Citations et conditions originales restent dans les claims indiqués et les mécanismes PM associés.

| Prédiction / sources PDF | Conditions, horizon, incompatibilité pertinente | Résultat ; explication concurrente |
|---|---|---|
| PRED-MICRO-01 ; CPC-0096 p.32, CPC-0019 | Intensité d’intrant moindre, prix de cet intrant fixe, même produit/frontière ; effet comptable immédiat. Coût de cet intrant accru à conditions réellement fixes serait incompatible. | FORMALLY_CONSISTENT ; NON_DISCRIMINATING. f×h baisse avec h à f fixe, par construction ; technique standard et substitution du parc donnent aussi ce résultat. Heat rate n’est pas la vitesse de tâche. |
| PRED-MICRO-02 ; CPC-0098 p.504, contexte503–506 | Coût total unitaire moindre, **profit absolu unitaire constant**, même qualité et autres conditions ; comparaison avant/après, aucun délai numérique imposé. Prix non réduit malgré ces conditions vérifiées serait incompatible. | NOT_IDENTIFIABLE. Ni coût total ni profit appariés ; comptabilité P=C+profit et concurrence produisent également cette branche. |
| PRED-MICRO-03 ; CPC-0097 p.20, contexte20–21 | Coût total moindre, prix maintenu, mêmes quantités unitaires/frontière ; profit unitaire accru. Profit non accru toutes ces conditions fixes serait incompatible. | NOT_IDENTIFIABLE. Pouvoir de marché, contrats et régulation peuvent aussi empêcher la transmission ; différence prix–combustible n’est pas profit. |
| PRED-MICRO-04 ; CPC-0099 p.33, CPC-0015 p.19 | Baisse de prix d’un panier fixe à qualité inchangée, budget fixe ; économie disponible immédiatement, dépense ultérieure facultative. Dépense du même panier non réduite à prix réellement moindres serait incompatible arithmétiquement. | FORMALLY_CONSISTENT ; NON_DISCRIMINATING. Identité budgétaire commune ; aucune obligation de consommation supplémentaire ni mesure de Money. |
| PRED-MICRO-05 ; CPC-0095 p.203, CPC-0119 p.455 ; formule p.207 | dT=cp·ω·dω, coefficient constant sur l’intégration et Utility pertinente ; mesures indépendantes de T,ω,cp nécessaires. Une relation incompatible sous ces conditions mesurées discriminerait le sous-modèle. Horizon numérique UNRESOLVED. | NOT_IDENTIFIABLE. T et cp non observés ; progrès technique ou substitution capital/travail expliquent l’efficacité sans tester cette forme quadratique. |

## Transmission : branches observées ou simplement suggérées ?

Seuil de quasi-stabilité préspecifié : |variation annuelle de prix|≤1%. Parmi les baisses du **proxy**, le repérage A (prix diminuant de plus de1%) ne trouve que **2002, précisément une rupture de couverture** : ce n’est pas une preuve de transmission. B (prix quasi stable) trouve2016. E (prix croissant de plus de1%) trouve2006,2009,2011,2012,2015,2019,2020,2023. Ces étiquettes sont des repérages, pas une attribution aux mécanismes de Campergue. C (marge accrue) n’est pas identifié. D (qualité accrue simultanément) n’est pas établi. Aucun taux de transmission complète, partielle ou différée n’est identifié par ces seuls agrégats.

Le [descriptif EIA des prix électriques](https://www.eia.gov/energyexplained/electricity/prices-and-factors-affecting-prices.php) mentionne investissements, exploitation, réseaux, combustibles, demande, météo et réglementation. Relation aux claims de transmission : **QUALIFIES**, non CONTRADICTS ; il rappelle les composantes absentes de notre proxy. Les tables descriptives **DOES_NOT_TEST** les variables propres à Campergue. Il n’est pas nécessaire d’inventer une contradiction bibliographique.

## Qualité, consommateur, Money

[Fiabilité EIA, méthode IEEE](https://www.eia.gov/electricity/annual/html/epa_11_01.html) : durée moyenne annuelle d’interruption par client236,2→366,6 minutes entre2014 et2023 ; hors événements majeurs114,2→123,9. **EMPIRICALLY_QUALIFIED** : mesure physique partielle, population déclarant et météo variables, pas une estimation de tendance causale. Capacité, confort, qualité de tension, préférences et services aval ne sont pas couverts : **UTILITY_NOT_IDENTIFIABLE**.

Un panier illustratif fixe de1000kWh coûte85,80→160USD nominaux ; en dollars2023,147,647→160, soit **12,353USD de coût supplémentaire**, non un gain réel sur les deux bornes. Les baisses ponctuelles et économies année par année figurent dans panel.csv. Un budget fixe de100USD2023 achète677,29→625kWh (−7,72%). Ce ne sont ni revenus observés, ni facture typique garantie par un tarif, ni surplus compensatoire, ni gain de qualité ; le prix est une recette moyenne réalisée par kWh. Les variations de quantité consommée restent distinctes.

**Money : NOT_IDENTIFIED.** L’arithmétique d’un budget libéré peut illustrer CPC-0099, mais ni ce budget ni les kWh ne calibrent Money. La chaîne énergie→transformation→coût total→prix→Utility→gain→Money demeure non identifiable avec ces données. Aucun résultat de cette passe ne distingue empiriquement Campergue d’une explication concurrente.

## Bilan et reproduction

127 claims conservés, aucune correction textuelle justifiée ici ; couverture247/562 inchangée (relecture de passages déjà couverts, pas de pages nouvelles revendiquées). Le résultat négatif concerne le protocole et les observables, pas la vérité du système. Formules/unités : rapport32. Agrégation synthétique : rapport33.

`.venv-research/bin/python analysis/run_micro_electricity.py --check` reconstruit résultats, panel et qualité et compare les valeurs archivées. Le benchmark n’est pas remplacé silencieusement. Prochain protocole utile : producteurs/produits appariés avec coûts totaux, prix transactionnels, investissements et qualité ; définition indépendante d’Utility/T ; horizon et conditions qui interdisent réellement certaines observations.

## Vérification exécutée

Le8septembre2026, `./verify.sh` : code de sortie0 ; **56 tests exécutés,56 PASS,0 FAIL,0 erreur**, dont8 nouveaux contrôles micro. Les calculs électriques et synthétiques ont été recalculés et comparés aux snapshots. Les avertissements de couverture, bibliographie et identification restent actifs ; ils ne signifient pas validation scientifique. Rapport machine : `validation/phase2_regression_results.json`. Branche `research/corpus-validation` ; aucun push ni modification du manuscrit original.
