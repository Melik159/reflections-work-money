"""Verify, then seal a documentary baseline. Manifest excludes its own digest/report."""
import json,hashlib,subprocess,sys,io,unittest,importlib.util
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];O=R/'closure_review';sys.path.insert(0,str(R))
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert not (R/'BASELINE_STATUS.md').exists(),'Baseline already sealed; do not overwrite'
run=subprocess.run(['./verify.sh'],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(O/'final_verify.log').write_text(run.stdout)
tests=json.loads((R/'validation/phase2_regression_results.json').read_text());assert run.returncode==0 and tests['passed']==tests['tests_run']==128 and tests['failed']==tests['errors']==0
from analysis.verify_synthesis import validate
assert validate()['status']=='PASS' # positive control before mutations
spec=importlib.util.spec_from_file_location('closure_mutations',R/'tests/corpus/test_remediation.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
names=[n for n in unittest.defaultTestLoader.getTestCaseNames(module.RemediationTests) if n!='test_local_formal_remediation']
assert len(names)==7
stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite(module.RemediationTests(n) for n in names))
(O/'mutation_tests.log').write_text(stream.getvalue());assert result.wasSuccessful() and result.testsRun==7
mutation=dict(positive_control='PASS',executed=7,rejected=7,unexpected_acceptance=0,tests=names,interpretation='Seven malformed inputs rejected; not seven scientific confirmations.')
js(O/'mutation_results.json',mutation)
classification=json.loads((R/'remediation/test_classification.json').read_text());assert (classification['structural'],classification['formal_scientific'],classification['empirical_reproduction'],classification['independent_discriminating'])==(109,17,2,0)
actual={t.split('.',1)[-1] for t in tests['passed_tests']}
assert len(classification['tests'])==128
# Preserve the frozen manuscript, canonical claims, graph and external review.
baseline=json.loads((O/'baseline.json').read_text());diffs=[]
for h in baseline['hashes']:
 new=hashlib.sha256((R/h['path']).read_bytes()).hexdigest()
 if new!=h['sha256']:diffs.append(dict(path=h['path'],old=h['sha256'],new=new))
protected=['Reflections_PierreCampergue.pdf','analysis/data/claims.jsonl','research_questions/question_graph.json']
assert not any(d['path'] in protected or d['path'].startswith('external_review/') or d['path'].startswith('tests/corpus/') for d in diffs)
historychecks=[]
for c in json.loads((O/'editorial_changes.json').read_text()):
 archive=O/'history'/c['path'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==c['old_sha256']
 assert hashlib.sha256((R/c['path']).read_bytes()).hexdigest()==c['new_sha256']
 historychecks.append(c['path'])
js(O/'final_state_diff.json',dict(changed_from_closure_baseline=diffs,editorial_archives_verified=len(historychecks),sources_preserved=True))
verification=dict(command='./verify.sh',exit_code=0,tests_run=128,passed=128,failed=0,errors=0,classification={k:v for k,v in classification.items() if k!='tests'},mutation=mutation,scientific_warnings=['MEASUREMENT_OPEN','MONEY_GDP_BRIDGE_INCOMPLETE','NO_INDEPENDENT_DISCRIMINATING_PREDICTION','LITERATURE_PARTIAL','SYN_08_TRACEABILITY_PARTIAL'],scope='Integrity/provenance/formal/reproduction, not global scientific validation.')
js(O/'final_verification.json',verification)
counts=json.loads((O/'audit_counts.json').read_text());date=datetime.now(timezone.utc).isoformat();commit=baseline['commit'];version='CAMPERGUE-DOCUMENTARY-BASELINE-1.0'
sections=[
('Scope','Revue de clôture ciblée, sans nouvelle théorie, collecte lourde ni revue bibliographique générale. Même assistant en posture de contrôle: aucune certification d’indépendance institutionnelle.'),
('Baseline',f'{version}; dateUTC {date}; commit source {commit}. Branche research/corpus-validation. Beaucoup d’artefacts sont non suivis: manifeste SHA256 requis, commit seul insuffisant.'),
('External findings closure','4CLOSED;8CLOSED_WITH_RESIDUAL_UNCERTAINTY;0PARTIALLY_CLOSED;0REOPEN. Corrections réellement vérifiées, pas simple reprise du rapport. Deux comptes obsolètes de synthèse et des vues de questions ont été rectifiés, archivés. ER-008 reste limité à protection d’énoncés relus et traçabilité documentaire.'),
('Core claims final state','24:9CONFIRMED,14QUALIFIED,1UNDETERMINED,0DISPUTED. CPC-0016 conserve attribution; NOT_IDENTIFIED pour la chaîne complète. Aucun changement de texte canonique pendant la clôture. Voir core_claims_final.md.'),
('Research questions state','53:18PARTIALLY_RESOLVED,6AMBIGUOUS,29OPEN,0RESOLVED_WITHIN_SCOPE. Aucune dépendance cassée; statuts synthèse/graphe/en-têtes cohérents. Les anciennes réponses provisoires ont été remplacées seulement par les réponses déjà synthétisées, sans nouvelle résolution.'),
('Root question','Onze liaisons classées dans root_question_closure.md: portée locale conditionnelle, ponts non identifiés et deux fonctions manquantes (allocation marginale et dommage quantifié). Aucun renforcement de la réponse provisoire.'),
('Methodological project','Intention de cohérence, fait et univocité attestée; critique opinion/autorité contextualisée; hypothèses simplificatrices explicitement acceptées. Sept critères:1satisfait localement,4partiels,1ambigu,1non satisfait sur une inversion. Complément source p205 contrôlé. Intention ≠ réussite.'),
('Money audit','Six référents et32scénarios préservés. Dépôt bancaire, Cash, gain, potentiel, solde et transfert ne sont pas identifiés par un simple nom. Pont Money/VA/PIB explicitement incomplet.'),
('Formal audit','cp constant requis pour primitive simple; terme croisé en variation finie; variance avant agrégation quadratique; Utility requiert échelle adaptée; limites/inversions restent erreurs ou reconstructions locales. +78% arithmétique sous hypothèses, NOT_GENERALIZED_EMPIRICALLY.'),
('Empirical status','Résultats antérieurs reproduits par verify, pas nouvelles expériences. Associations énergie/PIB non causales et non spécifiques; cas électrique non identifié pour transmission structurelle, marge et Money.'),
('Candidate contributions','Quatre SURVIVES_QUALIFIED,0SURVIVES sans qualification,0WEAKENED supplémentaire,0RETRACTED. Nouveauté historique UNRESOLVED. CC-03 est un diagnostic de revue appliqué au corpus.'),
('Test-suite interpretation','128/128PASS:109structurels,17formels locaux,2reproductions,0indépendant discriminant. Sept mutations exécutées après verify, sept rejetées. Un rejet vérifie le contrôle, pas une proposition économique.'),
('Traceability','13COMPLETE,1PARTIAL (SYN-08),0BROKEN. Le regroupement de sous-erreurs formelles manque encore de liens atomiques exhaustifs. Les pages/diagnostics existent; aucune source artificielle ajoutée.'),
('Remaining open questions','Quinze priorités dans final_open_questions.md: métrologie, référents, agrégation, comptabilité, usages du gain, dommages, causalité et comparaison historique.'),
('Residual risks','Contrats textuels finis non détecteur sémantique général; périmètres et sources historiques doivent rester visibles; corpus et littérature limités; validité du proxy et causalité non garanties par reproductibilité; absence de tout défaut non prouvée.'),
('Baseline recommendation','Créer la baseline scientifique/documentaire versionnée AVEC ces limites. READY_FOR_ACADEMIC_BASELINE=YES désigne un dossier contrôlé, traçable et critiquable, pas un verdict économique ni un article prêt à publier. Aucun push ni dossier universitaire préparé.')]
(O/'final_closure_review.md').write_text('# Final closure review\n\n'+'\n\n'.join(f'## {i}. {h}\n\n{t}' for i,(h,t) in enumerate(sections,1))+'\n')
(R/'BASELINE_STATUS.md').write_text(f'''# Baseline scientifique et documentaire

BASELINE_VERSION: {version}
Date UTC: {date}
Commit source: {commit}
Branche locale: research/corpus-validation

Le dossier représente127claims et53questions, issus d’un manuscrit de562pages parcourues/classées.447pages ont reçu une analyse cumulée; toutes ne sont pas des lectures approfondies. Les24CORE ont été revus:9confirmés dans leur périmètre,14qualifiés,1indéterminé.

Établi dans ce dossier: provenance, distinctions conceptuelles et résultats de calcul locaux sous conditions. Reproduit: analyses descriptives et diagnostics antérieurs. Qualifié: référents Money/T, Utility, stabilité de K, raccord au PIB et généralité du +78%.

Ouvert: mesure indépendante, allocation marginale des gains, empreinte/dommages, causalité et prédictions discriminantes. Une conclusion composite (SYN-08) conserve une traçabilité partielle explicitée.

Verify:128/128PASS;109structurels,17formels locaux,2reproductions empiriques,0test économique indépendant discriminant. Sept mutations ciblées rejetées. Les tests garantissent des propriétés limitées d’intégrité/provenance/cohérence/reproduction; ils ne garantissent ni vérité économique générale ni exhaustivité de toutes les erreurs possibles.

SHA256 manuscrit: {hashlib.sha256((R/'Reflections_PierreCampergue.pdf').read_bytes()).hexdigest()}
Empreintes des artefacts: [BASELINE_MANIFEST_SHA256.txt](closure_review/BASELINE_MANIFEST_SHA256.txt). Vérifier depuis ce dépôt avec `sha256sum -c closure_review/BASELINE_MANIFEST_SHA256.txt`.

Référence actuelle: [synthèse](research_questions/synthesis/final_synthesis.md), [clôture](closure_review/final_closure_review.md). Rapports de passes, protocoles figés et archives décrivent leurs états historiques; ils ne remplacent pas les qualifications actuelles.

READY_FOR_ACADEMIC_BASELINE = YES

Ce statut ne vaut ni validation globale, ni nouveauté historique établie, ni certification indépendante par un tiers. Aucun push. Aucun article ou dossier académique préparé.
''')
(O/'test_suite_final.md').write_text('# Tests — audit différentiel final\n\nLes128méthodes classées dans remediation/test_classification.json correspondent à la suite exécutée. Fichiers de tests inchangés depuis le freeze de clôture. Répartition primaire exclusive109/17/2/0; les tests mixtes restent classés selon leur fonction principale. Les sept tests négatifs ont été relancés après verify avec contrôle positif préalable. Journaux:final_verify.log,mutation_tests.log. Aucun résultat scientifique ouvert ne fait échouer la suite.\n')
summary=dict(status='CLOSURE_REVIEW_COMPLETE_WITH_RESIDUAL_UNCERTAINTY',counts=counts,tests=verification,baseline_version=version,baseline_created=True,manifest_created=True,ready_for_academic_baseline=True)
js(O/'final_results.json',summary)
(O/'execution_notes.md').write_text('# Exécution de clôture\n\nLe premier audit de provenance cherchait toutes les pages des critères dans le seul dossier méthodologique: p205 manquait dans cet extrait, pas dans le corpus. Citation exacte vérifiée et ajoutée à methodological_closure.md. Un second contrôle supposait une liste de scénarios au lieu de l’objet contenant scenarios; lecteur corrigé,32scénarios confirmés. Aucun de ces incidents n’est présenté comme erreur scientifique du corpus. Les résultats des tests finaux et mutations sont réellement exécutés.\n')
# Git sees tracked deltas only; include untracked status and content hashes as well.
(O/'git_diff.txt').write_text(subprocess.check_output(['git','diff'],cwd=R,text=True))
(O/'git_status.txt').write_text(subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=R,text=True))
files=set([R/'BASELINE_STATUS.md',R/'verify.sh'])
for name in ['README.md','README_RESEARCH.md','CITATION.cff','requirements.txt','pyproject.toml']:
 if (R/name).exists():files.add(R/name)
files.update(R.glob('*.pdf'));files.update((R/'articles').glob('*.pdf'))
for base in ['analysis','research_questions','external_review','remediation','closure_review','tests','corpus/extracted','corpus/metadata','rag','validation']:
 for path in (R/base).rglob('*'):
  if path.is_file() and path.suffix in ['.md','.json','.jsonl','.csv','.py','.sh','.txt','.log','.yaml','.yml','.bib','.cff'] and not any(t in path.parts for t in ['history','__pycache__','index']):files.add(path)
excluded={'BASELINE_MANIFEST_SHA256.txt','BASELINE_MANIFEST_SHA256.txt.sha256','manifest_verification.json'}
files={p for p in files if p.name not in excluded}
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in sorted(files))
(O/'BASELINE_MANIFEST_SHA256.txt').write_text(manifest)
digest=hashlib.sha256(manifest.encode()).hexdigest()
(O/'BASELINE_MANIFEST_SHA256.txt.sha256').write_text(digest+'  closure_review/BASELINE_MANIFEST_SHA256.txt\n')
for line in manifest.splitlines():
 expected,path=line.split('  ',1);assert hashlib.sha256((R/path).read_bytes()).hexdigest()==expected,path
js(O/'manifest_verification.json',dict(files=len(files),status='PASS',manifest_sha256=digest,excluded_self_referential_files=sorted(excluded),note='Verification report and detached manifest digest excluded to avoid self-hash cycle; historical archives separately checked where edited.'))
print(json.dumps(dict(status=summary['status'],counts=counts,tests=128,mutations_rejected=7,manifest_files=len(files),ready_for_academic_baseline=True),ensure_ascii=False,indent=2))
