# Littérature ciblée — énergie, agrégation et effets indirects

Six références ajoutées : cinq VERIFIED, une PARTIALLY_VERIFIED. « Vérifiée » concerne la référence et le passage consulté, pas une lecture intégrale ni une validation de Campergue. Les anciennes références et relations sont conservées. Fichiers : `bibliography/energy_aggregation_library.{json,bib}` et `analysis/data/literature_map.json`.

| Source | Passage réellement consulté | Relation et limite |
|---|---|---|
| BIB-0011, Banque mondiale, métadonnée EG.GDP.PUSE.KO.PP.KD | Définition, méthode, provenance et limites ; HTML archivé | DOES_NOT_TEST CPC-0118 : provenance des données, pas preuve du modèle |
| BIB-0012, OWID/EI/EIA, millésime2025 figé | CSV, codebook, README ; code amont primaire inspecté | DOES_NOT_TEST CPC-0118 : construction indépendante du PIB, pas mesure de T/M |
| BIB-0013, Stern2011 | Résumé et début de l’article dans le dépôt ANU, pp26–28 | SUPPORTS rôle énergétique général CPC-0018 ; QUALIFIES couplage rigide CPC-0118 ; DOES_NOT_TEST pont CPC-0119 |
| BIB-0014, Sorrell2007, UKERC | Notice et PDF, introduction et encadrés1.1–1.2, pages PDF15–18 | PARALLELS usage du gain CPC-0127 ; QUALIFIES universalité de la hausse d’énergie CPC-0120 |
| BIB-0015, Baqaee/Farhi2018, NBER25293 | Métadonnées et résumé officiel indexés seulement | QUALIFIES CPC-0117 au niveau méthodologique ; téléchargement direct403, pas de théorème détaillé utilisé |
| BIB-0016, Ling/Moebs/Sanny2016, OpenStax§4.6 | Fonction d’état et exemple4.5 sur refroidissement irréversible | QUALIFIES emploi de l’entropie CPC-0067 ; pas de rejet automatique du formalisme économique |

Stern présente des liens énergie/croissance modulés par rareté, technologie et composition ; cette approche offre une explication concurrente à une constante universelle. Sa discussion de causalité de Granger ne confère aucune identification causale à nos OLS. [Article, dépôt institutionnel ANU](https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/4535717f-80cb-429d-88d6-f7bc90c5f946/content).

Sorrell distingue demande supplémentaire du même service, achats ailleurs grâce au gain et effets macroéconomiques. Le passage de Campergue p.400 partage une partie de cette logique, mais pas un contrefactuel énergétique défini. Comparaison : **PARTIAL_PARALLEL**, non SAME_MECHANISM universel ni preuve de backfire. [Rapport UKERC](https://ukerc.rl.ac.uk/publications/research_report/The_Rebound_Effect_An_Assessment_of_the_Evidence_for_Economy-wide_Energy_Savings_from_Improved_Energy_Efficiency.pdf).

La notice de Baqaee/Farhi relie les caractéristiques macroéconomiques aux structures microéconomiques. Elle justifie de poser la question des pondérations ; nous n’en tirons aucune réfutation technique particulière de Campergue tant que le texte complet n’a pas été examiné. [Notice NBER](https://www.nber.org/papers/w25293).

Le point physique d’entropie est plus précis : un calcul entre états peut employer un chemin réversible fictif, mais le flux de chaleur réel irréversible ne suffit pas à donner dS par division par T. La présence de pertes ne fait pas cesser une fonction d’état physique d’être une fonction d’état. Les potentiels économiques doivent toutefois être évalués selon leurs propres définitions avant toute transposition de cette remarque. [OpenStax, §4.6](https://openstax.org/books/university-physics-volume-2/pages/4-6-entropy).

Les relations nouvelles totalisent : SUPPORTS1, QUALIFIES4, PARALLELS1, DOES_NOT_TEST3, CONTRADICTS0. Cela n’efface pas les difficultés locales : l’implication Force constante→a/e constants est examinée algébriquement, et l’opérationnalisation de GDP=K·énergie à K constant est confrontée aux données. Ce sont des objections distinctes d’une référence externe affirmant la fausseté d’un claim entier.

Accès non aboutis : archive OWID via navigateur web (dépôt GitHub figé utilisé à la place) ; notice Sussex initiale du rebond (rapport institutionnel UKERC accessible) ; accès direct NBER25293 et PDF403 (statut partiel conservé). Aucun DOI inventé ; Sorrell n’en possède pas dans la notice UKERC consultée.
