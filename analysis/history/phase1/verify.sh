#!/usr/bin/env bash
set -e
python rag/build_index.py >/tmp/rag_build.out
python - <<'PY'
import json,hashlib
assert len(open('corpus/extracted/Reflections_PierreCampergue.pages.jsonl').readlines())==562
assert json.load(open('rag/index/manifest.json'))['chunks']>=562
for l in open('analysis/data/claims.jsonl'):
 r=json.loads(l); assert r['source_document'] and r['page']
print('PASS corpus/RAG/claims')
PY
