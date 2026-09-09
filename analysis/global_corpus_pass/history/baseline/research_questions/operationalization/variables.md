# Carte des variables — troisième passe

Statuts métrologiques provisoires, pas verdicts théoriques. Les définitions ci-dessous sont INTERPRETATION reliée aux pages; citations dans les dossiers. Une procédure L3 n’est pas une collecte réalisée. L5 énergie décrit les séries physiques archivées, pas leur équivalence à T. Alias ω/productivity et cp/complexity ne sont pas observations indépendantes.

- LEVEL 0 — NOT DEFINED WELL ENOUGH
- LEVEL 1 — CONCEPTUALLY DEFINED
- LEVEL 2 — PROXY AVAILABLE
- LEVEL 3 — OPERATIONAL DEFINITION
- LEVEL 4 — INDEPENDENT MEASUREMENT AVAILABLE
- LEVEL 5 — REPEATED/REPLICABLE MEASUREMENT AVAILABLE

| ID | Variable | Statut | Niveau | Pages | Proxy ou procédure | Condition |
|---|---|---|---|---|---|---|
| VAR-01 | T | NOT_OPERATIONALIZED | 1 | [203, 207, 471] | PROXY: variation de vitesse; ne mesure pas T | cp constant et unité de tâche; calibration indépendante de Force et cp absente |
| VAR-02 | dT | NOT_OPERATIONALIZED | 1 | [203, 207, 471] | PROXY: changement de débit de tâche | dT=0 ne signifie pas T=0; terme 0.5 ω² dcp si cp varie dans la primitive |
| VAR-03 | cp | NOT_OPERATIONALIZED | 1 | [189, 201, 202] | PROXY: dureté ou complexité technique, non équivalente | Ni cp ni Force étalonnés indépendamment; cP distinct de cA |
| VAR-04 | ω | IDENTIFIABLE_WITH_ASSUMPTIONS | 3 | [197, 198] | Chronométrage de tâches homogènes; aucun nouveau jeu de mesures | Frontière de tâche, échelle, qualité et version du procédé fixes; pas PIB/heure automatiquement |
| VAR-05 | Force / Forces | NOT_OPERATIONALIZED | 1 | [201, 202, 283] | PROXY: effort technique ou pouvoir de négociation | Une Force économique ne se mesure pas en newtons par renommage |
| VAR-06 | Utility | PROXY_ONLY | 2 | [108, 109, 189, 190] | PROXY: classement, caractéristiques, service rendu ou WTP | p109 reconnaît absence de mesure; ordinal ne donne pas rapports cardinaux; qualité technique insuffisante |
| VAR-07 | Money | NOT_OPERATIONALIZED | 1 | [185, 192, 204, 207] | PROXY: gain budgétaire à panier fixe | Ne pas assimiler à dépôts ni USD; les scénarios monétaires ont des conditions distinctes |
| VAR-08 | Cash | DIRECTLY_OBSERVABLE | 3 | [189, 192] | Inventaire de supports et comptes dans un périmètre défini | Éviter double compte support/solde; cartes et billets ne forment pas un agrégat homogène |
| VAR-09 | n | DIRECTLY_OBSERVABLE | 3 | [204, 537] | Comptage de soldes nominalement libellés | Fixer monnaie, agents, instruments, consolidation et date; aucune nouvelle mesure collectée |
| VAR-10 | u | PROXY_ONLY | 2 | [204] | PROXY: inverse d’un indice de prix de panier | Choix du panier et distribution; ne constitue pas mesure de u universel |
| VAR-11 | K | AMBIGUOUS | 1 | [559] | PROXY: PIB/énergie observés, K_RESIDUAL | Ratio estimable des proxies ≠ K_STRUCTURAL; composition, unités, pertes variables |
| VAR-12 | cost | PROXY_ONLY | 2 | [273, 501] | PROXY: combustible f×h dans le cas électrique existant | Coût complet exige capital, travail, réseau, taxes; produit de moyennes ≠ moyenne des produits |
| VAR-13 | price | DIRECTLY_OBSERVABLE | 3 | [197, 198, 204] | Facture d’un même produit; collecte proposée | Prix moyen EIA est PROXY du prix d’exemplaire, pas mesure individuelle |
| VAR-14 | profit | DERIVABLE_FROM_OBSERVABLES | 3 | [43, 488, 490] | Comptes réconciliés, non disponibles dans le panel électrique | Écart prix résidentiel−coût gaz n’est pas profit; distinguer rente et profit économique |
| VAR-15 | productivity | IDENTIFIABLE_WITH_ASSUMPTIONS | 3 | [197, 198, 203] | PROXY macro: output/heure; direct seulement tâche homogène | Composition, sous-traitance, qualité et travail des machines; alias de ω non variable indépendante |
| VAR-16 | energy | DIRECTLY_OBSERVABLE | 5 | [455, 456, 459] | Séries indépendantes déjà archivées; protocole primaire/finale séparé | Niveau5 pour quantité physique uniquement; primary/final/electricity/exergy non interchangeables |
| VAR-17 | useful work | IDENTIFIABLE_WITH_ASSUMPTIONS | 3 | [455] | Couple×angle ou force×distance; protocole non collecté | Frontière physique et rendement mesuré; chaleur utile et exergie ne sont pas W mécanique automatiquement |
| VAR-18 | complexity | NOT_OPERATIONALIZED | 1 | [189, 202] | PROXY: caractéristiques techniques ou résistance à usinage | Même mot plusieurs usages; ne remplace pas cp par un score arbitraire |
| VAR-19 | labour | IDENTIFIABLE_WITH_ASSUMPTIONS | 3 | [197, 203] | Inventaire d’opérations et chronométrage | Pas heures de salarié par défaut; pondération de tâches hétérogènes à justifier |
| VAR-20 | consumer gain | PROXY_ONLY | 2 | [204, 400] | PROXY: économie sur panier fixe | Ni surplus compensateur, ni revenu observé, ni Money; qualité et consommation différentes |
| VAR-21 | wealth | NOT_OPERATIONALIZED | 1 | [185, 204] | PROXY: ressources ou consommation réelles | Patrimoine net standard ne remplace pas richesse monétaire Campergue |
| VAR-22 | standard of living | PROXY_ONLY | 2 | [29, 34, 43, 180] | PROXY: consommation réelle, temps, logement, mobilité, PIB/hab | Pas seuil source établi subsistance/abondance; moyenne ignore distribution |
| VAR-23 | environmental damage | PROXY_ONLY | 2 | [68, 69, 112, 113, 460] | PROXY: émissions, déchets, extraction; impacts distincts | Énergie ou matière ne sont pas dommages; exposition, toxicité et horizon nécessaires |
| VAR-24 | ca | NOT_OPERATIONALIZED | 1 | [202, 207] | Aucun proxy calibré | cp≠ca explicitement; normalisation commune non acquise |
| VAR-25 | ϖ | IDENTIFIABLE_WITH_ASSUMPTIONS | 3 | [198, 207] | Historique des étapes de fabrication valorisées | Prix annuel d’autres exemplaires n’est pas cette trajectoire |
| VAR-26 | η | NOT_OPERATIONALIZED | 1 | [385, 386, 387, 388, 389, 390] | PROXY physique interdit comme substitution directe | Rapports Utility et signes requis; optimum conditionné par géométrie |
