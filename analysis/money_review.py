"""Versioned editorial inputs and deterministic compilation of the targeted review.

Run once against the archived iteration-1 baseline. Refuses to overwrite its output.
Source excerpts are sliced from the existing deterministic extraction, never invented.
"""
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def load(p): return json.loads((ROOT/p).read_text())
def dump(p,x):
    q=ROOT/p; q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def write(p,t):
    q=ROOT/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(t)
P={x['page_pdf']:' '.join(x['text'].split()) for x in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
def src(page,anchor,length=360):
    text=P[page]; start=text.index(anchor); end=min(len(text),start+length)
    if end<len(text): end=text.rfind(' ',start,end)
    return dict(document='Reflections_PierreCampergue.pdf',page=page,pages=[page],quotation=text[start:end],normalization='whitespace')

# Each row is an editorial reconstruction, NOT a quotation. Four boundary cases
# are analytical possibilities, NOT observations or empirical refutations.
# label, name, page, literal source anchor, conditions, mechanism, result, limits
ROWS=[
('1','Stabilité globale',172,'In this case the number of units is constant','M et n constants; système entier','Aucune variation globale; redistribution interne possible','u constant','État stationnaire fonctionne; choc productif le quitte; répartition peut changer; agrégation inconnue empêche de conclure.'),
('2a','Émission à Money constant',173,'In this case the number of units is variable','M constant, n croissant, sans création productive','Compensation inverse de u; interprétée comme ajustement des prix','u décroît; M final inchangé','Renumérotation inverse fonctionne; prix rigides empêchent la compensation immédiate; quantité produite peut réagir; horizon final non défini.'),
('2b','Retrait et remboursement à Money constant',18,'Conversely, the repayment of a loan','M constant, n décroissant','Retrait des unités; appréciation inverse postulée','u augmente; pas de destruction de Money','Conversion inverse fonctionne; défaut bancaire ne ressemble pas au remboursement; bilan/crédit peuvent absorber le choc; panier et horizon manquants.'),
('3a','Création productive sans émission',19,'if yesterday a 1$ coin','n constant; produit comparable, baisse du prix transmise au consommateur','Work supplémentaire → productivité → prix inférieur → pouvoir d’achat','u et M augmentent','Panier fixe moins cher fonctionne; marge accrue sans baisse du prix interrompt la chaîne; qualité/quantités peuvent varier; effet agrégé non donné par un seul prix.'),
('3b','Destruction à nombre constant',178,'Analytical possibilities 3 and 4 above','n constant; destruction productive/prix en hausse','Diminution de Work et hausse des prix décrites comme destruction','u et M diminuent','Même panier plus cher réduit le pouvoir d’achat; hausse de qualité invalide la comparaison brute; substitution absorbe une partie; cause de la hausse indéterminée.'),
('4a','Émission accompagnant une création préalable',177,'Since by an increase of the Work performed','M augmente productivement; émetteur calibre n pour garder u constant','Émission proportionnée à Money déjà créé; distribution distincte','n et M augmentent, u constant','M=100→110,n=100→110,u=1 fonctionne; surémission quitte le cas; u absorbe une erreur de calibration; mesure indépendante de M nécessaire.'),
('4b','Retrait accompagnant une destruction',178,'Analytical possibilities 3 and 4 above','M diminue; retrait calibré, u maintenu constant','Symétrique négatif de 4a explicitement admis','n et M diminuent, u constant','M=100→90,n=100→90,u=1 fonctionne; retrait excessif quitte le cas; u ou activité peuvent varier; règle de calibration non fournie.'),
('2a1','Inflation dite incohérente',24,'As the number n increases','n augmente, u baisse insuffisamment selon la comparaison du manuscrit','Gain consommateur, consommation accrue, perte fournisseur; g variable aux pages 526–532','Enrichissement du consommateur puis désorganisation alléguée','n=110,u=.95 donne M=104.5; u=.8 ne donne pas ce gain; marges/emploi peuvent absorber; unités et pondérations de |dn| versus |du| non définies.'),
('2a2','Dévaluation correctrice',25,'It is therefore necessary for the unit u','Suite de 2a1; u baisse plus fortement que n ne croît','Perte compensant le gain jugé indu; retour obligatoire affirmé','Destruction du supplément, retour de référence','n=110,u=.8 donne M=88; baisse trop faible ne corrige pas; n/g peuvent aussi changer; référence et délai absents.'),
('2b1','Déflation dite incohérente',25,'Since the number n decreases','n baisse, u augmente insuffisamment selon le manuscrit','Consommation moindre malgré avantage initial fournisseur; g variable','Appauvrissement consommateur, activité puis emploi menacés','n=90,u=1.05 donne M=94.5; u=1.2 inverse le résultat; stocks/production peuvent réagir; emploi non déduit de l’identité.'),
('2b2','Réévaluation correctrice',25,'The undervaluation of the Money','Suite de 2b1; appréciation de u supérieure au retrait de n','Restitution du pouvoir d’achat antérieurement perdu','Retour au niveau de référence affirmé','n=90,u=1.2 donne M=108; appréciation insuffisante ne restaure pas; g varie; référence et délai non définis.'),
('U1','Prix et utilité baissent : enrichissement',291,'This hypothesis indicates that the majority','Force FA constante; produits moins prioritaires accessibles','Extension des besoins satisfaits à revenu donné','Enrichissement; rP constant dans le tableau','Panier élargi à prix plus faibles convient; qualité perdue contredit la lecture; composition du panier absorbe; utilité interpersonnelle non mesurée.'),
('U2','Prix baisse et utilité augmente : déflation',291,'despite a fall in prices','FA constante; besoins satisfaits plus indispensables','Baisse de prix ne suffit pas; rP diminue pour rétablir la Core Law (292–293)','Déflation, pas enrichissement automatique','Revenu diminuant plus que les prix convient; revenu stable et même panier ne suffit pas; complexité absorbe; relation avec 2b1 à établir.'),
('U3','Prix augmente et utilité baisse : inflation',291,'This hypothesis corresponds to the common case','FA constante; besoins moins prioritaires encore accessibles','Achats devenant difficiles; rP augmente (292–293)','Pouvoir d’achat décroissant dans ce passage','Revenu fixe/prix croissants convient; hausse compensatrice du revenu change le résultat; qualité/gadgets absorbent; tension avec gain du consommateur p24 non résolue.'),
('U4','Prix et utilité augmentent : appauvrissement',291,'Conversely to case 1','FA constante; retour aux besoins indispensables','Produits plus chers et priorités plus urgentes','Appauvrissement; rP constant dans le tableau','Panier contraint convient; meilleurs produits sans privation ne suffit pas; composition absorbe; choix volontaires et nécessité non distingués empiriquement.'),
('DENOM','Changement de dénomination',174,'Two typical examples of this case','Conversion de tous les montants par un même facteur; pas de transformation réelle','Ancien/nouveau franc; franc/euro comme illustration de 2b','n divisé, u multiplié; richesse inchangée','Conversion exhaustive fonctionne; arrondis et contrats non convertis rompent la pure équivalence; prix affichés absorbent; effets institutionnels non isolés.'),
('REDIST','Redistribution entre agents',173,"if some agents have increases in income",'M global constant; système isolé, prélèvements et transferts','Gain de certains payé par les autres','Richesse globale constante, distribution variable','Transfert fermé fonctionne; réponse productive viole toutes choses égales; consommation/marges peuvent changer; incidence réelle et effets ultérieurs ouverts.'),
('CREDIT','Attribution exclusive du crédit bancaire au cas 2',98,"a banker's professional actions",'Crédit non couvert classé uniquement en 2; refus uniquement en 1','Banque crée Cash/n, pas Work; impossibilité de 3/4 affirmée page99','Pas de création de Money par le crédit selon Campergue','Inscription sans production instantanée compatible; investissement ultérieur exige de distinguer financement et production; remboursement peut absorber dépôts; compensation réelle finale non établie par bilan seul.'),
('LAG','Inertie et compensation différée',175,'Of course, any economic system has a certain inertia','Revenus immédiats, prix retardés; clôture globale annoncée','Gain temporaire puis impoverishment compensatrice','Résultat final rigoureusement nul affirmé, non instantané','Hausse puis restitution exacte convient; persistance productive/institutionnelle empêche cette clôture; emploi/actifs peuvent absorber; horizon absent rend le test incomplet.'),
('CONF','Support métallique, surémission et confiance',101,'As long as the number','Sans Work; émission au-delà des stocks ou découverte massive d’or','Baisse proportionnelle de u; confiance tenue pour conséquence, non cause','M supposé constant quelle que soit la nature de Cash','Conversion de support à quantité réelle fixe convient; choc de demande de liquidité remet en cause causalité unidirectionnelle; prix du métal/usages industriels absorbent; récit Law non vérifié historiquement ici.'),
('HYPER','Vitesse des prix dépassant la consommation',26,'As long as the speed of price increases','Comparer vitesse de hausse des prix et délai de dépense','Consommateurs gagnants deviennent perdants faute de dépenser assez vite','Hyperinflation définie comme limite temporelle','Érosion avant achat convient; indexation immédiate peut compenser; fuite vers biens/devise absorbe; seuil quantitatif non défini.'),
('HOARD','Money créé non entièrement dépensé',523,'However, the created Money','Création antérieure à usage; Mc et Md distincts','Thésaurisation admise: Mc ≥ Md','Pas d’égalité obligatoire création/dépense','Mc=100,Md=80 convient; dépense financée par stock antérieur exige périmètre temporel; stock absorbe; différencier une inégalité ne préserve pas automatiquement son signe.'),
('FX','Revenu et prix fixes : intérieur et extérieur',183,'Some might indeed think','Revenu augmente à prix constants; distinction pays/devise','Équivalence intérieure admise, dévaluation extérieure nécessaire affirmée','Avantage intérieur opposé à compensation extérieure','Revenu/prix améliore bien pouvoir d’achat intérieur; régime de change fixe ne réalise pas mécaniquement dévaluation; réserves/commerce peuvent absorber; sens de dévaluation et horizon manquants.'),
('MIX','Combinaison quotidienne des possibilités',18,'The various developments represented','Plusieurs opérations/régimes; pas une seule expérience toutes choses égales','Composition des possibilités 1–4 explicitement admise','n,u,M observés agrégés peuvent combiner plusieurs effets','Somme d’opérations bien délimitées convient; attribuer tout changement à n seul échoue; composition sectorielle absorbe; décomposition non unique.'),
('SPEC','Couplage spéculateur–fournisseur et coefficients',533,'If we assume a speculator','2b1 M→T couplé à 2b2 T→M; coefficients variables','Md baisse,gMT monte,Tc constant; Td augmente,gTM baisse,Mc constant','Transfert et inégalités accrus','Produits gTM.Td et gMT.Md constants peuvent convenir; productivité simultanée quitte ce cas; g absorbe; confusion niveau constant/quantité créée nulle dans le texte.'),
('EXCLUDED','Variations simultanées de même signe exclues',30,'The dark shaded areas','dn et du tous deux positifs ou négatifs','Exclusion invoquant la conservation, non l’identité seule','Cas déclaré strictement impossible','Interdiction cohérente sous restriction explicite; n=110,u=1.1 respecte pourtant M=n.u; plusieurs chocs peuvent se combiner; tension avec MIX à résoudre.'),
('MARGIN','Coût décroissant, prix de vente constant',20,'if the selling price is kept constant','Coût baisse mais entrepreneur maintient prix','Décomposition en baisse productive puis hausse comptable','Gain non automatiquement transmis au consommateur','Marge qui augmente convient; concurrence imposant baisse quitte le cas; profit/salaire absorbe; séquence contrefactuelle pas observation de deux prix successifs.'),
('AGG','Prix local et nombre global N',537,'However, the number n of units','n de transformation distinct de N du système','Pondération locale/globale proposée; limite macro explicite page538','Ne pas identifier un prix local au pouvoir d’achat national','Panier pondéré serait opérationnel; utiliser un seul prix échoue; autres prix/poids absorbent; formules pages23,214,537 à réconcilier.'),
]

OLD='M=n.u ne démontre pas la neutralité : la compensation inverse constitue une hypothèse supplémentaire.'
NEW=('Campergue distingue Money global constant et variable. À M constant, la compensation inverse est une conséquence conditionnelle; à M variable, il traite la variation de u à n constant et l’ajustement de n maintenant u constant après création ou destruction productive. Il admet redistribution, inertie, combinaisons et évolutions dites incohérentes. La critique porte sur la justification et la sélection de ces conditions, les mécanismes et horizons de retour, non sur une déduction uniforme de neutralité à partir de M=n.u seul.')

def main():
    if (ROOT/'analysis/data/money_compensation_scenarios.json').exists():
        if '--finish-interrupted-build' in sys.argv and not (ROOT/'analysis/24_money_compensation_scenarios.md').exists():
            data=load('analysis/data/money_compensation_scenarios.json')
            claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
            return finish(claims,data['scenarios'],load('analysis/data/money_claim_revision_log.json')['reviewed'],data['previous_finding'],load('analysis/data/argument_graph.json'))
        raise SystemExit('Revision already compiled. Edit with explicit history; do not overwrite.')
    paths=['analysis/data/claims.jsonl','analysis/data/argument_graph.json','analysis/data/research_chapters.json','analysis/data/concepts.json','analysis/data/core_reviews.json','analysis/data/literature_map.json','analysis/data/page_coverage.json','analysis/data/phase2_progress.json','analysis/data/research_questions.json','analysis/data/hypotheses.json','analysis/data/claim_chapter_matrix.csv','analysis/chapters/CH02_monetary_measurement.md']
    for p in paths:
        target=ROOT/'analysis/history/pre_money_review'/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,target)
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    byid={c['id']:c for c in claims}
    scenarios=[]
    existing={'2a':'CPC-0012','3a':'CPC-0016','2a1':'CPC-0025','2b1':'CPC-0026','REDIST':'CPC-0014','CREDIT':'CPC-0013','MARGIN':'CPC-0020'}
    for num,(label,name,page,anchor,conditions,mechanism,result,limits) in enumerate(ROWS,1):
        sid=f'SC-MONEY-{num:02d}'; source=src(page,anchor)
        c=existing.get(label)
        if c is None:
            c=f'CPC-{len(claims)+1:04d}'
            claim=dict(id=c,statement=f'{name} : {result}, sous les conditions du scénario {sid}.',source=source,
                source_document=source['document'],page=page,quotation=source['quotation'],type='HYPOTHESIS',epistemic_status='SOURCE',interpretive=True,
                concepts=['money','unit','cash','purchasing'],depends_on=['CPC-0010'],supports=[],contradicts=[],criticality='MAJOR',
                testability='SCENARIO_CONDITIONAL_REVIEW_NOT_EMPIRICALLY_TESTED',root_question_relevance='Distinguer enrichissement productif, mesure et redistribution avant de répondre à la question racine.',
                interpretation_notes=f'Reconstruction ciblée, scénario {sid}; ni citation française ni validation empirique.',confidence_in_reconstruction=.8,money_scenarios=[sid])
            claims.append(claim);byid[c]=claim
        parts=limits.split('; ')
        scenarios.append(dict(id=sid,author_label=label,name=name,level='ELEMENTARY' if num<=11 else 'PRICE_UTILITY' if num<=15 else 'APPLICATION_OR_BOUNDARY',
            pages=[page],sources=[source],variables=['M','n','u'] if num<=11 else ['M','n','u','price','purchasing_power','Work','g','Utility'],
            initial_state=conditions,applied_change=name,fixed_variables=conditions,adjusted_variables=result,
            mechanism=mechanism,expected_result=result,conditions=conditions,exceptions=limits,
            identity_or_definition='M=n.u; dM=n.du+u.dn. Cette identité ne fixe pas le chemin temporel.',
            behavioral_assumption=conditions,causal_mechanism=mechanism,derived_consequence=result,
            generalization='Portée revendiquée à contrôler dans le passage; ne pas exporter à tous les régimes.',
            relation_to_identity='Branche conditionnelle, pas preuve autonome de neutralité.',
            relation_to_Money='M désigne la valeur réelle de Cash dans ce vocabulaire.',
            relation_to_Cash='Support/inscription et valeur distingués; n compte des unités, pas des objets physiques.',
            relation_to_purchasing_power=result,scope_by_author='Voir conditions, passage et contexte; classifications de niveaux différents non exclusives.',
            interpretation=mechanism,fragility=limits,interpretive=True,claims=[c],
            boundary_cases=dict(works=parts[0],does_not_work=parts[1],other_adjustment=parts[2],indeterminate=parts[3],epistemic_status='ANALYST_HYPOTHETICAL_NOT_EMPIRICAL')))
    # Extra evidence distinguishing source, summary and contextual quotations.
    extras={'2a':[(172,'Since the overall quantity'),(175,'Consequently, if nothing else changes')],
      '4a':[(17,'It should be noted that possibility 4'),(18,'Once this creation has taken place')],
      '3b':[(16,'3b.')],'4b':[(16,'4b.')],
      '2a1':[(526,'However, it is possible to envisage'),(532,'It is very clear')],
      '2a2':[(535,'As these developments are abnormal')], '2b2':[(26,'It is therefore necessary')],
      'U2':[(292,'the only solution is to change'),(293,'It should be noted')],
      'U3':[(292,'the only solution is to change'),(293,'For everyday Consumer Products')],
      'CONF':[(100,'From this paragraph it can be concluded')], 'MIX':[(182,'In everyday reality')], 'AGG':[(538,'If we consider a complex')]}
    for s in scenarios:
        for p,a in extras.get(s['author_label'],[]):s['sources'].append(src(p,a))
        s['pages']=sorted({q['page'] for q in s['sources']})
        for q in s['sources']:
            pos=P[q['page']].index(q['quotation'])
            q['context_before']=P[q['page']][max(0,pos-240):pos]
            q['context_after']=P[q['page']][pos+len(q['quotation']):pos+len(q['quotation'])+240]
            q['argument_function']=s['mechanism']
    revisions={
      'CPC-0005':('QUALIFY','Le manuscrit affirme que modifier seulement le nombre d’unités, sans Work productif, ne crée pas de richesse globale; il distingue cependant émission accompagnant une création, inertie et évolutions incohérentes.',[172,175,177,182]),
      'CPC-0012':('SPLIT','À Money global constant (hypothèse 1, possibilité 2), la variation de n est compensée inversement par u; l’attribution du crédit à cette branche et son extension finale sont des thèses distinctes.',[172,173,175,177]),
      'CPC-0013':('QUALIFY','Campergue classe le crédit non couvert uniquement dans la possibilité 2 : création de Cash, pas de Money; ce classement exclut la possibilité 4 pour le banquier et constitue une restriction causale.',[98,99,174,175,177]),
      'CPC-0014':('QUALIFY','Dans le système isolé et sans Work supplémentaire, une politique redistribue selon Campergue Money sans enrichissement global; les effets internes et transitoires ne sont pas niés.',[173,175,182]),
      'CPC-0016':('QUALIFY','Le mécanisme productif proposé relie Work supplémentaire, productivité et baisse de prix à Money accru : u augmente à n constant (3a), ou n est ensuite ajusté pour stabiliser u (4a).',[17,18,176,177,214]),
      'CPC-0025':('QUALIFY','Dans l’inflation dite incohérente 2a1, le consommateur gagne si la baisse de u ne compense pas sa hausse de n; le manuscrit distingue consommateurs, fournisseurs et épargnants et propose une correction ultérieure.',[24,25,26,532]),
      'CPC-0026':('QUALIFY','Dans la déflation dite incohérente 2b1, l’appréciation de u ne compense pas la baisse de n du consommateur; une réévaluation correctrice 2b2 est ensuite affirmée.',[25,26,532]),
    }
    reviewed=[]
    topics={'money','cash','unit','purchasing','inflation','deflation','creation','distribution','price','accounting','wealth'}
    for c in claims[:68]:
        if not topics.intersection(c['concepts']):continue
        old=c['statement']; action='KEEP'; reason='Énoncé local conservé; aucune neutralité générale ajoutée.'; pages=[]
        if c['id'] in revisions:
            action,c['statement'],pages=revisions[c['id']]
            reason='Retour au contexte et séparation des scénarios auparavant aplatis; citation initiale conservée comme preuve de la formulation forte du manuscrit.'
        linked=[s['id'] for s in scenarios if c['id'] in s['claims']]
        if c['id']=='CPC-0005':linked=[s['id'] for s in scenarios[:11]]
        c['money_scenarios']=linked
        if action!='KEEP':
            c['interpretation_notes']+=' Révision monétaire 2026-09-08 : '+reason
            c['additional_source_pages']=pages
        reviewed.append(dict(claim_id=c['id'],action=action,old_statement=old,new_statement=c['statement'],reason=reason,
            new_sources=[q for s in scenarios for q in s['sources'] if q['page'] in pages],scenarios=linked))
    byid['CPC-0012']['depends_on']=['CPC-0011',scenarios[0]['claims'][0]]
    byid['CPC-0013']['type']='HYPOTHESIS'
    for c in claims:
        c['source'].setdefault('pages',[c['source']['page']])
    write('analysis/data/claims.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
    dump('analysis/data/money_claim_revision_log.json',dict(date='2026-09-08',reviewed=reviewed,new_claims=[c['id'] for c in claims[68:]],actions=dict(Counter(r['action'] for r in reviewed))))
    finding=dict(old_statement=OLD,status='OVER_SIMPLIFIED',new_statement=NEW,reason='Vrai comme non-implication algébrique; incomplet comme représentation du manuscrit, qui expose explicitement conditions et ajustements multiples.',sources=[src(172,'Since the overall quantity'),src(177,'Since by an increase'),src(175,'Of course, any economic system'),src(182,'In everyday reality')])
    dump('analysis/data/money_compensation_scenarios.json',dict(status='QUALIFIED',exhaustiveness='Inventory of detected cases; targeted search is not proof of exhaustive reading of 562 pages.',previous_finding=finding,scenarios=scenarios))
    # Dependencies are scoped through scenario nodes. Relations are reconstruction,
    # not certifications of mathematical implications.
    graph=load('analysis/data/argument_graph.json')
    removed=[e for e in graph['edges'] if e['source']=='CPC-0012' and e['relation']=='DEPENDS_ON']
    graph['edges']=[e for e in graph['edges'] if e not in removed]
    for c in claims[68:]:graph['nodes'].append(dict(id=c['id'],kind=c['type']))
    for n in graph['nodes']:
        if n['id'] in byid:n['kind']=byid[n['id']]['type']
    for s in scenarios:
        graph['nodes'].append(dict(id=s['id'],kind='MONETARY_SCENARIO',conditions=s['conditions']))
        for a,b,r in [(s['id'],'CPC-0010','DEPENDS_ON'),(s['id'],s['claims'][0],'EXEMPLIFIES')]:
            graph['edges'].append(dict(source=a,target=b,relation=r,evidence=s['sources'][0],interpretive=True,conditions=s['conditions']))
    for c in claims[68:]+[byid['CPC-0012']]:
        for dep in c['depends_on']:graph['edges'].append(dict(source=c['id'],target=dep,relation='DEPENDS_ON',evidence=c['source'],interpretive=True,conditions='Voir scénario monétaire associé; pas de neutralité générale.'))
    graph['money_review']=dict(status='QUALIFIED',removed_edges=removed,finding_status='OVER_SIMPLIFIED',scenario_ids=[s['id'] for s in scenarios],no_autonomous_identity_proof=True)
    dump('analysis/data/argument_graph.json',graph)
    chapters=load('analysis/data/research_chapters.json')
    ch=next(c for c in chapters if c['id']=='CH-02')
    ch['central_question']='Quels scénarios distinguent mesure, compensation, création productive et redistribution, et sous quelles conditions ?'
    ch['root_question_relation']='Séparer accroissement réel du pouvoir d’achat, unités de compte et redistribution pour expliquer le passage à l’abondance.'
    ch['claims']+= [c['id'] for c in claims[68:]]
    ch['page_ranges']+=[[95,103],[213,214],[290,293],[523,538]]
    ch['money_review']='analysis/24_money_compensation_scenarios.md'
    dump('analysis/data/research_chapters.json',chapters)
    matrix=['claim_id,chapter_id\n']+[f"{cid},{ch['id']}\n" for ch in chapters for cid in ch['claims']]
    write('analysis/data/claim_chapter_matrix.csv',''.join(matrix))
    concepts=load('analysis/data/concepts.json')
    for concept in concepts:
        concept['used_in_claims']=[c['id'] for c in claims if concept['id'] in c['concepts']]
        if concept['id'] in ['money','cash','unit','inflation','deflation']:
            concept['money_review']='analysis/24_money_compensation_scenarios.md'
            concept['ambiguities'].append('Révision ciblée : ne pas confondre M constant et u constant; libellés Constant/Current divergents pp171,173,177; inflation pp24 et291 à réconcilier.')
    dump('analysis/data/concepts.json',concepts)
    reviews=load('analysis/data/core_reviews.json')
    for r in reviews:
        if r['claim_id'] in revisions:
            r['statement']=byid[r['claim_id']]['statement'];r['money_review']=NEW
            r['local_status']='UNCERTAIN';r['review_scope']='Targeted revision supersedes earlier unconditional-neutrality shorthand; see analysis/24.'
            p='analysis/core_reviews/'+r['claim_id']+'.md'
            target=ROOT/'analysis/history/pre_money_review'/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,target)
            write(p,(ROOT/p).read_text()+'\n## Révision monétaire — 2026-09-08\n\nLa formulation et la confrontation précédentes sont qualifiées comme suit :\n\n'+r['statement']+'\n\n'+NEW+'\n\nVoir [révision ciblée](../24_money_compensation_scenarios.md).\n')
    dump('analysis/data/core_reviews.json',reviews)
    literature=load('analysis/data/literature_map.json'); litlog=[]
    for r in literature['relations']:
        if r['claim_id'] in ['CPC-0005','CPC-0012']:
            old=dict(r);r['relation']='QUALIFIES' if r['source_id']=='BIB-0001' else 'UNCLEAR'
            r['scope']='Cash/dépôts ≠ Money. Bilan bancaire ne teste pas compensation de u. Effet réel d’un choc monétaire ne réfute ni redistribution ni inertie déjà admises; il faut distinguer création productive ultérieure, horizon et invariant revendiqué.'
            r['conceptual_translation_required']=True;r['assessment_status']='TARGETED_REVISION'
            litlog.append(dict(old=old,new=r,reason='L’ancienne contradiction visait une généralisation de l’analyste, pas tous les scénarios effectivement décrits.'))
    dump('analysis/data/literature_map.json',literature)
    dump('analysis/data/money_literature_revision_log.json',litlog)
    finish(claims,scenarios,reviewed,finding,graph)

