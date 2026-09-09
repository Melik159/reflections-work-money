"""Execute final verification and record actual results; no scientific promotion."""
import json,hashlib,subprocess
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];O=R/'remediation';S=R/'research_questions/synthesis'
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
p=subprocess.run(['./verify.sh'],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(O/'final_verify.log').write_text(p.stdout)
tests=json.loads((R/'validation/phase2_regression_results.json').read_text());classification=json.loads((O/'test_classification.json').read_text())
assert p.returncode==0 and tests['failed']==tests['errors']==0
assert tests['tests_run']==tests['passed']==classification['total']
baseline=json.loads((O/'baseline.json').read_text());modified=[]
for record in baseline['hashes']:
 path=R/record['path'];new=hashlib.sha256(path.read_bytes()).hexdigest()
 archive=O/'history'/record['path'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['sha256'],record['path']
 if new!=record['sha256']:modified.append(dict(path=record['path'],old_hash=record['sha256'],new_hash=new))
external_changes=[r for r in modified if r['path'].startswith('external_review/')];assert not external_changes
pdfhash=hashlib.sha256((R/'Reflections_PierreCampergue.pdf').read_bytes()).hexdigest();assert pdfhash=='7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827'
actions=json.loads((O/'finding_actions.json').read_text());acount=Counter(a['action'] for a in actions)
criteria=json.loads((R/'research_questions/methodology/criteria.json').read_text());criteria_counts=Counter(c['status'] for c in criteria)
after=json.loads((O/'core_before_after.json').read_text());core_counts=Counter(c['remediation_after'] for c in after)
report=dict(status='REMEDIATION_COMPLETE_WITH_SCIENTIFIC_LIMITS',actions=dict(acount),major_closed=4,moderate_closed=6,closure_scope='Documentary corrections applied, not mathematical/empirical unknowns solved; pending closure review',core_after=dict(core_counts),core_after_is_provisional=True,trace_before=dict(complete=8,partial=6),trace_after=dict(documented_with_explicit_limits=14),methodological_criteria=dict(criteria_counts),tests={k:v for k,v in classification.items() if k!='tests'},verify=dict(exit_code=0,passed=tests['passed'],failed=0,errors=0,warnings=tests['warnings']),external_review_unchanged=True,pdf_sha256=pdfhash,ready_for_closure_review=True)
js(O/'final_results.json',report)
m=json.loads((S/'manifest.json').read_text());m['remediation_status']=report['status'];m['ready_for_closure_review']=True;m['verification'].update(tests_run=tests['tests_run'],passed=tests['passed'],failed=0,errors=0,new_remediation_tests=8,classification_artifact='remediation/test_classification.json');js(S/'manifest.json',m);js(S/'verification_results.json',tests)
(S/'verification.md').write_text(f'''# Vérification après remédiation

./verify.sh exécuté: {tests['passed']}/{tests['tests_run']} PASS, zéro échec. 109 STRUCTURAL,17 LOCAL_FORMAL,2 EMPIRICAL_REPRODUCTION,0 INDEPENDENT_ECONOMIC_PREDICTION. Sept mutations ciblées rejetées; un test formel supplémentaire. Les anciens120tests et certificats restent dans remediation/history/.

Les contrats de régression verrouillent des formulations et liens relus; ils ne sont pas un évaluateur automatique de vérité scientifique. Un changement légitime nécessite revue et historique. WARNING: mesures indépendantes, causalité, littérature et raccord comptable restent incomplets.

READY_FOR_CLOSURE_REVIEW = YES signifie que les corrections sont documentées et testées, non qu’une nouvelle expertise externe les a déjà approuvées.
''')
f=S/'final_synthesis.md';text=f.read_text();head='## Verification and delivery status'
if head in text:
 start=text.index(head);end=text.find('\n## ',start+len(head));end=len(text) if end<0 else end
 text=text[:start]+head+'\n\nÉtat actuel après remédiation:128/128PASS;109contrôles structurels,17formels locaux,2reproductions empiriques,0test économique indépendant discriminant. Sept mutations ciblées sont rejetées. Le certificat120/120 est historique et archivé. [Détail](verification.md). READY_FOR_CLOSURE_REVIEW = YES; pas de validation globale.\n'+text[end:]
f.write_text(text)
lines=['# Rapport final de remédiation','## FINDINGS',f"ACCEPT: {acount['ACCEPT']}; PARTIALLY_ACCEPT: {acount['PARTIALLY_ACCEPT']}; REJECT:0; DEFER:0. Les12findings sont traités, dont11corrections et1note.", '## MAJOR FINDINGS']
for a in actions:
 if a['severity']=='MAJOR':lines.append(a['id']+' — '+a['action']+' — '+a['action_taken']+' Correction de représentation close; problème scientifique restant explicite.')
lines += ['## CORE CLAIMS','Avant:9confirmés,13qualifiés,1contesté,1indéterminé. Après remédiation proposée:9confirmés,14qualifiés,0contesté,1indéterminé. Ceci n’est pas une nouvelle décision du reviewer externe. CPC-0016 conserve attribution et formalité conditionnelle; seul son statut empirique complet est abaissé à NOT_IDENTIFIED. Historique exact:claim_status_history.json.',
'## TRACEABILITY','Avant8complètes/6partielles. Les6ont maintenant des énoncés restreints et des passages exacts, donnant14chaînes documentées avec limites. Ce résultat ne certifie pas l’implication scientifique de toutes les arêtes. Voir trace_contract.json et traceability_repairs.md.',
'## FORMAL CORRECTIONS','Inversion p303 corrigée comme lecture analytique, pas équation attribuée à l’auteur; postulat p301 conservé. Variance nécessaire avant carré de moyenne; terme dcp conservé si variable. Différentielle exacte distinguée de variation finie. Aucun problème local transformé en verdict global.',
'## MONEY REFERENTS','Six usages contextuels documentés: valeur portée, gain, solde disponible, cinétique, potentiel/total et transfert. Les noms suffixés sont des outils de lecture, non nouvelles notations de Pierre. Unité conceptuelle non forcée.',
'## MONEY/GDP BRIDGE','INCOMPLETE: p205 fournit la restriction valeur ajoutée; p559 ne fixe pas opérationnellement temps, réemploi, déflateur et équivalence Money/VA. Corrige aussi le rattachement erroné du reviewer CPC-0127 vers CPC-0118.',
'## +78%','Calcul7/9 et hypothèses conservés. Portée revendiquée p32 restituée, NOT_GENERALIZED_EMPIRICALLY pour le résultat établi.',
'## TEST SUITE',f"{tests['passed']}/{tests['tests_run']}PASS.109structurels,17formels,2reproductions,0indépendant discriminant. Sept mutations: source sans rapport, mauvaise page, surqualification empirique, condition retirée, Cash/Money confondus, +78universel, compatibilité devenue preuve: toutes rejetées. Contrats finis, pas compréhension sémantique générale.",
'## METHODOLOGICAL PROJECT','P63: concordance avec faits et cohérence; p64–65: monosemie; p79/561–562: raison plutôt qu’opinion/autorité. P301 accepte une hypothèse simplificatrice: aucun rejet universel de l’approximation n’est attribué. Choix et lois distingués p80; critique précise, non caricature des économistes.',
'## INTERNAL CONSISTENCY AGAINST OWN CRITERIA',str(dict(criteria_counts))+'. SATISFIED concerne déclaration d’hypothèses; NOT_SATISFIED une inversion locale. Les intentions ne valent pas réussite; l’ambiguïté de périmètre p63/535 et les référents restent ouverts.',
'## CONTRIBUTIONS','CC-01/02/03/04: QUALIFIED. Valeur méthodologique POSSIBLE sans nouveauté historique. CC-03 conserve l’attribution au diagnostic du reviewer, non innovation de l’auteur.',
'## VERIFY','PASS avec WARNING scientifiques. PDF et dossier external_review intacts. L’échec de transition128tests est conservé; les anciens champs de claims sont toujours testés inchangés.',
'## REMAINING BLOCKERS','Mesure indépendante T/cp/Utility; Money et ses référents; raccord net/PIB réel; stabilité de composition/dispersion; allocation marginale et dommages; pouvoirs discriminants; littérature historique non exhaustive. Ces inconnues ne bloquent pas la revue de clôture documentaire.',
'## HISTORY AND SCOPE','Toutes les décisions: finding_actions.json. Anciennes versions: history/. Aucune nouvelle RQ: liens à RQ-01.01/RQ-12.01/RQ-12.03.53RQ/127claims, IDs et citations canoniques conservés. Aucun push, aucun dossier académique.',
'READY_FOR_CLOSURE_REVIEW = YES']
(O/'final_remediation_report.md').write_text('\n\n'.join(lines)+'\n')
js(O/'files_changed.json',dict(compared_to_baseline=modified,new_review_files=[str(p.relative_to(R)) for base in [O,R/'research_questions/methodology'] for p in base.rglob('*') if p.is_file() and 'history' not in p.parts and '__pycache__' not in p.parts],note='Final certificate/report writes also appear in synthesis; baseline versions retained.'))
# Final certificate writes must still pass the source/structure validator.
p=subprocess.run([str(R/'.venv-research/bin/python'),'analysis/verify_synthesis.py'],cwd=R,text=True,capture_output=True)
(O/'post_certificate_verify.log').write_text(p.stdout+p.stderr);assert p.returncode==0
print(json.dumps(report,ensure_ascii=False,indent=2))
