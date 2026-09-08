PHASE 2 STATUS

INCOMPLETE — cette exécution ne satisfait pas la lecture intégrale demandée.
L'échec restant nécessite de poursuivre la lecture et la reconstruction ; aucune
inaccessibilité externe n'est invoquée. La grande revue externe n'a pas commencé.

SOURCE

commit : a697345c427fca8de0521108a17aa2b76f267654
pages : 562
SHA256 : 7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827

READING

48 / 562 : pages 1–37 et 184–194. Reprise séquentielle requise à la page 38,
puis 195 après la plage ciblée déjà examinée. Aucune page exclue définitivement.

CONCEPTS

36 entrées ; les mentions contextuelles sont distinguées des définitions formelles.

CLAIMS

total : 63
CORE : 24
MAJOR : 32
SUPPORTING : 7
PERIPHERAL : 0

CLAIM TYPES

ANALOGICAL : 2
ASSUMPTION : 4
AXIOM : 6
CONCEPTUAL : 10
DEFINITION : 19
DERIVED : 3
EMPIRICAL : 1
HYPOTHESIS : 10
MECHANISM : 1
METHODOLOGICAL : 5
NORMATIVE : 1
OPEN_QUESTION : 1

ARGUMENT GRAPH

nodes : 64
edges : 49
cycles détectés : 2
orphans (nœuds isolés) : 11
Orphelins de chapitre parmi les claims enregistrés : 0.

RESEARCH CHAPTERS

10 candidats provisoires ; classification définitive non établie.

CH-01 : Origine de la richesse et périmètre explicatif
CH-02 : Mesure monétaire et neutralité du nombre d’unités
CH-03 : Objets, supports, tâches et points de vue
CH-04 : Productivité, énergie et transmission aux prix
CH-05 : Principes, conservation et domaine du formalisme
CH-06 : Lois constitutives et transformations élémentaires
CH-07 : Cycles, création et rendements
CH-08 : Agrégation, potentiels et coefficients
CH-09 : Couplage énergétique et conservation
CH-10 : Agents, marchés et applications

ROOT QUESTION

“The key question is therefore to understand how the increase in living standards has led to these environmental damages, or how we have moved from a subsistence society to an affluent society.”

Correction : commence page PDF 2, se termine page 3. La phrase associée est page 3.
Les dix questions de chapitre portent sur les conditions, les grandeurs ou les
applications du mécanisme de création de richesse censé répondre à cette question.
Le volet environnemental reste particulièrement ouvert (exclusion locale p29).

RESEARCH QUESTIONS

10 questions, une par chapitre candidat.

TESTABLE HYPOTHESES

7 propositions de tests, non exécutées ; plusieurs nécessitent une mesure
indépendante encore indéfinie. Leur opérationnalisation n'est donc pas acquise.

RAG

Méthodes comparées : legacy TF brut × IDF, cosinus TF-IDF, BM25.
Golden questions : 66 (60 anglais, 6 français), jeu de développement partiel.
564 chunks ; 3 documents indexés.

| Méthode | Recall@1 | Recall@3 | Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|
| legacy | 0.2348 | 0.5530 | 0.5833 | 0.3838 |
| tfidf | 0.4621 | 0.6667 | 0.7727 | 0.5740 |
| bm25 | 0.4924 | 0.6818 | 0.8030 | 0.6121 |

BM25 devient le défaut, mais Recall@5 français = 0 sur les six questions.
Le corpus anglophone n'est pas rendu multilingue par ce changement.

REGRESSION

tests PASS : 20
tests FAIL : 1
errors : 0
skipped : 0
total : 21
verify.sh : FAIL, code 1 ; critère de sortie 48/562 non atteint.

UNRESOLVED

- 514 pages non examinées : 38–183 et 195–562.
- Table des matières encore provisoire pour le corps non lu ; sous-sections incomplètes.
- Définitions et changements de sens tardifs non reconstruits ; capital non documenté.
- Quatre chapitres candidats sans claims ; graphe encore partiel.
- Dimensions, loi vitesse/énergie, transmission coût/prix, coefficient g et signe du bilan à suivre.
- Portée de l'exclusion des critères humains versus Utility subjective à reconstruire.
- Section Entropy p463 et volet environnemental à examiner.
- Golden set non représentatif de l'ensemble ; pertinence non exhaustive ; français insuffisant.
- Deux PDF secondaires et documentation du code absents de l'index.
- Aucun résultat empirique reproduit ; données nécessaires aux tests non inspectées.
- Revue visuelle des formules, tableaux et schémas non faite.

FILES CREATED/MODIFIED

Créés :

- .gitignore
- analysis/10_phase2_baseline.md
- analysis/11_manuscript_structure.md
- analysis/12_claim_coverage.md
- analysis/13_semantic_invariants.md
- analysis/14_argument_reconstruction.md
- analysis/15_research_chapter_classification.md
- analysis/16_claim_chapter_coverage.md
- analysis/17_core_claims.md
- analysis/18_rag_evaluation.md
- analysis/19_phase2_handoff.md
- analysis/data/claim_chapter_matrix.csv
- analysis/data/core_claims.json
- analysis/data/graph_audit.json
- analysis/data/hypotheses.json
- analysis/data/manuscript_structure.json
- analysis/data/open_reconstruction_issues.json
- analysis/data/page_coverage.json
- analysis/data/phase2_progress.json
- analysis/data/regression_snapshot.json
- analysis/data/research_chapters.json
- analysis/data/research_questions.json
- analysis/data/root_question.json
- analysis/data/semantic_invariants.json
- analysis/history/phase1/analysis/02_root_question.md
- analysis/history/phase1/analysis/data/argument_graph.json
- analysis/history/phase1/analysis/data/claims.jsonl
- analysis/history/phase1/analysis/data/concepts.json
- analysis/history/phase1/rag/build_index.py
- analysis/history/phase1/rag/index/manifest.json
- analysis/history/phase1/rag/query.py
- analysis/history/phase1/verify.sh
- analysis/phase2_curate.py
- analysis/phase2_handoff.py
- analysis/phase2_reports.py
- analysis/reading_notes/p001_011.md
- analysis/reading_notes/p012_025.md
- analysis/reading_notes/p026_037.md
- analysis/reading_notes/p184_194.md
- analysis/schemas/claim.schema.json
- rag/evaluation/evaluate.py
- rag/evaluation/golden_questions.jsonl
- rag/evaluation/make_golden.py
- rag/evaluation/results.json
- rag/retrieval.py
- requirements.txt
- tests/corpus/test_phase2.py
- tests/run_phase2.py
- validation/phase2_files.json
- validation/phase2_regression_results.json

Modifiés par rapport à la phase 1 :

- README_RESEARCH.md
- analysis/02_root_question.md
- analysis/data/argument_graph.json
- analysis/data/claims.jsonl
- analysis/data/concepts.json
- rag/build_index.py
- rag/index/manifest.json
- rag/query.py
- verify.sh

GIT STATUS

```text
## research/corpus-validation
?? .gitignore
?? README_RESEARCH.md
?? analysis/
?? corpus/
?? rag/
?? requirements.txt
?? tests/
?? validation/
?? verify.sh

```

Aucun commit ni push effectué. Les sources PDF restent inchangées.

READY_FOR_BIBLIOGRAPHIC_ADVERSARIAL_REVIEW = NO
