# Revue bibliographique et red team

Sept sources primaires/méthodologiques vérifiées sur passages ciblés, non une recherche historique exhaustive. Les références internes ne sont pas toutes revérifiées. Aucun ORIGINAL.

## ER-BIB-01

[BEA, FAQ1197, 2018](https://www.bea.gov/help/faq/1197)

Définition institutionnelle: valeur ajoutée nette des consommations intermédiaires; somme égale au PIB. Entrée lue, pas audit complet des comptes.

## ER-BIB-02

[JCGM, VIM3 §1.26, 2012](https://jcgm.bipm.org/vim/en/1.26.html)

Les grandeurs ordinales ne permettent pas les opérations algébriques des quantités à échelle appropriée. Entrée métrologique; ne fournit pas une mesure de Utility.

## ER-BIB-03

[Ayres & Warr, 2002/70/EPS/CMER, INSEAD working paper](https://flora.insead.edu/fichiersti_wp/inseadwp2002/2002-70.pdf)

Le passage pp6–7 du PDF décrit déjà énergie/travail utile, coût, prix concurrentiel, demande et rétroactions; distingue corrélation et causalité. Working paper de 2002, pas substitution au texte publié en 2005; aucun résultat économétrique repris ici.

## ER-BIB-04

[Ritchie & Rosado, OWID, méthode de substitution, version historique](https://archive.ourworldindata.org/20260807-182216/energy-substitution-method.html)

L’équivalence primaire de l’électricité non fossile repose sur une efficacité thermique supposée. Méthode consultée; la base interne est épinglée en 2025, non la série actuelle modifiée en 2026.

## ER-BIB-05

[Marshall, Principles of Economics, 8e éd., 1920, III.VI](https://www.econlib.org/library/Marshall/marP.html?chapter_num=15)

Le surplus distingue paiement et bénéfice, avec demande et disposition à payer; ce n’est pas un gain budgétaire fixe identique. Section sur surplus lue; pas identité entre surplus et Money.

## ER-BIB-06

[BLS, Handbook of Methods, Productivity: Concepts](https://www.bls.gov/opub/hom/msp/concepts.htm)

Output, heures, composition du travail et inputs sont déjà séparés; les décompositions imposent leurs propres hypothèses. Méthode consultée, pas équivalence de T avec TFP.

## ER-BIB-07

[McLeay, Radia & Thomas, Money creation in the modern economy, 2014](https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/2014/money-creation-in-the-modern-economy.pdf)

Création de dépôts par crédit et destruction par remboursement sont des opérations de bilan. Passages de bilan et remboursement lus; money institutionnel non automatiquement Money Campergue.

## Quatre attaques comparatives

| id | title | source_pages | precedence | attack_precedence | renaming_test | measurement_attack | prediction_attack | assumption_attack | surviving_residue | review_status | novelty | bibliography | confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CC-01 | Séparer paiement, transformation et destination du gain | [159, 271, 363, 468, 479, 490, 507, 523] | KNOWN_PRECEDENT_FOUND | Paiement, production nette, transfert et surplus ont des précédents. | LIKELY_REFORMULATION pour le recouvrement; ne pas effacer le résidu décrit. | Aucune nouvelle mesure opérationnelle établie. | Aucune différence observable identifiée avec les variables disponibles. | Frontières/échelles/coefficient ou condition Utility doivent être fixés indépendamment. | Une présentation commune des frontières et bénéficiaires peut être utile; supériorité non mesurée. | QUALIFIED | NOVELTY_UNRESOLVED | ['ER-BIB-01', 'ER-BIB-05', 'ER-BIB-07'] | MEDIUM |
| CC-02 | Tâche, vitesse et Work additionnel | [203, 207, 208, 341, 355, 467, 470, 501, 547] | PARTIAL_PRECEDENT | Tâche, cadence et productivité sont déjà séparables; T quadratique n’est pas une simple traduction de TFP. | LIKELY_REFORMULATION pour le recouvrement; ne pas effacer le résidu décrit. | Aucune nouvelle mesure opérationnelle établie. | Aucune différence observable identifiée avec les variables disponibles. | Frontières/échelles/coefficient ou condition Utility doivent être fixés indépendamment. | Restriction formelle distincte sous cp fixe, mais ni T ni cp indépendamment mesurés. | QUALIFIED | NOVELTY_UNRESOLVED | ['ER-BIB-06'] | MEDIUM |
| CC-03 | Exigences d’échelle de Utility | [111, 132, 249, 285, 301, 377, 392, 425, 511, 520] | KNOWN_PRECEDENT_FOUND | Exigence d’échelle connue; diagnostic appliqué par les reviewers, pas nouveauté historique attribuable. | LIKELY_REFORMULATION pour le recouvrement; ne pas effacer le résidu décrit. | Aucune nouvelle mesure opérationnelle établie. | Aucune différence observable identifiée avec les variables disponibles. | Frontières/échelles/coefficient ou condition Utility doivent être fixés indépendamment. | Audit des opérations du corpus utile même sans contribution nouvelle de l’auteur. | QUALIFIED | NOVELTY_UNRESOLVED | ['ER-BIB-02'] | MEDIUM |
| CC-04 | Condition Utility dans le pont physique | [72, 159, 271, 454, 455, 456, 479, 559] | PARTIAL_PRECEDENT | Pont énergie/travail utile/coût/prix/demande possède un précédent explicite. | LIKELY_REFORMULATION pour le recouvrement; ne pas effacer le résidu décrit. | Aucune nouvelle mesure opérationnelle établie. | Aucune différence observable identifiée avec les variables disponibles. | Frontières/échelles/coefficient ou condition Utility doivent être fixés indépendamment. | Condition économique sur Utility constitue un résidu possible, actuellement sans mesure indépendante. | QUALIFIED | NOVELTY_UNRESOLVED | ['ER-BIB-03'] | MEDIUM |
