# WEAKEST_POINTS

Neuf points limitant la portée quantitative actuelle, non neuf réfutations.

1. La primitive quadratique ne fournit pas une mesure indépendante de T. Si cp varie, sa différentielle contient aussi ½ω²dcp. Réserve, état et transfert ne sont pas interchangeables. ([SYN-03](negative_results.md)). Source : [research_questions/operationalization/circularity_review.md](../../research_questions/operationalization/circularity_review.md)

2. Un ordre de Utility conserve des comparaisons, pas les rapports numériques utilisés dans certains rendements. Des différences pondérées peuvent covarier avec les coefficients; toutes les formules n'exigent donc pas la même échelle. ([SYN-04](negative_results.md)). Source : [research_questions/experiments/EXP-02/results.json](../../research_questions/experiments/EXP-02/results.json)

3. Sous additivité, unités communes et coefficients locaux fixes, K est une moyenne pondérée. Composition fixe est suffisante, pas nécessaire; invariance à toute composition exige des coefficients identiques sur les composantes actives. ([SYN-07](negative_results.md)). Source : [research_questions/experiments/EXP-03/results.json](../../research_questions/experiments/EXP-03/results.json)

4. Des erreurs ou sauts locaux restent documentés: égalité interpersonnelle issue de 0/0, force constante assimilée à force nette nulle, primitives, signes et passage d'inégalités de niveaux aux dérivées. Leur portée doit rester locale. ([SYN-08](negative_results.md)). Source : [analysis/global_corpus_pass/formal_checks.json](../../analysis/global_corpus_pass/formal_checks.json)

5. Une corrélation avec une énergie reconstituée depuis un ratio incorporant le PIB demande un audit de filiation. La présence du PIB dans le ratio ne prouve pas seule une circularité si une mesure énergétique indépendante est restituée. ([SYN-09](negative_results.md)). Source : [analysis/27_energy_data_independence.md](../../analysis/27_energy_data_independence.md)

6. GDP=K·W avec K strictement constant et W identifié à l'énergie primaire ne décrit pas les ratios observés. Cela qualifie cette identification forte, pas toutes les versions du coefficient économique. ([SYN-11](negative_results.md)). Source : [analysis/27_energy_results.md](../../analysis/27_energy_results.md)

7. Le cas électrique compare des frontières de coût et de prix non appariées. Il ne permet ni transmission structurelle, ni marge totale, ni mesure de Utility ou Money; les données négatives sont conservées. ([SYN-12](negative_results.md)). Source : [analysis/34_micro_empirical_results.md](../../analysis/34_micro_empirical_results.md)

8. Le pont entre travail physique et Economic Work comporte une condition sur Utility. Toute énergie consommée ne devient donc pas automatiquement richesse; les pertes et usages non productifs restent distincts. ([SYN-13](negative_results.md)). Source : [analysis/global_corpus_pass/concept_consistency.md](../../analysis/global_corpus_pass/concept_consistency.md)

9. La chaîne vers les dommages est effectivement présente. Restent absentes une allocation marginale précise du gain et une fonction de dommage pour le panier hétérogène; les usages épargnés empêchent une consommation automatique. ([SYN-14](negative_results.md)). Source : [analysis/global_corpus_pass/root_question_chain.md](../../analysis/global_corpus_pass/root_question_chain.md)


Complément de provenance SYN-08 : [bilan global, FORMAL ISSUES](../../analysis/global_corpus_pass/final_report.md), pour les égalités interpersonnelles et les forces constantes; le fichier formal_checks.json ne couvre que quatre diagnostics numériques locaux.
