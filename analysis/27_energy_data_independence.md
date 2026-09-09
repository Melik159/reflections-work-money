# 27 — Indépendance des données énergétiques

Statut : **QUALIFIED — ancienne reproduction conservée, nouvelle confrontation exécutée**. Passe du 8 septembre 2026. Baseline exécutée : 40/40 tests PASS, 113 claims, 175 pages examinées. Aucun PDF original ni résultat original modifié.

## Ancienne série : construction exacte et portée

Dans `articles/campergue_energy_gdp_code/src/energy_gdp_analysis.py`, lignes 151–174, le programme fusionne deux séries WDI puis calcule :

`energy = gdp_ppp_real / gdp_per_energy`

Le numérateur est `NY.GDP.MKTP.PP.KD`, PIB réel en dollars internationaux constants PPA ; le dénominateur `EG.GDP.PUSE.KO.PP.KD`, PIB-PPA par kg équivalent pétrole. Le résultat est donc une quantité totale en kg équivalent pétrole. Le PIB expliqué par la régression historique est `NY.GDP.MKTP.KD`, dollars US constants 2015, **pas exactement le numérateur PPA**. Le code prévoit également `--energy-file`, préférable, et un autre fallback PIB de marché/ratio PPA, explicitement déconseillé. Ce dernier n’est pas celui des sorties reproduites.

Les trois CSV historiques sont toujours reproduits par `run_empirical_iteration1.py`. Le diagnostic `run_productive_checks.py` retrouve la reconstruction à environ 2,22×10⁻¹⁶ d’erreur relative. Cela vérifie le calcul, pas une causalité.

### Correction méthodologique importante

La métadonnée WDI indique que le ratio utilise des bilans d’énergie primaire IEA et le PIB de la Banque mondiale. Ce n’est donc pas nécessairement une énergie inventée à partir du seul PIB. Si `I=Y_PPA/E_physique` et si millésimes, unités et périmètres concordent, `Y_PPA/I=E_physique` : le PIB s’annule. Avec des millésimes différents, on obtient plutôt `E_physique×Y_PPA_nouveau/Y_PPA_ancien`. La cohérence exacte de ces millésimes historiques n’est pas établie ici. [Métadonnée officielle WDI](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/EG.GDP.PUSE.KO.PP.KD).

Ainsi, **« dérivée du PIB ⇒ corrélation nécessairement tautologique » serait trop fort**. Le statut fidèle est `RECONSTRUCTED_FROM_GDP_RATIO / UNDERLYING_PHYSICAL_INPUT_DOCUMENTED / HISTORICAL_VINTAGE_CONSISTENCY_UNVERIFIED`. Ne pas étiqueter cette colonne comme une mesure directement acquise indépendamment du PIB. Elle peut néanmoins contenir une information énergétique réelle. La corrélation ne prouve ni causalité, ni spécificité Campergue, même après une reconstruction parfaitement correcte.

## Nouvelle série indépendante de la construction du PIB

