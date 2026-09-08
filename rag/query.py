"""python3 -m rag.query --method bm25 'Cash Money'"""
import argparse
import json
from pathlib import Path
from rag.retrieval import Retriever
from rag.bilingual import expand

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('question',nargs='+')
    parser.add_argument('--method',choices=['legacy','tfidf','bm25'],default='bm25')
    parser.add_argument('-k',type=int,default=5)
    parser.add_argument('--no-expansion',action='store_true')
    args=parser.parse_args()
    rows=json.loads((Path(__file__).parent/'index/chunks.json').read_text())
    question=' '.join(args.question)
    query=expand(question) if args.method=='bm25' and not args.no_expansion else question
    for hit in Retriever(rows).search(query,args.method,args.k):
        hit['query_used']=query
        hit['excerpt']=hit.pop('text')
        print(json.dumps(hit,ensure_ascii=False))

if __name__=='__main__':
    main()
