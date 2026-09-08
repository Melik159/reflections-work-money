#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
research_python=python3
if [[ -x .venv-research/bin/python ]]; then research_python=.venv-research/bin/python; fi
"$research_python" rag/build_index.py
"$research_python" -m rag.evaluation.evaluate
"$research_python" analysis/run_empirical_iteration1.py
"$research_python" analysis/run_productive_checks.py
"$research_python" analysis/run_independent_energy.py --check
"$research_python" analysis/run_micro_electricity.py --check
"$research_python" analysis/run_two_product_aggregation.py --check
"$research_python" analysis/verify_research_questions.py
"$research_python" analysis/run_second_pass_formal.py --check
"$research_python" analysis/run_metrology_checks.py --check
"$research_python" analysis/run_fourth_pass.py --check
"$research_python" analysis/verify_contribution.py
if "$research_python" tests/run_phase2.py; then
  echo 'PASS: infrastructure, provenance and reproduced results'
  echo 'WARNING / COVERAGE_IN_PROGRESS: see validation/phase2_regression_results.json for examined/total'
  echo 'WARNING: literature partial, chapters in progress, hypotheses not all tested'
  echo 'WARNING / MONEY_REVIEW_QUALIFIED: scenario provenance checked; causal mechanisms and textual discrepancies remain open'
  echo 'WARNING / PRODUCTIVE_REVIEW_QUALIFIED: conditional formulas checked; causal protocols not identifiable with current data'
  echo 'WARNING / TERMINAL_REVIEW_QUALIFIED: independent energy associations are not causal; aggregation, units and T/dT remain qualified'
  echo 'WARNING / MICRO_NOT_IDENTIFIABLE: unmatched sector cost/price boundaries; Utility, total profit and Money unmeasured'
  echo 'WARNING / METROLOGY_IN_PROGRESS: T, cp, Utility and Money lack independent calibration; see research_questions/operationalization'
else
  echo 'FAIL: infrastructure or reproducibility; see validation/phase2_regression_results.json'
  exit 1
fi
