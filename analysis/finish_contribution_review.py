"""Scenario crosswalk and narrow question-tree annotations."""
import json
from pathlib import Path
from build_contribution_review import ROOT,OUT,write,dump,table
SC={
1:'État stationnaire des soldes nominaux et de leur pouvoir d’achat',2:'Émission nominale avec ajustement réel supposé; crédit et compensation ne sont pas synonymes',3:'Remboursement de dépôts/dette; effet sur richesse réelle séparé',4:'Baisse de prix à soldes nominaux fixes; gain de panier',5:'Érosion du pouvoir d’achat à soldes fixes',6:'Accommodation nominale après modification productive; causalité à établir',7:'Contraction nominale après perte réelle postulée',8:'Inflation du corpus définie aussi par Utility: pas taux CPI automatiquement',9:'Dévaluation externe ou changement de valeur interne à distinguer',10:'Déflation du corpus et déflation d’un indice non équivalentes',11:'Réévaluation et appréciation réelle dépendent du référent',12:'Prix et Utility baissent: nomenclature de scénario, pas surplus mesuré',13:'Prix baisse et Utility augmente: ne pas confondre qualité supérieure et déflation standard',14:'Prix monte et Utility baisse: prix ajusté/évolution du besoin à distinguer',15:'Prix et Utility montent: préférence contextuelle distincte de prix réel',16:'Redénomination et invariance à l’unité de compte',17:'Incidence distributive et transferts entre agents',18:'Création bancaire de dépôts ≠ attribution exclusive à neutralité réelle',19:'Délais d’ajustement, inertie des prix; horizon explicite',20:'Monnaie marchandise, confiance et moyens de paiement',21:'Prix relatifs à revenu/consommation; dynamique nominale et réelle',22:'Épargne, encaisse de précaution et dépense différée',23:'Budget local et effets externes; frontière de système',24:'Combinaison de chocs nominaux, réels et distributifs',25:'Gain de détention / prix spéculatif / coefficient de conversion',26:'Restriction de co-variation n,u: non déduite de simple identité',27:'Baisse de coût, prix fixe et marge unitaire conditionnelle',28:'Normalisation locale/globale, agrégation et choix de numéraire',29:'Plus-value et réévaluation, pas nouvelle production automatiquement',30:'Dévaluation dans bilan d’intérêts; lien économique non identité',31:'Production couvrant service de dette; paiement d’intérêt ≠ nécessité universelle de Work supplémentaire',32:'Incidence réciproque des échanges; gain de transaction et transfert distincts'}
QMAP={
'RQ-02.01':['wealth','productive creation'],'RQ-02.02':['productive creation','transfer'],'RQ-02.03':['transfer','redistribution'],
'RQ-03.01':['Economic Work','labour'],'RQ-03.02':['Economic Work'],'RQ-03.03':['Economic Work','useful work'],
'RQ-04.02':['Economic Work','productivity-cost-price chain'],'RQ-05.01':['cost','price','productivity-cost-price chain'],'RQ-05.03':['Utility','consumer gain'],
'RQ-06.01':['Cash','Money','n','u'],'RQ-06.02':['Cash','Money','n','u'],'RQ-06.04':['Money','productive creation','transfer'],
'RQ-07.02':['redistribution','transfer'],'RQ-08.01':['K','Utility'],'RQ-08.02':['K'],'RQ-09.02':['energy','useful work','Economic Work'],
'RQ-09.03':['energy','useful work','Money'],'RQ-10.02':['consumer gain','environmental damage'],'RQ-11.01':['environmental damage','losses'],
'RQ-12.01':['Economic Work','K','Utility','Money'],'RQ-12.02':['wealth','environmental damage','productivity-cost-price chain']}
def main():
    if (OUT/'question_links.json').exists():raise SystemExit('Already integrated')
    scenarios=json.loads((ROOT/'analysis/data/money_compensation_scenarios.json').read_text())['scenarios'];rows=[]
    for s in scenarios:
        n=int(s['id'].split('-')[-1]);refs=['BIB-0001','BIB-0020','CBIB-01']
        if n in [12,13,14,15,27]:refs+=['CBIB-06','CBIB-10']
        if n in [17,25,29,30,31,32]:refs+=['BIB-0003','CBIB-04']
        rows.append(dict(id=s['id'],name=s['name'],sources=s['sources'],conditions=s['conditions'],campergue_result=s['expected_result'],standard_comparison=SC[n],translation='Cash: specified instruments/nominal accounts; Money: corpus value concept, not automatically bank deposits or standard real balance',difference='Preserve scenario conditions, Utility and actor/horizon; institutional deposit creation alone does not decide real gain.',relation='PARTIAL_PARALLEL',literature=refs,automatic_money_mapping=False,theoretical_contradiction_inferred_from_terms=False))
    dump('research_questions/contribution/money_scenario_comparisons.json',rows)
    write('research_questions/contribution/money_scenario_comparisons.md','#32 scénarios comparés après traduction\n\nLes sources, résultats et conditions originaux sont conservés dans le JSON associé. Chaque ligne nomme un comparateur, pas une validation de causalité ni un équivalent unique de Money.\n\n'+table(['Scénario','Nom source','Cadre voisin / différence','Littérature'],[(r['id'],r['name'],r['standard_comparison'],', '.join(r['literature'])) for r in rows]))
    concepts={r['term']:r for r in json.loads((OUT/'concepts.json').read_text())}
    g=json.loads((ROOT/'research_questions/question_graph.json').read_text());byid={q['id']:q for q in g['nodes']};history=json.loads((ROOT/'research_questions/history.json').read_text());links=[]
    for qid,terms in QMAP.items():
        q=byid[qid];comparisons=[concepts[t] for t in terms]
        fields=dict(EXISTING_FRAMEWORKS=[r['existing_framework'] for r in comparisons],CAMPERGUE_DIFFERENCE=[r['difference'] for r in comparisons],POTENTIAL_ADDED_VALUE='Clarification or conditional restriction relative to named frameworks; no new empirical prediction established.',NOVELTY_STATUS='HISTORICAL_NOVELTY_UNRESOLVED')
        q['contribution_review']=fields;q['contribution_comparisons']=[r['id'] for r in comparisons]
        history.append(dict(action='CONTRIBUTION_REVIEW',id=qid,old_status=q['status'],new_status=q['status'],old_statement=q['question'],new_statement=q['question'],reason='Add comparison dimension only; no source or scientific-status change',comparison_ids=q['contribution_comparisons']))
        path=f'research_questions/{qid}/contribution.md'
        write(path,f'# {qid} — Comparaison et valeur analytique\n\nQuestion conservée: {q["question"]}\n\n'+''.join('## '+k+'\n\n'+('\n'.join('- '+x for x in v) if isinstance(v,list) else v)+'\n\n' for k,v in fields.items())+'Sources et différences détaillées: '+', '.join(q['contribution_comparisons'])+' dans [comparaisons](../contribution/concept_comparisons.md). Aucun remplacement des définitions sources. Statut scientifique inchangé.\n')
        readme=f'research_questions/{qid}/README.md';write(readme,(ROOT/readme).read_text()+'\n## Contribution / cadres voisins\n\n[Comparaison ciblée](contribution.md): cadres existants, différence résiduelle et utilité potentielle. Aucune originalité historique ni valeur empirique déduite du vocabulaire.\n')
        links.append(dict(question=qid,concepts=terms,comparisons=q['contribution_comparisons']))
    dump('research_questions/question_graph.json',g);dump('research_questions/history.json',history);dump('research_questions/contribution/question_links.json',links)
    m=json.loads((OUT/'manifest.json').read_text());m.update(questions_updated=len(links),scenarios_compared=len(rows),claims_unchanged=127,coverage_unchanged=272);dump('research_questions/contribution/manifest.json',m)
if __name__=='__main__':main()
