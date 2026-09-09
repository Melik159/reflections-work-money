# EXP-09 — Trois lectures locales de T/dT

Statuts : FORMALLY_SUPPORTED localement, FORMALLY_QUALIFIED et NOT_IDENTIFIABLE pour la mesure indépendante. EXP-01 reste bloqué: EXP-09 n’est pas son exécution sous un autre nom.

## SOURCE_FORMALISM

PDF207 écrit T=½cpω² après intégration avec constante nulle. PDF203 parle d’absence de Work additionnel à vitesse constante. PDF471 utilise T pour une différence entre instants; PDF472 conserve la somme cinétique + potentielle restante.

## MINIMAL_RECONSTRUCTION

| Modèle | Sens | Relations compatibles | Qualification / incompatibilité conditionnelle | Unités et conséquences |
|---|---|---|---|---|
| MODEL-A | État E=½cpω² | primitive PDF207, dE=cpωdω à cp fixe | T de PDF471 doit être lu ΔE; vitesse constante n’implique pas E=0 | [cp][labour]²/[temps]²; origine choisie |
| MODEL-B | Réserve potentielle R | PDF471–472: dR=−dE, R+E constant dans bilan isolé | R ne peut être simultanément la même primitive positive E si celle-ci varie; réserve ≠ cumul monotone de toute activité | même unité formelle; origine/réserve initiale à spécifier |
| MODEL-C | Transfert signé T[a,b]=E(b)−E(a) | intégrale PDF471 et lecture du Work additionnel PDF203 | primitive PDF207 exige référence initiale; T[a,b] n’est pas un stock attaché au seul instant b | même unité, télescopage sur intervalles compatibles |

Les lettres E,R et indices sont ajoutés par l’analyste, pas des corrections silencieuses du manuscrit. Aucun modèle n’est sélectionné comme lecture unique des passages.

## Calculs

La trajectoire du protocole donne E=[1,9,4,1], transferts=[8,−5,−3], réserve=[100,92,97,100]. Le transfert net sur le cycle est nul, le cumul des seuls transferts positifs vaut8. Ces deux quantités ne doivent pas être confondues. Cela ne prouve pas absence d’énergie dissipée dans un procédé réel: aucun coût de dissipation n’est spécifié par ce jouet.

À ω constante et cp variable, la variation de E peut être non nulle alors que cpωdω est nul. Le terme manquant est ½ω²dcp. Ce diagnostic qualifie une extension à cp variable; il n’affirme pas que les intégrations locales à cp fixe sont erronées.

Changement d’échelle de tâche l'=s l : ω'=sω, cp'=cp/s² conserve E. Maintenir cp numériquement inchangé changerait la grandeur calculée. Cela ne calibre ni cp ni T en joules.

## Conclusion

Une notation séparant état, réserve et transfert rend compatibles des relations locales. Identifier sans distinction ces trois objets produit des incompatibilités conditionnelles. Le test ne fournit pas de mesure indépendante de T, ni de justification causale à la relation quadratique. REQUIRES_INDEPENDENT_T reste explicite.

Méthode: [OpenStax, champs conservatifs](https://openstax.org/books/calculus-volume-3/pages/6-3-conservative-vector-fields), source déjà utilisée et reconsultée; le lien entre primitive et différence d’extrémités est mathématique, sans établir que toutes les grandeurs économiques du corpus possèdent un potentiel.
