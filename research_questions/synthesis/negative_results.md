> ÉTAT APRÈS REMÉDIATION : les qualifications explicites ci-dessous actualisent les formulations historiques. CPC-0016 : NOT_IDENTIFIED pour la chaîne complète. Source et intention de l’auteur restent distinctes de la portée retenue.

# Résultats négatifs et non identifiables

Ne pas effacer ces diagnostics lors d’une nouvelle synthèse. NOT_IDENTIFIED n’est pas une contradiction; une erreur locale n’est pas un rejet global.

## SYN-03

La primitive quadratique ne fournit pas une mesure indépendante de T. Si cp varie, sa différentielle contient aussi ½ω²dcp. Réserve, état et transfert ne sont pas interchangeables.

Périmètre : NOT_IDENTIFIED. Source : [research_questions/operationalization/circularity_review.md](../../research_questions/operationalization/circularity_review.md)

## SYN-04

Un ordre de Utility conserve des comparaisons, pas les rapports numériques utilisés dans certains rendements. Des différences pondérées peuvent covarier avec les coefficients; toutes les formules n'exigent donc pas la même échelle.

Périmètre : MEASUREMENT_REQUIREMENT. Source : [research_questions/experiments/EXP-02/results.json](../../research_questions/experiments/EXP-02/results.json)

## SYN-07

Sous additivité, unités communes et coefficients locaux fixes, K est une moyenne pondérée. Composition fixe est suffisante, pas nécessaire; invariance à toute composition exige des coefficients identiques sur les composantes actives.

Périmètre : NOT_STRUCTURAL_K_ESTIMATE. Source : [research_questions/experiments/EXP-03/results.json](../../research_questions/experiments/EXP-03/results.json)

## SYN-08

Des erreurs ou sauts locaux restent documentés: égalité interpersonnelle issue de 0/0, force constante assimilée à force nette nulle, primitives, signes et passage d'inégalités de niveaux aux dérivées. Leur portée doit rester locale.

Périmètre : DOES_NOT_TEST_EMPIRICAL_SYSTEM. Source : [analysis/global_corpus_pass/formal_checks.json](../../analysis/global_corpus_pass/formal_checks.json)

## SYN-09

Une corrélation avec une énergie reconstituée depuis un ratio incorporant le PIB demande un audit de filiation. La présence du PIB dans le ratio ne prouve pas seule une circularité si une mesure énergétique indépendante est restituée.

Périmètre : INDEPENDENCE_REQUIRES_SOURCE_AUDIT. Source : [analysis/27_energy_data_independence.md](../../analysis/27_energy_data_independence.md)

## SYN-11

GDP=K·W avec K strictement constant et W identifié à l'énergie primaire ne décrit pas les ratios observés. Cela qualifie cette identification forte, pas toutes les versions du coefficient économique.

Périmètre : EMPIRICALLY_QUALIFIED. Source : [analysis/27_energy_results.md](../../analysis/27_energy_results.md)

## SYN-12

Le cas électrique compare des frontières de coût et de prix non appariées. Il ne permet ni transmission structurelle, ni marge totale, ni mesure de Utility ou Money; les données négatives sont conservées.

Périmètre : NOT_IDENTIFIABLE. Source : [analysis/34_micro_empirical_results.md](../../analysis/34_micro_empirical_results.md)

## SYN-13

Le pont entre travail physique et Economic Work comporte une condition sur Utility. Toute énergie consommée ne devient donc pas automatiquement richesse; les pertes et usages non productifs restent distincts.

Périmètre : ECONOMIC_BRIDGE_NOT_MEASURED. Source : [analysis/global_corpus_pass/concept_consistency.md](../../analysis/global_corpus_pass/concept_consistency.md)

## SYN-14

La chaîne vers les dommages est effectivement présente. Restent absentes une allocation marginale précise du gain et une fonction de dommage pour le panier hétérogène; les usages épargnés empêchent une consommation automatique.

Périmètre : GENERAL_COMPATIBILITY_NOT_ATTRIBUTION. Source : [analysis/global_corpus_pass/root_question_chain.md](../../analysis/global_corpus_pass/root_question_chain.md)


Complément de provenance SYN-08 : [bilan global, FORMAL ISSUES](../../analysis/global_corpus_pass/final_report.md), pour les égalités interpersonnelles et les forces constantes; le fichier formal_checks.json ne couvre que quatre diagnostics numériques locaux.


## Remédiation externe — qualifications actuelles

SYN-01: Cash, Money, création, transfert et redistribution restent distingués. M=n·u est une identité; neutralité conditionnelle au scénario, acteur, horizon et référent. Solde, gain, cinétique, potentiel et transfert ne sont pas unifiés sans dictionnaire.

SYN-06: Le +78% reproduit (8/6)²−1 sous tâche, cp et hypothèse quadratique fixes. P32 revendique une généralité sous homogénéité; le calcul ne l’établit pas. NOT_GENERALIZED_EMPIRICALLY.

SYN-07: Sous additivité et unités communes, K est une moyenne pondérée; invariance sous composition fixe reste conditionnelle. P559 moyenne les vitesses: moyenne des carrés ≠ carré de moyenne; conserver dispersion et coefficients avant agrégation.

SYN-08: Les erreurs locales de limites, inversion p303, Force constante et substitutions restent distinctes de postulats admissibles. P301 autorise une hypothèse simplificatrice; elle ne répare pas sa dérivation. Portée strictement locale.

SYN-11: GDP=K·W à K strictement constant et W énergie primaire est qualifié par les ratios observés. Le raccord Money/valeur ajoutée/PIB et nominal/réel reste auparavant incomplet; p205 empêche d’imputer un double compte brut inévitable.

SYN-14: La chaîne vers les dommages est présente; l’auteur revendique une dégradation systématique p112 et formule des généralisations p454/537. La conclusion défendable reste conditionnelle: allocation marginale et fonction de dommage non identifiées.

CPC-0016: attribution conservée; chaîne complète NOT_IDENTIFIED. Les états historiques restent dans remediation/history; les corrections explicites prévalent sur les résumés historiques. Les tests sont des contrôles classés, pas des validations économiques.
