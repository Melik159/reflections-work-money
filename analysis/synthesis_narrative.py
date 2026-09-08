"""Editorial synthesis, with explicit evidence anchors. Not new experiments."""

# ID | result | evidence artifact | RQs | pages | A | B | C
RESULTS = '''
SYN-01|Cash, Money, création, transfert et redistribution doivent rester distingués. M=n·u est une identité; la neutralité dépend du scénario, de l'acteur et de l'horizon.|analysis/data/money_compensation_scenarios.json|RQ-06.02,RQ-06.04|19,20,349,400|COHERENT_WITH_CONDITIONS|PARTIAL_PARALLEL|NO_DISTINCT_OBSERVABLE_ESTABLISHED
SYN-02|Economic Work n'est pas labour. À cp fixe, dT=cp·ω·dω admet T=½cp·ω²+C; dT nul à vitesse constante n'impose ni T nul ni dépense physique nulle.|research_questions/experiments/EXP-09/results.json|RQ-03.01,RQ-03.02,RQ-03.03|187,203,207,471,472|LOCALLY_CONSISTENT|ECONOMIC_MEASUREMENT_NOT_IDENTIFIED|CONDITIONAL_FORMAL_RESTRICTION
SYN-03|La primitive quadratique ne fournit pas une mesure indépendante de T. Si cp varie, sa différentielle contient aussi ½ω²dcp. Réserve, état et transfert ne sont pas interchangeables.|research_questions/operationalization/circularity_review.md|RQ-03.02,RQ-03.03|207,341,471,472|ASSUMPTION_DEPENDENT|NOT_IDENTIFIED|BLOCKED_BY_MEASUREMENT
SYN-04|Un ordre de Utility conserve des comparaisons, pas les rapports numériques utilisés dans certains rendements. Des différences pondérées peuvent covarier avec les coefficients; toutes les formules n'exigent donc pas la même échelle.|research_questions/experiments/EXP-02/results.json|RQ-05.03|108,109,283,349,386,415|FORMALLY_QUALIFIED|MEASUREMENT_REQUIREMENT|REVIEW_DIAGNOSTIC_NOT_AUTHOR_NOVELTY
SYN-05|Une baisse de coût peut être transmise, retenue, partagée ou différée. Les pages tardives de partage empêchent d'attribuer au corpus une transmission automatique intégrale.|analysis/global_corpus_pass/findings.json|RQ-05.01,RQ-06.04,RQ-10.01|20,21,363,364,468,504,507,508,523|CONDITIONAL_BRANCHES|PARTIAL_PARALLEL|NON_DISCRIMINATING
SYN-06|Le +78% reproduit (8/6)²−1 à tâche et cp fixés. Le calcul ne mesure ni une loi générale de productivité ni un rendement énergétique empirique.|analysis/25_productive_review_report.md|RQ-04.02,RQ-04.04|32,196,197,198,207|FORMALLY_DERIVED_WITH_ASSUMPTIONS|NOT_EMPIRICALLY_TESTED|REQUIRES_INDEPENDENT_T
SYN-07|Sous additivité, unités communes et coefficients locaux fixes, K est une moyenne pondérée. Composition fixe est suffisante, pas nécessaire; invariance à toute composition exige des coefficients identiques sur les composantes actives.|research_questions/experiments/EXP-03/results.json|RQ-08.01,RQ-08.02,RQ-08.04|538,559|FORMALLY_SUPPORTED_WITHIN_RECONSTRUCTION|NOT_STRUCTURAL_K_ESTIMATE|GENERAL_AGGREGATION_PROBLEM
SYN-08|Des erreurs ou sauts locaux restent documentés: égalité interpersonnelle issue de 0/0, force constante assimilée à force nette nulle, primitives, signes et passage d'inégalités de niveaux aux dérivées. Leur portée doit rester locale.|analysis/global_corpus_pass/formal_checks.json|RQ-05.03,RQ-08.03,RQ-03.02|249,250,251,252,467,470,525,526,528|LOCALLY_PROBLEMATIC|DOES_NOT_TEST_EMPIRICAL_SYSTEM|NOT_A_GLOBAL_REJECTION
SYN-09|Une corrélation avec une énergie reconstituée depuis un ratio incorporant le PIB demande un audit de filiation. La présence du PIB dans le ratio ne prouve pas seule une circularité si une mesure énergétique indépendante est restituée.|analysis/27_energy_data_independence.md|RQ-09.03|558,559|PROVENANCE_QUALIFICATION|INDEPENDENCE_REQUIRES_SOURCE_AUDIT|METHODOLOGICAL_NOT_SPECIFIC
SYN-10|La série primaire indépendante montre une association monde PIB–énergie et des régimes différents en France/Allemagne. Une association ou un co-mouvement ne démontre ni causalité ni conversion énergie→Money.|analysis/27_energy_results.md|RQ-09.03,RQ-12.01|455,456,558,559|PROXIES_NOT_SOURCE_VARIABLES|EMPIRICALLY_SUPPORTED_WITHIN_DESCRIPTIVE_SCOPE|NON_DISCRIMINATING
SYN-11|GDP=K·W avec K strictement constant et W identifié à l'énergie primaire ne décrit pas les ratios observés. Cela qualifie cette identification forte, pas toutes les versions du coefficient économique.|analysis/27_energy_results.md|RQ-08.02,RQ-09.03,RQ-12.02|559|CONDITIONAL_OPERATIONALIZATION|EMPIRICALLY_QUALIFIED|REJECTS_PROXY_RESTRICTION_ONLY
SYN-12|Le cas électrique compare des frontières de coût et de prix non appariées. Il ne permet ni transmission structurelle, ni marge totale, ni mesure de Utility ou Money; les données négatives sont conservées.|analysis/34_micro_empirical_results.md|RQ-05.01,RQ-05.03,RQ-12.02|363,364,349,400|BOUNDARIES_UNMATCHED|NOT_IDENTIFIABLE|NON_DISCRIMINATING
SYN-13|Le pont entre travail physique et Economic Work comporte une condition sur Utility. Toute énergie consommée ne devient donc pas automatiquement richesse; les pertes et usages non productifs restent distincts.|analysis/global_corpus_pass/concept_consistency.md|RQ-09.02,RQ-09.03|159,203,455,456|EXPLICIT_CONDITIONAL_CONSTRUCTION|ECONOMIC_BRIDGE_NOT_MEASURED|POTENTIALLY_DISTINCT_CLASSIFICATION
SYN-14|La chaîne vers les dommages est effectivement présente. Restent absentes une allocation marginale précise du gain et une fonction de dommage pour le panier hétérogène; les usages épargnés empêchent une consommation automatique.|analysis/global_corpus_pass/root_question_chain.md|RQ-10.01,RQ-10.02,RQ-11.01,RQ-11.02,RQ-11.03,RQ-12.01|52,72,112,163,164,165,454,460,523|EXPLICIT_LINKS_WITH_MISSING_CLOSURE|GENERAL_COMPATIBILITY_NOT_ATTRIBUTION|SPECIFIC_CAUSAL_EXPLANATION_NOT_IDENTIFIED
'''

