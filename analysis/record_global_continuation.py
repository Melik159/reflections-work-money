"""Checkpoint actual editorial readings; archive all modified artifacts first.

No classification is inferred from text searches or historical coverage.
This command is idempotent: previously scanned pages are never re-counted.
"""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from global_pass_continuation_catalog import NOTES, ANALYTICAL, questions

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'

def dump(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def csvtext(rows):
    s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return s.getvalue()

def main():
    rows=list(csv.DictReader((OUT/'page_matrix.csv').open()))
    pending=[int(r['page']) for r in rows if r['scan_status']=='UNREVIEWED' and int(r['page']) in NOTES]
    if not pending:
        print('No newly read pages to checkpoint.');return
    archive=OUT/f'history/before_pages_{min(pending):03}_{max(pending):03}'
    archive.mkdir(parents=True,exist_ok=False)
    backups=[]
    def write(path,content):
        if path.exists():
            rel=path.relative_to(ROOT);b=archive/rel;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(path.read_bytes())
            backups.append({'path':str(rel),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    graph=json.loads((ROOT/'research_questions/question_graph.json').read_text())
    qids={q['id'] for q in graph['nodes']}
    coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
    for p in pending:
        r=rows[p-1];qs=questions(p);assert set(qs)<=qids,(p,qs-qids)
        structural=p not in {1,5,6,7,8,9,10,11,27,41,63,65,66,76,79,83,86,90,96,102,119,120,134,140,141,145,153,154,155,169}
        r.update(scan_status='ANALYTICALLY_REVIEWED' if p in ANALYTICAL else 'SCANNED',
                 questions=';'.join(qs) if structural else '',importance='STRUCTURAL' if structural else 'ILLUSTRATIVE',notes=NOTES[p])
        r['section']='Préliminaires' if p<=11 else 'Préambule' if p<=37 else 'Prolegomena' if p<=167 else 'Prolegomena / valeur de l’unité monétaire' if p==168 else 'Valeur de l’unité monétaire'
        if p>=184:r['section']='Définitions' if p<=194 else 'Mécanique des échanges' if p<=216 else 'Principes' if p<=230 else 'Énergies internes' if p<=257 else 'Flux et transformations' if p<=278 else 'Core Laws'
        if p>=302:r['section']='Définitions additionnelles' if p<=318 else 'Difficultés' if p<=334 else 'Structure des échanges' if p<=344 else 'Cycles' if p<=371 else 'Conditions de création' if p<=382 else 'Rendements' if p<=401 else 'Offre et demande' if p<=412 else 'Potentiels' if p<=425 else 'Coefficients' if p<=453 else 'Pont physique-économie' if p<=464 else 'Conservation' if p<=472 else 'Agents' if p<=485 else 'Monopoles et concurrence' if p<=493 else 'Cycles polaires'
        start=((p-1)//25)*25+1;end=min(start+24,562);note=f'../global_corpus_pass/blocks/p{start:03}_p{end:03}.md'
        if p in ANALYTICAL:
            item=coverage[p-1]
            if not item['examined']: item.update(examined=True,reading_note=note,reason='GLOBAL_ANALYTICAL_REVIEW',excluded=False)
            item['global_pass_note']=note
    for start in sorted({((p-1)//25)*25+1 for p in pending}):
        end=min(start+24,562);subset=rows[start-1:end];scanned=[r for r in subset if r['scan_status']!='UNREVIEWED']
        status='QUALIFIES_EXISTING' if len(scanned)==len(subset) else 'REQUIRES_REVIEW'
        content=f'# Bloc PDF {start:03}–{end:03}\n\nStatut : {status}. Pages effectivement parcourues : {len(scanned)}/{len(subset)}.\n\nSOURCE : texte extrait par page; contrôle visuel seulement lorsque indiqué. Les notes sont INTERPRETATION. Aucun classement automatique ne vaut lecture.\n'
        for r in scanned:
            content+=f"\n## PDF {r['page']} — {r['scan_status']}\n\n{r['notes']}\n\nQuestions : {r['questions'] or 'NON_STRUCTURAL / ILLUSTRATIVE'}. Claims : {r['claims'] or 'voir rapprochements transversaux'}. Concepts : {r['concepts'] or 'voir note'}. Formules : {r['formulas'] or 'voir note; inventaire en cours'}. Visuel : {r['visual_checked']}.\n"
        content+='\nConflits, scénarios, exceptions et références : identifiés dans les notes paginées; ceux nécessitant une confrontation supplémentaire restent ouverts.\n'
        write(OUT/f'blocks/p{start:03}_p{end:03}.md',content)
    manifest=json.loads((OUT/'manifest.json').read_text());counts=Counter(r['scan_status'] for r in rows)
    manifest.update(pages_scanned=562-counts['UNREVIEWED'],pending_pages=[int(r['page']) for r in rows if r['scan_status']=='UNREVIEWED'],analytical_this_pass=counts['ANALYTICALLY_REVIEWED']+counts['DEEP_REVIEWED'],deep_this_pass=counts['DEEP_REVIEWED'],cumulative_analytical_after=sum(p['examined'] for p in coverage),verification_status='NOT_RERUN_SINCE_CHECKPOINT')
    progress=json.loads((ROOT/'analysis/data/phase2_progress.json').read_text());progress['pages_examined']=manifest['cumulative_analytical_after'];progress['global_consolidation_note']=f"{manifest['pages_scanned']}/562 pages parcourues; consolidation en cours, aucune certification intégrale."
    write(OUT/'page_matrix.csv',csvtext(rows));write(OUT/'manifest.json',dump(manifest));write(ROOT/'analysis/data/page_coverage.json',dump(coverage));write(ROOT/'analysis/data/phase2_progress.json',dump(progress))
    # Preserve the previous report verbatim; no scientific completeness inferred.
    report=(OUT/'final_report.md').read_text()
    report+=f"\n## Checkpoint de continuation — pages {min(pending)}–{max(pending)}\n\n{len(pending)} pages nouvelles réellement lues. Total spécifique : {manifest['pages_scanned']}/562. Couverture analytique cumulée : {manifest['cumulative_analytical_after']}/562. Aucun nouveau DEEP_REVIEWED. Les statistiques de la tranche antérieure ci-dessus sont historiques. Revue globale des claims/formules toujours en cours. Verify à relancer avant certification.\n\nREADY_FOR_SYNTHESIS = NO\n"
    write(OUT/'final_report.md',report)
    (archive/'archive_manifest.json').write_text(dump(backups))
    print(dump({'new_pages':len(pending),'scanned':manifest['pages_scanned'],'analytical':manifest['cumulative_analytical_after'],'archive':str(archive.relative_to(ROOT))}))

if __name__=='__main__': main()
