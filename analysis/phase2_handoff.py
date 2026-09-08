"""Snapshot the actual partial state, test results and exact research file changes."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())

MODIFIED=[
 'README_RESEARCH.md','analysis/02_root_question.md','analysis/data/claims.jsonl',
 'analysis/data/concepts.json','analysis/data/argument_graph.json',
 'rag/build_index.py','rag/query.py','rag/index/manifest.json','verify.sh']
UNCHANGED={
 'analysis/00_file_inventory.tsv','analysis/00_git_status.txt','analysis/00_hashes.txt',
 'analysis/00_repository_inventory.json','analysis/00_repository_inventory.md',
 'analysis/01_pdf_extraction_report.md','analysis/05_argument_graph.md',
 'analysis/06_research_chapters.md','analysis/09_root_question_answer.md',
 'rag/index/chunks.json'}

def main():
    progress=load('analysis/data/phase2_progress.json')
    if progress.get('status')=='SUFFICIENT_FOR_ITERATIVE_RESEARCH':
        raise SystemExit('Historical handoff frozen; current policy no longer blocks on coverage.')
    graph=load('analysis/data/graph_audit.json')
    chapters=load('analysis/data/research_chapters.json')
    tests=load('validation/phase2_regression_results.json')
    rag=load('rag/evaluation/results.json')
    files=set()
    for directory in ['analysis','rag','tests','validation']:
        files|={str(p.relative_to(ROOT)) for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    files|={'.gitignore','requirements.txt','validation/phase2_files.json','analysis/19_phase2_handoff.md'}
    created=sorted(files-set(MODIFIED)-UNCHANGED)
    manifest=dict(created=created,modified=sorted(MODIFIED),unchanged_rebuilt=['rag/index/chunks.json'],
        note='Modified means relative to phase 1 artifacts, even though these are still untracked in Git. Python bytecode caches excluded.')
    (ROOT/'validation/phase2_files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    status=subprocess.check_output(['git','status','--short','--branch'],cwd=ROOT,text=True)
    crit=progress['criticality']; types=progress['types']
    text=f'''PHASE 2 STATUS

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

total : {progress['claims']}
CORE : {crit.get('CORE',0)}
MAJOR : {crit.get('MAJOR',0)}
SUPPORTING : {crit.get('SUPPORTING',0)}
PERIPHERAL : {crit.get('PERIPHERAL',0)}

CLAIM TYPES

'''+ '\n'.join(f'{k} : {v}' for k,v in sorted(types.items()))+f'''

ARGUMENT GRAPH

nodes : {graph['nodes']}
edges : {graph['edges']}
cycles détectés : {len(graph['cycles'])}
orphans (nœuds isolés) : {len(graph['orphans'])}
Orphelins de chapitre parmi les claims enregistrés : 0.

RESEARCH CHAPTERS

10 candidats provisoires ; classification définitive non établie.

'''+ '\n'.join(f"{ch['id']} : {ch['title']}" for ch in chapters)+'''

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
'''
    for method,run in rag['methods'].items():
        text+='| '+method+' | '+' | '.join(f'{run["metrics"][k]:.4f}' for k in ['Recall@1','Recall@3','Recall@5','MRR'])+' |\n'
    text+=f'''
BM25 devient le défaut, mais Recall@5 français = 0 sur les six questions.
Le corpus anglophone n'est pas rendu multilingue par ce changement.

REGRESSION

tests PASS : {tests['passed']}
tests FAIL : {tests['failed']}
errors : {tests['errors']}
skipped : {tests['skipped']}
total : {tests['tests_run']}
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

'''+ '\n'.join('- '+p for p in created)+'\n\nModifiés par rapport à la phase 1 :\n\n'+ '\n'.join('- '+p for p in sorted(MODIFIED))+'''

GIT STATUS

```text
'''+status+'''
```

Aucun commit ni push effectué. Les sources PDF restent inchangées.

READY_FOR_BIBLIOGRAPHIC_ADVERSARIAL_REVIEW = NO
'''
    (ROOT/'analysis/19_phase2_handoff.md').write_text(text)

if __name__=='__main__':main()
