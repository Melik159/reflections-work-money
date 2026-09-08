import json,re,sys,math
rows=json.load(open('rag/index/chunks.json'))
q=' '.join(sys.argv[1:]).lower(); terms=re.findall(r'\w+',q); N=len(rows)
df={t:sum(t in r['text'].lower() for r in rows) for t in set(terms)}
out=[]
for r in rows:
 words=re.findall(r'\w+',r['text'].lower()); score=sum(words.count(t)*math.log((N+1)/(df[t]+1)) for t in terms)
 if score: out.append((score,r))
for s,r in sorted(out,reverse=True,key=lambda x:x[0])[:5]: print(json.dumps({'document':r['document'],'page':r['page'],'chunk':r['chunk'],'score':round(s,3),'excerpt':r['text'][:500]},ensure_ascii=False))
