"""Three descriptive experiments, offline, frozen inputs; no causal identification.

OLS uncertainty: Newey-West/Bartlett HAC, lag 3, n/(n-p) correction,
normal asymptotic 95% intervals. These intervals do not cure nonstationarity.
--check compares numerical results instead of overwriting the benchmark.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/empirical/independent_energy'
GDP = ROOT / 'articles/campergue_energy_gdp_code/output_macro/merged_energy_gdp.csv'
COUNTRIES = {'World':'WLD', 'France':'FRA', 'Germany':'DEU', 'United States':'USA', 'China':'CHN', 'India':'IND'}

def fit(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    X = np.column_stack([np.ones(len(y)), x])
    n, p = X.shape
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y-X@b
    z = X*resid[:, None]
    meat = z.T@z
    for lag in range(1, min(3, n-1)+1):
        cross = z[lag:].T@z[:-lag]
        meat += (1-lag/4)*(cross+cross.T)
    bread = np.linalg.inv(X.T@X)
    cov = bread@meat@bread*n/(n-p)
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    return dict(N=n, coefficients=b.tolist(), se_HAC=se.tolist(),
                ci95=[[float(v-1.96*s), float(v+1.96*s)] for v,s in zip(b,se)],
                R2=float(1-np.sum(resid**2)/np.sum((y-y.mean())**2)))

def compute():
    source = OUT/'source'
    manifest = json.loads((source/'manifest.json').read_text())
    for f in manifest['files']:
        assert hashlib.sha256((ROOT/f['file']).read_bytes()).hexdigest() == f['sha256']
    energy = pd.read_csv(source/'owid-energy-data.csv', usecols=['country','year','primary_energy_consumption','population'])
    energy = energy[energy.country.isin(COUNTRIES) & energy.year.between(1990,2023)].copy()
    energy['Country Code'] = energy.country.map(COUNTRIES)
    old = pd.read_csv(GDP)
    df = old[['Country Code','year','gdp_real','gdp_ppp_real']].merge(energy,on=['Country Code','year'],how='outer',validate='one_to_one',indicator=True)
    missing = df[df[['gdp_real','gdp_ppp_real','primary_energy_consumption','population']].isna().any(axis=1)][['Country Code','year','_merge']].astype(str).to_dict('records')
    df = df.dropna(subset=['gdp_real','gdp_ppp_real','primary_energy_consumption','population']).drop(columns='_merge').sort_values(['Country Code','year'])
    assert (df[['gdp_real','gdp_ppp_real','primary_energy_consumption','population']]>0).all().all()
    results = []
    for code, d in df.groupby('Country Code',sort=True):
        assert np.all(np.diff(d.year)==1), 'Annual differences require consecutive years'
        e, g = d.primary_energy_consumption.to_numpy(), d.gdp_real.to_numpy()/1e9
        pop = d.population.to_numpy()
        variants = [('TEST-E1','level',e,g,'billion constant market USD / TWh'),
                    ('TEST-E1','loglog',np.log(e),np.log(g),'elasticity'),
                    ('TEST-E1','dlog',np.diff(np.log(e)),np.diff(np.log(g)),'annual log-change slope'),
                    ('TEST-E2','per_capita_loglog',np.log(e*1e9/pop),np.log(d.gdp_ppp_real.to_numpy()/pop),'PPP GDP/person on kWh/person elasticity')]
        for exp, model, x, y, unit in variants:
            r = fit(x,y)
            r.update(experiment=exp,country=code,model=model,start=int(d.year.min())+(model=='dlog'),end=int(d.year.max()),unit=unit,
                     classification='TEMPORAL_CO_MOVEMENT' if model=='dlog' else 'ASSOCIATION',
                     specificity=['COMPATIBLE_WITH_CAMPERGUE','ALSO_COMPATIBLE_WITH_STANDARD_EXPLANATIONS'],
                     compatibility_scope='Broad energy-production relevance only; not a test of Money, Work, fixed yields or a universal positive slope',
                     causal_identified=False, predictive_validated=False)
            results.append(r)
        # Prespecified calendar split, not selected by goodness of fit.
        lx, ly = np.log(e), np.log(g)
        post = (d.year.to_numpy()>=2007).astype(float)
        r = fit(np.column_stack([lx,post,lx*post]),ly)
        r.update(experiment='TEST-E3',country=code,model='loglog_break_2007',start=int(d.year.min()),end=int(d.year.max()),
                 coefficient_order=['intercept_pre','slope_pre','intercept_shift','slope_shift'],
                 classification='ASSOCIATION',causal_identified=False,predictive_validated=False,
                 specificity=['ALSO_COMPATIBLE_WITH_STANDARD_EXPLANATIONS'],
                 discrimination='NO: stability of a descriptive proxy, not of the unmeasured Campergue yield chain')
        r['periods'] = []
        for label, mask in [('1990-2006',post==0),('2007-2023',post==1)]:
            f = fit(lx[mask],ly[mask]); f['period']=label; r['periods'].append(f)
        results.append(r)
    # A ratio reconstruction can recover independent energy; do not label it tautological solely for using GDP.
    reconstructed = old.gdp_ppp_real/old.gdp_per_energy
    diag = float(np.max(np.abs(reconstructed-old.energy)/old.energy))
    out = dict(status='EXECUTED_DESCRIPTIVE_NOT_CAUSAL',experiments=['TEST-E1','TEST-E2','TEST-E3'],
               energy_independent_of_gdp_construction=True, statistically_exogenous=False,
               source_commit=manifest['commit'], gdp_input_sha256=hashlib.sha256(GDP.read_bytes()).hexdigest(),
               rows=len(df),missing_observations=missing,period=[1990,2023],
               uncertainty='HAC Newey-West lag 3, Bartlett weights, finite-sample n/(n-p), asymptotic normal 95%; does not correct common trends or measurement bias',
               old_reconstruction_max_relative_error=diag,results=results,
               limitations=['No cointegration or causal instrument', 'GDP is not Campergue Money or a full living-standard index',
                            'Primary energy substitution convention, not final energy/exergy',
                            'Country domestic production boundaries, not consumption footprint',
                            'Population common denominator can induce association; E2 is within-country descriptive',
                            'Six purposively selected economies, not a representative cross-country sample',
                            '2020 shock retained; short split samples and no multiple-testing correction'])
    return out, df

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    result, df = compute()
    path = OUT/'results.json'
    if args.check or path.exists():
        old = json.loads(path.read_text())
        def compare(a,b):
            if isinstance(a,dict):
                assert a.keys()==b.keys()
                for k in a: compare(a[k],b[k])
            elif isinstance(a,list):
                assert len(a)==len(b)
                for x,y in zip(a,b): compare(x,y)
            elif isinstance(a,float): assert np.isclose(a,b,rtol=1e-9,atol=1e-9), (a,b)
            else: assert a==b,(a,b)
        compare(result,old)
        pd.testing.assert_frame_equal(df.reset_index(drop=True),pd.read_csv(OUT/'analysis_panel.csv'),check_exact=False,rtol=1e-10)
    else:
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        df.to_csv(OUT/'analysis_panel.csv',index=False)
    print('PASS: TEST-E1/E2/E3 execution or numerical comparison; WARNING: associations are noncausal; strict constant-K restriction assessed separately')
    for r in result['results']:
        if r['model']=='loglog': print(r['country'],r['N'],r['coefficients'][1],r['R2'],r['ci95'][1])

if __name__ == '__main__': main()
