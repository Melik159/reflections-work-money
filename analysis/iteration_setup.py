"""Idempotent archive and policy migration; never changes scientific source PDFs."""
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    for name in ['verify.sh','tests/corpus/test_phase2.py','tests/run_phase2.py',
        'analysis/data/phase2_progress.json','analysis/data/page_coverage.json',
        'analysis/data/claims.jsonl','analysis/data/concepts.json','analysis/data/argument_graph.json',
        'analysis/data/research_chapters.json','analysis/data/regression_snapshot.json',
        'rag/evaluation/results.json','rag/index/manifest.json','validation/phase2_regression_results.json']:
        src=ROOT/name; dest=ROOT/'analysis/history/pre_iteration1'/name
        if src.exists() and not dest.exists():
            dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dest)
    p=ROOT/'analysis/data/phase2_progress.json'; state=json.loads(p.read_text())
    state.update(status='SUFFICIENT_FOR_ITERATIVE_RESEARCH',ready_for_bibliographic_adversarial_review=True,
        coverage_status='COVERAGE_IN_PROGRESS',policy='User authorizes iterative research without exhaustive prior reading.')
    p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