MINIMAL = '''# Reconstruction minimale

INTERPRETATION de synthèse : ce noyau descriptif n'est pas un remplacement silencieux des lois proposées. Les branches formelles supplémentaires sont indiquées séparément. [SYN-01–14](results.json).

| Liaison minimale | Statut | Source PDF / contrôle |
|---|---|---|
| Cash support et nombre n; u valeur attribuée; M=n·u | EXPLICIT, définition | CPC-0053, scénarios monétaires; SYN-01 |
| Product support de transformations et Utility contextuelle | EXPLICIT | p108–111,159; SYN-04/13 |
| tâche/labour ≠ Economic Work | EXPLICIT | p187–207; SYN-02 |
| changement de procédé/vitesse → variation Work | CONDITIONAL | cp, tâche, frontière et référence fixés; SYN-02/03 |
| transformation productive → effet sur coût | CONDITIONAL | p19–21,196–207,361–364; SYN-05/06 |
| coût → prix, marge, partage entre acteurs | CONDITIONAL, branches distinctes | p363–364,504–508; SYN-05 |
| prix/Utility → gain du destinataire / Money | EXPLICIT dans la construction, UNRESOLVED en mesure | p291,349,400; SYN-01/04/12 |
| gain → possibilités d'usage, et non consommation nécessaire | EXPLICIT | p52,468,523; SYN-14 |
| énergie physique → travail physique utile → Work économique | CONDITIONAL sur Utility | p455–456; SYN-13 |
| production/usages → flux et déchets → dommages | EXPLICIT dans le récit, UNRESOLVED quantitativement | p72,112,454–460; SYN-14 |
| somme micro → coefficient macro stable | UNRESOLVED hors hypothèses d'agrégation | p538,559; SYN-07/11 |

Le plus petit modèle utile suit donc **transformation, support, valeur pour un acteur et destination du gain**. Le paiement seul ne renseigne pas ces quatre choses. Les quantités physiques, coûts/prix et flux comptables ne sont pas assimilés à T, Utility ou Money.

## Extension formelle à garder visible

La primitive T=½cpω² à cp fixe, les Core Laws reliant Forces et Utility, les potentiels, cycles et conversions Work/Money donnent des restrictions supplémentaires. Ce ne sont pas des conséquences du seul noyau descriptif. Le corpus reconnaît des hypothèses simplificatrices p301–303; les unités, conditions d'intégrabilité et étalons restent à spécifier. Voir [CORE](core_claims.md), [résultats négatifs](negative_results.md), SYN-02/03/04/07/08.

LEVEL A — INTERNAL : cohérences locales et branches restituées; plusieurs passages formels restent qualifiés.

LEVEL B — EXTERNAL COMPATIBILITY : boucles productivité/coût/demande et distinctions de comptes ont des précédents; aucune assimilation lexicale unique.

LEVEL C — DISTINCTIVE EXPLANATION : restrictions formelles repérables, mais pas encore de prédiction empirique indépendante départageant l'ensemble de la chaîne.
'''

