#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
research_python=python3
if [[ -x .venv-research/bin/python ]]; then research_python=.venv-research/bin/python; fi
"$research_python" -m rag.iterative build
./verify.sh
"$research_python" -m unittest research_state.test_state -v
sha256sum --quiet -c closure_review/BASELINE_MANIFEST_SHA256.txt
echo 'PASS: iterative state, collection boundaries and frozen baseline'
echo 'WARNING: metadata guards do not establish independent measurements; semantic embeddings and held-out multi-level retrieval evaluation remain OPEN'
