# 28 — Agrégation, potentiels et coefficients

Statut CH-08 : **UNCERTAIN / première reconstruction substantielle, qualifiée**. Sources : pages PDF 402–410 sélectionnées, 413–446 sélectionnées, 452–453 et 536–559 ; couverture exacte dans les notes. Claims ajoutés : CPC-0114 à 0117 et CPC-0126. Les autres claims sont conservés.

## Ce qui est effectivement agrégé

1. **Contributeurs au même processus**, p.210 : addition de T, emploi e et contributions productives (CPC-0111). Une telle somme exige unités, référent et frontières communes. Une contribution humaine qui commande une machine ne doit pas être comptée à nouveau comme toute l’énergie de la machine. Ce risque est une objection analytique, pas un double compte numériquement démontré.
2. **Copies d’un Product**, p.402–403 : offre et demande définies en débits, avec possibilité de vitesses moyennes. Débit total, moyenne par fournisseur et moyenne temporelle ne sont pas interchangeables. Les sommes de quantités sont intelligibles pour des produits homogènes ; aucun panier hétérogène univoque n’est construit dans ces passages.
3. **Product/Cash**, p.406 : `DP=SA/p`, `DA=SP·p`, puis `SA·SP=DA·DP`. Identités conditionnelles de valeur à prix commun, non loi de formation du prix. P.407–408 ajoute `DP=SA·l`, `DA=SP/l`, donc `p·l=1`. Ce second couple n’est pas une conséquence du premier sans définition réciproque ou normalisation de l. Le « 1 » ne peut être traité comme invariant d’unités quelconques.
4. **Monnaie locale/globale**, p.536–538 : `n` local, `N` global, puis `(∂M)n,N=(n/N)∂u`. Cette pondération n’est pas la même grandeur que `n∂u` sans normalisation de M par N. Le manuscrit avertit : “it cannot apprehend this creation of wealth directly in its entirety.” (p.538). Il ne faut donc pas lui attribuer une agrégation générale déjà achevée.

## Potentiels : structure propre, pas simple métaphore, mais conditions supplémentaires

P.413–414, Campergue définit explicitement des fonctions d’état économiques et restreint leurs relations à l’absence de pertes. P.420 présente les potentiels, par exemple `ETM^L=ETM+UP·P` et `X=ETM−FA·V`. P.415 donne `dETM^L=P·dUP+FA·dp`. Ces combinaisons et règles du produit sont formellement contrôlables ; cela ne prouve ni mesure indépendante d’Utility, ni existence d’un potentiel économique expérimental.

Les égalités croisées dites de Maxwell p.422 nécessitent un potentiel suffisamment différentiable et des différentielles exactes. Les potentiels ne deviennent pas tels simplement parce qu’on nomme deux extrémités « états ». Les extremums spontanés p.424 gardent leurs contraintes : B/A, B/UA, FP/A ou FP/UA constants. Retirer ces indices transforme une conclusion conditionnelle en loi universelle indue.

P.431–433, coefficients définis par dérivées partielles : `αTM=−(1/V)(∂V/∂UP)FA`, `βTM=−(1/FA)(∂FA/∂UP)V`, `χTM=(1/V)(∂V/∂FA)UP`. La règle cyclique donne `FA=−αTM/(βTM·χTM)` si les inverses existent. Les unités de α, β sont l’inverse d’Utility ; χ l’inverse de Force. Une limite nulle/singulière interdit les divisions employées.

P.441 appelle trois variables « independent », mais choisit ensuite deux d’entre elles avec rP constant et `FA·V=rP·UP`. Lecture charitable : trois coordonnées, deux degrés de liberté. Les p.442/446 reparamètrent `dT`, et p.452–453 `dM`. Ce sont des calculs locaux sur une loi constitutive supposée, pas des coefficients macroéconomiques estimés.

## Le champ n’est pas la somme

P.538–550, l’auteur propose un champ labour-prix, d’abord scalaire `Ω=varpi/ω=−dp/dl`, puis vectoriel `Ω²=ω²+varpi²`. Il précise que l et p doivent appartenir au même Product. P.558, un ensemble de vecteurs représente des entreprises ; les trajectoires réelles ne sont pas nécessairement circulaires et Work/Money peuvent varier largement.

L’addition de carrés de vitesses dans deux unités différentes exige une métrique ou des échelles. Changer dollars en centimes change un angle si l’autre axe ne change pas ; le seuil π/4 n’est donc pas encore un classement invariant. P.554, vérifiée visuellement, les dénominateurs ca/cp affichés après substitution de a/e diffèrent de ceux attendus au carré à partir de a=−ca·varpi et e=cp·ω. Une normalisation implicite reste possible : **AMBIGUOUS**, non erreur globale proclamée.

## La véritable hypothèse macroéconomique finale

P.559 : “the more Products are taken into account, the more the coefficient K can be considered constant”. Le passage de coefficients hétérogènes à K constant n’est pas démontré par le seul grand nombre. Des poids ou une composition changeants peuvent faire varier la moyenne même avec des millions de produits. Ensuite l’auteur identifie PIB, Money dépensé précédemment créé et énergie consommée. Ces trois ponts doivent rester distincts dans le graphe :

`contributions locales → [pondérations/composition] → K agrégé → [PIB/Money] → [énergie utile/totale] → GDP=K·Wconsumed`

E3 explore la stabilité d’un **proxy externe**, pas tous ces ponts. Le parallèle bibliographique avec les problèmes d’agrégation est méthodologique : voir BIB-0015, sans prétendre qu’un théorème externe réfute directement des grandeurs différentes.

## Conditions à conserver et prochaines questions

Le fichier [aggregation_mechanisms.json](data/aggregation_mechanisms.json) explicite six mécanismes avec conditions. Priorités : définir une normalisation n/N ; construire un exemple à deux producteurs avec hétérogénéité de K ; tester l’indépendance de la mesure d’Utility ; définir la métrique du champ. Sans cela, la contribution à la question racine reste une articulation proposée entre richesse locale et niveau de vie collectif, pas un résultat macroéconomique établi.