ROOT_ANSWER = '''# Réponse provisoire à la question racine

## SOURCE

> The key question is therefore to understand how the increase in living standards has led to these environmental damages, or how we have moved from a subsistence society to an affluent society.

PDF **2–3**, début page2, continuation page3; CPC-0001. La phrase associée, page3, est :

> This essay should only be understood as a proposed answer to this question.

[Provenance corrigée](../../analysis/02_root_question.md) : la mention historique «page3» seule ne localise pas le début. [Chaîne consolidée](../../analysis/global_corpus_pass/root_question_chain.md). Les passages source sont distingués de l'INTERPRETATION ci-dessous.

## WHAT_CAMPERGUE_PROPOSES

Une explication par transformations productives, énergie bon marché, effets sur coût et possibilités de consommation. Sa construction relie Work, Utility et Money, sans assimiler tout paiement ou toute consommation physique d'énergie à une création. Les usages, pertes et acteurs introduisent plusieurs branches. RQ-02/03/06/09/10/11; CPC-0001,0015,0017,0022,0046; SYN-01/02/05/13/14.

## WHAT_IS_WELL_RECONSTRUCTED

Cash/Money, tâche/Work, création/transfert et coût/prix doivent rester séparés. Les scénarios de compensation monétaire et de partage du gain sont documentés, comme les exceptions de transport, brevet/rente et épargne. La lecture de562pages rend ces distinctions plus fidèles, pas automatiquement correctes dans tous leurs usages. SYN-01/05/14; [recontrôle des claims](../../analysis/global_corpus_pass/claim_rechecks.json).

## WHAT_IS_FORMALLY_SUPPORTED

Des dérivations locales tiennent à conditions annoncées : primitive quadratique à cp fixe, arithmétique +78%, conservation d'un bilan à frontière commune, invariance de K sous certaines compositions. Les recodages de Utility précisent au contraire quelles opérations ne sont pas ordinales. Ce support porte sur ces résultats conditionnels ou diagnostics, pas sur une loi économique autonome. SYN-02/03/04/06/07; RQ-03.02/03.03/04.02/05.03/08.02.

## WHAT_IS_EMPIRICALLY_COMPATIBLE

Les associations énergie/activité, les mécanismes de productivité et la réaffectation de gains sont compatibles avec des parties du récit. Des cadres de production, d'incidence des coûts, de surplus et de travail physique utile produisent aussi de telles observations. Compatibilité n'implique donc ni exclusivité ni attribution causale. SYN-10/13/14; [comparaisons](contributions.md).

## WHAT_IS_EMPIRICALLY_SUPPORTED_WITHIN_SCOPE

L'étude a reproduit des faits descriptifs : association mondiale positive PIB/énergie primaire sur1990–2023, co-mouvements annuels, variation des ratios et hétérogénéité des pays/périodes. Ce sont des résultats sur les données choisies, avec incertitude statistique, non une mesure de T ou Money. Le test micro ne fournit pas un coefficient de transmission structurel. SYN-10/11/12; [rapport empirique](../../analysis/27_energy_results.md).

## WHAT_REMAINS_UNMEASURED

T indépendant de la relation qui le construit, cp et Forces étalonnés, Utility sur une échelle compatible, Money indépendant, gain marginal alloué et dommages correspondants. Les niveaux L3 représentent des procédures possibles, pas nécessairement des mesures déjà disponibles; l'énergie physique L5 ne rend pas son pont économique observable. RQ-03.03/05.03/09.02/10.02/11.03; [métrologie](../operationalization/variables.md).

## WHAT_IS_AMBIGUOUS

Les référents de T/dT, certaines égalités de Utility entre acteurs, les unités et contraintes des potentiels, la composition de K et certaines frontières de création. Les ambiguïtés n'autorisent ni une réparation tacite ni une contradiction globale. SYN-03/04/07/08; RQ-03.02/05.03/08.03/08.04/09.02.

## WHAT_IS_QUALIFIED_OR_WEAKENED

La transmission automatique coût→prix n'est pas la reconstruction correcte; la neutralité ne suit pas de M=n·u seul. Le coefficient macro constant n'est pas assuré par le nombre de produits; sa version énergie primaire/PIB fixe ne décrit pas les observations. Certains raisonnements locaux de limites, signes et conservation demandent correction ou hypothèses supplémentaires. SYN-01/05/07/08/11.

## WHAT_ALTERNATIVE_EXPLANATIONS_EXIST

Progrès technique, substitution d'intrants, mécanisation, échelle, concurrence, marges, demandes et institutions; réaffectation de dépenses et changements de composition; effets physiques du mix énergétique et des matériaux. La bibliothèque comparée en documente plusieurs, sans revue historique exhaustive. Ayres–Warr fournit notamment un précédent de boucle travail physique utile/coûts/prix/demande, non un équivalent de Money. [Sources](source_register.md), CBIB-02, BIB-0002, CBIB-06, BIB-0021.

## PROVISIONAL_ANSWER

Le corpus propose une voie explicative conditionnelle : des transformations productives, souvent appuyées sur l'énergie mécanique, élargissent ce qu'il est possible de produire ou d'obtenir pour un coût donné. Selon le partage du gain, les prix, la qualité et les usages, ces possibilités peuvent alimenter davantage de consommation et de production. Leurs besoins physiques, pertes et déchets contribuent alors à des pressions environnementales. Cette chaîne est effectivement présente dans le manuscrit; elle n'est ni une identité inévitable entre abondance et dommage, ni une causalité historique quantifiée. L'allocation marginale des gains, la fonction de dommage et la mesure indépendante de plusieurs variables propres au système manquent encore. La contribution explicative spécifique de ce formalisme, au-delà de mécanismes économiques et physiques déjà connus, reste à identifier. SYN-01–14; RQ-12.01/12.02/12.03, CPC-0001.

## CONFIDENCE

MEDIUM pour cette réponse narrative conditionnelle et ses limites; LOW pour une attribution causale quantitative ou une supériorité explicative spécifique. La fidélité textuelle des passages cités est distincte de ces jugements. Aucune moyenne de confiance ni verdict binaire global.
'''

