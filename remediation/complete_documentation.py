import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'remediation';S=R/'research_questions/synthesis';M=R/'research_questions/methodology'
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
pages={x['page_pdf']:' '.join(x['text'].split()) for x in map(json.loads,(R/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
terms=['opinion','belief','approximation','definition','measure','coherence','logic','demonstration','hypothesis','theory','science','truth','error','model','expert','authority','consensus','opinion makers',"faiseurs d’opinion",'croyance','définition','mesure','cohérence','démonstration','hypothèse','vérité','erreur','modèle','autorité']
js(M/'search_inventory.json',dict(method='Candidate search across all562pages then direct reading, not claims extraction.',terms={term:[p for p,t in pages.items() if term.casefold() in t.casefold()] for term in terms},directly_read_pages=[15,63,64,65,79,80,109,301,303,523,535,561,562]))
p=M/'corpus_passages.md';t=p.read_text()
for page in [64,65,562]:
 marker=f'## Additional SOURCE — PDF {page}'
 if marker not in t:t+='\n\n'+marker+'\n\nSOURCE\n\n> '+pages[page]+'\n\nINTERPRETATION: monosemie p64–65; devise personnelle p562. Citations d’autres auteurs rapportées comme texte du manuscrit, non références externes vérifiées.\n'
p.write_text(t)
criteria=json.loads((M/'criteria.json').read_text());c=criteria[1];c['source_pages']=[15,63,64,65];c['criterion']='Concepts rationnels, monosemie et cohérence analytique';c['demands']='P64 réclame une désignation univoque, idéalement monosémique; p65 l’applique à Work/Money.';criteria[5]['source_pages']=[63,79,561,562]
js(M/'criteria.json',criteria)
(M/'internal_consistency_test.md').write_text('# Critères internes\n\nStatuts limités au périmètre explicité; intention ≠ réussite.\n\n'+'\n\n'.join('## '+c['id']+'\n\n'+'\n\n'.join(f'{k}: {v}' for k,v in c.items()) for c in criteria))
p=M/'epistemic_program.md';t=p.read_text()
if '## Monosemie et clôture' not in t:p.write_text(t+'\n\n## Monosemie et clôture autobiographique\n\nP64–65 exige une désignation univoque: le dictionnaire Money répond à une exigence explicite, pas seulement à une préférence du reviewer. P562 donne une devise de recherche de raison; les citations Besnier/Keynes ne sont pas vérifiées indépendamment ici. P64 reconnaît lui-même la tension entre économie recherchée par les agents et absence annoncée de caractère anthropique.\n')
actions=json.loads((O/'finding_actions.json').read_text());a=next(a for a in actions if a['id']=='ER-002');a['action']='PARTIALLY_ACCEPT';a['action_taken']='Pont incomplet accepté; rattachement corrigé: CPC-0118 p559, non CPC-0127 p400 (destination du gain).';a['claim_status_impact']='Qualification du raccord CPC-0118, attribution conservée; erreur de rattachement externe documentée.';js(O/'finding_actions.json',actions)
(O/'review_target_correction.md').write_text('# Rattachement ER-002\n\nLa revue indiquait CPC-0127 pour le PIB. Ce claim p400 porte sur la destination du gain. Le claim macro est CPC-0118 p559, accompagné de CPC-0117 pour K. Le fond est retenu, le rattachement corrigé. Revue externe historique inchangée. PARTIALLY_ACCEPT.\n')
manifest=json.loads((S/'manifest.json').read_text());manifest['scientific_status_changes']=json.loads((O/'claim_status_history.json').read_text());manifest['canonical_claim_changes']=[dict(id=id,kind='METADATA_OR_CONTEXT_EXTENSION_ONLY',history='remediation/history/analysis/data/claims.jsonl') for id in ['CPC-0016','CPC-0035','CPC-0041','CPC-0048']];js(S/'manifest.json',manifest)
p=S/'question_synthesis.md';t=p.read_text()
for phrase in ['VAR-06 Utility: L2 PROXY_ONLY','VAR-23 environmental damage: L2 PROXY_ONLY']:t=t.replace(phrase,phrase.replace('L2 PROXY_ONLY','L1 NOT_OPERATIONALIZED (candidate proxy L2)'))
t=t.replace('VAR-16 energy: L5 DIRECTLY_OBSERVABLE','VAR-16 energy: L5 DERIVABLE_FROM_OBSERVABLES').replace('VAR-07 Money: L1 NOT_OPERATIONALIZED','VAR-07 Money: L1 AMBIGUOUS');p.write_text(t)
