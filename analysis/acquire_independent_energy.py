"""Acquire a pinned pre-2026-method-change OWID release; never replace snapshots."""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/empirical/independent_energy/source'
COMMIT = '4249f7c21c2c833d76741e757be92a639517caa3'

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name in ['owid-energy-data.csv', 'owid-energy-codebook.csv', 'README.md']:
        url = f'https://raw.githubusercontent.com/owid/energy-data/{COMMIT}/{name}'
        path = OUT / name
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        manifest.append(dict(file=str(path.relative_to(ROOT)), url=url,
                             sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             bytes=path.stat().st_size))
    result = dict(commit=COMMIT, acquisition_date='2026-09-08', files=manifest,
                  energy_column='primary_energy_consumption', unit='TWh',
                  population_column='population',
                  independent_of_gdp_construction=True, statistically_exogenous=False,
                  convention='Pinned 2025 release; primary energy substitution convention, not final energy or exergy',
                  scope='Energy Institute/EIA compiled by OWID; see codebook and source README. No energy/GDP column used.')
    target = OUT / 'manifest.json'
    if target.exists():
        assert json.loads(target.read_text()) == result, 'Snapshot drift'
    else:
        target.write_text(json.dumps(result, indent=2) + '\n')
    audit_files = []
    etl = '3bad71c46a5810338b081bb95ebb0fe78501a9a0'
    for name, url in [
        ('primary_energy_processing.py', f'https://raw.githubusercontent.com/owid/etl/{etl}/etl/steps/data/garden/energy/2025-06-27/primary_energy_consumption.py'),
        ('wb_energy_ratio_metadata.html', 'https://databank.worldbank.org/metadataglossary/world-development-indicators/series/EG.GDP.PUSE.KO.PP.KD'),
    ]:
        p = OUT/name
        if not p.exists():
            p.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        audit_files.append(dict(file=str(p.relative_to(ROOT)),url=url,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    audit = dict(etl_commit=etl,acquisition_date='2026-09-08',files=audit_files,
                 note='ETL reference implementation inspected, not a claim to have rerun all upstream ETL; WB live metadata snapshot, not proof of identical historical vintages.')
    p = OUT/'upstream_audit.json'
    if p.exists(): assert json.loads(p.read_text()) == audit
    else: p.write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