OPEN = '''# Questions majeures restant ouvertes

Ces15priorités regroupent les53questions sans les supprimer ni changer leurs identifiants. Sources et qualifications : [fiches](question_synthesis.md), [résultats](results.json).

| Type | Question restante | RQ / enjeu |
|---|---|---|
| FORMAL | Quel référent unique, ou quels référents locaux explicites, distinguent état T, réserve et transfert dT? | RQ-03.02; SYN-02/03 |
| METROLOGICAL | T, cp et Force peuvent-ils être mesurés sans la relation quadratique à tester? | RQ-03.03; SYN-03 |
| METROLOGICAL | Quelle échelle de Utility autorise différences, rapports et comparaison entre acteurs? | RQ-05.03; SYN-04 |
| FORMAL | Les Core Laws restent-elles cohérentes après explicitation des limites, contraintes et conditions d'intégrabilité? | RQ-08.03; SYN-08 |
| FORMAL | Sous quelles conditions les cycles, signes, bornes et optimum se raccordent-ils? | RQ-04.04; SYN-06/08 |
| METROLOGICAL | Quel contenu économique de K peut être fixé indépendamment plutôt qu'absorber les résidus? | RQ-08.02/08.04; SYN-07/11 |
| METROLOGICAL | Le pont travail physique utile→Economic Work a-t-il un étalon indépendant de Utility? | RQ-09.02/09.03; SYN-13 |
| EMPIRICAL | Un même produit permet-il de suivre coût complet, prix, qualité, quantité et partage du gain? | RQ-05.01; SYN-05/12 |
| METROLOGICAL | Une variation de Money possède-t-elle une conséquence observable indépendante de sa définition? | RQ-06.04; SYN-01/03 |
| CAUSAL | Quelle destination marginale d'un gain est attribuable à sa source productive? | RQ-10.01/10.02; SYN-14 |
| EMPIRICAL | Comment relier le panier additionnel aux flux importés, au mix et aux dommages? | RQ-11.01/11.03; SYN-14 |
| HISTORICAL | Quel seuil et quel contrefactuel rendent testable la transition subsistance→abondance? | RQ-01.03; SYN-14 |
| HISTORICAL | L'assemblage formel a-t-il un antécédent précis et quelle utilité apporte-t-il après traduction? | RQ-12.02; CC-01–04 |
| FORMAL | La frontière productive classe-t-elle uniformément services, rente, crédit et transport selon les acteurs? | RQ-02.02/07.02; SYN-05/13 |
| CAUSAL | Quelle restriction observable préenregistrée départage effectivement le système et les explications concurrentes? | RQ-12.01/12.02/12.03; SYN-10/12/14 |
'''

