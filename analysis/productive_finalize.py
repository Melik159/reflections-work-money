"""Explicit integration of scoped dependencies, references and regression rules."""
import json,shutil
from pathlib import Path
from productive_review import source
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):(ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
if (ROOT/'analysis/data/productive_invariant_snapshot.json').exists():raise SystemExit('Already integrated; preserve history.')
for p in ['analysis/data/semantic_invariants.json','analysis/data/regression_snapshot.json','analysis/data/literature_map.json','bibliography/initial_research_library.json']:
    t=ROOT/'analysis/history/pre_productive_review'/p;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,t)
ms=load('analysis/data/productive_mechanisms.json')['mechanisms']
deps=[['CPC-0051'],['CPC-0052'],['CPC-0052','CPC-0017'],['CPC-0019','CPC-0021'],['CPC-0021','CPC-0019'],['CPC-0015'],['CPC-0055','CPC-0045'],['CPC-0055','CPC-0045'],['CPC-0041','CPC-0055'],['CPC-0038'],['CPC-0038','CPC-0043'],['CPC-0018'],['CPC-0051','CPC-0052'],['CPC-0010','CPC-0016'],['CPC-0065'],['CPC-0044'],['CPC-0052','CPC-0019'],['CPC-0052'],['CPC-0068'],['CPC-0055','CPC-0060']]
claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()];byid={c['id']:c for c in claims}
g=load('analysis/data/argument_graph.json');g['edges']=[e for e in g['edges'] if not(e['target'].startswith('PM-') and e['source']=='CPC-0052' and e['relation']=='QUALIFIES')]
for m,ds in zip(ms,deps):
    byid[m['claims'][0]]['depends_on']=ds
    for d in ds:g['edges'].append(dict(source=d,target=m['id'],relation='DEPENDS_ON',direction='premise_to_dependent',evidence=m['source'],conditions=m['conditions'],interpretive=True))
save('analysis/data/argument_graph.json',g)
(ROOT/'analysis/data/claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
rules=[
 ('INV-009','Distinguer le niveau T de sa variation dT; Work nul à vitesse constante ne signifie pas labour ou W nul.',203,"if the speed of execution",['CPC-0064','CPC-0095']),
 ('INV-010','Une transmission coût–prix doit conserver les conditions de profit, de complexité et de point de vue.',504,'these segments have the same length',['CPC-0097','CPC-0098']),
 ('INV-011','Une dérivation mathématique conditionnelle ne doit pas devenir une validation empirique.',198,'they only give a measure',['CPC-0068','CPC-0096']),
 ('INV-012','Compatibilité énergie/PIB et énergie reconstruite ne prouvent pas causalité Work/Money.',456,'However, this relationship only expresses',['CPC-0018','CPC-0105']),
 ('INV-013','Chaque mécanisme productif conserve conditions, exceptions, horizon et niveau micro/macro.',205,'It is therefore necessary to consider',['CPC-0103','CPC-0104'])]
invs=load('analysis/data/semantic_invariants.json');snap=load('analysis/data/regression_snapshot.json')
for id,form,p,a,cids in rules:
    invs.append(dict(id=id,formulation=form,concepts=['work','money'],sources=[source(p,a)],importance='CORE_FIDELITY',claims=cids,regression_type='OMISSION_OR_CONFLATION',scope='ANALYST_RECONSTRUCTION_RULE_NOT_AUTHOR_QUOTATION',interpretive=True))
    snap['invariants'][id]=form
snap['change_log'].append(dict(old_status='8 semantic invariants',new_status='13 semantic invariants',new_evidence='Targeted productive reading and reports25–26',justification='Append scoped reconstruction rules; retain all eight previous formulations including Cash/Money.'))
save('analysis/data/semantic_invariants.json',invs);save('analysis/data/regression_snapshot.json',snap)
save('analysis/data/productive_invariant_snapshot.json',dict(conditions={m['id']:m['conditions'] for m in ms},policy='Change allowed only with old/new condition, new source and justification; do not silently delete branches.'))
refs=[dict(id='BIB-0009',authors='Lucia Foster and John Haltiwanger and Chad Syverson',title='Reallocation, Firm Turnover, and Efficiency: Selection on Productivity or Profitability?',year=2005,doi='10.3386/w11555',url='https://www.nber.org/papers/w11555',verification_url='https://www.census.gov/library/working-papers/2005/adrm/ces-wp-05-11.html',status='VERIFIED',access='Primary metadata and abstract read; full study and microdata not reproduced',summary='Physical and revenue productivity have different price correlations; not evidence for a universal speed-squared law.'),
 dict(id='BIB-0010',authors='Cyrille Schwellnus and Andreas Kappeler and Pierre-Alain Pionnier',title='Decoupling of wages from productivity: Macro-level facts',year=2017,doi='10.1787/d4764493-en',url='https://www.oecd.org/en/publications/decoupling-of-wages-from-productivity_d4764493-en.html',status='VERIFIED',access='Official DOI, authors, date and abstract read; full study not reproduced',summary='Labour shares and wage distribution qualify transmission to real median compensation.')]
save('bibliography/productive_library.json',refs)
library=load('bibliography/initial_research_library.json');library+=refs;save('bibliography/initial_research_library.json',library)
lit=load('analysis/data/literature_map.json');lit['sources']+=refs
for b,c,rel,scope in [('BIB-0009','CPC-0096','SUPPORTS','Only compatible negative correlation physical productivity/price; not causal or universal confirmation'),('BIB-0009','CPC-0098','QUALIFIES','Separate prices, quantities and demand before inferring transmission'),('BIB-0009','CPC-0035','DOES_NOT_TEST','No independent test of Campergue Economic Work or quadratic law in inspected abstract'),('BIB-0010','CPC-0016','QUALIFIES','Median worker remuneration is not identical to consumer gain at fixed income'),('BIB-0010','CPC-0064','DOES_NOT_TEST','Statistical labour productivity not independent measurement of T')]:
    lit['relations'].append(dict(source_id=b,claim_id=c,relation=rel,scope=scope,assessment_status='PRODUCTIVE_TARGETED_REVIEW_ABSTRACT_ONLY',interpretive=True))
save('analysis/data/literature_map.json',lit)
(ROOT/'bibliography/productive_library.bib').write_text('\n'.join('@techreport{'+r['id']+',\n  author = {'+r['authors']+'},\n  title = {'+r['title']+'},\n  year = {'+str(r['year'])+'},\n  doi = {'+r['doi']+'},\n  url = {'+r['url']+'}\n}\n' for r in refs))
