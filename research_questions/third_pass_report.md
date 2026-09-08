# Troisième passe — opérationnalisation

## QUESTIONS REVIEWED

10/10 dossiers enrichis dans le périmètre métrologique. Lecture dirigée et réutilisation des analyses existantes; pas nouvelle lecture exhaustive des 562 pages ni collecte empirique lourde. Les dix fichiers `RQ-XX/metrology.md` contiennent reconstruction, conditions, limites et protocole proposé.

## VARIABLES MAPPED

26 entrées, avec alias explicités : ω/productivity et cp/complexity ne sont pas des mesures indépendantes. [Carte](operationalization/variables.md), [JSON](operationalization/variables.json), [matrice](operationalization/measurement_matrix.csv).

## MEASUREMENT LEVELS

| Niveau | Nombre |
|---|---:|
| L0 | 0 |
| L1 | 10 |
| L2 | 6 |
| L3 | 9 |
| L4 | 0 |
| L5 | 1 |

L3 signifie procédure définissable dans un périmètre précis, **pas données effectivement collectées**. L5 concerne l’énergie physique indépendante déjà archivée. Une série répétée d’un proxy ne fait pas monter la grandeur Campergue au niveau5. Zéro L0 n’affirme pas que toutes les définitions sont sans ambiguïté : les entrées ont un contenu conceptuel, avec ambiguïtés enregistrées.

## DIRECTLY MEASURABLE

Cash comme inventaire de supports, n comme solde nominal dans une frontière donnée, prix comme transaction appariée, énergie physique. Seule cette dernière bénéficie ici de mesures répétées déjà archivées. La présence d’un solde ou d’une facture ne mesure pas Money ou Utility. Productivité de tâche, travail mécanique utile et profit peuvent être calculés sous les conditions précisées; pas assimilés à observations nouvelles.

## PROXY ONLY

Utility, u, coût dans le jeu électrique actuellement disponible, gain consommateur, niveau de vie, dommage environnemental. Pour chaque proxy, cible, frontière, limites et hypothèses restent distinctes. Une marge comptable complète serait calculable, mais prix résidentiel moins coût gaz n’est pas cette marge.

## NOT OPERATIONALIZED

T, dT, cp, Forces, Money, complexité, richesse au sens retenu, ca et rendement économique η. K reste AMBIGUOUS selon son usage; un ratio PIB/énergie calculable ne résout pas son interprétation structurelle.

## CIRCULARITY RISKS

[Audit par protocole](operationalization/circularity_review.md) : T construit par sa loi quadratique; cp récupéré depuis le même T; Utility construite par la Core Law; Money construit par son identité; K recalculé pour chaque observation; dommage assimilé à énergie. Ces calculs peuvent être cohérents mais ne testent pas indépendamment les relations de construction.

Nuance conservée : GDP/(GDP/E) peut restituer une énergie physique indépendante si le ratio source incorpore cette énergie. Présence algébrique du PIB ≠ circularité prouvée. Traçabilité, millésimes et frontières décident.

## STATUS CHANGES

| Question | Avant | Après | Apport |
|---|---|---|---|
| RQ-03.03 | AMBIGUOUS | AMBIGUOUS | Voie de mesure indépendante de Force/cp non identifiée |
| RQ-05.03 | AMBIGUOUS | AMBIGUOUS | Absence de mesure reconnue explicitement PDF109 |
| RQ-08.02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Ratio résiduel distingué de coefficient structurel |
| RQ-09.02 | AMBIGUOUS | AMBIGUOUS | Pont physique explicite mais condition Utility non mesurée |
| RQ-10.02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Destinations possibles ≠ fractions marginales causales |
| RQ-11.01 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Pressions séparées des dommages finaux |
| RQ-12.02 | OPEN | OPEN | Signatures examinées; nécessité/suffisance historique non établie |
| RQ-04.04 | OPEN | PARTIALLY_RESOLVED | Valeur conditionnelle reproduite, optimum contraint non clos |
| RQ-01.03 | OPEN | PARTIALLY_RESOLVED | Panier et dimensions possibles identifiés, seuils non définis |
| RQ-05.01 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Protocole produit-usine-client spécifié |

Les conclusions générales et leurs niveaux de confiance historiques sont conservés; chaque dossier ajoute une confiance métrologique et ses limites. Aucune question RESOLVED_WITHIN_SCOPE ajoutée. Dépendances et IDs inchangés; corrections archivées dans `history/third_pass_before`, événements dans `history.json`.

## T / cp

PDF207 dérive T=½cpω² par substitution des Forces et intégration, à constante nulle. Cela n’est pas une mesure indépendante. ∫FP dl ne fournit une seconde voie que si FP n’est pas lui-même construit par cp·dω/dt. cp constant et origine de T doivent être déclarés; cp variable introduit un terme supplémentaire dans la différentielle de la primitive. Aucun étalon indépendant identifié dans les passages examinés.

## UTILITY

Le passage PDF109 dit exactement :

> If it's possible to measure need, the same cannot be said for Utility.

Le texte envisage une mesure future et un classement présent. Un ordre ne détermine pas un rapport cardinal : U1=4,U2=2 donne η=.5; la transformation croissante U² conserve l’ordre mais donne η=.75. Ce diagnostic formel n’invalide pas une éventuelle future échelle de rapport. Qualité, WTP et service rendu restent des comparateurs explicitement distincts. [Dossier](RQ-05.03/utility_operationalization.md).

## K

K local calibrable seulement avec M,T indépendants; K=GDP/E estimable comme ratio de proxies et résiduel si ajusté à chaque date; constance structurelle hypothétique. Diagnostic : deux produits donnent K=1.142857 puis .8 sous recomposition; trois donnent 1.674419 puis .862745. Répliquer toutes les quantités cent fois conserve K initial dans les deux cas. Hypothèses de calcul : additivité, unités communes, frontières identiques, pas somme de Utility. [Résultats reproductibles](operationalization/formal_results.json).

