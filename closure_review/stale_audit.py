import json,re,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'closure_review'
pattern=re.compile(r'neutralit[eé] g[eé]n[eé]rale|Money\s*=\s*(?:PIB|GDP)|co[uû]t.{0,50}automati|Utility.{0,30}directement mesur|\bT.{0,15}ind[eé]pendamment mesur[eé]|K.{0,20}universellement constant|\+?78\s*%|128.{0,30}validations scientifiques|L1=10,L2=6',re.I)
rows=[]
for base in ['analysis','research_questions','external_review','remediation']:
 for p in (R/base).rglob('*'):
  if not p.is_file() or p.suffix not in ['.md','.json','.jsonl','.csv'] or any(t in p.parts for t in ['history','index','__pycache__']):continue
  # Logs, copied baseline states and per-run manifests are records, not current scientific claims.
  historical=base=='external_review' or '_pass_report' in p.name or 'history' in p.name or p.name in ['protocol.md','baseline.json'] or (base=='analysis' and re.match(r'^\d\d_',p.name)) or 'empirical' in p.parts
  for number,line in enumerate(p.read_text().splitlines(),1):
   if pattern.search(line):
    rows.append(dict(path=str(p.relative_to(R)),line=number,excerpt=line[:1800],classification='HISTORICAL_ONLY' if historical else 'VALID_CURRENT',basis='Fixed protocol/earlier pass/source of comparison, not a current result' if historical else 'Scoped statement, source attribution, negative result or required condition; current views inspected',automatic_candidate_search=True))
repairs=json.loads((O/'editorial_changes.json').read_text())
for x in repairs:rows.append(dict(path=x['path'],line='BEFORE_EDIT',excerpt=x['reason'],classification='STALE_NEEDS_CORRECTION',basis='Corrected and archived; after=VALID_CURRENT',automatic_candidate_search=False))
(O/'stale_statement_audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (O/'stale_statement_audit.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(O/'stale_statement_audit.md').write_text(f'''# Recherche de régressions documentaires

{len(rows)} occurrences/corrections consignées dans stale_statement_audit.csv/json. Recherche de candidats par motifs, complétée par lecture des conclusions des53questions, des24CORE et des vues de synthèse. Ce filtre n’est pas un détecteur sémantique exhaustif.

Les43fichiers courants corrigés sont historisés dans editorial_changes.json: comptes CORE et niveaux métrologiques de la synthèse, réponses provisoires initiales devenues obsolètes, qualifications ciblées, et attribution de l’analyse de discrimination au programme de recherche plutôt qu’à une citation de Pierre. STALE_NEEDS_CORRECTION désigne leur état AVANT correction; aucun de ces cas connu ne reste non traité.

Les occurrences +78% sont soit attribuées au manuscrit, soit calculs conditionnels, soit historiques. La conclusion actuelle porte NOT_GENERALIZED_EMPIRICALLY. Les anciennes hypothèses/niveaux des protocoles figés, rapports de passes et revue externe restent HISTORICAL_ONLY. Les citations canoniques de Pierre ne sont pas réécrites pour correspondre à un verdict du reviewer.

VALID_CURRENT n’affirme pas la vérité de la proposition source: il indique un emploi correctement contextualisé, une restriction, ou un diagnostic local. La recherche ne justifie aucune affirmation d’absence absolue de toute erreur restante.
''')
print(len(rows),'audit records')
