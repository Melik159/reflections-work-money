"""Acquire modest official snapshots after a written design, with no overwrites."""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/empirical/micro_electricity/source'
URLS={
    **{table+'.csv':'https://www.eia.gov/totalenergy/data/browser/csv.php?tbl='+table for table in ['T09.08','T09.09','TA6','T07.02B','T07.06']},
    'reliability.html':'https://www.eia.gov/electricity/annual/html/epa_11_01.html',
    'heat_rate_notes.html':'https://www.eia.gov/electricity/annual/html/epa_08_01.html',
    **{f'bls_cpi_{a}_{b}.json':f'https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear={a}&endyear={b}' for a,b in [(2001,2010),(2011,2020),(2021,2023)]},
}
def main():
    design=ROOT/'analysis/31_micro_test_design.md';assert design.exists()
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'manifest.json'
    if target.exists():
        m=json.loads(target.read_text())
        for f in m['files']:
            assert hashlib.sha256((ROOT/f['file']).read_bytes()).hexdigest()==f['sha256']
        print('Snapshots already present; hashes verified, no network or overwrite.');return
    files=[]
    for name,url in URLS.items():
        p=OUT/name
        if not p.exists():
            data=urllib.request.urlopen(url,timeout=45).read()
            assert len(data)>100,(name,'empty source')
            p.write_bytes(data)
        files.append(dict(file=str(p.relative_to(ROOT)),url=url,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
    m=dict(acquired='2026-09-08',design_file=str(design.relative_to(ROOT)),design_sha256=hashlib.sha256(design.read_bytes()).hexdigest(),
           selection_file='analysis/31_micro_data_selection.md',files=files,
           snapshot_policy='Live institutional downloads archived once; future revisions need a new directory and manifest.',
           selected_window=[2001,2023],quality_window=[2014,2023],
           failed_acquisitions=[dict(url='https://fred.stlouisfed.org/graph/graph.csv?id=CPIAUCNS&cosd=2001-01-01&coed=2023-12-31',status='HTTP404',fallback='Direct BLS API CUUR0000SA0, same general CPI-U NSA concept')])
    target.write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps(m,indent=2))
if __name__=='__main__':main()
