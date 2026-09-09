# EXP-03 — Conditions de stabilité de K

Statuts : FORMALLY_SUPPORTED pour les conditions démontrées; FORMALLY_QUALIFIED pour la stabilité par agrégation. Aucun K économique mesuré. Données synthétiques rationnelles et protocole figé.

## SOURCE

PDF559 reconnaît K variable par Product puis propose une stabilité avec davantage de Products. CPC-0117 conserve cette affirmation; CPC-0118 le couplage final proposé. La formule de moyenne ci-dessous est MINIMAL_RECONSTRUCTION sous additivité, non citation d’une règle explicitement établie par ce passage.

## Démonstration

Si Mi=KiTi pour chaque produit, si M et T sont additifs, sans double compte, et si les unités/frontières sont communes, alors

`Kbar = Σ qi Mi / Σ qi Ti = Σ wi Ki`, avec `wi=qiTi/Σ qjTj`.

Dans les diagnostics Ti>0, qi>0 : les poids sont positifs et de somme1. Si des T signés sont agrégés, la convexité n’est plus acquise; dénominateur nul interdit, proximité de zéro instable.

Pour Ki fixes, la condition nécessaire et suffisante de stabilité entre deux compositions est

`Σ (wi_new−wi_old) Ki = 0`.

Ainsi:

- mêmes proportions et coefficients fixes : stabilité;
- multiplication de toutes quantités par un même facteur : stabilité;
- Ki identiques : stabilité pour toute composition admissible;
- Ki différents : stabilité possible par compensation, pas garantie;
- mêmes proportions mais Ki variables : stabilité non garantie.

Pour invariance à **toutes** les compositions positives, avec Ti fixes positifs, l’égalité des Ki actifs est nécessaire et suffisante. Suffisance: moyenne d’une constante. Nécessité: si deux Ki diffèrent, concentrer progressivement les poids sur l’un ou l’autre donne des limites différentes. Une liste finie de simulations illustre cette preuve, ne la remplace pas.

Si Ki varient, la décomposition exacte est `ΔKbar=Σ wi_new ΔKi + Σ Δwi Ki_old`. Une variation des coefficients peut compenser une recomposition; aucune stabilité universelle n’est postulée.

## Calculs exécutés

Énumération de9 compositions à deux produits et27 à trois produits. Chaque cas compare coefficients différents, coefficients identiques et réplication par7. Un changement `[1,1,1]→[2,1,2]` avec les Ti/Ki du protocole conserve K tout en changeant les poids. Ce contre-exemple empêche d’ériger « composition fixe » en condition nécessaire.

## Normalisation

Sous Ti'=siTi et Ki'=Ki/si, chaque Mi est conservé, mais additionner les Ti' exprimés dans des unités propres aux produits change arbitrairement le dénominateur. Reconvertir à l’unité commune rétablit K. Un changement **commun** d’unité de T change numériquement K à l’inverse: covariance dimensionnelle, pas invariance du nombre brut.

Répéter un panier identique ne crée pas une nouvelle preuve de convergence statistique. Une augmentation du nombre de produits distincts ne suffit pas sans hypothèses de distribution, poids et stabilité des coefficients. Le protocole ne teste aucune distribution empirique de Ki.

Impact CPC-0117 : REQUIRES_NEW_CONDITION, sans effacer l’affirmation source. CPC-0118 : UNCHANGED sur sa portée empirique; ce test ne mesure pas le pont PIB/énergie. Référentiel de mesure réutilisé: MET-BIB-01/02, dimensions et modèle de mesure; la démonstration de moyenne est donnée ci-dessus, sans référence externe décorative.
