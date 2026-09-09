"""Editorial development questions on actually examined pages, not held-out."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
QUESTIONS='''1|root_question|What key question links living standards, environmental damages and the affluent society?
3|root_question|How does the abstract compare work into money with heat into work?
4|argument_dependencies|Which slow and regular behaviours permit application of the formalism?
5|money|Does changing the number of monetary units alter the overall wealth of the system?
6|definitions|What is manufactured or accomplished by humans under the definition of Product?
7|definitions|Which of creation distribution and use belong to natural and human sciences?
8|production|Does production take place before consumption?
9|argument_dependencies|What is the law that only work generates change?
10|money|How is Money measured as number of units multiplied by value of unit?
11|argument_dependencies|What differential follows from M=n.u?
12|money|Why would changing the number of units cause an inverse change in their value?
13|money|Do loans not covered by deposits create Money?
14|mechanisms|What happens to existing Money under an economic policy without Work expenditure?
15|purchasing_power|How is Money defined as the additional amount held after a price drop?
16|mechanisms|What phenomenological sequence connects additional supplier work to additional consumer money?
17|energy|Why is increasing productivity said to require additional Work as energy?
18|energy|What role do low-cost artificial energy sources play in the transition to abundance?
19|work|How does a reduction in cost price distinguish productive and unproductive Work?
20|prices|Can the selling price remain constant despite a drop in cost price?
21|prices|Who chooses selling prices subject to competition and regulations?
22|mechanisms|What supplementary Work is transformed into supplementary Money?
23|argument_dependencies|How does destruction of Work to be done compensate the Money generated?
24|mechanisms|How is physical transformation distinguished from an accounting flow?
25|purchasing_power|Why does the consumer get richer when unit value decreases less than number increases?
26|purchasing_power|Why does the consumer become poorer in deflation?
27|prices|What balance is sought between supply policy and demand policy?
28|counterexamples|Can bankers be useful to society despite being unable to create Money?
29|environment|What is claimed about purchasing power from the Neolithic period to the eighteenth century?
30|argument_dependencies|Why must studies of creation of Money exclude reference to the Human Being?
31|environment|Which effects and environmental impacts are excluded from the economic preamble?
32|work|What external constraints limit the maximum Economy of Work?
33|money|What external constraints limit the maximum Economy of Money?
34|money|Is Money exchanged in barter?
35|energy|Why does the eight hours to six hours example claim about 78 percent more Work?
36|work|Is a Work variation used to manufacture a Product or to vary its price?
37|production|How is the offer defined by manufacturing cycles per unit of time?
38|production|How do purchase manufacturing contract and use correspond to thermodynamic cycle steps?
39|energy|Are Work and Money considered forms of Economic Energy?
40|work|Should Work to be done or Work performed be taken into account?
41|definitions|Which vector-supports contain economic Work and Money?
42|energy|Why is entropy prohibited in the economic formalism?
43|mechanisms|What equivalence principle is written as M=g.T?
44|counterexamples|Must the transformation coefficient g be constant in Economics?
45|prices|How does consumer Force F and price variation dp define dM?
47|counterexamples|Why do abrupt sale discounts challenge continuous price variations?
48|definitions|Does monetary wealth include the assets of an economic agent?
50|money|Is an inscription of a bank credit line Money or Cash?
51|definitions|What is labour l for a given Product and manufacturing method?
52|work|Can Work vary with execution speed while labour remains constant?
53|definitions|How is Money defined as the measure of the value of Cash?
54|definitions|How does complexity c represent inertia against changes in labour execution speed?
55|definitions|Can Utility be subjective or objective, accurate or erroneous?
56|bibliography|Whose sense of Utility is used instead of marginal utility?
57|counterexamples|How can Utility vary between agents such as a surgeon and other consumers?
58|counterexamples|Why is the price of a work of art said not to decrease?
59|purchasing_power|How is Utility of Cash related to the income of an agent?
60|definitions|Can a wholesaler or trader be a manufacturer without modifying a Product?
61|argument_dependencies|Which of Seller Transformer and Acquirer are inside the system?
62|mechanisms|How does the position of the observer change the Utility perspective?
63|argument_dependencies|Which sign is assigned to what the Transformer receives?'''
FRENCH='''1|root_question|Quelle question initiale relie niveau de vie, abondance et dommages environnementaux ?
53|money|Quelle différence entre Cash et Money ?
51|work|Comment distinguer labour et Economic Work ?
16|mechanisms|Comment la productivité crée-t-elle du pouvoir d’achat ?
19|production|Quel critère distingue travail productif et improductif ?
42|energy|Quelle place l’auteur accorde-t-il à l’entropie ?'''

def main():
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    pages={r['page_pdf']:' '.join(r['text'].split()) for r in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    result=[]
    for language,questions in [('en',QUESTIONS),('fr',FRENCH)]:
        for line in questions.splitlines():
            number,category,question=line.split('|'); number=int(number)
            c=claims[number-1]; source=c['source']
            evidence=[dict(page=p,passage=source['quotation']) for p in source['pages'] if source['quotation'] in pages[p]]
            if number==1:
                evidence=[dict(page=2,passage='The key question is therefore to understand how the increase in living standards has led to these environmental'),dict(page=3,passage='damages, or how we have moved from a subsistence society to an affluent society.')]
            assert evidence,(number,source)
            result.append(dict(id=f'GQ-{len(result)+1:03}',question=question,category=category,language=language,
                expected_document=source['document'],expected_pages=[e['page'] for e in evidence],
                expected_claims=[c['id']],expected_concepts=c['concepts'],expected_passages=evidence,
                split='development',scope='examined_pages_only',relevance_complete=False))
    (ROOT/'rag/evaluation/golden_questions.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in result))

if __name__=='__main__':
    main()
