"""Read-only corpus retrieval and dependency map before second-pass analysis."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rag.retrieval import Retriever
OUT=ROOT/'research_questions'
ORDER=['RQ-03.02','RQ-08.03','RQ-08.01','RQ-08.04','RQ-06.04','RQ-10.01','RQ-09.03','RQ-11.02','RQ-11.03','RQ-12.01']
QUERIES={
'RQ-03.02':'Work remaining integral potential kinetic positive negative dT reference',
'RQ-08.03':'state functions potentials exact differential Maxwell losses',
'RQ-08.01':'sum different Works average Products additive quantities',
'RQ-08.04':'field vectors competitiveness angle units labour price coefficient',
'RQ-06.04':'bank credit interest repayment monetary creation destruction saving',
'RQ-10.01':'Money saving consumer investment later purchasing power income price',
'RQ-09.03':'GDP absolute coupling energy consumed useful Work Money',
'RQ-11.02':'consumption savings more Products energy efficiency waste',
'RQ-11.03':'environment damages pollution raw materials transport resources fossil',
'RQ-12.01':'causes analytical relationship coefficient constant experimental reality'}
def main():
    g=json.loads((OUT/'question_graph.json').read_text());by={q['id']:q for q in g['nodes']}
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    text='# Deuxième passe — dépendances avant analyse\n\nOrdre retenu : '+' → '.join(ORDER)+'.\n\n'
    text+='T/dT précède les potentiels ; additivité précède le champ ; le bilan monétaire précède usage et dommage. Les contraintes directes des dix nœuds sont respectées. Les prérequis hors sélection restent visibles et ne sont pas déclarés résolus par cet ordre. RQ-12.01 est traitée en dernier conformément à sa fonction de comparaison ; cela ne transforme pas une priorité de travail en implication textuelle.\n\n'
    for id in ORDER:
        q=by[id];reverse=[x['id'] for x in g['nodes'] if id in x['dependencies']]
        text+=f'## {id}\n\n'+q['question']+'\n\n'
        for name,items in [('Prérequis',[d+' ('+by[d]['status']+')' for d in q['dependencies']]),('Dépendants directs',reverse),
            ('CORE',[c for c in q['claims'] if claims[c]['criticality']=='CORE']),('MAJOR',[c for c in q['claims'] if claims[c]['criticality']=='MAJOR']),('Concepts',q['concepts']),('Chapitres',q['chapters'])]:
            text+=name+' : '+(', '.join(items) or 'aucun direct')+'.\n\n'
    text+='## Périmètres complémentaires sans renommage\n\nRQ-06.04 reste la question du crédit : les bilans création/destruction couvrent aussi RQ-06.02/06.03. RQ-10.01 reste la question du gain réel : les usages demandés sont traités en liaison avec RQ-10.02, sans changer silencieusement son ID ni sa formulation.\n'
    target=OUT/'second_pass_dependency_map.md'
    if target.exists():assert target.read_text()==text
    else:target.write_text(text)
    retriever=Retriever(json.loads((ROOT/'rag/index/chunks.json').read_text()))
    results={id:dict(query=query,hits=retriever.search(query,'bm25',8)) for id,query in QUERIES.items()}
    path=OUT/'second_pass_retrieval.json'
    if path.exists():assert json.loads(path.read_text())==results
    else:path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    for id,item in results.items():
        print(id,[(h.get('document'),h.get('pages'),h.get('page_start'),h.get('score')) for h in item['hits'][:5]])
if __name__=='__main__':main()