FUTURE = '''# Programme futur — protocoles proposés, non exécutés dans cette synthèse

La priorité va à l'identification et aux étalons, pas à une multiplication de corrélations. Toutes les propositions restent DESIGN_ONLY. [Niveaux actuels](../operationalization/variables.md), [expériences antérieures](../fourth_pass_report.md).

| Priorité / travail | Question et hypothèse | Variables et données nécessaires | Méthode / alternative | Pouvoir discriminant / difficulté |
|---|---|---|---|---|
| 1 — Étendre l'audit T/cp | RQ-03.03 : un étalon indépendant est possible | T,cp,ω,Force; procédé contrôlé, mesure externe à la primitive | Fixer définitions et unités avant calibration; comparer primitive et autre fonction sans reconstruire la cible | Potentiellement élevé, actuellement bloqué; élevée |
| 2 — Échelle Utility | RQ-05.03 : les rendements sont invariants aux changements d'unités admissibles | Utility et coefficients; protocole d'élicitation, contexte et zéro spécifiés | Tester recodages admissibles; distinguer ordinal, affine et ratios, pas WTP substitué silencieusement | Élevé formel, empirique indéterminé; moyenne/élevée |
| 3 — Micro apparié | RQ-05.01 : un scénario donné prévoit partage du gain | coût complet, prix, marge, quantité, caractéristiques même produit/acteur | Panel court autour changement de procédé; différence-en-différences seulement avec groupe/tendances crédibles; contrôle intrants/demande | Moyen si restriction préfixée; élevée, NEEDS_DATA |
| 4 — K hors calibration | RQ-08.02 : coefficients locaux fixes prédisent l'agrégat nouveau | unités communes,T ou proxy déclaré, composition, K locaux calibrés antérieurement | Séparer estimation et période test; comparer moyenne pondérée variable et constante | Moyen pour restriction spécifiée, pas K résiduel; élevée |
| 5 — Destination du gain | RQ-10.02 : baisse de prix modifie panier, épargne et dette | dépenses ménages longitudinales, revenus, prix, chocs comparables | Quasi-expérience préenregistrée; concurrence de l'effet revenu, substitution et anticipation | Moyen, non spécifique isolément; élevée |
| 6 — Chaîne d'impacts | RQ-11.03 : panier marginal augmente certaines pressions | résultat du travail5, tables entrées-sorties environnementales, importations/mix | Comptabilité consommation avec incertitude; énergie, matière, émissions et dommages séparés | Faible seul, utile pour clôture causale; élevée |
| 7 — Réparer puis tester les dérivations locales | RQ-08.03/04.04 : hypothèses explicites suffisent | formules source, unités, domaines, signes et contraintes | SOURCE_FORMALISM contre MINIMAL_RECONSTRUCTION; contre-exemples symboliques et bornes avant optimisation | Élevé formel local; moyenne, DO_NOW |
| 8 — Audit comparatif des classements | RQ-02.02/12.02 : distinctions améliorent un diagnostic | mêmes transactions mixtes, taxonomie source, comptes usuels et surplus | Double codage indépendant, erreurs/désaccords préspécifiés; recherche historique ciblée | Moyen pour valeur analytique, aucun test causal Money; moyenne |
'''

