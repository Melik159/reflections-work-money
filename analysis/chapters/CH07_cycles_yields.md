# CH-07 — Cycles, création et rendements

Statut local : **UNCERTAIN**. Claims CPC-0037,0038,0099,0103,0104,0109; PM-06,10,11,16. Frontières conservées; sections345–350 et383–392 examinées, pas tout le chapitre.

## Question et relation à la racine

Comment un cycle peut-il transformer Work en supplément de Money, avec pertes, réciprocité et contraintes ? La réponse doit expliquer une création réelle plutôt qu’un simple paiement circulant.

## Définitions et meilleure reconstruction

Le cycle comprend contrat d’achat, fabrication, contrat de vente, usage (34,295–296). Le caractère isophèle/adiabatique dépend du support et de la transformation T→M ou M→T; ne pas transférer la description du Product au Cash. Pendant une branche adiabatique, absence de transfert externe n’implique pas absence de toute variation interne (346–349).

## Équations et conditions

M isophèle est une intégrale de FA.dp avec Utility constante (347). À prix constant, dM=0; l’auteur écarte explicitement la constante pour parler de Money créé nul (349). Le rendement ηTM=−M/T1 dépend du signe des flux et d’une conversion compatible. Le rendement global est un produit de deux rendements (388); les transformations sont couplées et non deux machines arbitrairement indépendantes.

## Hypothèses et conséquences

Premier principe, second principe, réversibilité, utilités de référence et conditions géométriques soutiennent les calculs. La valeur (2−√2)²=0.34314575 à angles égaux est arithmétiquement reproductible. Elle ne suffit pas à prouver un maximum universel de toute économie. Les coefficients variables sont explicitement envisagés523–532; ne pas figer g hors de la branche cohérente.

## Fragilités localisées

Page385, une borne inférieure η≥1−UP2/UP1 ne donne pas seule η=0 lorsque les utilités sont égales; une condition additionnelle est nécessaire. La signification du Work restant est donnée par l’auteur et doit être prise en compte avant de critiquer le sens de l’inégalité. Page389, l’expression carrée (1−tanα)² vaut1 à α=0, donc ne possède pas le maximum annoncé à π/8 sur tout [0,π/4]. Le tableau392 représente un couplage différent hors de l’égalité des angles : domaine admissible et passage entre expressions à réconcilier. Ce constat n’est pas une réfutation globale des cycles.

## Testabilité et bilan

Il faut observer un cycle, ses entrées/sorties, Utility et pertes, avec conversions fixées avant mesure. Les secteurs PIB/énergie du dépôt ne sont pas ces cycles. Les calculs conditionnels et non-implications sont testés dans `run_productive_checks.py`; aucun rendement économique universel n’est déclaré empiriquement validé.

Création avant usage, contraintes et pertes sont réellement présentes. Restent ouverts la mesure des rendements, l’interprétation des signes, l’optimum, le capital immobilisé et la transmission du financement à la création productive.
