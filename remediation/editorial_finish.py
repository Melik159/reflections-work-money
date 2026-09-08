import json,csv,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'remediation';S=R/'research_questions/synthesis'
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
failure=json.loads((R/'validation/phase2_regression_results.json').read_text())
if failure['failed'] and not (O/'first_test_failure.json').exists():js(O/'first_test_failure.json',failure)
# Preserve exact input snapshots for new reviewer-owned validation code too.
records=json.loads((S/'input_manifest.json').read_text())
for path in ['remediation/trace_contract.json','remediation/validate_contracts.py','research_questions/methodology/criteria.json','research_questions/methodology/epistemic_program.md']:
 if path not in {r['path'] for r in records}:records.append(dict(path=path,sha256=hashlib.sha256((R/path).read_bytes()).hexdigest()))
js(S/'input_manifest.json',records)
# Reconcile measurement references in current question/matrix views, without changing statuses.
variables=json.loads((R/'research_questions/operationalization/variables.json').read_text())
qs=json.loads((S/'questions.json').read_text())
for q in qs:
 vals=[f"{v['id']} {v['name']}: L{v['measurement_level']} {v['measurement_status']}" for v in variables if q['id'] in v['dependent_questions']]
 if vals:q['measurement_maturity']=vals
js(S/'questions.json',qs)
for name,key in [('question_synthesis.csv','id'),('master_matrix.csv','Item')]:
 with (S/name).open() as f:rows=list(csv.DictReader(f))
 for row in rows:
  q=next((q for q in qs if q['id']==row[key]),None)
  if q:row['measurement_maturity' if key=='id' else 'Measurement maturity']='; '.join(q['measurement_maturity'])
 with (S/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for name in ['final_synthesis.md','root_question_answer.md','negative_results.md']:
 p=S/name;text=p.read_text()
 banner='> ÉTAT APRÈS REMÉDIATION : les qualifications explicites ci-dessous actualisent les formulations historiques. CPC-0016 : NOT_IDENTIFIED pour la chaîne complète. Source et intention de l’auteur restent distinctes de la portée retenue.\n\n'
 if not text.startswith(banner):p.write_text(banner+text)
actions=json.loads((O/'finding_actions.json').read_text())
mapping={1:['research_questions/synthesis/final_synthesis.md','research_questions/methodology/epistemic_program.md'],2:['remediation/money_gdp_bridge.md','research_questions/synthesis/results.json'],3:['remediation/money_referents.json','research_questions/operationalization/variables.json'],4:['remediation/formal_corrections.json','research_questions/synthesis/results.json'],5:['remediation/formal_corrections.json','research_questions/synthesis/results.json'],6:['research_questions/operationalization/variables.json'],7:['research_questions/operationalization/variables.json','research_questions/operationalization/experiments.json'],8:['analysis/verify_synthesis.py','remediation/validate_contracts.py','tests/corpus/test_remediation.py'],9:['analysis/data/claims.jsonl','research_questions/synthesis/core_claims.json'],10:['analysis/data/claims.jsonl','research_questions/synthesis/results.json'],11:['analysis/data/claims.jsonl','research_questions/synthesis/core_claims.json'],12:['research_questions/synthesis/contributions.json','research_questions/synthesis/contributions.md']}
for a in actions:a['files_modified']=mapping[int(a['id'][3:])]
js(O/'finding_actions.json',actions)
# Current verdict is an administrative remediation assessment, not a new external review.
before=json.loads((R/'external_review/core_claim_review.json').read_text())
after=[]
for c in before:
 after.append(dict(id=c['id'],external_before=c['reviewer_status'],remediation_after='REVIEWER_QUALIFIES' if c['id']=='CPC-0016' else c['reviewer_status'],scope='Provisional remediation assessment; original external verdict unchanged; closure reviewer must recheck.'))
js(O/'core_before_after.json',after)
(O/'execution_notes.md').write_text('''# Historique d’exécution

Baseline:120/120PASS. Le premier contrôle du nouveau validateur a échoué sur un chemin d’import; chemin du dépôt rendu explicite. Première exécution complète des tests unitaires:127/128, un contrôle historique exigeait encore l’égalité binaire des claims. Le contrôle vérifie désormais tous les champs antérieurs inchangés et l’historique des ajouts; aucune assertion de provenance n’a été retirée sans remplacement. Résultat initial conservé dans first_test_failure.json.

Les nouveaux contrats verrouillent un ensemble fini d’énoncés relus et leurs passages. Ils ne résolvent PAS la compréhension sémantique générale; ils rendent détectables les mutations demandées. Une nouvelle conclusion légitime exige une revue et un historique, pas une mise à jour automatique du contrat. verify.sh ne rafraîchit pas les empreintes d’entrée: seul le script explicite de remédiation le fait, en historisant chaque changement.

Les verdicts externes restent inchangés dans external_review/. Le reclassement post-remédiation de CPC-0016 est proposé pour contrôle de clôture, non nouvelle expertise externe.
''')
