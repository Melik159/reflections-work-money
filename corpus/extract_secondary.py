"""Deterministic page extraction of the two secondary PDFs only."""
import hashlib
import json
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
def main():
    records=[]
    for name in ['economic_growth_energy_campergue','hidden_materiality_of_growth']:
        source=ROOT/'articles'/f'{name}.pdf'
        with pymupdf.open(source) as doc:
            pages=[dict(document=f'articles/{name}.pdf',page_pdf=i+1,text=p.get_text('text'),section=None) for i,p in enumerate(doc)]
        dest=ROOT/'corpus/extracted'/f'{name}.pages.jsonl'
        dest.write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in pages))
        records.append(dict(document=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),pages=len(pages),empty_pages=[p['page_pdf'] for p in pages if not p['text'].strip()],extractor='PyMuPDF',version=pymupdf.VersionBind))
    (ROOT/'corpus/metadata/secondary_extraction.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records))
if __name__=='__main__':main()
