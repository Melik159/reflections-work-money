"""Independent review artifacts; never rewrites the internal synthesis."""
import argparse,ast,csv,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'external_review'
def write_json(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def freeze():
    if (OUT/'baseline.json').exists():raise SystemExit('Existing freeze: do not overwrite')
    paths=set((ROOT/'research_questions/synthesis').glob('*'))
    paths.update((ROOT/'tests/corpus').glob('test_*.py'))
    for s in ['analysis/data/claims.jsonl','analysis/data/concepts.json','analysis/data/argument_graph.json',
      'research_questions/question_graph.json','research_questions/operationalization/variables.json',
      'verify.sh','analysis/run_independent_energy.py','analysis/run_micro_electricity.py',
      'analysis/empirical/independent_energy/analysis_panel.csv','analysis/empirical/micro_electricity/panel.csv']:
        paths.add(ROOT/s)
    paths.update(ROOT.glob('*.pdf'));paths.update((ROOT/'articles').glob('*.pdf'))
    hashes=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(paths) if p.is_file()]
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    graph=json.loads((ROOT/'research_questions/question_graph.json').read_text())
    baseline=dict(timestamp=datetime.now(timezone.utc).isoformat(),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
      git_status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=ROOT,text=True),
      questions=len([n for n in graph['nodes'] if n['id']!='RQ-ROOT']),claims=len(claims),core=sum(c['criticality']=='CORE' for c in claims),hashes=hashes,
      independence_scope='Same assistant, explicit adversarial posture; not organizationally or person-independently peer reviewed.')
    write_json('baseline.json',baseline)
    result=subprocess.run(['./verify.sh'],cwd=ROOT,capture_output=True,text=True)
    (OUT/'baseline_verify.log').write_text(result.stdout+'\n'+result.stderr)
    tests=json.loads((ROOT/'validation/phase2_regression_results.json').read_text())
    baseline['verification']=dict(exit_code=result.returncode,tests=tests)
    baseline['synthesis_unchanged_after_verify']=all(hashlib.sha256((ROOT/h['path']).read_bytes()).hexdigest()==h['sha256'] for h in hashes if h['path'].startswith('research_questions/synthesis/'))
    write_json('baseline.json',baseline)
    (OUT/'00_review_baseline.md').write_text(f"""# État figé pour revue adversariale

Date UTC : {baseline['timestamp']}. Branche : `{baseline['branch']}`. Commit source : `{baseline['commit']}`.

Questions : {baseline['questions']}; claims : {baseline['claims']}; CORE : {baseline['core']}.

`./verify.sh` exécuté : code {result.returncode}; {tests['passed']}/{tests['tests_run']} PASS, {tests['failed']} FAIL, {tests['errors']} ERROR. Journal : baseline_verify.log.

Les empreintes SHA256, tailles et état Git **exact** sont dans baseline.json. Le commit seul ne fige pas le travail : les artefacts de recherche sont non suivis dans l'état Git. Leurs empreintes constituent ici la référence documentaire. Synthèse inchangée après verify : {baseline['synthesis_unchanged_after_verify']}.

La revue a une posture adversariale mais est conduite par le même assistant : ce n'est pas une expertise indépendante au sens institutionnel ou humain. Aucune modification de synthèse, aucun push. Les erreurs éventuelles de reconstruction seront distinguées des erreurs du manuscrit et des limites d'identification.
""")
    print(json.dumps(dict(exit_code=result.returncode,tests=tests['tests_run'],passed=tests['passed'],synthesis_unchanged=baseline['synthesis_unchanged_after_verify'])))
def pages(nums):
    data={p['page_pdf']:p['text'] for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    for n in nums:print(f'\n=== PDF PAGE {n} ===\n'+data[n])
def test_sources():
    for p in sorted((ROOT/'tests/corpus').glob('test_*.py')):
        source=p.read_text();tree=ast.parse(source)
        for cls in (n for n in tree.body if isinstance(n,ast.ClassDef)):
            for n in cls.body:
                if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'):
                    print(f'{p.name}:{n.lineno} {cls.name}.{n.name}')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['freeze','pages','tests']);p.add_argument('numbers',nargs='*',type=int);a=p.parse_args()
    if a.action=='freeze':freeze()
    elif a.action=='pages':pages(a.numbers)
    else:test_sources()
