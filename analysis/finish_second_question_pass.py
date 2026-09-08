"""Complete scenario ledger, evidence counters and second-pass reporting."""
import json
from pathlib import Path
from integrate_second_question_pass import ROOT,OUT,write,dump,table
from second_pass_catalog import ORDER,REVIEWS

def main():
    # Reserve new BIB IDs in the central registries, preventing future collisions.
    local=json.loads((OUT/'second_pass_literature.json').read_text())
    new=[s for s in local['sources'] if s['id'] in local['new_ids']]
    central=ROOT/'bibliography/initial_research_library.json'
    library=json.loads(central.read_text());known={s['id'] for s in library}
    library += [s for s in new if s['id'] not in known];dump(central,library)
    mpath=ROOT/'analysis/data/literature_map.json';mapping=json.loads(mpath.read_text());known={s['id'] for s in mapping['sources']}
    mapping['sources'] += [s for s in new if s['id'] not in known];dump(mpath,mapping)
    bpath=ROOT/'bibliography/research_library.bib';btext=bpath.read_text()
    if '@misc{BIB-0017,' not in btext:write(bpath,btext+'\n'+(ROOT/'bibliography/second_pass_research.bib').read_text())
    scenarios=json.loads((ROOT/'analysis/data/money_compensation_scenarios.json').read_text())['scenarios']
    tags={1:[],2:['REVALUED'],3:['REVALUED'],4:['CREATED'],5:['DESTROYED'],6:['CREATED'],7:['DESTROYED'],
        8:['REVALUED'],9:['DESTROYED','REVALUED'],10:['REVALUED'],11:['REVALUED'],12:['CREATED'],13:['REVALUED'],
        14:['REVALUED'],15:['DESTROYED'],16:[],17:['REDISTRIBUTED'],18:['REVALUED'],19:['REVALUED'],20:['REVALUED'],
        21:['REVALUED'],22:[],23:['REDISTRIBUTED'],24:[],25:['TRANSFERRED','REDISTRIBUTED'],26:[],27:['REDISTRIBUTED'],
        28:[],29:['REVALUED'],30:['REVALUED'],31:['CREATED'],32:[]}
    ledger=[]
    md='# Bilans des32 scénarios conservés\n\nTypologie éditoriale non exclusive ; une étiquette ne tranche pas le bilan global. CREATED/DESTROYED reprend l’issue annoncée dans la branche, pas un résultat empirique. REVALUED peut coexister avec M global constant. Étiquette vide : stabilité, mélange, représentation ou conclusion non univoque. Les scénarios restent ceux de l’inventaire antérieur, non32 nouvelles lectures exhaustives.\n\n'
    md+='| Scénario / pages | Opérations | État fixe | Ajustement | Résultat |\n|---|---|---|---|---|\n'
    for i,s in enumerate(scenarios,1):
        row=dict(id=s['id'],name=s['name'],pages=s['pages'],sources=s['sources'],operation_tags=tags[i],
            initial_state=s['initial_state'],fixed=s['fixed_variables'],adjusted=s['adjusted_variables'],
            result=s['expected_result'],conditions=s['conditions'],exceptions=s['exceptions'],
            agents='Voir acteurs nommés dans sources/contexte ; global, consommateur et fournisseur ne sont pas interchangeables.',
            horizon='Différé explicitement' if i in [8,9,10,11,19,22,29] else 'Comparaison de scénarios ; délai numérique non spécifié',
            Cash=s['relation_to_Cash'],Money=s['relation_to_Money'],purchasing_power=s['relation_to_purchasing_power'],
            production=s['causal_mechanism'],credit_interest='Crédit/remboursement ou intérêts explicites' if i in [3,18,30,31] else 'Pas de variable de crédit imposée',
            balance_status='CONDITIONAL_SOURCE_RECONSTRUCTION_NOT_EMPIRICAL')
        ledger.append(row)
        clean=lambda x:str(x).replace('|','/').replace('\n',' ')
        md+='| '+' | '.join(map(clean,[s['id']+' '+str(s['pages']),', '.join(tags[i]) or 'sans classement forcé',s['fixed_variables'],s['adjusted_variables'],s['expected_result']]))+' |\n'
    md+='\nLe JSON associé conserve citations, agents/frontières, horizon, Cash, Money, pouvoir d’achat, conditions, exceptions et rôle productif. Il ne transforme pas émission de dépôts en création de richesse. L’écriture de crédit est distincte du financement éventuel d’une transformation ultérieure.\n'
    write(OUT/'RQ-06.04/scenario_balances.md',md);dump(OUT/'RQ-06.04/scenario_balances.json',ledger)
    g=json.loads((OUT/'question_graph.json').read_text());by={q['id']:q for q in g['nodes']};history=json.loads((OUT/'history.json').read_text())
    for id in ORDER:
        q=by[id];r=REVIEWS[id]
        claimed={
            'RQ-03.02':'Le Work dépensé correspond à une variation cinétique compensée par une réserve ; l’auteur explicite des référents accompli/restant.',
            'RQ-08.03':'Les potentiels annoncés sont des fonctions d’état dans le domaine sans pertes et permettent les relations entre variables conjuguées.',
            'RQ-08.01':'Les contributions l,T,e s’additionnent, tandis que les Utilities ne s’additionnent pas.',
            'RQ-08.04':'Le champ labour-prix permet de visualiser et comparer les compétitivités des entreprises.',
            'RQ-06.04':'Crédit et remboursement seuls modifient Cash sans création/destruction globale de Money ; les possibilités se combinent dans la réalité.',
            'RQ-10.01':'Le consommateur dispose d’un supplément après une baisse de prix et peut le conserver ou l’utiliser ultérieurement.',
            'RQ-09.03':'Le Work utile transformé en Money fournit finalement un couplage PIB–énergie, sous le coefficient macro proposé.',
            'RQ-11.02':'L’accès accru aux Products et l’accélération des transformations s’accompagnent de consommation énergétique et de pertes accrues dans l’argument.',
            'RQ-11.03':'Les transformations dégradent l’environnement et ne peuvent être poursuivies indéfiniment dans le raisonnement proposé.',
            'RQ-12.01':'Le manuscrit revendique un formalisme explicatif/prédictif, notamment Core Law et couplage énergétique ; la classification comparative est celle du chercheur.'}
        path=OUT/id/'reconstruction.md';text=path.read_text()
        old='## CLAIMED_RESULT / RECONSTRUCTED_RESULT\n\n'+r['result']
        if old in text:
            text=text.replace(old,'## CLAIMED_RESULT\n\n'+claimed[id])
            text=text.replace('## INTERNAL REVIEW — après reconstruction\n\n','## INTERNAL REVIEW — après reconstruction\n\nConclusion de recherche : '+r['result']+'\n\n')
            write(path,text)
        if id in ['RQ-03.02','RQ-08.01','RQ-08.03','RQ-08.04','RQ-06.04']:
            eid='EVID-SUPPORT-'+id+'-FORMAL'
            if eid not in q['evidence']:
                e=dict(id=eid,question=id,claim=None,type='FORMAL',relation='PARTIALLY_SUPPORTS',
                    source={'artifact':'research_questions/second_pass_formal_results.json'},content=r['derivation'],
                    force='STRONG for conditional calculation ONLY',limit=r['conditions'],interpretive=True)
                g['evidence'].append(e);q['evidence'].append(eid)
                p=OUT/id/'evidence.md';write(p,p.read_text()+'\n### '+eid+'\n\nFORMAL ; PARTIALLY_SUPPORTS ; STRONG pour le calcul conditionnel seulement.\n\n'+r['derivation']+'\n\nSource : second_pass_formal_results.json ; limites : '+r['conditions']+'\n')
        if id in ['RQ-09.03','RQ-10.01']:
            e=next(e for e in g['evidence'] if e['id']=='EVID-COUNTER-'+id+'-01')
            e['type']='EMPIRICAL';e['source']={'artifact':'analysis/empirical/'+('independent_energy' if id=='RQ-09.03' else 'micro_electricity')+'/results.json'}
            p=OUT/id/'evidence.md';write(p,p.read_text().replace('Type : LOGICAL ; relation : QUALIFIES','Type : EMPIRICAL ; relation : QUALIFIES'))
        for h in history:
            if h.get('action')=='SECOND_PASS' and h.get('id')==id:h['new_evidence']=q['evidence']
    dump(OUT/'question_graph.json',g);dump(OUT/'history.json',history)
    table(OUT/'evidence_matrix.csv',['Question','Corpus evidence','Formal evidence','Empirical evidence','External literature','Counterevidence','Tests available','Status','Confidence'],
        [(q['id'],sum(e['type']=='TEXTUAL' for e in g['evidence'] if e['question']==q['id']),
          sum(e['type'] in ['FORMAL','LOGICAL'] for e in g['evidence'] if e['question']==q['id']),
          sum(e['type']=='EMPIRICAL' for e in g['evidence'] if e['question']==q['id']),len(q['literature']),
          sum(e.get('counter_kind') is not None or e['type']=='COUNTEREXAMPLE' for e in g['evidence'] if e['question']==q['id']),q['test_design_status'],q['status'],q['confidence']) for q in g['nodes']])
    print('32 scenario ledgers; formal and empirical evidence counters synchronized')
if __name__=='__main__':main()
