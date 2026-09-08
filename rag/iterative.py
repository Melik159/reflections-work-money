"""Opt-in provenance-separated retrieval. Does not modify the frozen baseline index.

python -m rag.iterative build
python -m rag.iterative query --collection SOURCE_CORPUS 'Money saved'
python -m rag.iterative benchmark
Vector fallback: local lexical TF-IDF, NOT semantic/neural embeddings.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from rag.retrieval import Retriever
from rag.bilingual import expand
from rag.evaluation.evaluate import measure

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'rag/index/iterative.json'
COLLECTIONS=['SOURCE_CORPUS','DERIVED_ANALYSIS','EXTERNAL_LITERATURE']

def load_claims():
    return [json.loads(s) for s in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]

def build():
    claims=load_claims()
    questions=json.loads((ROOT/'research_questions/question_graph.json').read_text())['nodes']
    rows=[]; inputs={}
    def read(p):
        b=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest()
        return b.decode('utf-8')
    def add(document,page,section,text,level,collection,linked=(),locator=None):
        if not text.strip():return
        ids=[c['id'] for c in linked]
        key=f'{collection}:{document}:{page}:{level}:{locator or section}'
        chunk=key+':'+hashlib.sha256(text.encode()).hexdigest()[:12]
        rows.append(dict(document=document,page=page,section=section,chunk_id=chunk,chunk=chunk,
            text=text,level=level,collection=collection,source_type=collection,
            concepts=sorted({x for c in linked for x in c.get('concepts',[])}),claims=ids,
            questions=[q['id'] for q in questions if set(ids)&set(q.get('claims',[]))],
            locator=locator,metadata_origin='Analyst links; not part of source quotation'))
    for p in sorted((ROOT/'corpus/extracted').glob('*.jsonl')):
        for line in read(p).splitlines():
            r=json.loads(line);page=r['page_pdf'];doc=r['document'];text=r['text']
            linked=[c for c in claims if c['source']['document']==doc and page in c['source'].get('pages',[c['source']['page']])]
            add(doc,page,'UNDETECTED',text,'PAGE','SOURCE_CORPUS',linked)
            # Extraction boundaries only: no claim of syntactic paragraph detection.
            for i,paragraph in enumerate(re.split(r'\n\s*\n',text)):
                if len(paragraph.strip())>=80:
                    add(doc,page,'UNDETECTED',paragraph,'PARAGRAPH','SOURCE_CORPUS',linked,str(i))
            for c in linked:
                # Full source page context, not the assistant's claim statement.
                add(doc,page,'UNDETECTED',text,'CLAIM_WINDOW','SOURCE_CORPUS',[c],c['id'])
    original=['README.md','articles/purpose.md']
    for name in original:
        p=ROOT/name;add(name,None,'DOCUMENT',read(p),'SECTION','SOURCE_CORPUS')
    paths=set()
    for folder in ['analysis','research_questions','external_review','remediation','closure_review']:
        for p in (ROOT/folder).rglob('*.md'):
            if not any(x in p.parts for x in ['history','global_corpus_pass','synthesis_draft_before_editorial_check']):paths.add(p)
    paths.update(ROOT/n for n in ['analysis/data/claims.jsonl','analysis/data/concepts.json','research_questions/question_graph.json'])
    for p in sorted(paths):
        name=str(p.relative_to(ROOT));text=read(p)
        linked=[c for c in claims if c['id'] in text]
        if p.suffix=='.md':
            # Preserve the Markdown heading hierarchy in section metadata.
            headings=[];buffer=[];n=0
            for line in text.splitlines()+['# END_SENTINEL']:
                m=re.match(r'^(#{1,6})\s+(.*)',line)
                if m:
                    if buffer:
                        add(name,None,' / '.join(headings) or 'PREAMBLE','\n'.join(buffer),'SECTION','DERIVED_ANALYSIS',linked,str(n));n+=1
                    headings=headings[:len(m[1])-1]+[m[2]];buffer=[line]
                else:buffer.append(line)
        else:
            values=[json.loads(s) for s in text.splitlines()] if p.suffix=='.jsonl' else json.loads(text)
            if isinstance(values,dict):values=values.get('nodes',[values])
            for i,value in enumerate(values):add(name,None,str(value.get('id',i)),json.dumps(value,ensure_ascii=False),'CLAIM_WINDOW','DERIVED_ANALYSIS',linked,str(i))
    result=dict(rows=rows,input_sha256=inputs,collections={c:sum(r['collection']==c for r in rows) for c in COLLECTIONS},
        external_policy='Empty until verified external full texts are explicitly registered; internal literature notes remain DERIVED_ANALYSIS.',
        embeddings='UNAVAILABLE: no installed sentence-transformers or cached model; TF-IDF lexical vectors used, not semantic embeddings.',
        paragraph_policy='Blank-line extraction blocks; not guaranteed true paragraphs. PDF sections UNDETECTED, never invented.')
    INDEX.parent.mkdir(exist_ok=True);INDEX.write_text(json.dumps(result,ensure_ascii=False))
    print(json.dumps(result['collections']))

def search(rows,question,method='bm25',k=5):
    engine=Retriever(rows);q=expand(question)
    if method!='hybrid':return engine.search(q,method,k)
    fused={};scores=Counter()
    for backend in ['bm25','tfidf']:
        for rank,h in enumerate(engine.search(q,backend,50),1):
            key=h['chunk_id'];fused[key]=h;scores[key]+=1/(60+rank)
    return [dict(fused[key],score=value,score_type='RRF_BM25_TFIDF') for key,value in scores.most_common(k)]

def benchmark():
    data=json.loads(INDEX.read_text());pages=[r for r in data['rows'] if r['collection']=='SOURCE_CORPUS' and r['level'] in ['PAGE','SECTION']]
    old=json.loads((ROOT/'rag/index/chunks.json').read_text())
    qs=[json.loads(s) for s in (ROOT/'rag/evaluation/golden_questions.jsonl').read_text().splitlines()]
    results={}
    for name,rows,method in [('baseline_bm25',old,'bm25'),('separated_bm25',pages,'bm25'),('separated_tfidf',pages,'tfidf'),('separated_hybrid',pages,'hybrid')]:
        details=[dict(id=q['id'],metrics=measure(search(rows,q['question'],method),q)) for q in qs]
        results[name]=dict(metrics={m:sum(d['metrics'][m] for d in details)/len(details) for m in ['Recall@1','Recall@3','Recall@5','MRR']},details=details)
    out=dict(golden_questions=len(qs),methods=results,scope='Existing development set, page+exact-passage relevance. No derived-collection golden set or held-out evidence. Paragraph/section retrieval NOT benchmarked by these page comparisons.',
        index_sha256=hashlib.sha256(INDEX.read_bytes()).hexdigest(),default='bm25',embeddings=data['embeddings'])
    (ROOT/'research_state/rag_benchmark.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v['metrics'] for k,v in results.items()},indent=2))

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    s.add_parser('build');s.add_parser('benchmark');q=s.add_parser('query')
    q.add_argument('question');q.add_argument('--collection',choices=COLLECTIONS,required=True)
    q.add_argument('--level',choices=['PAGE','PARAGRAPH','SECTION','CLAIM_WINDOW']);q.add_argument('--method',choices=['bm25','tfidf','hybrid'],default='bm25');q.add_argument('-k',type=int,default=5)
    a=p.parse_args()
    if a.cmd=='build':build()
    elif a.cmd=='benchmark':benchmark()
    else:
        rows=[r for r in json.loads(INDEX.read_text())['rows'] if r['collection']==a.collection and (not a.level or r['level']==a.level)]
        if a.collection=='SOURCE_CORPUS' and not a.level:
            rows=[r for r in rows if r['level'] in ['PAGE','SECTION']]
        for hit in search(rows,a.question,a.method,a.k):print(json.dumps(hit,ensure_ascii=False))
if __name__=='__main__':main()