def finish(claims,scenarios,reviewed,finding,graph):
    # Search audit: all indexed documents, without claiming all candidates read.
    from rag.retrieval import Retriever
    index=load('rag/index/chunks.json');retriever=Retriever(index)
    queries=['coherent incoherent monetary developments compensation number units','value monetary unit constant variable hypothesis','inflation deflation revaluation devaluation','monetary creation distribution money cash n u','confidence cash gold hoarding','price utility complexity inflation']
    patterns=['Money','Cash','unit','number of units','compensat','neutral','purchasing power','creation','distribution','inflation','deflation','price','value','currency','monetary',r'\bn\b',r'\bu\b',r'\bM\b']
    audit=dict(method='BM25 then exact extracted pages; visual checks 171,173,177,531,532',queries=[dict(query=q,hits=[dict(document=h['document'],page=h['page'],score=h['score']) for h in retriever.search(q,k=15)]) for q in queries],
       occurrence_pages={pattern:[p for p,t in P.items() if re.search(pattern,t,re.I)] for pattern in patterns},
       limitation='Lexical search covers all pages; reading is targeted, not exhaustive. Secondary PDFs searched via RAG, no new distinct monetary regime established in this pass.')
    dump('analysis/data/money_search_audit.json',audit)
    examined=list(range(95,104))+list(range(168,184))+list(range(213,217))+list(range(290,294))+list(range(523,539))
    coverage=load('analysis/data/page_coverage.json')
    for row in coverage:
        if row['page'] in examined and not row['examined']:
            row.update(examined=True,reading_note='money_targeted_review.md',reason='TARGETED_ANALYTICAL_READING')
        row['claims']=[c['id'] for c in claims if row['page'] in c['source']['pages']]
    dump('analysis/data/page_coverage.json',coverage)
    state=load('analysis/data/phase2_progress.json');state['pages_examined']=sum(r['examined'] for r in coverage);state['claims']=len(claims);state['money_review_status']='QUALIFIED';dump('analysis/data/phase2_progress.json',state)
    write('analysis/reading_notes/money_targeted_review.md','# Lecture monétaire dirigée\n\nPages examinées : 95–103, 168–183, 213–216, 290–293, 523–538. Pages 14–30 relues.\n\n95–103 : support/valeur, banque et confiance. 168–183 : hypothèses explicites, quatre possibilités, inertie, redistribution, change. 213–216 : variation locale des prix et émission compensatrice. 290–293 : quatre configurations prix/utilité, ajustement de complexité. 523–538 : coefficients, thésaurisation, tableaux cohérents/incohérents, spéculation, limite macro.\n\nLes scénarios et citations page par page figurent dans ../24_money_compensation_scenarios.md. Contrôle visuel des pp171,173,177,531,532; p531 non récupérée textuellement, ne pas prendre le numéro de page pour une extraction du tableau.\n')
    report=['# Révision ciblée Money / compensation\n\nStatut : QUALIFIED. Aucun verdict global.\n',
      '## Finding antérieur\n\n> '+OLD+'\n\n**OVER_SIMPLIFIED**. '+finding['reason']+'\n\n**Reformulation :** '+NEW+'\n',
      '## Périmètre\n\n28 entrées : 11 régimes élémentaires nommés par l’auteur, 4 configurations prix/utilité et 13 applications, compositions ou limites. Elles se recoupent : ce ne sont pas 28 lois indépendantes. Recherche sur les 562 pages indexées et le corpus secondaire, retour ciblé aux pages; aucune garantie d’exhaustivité absolue. Voir money_search_audit.json.\n',
      '## Identité et restrictions\n\nPour n,u positifs, dM=0 implique du/u=−dn/n, et exactement u=M₀/n. La page173 omet la constante d’intégration. Les variations finies vérifient ΔM=u₀Δn+n₀Δu+ΔnΔu. Comparer directement |dn| et |du| (pp23–25) demande unités et pondérations; ce n’est pas la même assertion que comparer les variations relatives.\n\nÀ n constant, dM=n.du; à u constant, dM=u.dn. Ce dernier régime est explicitement présent chez Campergue : FORM-002 ne constitue donc pas un contre-exemple à tout son système. Il ne démontre que la non-implication à partir de l’identité sans conditions.\n\nLa conservation revendiquée Work/Money et l’exclusion des actions humaines de la création sont des prémisses du manuscrit : la compensation n’est pas une hypothèse arbitrairement inventée par l’analyste, mais une conséquence conditionnelle de ce cadre. Reste à justifier l’application exclusive de ce cadre à une opération bancaire et ses effets ultérieurs.\n',
      '## Inventaire sourcé\n']
    for s in scenarios:
        report.append(f"\n### {s['id']} — {s['name']} ({s['author_label']})\n\nNiveau : {s['level']}. Claim : {s['claims'][0]}.\n\n**A — Identité :** {s['identity_or_definition']}\n\n**B — État, changement et conditions :** {s['conditions']} ; {s['applied_change']}.\n\n**C — Mécanisme proposé :** {s['mechanism']}\n\n**D — Résultat sous conditions :** {s['expected_result']}\n\n**E — Portée :** {s['generalization']}\n\nMoney = valeur de Cash; n = nombre d’unités; aucun mapping automatique vers un agrégat bancaire.\n\n**INTERPRETATION — Cas limites :** {s['fragility']} Ces cas sont hypothétiques, pas des tests empiriques exécutés.\n")
        for q in s['sources']:
            report.append(f"\n**SOURCE_TEXT — page PDF {q['page']} :**\n\n> {q['quotation']}\n\nContexte avant : {q['context_before']}\n\nContexte après : {q['context_after']}\n\nFonction : {q['argument_function']}\n")
    report.append('\n## Révisions et graphe\n\nJournal old/new/action/reason/sources : `data/money_claim_revision_log.json`. Les IDs anciens sont préservés, 21 claims ajoutés pour séparer les branches manquantes. Le graphe comporte des nœuds SC-MONEY et des conditions explicites; aucun lien ne certifie une neutralité générale depuis la seule identité. Archives avant révision : `history/pre_money_review/`.\n\n## Réserves textuelles à préserver\n\n1. Pages171/173/177 : Constant Money désigne initialement u constant, mais les étiquettes des possibilités 2 et4 ne respectent pas cette règle. Vérifié visuellement, pas corrigé silencieusement.\n2. Page171 associe 2 et4 à unité constante, alors que 2 fait varier u.\n3. Pages24 et291 : inflation associée respectivement à gain puis baisse du pouvoir d’achat consommateur; agents, phases ou indicateurs pourraient différer, mais la correspondance n’est pas établie.\n4. Page531 est un tableau image. Comparaison visuelle avec532 : ligne 2a2, Td monte dans le tableau T→M de531, reste constant en532; Md baisse dans M→T de531, reste constant en532. Ligne 2b2, n monte dans M→T de531 mais baisse dans T→M et dans le préambule.\n5. Pages528–529 supposent les Works constants dans les évolutions incohérentes, alors que les branches 2b des tableaux font varier Td.\n6. Mc≥Md (523) ne donne pas sans hypothèse temporelle dMc≥dMd (528), encore moins l’égalité utilisée ensuite.\n7. Les formules d’agrégation de23,214,537 n’utilisent pas uniformément n,N; page538 restreint expressément le résultat à la transformation individuelle.\n8. Les généralisations fortes des pages17,28,98–99 ne disparaissent pas : elles doivent être articulées avec 4a/4b, les mélanges et l’inertie. La révision charitable ne doit pas les remplacer par une théorie plus faible inventée.\n\n## Comparaison externe et tests\n\nVoir `24_money_literature_translation.md` et `tests/corpus/test_money_review.py`. Les tests vérifient fidélité, conditions et calculs; ils ne certifient pas les mécanismes causaux. Les anciens rapports 21–23 restent historiques et sont expressément amendés par cette révision.\n')
    compiled=''.join(report).replace('Td monte dans le tableau T→M de531, reste constant en532; Md baisse dans M→T de531, reste constant en532. Ligne 2b2, n monte dans M→T de531 mais baisse dans T→M et dans le préambule.', 'Td monte dans le tableau T→M de531, reste constant en532. Seconde inspection agrandie : Md est constant dans M→T pour 2a2, et n baisse pour 2b2; ces deux divergences initialement soupçonnées ne sont PAS présentes.')
    write('analysis/24_money_compensation_scenarios.md',compiled)
    dump('analysis/data/money_review_summary.json',dict(status='QUALIFIED',scenarios=len(scenarios),claims_reviewed=len(reviewed),actions=dict(Counter(r['action'] for r in reviewed)),new_claims=len(claims)-68,total_claims=len(claims),coverage=state['pages_examined'],previous_finding_status='OVER_SIMPLIFIED',graph_nodes=len(graph['nodes']),graph_edges=len(graph['edges']),unresolved=['Exhaustivité ciblée non garantie','Libellés Constant/Current','Tableaux 531/532','Variations absolues versus relatives','Horizon du retour exact','Agrégation n/N','Causalité crédit/production','Inflation et pouvoir d’achat aux pages24/291']))

if __name__=='__main__':main()
