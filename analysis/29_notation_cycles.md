# T, dT, signes et cycles — réconciliation ciblée

Statut : **PARTIALLY_RESOLVED ; ambiguïté globale de notation conservée**. Ce tableau distingue une lecture analytique de la notation originale.

| Notation | Signification localisée | Unité ou dimension | Relation et réserve |
|---|---|---|---|
| T, p.207 | Primitive quadratique à constante choisie nulle | [cp]·[ω]², pas heures salariées | T=½cpω² ; niveau dépend du zéro choisi |
| dT, p.203/471 | Contribution différentielle de la transformation | Même dimension économique que T | dT=cpωdω à cp fixe ; dω=0⇒dT=0 n’exige pas T=0 |
| T, p.471 | Intégrale **entre deux instants** | [cp]·[ω]² | T=½cp(ω₂²−ω₁²), donc variation finie ici et non état unique |
| Ttotal, p.470–472 | Work créé + Work à faire | Échelle commune supposée | Conservation obtenue par identification des variations opposées |
| Tpos/Tneg, p.553–554 | Work fait / à faire, avec référents explicités | Grandeur économique ; signe lié au référent | P.554 retient Tneg et Mpos, contrairement à une lecture uniforme de toutes les formules antérieures |
| T, p.547 | Work exclusivement à faire | Pas volume d’heures déjà accomplies | Énoncé général à rapprocher des emplois intégrés précédents |
| T, p.464 | **Température physique** | Kelvin requis pour l’entropie | Aucun lien d’identité avec Economic Work ; désambiguïser en T_temperature dans l’analyse |

Il est possible de réserver analytiquement `K_T=½cpω²`, `ΔK_T` à l’intégrale et `T_remaining` au potentiel restant. **Ce sont des notations proposées par l’analyste**, pas une correction silencieuse du manuscrit. Aucun changement des claims antérieurs à ce sujet.

## Cas de signes et de rendement

- **RESOLVED dans la branche p.455–456** : Mcreated sort du système donc est négatif ; Qconsumed entrant est positif ; `Q=−M/Πη` est alors positif pour rendements positifs. M négatif ne signifie pas automatiquement destruction de richesse du consommateur.
- **PARTIALLY_RESOLVED**, p.551–552 : `η=−M/T`, `dη=(M·dT−T·dM)/T²` est bien la règle du quotient ; conserver ce qui est fixé et T≠0.
- **AMBIGUOUS**, p.553–557 : les référents fait/à faire changent explicitement. P.556–557 montre aussi dT=0 à divers niveaux T (maximum, intermédiaire, zéro), confirmant que dérivée nulle ne détermine pas l’état. Les flèches et fractions du cycle n’ont pas toutes reçu un audit visuel ; pas de résolution générale annoncée.
- **PARTIALLY_RESOLVED**, p.545–547 : Utility constante pendant tractation dans T→M, pendant fabrication dans M→T. L’auteur répond à l’apparente contradiction du gradient continu en distinguant coordonnées temporelles et champ labour/prix. Une différence de paramétrage n’est pas d’emblée une contradiction ; l’intégrabilité reste à étudier.
- **AMBIGUOUS**, optimum p.388–389 : le calcul 0,34314575 reste reproduit dans la passe précédente ; la contrainte autorisant son appellation de maximum n’est pas résolue par les pages terminales. Aucun statut EMPIRICALLY_SUPPORTED ajouté.
- **INCONSISTENT localement**, p.467 et 470 : Force constante non nulle pendant un intervalle non nul produit une variation de a/e selon l’équation précédente. Le texte peut viser une Force additionnelle nulle, mais ce n’est pas l’énoncé affiché. P.467 a été vérifiée visuellement, p.470 dans l’extraction complète.

Contrôle visuel supplémentaire p.554 : Ω est affiché avec e²/cp et a²/ca ; la substitution dans une norme de vitesses donnerait normalement cp²/ca². **AMBIGUOUS** tant que l’échelle ou le changement de signification n’est pas spécifié. Nous conservons la formule imprimée, pas une réparation implicite.

Registre machine-readable : [terminal_review_issues.json](data/terminal_review_issues.json). Les problèmes précédemment ouverts restent dans leurs registres historiques ; ceux-ci ne sont ni écrasés ni réputés résolus par cette passe.
