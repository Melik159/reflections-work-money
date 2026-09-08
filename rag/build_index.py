"""Rebuild the existing page index; does not re-extract or claim analytical reading."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    rows=[]; sources=[]
    for p in sorted((ROOT/'corpus/extracted').glob('*.jsonl')):
        sources.append(p)
        for line in p.read_text().splitlines():
            r=json.loads(line); txt=r['text'].strip()
            if txt:
                rows.append(dict(document=r['document'],page=r['page_pdf'],chunk=f"{r['document']}#p{r['page_pdf']}",text=txt))
    for name in ['README.md','articles/purpose.md']:
        p=ROOT/name; sources.append(p)
        rows.append(dict(document=name,page=None,chunk=name,text=p.read_text()))
    dest=ROOT/'rag/index'; dest.mkdir(exist_ok=True)
    (dest/'chunks.json').write_text(json.dumps(rows,ensure_ascii=False))
    manifest=dict(chunks=len(rows),documents=sorted({r['document'] for r in rows}),
        methods=['legacy','tfidf','bm25'],default='bm25',chunking='existing one-page chunks; Markdown whole-file',
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        query_expansion='rag/bilingual.py; French to English vocabulary; disable with --no-expansion',
        scope='Three PDFs and two Markdown files. Code documentation not yet indexed.')
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(len(rows))

if __name__=='__main__': main()
