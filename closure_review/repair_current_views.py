"""Scoped editorial repairs only; archive every replaced current file."""
import json,re,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];O=R/'closure_review'
assert not (O/'editorial_changes.json').exists()
changes=[]
def edit(path,text,reason):
 p=R/path;old=p.read_text()
 if old==text:return
 h=O/'history'/path;h.parent.mkdir(parents=True,exist_ok=True);h.write_text(old)
 p.write_text(text);changes.append(dict(path=path,reason=reason,old_sha256=hashlib.sha256(old.encode()).hexdigest(),new_sha256=hashlib.sha256(text.encode()).hexdigest(),classification_before='STALE_NEEDS_CORRECTION',classification_after='VALID_CURRENT'))
cores=json.loads((R/'research_questions/synthesis/core_claims.json').read_text());counts=dict(Counter(s for c in cores for s in c['status']))
p='research_questions/synthesis/final_synthesis.md';t=(R/p).read_text()
t=re.sub(r"Les classifications sont non exclusives : \{[^\n]+?\}\.",f'Les classifications sont non exclusives : {counts}.',t)
t=t.replace('L0=0,L1=10,L2=6,L3=9,L4=0,L5=1','L0=0,L1=12,L2=4,L3=9,L4=0,L5=1')
edit(p,t,'Synchronise les comptes actuels CORE et métrologie; les anciennes valeurs étaient restées dans le corps de la synthèse.')
qs=json.loads((R/'research_questions/synthesis/questions.json').read_text())
notes={
 'RQ-03.02':'T/dT et cp restent conditionnels; aucun T indépendant. Voir ../../remediation/formal_corrections.md.',
 'RQ-04.02':'+78%: NOT_GENERALIZED_EMPIRICALLY; revendication de généralité p32 distincte du calcul conditionnel. Voir ../../remediation/formal_corrections.md.',
 'RQ-05.03':'Utility cible L1 NOT_OPERATIONALIZED; candidats proxies L2 sans échelle cardinale établie. Voir ../operationalization/variables.json.',
 'RQ-06.01':'Référents solde, gain, valeur portée, cinétique, potentiel et transfert distincts; aucun dictionnaire unifié imposé. Voir ../../remediation/money_referents.md.',
 'RQ-06.04':'Création de dépôts distincte de Money; conserver référents et32scénarios. Voir ../../remediation/money_referents.md.',
 'RQ-08.01':'P205 limite au Transformer et à la valeur ajoutée; ce n’est pas un pont opérationnel acquis au PIB. Voir ../../remediation/money_gdp_bridge.md.',
 'RQ-08.02':'La variance distingue moyenne des carrés et carré de moyenne p559; K conditionnel ne règle pas ce passage. Voir ../../remediation/formal_corrections.md.',
 'RQ-09.02':'Énergie primaire par substitution: quantité construite, indépendante du PIB mais non directement mesurée ni exogène. L5 désigne la reproductibilité. Voir ../operationalization/variables.json.',
 'RQ-09.03':'Pont Money/valeur ajoutée/PIB explicitement incomplet avant le test de K. Ne pas imputer double compte inévitable, ni conversion physique directe. Voir ../../remediation/money_gdp_bridge.md.',
 'RQ-11.01':'Dommage cible L1; pression candidate L2. P112/534/537 comporte des généralisations de l’auteur, distinctes de la conclusion conditionnelle du reviewer.',
 'RQ-11.03':'Allocation marginale et fonction de dommage absentes; absence de test causal ou discriminant. Voir ../../remediation/traceability_repairs.md.'}
for q in qs:
 path=f"research_questions/{q['id']}/conclusion.md";t=(R/path).read_text();old=t
 generic='OPEN : dossier indexé, non examiné en profondeur dans cette passe. Le texte atteste les propositions liées ; il ne suffit pas à répondre à la question.'
 if generic in t:
  t=t.replace(generic,q['status']+' — '+q['main_corpus_answer']+'\n\nLimite empirique actuelle: '+q['empirical_status'])
  t=t.replace('Couverture ciblée et absence de revue approfondie ; pas une réfutation.','Le statut courant tient compte de la consolidation; elle ne constitue ni mesure indépendante ni résolution de cette question. Les remarques de passes datées ci-dessous restent historiques.')
  t=re.sub(r'(## CONFIDENCE\s*\n\s*)LOW\b',lambda m:m[1]+q['confidence'],t,count=1)
 if q['id']=='RQ-12.01':
  t=t.replace('## WHAT_CAMPERGUE_CLAIMS\n\nPour discriminer','## WHAT_CAMPERGUE_CLAIMS\n\nINTERPRETATION DU PROGRAMME DE RECHERCHE, non citation de Campergue: pour discriminer')
  t=t.replace('aucune signature empirique de la théorie complète établie','aucune signature empirique propre au système complet établie')
 if q['id']=='RQ-09.03':t=t.replace('Énergie physique consommée observable ;','Série primaire par substitution construite et reproductible, non mesure physique directe sans conventions ;')
 rem=[]
 if q['id'] in notes:rem.append(notes[q['id']])
 if 'CPC-0016' in q['claims']:rem.append('CPC-0016: attribution conservée, statut empirique de la chaîne complète NOT_IDENTIFIED; compatibilité de sous-relations ne le promeut pas.')
 if rem:t+='\n\n## Qualifications actuelles — clôture\n\n'+'\n\n'.join(rem)+'\n\nStatut de la question inchangé. Référence courante: ../synthesis/questions.json; versions remplacées dans closure_review/history/.\n'
 if t!=old:edit(path,t,'Aligne la conclusion courante sur synthèse/graphe; incorpore uniquement remédiations pertinentes, sans nouvelle résolution.')
(O/'editorial_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('Current views repaired:',len(changes))
