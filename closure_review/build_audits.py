"""Closure judgments and structural checks, distinct from scientific proof."""
import json,csv,re,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];O=R/'closure_review'
def load(p):return json.loads((R/p).read_text())
def js(p,x):(O/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def md(p,s):(O/p).write_text(s+'\n')
def table(rows):
 keys=list(rows[0]);return '| '+' | '.join(keys)+' |\n|'+'|'.join(['---']*len(keys))+'|\n'+'\n'.join('| '+' | '.join(str(r[k]).replace('|','/').replace('\n',' ') for k in keys)+' |' for r in rows)
claims={c['id']:c for c in map(json.loads,(R/'analysis/data/claims.jsonl').read_text().splitlines())}
graph=load('research_questions/question_graph.json');nodes={q['id']:q for q in graph['nodes']};qs=load('research_questions/synthesis/questions.json')
assert len(claims)==127 and len(qs)==53 and set(q['id'] for q in qs)==set(nodes)-{'RQ-ROOT'}
question_audit=[]
for q in qs:
 text=(R/f"research_questions/{q['id']}/conclusion.md").read_text()
 header=re.search(r'## STATUS\s*\n\s*(\w+)',text).group(1)
 assert header==q['status']==nodes[q['id']]['status'],q['id']
 assert all(c in claims for c in q['claims'])
 assert nodes[q['id']]['parent'] in nodes
 question_audit.append(dict(id=q['id'],question=q['question'],status=q['status'],confidence=q['confidence'],conclusion=f"research_questions/{q['id']}/conclusion.md",current_answer=q['main_corpus_answer'],empirical_limit=q['empirical_status'],review='CONSISTENT_CURRENT',remediation_note='Direct updates or current synthesis cross-reference; earlier named passes historical.'))
for e in graph['edges']:
 # Graph uses source/target IDs, with no missing endpoints allowed.
 assert e['source'] in nodes and e['target'] in nodes
js('question_status_audit.json',question_audit)
md('question_status_audit.md','# 53 questions — clôture\n\nStatuts du graphe, de la synthèse et en-têtes des conclusions contrôlés: aucun changement de statut. Les réponses de première passe devenues obsolètes ont été archivées puis alignées sur la synthèse actuelle. Les passages de passes datées ne sont pas réécrits.\n\n'+table(question_audit))

cores=load('research_questions/synthesis/core_claims.json');proposed={c['id']:c for c in load('remediation/core_before_after.json')}
finalcore=[]
for c in cores:
 original=claims[c['id']];assert c['statement']==original['statement'] and c['source']==original['source']
 assert all(x in claims for x in original['depends_on'])
 status={'REVIEWER_CONFIRMS':'CONFIRMED','REVIEWER_QUALIFIES':'QUALIFIED','REVIEWER_CANNOT_DETERMINE':'UNDETERMINED','REVIEWER_DISPUTES':'DISPUTED'}[proposed[c['id']]['remediation_after']]
 related=[f['id'] for f in load('external_review/findings.json') if c['id'] in f['claim_question']]
 if c['id']=='CPC-0016':assert 'NOT_IDENTIFIED' in c['status'] and 'EMPIRICALLY_COMPATIBLE' not in c['status']
 if c['id'] in ['CPC-0041','CPC-0048']:assert c.get('source_context_extension')
 finalcore.append(dict(id=c['id'],claim=c['statement'],source=c['source'],scientific_status=c['status'],closure_status=status,qualification=c['global_qualification'],remediation=c.get('scope_qualification',c.get('empirical_support')),related_findings=related,dependencies=original['depends_on'],root_impact=original['root_question_relevance'],reason='Current scope matches sourced attribution and explicit limits; confirmation is not an empirical truth certificate.'))
js('core_claims_final.json',finalcore)
md('core_claims_final.md','# 24 CORE — état final de clôture\n\n9 CONFIRMED,14 QUALIFIED,1 UNDETERMINED,0 DISPUTED. La clôture confirme le reclassement documentaire proposé, non une observation nouvelle. CPC-0016 est conservé mais sa chaîne complète non identifiée.\n\n'+'\n\n'.join('## '+c['id']+'\n\n'+'\n\n'.join(f'{k}: {v}' for k,v in c.items()) for c in finalcore))

actions=load('remediation/finding_actions.json');findings=[]
residuals={1:'Généralité de l’auteur désormais explicite; sa justification reste ouverte.',2:'Raccord net Money/VA/PIB demeure incomplet; CPC-0118 est la cible correcte.',3:'Six référents distingués sans prouver leur équivalence.',4:'Erreur locale conservée comme erreur; postulat non validé par réparation.',5:'Moments/dispersion et composition restent à mesurer.',7:'Cibles L1/proxies candidats L2; validité de correspondance ouverte.',8:'Contrats et mutations ne font pas une preuve sémantique; SYN-08 reste composite.',10:'Universalité empirique non acquise malgré calcul exact.'}
for a in actions:
 for path in a['files_modified']:assert (R/path).is_file()
 n=int(a['id'][3:]);finding=dict(a)
 finding['closure_status']='CLOSED_WITH_RESIDUAL_UNCERTAINTY' if n in residuals else 'CLOSED'
 finding['closure_evidence']='Files inspected, current JSON/Markdown agreement, targeted tests executed separately; see final_verification.json.'
 finding['remaining_uncertainty']=residuals.get(n,'Correction documentaire spécifique effectivement appliquée; aucune promotion scientifique.')
 findings.append(finding)
js('findings_closure.json',findings)
md('findings_closure.md','# Clôture des 12 findings\n\nCLOSED décrit la correction, non la résolution d’un système entier.\n\n'+table([dict(id=f['id'],severity=f['severity'],decision=f['action'],status=f['closure_status'],applied=f['action_taken'],files=f['files_modified'],residual=f['remaining_uncertainty']) for f in findings]))

chain=load('research_questions/synthesis/root_question_chain.json')
states=['QUALIFIED','NOT_IDENTIFIED','ROBUST_WITHIN_SCOPE','QUALIFIED','NOT_IDENTIFIED','QUALIFIED','QUALIFIED','QUALIFIED','MISSING','MISSING','AMBIGUOUS']
links=[(['RQ-01.03','RQ-09.01'],['CPC-0018','CPC-0029']),(['RQ-09.02'],['CPC-0119']),(['RQ-04.01','RQ-04.02'],['CPC-0096']),(['RQ-05.01'],['CPC-0097','CPC-0098']),(['RQ-06.01','RQ-05.03'],['CPC-0015','CPC-0100']),(['RQ-10.02'],['CPC-0099','CPC-0127']),(['RQ-11.01'],['CPC-0120']),(['RQ-11.03'],['CPC-0120']),(['RQ-10.02'],['CPC-0127']),(['RQ-11.03'],['CPC-0120']),(['RQ-09.03','RQ-08.02'],['CPC-0117','CPC-0118'])]
root=[]
for x,status,(rq,cs) in zip(chain,states,links):
 root.append(dict(id=x['id'],link=x['link'],source_pages=x['source_pages'],questions=rq,claims=cs,status=status,limit=x['qualification'],causal_identification='NOT_IDENTIFIED',scope='Conditional local cost arithmetic only' if status=='ROBUST_WITHIN_SCOPE' else 'Textual narrative/qualification, not demonstrated historical causality'))
js('root_question_closure.json',root)
md('root_question_closure.md','# Question racine — revue de clôture\n\nLa réponse actuelle distingue le corpus, les conditions et l’absence d’identification. Aucun renforcement. Les rattachements ci-dessous précisent la chaîne; CPC-0001 reste la racine mais n’est pas la seule preuve des11flèches.\n\n'+table(root)+'\n\nLa source p112 formule des nécessités plus fortes que la réponse conditionnelle du reviewer. Cette différence est explicitement conservée. ROBUST_WITHIN_SCOPE porte sur un calcul de coût sous hypothèses, pas sur la transition historique entière.')

criteria=load('research_questions/methodology/criteria.json')
source=(R/'research_questions/methodology/corpus_passages.md').read_text()
for c in criteria:
 for p in c['source_pages']:
  assert f'PDF {p}' in source or p==205,p
md('methodological_closure.md','# Projet méthodologique\n\nMETHODOLOGICAL_INTENT ≠ METHODOLOGICAL_SUCCESS. Sources p15,63–65,79–80,109,301/303,561–562; prescriptions p535 conservées comme tension de périmètre. Le corpus admet des hypothèses simplificatrices; rejet universel des approximations non attribué. Les citations de Besnier/Keynes rapportées en p562 restent des citations dans le corpus, non une vérification historique externe.\n\n'+table(criteria)+'\n\nRépartition confirmée:1SATISFIED (déclaration locale des hypothèses),4PARTIALLY_SATISFIED,1AMBIGUOUS,1NOT_SATISFIED (inversion locale). Aucun score global.')
page205=next(p for p in map(json.loads,(R/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines()) if p['page_pdf']==205)
quote='we must always rely on experience, that is to say, on the reality of economic life'
assert quote in ' '.join(page205['text'].split())
with (O/'methodological_closure.md').open('a') as f:f.write('\n\n## Complément de provenance CRITERION-01\n\nSOURCE — Reflections_PierreCampergue.pdf, p205: «'+quote+'».\n\nINTERPRETATION: cette référence du critère n’était pas reproduite dans le dossier méthodologique; elle est vérifiée ici dans le texte extrait. Cela documente une exigence, non sa satisfaction empirique.\n')

scenarios=load('analysis/data/money_compensation_scenarios.json')['scenarios']
assert len(scenarios)==32
money=load('remediation/money_referents.json');assert len(money)==6
md('money_final_audit.md','# Dernier audit Money\n\n32scénarios présents; six référents analytiques conservés. Leurs noms ne sont pas introduits comme notations originales de l’auteur.\n\n'+table(money)+'\n\nM=n·u: identité; compensation exige conditions. Création de dépôts bancaires ≠ Money automatiquement; table de traduction research_questions/contribution/cash_money_crosswalk.md. Pont Money/VA/PIB: incomplet; restriction nette p205 conservée, généralisation p559 distincte. Crédit et paiements ne mesurent pas indépendamment Money. Tests de provenance des32scénarios réexécutés dans verify; aucune équivalence artificielle ajoutée.')
formal=load('remediation/formal_corrections.json')
md('formal_final_audit.md','# Formalisme — périmètre limité aux problèmes connus\n\n'+table([dict(id=f['id'],source=f['pages'],ORIGINAL_ISSUE=f['objection'],REMEDIATION=f['recalculation'],CURRENT_STATUS=f['result'],RESIDUAL_RISK=f['condition']) for f in formal])+'\n\nUtility: ordre insuffisant à certains ratios; coefficients peuvent covarier dans d’autres opérations. Potentiels/agrégation: exactitude, unité et frontière sont des conditions, pas résultats empiriques. T/dT: niveau, transfert et réserve séparés, pas un référent global imposé. +78%: arithmétique, hypothèse quadratique et non-généralisation empirique conservées. Les sept mutants ciblés vérifient la conservation de ces énoncés, non leur vérité universelle.')

contrib=load('research_questions/synthesis/contributions.json')
for c in contrib:
 assert not c['originality_asserted'] and not c['different_testable_prediction_established']
 c['closure_status']='SURVIVES_QUALIFIED';c['novelty_final']='UNRESOLVED';c['formal_value']='Diagnostic/restriction locale conditionnelle; pas mesure indépendante.'
js('contributions_final.json',contrib)
md('contributions_final.md','# Quatre candidats\n\nQuatre SURVIVES_QUALIFIED; nouveauté UNRESOLVED. CC-03 demeure diagnostic de revue, non innovation attribuée à Pierre.\n\n'+table([dict(id=c['id'],definition=c['title'],pages=c['source_pages'],comparisons=c['literature'],survives=c['difference'],conceptual=c['conceptual_clarity'],formal=c['formal_value'],empirical=c['empirical_value'],methodological=c['methodological_value'],limit=c['limit'],status=c['closure_status'],novelty=c['novelty_final']) for c in contrib]))

results=load('research_questions/synthesis/results.json');contract={c['id']:c for c in load('remediation/trace_contract.json')};traces=[]
for s in results:
 assert s['statement']==contract[s['id']]['approved_statement']
 for path in s['sources']:assert (R/path).exists()
 traces.append(dict(id=s['id'],conclusion=s['statement'],status='PARTIAL' if s['id']=='SYN-08' else 'COMPLETE',questions=s['questions'],claims=s['claims'],pages=s['source_pages'],evidence=s['sources'],missing='Lien atomique entre chaque sous-erreur, son équation et son propre claim/test; pages et diagnostics disponibles mais regroupement encore composite.' if s['id']=='SYN-08' else 'Aucun chaînon documentaire manquant identifié; absence de preuve empirique peut rester le résultat tracé.',scope='Recoverable documentary chain, not full empirical demonstration'))
js('traceability_final.json',traces)
md('traceability_final.md','# 14 conclusions — jugement de clôture\n\n13COMPLETE,1PARTIAL,0BROKEN. La remédiation annonçait14chaînes documentées: cette propriété n’implique pas14traçabilités atomiques complètes. SYN-08 reste composite, sans source inventée pour gonfler le score. Les liens fins complémentaires se trouvent dans remediation/trace_edges.json; pour +78%, RQ-04.02 est la question primaire, RQ-04.04 un voisinage des rendements.\n\n'+table(traces))

opens=[('FORMAL','Référents T, dT, réserve et transfert: raccords cohérents','RQ-03.02'),('METROLOGICAL','Étalonnage indépendant de cp et Force','RQ-03.03'),('METROLOGICAL','Échelle de Utility compatible avec ratios et contexte','RQ-05.03'),('METROLOGICAL','Mesure des différents référents Money sans les confondre','RQ-06.01'),('FORMAL','Money/VA/PIB: net, période, prix réels, double compte','RQ-09.03'),('FORMAL','K: dispersion, composition, coefficients et unités','RQ-08.02'),('FORMAL','Potentiels: intégrabilité, domaine et contraintes','RQ-08.03'),('EMPIRICAL','Variables appariées coût/prix/qualité/marge','RQ-05.01'),('CAUSAL','Sélection préalable de scénario et usage marginal du gain','RQ-10.02'),('EMPIRICAL','Panier marginal, matières/énergie et importations','RQ-11.03'),('CAUSAL','Exposition et fonction de dommages du panier','RQ-11.01'),('CAUSAL','Conversion travail physique utile→Economic Work','RQ-09.02'),('CAUSAL','Signature indépendante discriminant les explications','RQ-12.01'),('HISTORICAL','Subsistance, seuils, chronologie et alternatives institutionnelles','RQ-01.03'),('HISTORICAL','Nouveauté historique et utilité décisionnelle comparée','RQ-12.03')]
js('final_open_questions.json',[dict(type=a,question=b,related_rq=c) for a,b,c in opens]);md('final_open_questions.md','# Quinze inconnues prioritaires\n\n'+table([dict(type=a,question=b,related_rq=c) for a,b,c in opens])+'\n\nLa complétude documentaire n’exige pas leur résolution. Aucune expérience lourde ni revue bibliographique nouvelle menée ici.')
md('history_audit.md','# Histoire conservée\n\nLes snapshots de Money, scénarios, claims et lectures précédentes restent dans analysis/history et research_questions/history. La revue externe demeure inchangée. remediation/history préserve l’état avant correction; claim_status_history.json conserve CPC-0016; applied_changes.json et input_refresh_history.json enregistrent les ajouts. Les corrections de clôture sont dans editorial_changes.json avec copies complètes dans closure_review/history. Les protocoles d’expériences figés (notamment Utility L2 lors de rédaction) restent HISTORICAL_ONLY, non niveaux actuels.\n\nLa baseline finale vérifie les empreintes; elle ne réécrit pas un état historique comme s’il avait toujours été corrigé.')
js('audit_counts.json',dict(findings=dict(Counter(f['closure_status'] for f in findings)),core=dict(Counter(c['closure_status'] for c in finalcore)),questions=dict(Counter(q['status'] for q in qs)),traceability=dict(Counter(t['status'] for t in traces)),contributions=dict(Counter(c['closure_status'] for c in contrib)),methodology=dict(Counter(c['status'] for c in criteria))))
print((O/'audit_counts.json').read_text())
