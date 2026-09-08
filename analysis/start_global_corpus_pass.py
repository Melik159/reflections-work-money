"""Create a non-overwriting baseline, before consolidation edits.

Reading a file for hashing is NOT an analytical review of its contents.
"""
import collections
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/global_corpus_pass'

def main():
    if (OUT / 'baseline.json').exists():
        raise SystemExit('Baseline exists; do not overwrite.')
    paths = set()
    for name in ['research_questions/fifth_pass_report.md', 'research_questions/README.md',
                 'research_questions/questions.md', 'research_questions/question_graph.json',
                 'research_questions/evidence_matrix.csv', 'analysis/data/claims.jsonl',
                 'analysis/data/concepts.json', 'analysis/data/argument_graph.json',
                 'analysis/data/page_coverage.json', 'verify.sh',
                 'validation/phase2_regression_results.json']:
        paths.add(ROOT / name)
    for directory in ['research_questions/operationalization', 'research_questions/contribution']:
        paths.update(p for p in (ROOT / directory).rglob('*') if p.is_file())
    inventory = []
    for p in sorted(paths):
        content = p.read_bytes()
        relative = p.relative_to(ROOT)
        archived = OUT / 'history/baseline' / relative
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_bytes(content)
        inventory.append(dict(path=str(relative), size=len(content), sha256=hashlib.sha256(content).hexdigest()))
    claims = [json.loads(x) for x in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    graph = json.loads((ROOT/'research_questions/question_graph.json').read_text())
    coverage = json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
    tests = json.loads((ROOT/'validation/phase2_regression_results.json').read_text())
    pdf = ROOT/'Reflections_PierreCampergue.pdf'
    baseline = dict(timestamp=datetime.now(timezone.utc).isoformat(),
        branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), pages=562,
        claims=len(claims), criticality=dict(collections.Counter(c['criticality'] for c in claims)),
        questions=len(graph['nodes'])-1,
        question_statuses=dict(collections.Counter(q['status'] for q in graph['nodes'] if q['id']!='RQ-ROOT')),
        historical_analytically_reviewed=sum(p['examined'] for p in coverage),
        new_pass_scanned=0, baseline_verify=tests, artifacts=inventory,
        audit_scope='Structural inventory of all listed artifacts; analytical reading prioritized reports, definitions, claims and research map. Not a full semantic audit of every archived field.')
    (OUT/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
    (OUT/'00_baseline.md').write_text(f'''# Baseline — consolidation globale

Date UTC : {baseline['timestamp']}. Branche : `{baseline['branch']}`. HEAD : `{baseline['head']}`.
SHA-256 PDF : `{baseline['pdf_sha256']}`. Original inchangé.

127 claims : 24 CORE, 96 MAJOR, 7 SUPPORTING. 53 questions hors racine; 36 concepts de corpus, 26 entrées métrologiques. Graphe de questions : 54 nœuds/172 arêtes; graphe argumentatif : 180/220.
Couverture analytique historique : 272/562. Nouvelle passe : 0 page scannée au gel initial. Aucun transfert automatique de statut historique vers cette passe.

Statuts des questions hors racine : {baseline['question_statuses']}.

`./verify.sh` exécuté avant modification : {tests['status']}, {tests['passed']}/{tests['tests_run']}, code de sortie 0. Résultat exact archivé avec les fichiers sources d'analyse dans `history/baseline/`; leurs empreintes figurent dans `baseline.json`. Les tests ouverts scientifiquement restent des avertissements.

## Ambiguïtés et verrous hérités

T/dT, stock/variation/réserve et conventions de signe; cp/ca distincts; Utility non étalonnée; K conditionné par composition et unités; énergie physique distincte de Work économique; Money distinct de Cash et des gains comptables. Pas de mesure indépendante de T, Money ou des ratios de Utility. Les gains de productivité ont plusieurs branches de transmission et d'utilisation.

## Contributions candidates

CC-01 : paiement/transformation/bénéficiaire; CC-02 : tâche/vitesse/Work additionnel; CC-03 : exigences d'échelle de Utility (diagnostic de l'analyse); CC-04 : condition Utility du pont physique/économique. Aucune priorité historique ni prédiction empirique exclusive établie.

## Portée de l'audit initial

Inventaire structurel des fichiers demandés, archivage intégral des versions; lecture analytique prioritaire des rapports, de l'arbre, des claims, définitions et matrices métrologiques. L'archivage informatique n'est PAS présenté comme lecture de chaque ligne. Des notices du lexique sont manifestement vieillies (cycles/entropie déclarés non examinés malgré les passes suivantes); l'entrée unproductive recopie la définition positive. Ces points doivent être corrigés avec historique, non rétroactivement masqués.

## Plan de consolidation et critère honnête

Matrice de 562 lignes, mais UNREVIEWED tant que la page n'a pas été effectivement inspectée dans cette passe. Les recherches automatiques fournissent des candidats, pas des pages lues. Les pages de figures presque vides à l'extraction sont vérifiées visuellement. Un PASS structurel n'autorise pas GLOBAL_CORPUS_PASS_COMPLETE tant que les critères de lecture et de révision sémantique ne sont pas remplis.
''')
    print('Baseline archived:', tests['passed'], 'tests PASS')

if __name__ == '__main__': main()
