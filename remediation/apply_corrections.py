"""One-time, authored remediation with exact before/after history."""
import json,csv,hashlib,io,shutil
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];O=R/'remediation';S=R/'research_questions/synthesis'
def load(p):return json.loads((R/p).read_text())
changes=[]
def write(p,t):
 p=R/p;old=p.read_text() if p.exists() else None
 if old==t:return
 if old is not None:
  h=O/'history'/p.relative_to(R);h.parent.mkdir(parents=True,exist_ok=True)
  if not h.exists():h.write_text(old)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
 changes.append(dict(path=str(p.relative_to(R)),old_sha256=hashlib.sha256(old.encode()).hexdigest() if old is not None else None,new_sha256=hashlib.sha256(t.encode()).hexdigest()))
def js(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def mdtable(rows):
 keys=list(rows[0]);return '| '+' | '.join(keys)+' |\n|'+'|'.join(['---']*len(keys))+'|\n'+'\n'.join('| '+' | '.join(str(r[k]).replace('|','/').replace('\n',' ') for k in keys)+' |' for r in rows)
def csvwrite(p,rows):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);write(p,s.getvalue())
def append(p,t):write(p,(R/p).read_text()+'\n\n'+t+'\n')
assert (O/'baseline.json').exists()
assert not (O/'applied_changes.json').exists(),'Already applied; do not repeat'
pages={x['page_pdf']:' '.join(x['text'].split()) for x in map(json.loads,(R/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
refs=[
dict(usage='Valeur portée / mesure',pages=[15],context='M=n u; nombre et valeur unitaire',same_variable='Non démontré avec les autres référents',compatible='Conditionnel: étalon et panier communs',ambiguity='Valeur de u non opérationnalisée indépendamment'),
dict(usage='Gain du consommateur',pages=[19,204],context='0.1 dollar conservé pour un kilogramme après baisse de prix',same_variable='deltaM_gain, label analytique seulement',compatible='Budget fixe mesurable; pas identité démontrée avec toute richesse',ambiguity='Panier, qualité, revenu et dépenses ultérieures'),
dict(usage='Solde / Money disponible',pages=[204],context='Même dollar avant/après, plus grande possibilité d’achat',same_variable='M_solde, pas symbole nouveau de l’auteur',compatible='Ne pas additionner le gain au Cash nominal comme une émission',ambiguity='Solde nominal vs valeur portée'),
dict(usage='Grandeur cinétique relative',pages=[207],context='M=−½caϖ², constante choisie nulle',same_variable='M_cinétique, référent analytique',compatible='Possible avec origine et signe orientés; non identité automatique au solde',ambiguity='Étalon, ca et référence'),
dict(usage='Potentiel / total',pages=[467],context='Total = cinétique échange + potentiel épargne',same_variable='Total composé, pas forcément M cinétique seul',compatible='Décomposition à expliciter',ambiguity='Épargne comptable vs potentiel'),
dict(usage='Transfert orienté',pages=[205,206,455],context='Entrée/sortie de système, création/destruction orientées',same_variable='Flux/transfert, pas état',compatible='Frontière, temps, convention et conversion nécessaires',ambiguity='Création locale ne signifie pas création globale')]
js('remediation/money_referents.json',refs)
write('remediation/money_referents.md','# Money: référents conservés, unité non forcée\n\nLes labels M_solde/deltaM_gain/M_cinétique sont INTERPRETATION, non notations attribuées à Pierre.\n\n'+mdtable(refs))
bridge='''# Money / valeur ajoutée / PIB

## WHAT_CAMPERGUE_EXPLICITLY_STATES

P205 restreint l’étude à la valeur ajoutée d’un Transformer; p559 identifie PIB et Money dépensé, puis GDP=K Tspent et GDP=K Wconsumed. P529/537 discutent richesse et prix; ce n’est pas une définition opérationnelle du PIB réel.

## WHAT_CAN_BE_DERIVED

Sous frontière nette cohérente, les achats intermédiaires ne doivent pas être comptés deux fois. L’exemple brut100+150=250 contre VA100+50=150 ne réfute pas p205; il interdit une lecture brute de p559.

## WHAT_REQUIRES_INTERPRETATION

Équivalence du Money-gain au flux de valeur ajoutée, période, stocks, réemploi des paiements, déflateur et raccord des agents. Une simple constante K ne résout pas ces choix.

## WHAT_REMAINS_UNRESOLVED

Le raccord opérationnel Money/VA/PIB reste incomplet. Aucune identité nouvelle n’est introduite pour le réparer. Le test énergie primaire/PIB qualifie seulement une identification forte, non toutes les acceptions de K.
'''
write('remediation/money_gdp_bridge.md',bridge)
formal=[
dict(id='FORMAL-REMED-01',pages=[285,301,303],equation='Fp=rU; F=(p/r)U imprimé',current='Dérivation/postulat insuffisamment séparés',objection='Limite à U fixe et inversion',recalculation='r=2,U=3,p=4: F=rU/p=1.5, formule imprimée6',result='LOCAL_ERROR',condition='La relation de p301 reste une hypothèse proposée, non une démonstration'),
dict(id='FORMAL-REMED-02',pages=[538,559],equation='T=½cpω² et vitesse moyenne',current='K pondéré sous additivité',objection='Moyenne quadratique ≠ carré de moyenne',recalculation='cp=2,ω=[1,3]: mean(T)=5, T(meanω)=4; écart=variance1',result='CORRECT_WITH_CONDITION',condition='Conserver variance et composition; K peut absorber sans constance structurelle'),
dict(id='FORMAL-REMED-03',pages=[207],equation='T=½cpω²',current='Primitive à cp fixe',objection='cp variable',recalculation='dT=cpωdω+½ω²dcp; cp2→3 à ω2: variation2',result='CORRECT_WITH_CONDITION',condition='cp fixe pour primitive à un seul terme'),
dict(id='FORMAL-REMED-04',pages=[15],equation='M=nu',current='Différentielle',objection='Ne pas confondre variation finie',recalculation='ΔM=uΔn+nΔu+ΔnΔu',result='CORRECT_AS_STATED',condition='dM infinitésimal; compensation exige u dn+n du=0'),
dict(id='FORMAL-REMED-05',pages=[249,250,467,470],equation='Rapports0/0 et Force constante',current='Égalités locales généralisées',objection='Limite dépendante du chemin; constante≠nulle',recalculation='2ε/ε=2; F2×Δt3=6',result='LOCAL_ERROR',condition='Une égalité peut être postulée séparément; impulsion nulle exige Force nette nulle'),
dict(id='FORMAL-REMED-06',pages=[32,197,207],equation='(8/6)²−1',current='+78%',objection='Universalité revendiquée non testée',recalculation='7/9=0.777777…',result='CORRECT_WITH_CONDITION',condition='Tâche, cp et hypothèse quadratique fixes; NOT_GENERALIZED_EMPIRICALLY')]
js('remediation/formal_corrections.json',formal);write('remediation/formal_corrections.md','# Corrections de lecture, non réécriture des équations sources\n\nRecalculs exécutables: external_review/independent_checks.py; les résultats originaux restent archivés.\n\n'+mdtable(formal))
claims=[json.loads(l) for l in (R/'analysis/data/claims.jsonl').read_text().splitlines()]
history=[]
for c in claims:
 if c['id']=='CPC-0016':
  c['attribution_status']='ATTRIBUTION_CONFIRMED';c['formal_status']='ASSUMPTION_DEPENDENT';c['empirical_status']='NOT_IDENTIFIED'
  c['remediation']={'finding':'ER-009','reason':'Chaîne complète non mesurée; compatibilité de sous-relations non transférable au claim entier.'}
 if c['id'] in ['CPC-0041','CPC-0048']:
  p=c['source']['page'];c['source_context_extension']={'document':'Reflections_PierreCampergue.pdf','page':p,'text':pages[p],'kind':'SOURCE','finding':'ER-011'}
 if c['id']=='CPC-0035':c['scope_qualification']='NOT_GENERALIZED_EMPIRICALLY; arithmetic and conditional derivation retained; author universality p32 distinguished.'
write('analysis/data/claims.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
cores=load('research_questions/synthesis/core_claims.json')
for c in cores:
 if c['id']=='CPC-0016':
  old=c['status'][:];c['status']=[s for s in old if s!='EMPIRICALLY_COMPATIBLE']
  if 'NOT_IDENTIFIED' not in c['status']:c['status'].append('NOT_IDENTIFIED')
  c['empirical_support']='NOT_IDENTIFIED pour Work→u→Money complet; les sous-relations descriptives ne le confirment pas.';c['external_compatibility']=c['empirical_support']
  history.append(dict(id=c['id'],old_status=old,new_status=c['status'],finding='ER-009',reason=c['empirical_support']))
 if c['id'] in ['CPC-0041','CPC-0048']:c['source_context_extension']=next(x for x in claims if x['id']==c['id'])['source_context_extension']
 if c['id']=='CPC-0035':c['scope_qualification']='NOT_GENERALIZED_EMPIRICALLY; p32 revendique une généralité sous homogénéité, non établie par 7/9.'
js('research_questions/synthesis/core_claims.json',cores)
js('remediation/claim_status_history.json',history)
variables=load('research_questions/operationalization/variables.json')
for v in variables:
 if v['id']=='VAR-16':v['measurement_status']='DERIVABLE_FROM_OBSERVABLES';v['directly_observable']=False;v['remediation_note']='ER-006: série par substitution construite, indépendante du PIB; L5 reproductibilité conservé.'
 if v['id'] in ['VAR-06','VAR-23']:
  v['measurement_level']=1;v['measurement_status']='NOT_OPERATIONALIZED';v['candidate_proxy_level']=2;v['remediation_note']='ER-007: cible L1, candidats proxies L2 sans équivalence quantitative établie.'
 if v['id']=='VAR-07':v['measurement_status']='AMBIGUOUS';v['referents_source']='remediation/money_referents.json'
 if v['id']=='VAR-12':v['remediation_note']='Proxy actuellement L2; coût comptable défini pourrait être L3, pas promotion de ce proxy.'
js('research_questions/operationalization/variables.json',variables)
exps=load('research_questions/operationalization/experiments.json');byvar={v['id']:v for v in variables}
for e in exps:
 for v in e['variables']:v['measurement_level']=byvar[v['id']]['measurement_level']
js('research_questions/operationalization/experiments.json',exps)
write('research_questions/operationalization/variables.md','# Variables — état après remédiation\n\nÉtat antérieur intégral conservé dans remediation/history/. Cible et proxy sont distincts.\n\n'+mdtable(variables))
csvwrite('research_questions/operationalization/measurement_matrix.csv',[dict(id=v['id'],name=v['name'],measurement_level=v['measurement_level'],measurement_status=v['measurement_status'],candidate_proxy_level=v.get('candidate_proxy_level','NOT_ASSIGNED'),necessary_assumptions=v['necessary_assumptions']) for v in variables])

result_updates={
'SYN-01':('Cash, Money, création, transfert et redistribution restent distingués. M=n·u est une identité; neutralité conditionnelle au scénario, acteur, horizon et référent. Solde, gain, cinétique, potentiel et transfert ne sont pas unifiés sans dictionnaire.',[15,19,204,207,467],'remediation/money_referents.md'),
'SYN-06':('Le +78% reproduit (8/6)²−1 sous tâche, cp et hypothèse quadratique fixes. P32 revendique une généralité sous homogénéité; le calcul ne l’établit pas. NOT_GENERALIZED_EMPIRICALLY.',[32,197,207],'remediation/formal_corrections.md'),
'SYN-07':('Sous additivité et unités communes, K est une moyenne pondérée; invariance sous composition fixe reste conditionnelle. P559 moyenne les vitesses: moyenne des carrés ≠ carré de moyenne; conserver dispersion et coefficients avant agrégation.',[538,559],'remediation/formal_corrections.md'),
'SYN-08':('Les erreurs locales de limites, inversion p303, Force constante et substitutions restent distinctes de postulats admissibles. P301 autorise une hypothèse simplificatrice; elle ne répare pas sa dérivation. Portée strictement locale.',[249,250,285,301,303,467,470],'remediation/formal_corrections.md'),
'SYN-11':('GDP=K·W à K strictement constant et W énergie primaire est qualifié par les ratios observés. Le raccord Money/valeur ajoutée/PIB et nominal/réel reste auparavant incomplet; p205 empêche d’imputer un double compte brut inévitable.',[205,529,537,559],'remediation/money_gdp_bridge.md'),
'SYN-14':('La chaîne vers les dommages est présente; l’auteur revendique une dégradation systématique p112 et formule des généralisations p454/537. La conclusion défendable reste conditionnelle: allocation marginale et fonction de dommage non identifiées.',[112,159,271,454,460,534,537,523],'remediation/traceability_repairs.md')}
results=load('research_questions/synthesis/results.json');repairs=[]
for s in results:
 if s['id'] in result_updates:
  statement,pp,path=result_updates[s['id']];old=s['statement'];s['statement']=statement;s['source_pages']=pp
  if path not in s['sources']:s['sources'].append(path)
  repairs.append(dict(id=s['id'],before='PARTIALLY_TRACEABLE',after='TRACEABLE_WITH_EXPLICIT_LIMITS',old_statement=old,new_statement=statement,questions=s['questions'],claims=s['claims'],sources=s['sources'],pages=pp,scope='Rattachement documentaire complété; implication économique ne devient pas démontrée.'))
js('research_questions/synthesis/results.json',results);js('remediation/traceability_repairs.json',repairs)
write('remediation/traceability_repairs.md','# Six conclusions: réparation documentaire et restriction\n\nChaque ligne conserve les anciens énoncés. Les listes de claims sont des rattachements, non toutes des prémisses nécessaires. Les extraits exacts par page et le rôle probant sont dans trace_contract.json.\n\n'+mdtable(repairs))
# Narrow approved-claim/source contracts; not a general semantic oracle.
contract=[]
for s in results:
 contract.append(dict(id=s['id'],approved_statement=s['statement'],sources=s['sources'],source_pages=s['source_pages'],claims=s['claims'],questions=s['questions'],conditions='Scénario, référent, frontière et hypothèses formelles conservés; pas causalité par compatibilité.',passages=[dict(document='Reflections_PierreCampergue.pdf',page=p,quotation=pages[p],role='SOURCE_CONTEXT_NOT_AUTOMATIC_ENTAILMENT') for p in s['source_pages']],status=s['status'],external_compatibility=s['external_compatibility'],distinctive_explanation=s['distinctive_explanation']))
js('remediation/trace_contract.json',contract)

# Methodological intent: exact corpus, including counterexamples to an anti-approximation caricature.
methodpages=[15,63,79,80,109,301,303,523,535,561]
write('research_questions/methodology/corpus_passages.md','# SOURCE — passages intégraux sélectionnés\n\nRecherche lexicale sur562pages puis lecture directe des pages retenues; séparation opinion/autorité, conventions, expérience et hypothèses.\n\n'+'\n\n'.join(f'## METHOD-SOURCE-{i:02} — PDF {p}\n\nSOURCE\n\n> '+pages[p]+f'\n\nINTERPRETATION: voir epistemic_program.md et critères, sans équivalence entre intention et réussite.' for i,p in enumerate(methodpages,1)))
criteria=[
dict(id='CRITERION-01',criterion='Concordance des résultats avec faits',source_pages=[63,205],demands='Critère essentiel de l’approche',evidence='Tests descriptifs et retour à expérience revendiqués',counterevidence='T/cp/Utility non indépendamment mesurés',status='PARTIALLY_SATISFIED'),
dict(id='CRITERION-02',criterion='Concepts rationnels et cohérence analytique',source_pages=[15,63],demands='Séparer significations et déduire explicitement',evidence='Cash/Money, Work/labour et différentielle explicités',counterevidence='Référents de M, inversion303, limites285',status='PARTIALLY_SATISFIED'),
dict(id='CRITERION-03',criterion='Séparer choix humains et lois/applications',source_pages=[63,79,80],demands='Ne pas confondre choix de projet et contraintes',evidence='Exemple du viaduc et champ annoncé clairement séparés',counterevidence='P535 prescrit interdictions/sanctions malgré exclusion annoncée; applications peuvent expliquer une partie du changement de champ',status='AMBIGUOUS'),
dict(id='CRITERION-04',criterion='Mesure relative à une grandeur de même espèce',source_pages=[15,109],demands='Unité et comparaison homogènes',evidence='M=n u explicite; p109 reconnaît difficulté de Utility',counterevidence='Échelle indépendante Utility et conversion physique/économique manquent',status='PARTIALLY_SATISFIED'),
dict(id='CRITERION-05',criterion='Déclarer les hypothèses simplificatrices',source_pages=[301,303],demands='Autorise hypothèse et Product parfait comme construction',evidence='Réserves de p301/303 explicites',counterevidence='Déclaration ne démontre pas adéquation empirique; généralisations tardives plus fortes',status='SATISFIED'),
dict(id='CRITERION-06',criterion='Ne pas substituer autorité à raison',source_pages=[79,561],demands='Expliquer au-delà des doctrines et opinions dominantes',evidence='Effort de définition et formalisation explicite',counterevidence='P63 présume transférabilité du canon thermomécanique et limite la critique aux concepts initiaux; calculs locaux restent critiquables',status='PARTIALLY_SATISFIED'),
dict(id='CRITERION-07',criterion='La cohérence alléguée doit suivre les opérations exposées',source_pages=[63,301,303],demands='Cohérence du modèle analytique',evidence='Postulat Fp=rU possible et différentielles locales correctes',counterevidence='Inversion F=(p/r)U incompatible avec Fp=rU; statut limité à cette dérivation',status='NOT_SATISFIED')]
js('research_questions/methodology/criteria.json',criteria)
write('research_questions/methodology/internal_consistency_test.md','# Intention vs réussite selon critères sourcés\n\nSATISFIED concerne la déclaration locale des hypothèses, pas leur vérité; NOT_SATISFIED concerne une dérivation précise. Ne pas imposer un rejet universel des approximations absent du corpus.\n\n'+mdtable(criteria))
program='''# METHODOLOGICAL_INTENT

P561 explique l’insatisfaction personnelle devant les «makers of opinion makers» et ses lectures économiques. P79 critique la domination possible d’Autorités lorsque des opinions prennent la place de lois exprimées. Il ne s’agit pas seulement d’une accusation contre tous les économistes: le mécanisme visé est le remplacement d’une explication par autorité et doctrine.

P63 exige concepts rationnels, cohérence du modèle et concordance avec les faits; il sépare lois et applications humaines. P80 illustre le contraste par le choix d’un viaduc et les contraintes de réalisation. P15 définit une mesure par unité de même espèce.

## APPROXIMATION

La recherche sur le terme approximation ne justifie PAS «Pierre refuse toute approximation»: p168 utilise le terme dans un rapprochement des coûts. P301 accepte explicitement une hypothèse simplificatrice et p303 un Product parfait. Son intention est mieux décrite comme explication explicite et cohérente, pas absence universelle d’hypothèses.

## METHODOLOGICAL_SUCCESS

Les distinctions sont réelles, la réserve métrologique Utility p109 aussi. En revanche l’assurance de transfert du canon thermomécanique p63 ne démontre pas son adéquation; la restriction des critiques aux concepts initiaux ne soustrait pas les calculs à vérification. Les prescriptions p535 mettent en tension l’exclusion annoncée p63. Ce sont des problèmes locaux/de périmètre, non annulation du projet.

## QUESTION LINKS

RQ-01.01: périmètre; RQ-12.01: discrimination; RQ-12.03: réponse limitée. Ces questions couvrent le problème: aucune nouvelle branche ni renumérotation nécessaire. METHODOLOGICAL_VALUE = POSSIBLE; aucune originalité historique inférée de l’intention.
'''
write('research_questions/methodology/epistemic_program.md',program)
write('research_questions/methodology/README.md','# Programme méthodologique\n\n[Passages](corpus_passages.md), [reconstruction](epistemic_program.md), [test symétrique](internal_consistency_test.md). Intention et réussite distinctes; liens RQ-01.01/RQ-12.01/RQ-12.03; pas nouvelle question nécessaire.\n')
for q in ['RQ-01.01','RQ-12.01','RQ-12.03']:
 append(f'research_questions/{q}/conclusion.md','## Remédiation méthodologique\n\nVoir ../methodology/epistemic_program.md: intention de cohérence distincte de réussite; statut scientifique conservé. Critères et réserves sourcés, pas nouvelle preuve causale.')
contrib=load('research_questions/synthesis/contributions.json')
for c in contrib:
 c['remediation_status']='QUALIFIED';c['methodological_value']='POSSIBLE';c['remediation_note']='Distinction utile possible, ni supériorité mesurée ni nouveauté historique. CC-03: diagnostic du reviewer, pas contribution historique attribuée à l’auteur.' if c['id']=='CC-03' else 'Utilité de séparation possible; pas prédiction différente mesurée.'
js('research_questions/synthesis/contributions.json',contrib)
section='''## METHODOLOGICAL AND EPISTEMIC PROJECT

METHODOLOGICAL_INTENT: p63 réclame cohérence analytique et concordance avec les faits; p79/561 critique le remplacement d’une explication par opinion et autorité. P301 accepte des hypothèses simplificatrices: ne pas lui attribuer un rejet général des approximations. METHODOLOGICAL_SUCCESS: distinctions et réserves existent, mais unité des référents, mesure indépendante et dérivations locales restent problématiques. La séparation lois/applications annoncée p63 doit être confrontée aux prescriptions p535.

Audit symétrique: un critère satisfait dans son périmètre déclaratif, quatre partiels, un ambigu, un non satisfait pour une inversion locale. Dossier: [méthodologie](../methodology/README.md). Aucune originalité ni réussite empirique déduite de l’intention.

### AUTHOR_CLAIMED_GENERALITY / REVIEWER_SUPPORTED_SCOPE

L’auteur généralise les dommages p112, restreint la richesse sectorielle p534 et juge toute baisse de prix bénéfique p537. Ces affirmations sont conservées comme SOURCE, en tension avec services productifs p159/271. Le reviewer ne retient qu’une portée conditionnelle, sans réécrire l’intention de l’auteur.
'''
append('research_questions/synthesis/final_synthesis.md',section)
patchtext='## Remédiation externe — qualifications actuelles\n\n'+'\n\n'.join(s['id']+': '+s['statement'] for s in results if s['id'] in result_updates)+'\n\nCPC-0016: attribution conservée; chaîne complète NOT_IDENTIFIED. Les états historiques restent dans remediation/history; les corrections explicites prévalent sur les résumés historiques. Les tests sont des contrôles classés, pas des validations économiques.'
for name in ['root_question_answer.md','negative_results.md','final_synthesis.md']:
 append('research_questions/synthesis/'+name,patchtext)
write('research_questions/synthesis/core_claims.md','# CORE — état corrigé\n\nAttributions conservées; statut empirique CPC-0016 abaissé explicitement, historique remediation/claim_status_history.json.\n\n'+'\n\n'.join('## '+c['id']+'\n\n'+ '\n\n'.join(f'{k}: {v}' for k,v in c.items()) for c in cores))
write('research_questions/synthesis/contributions.md','# Contributions après remédiation\n\nQuatre QUALIFIED; valeur méthodologique POSSIBLE, non preuve d’originalité. CC-03 distingue diagnostic de revue et opérations de l’auteur.\n\n'+mdtable(contrib))
with (S/'master_matrix.csv').open() as f:matrix=list(csv.DictReader(f))
for row in matrix:
 item=next((x for x in cores+results+contrib if x['id']==row['Item']),None)
 if item:
  row['Status']='; '.join(item['status']) if isinstance(item['status'],list) else item['status']
  row['Empirical support']=item.get('empirical_support',item['external_compatibility'])
  row['Source']='; '.join(item.get('sources',item.get('source_artifacts',[])))
  if item['id'] in result_updates:row['Counterevidence']=item['statement']
csvwrite('research_questions/synthesis/master_matrix.csv',matrix)
manifest=load('research_questions/synthesis/manifest.json');manifest['remediation_history']='remediation/claim_status_history.json';manifest['core_classification_counts']=dict(Counter(s for c in cores for s in c['status']));manifest['remediation_status']='APPLIED_PENDING_VERIFICATION'
js('research_questions/synthesis/manifest.json',manifest)
actions=[]
for f in load('external_review/findings.json'):
 actions.append(dict(id=f['id'],severity=f['severity'],target=f['target'],problem=f['problem'],review_evidence=f['evidence'],correction_proposed=f['recommended_correction'],action='PARTIALLY_ACCEPT' if f['id']=='ER-007' else 'ACCEPT',action_taken='Cible/proxy séparés; pas promotion automatique du coût ni critère de mesure inventé.' if f['id']=='ER-007' else 'Correction documentaire ou formelle appliquée; inconnue scientifique conservée.',files_modified=[x['path'] for x in changes if not x['path'].startswith('research_questions/RQ')],claim_status_impact='CPC-0016 empirique NOT_IDENTIFIED' if f['id']=='ER-009' else 'Attribution conservée; qualifications explicites',question_status_impact='Aucune promotion; 53 questions et statuts conservés',remaining_uncertainty='La remédiation de représentation ne résout pas mesure, causalité ou histoire.',closure='CLOSED_WITH_SCIENTIFIC_LIMITS'))
js('remediation/finding_actions.json',actions)
js('remediation/applied_changes.json',changes)
print('Applied',len(changes),'changes; baseline preserved')
