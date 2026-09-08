#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python3 rag/build_index.py
python3 -m rag.evaluation.evaluate
if python3 tests/run_phase2.py; then
  echo 'PASS: technical regression and phase 2 exit criteria'
else
  echo 'FAIL: see validation/phase2_regression_results.json; incomplete reading prevents a global PASS'
  exit 1
fi