## ENERGY → WORK

PDF455 écrit Tused=−Wcreated, sous condition d’évolution de Utility. Ce pont est explicite : le réduire à une simple ressemblance omettrait une proposition du texte. Mais mesurer Q et W mécaniques n’étalonne pas automatiquement T. Rendement thermique, exergie et Work économique ne sont pas interchangeables. [Table de mesure](RQ-09.02/physical_economic_measurement_bridge.md).

## LIVING STANDARD

Panier réel, diversité, logement, mobilité, temps et distribution sont des candidats; pas de seuil source de subsistance/abondance retrouvé dans ce dossier. PIB/habitant, consommation réelle et HDI mesurent des objets différents. Le [UNDP](https://hdr.undp.org/data-center/human-development-index) fournit un comparateur multidimensionnel, pas la définition opérationnelle du manuscrit. La stabilité historique alléguée reste ouverte.

## ENVIRONMENTAL DAMAGE

Pressions multiples plutôt qu’indicateur unique calibré. Ressources, déchets, énergie et transport sont présents; fonctions dose-réponse et dommages quantifiés non établis dans les passages retenus. Absence locale ≠ absence dans l’ensemble du manuscrit. [Catégories](RQ-11.01/environmental_measurands.md).

## DISCRIMINATING SIGNATURES

La relation pertes/vitesse PDF165 est une candidate conditionnellement accessible dans un procédé homogène. T quadratique et optimum .3431 sont caractéristiques mais non testables indépendamment sans leurs grandeurs et conditions. K stable et coût→prix sont également compatibles avec des explications usuelles. Aucune signature HIGH_DISCRIMINATING_POWER actuellement établie. [Table](RQ-12.02/signatures.md).

## FORMAL RESULTS

Diagnostics exécutés : invariance sous réplication puis sensibilité à composition; ordre Utility sans invariance de rapport; valeur de rendement à π/8 et dérivée libre non nulle; zéro résiduel d’un T construit, explicitement interdit comme preuve indépendante.

La dérivée non nulle à π/8 n’est pas une réfutation de tout optimum **contraint**. Elle établit que la fonction seule ne sélectionne pas le point : domaine et contraintes restent nécessaires. Le +78% reste un résultat arithmétique conditionné par une hypothèse quadratique; aucune nouvelle preuve empirique apportée.

## EXPERIMENTS

8 propositions, [détails et niveaux des variables](operationalization/experiments.md).

- DO_NOW : EXP-02,03,04, diagnostics formels exécutés.
- DO_LATER : EXP-08, stabilité prédictive sur données déjà archivées, non exécutée cette passe.
- NEEDS_DATA : EXP-05,06,07, procédé physique, panel coût/prix, destination du gain.
- NEEDS_DEFINITION : EXP-01, indication indépendante de T/Force/cp; NOT_CURRENTLY_TESTABLE dans l’état actuel.

Pas de nouvelle régression ni collecte massive. Les analyses empiriques antérieures ont été vérifiées par le point d’entrée habituel, non présentées comme expériences nouvelles.

## CORPUS COVERAGE

Avant 271/562; après **272/562**. Dix-sept pages relues intégralement, dont une nouvelle page109. La note de lecture et le manifeste donnent la liste exacte. 127 claims conservés, 0 nouveau claim; ajout d’une preuve textuelle directe au dossier Utility, sans dupliquer artificiellement les claims.

## LITERATURE

4 nouvelles entrées officielles vérifiées : JCGM mesurande, JCGM modèle de mesure, BLS ajustement de qualité, UNDP HDI. Deux entrées appartiennent au même vocabulaire JCGM : pas quatre preuves indépendantes. Registre spécialisé MET-BIB; 19 références mobilisées dans la deuxième passe conservées séparément. Vérification limitée aux pages sélectionnées, pas aux ressources liées. [Registre](operationalization/literature.md).

## VERIFY

**PASS — 80/80 tests**, dont8 nouveaux; `./verify.sh` exécuté avec code de sortie0. Premier lancement des tests : 79/80, erreur de champ execution_status sur EXP-01 corrigée en DESIGNED_NOT_EXECUTED; second lancement complet : 80/80.

WARNING : couverture partielle, proxies, absence d’étalonnage indépendant, bibliographie ciblée et hypothèses non testées. Les tests historiques ont été ajustés pour comparer l’état courant au dernier événement de révision et considérer la couverture antérieure comme un snapshot, sans modifier les anciens événements. Ces warnings ne sont pas des validations théoriques.

## NEXT

1. EXP-01 : définir une indication indépendante de Force ou conclure explicitement au blocage de calibration.
2. RQ-05.03 : rechercher un protocole cardinal compatible avec l’Utility non additive et contextuelle.
3. RQ-04.04 : formaliser le domaine admissible des angles et les contraintes d’optimum.
4. EXP-05 : sélectionner un procédé pour la relation pertes/vitesse, en fixant le domaine avant mesures.
5. EXP-06 : obtenir des coûts complets et factures appariées pour un produit homogène.
6. EXP-07 : définir exposition, horizon et contrefactuel pour la destination marginale du gain.
7. RQ-11.01 : choisir un dommage précis distinct de son indicateur de pression.
8. RQ-01.03 : définir panier, distribution et seuils de comparaison sans les attribuer à Campergue.

Conclusion de cette passe : les données physiques et comptables permettent des tests de sous-mécanismes; elles ne mesurent pas encore indépendamment T, Utility et Money. Tester les lois propres au formalisme exige de combler ces ponts de mesure, sans utiliser les lois elles-mêmes comme preuve de leur validité.
