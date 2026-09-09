import json,glob,os,re
os.makedirs('rag/index',exist_ok=True)
rows=[]
for p in glob.glob('corpus/extracted/*.jsonl'):
 for line in open(p):
  r=json.loads(line); txt=r['text'].strip()
  if txt: rows.append({'document':r['document'],'page':r['page_pdf'],'chunk':f"{r['document']}#p{r['page_pdf']}",'text':txt})
for p in ['README.md','articles/purpose.md']:
 txt=open(p,encoding='utf8').read(); rows.append({'document':p,'page':None,'chunk':p,'text':txt})
json.dump(rows,open('rag/index/chunks.json','w'),ensure_ascii=False)
json.dump({'chunks':len(rows),'method':'lexical TF-IDF fallback','source':'local'},open('rag/index/manifest.json','w'),indent=2)
print(len(rows))
