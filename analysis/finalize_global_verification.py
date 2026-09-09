"""Repair legacy note pointers and record actual verification, with history."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'

def main():
    p=argparse.ArgumentParser();p.add_argument('--repair-notes',action='store_true');p.add_argument('--finalize',action='store_true');args=p.parse_args()
    results=ROOT/'validation/phase2_regression_results.json'
    if args.repair_notes:
        history=OUT/'history/first_final_verification.json'
        if not history.exists():history.write_bytes(results.read_bytes())
        path=ROOT/'analysis/data/page_coverage.json';rows=json.loads(path.read_text());changes=[]
        for r in rows:
            if r['examined'] and not r.get('reading_note') and r.get('global_pass_note'):
                new='../global_corpus_pass/blocks/'+Path(r['global_pass_note']).name
                changes.append(dict(page=r['page'],old_reading_note=r['reading_note'],new_reading_note=new,
                    reason='Legacy note field now points to the actual analytical note, not an empty placeholder.'))
                r['reading_note']=new
        path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
        log=OUT/'history/coverage_note_repair.json'
        if not log.exists():log.write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
        print('Repaired actual note links:',len(changes))
    if args.finalize:
        tests=json.loads(results.read_text());assert tests['status']=='PASS' and tests['failed']==0 and tests['errors']==0
        target=OUT/'verification_results.json';target.write_bytes(results.read_bytes())
        manifest_path=OUT/'manifest.json';manifest=json.loads(manifest_path.read_text())
        manifest['verification_status']='PASS';manifest['regression_tests']=tests['tests_run']
        manifest['regression_passed']=tests['passed'];manifest['regression_failed']=0
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        report=OUT/'final_report.md';history=OUT/'history/report_before_final_verification.md'
        if not history.exists():history.write_bytes(report.read_bytes())
        text=report.read_text().replace('**PENDING_FINAL_EXECUTION**',f"**PASS — {tests['passed']}/{tests['tests_run']} tests, code de sortie0 de ./verify.sh**")
        text+='\n### Journal de vérification\n\nPremier contrôle après modification :101 PASS,1 ERROR (pointeur de note analytique ancien vide). Résultat négatif conservé dans history/first_final_verification.json. Raccordement aux notes réellement écrites corrigé, sans désactiver le test. Relance complète de ./verify.sh :102/102 PASS. WARNING : consolidation intégrale inachevée; ce PASS ne certifie pas562pages lues.\n'
        report.write_text(text)
        print('Recorded:',tests['passed'],'/',tests['tests_run'],'PASS; readiness remains NO')

if __name__=='__main__':main()
