import json,hashlib,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];O=R/'remediation'
assert not (O/'baseline.json').exists(),'Baseline already exists'
paths=[p for base in ['research_questions/synthesis','research_questions/operationalization','external_review','analysis/data','tests/corpus'] for p in (R/base).glob('*') if p.is_file()]
paths += [R/'verify.sh',R/'analysis/verify_synthesis.py']
records=[]
for p in paths:
 rel=p.relative_to(R);dst=O/'history'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
 records.append(dict(path=str(rel),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
p=subprocess.run(['./verify.sh'],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(O/'baseline_verify.log').write_text(p.stdout)
b=dict(date=datetime.now(timezone.utc).isoformat(),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),git_status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=R,text=True),hashes=records,verify_exit=p.returncode,tests=json.loads((R/'validation/phase2_regression_results.json').read_text()),corrections=json.loads((R/'external_review/proposed_corrections.json').read_text()),core_before=json.loads((R/'research_questions/synthesis/core_claims.json').read_text()))
(O/'baseline.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
(O/'00_baseline.md').write_text(f"# Baseline de remédiation\n\nCommit {b['commit']}; branche research/corpus-validation. Onze corrections ER-001–011 et note ER-012. Empreintes, état Git exact, statuts CORE et copies récupérables: baseline.json et history/.\n\nverify avant modification: {b['tests']['passed']}/{b['tests']['tests_run']} PASS; code {p.returncode}. Aucun push; PDF intacts.\n")
assert p.returncode==0
