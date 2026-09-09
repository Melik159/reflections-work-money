# Reproduction

Statut courant : `PHASE_2_STATUS = SUFFICIENT_FOR_ITERATIVE_RESEARCH`.
247/562 pages du manuscrit examinées; détail dans `analysis/data/page_coverage.json`.
La couverture partielle est un avertissement, conformément à la nouvelle instruction
de l'utilisateur. Aucun verdict global sur la théorie.

Environnement testé : Python 3.14.4 ; dépendances directes verrouillées dans
requirements.txt. Le retrieval utilise uniquement la bibliothèque standard ;
PyMuPDF sert aux PDF secondaires, NumPy/pandas/matplotlib à la reproduction.

```bash
python3 -m venv .venv-research
.venv-research/bin/python -m pip install -r requirements.txt
./verify.sh
python3 -m rag.query --method bm25 "Quelle différence entre Cash et Money ?"
python3 -m rag.query --method bm25 --no-expansion "Cash Money"
python3 -m rag.query --method legacy "Cash Money"
python3 -m rag.query --method tfidf "Cash Money"
```

Le script vérifie les empreintes des trois PDF, les 562 pages JSONL, les citations,
les schémas, les liens, les invariants et le benchmark. Il réexécute le smoke test
original et les analyses macro dans un répertoire temporaire, puis compare les
trois CSV aux sorties du dépôt. Les sources et sorties originales restent intactes.
Il renvoie FAIL sur une incohérence technique ou un désaccord reproductible ;
couverture, bibliographie partielle et hypothèses ouvertes restent WARNING.
Résultats exacts : `validation/phase2_regression_results.json` et
`analysis/empirical/iteration1/results.json`. La vérification n'utilise pas de réseau.

L'index reste à la granularité existante d'une page, avec deux Markdown complets.
Les trois PDF et deux Markdown sont indexés : 590 chunks, cinq documents.
La documentation du code n'est pas encore indexée.
Les 66 questions constituent un jeu de développement localisé aux pages examinées,
pas une validation de retrieval sur tout le manuscrit. Les résultats négatifs,
notamment français/anglais, sont conservés. BM25 est le défaut avec un petit
dictionnaire d'expansion français–anglais, désactivable par --no-expansion.
Les trois baselines utilisent le corpus initial ; les trois variantes extended,
normalized et bilingual utilisent le corpus augmenté. Le gain bilingue est mesuré
sur un jeu de développement, pas un échantillon indépendant.

Pour refaire l'extraction secondaire et le benchmark :

```bash
.venv-research/bin/python corpus/extract_secondary.py
python3 rag/build_index.py
python3 -m rag.evaluation.evaluate
./verify.sh
```

Les scripts historiques `phase2_curate.py`, `phase2_reports.py` et
`phase2_handoff.py` sont bloqués pour éviter d'écraser les ajouts ultérieurs.
Les entrées éditoriales de la passe sont dans `iteration1_science.py`, les notes
et les cinq fichiers de chapitre ; ce script ne constitue pas une lecture automatique.
Les générateurs `iteration1_science.py` et `iteration1_finalize.py` sont désormais
bloqués pour préserver la révision monétaire. Ne pas les relancer pour vérifier le corpus.
Les fichiers antérieurs à cette passe sont archivés dans
`analysis/history/pre_iteration1/`. Toute révision du snapshot doit conserver
ancien statut, nouveau statut, preuve et justification.

Correction de provenance : QUESTION_RACINE commence page 2 et finit page 3.
Les rapports 05–19 restent historiques. Le rapport courant est
`analysis/24_money_compensation_scenarios.md` pour la révision monétaire ciblée;
`analysis/23_iteration1_report.md` reste historique. Les fiches sont dans `analysis/core_reviews/`
et `analysis/chapters/`. Les références et leur profondeur d'accès sont dans
`bibliography/initial_research_library.json`. Les résultats empiriques reproduits
ne valident pas les équations ni le système complet de Campergue.

## Révision monétaire ciblée

32 entrées de scénarios à plusieurs niveaux; 41 claims existants revus, 25 ajoutés
(93 au terme de cette passe monétaire). Le finding précédent est classé OVER_SIMPLIFIED, pas simplement
inversé. Les journaux `money_*revision_log.json` et l’archive
`analysis/history/pre_money_review/` conservent les états antérieurs.
Les scripts `money_review.py` et `money_review_finalize.py` documentent la compilation
éditoriale initiale et refusent l’écrasement; ils ne remplacent pas une lecture humaine.
`./verify.sh` découvre automatiquement les tests de `tests/corpus/test_money_review.py`.
La vérification des tableaux-images repose sur des transcriptions manuelles localisées,
pas sur une citation prétendument extraite. La couverture et les ambiguïtés scientifiques
restent WARNING; les incohérences techniques restent FAIL.

