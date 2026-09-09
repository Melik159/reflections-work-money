"""One-shot editorial integration. Sources are exact whitespace-normalized passages.
Never rerun to overwrite later research: the revision journal is an explicit guard.
"""
import csv
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
def save(p,x):
    target=ROOT/p; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
pages={r['page_pdf']:' '.join(r['text'].split()) for r in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
def source(page,quote):
    assert quote in pages[page], (page,quote)
    i=pages[page].index(quote)
    return dict(document='Reflections_PierreCampergue.pdf',page=page,pages=[page],quotation=quote,
                normalization='whitespace',context_before=pages[page][max(0,i-200):i],context_after=pages[page][i+len(quote):i+len(quote)+200])

def main():
    journal='analysis/data/energy_review_revision_log.json'
    if (ROOT/journal).exists(): raise SystemExit('Already integrated; use a new explicit revision, not regeneration.')
    changed=['analysis/data/claims.jsonl','analysis/data/argument_graph.json','analysis/data/research_chapters.json',
             'analysis/data/page_coverage.json','analysis/data/claim_chapter_matrix.csv','analysis/data/concepts.json',
             'analysis/data/literature_map.json','bibliography/initial_research_library.json','validation/phase2_regression_results.json']
    for path in changed:
        target=ROOT/'analysis/history/pre_energy_review'/path; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/path,target)
    claims=[json.loads(x) for x in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    assert len(claims)==113
    # ID, chapter, type, page, quotation, reconstruction, assumptions, dependencies.
    specs=[
      (114,8,'DEFINITION',403,"In the same way as supply, demand D must be considered as speed, as it's necessary to specify the time during which a certain number of copies of the Product are sold.",
       'La demande D est définie comme un débit de copies vendues, symétriquement à l’offre de copies fabriquées.',
       ['Même Product et période; débit réalisé, pas courbe de demande contrefactuelle.'],['CPC-0037']),
      (115,8,'ASSUMPTION',413,'However, it should be noted that these relationships are only valid in the absence of losses.',
       'Les potentiels économiques sont présentés comme fonctions d’état sous une restriction explicite d’absence de pertes.',
       ['État correctement défini; indépendance du chemin postulée; pour les relations de Maxwell, différentiabilité et intégrabilité requises.'],['CPC-0039']),
      (116,8,'METHODOLOGICAL',441,'By choosing any 2 variables among them and since r P is a constant, there are therefore three possibilities, namely :',
       'Le calcul des coefficients écométriques emploie deux variables parmi FA, V, UP, avec rP constant dans la Core Law.',
       ['Deux degrés de liberté sur la surface constitutive, malgré le mot independent appliqué aux trois variables.'],['CPC-0055']),
      (117,8,'HYPOTHESIS',559,'Then, the more Products are taken into account, the more the coefficient K can be considered constant, and therefore only a function of the units used.',
       'Le manuscrit suppose qu’agréger davantage de Products stabilise K, pourtant variable selon le produit, jusqu’à ne plus dépendre que des unités.',
       ['Composition et pondérations stables non démontrées; nombre élevé ne suffit pas à lui seul.'],['CPC-0111']),
      (118,9,'HYPOTHESIS',559,'which shows the absolute coupling of the GDP of a system to the energy consumed in it.',
       'La fin du manuscrit propose GDP=K·Wconsumed comme couplage absolu, en absorbant dans K l’énergie sans création de Money.',
       ['K stable; identification GDP/Money dépensé; équivalence des frontières, périodes, unités et énergies.'],['CPC-0117']),
      (119,9,'ASSUMPTION',455,"However, it must be kept in mind that this mechanical work (Wcreated) is only economically useful if it allows the Utility of a Product to evolve.",
       'Le pont Tused=−Wcreated est restreint au travail mécanique économiquement utile, qui fait évoluer l’Utility du Product.',
       ['Frontière physique/économique et signe entrée/sortie; unité commune ou conversion nécessaire; énergie non utile séparée.'],['CPC-0095']),
      (120,9,'MECHANISM',460,'This remark therefore highlights the increasing consumption of fuels induced by the acceleration of manufacturing processes, and consequently its inevitable increasingly intense impact on the environment.',
       'Campergue relie accélération productive, pertes croissant plus vite que la productivité, consommation accrue de combustibles et dommages environnementaux.',
       ['Évolution relative des pertes postulée; mix énergétique, matières et dommages spécifiques non quantifiés ici.'],['CPC-0018','CPC-0119']),
      (121,9,'HYPOTHESIS',472,'which shows the conservation, over time, of the total Work (Work created + Work to be done).',
       'La conservation du Work total est obtenue en compensant la variation cinétique par la variation de Work potentiel restant.',
       ['Système ceteris paribus; cp fixe dans l’intégration; identification des variations potentielles et cinétiques.'],['CPC-0023']),
      (122,9,'CONCEPTUAL',466,'In this note, which is outside the realm of physics, there is neither quantity of movement nor energy in the mechanical sense.',
       'Les conservations économiques sont présentées avec des caractéristiques similaires, mais explicitement non mécaniques, avant leur application ceteris paribus.',
       ['Ne pas confondre Money avec joules ou emploi e avec effectifs salariés.'],['CPC-0039']),
      (123,10,'DEFINITION',477,'The “Makers” are the people who done labour at a constant speed, i.e. without exerting Force and therefore without varying the Utility of the Product. No Money is created.',
       'Les Makers réalisent du labour sans création de Money; les Workers sont distingués par Force et variation d’Utility, non par simple utilité sociale.',
       ['Taxonomie propre au manuscrit; utilité culturelle, médicale et sociale explicitement préservée.'],['CPC-0064','CPC-0065']),
      (124,10,'HYPOTHESIS',488,'Consequently, the Cash covering this price increase will necessarily come from others, i.e. the Buyers. It will therefore only be a transfer of Cash. If the monopoly gets richer, consumers get poorer.',
       'Dans le scénario monopolistique à service et Utility inchangés, la hausse de prix est attribuée à un transfert de Cash depuis les acheteurs.',
       ['Absence de Force effective du consommateur; même service; aucun Work supplémentaire; périmètre comprenant les deux acteurs.'],['CPC-0093']),
      (125,10,'MECHANISM',490,'It provides some Work in order to increase the Utility of the Product and it increases the price. But because of his monopoly position, he raises the price even more without having done any extra labour.',
       'Le monopole de brevet peut combiner un Work augmentant l’Utility et une hausse supplémentaire de prix sans travail supplémentaire, attribuée au transfert.',
       ['Séparer composante productive et prélèvement supplémentaire; ne pas généraliser le scénario sans Work à tout monopole.'],['CPC-0055']),
      (126,8,'METHODOLOGICAL',558,'Therefore, considering a group of enterprises, it would be possible to plot a set of vectors, each of which represents the competitiveness of each enterprise.',
       'Le champ labour-prix juxtapose des vecteurs de compétitivité d’entreprises; il ne fournit pas à lui seul une somme macroéconomique de Work ou Money.',
       ['Même Product pour l et p; normalisation des axes; distinguer ensemble de vecteurs et agrégat.'],['CPC-0116']),
      (127,10,'MECHANISM',400,'In fact, the greater the Work done by the supplier, the lower the price, which leads to a surplus of Money for the consumer and, therefore, allows him to acquire more and/or higher quality Products.',
       'Le supplément de Money issu du scénario de baisse de prix permet davantage de Products ou des Products de meilleure qualité.',
       ['Possibilité de consommation, non obligation de dépense immédiate; empreinte du panier supplémentaire non mesurée.'],['CPC-0099'])]
    graph=load('analysis/data/argument_graph.json'); chapters=load('analysis/data/research_chapters.json')
    byid={c['id']:c for c in claims}; edits=[]
    for num,ch,typ,p,q,statement,conditions,deps in specs:
        cid=f'CPC-{num:04d}'; s=source(p,q)
        concepts={8:['coefficient','utility','money'],9:['energy','work','money'],10:['agent','money','price']}[ch]
        c=dict(id=cid,statement=statement,source=s,source_document=s['document'],page=p,quotation=q,
               type=typ,epistemic_status='SOURCE',interpretive=True,concepts=concepts,depends_on=deps,supports=[],contradicts=[],
               criticality='MAJOR',conditions=conditions,chapters=[f'CH-{ch:02d}'],testability='CONDITIONAL_NOT_EMPIRICALLY_VALIDATED',
               root_question_relevance='Relier transformations locales, richesse, consommation et environnement sans supposer leur agrégation automatique.',
               interpretation_notes='Reconstruction française; citation anglaise seule verbatim. Voir revue27–29 et cas alternatifs.',confidence_in_reconstruction=0.85)
        claims.append(c); byid[cid]=c; chapters[ch-1]['claims'].append(cid)
        graph['nodes'].append(dict(id=cid,kind=typ))
        for dep in deps: graph['edges'].append(dict(source=dep,target=cid,relation='DEPENDS_ON',direction='premise_to_dependent',evidence=s,conditions=conditions,interpretive=True))
        graph['edges'].append(dict(source=cid,target='QUESTION_RACINE',relation='ANSWERS',evidence=s,conditions=conditions,interpretive=True,scope='PROPOSED_PARTIAL_ANSWER_NOT_VALIDATION'))
        edits.append(dict(id=cid,action='ADD',old_statement=None,new_statement=statement,reason='Distinct proposition in newly scoped terminal reconstruction.',new_sources=[s]))
    for ch,extra in [(8,['CPC-0089','CPC-0111','CPC-0109']),(9,['CPC-0018','CPC-0104','CPC-0117','CPC-0127']),(10,['CPC-0065','CPC-0092','CPC-0093','CPC-0108','CPC-0084'])]:
        chapters[ch-1]['claims']=list(dict.fromkeys(chapters[ch-1]['claims']+extra))
        chapters[ch-1].update(analysis_status='UNCERTAIN',analysis_file={8:'analysis/chapters/CH08_aggregation.md',9:'analysis/chapters/CH09_energy_conservation.md',10:'analysis/chapters/CH10_agents_markets.md'}[ch],
                              review_status='FIRST_SUBSTANTIVE_REVIEW_QUALIFIED',coverage_status='TARGETED_NOT_EXHAUSTIVE')
    chapters[7]['major_uncertainties']=['Moyennes et K stables non démontrés','Échelles du champ labour-prix','Intégrabilité et coefficients variables']
    chapters[8]['major_uncertainties']=['Pont Money/joules non calibré','Couplage absolu distinct de corrélation','Noether et entropy: conditions à vérifier']
    chapters[9]['major_uncertainties']=['Monopole productif vs transfert','Taxonomie services vs utilité sociale','Mesure séparée des variations globales et transferts']
    chapters[8]['potential_tests']=['TEST-E1','TEST-E2','TEST-E3']
    save('analysis/data/research_chapters.json',chapters); save('analysis/data/argument_graph.json',graph)
    (ROOT/'analysis/data/claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
    with (ROOT/'analysis/data/claim_chapter_matrix.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['claim_id','chapter_id'])
        for ch in chapters:
            for cid in ch['claims']:w.writerow([cid,ch['id']])
    concepts=load('analysis/data/concepts.json')
    for c in concepts: c['used_in_claims']=[x['id'] for x in claims if c['id'] in x['concepts']]
    save('analysis/data/concepts.json',concepts)
    examined=set([33,34,380,399,400,402,403,405,406,407,408,409,410,413,414,415,420,422,424,431,432,433,438,441,442,446,452,453]+list(range(454,493))+list(range(536,563)))
    coverage=load('analysis/data/page_coverage.json'); old_count=sum(r['examined'] for r in coverage)
    for r in coverage:
        if r['page'] in examined and not r['examined']:
            r.update(examined=True,reading_note='energy_aggregation_agents_review.md',reason='TARGETED_SOURCE_REVIEW')
        r['claims']=[c['id'] for c in claims if r['page'] in c['source'].get('pages',[c['page']])]
    save('analysis/data/page_coverage.json',coverage)
    save(journal,dict(date='2026-09-08',baseline=dict(claims=113,examined=175,tests_pass=40),new_claims=len(claims),
                      old_examined=old_count,new_examined=sum(r['examined'] for r in coverage),changes=edits,
                      old_claim_statements_changed=[],chapter_change='CH08–10 NOT_TESTED → UNCERTAIN, targeted substantive reconstruction',
                      correction=dict(old='Énergie reconstruite à partir du PIB, donc association nécessairement circulaire',
                                      new='Construction dérivée confirmée; circularité non automatique si le ratio restitue un bilan énergétique indépendant; nouvelle série directe utilisée.',
                                      reason='World Bank metadata documents physical IEA denominator; cancellation and vintage qualifications made explicit in report27.'),
                      reading_pages_this_pass=sorted(examined),history='analysis/history/pre_energy_review'))
    # Machine-readable reconstruction conditions, not an assertion of theory validity.
    aggregation=[
        dict(id='AG-01',claims=['CPC-0111'],pages=[210],mechanism='Somme des contributions T',conditions=['Unités et référence communes','Contributions sans double compte','Interactions non implicitement absorbées'],status='ASSUMPTION_DEPENDENT'),
        dict(id='AG-02',claims=['CPC-0037','CPC-0114'],pages=[402,403,406,408],mechanism='Débits et identité de valeur pQ',conditions=['Product homogène','Prix commun ou somme p_i Q_i','Débit total distinct de moyenne de vitesses','p*l=1 demande normalisation supplémentaire'],status='QUALIFIED'),
        dict(id='AG-03',claims=['CPC-0115','CPC-0116'],pages=[413,414,420,422,431,432,441,446],mechanism='Potentiels et dérivées partielles locales',conditions=['Absence de pertes annoncée','État intégrable et dérivable','Deux variables libres pour rP fixe','Dérivées inverses non nulles'],status='ASSUMPTION_DEPENDENT'),
        dict(id='AG-04',claims=['CPC-0089'],pages=[536,537,538],mechanism='Pondération locale n/N',conditions=['n local et N global distincts','Normalisation M/N à expliciter','Pas de somme répétant le même stock Cash'],status='AMBIGUOUS'),
        dict(id='AG-05',claims=['CPC-0126'],pages=[538,539,548,550,554,558],mechanism='Champ de vecteurs de compétitivité',conditions=['l,p pour même Product','Échelle commune ou métrique pour axes hétérogènes','Pas une fonction de production agrégée fournie'],status='QUALIFIED'),
        dict(id='AG-06',claims=['CPC-0117','CPC-0118'],pages=[558,559],mechanism='Stabilisation de K et passage GDP=K W',conditions=['Stabilité des poids et composition','Pont GDP/Money','Énergie utile et totale distinguées','Périodes et unités compatibles'],status='NOT_ESTABLISHED')]
    for a in aggregation:a['source']=byid[a['claims'][-1]]['source'];a['interpretive']=True
    save('analysis/data/aggregation_mechanisms.json',aggregation)
    chain=[
       ('ENV-01','subsistance','abondance par cycles accélérés','SOURCE_EXPLICIT',34,'This is how, at least in “occidental” countries, we have passed :'),
       ('ENV-02','énergie mécanique peu coûteuse','mobilité et transports','SOURCE_EXPLICIT',460,'this quasi-gratuity of mechanical energy that explains the development of mobility in general.'),
       ('ENV-03','Work fourni et prix plus faible','surplus Money et achats plus nombreux/qualitatifs','SOURCE_EXPLICIT',400,'allows him to acquire more and/or higher quality Products.'),
       ('ENV-04','Money économisé','usage ultérieur possible','SOURCE_EXPLICIT',33,'The consumer can therefore use this Money at a later date, in principle at his convenience.'),
       ('ENV-05','achats supplémentaires','empreinte énergétique et matérielle du nouveau panier','RESEARCH_INTERPRETATION',400,'allows him to acquire more and/or higher quality Products.'),
       ('ENV-06','accélération des processus et pertes','combustibles et environnement','SOURCE_EXPLICIT',460,'increasing consumption of fuels induced by the acceleration of manufacturing processes'),
       ('ENV-07','développement et énergie fossile','dommages environnementaux','SOURCE_EXPLICIT',454,'contribute strongly to the current environmental degradations.')]
    env=[]
    for id,start,end,level,p,q in chain:env.append(dict(id=id,from_node=start,to_node=end,epistemic_level=level,source=source(p,q),conditions=['Pas de quantification des émissions, matières ou dommages; attribution causale non testée'],causal_validated=False))
    save('analysis/data/environmental_chain.json',dict(edges=env,missing=['Panier marginal et énergie incorporée','Mix et intensité carbone','Fonction émissions/matières → dommages','Contrefactuel efficacité sans réponse de demande'],rebound_comparison='PARTIAL_PARALLEL',reason='Usage du surplus explicite; gain d’efficacité énergétique et économies contrefactuelles non définis comme dans un test de rebond.'))
    agents=[
      ('ACT-01','Consommateur','Fournisseur','Cash contre Product',405,'TRANSFER','Transaction bilatérale; pas création globale du seul fait du paiement'),
      ('ACT-02','Fournisseur','Consommateur','Baisse de prix / gain Money',33,'PRODUCTIVE_CREATION_CLAIM','Work productif et branche de transmission; distinct de Cash transféré'),
      ('ACT-03','Cotisants','Retraités par répartition','cash',475,'REDISTRIBUTION','Flux de contributions, pas jugement sur utilité sociale'),
      ('ACT-04','Contribuables','État puis infrastructures et agents','prélèvements',479,'DESTRUCTION_IN_AUTHOR_SENSE','Pertes utiles; ne signifie pas disparition comptable de Cash ni absence de bénéfice social'),
      ('ACT-05','Acheteurs','Monopole sans variation Utility','Supplément Cash',488,'TRANSFER','Service et Work inchangés'),
      ('ACT-06','Acheteurs','Monopole de brevet','Composantes productive et supplémentaire',490,'MIXED','Séparer amélioration Utility et prix supplémentaire non productif'),
      ('ACT-07','Emprunteur','Prêteur','Principal et intérêts',344,'CONDITIONAL_BRANCHES','Voir SC-MONEY-30/31: dévaluation ou Work supplémentaire; pas une seule branche'),
      ('ACT-08','Détenteur Money','Même détenteur','Épargne puis dépense',468,'INTERTEMPORAL_REALLOCATION','Potentiel/cinétique économique, pas énergie mécanique littérale')]
    save('analysis/data/agent_transfers.json',[dict(id=id,from_actor=a,to_actor=b,object=obj,page=p,classification=kind,conditions=[cond],global_creation_from_transfer_alone=False) for id,a,b,obj,p,kind,cond in agents])
    save('analysis/data/terminal_review_issues.json',[
      dict(id='TERM-01',pages=[467,470],status='INCONSISTENT',scope='Local displayed implication constant Force → constant a/e',reason='F*Δt=Δa (ou Δe) requires F=0 or zero interval, not arbitrary nonzero constant F; prose no additional force may mean zero net force.',visual_checked_pages=[467]),
      dict(id='TERM-02',pages=[413,414,464],status='PARTIALLY_RESOLVED',scope='État économique versus entropie physique',reason='Hypothèse sans pertes conservée; dS=δQ/T exige chemin réversible ou bilan de production d’entropie, non fourni par simple insertion des rendements.'),
      dict(id='TERM-03',pages=[203,207,471,547,553,554,556,557],status='AMBIGUOUS',scope='T / dT / Tpos / Tneg',reason='T intégré entre deux instants p471; état quadratique p207; Work restant p547; changement de référent explicite p553–554; aucune conversion globale univoque établie.',visual_checked_pages=[554]),
      dict(id='TERM-04',pages=[384,385,388,389,551,552],status='PARTIALLY_RESOLVED',scope='Rendements et signes',reason='η=−M/T avec M sortant négatif; dérivée quotient cohérente. Domaine de maximum34% et signe des branches hors équilibre restent ouverts.'),
      dict(id='TERM-05',pages=[548,550,553,554],status='AMBIGUOUS',scope='Métrique du champ',reason='Addition ω²+varpi² et seuil d’angle exigent échelles communes. Substitution e=cpω dans ω² donne e²/cp², tandis que p554 affiche des dénominateurs cp,ca; changement de normalisation non explicité.',visual_checked_pages=[554]),
      dict(id='TERM-06',pages=[489,490],status='PARTIALLY_RESOLVED',scope='Monopole ne crée jamais',reason='La formule générale p489 doit conserver la branche brevet productif p490; pas de réfutation globale à partir du seul intitulé.'),
      dict(id='TERM-07',pages=[538,558,559],status='NOT_ESTABLISHED',scope='Micro → macro et K',reason='Réserve explicite locale puis hypothèse de stabilisation et identification GDP. Les données ne testent pas les variables T/M indépendamment.')])
    # This file does not alter previous locked productive/money scenario snapshots.
    save('analysis/data/terminal_regression_rules.json',dict(
        energy_gdp_derived_is_independent=False,energy_direct_is_statistically_exogenous=False,
        correlation_implies_causation=False,physical_energy_equals_economic_variable_by_default=False,
        transfer_implies_global_creation=False,aggregation_requires_conditions=True,
        required_aggregation_ids=[a['id'] for a in aggregation],environmental_levels=['SOURCE_EXPLICIT','SOURCE_IMPLICIT','RESEARCH_INTERPRETATION'],
        required_alternatives=['CPC-0124','CPC-0125'],prior_claims_preserved=True))
    print('Integrated',len(claims),'claims;',sum(r['examined'] for r in coverage),'pages examined')

if __name__=='__main__':main()
