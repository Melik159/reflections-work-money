# Calculs, +78 %, énergie et littérature ciblée

## Le +78 % : six niveaux à conserver

**A — Arithmétique.** Pour une même tâche, vitesse multipliée par8/6. Sous T proportionnel au carré de cette vitesse : T₂/T₁=(8/6)²=16/9; supplément7/9=77,777…%. Le coût horaire20$ donne160→120$, soit−25%; ce n’est pas une baisse du coût de78%.

**B — Hypothèse.** cP, tâche et méthode fixes, constante de référence nulle; distinguer niveau T₂/T₁ et différence T₂−T₁. À constante d’intégration non nulle, le ratio des niveaux n’est plus automatiquement16/9.

**C — Justification interne.** Le préambule32 invoque les lois de la physique. Les pages201–207 introduisent Force=cP.accélération, dT=Force.dlabour puis intègrent dT=cP.ω.dω. Ce n’est donc pas un nombre posé sans développement; la dérivation est conditionnelle aux identifications économiques.

**D — Origine physique.** La page458 compare à l’énergie cinétique mv²/2. Cette relation de niveau ne mesure pas à elle seule toute l’énergie consommée par un processus, ses frottements, sa durée et ses pertes. Il faut une correspondance indépendante entre variables avant de transférer son exponent2 à une production économique.

**E — Transposition.** Economic Work, complexité et vitesse de tâche ne sont pas automatiquement joules, masse et vitesse de déplacement. L’analogie motive une loi proposée, pas une preuve empirique. Le texte distingue lui-même W et T (203,455).

**F — Test.** Observer des tâches identiques et des vitesses différentes, mesurer indépendamment Work utile, complexité et rendements. Les trois séries macro du dépôt ne suffisent pas.

Statuts simultanés : **ARITHMETICALLY_REPRODUCED**, **FORMALLY_DERIVED** sous les hypothèses, **ASSUMPTION_DEPENDENT**, **NOT_EMPIRICALLY_TESTED**. Ni EMPIRICALLY_SUPPORTED ni CONTRADICTED attribué globalement au +78%.

## Autres contrôles exécutés

`analysis/run_productive_checks.py` exécute cinq contrôles formels : +78%; substitution couplée des variables de24-03; valeur34,3146%; non-implication à partir de la borne de rendement; coûts relatifs stylisés de461. Les sorties sont dans `analysis/empirical/productive/results.json`.

Deux résultats à examiner, sans les transformer en verdict global :

- À cP fixe, e=cPω change avec la vitesse. Substituer cette relation dans p=e.Ch.l/(2T) donne p=Ch.l/ω, donc p proportionnel à1/√T sous les autres constantes. Garder simultanément e et cP fixes pendant une accélération serait incohérent avec ces propres équations.
- La valeur34,3146% à π/8 est bien reproduite. La fonction carrée de389 n’a pas là son maximum sur tout[0,π/4]. Le domaine contraint et le tableau392 doivent être réconciliés avant d’annoncer un rendement universel.

## Trois protocoles empiriques réalistes

1. **Vitesse–Work :** séries par processus, tâche/qualité constantes, mesure indépendante de l’énergie utile; distinguer exponent2, coûts fixes et efficacité variable.
2. **Transmission coût–prix :** données produit/entreprise avant-après, coûts, prix de transaction et profits en montant; distinguer branche à profit fixe et marges variables.
3. **Couplage énergétique :** Q et Money mesurés séparément, rendements observés; comparer à tendances communes et explications concurrentes.

Les trois sont **NOT_IDENTIFIABLE_WITH_CURRENT_DATA**. Un diagnostic est réellement exécuté pour le troisième : reconstruction energy=GDP_PPP/gdp_per_energy et régressions mondiales niveaux/différences. Il ne constitue pas un test de causalité, ni une correspondance validée entre PIB et Money. Les valeurs exactes, variables manquantes et critères de réfutation/non-conclusion sont enregistrés dans le JSON.

## Littérature : confrontation limitée et vérifiée

**BIB-0009 — Foster, Haltiwanger, Syverson (2005).** Les auteurs distinguent productivité physique et productivité mesurée en revenus; leurs corrélations aux prix diffèrent. **SUPPORTS**, au sens limité de résultat compatible avec CPC-0096/PM-03; **QUALIFIES** CPC-0098/PM-05 pour l’identification des effets; **DOES_NOT_TEST** CPC-0035 pour le carré de la vitesse. Notice et résumé primaires lus, pas reproduction de leurs microdonnées. [Census Bureau](https://www.census.gov/library/working-papers/2005/adrm/ces-wp-05-11.html), [working paper et DOI](https://www.nber.org/papers/w11555).

**BIB-0010 — Schwellnus, Kappeler, Pionnier (2017).** Le découplage entre productivité et rémunération médiane est décomposé en part du travail et dispersion salariale. **QUALIFIES** CPC-0016 : le gain productif ne garantit pas à lui seul la même hausse pour le travailleur médian. **DOES_NOT_TEST** CPC-0064 : leur productivité n’est pas une mesure indépendante d’Economic Work. Ce n’est pas une réfutation du gain de pouvoir d’achat du consommateur dans une branche à revenu constant. Métadonnées et résumé officiel lus. [OCDE](https://www.oecd.org/en/publications/decoupling-of-wages-from-productivity_d4764493-en.html).

Le manuel de productivité BIB-0002, déjà recensé, reste nécessaire pour la traduction des mesures. La piste *Rising Markups or Changing Technology?*, NBER30491, n’est pas utilisée comme preuve : accès direct refusé403, métadonnées/extraits indexés seulement. Aucune bibliographie complète du rebond n’est revendiquée dans cette passe. Le rebond est une question future distincte de la seule corrélation PIB–énergie.