LIMITATIONS = '''## LIMITATIONS_OF_THIS_REVIEW

Le corpus disponible et sa traduction/extraction bornent l'étude.562pages scannées ne signifient pas562analyses approfondies :447pages ont une lecture analytique cumulée, et aucune nouvelle étiquette DEEP_REVIEWED n'a été attribuée pendant la consolidation. Les formules sensibles ont des contrôles locaux mais tous les298labels ne sont pas298démonstrations auditées indépendamment.

La littérature est ciblée, non exhaustive; certains rapprochements reposent sur métadonnées ou résumés explicitement PARTIALLY_VERIFIED. Aucune priorité historique générale n'est établie. Les catégories économiques courantes sont des comparateurs, pas des traductions automatiques de Money, Utility ou Work.

Les données empiriques sont limitées, agrégées ou mal appariées au niveau micro. Les tendances, changements de composition et causalités inverses restent des explications concurrentes. Les intervalles statistiques ne capturent pas toute l'incertitude de mesure ou de spécification.

Plusieurs variables propres au système manquent d'étalon indépendant. Une définition opératoire L3 n'est pas une donnée déjà mesurée. Les résultats formels synthétiques testent des constructions explicites, pas des comportements observés. Les problèmes locaux de signe, limite, unité et agrégation restent ouverts sans conclusion globale.

La synthèse est une INTERPRETATION traçable, pas une déclaration de l'auteur. Les tests contrôlent sa couverture, sa provenance et sa reproductibilité; ils ne certifient pas les jugements scientifiques. Source : bilan de consolidation, rapports2–5, résultats SYN-01–14 et registre bibliographique.
'''
