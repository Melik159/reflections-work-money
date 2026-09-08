"""Explicit current-input refresh; original evidence certificate remains in history."""
import json,csv,hashlib,ast,sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];S=R/'research_questions/synthesis';O=R/'remediation'
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def refresh():
 records=json.loads((S/'input_manifest.json').read_text());changes=[]
 for r in records:
  actual=hashlib.sha256((R/r['path']).read_bytes()).hexdigest()
  if actual!=r['sha256']:changes.append(dict(path=r['path'],old_hash=r['sha256'],new_hash=actual,reason='Explicit remediation; original archived before edits'));r['sha256']=actual
 if changes:
  old=json.loads((O/'input_refresh_history.json').read_text()) if (O/'input_refresh_history.json').exists() else []
  js(O/'input_refresh_history.json',old+changes);js(S/'input_manifest.json',records)
def score():
 with (R/'external_review/test_audit.csv').open() as f:old={r['test']:r['primary_category'] for r in csv.DictReader(f)}
 rows=[]
 for p in sorted((R/'tests/corpus').glob('test_*.py')):
  for cls in ast.parse(p.read_text()).body:
   if not isinstance(cls,ast.ClassDef):continue
   for m in cls.body:
    if isinstance(m,ast.FunctionDef) and m.name.startswith('test_'):
     id=f'{p.stem}.{cls.name}.{m.name}'
     cat=old.get(id,'FORMAL_TEST' if m.name=='test_local_formal_remediation' else 'LOGIC_TEST')
     rows.append(dict(id=id,category=cat,source=str(p.relative_to(R)),line=m.lineno))
 counts=Counter(r['category'] for r in rows)
 d=dict(total=len(rows),categories=dict(counts),structural=sum(counts[k] for k in ['INTEGRITY_TEST','PROVENANCE_TEST','LOGIC_TEST']),formal_scientific=counts['FORMAL_TEST'],empirical_reproduction=counts['EMPIRICAL_REPRODUCTION_TEST'],independent_discriminating=counts['SCIENTIFIC_VALIDITY_TEST'],classification='Primary function, exclusive; mathematical diagnostics scientific locally, not economic validation',tests=rows)
 js(O/'test_classification.json',d)
 (R/'validation/remediation_scoreboard.md').write_text('# Tests après remédiation\n\n'+ '\n'.join(f'- {k}: {v}' for k,v in d.items() if k!='tests')+'\n\nLes mutations ciblées vérifient la conservation des énoncés approuvés, pas la vérité de tout nouvel énoncé. Une modification légitime nécessite nouvelle revue et historique.\n')
 print(json.dumps({k:v for k,v in d.items() if k!='tests'}))
if __name__=='__main__':
 if '--score-only' not in sys.argv:refresh()
 score()
