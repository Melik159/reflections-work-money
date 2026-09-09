"""Review completion checks; no edits outside external_review."""
import hashlib,json,subprocess,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'external_review'
def read(p):return json.loads((O/p).read_text())
def save(p,v):(O/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
b=read('baseline.json')
checks={}
core=read('core_claim_review.json');variables=read('measurement_review.json')
checks['24_core_unique']=len(core)==len({c['id'] for c in core})==24
checks['26_variables_unique']=len(variables)==len({v['id'] for v in variables})==26
checks['120_tests_classified']=read('test_audit.json')['total']==120
checks['14_conclusions']=len(read('traceability.json'))==14
checks['4_candidates']=len(read('candidate_review.json'))==4
checks['findings_have_evidence']=all(f['evidence'] and f['recommended_correction'] and f['charity_test'] for f in read('findings.json'))
checks['core_have_source_context']=all(c['source']['quotation'] and c['context_pages'] for c in core)
checks['all_frozen_files_unchanged_before']=all(hashlib.sha256((R/h['path']).read_bytes()).hexdigest()==h['sha256'] for h in b['hashes'])
p=subprocess.run(['./verify.sh'],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(O/'final_verify.log').write_text(p.stdout)
checks['verify_exit_zero']=p.returncode==0
checks['all_frozen_files_unchanged_after']=all(hashlib.sha256((R/h['path']).read_bytes()).hexdigest()==h['sha256'] for h in b['hashes'])
result={'checks':checks,'review_checks_pass':sum(checks.values()),'review_checks_fail':sum(not x for x in checks.values()),'verify_exit':p.returncode,'frozen_files':len(b['hashes']),'verification_log':'external_review/final_verify.log','note':'Review structural checks are not scientific proofs.'}
save('final_verification.json',result)
s=read('review_summary.json');s['verification']='PASS' if all(checks.values()) else 'FAIL';s['ready_for_remediation']=all(checks.values());save('review_summary.json',s)
(O/'verification_status.md').write_text('# Final verification\n\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
