# Iteration report — première livraison

CYCLES COMPLETED: 3/10. INITIAL_SERIES_PARTIAL : les sept autres cycles thématiques ne sont pas exécutés. Le plafond de dix n'est pas présenté comme dix analyses terminées.

CLAIMS CHANGED: 0. QUESTIONS CHANGED: 0. Aucun nouveau statut de vérité ni synthèse globale.

NEW DISPUTES: 1 objet de suivi (DISPUTE-0001), réenregistrant une ambiguïté connue; 0 contradiction scientifique nouvelle. DISPUTES RESOLVED: 0.

NEW EVIDENCE: 0 donnée empirique, 0 nouvelle preuve corpus, 1 diagnostic de bilan synthétique conditionnel et 2 contrôles de schémas métrologiques. Les invariances de T/Utility déjà dans EXP-09/EXP-02 ne sont pas recomptées.

NEW TESTS: 8 (7 structurels/provenance/métadonnées et 1 bilan formel local). La baseline conserve ses 128 tests: 109 structurels, 17 formels locaux, 2 reproductions, 0 économique indépendant discriminant. Les 136 contrôles ne sont pas 136 preuves scientifiques.

CANDIDATE DISCRIMINATING RESULTS: 0. Tous les résultats de cette livraison sont NON_DISCRIMINATING.

## Cycles et résultats

- CYCLE-001: retour PDF204–208,254–258,466–469. La condition sans pertes est explicite; bilan fermé et gain économique ne sont pas synonymes. Frontière/étalon et raccord des composantes restent ouverts.
- CYCLE-002: PDF201–210 et EXP-09. Filtre de protocole rejetant T construit par sa loi cible; aucun étalonnage indépendant fourni. BLOCKED_BY_MEASUREMENT.
- CYCLE-003: PDF108–111,384–387 et EXP-02. Filtre exigeant une calibration commune pour le quotient; un ordre ou deux échelles non raccordées sont insuffisants. BLOCKED_BY_MEASUREMENT.

Les protocoles sont figés avant exécution; les résultats et journaux sont conservés dans cycles/. Les rôles sont simulés, pas indépendants. Les nouvelles tâches scientifiques bloquées sont distinctes des tâches documentaires DONE.

## Coverage improvement

27 pages réellement relues; trois contrôles visuels d'équations. Pages nouvelles par rapport au drapeau analytique courant: [254, 258]. Aucun 562/562 approfondi revendiqué. Couverture gelée conservée, supplément dans coverage_overlay.json. Audit de sous-utilisation limité aux citations directes des claims; fréquences de sections/formules encore OPEN.

## RAG

Chunks: {'SOURCE_CORPUS': 1473, 'DERIVED_ANALYSIS': 5222, 'EXTERNAL_LITERATURE': 0}. SOURCE_CORPUS contient les trois PDF et les deux Markdown d'origine. DERIVED_ANALYSIS contient les rapports, claims, questions et ontologie. EXTERNAL_LITERATURE est vide: les notes bibliographiques internes ne sont pas reclassées comme textes externes.

| Méthode | Recall@1 | Recall@3 | Recall@5 | MRR@5 |
|---|---|---|---|---|
| baseline_bm25 | 0.5000 | 0.7424 | 0.8182 | 0.6303 |
| separated_bm25 | 0.5000 | 0.7424 | 0.8182 | 0.6303 |
| separated_tfidf | 0.4848 | 0.6818 | 0.8030 | 0.5980 |
| separated_hybrid | 0.4697 | 0.6667 | 0.8333 | 0.6061 |

66 questions, benchmark de développement existant, mêmes pages et passages attendus. Aucun gain imputable aux analyses internes. Fusion lexicale meilleure à k=5 mais moins bonne au premier rang et en MRR; BM25 reste le défaut. Embeddings sémantiques NON EXÉCUTÉS (bibliothèque et modèle local absents); TF-IDF est seulement le fallback vectoriel lexical. Aucun reranker neuronal. Les niveaux PARAGRAPH/CLAIM_WINDOW et la collection dérivée ne bénéficient pas encore d'un golden set propre.

## Most important problems

- Une déclaration de calibration dans un formulaire ne prouve pas une calibration indépendante.
- La conservation postulée ne mesure pas la richesse ni le Money-gain.
- Les limites métrologiques existaient déjà : ne pas produire une fausse nouveauté par répétition des tests.
- Les collections dérivées contiennent des rapports historiques datés : leur conclusion n'est jamais une citation primaire et doit être confrontée à la version courante.
- Les hypothèses H1/H2/H3 de energy_growth_branch.md sont un plan de comparaison, pas encore des modèles économétriques identifiés.

## VERIFY

Chaque cycle DONE a exécuté ./verify.sh (128 PASS), huit nouveaux tests et le contrôle du manifeste gelé (PASS). Avertissements scientifiques conservés. Commande de relecture complète: bash research_state/verify.sh. Aucun push.

## Recommended next cycles

TASK-004 K; TASK-005 énergie utile; TASK-006 innovation; TASK-007 destination des gains; TASK-008 dommages; TASK-009 épistémologie; TASK-010 adversarial transversal. TASK-011/012 attendent une définition métrologique; TASK-013 complète le benchmark du RAG.