## Reconstruction productive ciblée

État au terme de la passe productive :113 claims,20 mécanismes PM,20 fiches de formules et sept chapitres
analysés à des profondeurs inégales. Lecture ciblée, pas exhaustivité revendiquée.
Voir `analysis/25_productive_review_report.md`, `25_productive_mechanism.md` et
`26_cost_price_transmission.md`; CH06/CH07 restent UNCERTAIN.

`./verify.sh` exécute désormais aussi `analysis/run_productive_checks.py` et découvre
huit tests additionnels. Cinq calculs formels sont reproduits et un diagnostic des
données est exécuté; trois protocoles causaux restent NOT_IDENTIFIABLE_WITH_CURRENT_DATA.
Les résultats sont dans `analysis/empirical/productive/results.json`.
Les générateurs éditoriaux `productive_review.py` et `productive_finalize.py` refusent
les écrasements; les états antérieurs sont dans `analysis/history/pre_productive_review/`.
Les deux nouvelles références sont vérifiées au niveau des métadonnées et résumés
primaires; aucune reproduction de leurs données n’est revendiquée.

## Énergie indépendante et CH-08 à CH-10

État courant :127 claims,247 pages examinées, dix chapitres ayant une première
analyse à des profondeurs inégales. CH-08/09/10 restent UNCERTAIN.
Voir `analysis/27_energy_data_independence.md`, `27_energy_results.md`,
`28_aggregation_review.md`, `29_agents_markets_review.md`, `29_notation_cycles.md`.

Les trois expériences E1/E2/E3 sont descriptives, non causales. Une archive OWID
2025 est figée par commit/SHA, avec le traitement amont et la convention énergétique.
Le rapport27 corrige l'idée trop forte qu'une reconstruction par ratio PIB/énergie
rendrait nécessairement toute association tautologique. Les sorties antérieures
sont préservées; l'énergie directement acquise constitue une nouvelle confrontation.

```bash
# Acquisition initiale seulement : réseau requis, téléchargement figé, pas d'écrasement.
.venv-research/bin/python analysis/acquire_independent_energy.py
# Reproduction locale avec comparaison aux résultats archivés : aucun réseau.
.venv-research/bin/python analysis/run_independent_energy.py --check
./verify.sh
```

`verify.sh` découvre aussi huit nouveaux contrôles dans `test_terminal_review.py`.
La couverture partielle, les ambiguïtés T/dT, les conditions d'agrégation et
l'absence d'identification causale restent WARNING, pas FAIL. Une divergence
numérique ou une provenance cassée reste FAIL. Les générateurs éditoriaux
`energy_review_integrate.py` et `energy_review_finalize.py` sont protégés contre
la réexécution; ils ne sont pas une lecture automatisée. Les états antérieurs sont
dans `analysis/history/pre_energy_review/`. Le premier essai de régression ayant
détecté une métrique de couverture non synchronisée est également conservé.
# Passe microéconomique — électricité et agrégation

Protocole préalable : [31](analysis/31_micro_test_design.md), puis sélection et amendement distincts ; unités : [32](analysis/32_dimensional_consistency.md) ; expérience synthétique : [33](analysis/33_two_product_aggregation_test.md) ; résultats et cinq prédictions conditionnelles : [34](analysis/34_micro_empirical_results.md).

Cas États-Unis2001–2023, EIA et BLS. Snapshots textuels sous `analysis/empirical/micro_electricity/source/`, URL et SHA dans manifest.json. `analysis/acquire_micro_electricity.py` décrit l’acquisition publique ; les sources en ligne peuvent être révisées, donc les résultats sont reproduits depuis les snapshots conservés, sans connexion. Le protocole initial est verrouillé par SHA ; les changements de sélection sont documentés séparément.

Avec les dépendances déjà installées :

```bash
.venv-research/bin/python analysis/run_micro_electricity.py --check
.venv-research/bin/python analysis/run_two_product_aggregation.py --check
./verify.sh
```

Ces deux vérifications sont désormais intégrées à verify.sh. Un benchmark existant est comparé, jamais remplacé implicitement. Les résultats sont **NON_DISCRIMINATING** ; la chaîne complète est **NOT_IDENTIFIABLE**. Coût combustible construit ≠ coût total ; prix moins ce proxy ≠ profit ; fiabilité ≠ Utility ; économie budgétaire ≠ Money. Le jouet à deux produits est formel et synthétique. Claims inchangés127, couverture inchangée247/562. Les avertissements scientifiques ne sont pas des erreurs d’infrastructure. Les fichiers de contrôle antérieurs sont préservés dans `analysis/history/pre_micro_review/`.
