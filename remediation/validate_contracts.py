"""Targeted regression guard: approved wording and page evidence, not truth oracle."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def validate_contracts(results,cores):
 contracts={x['id']:x for x in json.loads((R/'remediation/trace_contract.json').read_text())}
 pages={x['page_pdf']:' '.join(x['text'].split()) for x in map(json.loads,(R/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
 for r in results:
  c=contracts[r['id']]
  assert r['statement']==c['approved_statement'],('Unreviewed conclusion/condition change',r['id'])
  for key in ['sources','source_pages','claims','questions','status','external_compatibility','distinctive_explanation']:
   assert r[key]==c[key],('Unreviewed evidence/scope change',r['id'],key)
  for passage in c['passages']:
   assert passage['quotation']==pages[passage['page']],('Passage not on referenced page',r['id'])
 c=next(c for c in cores if c['id']=='CPC-0016')
 assert 'EMPIRICALLY_COMPATIBLE' not in c['status'] and 'NOT_IDENTIFIED' in c['status'],'Whole chain not independently measured'