Source : OWID Energy, compilation Energy Institute/EIA, figée au commit `4249f7c21c2c833d76741e757be92a639517caa3` (dernier commit disponible avant fin 2025). Colonne utilisée exclusivement : `primary_energy_consumption`, **TWh d’énergie primaire**. Population : colonne `population`, personnes. L’acquisition conserve le CSV complet, le codebook, le README, leurs SHA-256 et URLs immuables. [Dépôt au commit utilisé](https://github.com/owid/energy-data/tree/4249f7c21c2c833d76741e757be92a639517caa3).

Le traitement amont archivé au commit ETL `3bad71c46a5810338b081bb95ebb0fe78501a9a0` sélectionne `primary_energy_consumption_equivalent_twh` d’EI ou `energy_consumption` d’EIA, puis privilégie EI sur les observations communes. Il ajoute ensuite la population et le PIB pour **d’autres colonnes**. La colonne d’énergie totale n’est pas divisée ou multipliée par le PIB. Nous avons inspecté ce code, sans prétendre avoir reconstruit tout l’ETL amont.

Le README de ce millésime précise la convention de **substitution** pour les renouvelables et la conversion EJ→TWh. Ce n’est ni énergie finale, ni électricité seule, ni exergie. Le changement méthodologique OWID de 2026 n’est pas introduit dans cette passe. Les bilans WDI/IEA peuvent inclure une couverture différente des combustibles renouvelables et déchets : les écarts entre séries ne mesurent donc pas seulement une erreur statistique.

L’indépendance signifie ici **absence de PIB dans la construction de la variable énergétique utilisée**, jamais exogénéité statistique. Énergie et production restent conjointement déterminées.

## Périmètre et transformations

Panneau choisi avant estimation : monde, France, Allemagne, États-Unis, Chine, Inde, 1990–2023. 204 observations, 34 par zone ; aucune observation manquante après jointure, aucune interpolation, aucun lissage. Le monde vient de la ligne World, pas de la somme des cinq pays. Allemagne : début en 1990, sensibilité possible à la réunification et à la restructuration industrielle. La couverture de l’archive dépasse ce panneau ; seule cette fenêtre commune est analysée.

Inventaire effectif de la colonne énergétique archivée : 13 255 valeurs non manquantes, 277 entités (pays **et agrégats**, non 277 pays), 1965–2024. Pour chacune des six zones retenues, les bornes énergétiques sont1965–2024 ; celles de la population sont1900–2024. Ces bornes n’impliquent pas que chaque entité de l’archive possède une série complète. La jointure étudiée, elle, est sans lacune.

Énergie : TWh ; niveau PIB : milliards de dollars US constants 2015. Log-log : logarithmes naturels. Variations : différences annuelles de logarithmes, années consécutives vérifiées. Par habitant : énergie×10⁹/population en kWh/personne ; PIB-PPA réel/population pour le proxy de niveau de vie. La base de population commune peut induire de l’association. Aucune régression transversale regroupant arbitrairement les six zones n’est effectuée.

Ruptures possibles : révisions des bilans, couverture des sources, substitution énergétique, mix de combustibles, composition sectorielle, commerce incorporé, changements de population. Pas de correction de rupture imposée aux données ; le partage 1990–2006/2007–2023 sert uniquement au test descriptif E3. Les frontières sont celles des séries nationales, pas une empreinte de consommation mondiale réattribuée aux consommateurs.

## Trois expériences, pas trois preuves de causalité

| Expérience | Estimation | Ce qu’elle peut établir | Ce qu’elle ne peut établir |
|---|---|---|---|
| TEST-E1 | PIB sur énergie : niveau, log-log, Δlog | Association de niveau et co-mouvement temporel | Sens causal, mécanisme Work/Money, rôle indépendant des institutions |
| TEST-E2 | PIB-PPA/personne sur énergie/personne en logs | Association intra-pays de deux indicateurs par habitant | Bien-être complet, effet du revenu sur énergie ou inversement |
| TEST-E3 | Pentes log-log avant/après 2007 et interaction | Instabilité descriptive inter-pays/inter-périodes | Rupture causée par 2007, test de toutes les versions du formalisme |

OLS avec constante ; incertitude Newey–West/HAC, retard 3, noyau Bartlett, correction N/(N−p), IC asymptotiques normaux à 95 %. Les erreurs standards robustes **ne guérissent pas les tendances communes**, les erreurs de mesure, ni une non-stationnarité. Pas de test de cointégration, pas d’instrument, pas de prévision hors échantillon. « Granger », « prédictif » ou « causal » ne sont pas attribués à ces résultats.

Les coefficients, IC, N et R² complets sont dans [résultats numériques](empirical/independent_energy/results.json) et [table lisible](27_energy_results.md). Scripts : `acquire_independent_energy.py`, puis `run_independent_energy.py`; `--check` compare les résultats figés et échoue en cas de divergence au lieu de les écraser.

### Comparaison conservant les résultats antérieurs

| Zone, log-log1990–2023 | β ancien / R² ancien | β indépendant / R² indépendant |
|---|---|---|
| Monde | 1,605 / 0,991 | 1,535 / 0,992 |
| France | 0,259 / 0,012 | −0,662 / 0,115 |
| Allemagne | −1,270 / 0,611 | −1,728 / 0,543 |

La tendance allemande négative était donc **déjà présente** dans la reproduction historique. Le résultat français, faible et sensible au jeu de données, ne doit pas devenir une conclusion de signe universelle. La convergence mondiale entre deux constructions est un contrôle de robustesse descriptif, non une validation causale. Les différences de bilans et de conventions ne permettent pas d’attribuer tout écart au quotient par le PIB.

## Spécificité et reclassement

L’association mondiale positive est `COMPATIBLE_WITH_CAMPERGUE` au sens limité du rôle énergétique, mais aussi `ALSO_COMPATIBLE_WITH_STANDARD_EXPLANATIONS`. Elle n’identifie pas les coefficients économiques, la grandeur Money, ni l’équivalence physique proposée.

La version macroéconomique forte p.559 — `GDP=K·Wconsumed` avec K réduit aux unités — est plus restrictive. À frontières et définitions fixées, elle demanderait un ratio stable et une élasticité unitaire, pas seulement un grand R². Les tendances France/Allemagne et l’évolution des ratios vont contre cette **opérationnalisation à K constant**. Une variante à rendements, composition ou K variables peut rester compatible, mais perd alors cette prédiction discriminante. Aucun rejet du système complet n’en découle.

Littérature ciblée et traduction des concepts : [revue des sources](27_targeted_literature.md). Le PIB est un proxy externe que Campergue critique lui-même p.537/540 avant de le réutiliser p.559 ; ne pas l’identifier silencieusement à Money.
