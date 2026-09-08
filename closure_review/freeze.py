import json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];O=R/'closure_review'
assert not (O/'baseline.json').exists()
paths=set()
for base in ['research_questions','analysis/data','external_review','remediation','tests/corpus']:
 for p in (R/base).rglob('*'):
  if p.is_file() and not any(x in p.parts for x in ['history','__pycache__']) and p.suffix in ['.md','.json','.jsonl','.csv','.py']:paths.add(p)
paths.update([R/'verify.sh',R/'Reflections_PierreCampergue.pdf',R/'analysis/verify_synthesis.py'])
records=[dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths)]
b=dict(date=datetime.now(timezone.utc).isoformat(),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip(),git_status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=R,text=True),hashes=records,claims=127,questions=53,tests=json.loads((R/'validation/phase2_regression_results.json').read_text()),core=json.loads((R/'remediation/core_before_after.json').read_text()))
assert b['branch']=='research/corpus-validation'
(O/'baseline.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
(O/'00_baseline.md').write_text(f"# Baseline de clôture\n\nDate {b['date']}; commit {b['commit']}; branche {b['branch']}.127claims,53questions; dernier résultat enregistré {b['tests']['passed']}/{b['tests']['tests_run']}PASS (sera réexécuté). CORE proposé9/14/1/0. État Git exact et {len(records)}empreintes dans baseline.json. Le commit seul ne fige pas les nombreux fichiers non suivis.\n\nRéférences: research_questions/synthesis/final_synthesis.md; external_review/final_external_review.md; remediation/final_remediation_report.md. Aucun PDF modifié, aucun push.\n")
