"""Editorial first-pass CORE reviews. External evidence and source claims stay separate."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,t):
    dest=ROOT/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(t+'\n')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2))

# References actually inspected in this iteration; limited access is explicit.
SOURCES=[
('BIB-0001','Michael McLeay and Amar Radia and Ryland Thomas','Money creation in the modern economy',2014,
 'https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy',None,'VERIFIED','Institutional article; official page introduction read',
 'Les prêts bancaires créent des dépôts. Ce mécanisme institutionnel ne prouve pas une création instantanée de richesse réelle.', 'Official introduction, published 14 March 2014'),
('BIB-0002','OECD','Measuring Productivity - OECD Manual',2001,
 'https://www.oecd.org/content/dam/oecd/en/publications/reports/2001/07/measuring-productivity-oecd-manual_g1gh2484/9789264194519-en.pdf','10.1787/9789264194519-en','VERIFIED','Institutional manual; selected passages inspected',
 'Le manuel distingue productivité, facteurs de production, changements techniques et organisationnels. Il fournit une approche des coûts, sans loi universelle imposant plus d’énergie à toute amélioration.', 'PDF pp12,116–119; printed pp11,115–118; sections 2.1 and 10'),
('BIB-0003','European Commission and International Monetary Fund and OECD and United Nations and World Bank','System of National Accounts 2008',2009,
 'https://unstats.un.org/unsd/nationalaccount/docs/SNA2008.pdf',None,'VERIFIED','Statistical framework; chapter 13 inspected directly with PyMuPDF',
 'La richesse nationale et les bilans comprennent actifs non financiers et positions financières nettes. Ce périmètre diffère de wealth restreint à Money chez Campergue.', 'Chapter 13, paragraphs 13.1–13.5, printed p257 / PDF p315'),
('BIB-0004','IPCC','Climate Change 2022: Mitigation of Climate Change, Chapter 2: Emissions trends and drivers',2022,
 'https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-2/',None,'VERIFIED','Assessment chapter; primary-source indexed passages inspected, direct opening intermittent',
 'Les trajectoires globales relient activité, énergie et émissions, avec des évolutions d’intensité et des cas de découplage. Énergie, CO2 et ensemble des dommages environnementaux ne sont pas interchangeables.', 'Chapter 2, drivers and decoupling; primary search excerpts'),
('BIB-0005','Òscar Jordà and Sanjay R. Singh and Alan M. Taylor','The Long-Run Effects of Monetary Policy',2020,
 'https://www.nber.org/papers/w26666','10.3386/w26666','VERIFIED','NBER working paper; official abstract and metadata inspected; revision September 2024',
 'Les auteurs rapportent des effets réels persistants de chocs monétaires restrictifs. Leur identification n’équivaut pas à une expérience isolant le nombre d’unités de Campergue.', 'NBER Working Paper 26666, abstract; revision September 2024'),
('BIB-0006','Herbert A. Simon','Rational Decision-Making in Business Organizations',1978,
 'https://www.nobelprize.org/uploads/2018/06/simon-lecture.pdf',None,'VERIFIED','Nobel lecture; official metadata and indexed empirical passage inspected; direct PDF opening intermittent',
 'La rationalité limitée et les observations organisationnelles invitent à tester les hypothèses de maximisation plutôt qu’à les poser comme lois comportementales universelles.', 'Lecture 8 December 1978; Empirical Studies, printed p354'),
('BIB-0007','Nicholas Georgescu-Roegen','The Entropy Law and the Economic Process',1971,
 'https://www.degruyterbrill.com/document/doi/10.4159/harvard.9780674281653/html','10.4159/harvard.9780674281653','PARTIALLY_VERIFIED','Publisher bibliographic record verified; full text not inspected',
 'Piste bibliographique sur économie et entropie ; aucune équivalence avec les équations de Campergue n’est établie par cette vérification bibliographique.', 'Publisher metadata only'),
('BIB-0008','International Monetary Fund and partner statistical organizations','Consumer Price Index Manual: Concepts and Methods',2020,
 'https://www.imf.org/-/media/Files/Data/CPI/cpi-manual-concepts-and-methods.ashx',None,'VERIFIED','Institutional manual; official indexed passages inspected',
 'La déflation d’un revenu nominal par un indice de prix permet une mesure du revenu réel. Le choix du panier et la qualité des produits restent déterminants.', 'Chapter 2; real income and current purchasing power accounts, paragraph 2.39')]

# id | status | role/reconstruction | premises | consequences | test/fragility | bibliographic relations
REVIEWS='''1|UNCERTAIN|La question associe histoire de l’abondance et dommages ; sa formulation est une problématique, pas une proposition causale déjà démontrée.|Choisir niveau de vie, périmètre géographique et indicateur environnemental.|Le mécanisme doit expliquer deux phénomènes distincts ; une corrélation PIB–énergie ne couvre pas toute la question.|Comparer trajectoires matérielles et environnementales ; distinguer énergie et émissions.|4:PARTIALLY_SUPPORTS
3|COHERENT|L’analogie est explicitement non identitaire. Elle fournit un programme de formalisation, sans transférer automatiquement la validité des lois physiques.|Définir indépendamment chaque variable économique et sa mesure.|Les propriétés physiques doivent être redémontrées ou déclarées axiomes dans le nouveau domaine.|Vérifier dimensions et hypothèses de chaque transfert ; proximité bibliographique encore limitée.|7:UNCLEAR
5|UNCERTAIN|La neutralité est une restriction économique substantielle, au-delà d’un changement d’échelle des unités.|Isoler une émission sans changement réel et définir u sur un panier fixé.|Le crédit serait redistributif dans ce périmètre ; cela ne préjuge pas de ses effets ultérieurs sur la production.|Le numéraire pur est neutre par construction ; le crédit qui finance une production n’est pas une simple renumérotation.|1:QUALIFIES,5:CONTRADICTS
9|UNCERTAIN|Seul le travail engendrerait le changement ; la force du propos dépend du sens mécanique, économique ou causal donné à travail.|Spécifier changement visé et ne pas définir tout changement comme Work après coup.|L’axiome sert à exclure les interventions sans Work de la création de Money.|Rechercher une variation productive non couverte par la mesure indépendante de Work ; risque de tautologie si Work est défini par son effet.|2:QUALIFIES
10|COHERENT|M=n.u est une identité de mesure si n et u sont correctement définis ; elle ne décide pas comment u réagit à n.|Unité de référence fixée, n nombre d’unités et u leur valeur réelle.|La règle du produit donne le différentiel ; elle ne donne ni neutralité ni causalité.|Contrôle FORM-002 : n varie à u constant ; l’identité reste vraie et M change.|8:PARALLEL
12|UNCERTAIN|La compensation inverse automatique de u et n ajoute une hypothèse d’équilibre ou de conservation à l’identité.|Même périmètre, ajustement inverse exact et horizon de réponse déterminé.|Sans cette compensation, la conclusion de non-création ne découle pas du calcul seul.|HYP-0007 exige une mesure indépendante de u et des chocs ; contradictions externes concernent seulement une neutralité causale générale.|5:CONTRADICTS,1:QUALIFIES
15|PARTIALLY_SUPPORTED|À revenu nominal et panier fixés, une baisse de prix permet un supplément d’achats ; appeler ce supplément Money créé est une définition propre.|Quantité comparée, qualité, revenu et prix des autres biens contrôlés.|Le pouvoir d’achat d’un acheteur augmente ; la richesse agrégée ne suit pas sans examiner revenus et producteurs.|Comparer gain d’achat individuel, recettes fournisseurs et variation réelle de production.|8:PARTIALLY_SUPPORTS
16|PLAUSIBLE|La chaîne travail→productivité→coût→prix→pouvoir d’achat constitue un mécanisme possible, mais chacune de ses flèches est conditionnelle.|Technique, coût unitaire et transmission aux prix ; p20–21 admettent prix de vente inchangé.|La baisse de coût peut enrichir le consommateur si elle se transmet effectivement au prix.|HYP-0002 : panel coûts/prix/qualité ; ne pas confondre prix de revient et prix payé.|2:PARTIALLY_SUPPORTS,8:QUALIFIES
17|UNCERTAIN|La hausse nécessaire de Work lors d’un gain de productivité demande de distinguer T économique, travail physique et énergie par produit.|Périmètre énergétique, méthode et tâche constants ; p203 affirme T nul sans accélération.|Une hausse du débit n’est pas à elle seule une mesure d’énergie supplémentaire par unité produite.|HYP-0001 : mesures physiques indépendantes ; une hausse de puissance n’établit pas une hausse d’énergie par tâche.|2:QUALIFIES
22|UNCERTAIN|La transformation du supplément de travail en supplément de Money reformule la chaîne productive en bilan.|Mesures de T et M compatibles, transmission de coût, coefficient et frontière du système.|Le mot transformation ne démontre pas une conservation quantitativement mesurable.|Comparer bilan calculé et indicateurs indépendants ; éviter de définir g après observation pour garantir l’égalité.|7:UNCLEAR
23|UNCERTAIN|La conservation concerne travail restant détruit et Money créé dans un système déclaré isolé.|Signes, unités, échanges externes et g doivent être fixés.|Un bilan cohérent est possible comme modèle ; sa portée économique exige des observables.|Tester les bilans sur un cycle complet ; contrôler variable restante versus travail effectué.|7:UNCLEAR
32|UNCERTAIN|Économiser Work sous contraintes peut être une hypothèse d’optimisation, pas une loi dynamique universelle acquise.|Objectif, information, ensemble faisable et stabilité des contraintes.|Les comportements observés doivent correspondre à une métrique indépendante d’économie de Work.|Chercher décisions répétées non maximisantes après contrôle des contraintes ; ne pas redéfinir celles-ci pour absorber toute observation.|6:QUALIFIES
33|UNCERTAIN|L’économie de Money vers un maximum pose une hypothèse comportementale distincte d’une identité comptable.|Préférences, qualité, risque, information et contraintes budgétaires.|Un prix plus bas n’est pas le seul objectif possible d’un acheteur.|Tester choix et objectifs ; ne pas assimiler achat moins cher, utilité accrue et Money conservé.|6:QUALIFIES
35|COHERENT|Le supplément annoncé de 78 % correspond numériquement à (8/6)^2−1 ; c’est une cohérence arithmétique conditionnelle.|Même tâche et complexité, grandeur supposée proportionnelle au carré de la vitesse.|Le calcul ne suffit pas à établir la loi énergétique ou à valider une machine réelle.|FORM-001 reproduit 77,777… % ; l’hypothèse HYP-0006 demeure partiellement opérationnelle seulement.|2:QUALIFIES
39|UNCERTAIN|Economic Energy est une catégorie postulée regroupant Work et Money ; le nom ne lui confère pas l’unité joule.|Définir conversion, dimensions et signification du stock ou du flux.|Une équivalence formelle peut être étudiée ; l’équivalence physique n’est pas acquise.|Rechercher mesures indépendantes et stabilité du coefficient ; comparaison thermodynamique encore bibliographiquement ouverte.|7:UNCLEAR
40|COHERENT|Le choix du travail restant rend explicite un état qui décroît pendant l’exécution ; ce choix n’efface pas l’activité déjà accomplie.|Frontière temporelle, tâche initiale et convention de signe.|Les signes de la conservation dépendent de ce choix ; p197 précise aussi labour restant.|Contrôler sur une tâche observée que l’état restant et le débit d’exécution ne sont pas interchangés.|2:QUALIFIES
41|COHERENT|Product et Cash servent de supports respectifs ; cette séparation sémantique évite de confondre objet, inscription et grandeur.|Distinguer attribut mesuré et support, y compris numérique.|Les transferts de supports n’établissent pas à eux seuls des variations de valeur réelle.|Tester fidélité des citations et du vocabulaire ; ce n’est pas une hypothèse causale autonome.|1:PARALLEL
43|UNCERTAIN|M=g.T peut être une loi testable si g est connu indépendamment ; avec g=M/T choisi après coup, elle devient une identité.|Définir valeurs, signes, période et détermination de g avant observation.|Prédiction possible hors échantillon uniquement si g est contraint.|Comparer g entre produits et périodes, avec mesures indépendantes ; p36 avertit que g n’est pas nécessairement constant.|7:UNCLEAR
45|UNCERTAIN|dM=−F.dp formalise un gain associé à baisse de prix ; la force consommateur doit avoir une mesure propre.|Définition de F, unités, quantités achetées et autres prix.|À F fixé le signe est clair ; le mécanisme causal du prix reste séparé.|Identifier F autrement que par −dM/dp ; p204 reprend cette relation comme définition.|8:QUALIFIES
46|COHERENT|Money comme valeur de Cash est une convention lisible ; Cash inclut chez l’auteur davantage que les seules espèces.|Expliciter le panier de valorisation et les supports admis.|Un dépôt créé peut accroître Cash sans qu’un gain réel soit établi instantanément.|Comparer conventions avant toute confrontation à la création bancaire ; aucun désaccord de vocabulaire n’est une réfutation.|1:QUALIFIES,8:PARALLEL
48|COHERENT|Wealth est restreint à Money, hors patrimoine ; p204 reconnaît aussi des richesses culturelles et des services non marchands.|Maintenir le périmètre monétaire annoncé plutôt que lire wealth comme tout bien-être.|Les conclusions sur la richesse ainsi définie ne s’étendent pas automatiquement à la richesse nationale ou au bien-être.|Construire une table de correspondance ; une définition conventionnelle distincte n’est pas un résultat empirique faux.|3:QUALIFIES
51|COHERENT|Labour est une tâche pour une méthode et un produit donnés ; ce n’est ni des heures de travail ni T.|Décrire tâche et méthode et fixer leur unité.|Le temps peut changer sans que la tâche change ; toute comparaison de méthodes demande une nouvelle référence.|Comparer temps pour même tâche, sans importer automatiquement labour des statistiques.|2:QUALIFIES
52|UNCERTAIN|Work varie avec la vitesse pour une tâche fixée, mais p203 précise que le Work économique effectué est nul sans variation de vitesse.|Distinguer niveau d’un état cinétique, différentiel de Work et énergie physique consommée.|La formulation prototype doit être lue avec la définition différentielle, pas comme une équivalence générale débit–énergie.|Examiner les relations 04-05 à 04-09 et les signes avant une mesure expérimentale.|2:QUALIFIES
53|COHERENT|La valeur portée par Cash varie selon le lieu et le temps ; cette variation ne doit pas être confondue avec le nombre d’unités.|Choisir unité réelle, panier et comparabilité spatiale.|Une même inscription nominale peut représenter différents pouvoirs d’achat.|Tests d’indice et qualité du panier ; le caractère mesurable dépend de la définition de u.|8:PARALLEL'''

NEW=[
(64,203,'À vitesse d’exécution constante, Economic Work effectué est nul, même si le travail physique est important.',"if the speed of execution of the labour doesn't vary, the Work done (Economic Work) is zero",['work','labour','productivity'],'QUALIFIES',52,'CH-04'),
(65,204,'L’absence de création de richesse monétaire n’exclut pas les richesses culturelles ou les services non marchands.', 'Even if agents don’t create monetary wealth, they may produce other types of wealth', ['wealth','work'],'QUALIFIES',48,'CH-01'),
(66,202,'Les complexités du Product et de Cash ne sont pas égales malgré une notation c parfois commune.', "This simplification means that they would be equal, which isn't true.", ['complexity','cash','product'],'QUALIFIES',54,'CH-03'),
(67,463,'Une section informative réintroduit une relation avec l’entropie physique via le rendement global.', "Entropy This paragraph isn't of particular interest and is presented for information purposes only. Previously, the 19-01 relationship linking heat to the Money and the respective physical and economic efficiencies has been determined above, namely :", ['entropy','energy','coefficient'],'QUALIFIES',42,'CH-09'),
(68,198,'Les relations de vitesse mesurent les évolutions sans en déterminer les causes.', 'they only give a measure of these speeds and in no case do they stipulate for what reason', ['productivity','price'],'QUALIFIES',52,'CH-04')]

def main():
    if (ROOT/'analysis/data/money_compensation_scenarios.json').exists():
        raise SystemExit('Historical generator: monetary revision exists; do not overwrite it.')
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    original_core=[c for c in claims if c['criticality']=='CORE']
    assert len(original_core)==24
    concepts=read('analysis/data/concepts.json'); chapters=read('analysis/data/research_chapters.json')
    graph=read('analysis/data/argument_graph.json'); coverage=read('analysis/data/page_coverage.json')
    pages={p['page_pdf']:' '.join(p['text'].split()) for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    for n,p,statement,quotation,terms,rel,target,ch in NEW:
        assert quotation in pages[p]
        cid=f'CPC-{n:04}'
        if n==67:
            existing=next((c for c in claims if c['id']==cid),None)
            if existing and existing['source']['quotation']=="This paragraph isn't of particular interest and is presented for information purposes only.":
                existing['source']['quotation']=quotation;existing['quotation']=quotation
                for edge in graph['edges']:
                    if edge['source']==cid:edge['evidence']=existing['source']
        if not any(c['id']==cid for c in claims):
            claims.append(dict(id=cid,statement=statement,source=dict(document='Reflections_PierreCampergue.pdf',page=p,pages=[p],quotation=quotation),
                source_document='Reflections_PierreCampergue.pdf',page=p,quotation=quotation,type='METHODOLOGICAL' if n in [67,68] else 'CONCEPTUAL',
                epistemic_status='SOURCE',interpretive=True,criticality='MAJOR',concepts=terms,depends_on=[],supports=[],contradicts=[],
                testability='CONCEPTUAL_OR_FORMAL_REVIEW',root_question_relevance='Précise le domaine du mécanisme travail–Money.',
                interpretation_notes='Lecture dirigée itération 1 ; qualification du claim initial, pas remplacement silencieux.',confidence_in_reconstruction=.9))
            graph['nodes'].append(dict(id=cid,kind=claims[-1]['type']))
            graph['edges'].append(dict(source=cid,target=f'CPC-{target:04}',relation=rel,interpretive=True,evidence=claims[-1]['source']))
        chapter=next(c for c in chapters if c['id']==ch)
        if cid not in chapter['claims']:chapter['claims'].append(cid)
        if cid not in coverage[p-1]['claims']:coverage[p-1]['claims'].append(cid)
        for term in terms:
            c=next(c for c in concepts if c['id']==term)
            if cid not in c['used_in_claims']:c['used_in_claims'].append(cid)
    for p in list(range(195,206))+[463,464]:
        coverage[p-1].update(examined=True,reading_note='iteration1_directed.md',reason='DIRECTED_READING')
    for c in concepts:
        if c['id'] in ['work','complexity','entropy']:
            note={'work':'p203 : T effectué nul à vitesse constante ; ne pas confondre niveau cinétique et différentiel.',
                  'complexity':'p202 : cP et cA distincts malgré notation parfois commune.',
                  'entropy':'p463–464 : réintroduction informative de l’entropie physique ; distinguer du formalisme économique p36.'}[c['id']]
            if note not in c['definition_changes']:c['definition_changes'].append(note)
    for ch in chapters:ch['classification_status']='PROVISIONAL_STABLE_ITERATION1'
    write('analysis/data/claims.jsonl','\n'.join(json.dumps(c,ensure_ascii=False) for c in claims))
    for name,data in [('concepts',concepts),('argument_graph',graph),('research_chapters',chapters),('page_coverage',coverage)]:dump(f'analysis/data/{name}.json',data)
    state=read('analysis/data/phase2_progress.json'); state.update(pages_examined=sum(p['examined'] for p in coverage),claims=len(claims),criticality=dict(Counter(c['criticality'] for c in claims)),types=dict(Counter(c['type'] for c in claims)))
    dump('analysis/data/phase2_progress.json',state)
    write('analysis/data/claim_chapter_matrix.csv','claim_id,chapter_id\n'+'\n'.join(f"{c},{ch['id']}" for ch in chapters for c in ch['claims']))
    library=[]
    for sid,authors,title,year,url,doi,status,access,summary,locator in SOURCES:
        library.append(dict(id=sid,authors=authors,title=title,year=year,url=url,doi=doi,status=status,access=access,summary=summary,locator=locator,verification='Actual primary site or primary indexed excerpt inspected during this iteration; not necessarily full text.'))
    dump('bibliography/initial_research_library.json',library)
    bib=[]
    for s in library:
        fields={'author':s['authors'],'title':s['title'],'year':str(s['year']),'url':s['url'],'note':s['access']}
        if s['doi']:fields['doi']=s['doi']
        bib.append('@misc{'+s['id']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}')
    write('bibliography/research_library.bib','\n\n'.join(bib))
    reviews=[]; relations=[]
    for line in REVIEWS.splitlines():
        n,status,role,premises,consequences,test,refs=line.split('|'); cid=f'CPC-{int(n):04}'
        c=next(c for c in claims if c['id']==cid)
        links=[]
        for ref in refs.split(','):
            number,relationship=ref.split(':'); sid=f'BIB-{int(number):04}'
            links.append(sid)
            relations.append(dict(claim_id=cid,source_id=sid,relation=relationship,
                scope='Only the stronger inference of unconditional causal monetary neutrality, not the author’s private definition of Money.' if relationship=='CONTRADICTS' else 'Local conceptual comparison; not validation of the full claim.',
                assessment_status='INITIAL_REVIEW',interpretive=True))
        review=dict(claim_id=cid,statement=c['statement'],source=c['source'],role=role,premises=premises,
            formal_dependencies=c['depends_on'],consequences=consequences,chapters=[ch['id'] for ch in chapters if cid in ch['claims']],
            character=c['type'],test_and_fragility=test,local_status=status,literature=links,review_scope='Initial substantive review; not exhaustive bibliography or global verdict.')
        reviews.append(review)
        text=f"# {cid} — {status}\n\n## Formulation et source\n\n{c['statement']}\n\n> {c['source']['quotation']}\n\nManuscrit, pages PDF {c['source']['pages']}. La formulation française est une reconstruction.\n\n## Rôle et mécanisme\n\n{role}\n\n## Prémisses\n\n{premises}\n\n## Conséquences\n\n{consequences}\n\n## Caractère, chapitre, test et fragilité\n\nType source : {c['type']}. Chapitres : {', '.join(review['chapters'])}.\n\n{test}\n\n## Littérature initiale\n\n"
        for sid in links:
            s=next(s for s in library if s['id']==sid)
            relation=next(r for r in relations if r['claim_id']==cid and r['source_id']==sid)
            text+=f"- [{sid} — {s['title']}]({s['url']}) : {relation['relation']}. {relation['scope']}\n"
        write(f'analysis/core_reviews/{cid}.md',text)
    dump('analysis/data/core_reviews.json',reviews)
    dump('analysis/data/literature_map.json',dict(sources=library,relations=relations,
        limitations=['Initial targeted review, no originality verdict.','Publication dates do not establish priority relative to an undated original manuscript.','Relations labelled CONTRADICTS concern an explicitly stated stronger interpretation only.']))
    write('analysis/20_initial_literature_review.md','# Revue initiale liée aux CORE\n\nLes relations sont locales et interprétatives. Une définition ne devient pas fausse parce que les institutions utilisent un autre mot. Les deux relations CONTRADICTS portent sur une neutralité causale générale, pas sur une renumérotation ni sur la seule définition de Money.\n\n'+'\n\n'.join(f"## {s['id']}\n\n[{s['title']}]({s['url']}) — {s['year']}, {s['status']}.\n\n{s['summary']}\n\nAccès : {s['access']}. Repère : {s['locator']}." for s in library)+'\n\nAucun claim d’originalité établi. Aucun DOI ajouté lorsqu’il n’a pas été vérifié dans les métadonnées consultées.')
    hs=read('analysis/data/hypotheses.json')
    classes=['DIFFICULT','MODERATE','DIFFICULT','NOT_OPERATIONAL_YET','NOT_OPERATIONAL_YET','EASY','NOT_OPERATIONAL_YET']
    for h,cls in zip(hs,classes):
        h['difficulty']=cls
        h['iteration1_result']='Conditional arithmetic executed; physical law not validated.' if h['id']=='HYP-0006' else 'NOT_TESTED'
        # Keep original status: the scientific hypothesis is not validated by a partial calculation.
    dump('analysis/data/hypotheses.json',hs)
    dump('analysis/data/iteration1_change_log.json',dict(policy_change={'old':'INCOMPLETE blocks verify','new':'SUFFICIENT_FOR_ITERATIVE_RESEARCH; coverage warning','evidence':'Explicit user instruction this iteration'},
        claims_added=[f'CPC-{n:04}' for n,*rest in NEW],new_reading_pages=list(range(195,206))+[463,464],
        interpretation_changes=['CPC-0052 qualified by CPC-0064, not silently replaced.','Entropy scope clarified by CPC-0067; ISS-007 retained OPEN pending full derivation.'],
        bibliography_scope='7 VERIFIED and 1 PARTIALLY_VERIFIED records; heterogeneous access depth.'))
    print('24 CORE reviewed; 5 contextual claims added; 61 manuscript pages examined')

if __name__=='__main__':main()
