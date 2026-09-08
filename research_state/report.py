"""Summarize executed cycles, without claiming unread coverage or scientific novelty."""
import csv
import json
from datetime import datetime,timezone
from research_state.cycle import S,ROOT,CONFIG,tasks,save_tasks,write,js

ts=tasks()
if not any(t['id']=='TASK-011' for t in ts):
    t=dict(ts[1]);t.update(id='TASK-011',priority=1,topic='Étalonnage indépendant T/cp',status='BLOCKED',created_from='CYCLE-002',
        required_sources=['research_state/calibration_protocols.md'],notes='NEEDS_DEFINITION; ajout de suivi après clôture documentaire du cycle, pas une mesure indépendante.')
    ts.append(t)
if not any(t['id']=='TASK-013' for t in ts):
    ts.append(dict(id='TASK-013',priority=8,topic='Retrieval multi-niveaux et embeddings',question='La recherche de passages et collections gagne-t-elle sur un jeu tenu à l’écart ?',
        related_rq=[],related_claims=[],pages_hint=[],required_sources=['research_state/rag_benchmark.json'],status='OPEN',created_from='Initial retrieval benchmark',
        notes='Golden set DERIVED_ANALYSIS et multi-niveaux manquant; modèle sémantique local non installé. Ne pas appeler TF-IDF embeddings sémantiques.'))
save_tasks(ts)
done=[c for c in CONFIG if next(t for t in ts if t['id']=='TASK-'+c['id'][-3:])['status']=='DONE']
pages=sorted({p for c in done for p in c['pages']})
old={r['page'] for r in json.loads((ROOT/'analysis/data/page_coverage.json').read_text()) if r.get('examined')}
js(S/'coverage_overlay.json',dict(pages_reread=pages,visual_pages=[207,386,468],new_to_analytical_flag=sorted(set(pages)-old),
    baseline_analytical_count=len(old),baseline_not_modified=True,meaning='Actual readings in this session; never inferred from retrieval hits or index building.'))
bench=json.loads((S/'rag_benchmark.json').read_text());counts=json.loads((ROOT/'rag/index/iterative.json').read_text())['collections']
rows='\n'.join(f"| {k} | {v['metrics']['Recall@1']:.4f} | {v['metrics']['Recall@3']:.4f} | {v['metrics']['Recall@5']:.4f} | {v['metrics']['MRR']:.4f} |" for k,v in bench['methods'].items())
text=f'''# Iteration report — première livraison

CYCLES COMPLETED: {len(done)}/10. INITIAL_SERIES_PARTIAL : les sept autres cycles thématiques ne sont pas exécutés. Le plafond de dix n'est pas présenté comme dix analyses terminées.

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

{len(pages)} pages réellement relues; trois contrôles visuels d'équations. Pages nouvelles par rapport au drapeau analytique courant: {sorted(set(pages)-old)}. Aucun 562/562 approfondi revendiqué. Couverture gelée conservée, supplément dans coverage_overlay.json. Audit de sous-utilisation limité aux citations directes des claims; fréquences de sections/formules encore OPEN.

## RAG

Chunks: {counts}. SOURCE_CORPUS contient les trois PDF et les deux Markdown d'origine. DERIVED_ANALYSIS contient les rapports, claims, questions et ontologie. EXTERNAL_LITERATURE est vide: les notes bibliographiques internes ne sont pas reclassées comme textes externes.

| Méthode | Recall@1 | Recall@3 | Recall@5 | MRR@5 |
|---|---|---|---|---|
{rows}

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
'''
write(S/'iteration_report.md',text)
with (S/'DECISIONS.md').open('a') as f:
    f.write(f'\n\nDEC-0005 — {datetime.now(timezone.utc).isoformat()}. Target: suivi de série. Ancien état: trois tâches documentaires seules. Nouvel état: protocoles de mesure manquants TASK-011/012 et benchmark TASK-013 explicités; sept cycles thématiques restent OPEN. Motif: ne pas assimiler DONE documentaire à mesure résolue. Sources: EXP-09/EXP-02, résultats des trois cycles; confiance HIGH sur le suivi, empirique LOW.\n')
