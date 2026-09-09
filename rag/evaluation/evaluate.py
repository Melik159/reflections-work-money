"""Page-and-passage retrieval benchmark. No language model involved."""
import hashlib
import json
from pathlib import Path
from rag.retrieval import Retriever
from rag.bilingual import expand, normalized
ROOT=Path(__file__).resolve().parents[2]

def measure(hits,q):
    relevant={p['page']:p['passage'] for p in q['expected_passages']}
    ranks=[]
    good=set()
    recall={}
    for rank,hit in enumerate(hits,1):
        p=hit['page']
        if (hit['document']==q['expected_document'] and p in relevant and
            relevant[p] in ' '.join(hit['text'].split())):
            ranks.append(rank); good.add(p)
        if rank in [1,3,5]:
            recall[f'Recall@{rank}']=len(good)/len(relevant)
    for k in [1,3,5]:
        recall.setdefault(f'Recall@{k}',len(good)/len(relevant))
    return dict(recall,MRR=1/min(ranks) if ranks else 0)

def main():
    index=ROOT/'rag/index/chunks.json'; golden=ROOT/'rag/evaluation/golden_questions.jsonl'
    rows=json.loads(index.read_text())
    retriever=Retriever([r for r in rows if r['document'] in ['Reflections_PierreCampergue.pdf','README.md','articles/purpose.md']])
    extended=Retriever(rows)
    qs=[json.loads(l) for l in golden.read_text().splitlines()]
    runs={}
    for method in ['legacy','tfidf','bm25','bm25_extended','bm25_normalized','bm25_bilingual']:
        details=[]
        for q in qs:
            query=expand(q['question']) if method=='bm25_bilingual' else normalized(q['question']) if method=='bm25_normalized' else q['question']
            engine=extended if method in ['bm25_extended','bm25_normalized','bm25_bilingual'] else retriever
            hits=engine.search(query,'bm25' if method.startswith('bm25') else method,5)
            details.append(dict(id=q['id'],language=q['language'],metrics=measure(hits,q),
                retrieved=[dict(document=h['document'],page=h['page'],chunk=h['chunk'],score=h['score']) for h in hits]))
        aggregate=lambda rows:{key:sum(r['metrics'][key] for r in rows)/len(rows) for key in ['Recall@1','Recall@3','Recall@5','MRR']}
        runs[method]=dict(metrics=aggregate(details),by_language={lang:aggregate([r for r in details if r['language']==lang]) for lang in ['en','fr']},details=details)
    result=dict(golden_questions=len(qs),comparison_scopes={'legacy/tfidf/bm25':'original 3 documents, unchanged baseline','bm25_extended/normalized/bilingual':'5 documents including both secondary PDFs'},index_sha256=hashlib.sha256(index.read_bytes()).hexdigest(),golden_sha256=hashlib.sha256(golden.read_bytes()).hexdigest(),
        scope='Development benchmark on reviewed pages; not a whole-manuscript or held-out evaluation.',
        mrr_definition='MRR truncated at rank 5',recall_definition='Fraction of expected pages retrieved with exact normalized supporting passage.',methods=runs)
    (ROOT/'rag/evaluation/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({m:v['metrics'] for m,v in runs.items()},indent=2))

if __name__=='__main__':
    main()
