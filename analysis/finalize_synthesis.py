"""Record the executed verification, preserving the previous certificate state.

Run only after ./verify.sh succeeds. Does not change claims or question statuses.
"""
import csv
import hashlib
import json
from pathlib import Path
from verify_synthesis import validate,OUT,ROOT

def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def main():
    manifest_path=OUT/'manifest.json'
    m=json.loads(manifest_path.read_text())
    if m['status']!='SYNTHESIS_WRITTEN_PENDING_VERIFICATION':
        raise SystemExit('Certificate already finalized; do not overwrite its history.')
    checks=validate()
    report=json.loads((ROOT/'validation/phase2_regression_results.json').read_text())
    assert report['status']=='PASS' and report['tests_run']==report['passed']==120
    assert report['failed']==report['errors']==report['skipped']==0
    assert sum('test_synthesis.' in s for s in report['passed_tests'])==14
    # An explicit provenance extension, not a change of scientific conclusion:
    # four local numerical checks alone do not document every textual problem in SYN-08.
    results=json.loads((OUT/'results.json').read_text())
    result=next(r for r in results if r['id']=='SYN-08')
    previous_sources=result['sources'][:]
    result['sources'].append('analysis/global_corpus_pass/final_report.md')
    dump(OUT/'results.json',results)
    with (OUT/'master_matrix.csv').open() as f:
        reader=csv.DictReader(f); fields=reader.fieldnames;matrix=list(reader)
    next(r for r in matrix if r['Item']=='SYN-08')['Source']='; '.join(result['sources'])
    with (OUT/'master_matrix.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(matrix)
    for name in ['negative_results.md','weakest_points.md']:
        p=OUT/name
        p.write_text(p.read_text()+'\n\nComplément de provenance SYN-08 : [bilan global, FORMAL ISSUES](../../analysis/global_corpus_pass/final_report.md), pour les égalités interpersonnelles et les forces constantes; le fichier formal_checks.json ne couvre que quatre diagnostics numériques locaux.\n')
    dump(OUT/'certificate_history.json',dict(previous_manifest=m,provenance_extension=dict(
        item='SYN-08',old_sources=previous_sources,new_sources=result['sources'],
        reason='Separate the complete textual catalogue from the four executable numerical diagnostics; statement unchanged.')))
    dump(OUT/'verification_results.json',report)
    m.update(status='SYNTHESIS_COMPLETE',ready_for_external_review=True,
       verification=dict(command='./verify.sh',exit_code=0,tests_run=120,passed=120,failed=0,errors=0,skipped=0,
          new_synthesis_tests=14,result_artifact='research_questions/synthesis/verification_results.json',
          warnings=checks['warnings'],scientific_validation=False))
    dump(manifest_path,m)
    inputs=json.loads((OUT/'input_manifest.json').read_text())
    path='analysis/finalize_synthesis.py'
    inputs.append(dict(path=path,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()))
    dump(OUT/'input_manifest.json',sorted(inputs,key=lambda r:r['path']))
    (OUT/'verification.md').write_text('''# Vérification de la synthèse

`./verify.sh` effectivement exécuté, code de sortie0 : **120/120 tests PASS**, 0FAIL, 0ERROR, 0SKIP. Les14nouveaux tests incluent des contrôles négatifs de suppression de source, de disparition de qualification, de promotion silencieuse, de fausse originalité et de validation globale.

Les calculs antérieurs ont été contrôlés à nouveau par le point d'entrée; aucune expérience empirique nouvelle n'a été lancée. Le snapshot des résultats de tests est conservé dans `verification_results.json`. La modification finale de provenance SYN-08 est historisée et fait l'objet d'un nouveau passage de vérification avant remise.

WARNING : questions scientifiques ouvertes; étalons T/cp/Utility/Money manquants; littérature partielle; causalité et pouvoir discriminant non identifiés. Couverture :562/562scannées,447/562analytiquement examinées cumulées.

SYNTHESIS_COMPLETE. READY_FOR_EXTERNAL_REVIEW = YES concerne un dossier documenté et testable par des lecteurs externes; cela n'affirme ni résolution des53questions ni confirmation du système.
''')
    p=OUT/'final_synthesis.md'
    p.write_text(p.read_text()+'''\n## Verification and delivery status

SYNTHESIS_COMPLETE. `./verify.sh` :120/120PASS, aucun échec;14nouveaux tests de synthèse. [Détail et avertissements](verification.md). [Inventaire exact des fichiers créés/modifiés](files_created.json). Aucun PDF source modifié, aucun push. READY_FOR_EXTERNAL_REVIEW = YES : prêt à une revue externe documentaire et contradictoire, pas certificat de justesse économique.
''')
    (OUT/'editorial_history.md').write_text((OUT/'editorial_history.md').read_text()+'''\n4. Avant remise, SYN-08 reçoit aussi le bilan global comme source explicite des problèmes textuels; les quatre calculs de formal_checks.json seuls ne couvrent pas tous ces problèmes. Énoncé et statut inchangés; ancienne/nouvelle provenance dans certificate_history.json.\n''')
    added=[str(p.relative_to(ROOT)) for p in OUT.iterdir() if p.is_file()]
    added += ['research_questions/synthesis/files_created.json','analysis/synthesis_catalog.py',
      'analysis/synthesis_narrative.py','analysis/build_final_synthesis.py','analysis/verify_synthesis.py',
      'analysis/finalize_synthesis.py','tests/corpus/test_synthesis.py']
    archives=[str(p.relative_to(ROOT)) for directory in ['analysis/history/synthesis_build_attempt_01',
       'analysis/history/synthesis_draft_before_editorial_check'] for p in (ROOT/directory).rglob('*') if p.is_file()]
    dump(OUT/'files_created.json',dict(created=sorted(set(added)),archived_drafts=sorted(archives),
       modified=['verify.sh','research_questions/README.md','validation/phase2_regression_results.json'],
       note='Other existing computational outputs refreshed by verify retain their prior role. Canonical claims and scientific statuses unchanged. No push.'))
    print(json.dumps(validate(),ensure_ascii=False))

if __name__=='__main__':main()
