"""One descriptive regression plus fixed-basket arithmetic; never infer Money.
Offline computation after design31 and its explicitly documented amendment.
Existing numerical benchmarks are compared, never silently replaced.
"""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/empirical/micro_electricity'
SOURCE=OUT/'source'
YEARS=list(range(2001,2024))
ALLOWED={'FORMALLY_CONSISTENT','EMPIRICALLY_COMPATIBLE','EMPIRICALLY_QUALIFIED','EMPIRICALLY_CONTRADICTED','NON_DISCRIMINATING','NOT_IDENTIFIABLE'}

class Rows(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=[];self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        if tag in ['td','th']:self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ['td','th'] and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
        if tag=='tr' and self.row:self.rows.append(self.row)

def mer(table,code,name,unit):
    raw=pd.read_csv(SOURCE/(table+'.csv'),dtype={'YYYYMM':str})
    d=raw[(raw.MSN==code)&raw.YYYYMM.str.endswith('13')].copy()
    assert len(d)>0,(table,code)
    assert set(d.Unit)=={unit},(code,set(d.Unit))
    d['year']=d.YYYYMM.str[:4].astype(int)
    d=d[d.year.isin(YEARS)]
    d[name]=pd.to_numeric(d.Value,errors='coerce')
    assert not d.year.duplicated().any(),code
    meta=dict(column=name,file=table+'.csv',series=code,unit=unit,description=d.Description.iloc[0],
              annual_selection='YYYYMM ends in13; official annual observations, not unweighted monthly prices',
              missing_years=[y for y in YEARS if y not in set(d.dropna(subset=[name]).year)])
    return d.set_index('year')[name],meta

def cpi():
    rows=[]
    for f in sorted(SOURCE.glob('bls_cpi_*.json')):
        j=json.loads(f.read_text());assert j['status']=='REQUEST_SUCCEEDED'
        s=j['Results']['series'];assert len(s)==1 and s[0]['seriesID']=='CUUR0000SA0'
        for r in s[0]['data']:
            if re.fullmatch(r'M(0[1-9]|1[012])',r['period']):rows.append((int(r['year']),r['period'],float(r['value'])))
    d=pd.DataFrame(rows,columns=['year','month','cpi'])
    assert not d.duplicated(['year','month']).any()
    assert set(d.year)==set(YEARS)
    assert (d.groupby('year').size()==12).all()
    return d.groupby('year').cpi.mean()

def reliability():
    reader=Rows();reader.feed((SOURCE/'reliability.html').read_text())
    rows=[]
    for r in reader.rows:
        if len(r)==16 and re.fullmatch(r'20\d\d',r[0]) and 2014<=int(r[0])<=2023:
            rows.append(dict(year=int(r[0]),saidi_ieee_all=float(r[1]),saidi_ieee_without_major=float(r[4])))
    d=pd.DataFrame(rows).sort_values('year').reset_index(drop=True)
    assert d.year.tolist()==list(range(2014,2024)),d
    return d

def hac_fit(x,y,years):
    X=np.column_stack([np.ones(len(x)),np.asarray(x)]);y=np.asarray(y);years=np.asarray(years)
    b=np.linalg.lstsq(X,y,rcond=None)[0];u=y-X@b;z=X*u[:,None];meat=z.T@z
    for lag in [1,2]:
        for i in range(len(years)):
            for j in range(i):
                if years[i]-years[j]==lag:
                    a=np.outer(z[i],z[j]);meat+=(1-lag/3)*(a+a.T)
    n,p=X.shape;bread=np.linalg.inv(X.T@X);cov=bread@meat@bread*n/(n-p)
    se=np.sqrt(np.maximum(np.diag(cov),0))
    return dict(N=n,years=years.tolist(),coefficient=float(b[1]),intercept=float(b[0]),
                se_HAC2=float(se[1]),ci95=[float(b[1]-1.96*se[1]),float(b[1]+1.96*se[1])],
                R2=float(1-(u@u)/np.sum((y-y.mean())**2)),
                uncertainty='Calendar-lag Newey-West/Bartlett2, n/(n−2), asymptotic normal95%; no causal interpretation')

def compute():
    m=json.loads((SOURCE/'manifest.json').read_text())
    assert hashlib.sha256((ROOT/m['design_file']).read_bytes()).hexdigest()==m['design_sha256']
    for f in m['files']:assert hashlib.sha256((ROOT/f['file']).read_bytes()).hexdigest()==f['sha256']
    columns=[];metadata=[]
    for args in [
        ('T09.08','ESRCUUS','retail_cents_kwh','Cents per Kilowatthour,  Including Taxes'),
        ('T09.09','NGERDUS','gas_usd_mmbtu','Dollars per Million Btu, Including Taxes'),
        ('TA6','NGETKUS','gas_heat_btu_kwh','Btu per Kilowatthour'),
        ('T07.02B','NGEGPUS','gas_generation_million_kwh','Million Kilowatthours'),
        ('T07.02B','ELEGPUS','generation_million_kwh','Million Kilowatthours'),
        ('T07.06','ESRCPUS','residential_sales_million_kwh','Million Kilowatthours')]:
        col,meta=mer(*args);columns.append(col);metadata.append(meta)
    d=pd.concat(columns,axis=1).reindex(YEARS);d.index.name='year';d['cpi']=cpi()
    missing={c:[int(y) for y in d.index[d[c].isna()]] for c in d.columns}
    assert not any(missing.values()),missing
    assert (d>0).all().all()
    d['fuel_cost_proxy_cents_kwh']=d.gas_usd_mmbtu*d.gas_heat_btu_kwh/10000
    d['heat_efficiency_proxy']=3412/d.gas_heat_btu_kwh
    d['retail_real2023_cents_kwh']=d.retail_cents_kwh*d.loc[2023,'cpi']/d.cpi
    d['nominal_budget100_kwh']=10000/d.retail_cents_kwh
    d['real2023_budget100_kwh']=10000/d.retail_real2023_cents_kwh
    # This is not a measured profit or markup.
    d['retail_minus_fuel_proxy_NOT_MARGIN']=d.retail_cents_kwh-d.fuel_cost_proxy_cents_kwh
    for col in ['retail_cents_kwh','fuel_cost_proxy_cents_kwh','gas_heat_btu_kwh','gas_usd_mmbtu']:
        d['dlog_'+col]=np.log(d[col]).diff()
    d['price_pct_change']=d.retail_cents_kwh.pct_change()*100
    d['cost_proxy_pct_change']=d.fuel_cost_proxy_cents_kwh.pct_change()*100
    d['nominal_gain_fixed1000kwh_usd']=-10*d.retail_cents_kwh.diff()
    d['real_gain_fixed1000kwh_usd2023']=-10*d.retail_real2023_cents_kwh.diff()
    d['screening_branch']='NO_COST_PROXY_DECLINE'
    d.loc[2001,'screening_branch']='NO_PREVIOUS_YEAR'
    down=d.cost_proxy_pct_change<0
    d.loc[down & (d.price_pct_change < -1),'screening_branch']='A_PROXY_COST_DOWN_PRICE_DOWN'
    d.loc[down & (d.price_pct_change.abs()<=1),'screening_branch']='B_PROXY_COST_DOWN_PRICE_NEAR_STABLE'
    d.loc[down & (d.price_pct_change > 1),'screening_branch']='E_PROXY_COST_DOWN_PRICE_UP'
    rdata=d.loc[~d.index.isin([2001,2002,2013])]
    assert len(rdata)>=15
    reg=hac_fit(rdata.dlog_fuel_cost_proxy_cents_kwh,rdata.dlog_retail_cents_kwh,rdata.index)
    reg.update(formula='Δlog(residential average price) ~ 1 + Δlog(gas fuel cost weak proxy)',
               excluded_changes=[2002,2013],result_status='EMPIRICALLY_QUALIFIED',specificity_status='NON_DISCRIMINATING',
               causal_identified=False,structural_pass_through_identified=False)
    quality=reliability()
    selected=['retail_cents_kwh','retail_real2023_cents_kwh','gas_usd_mmbtu','gas_heat_btu_kwh','heat_efficiency_proxy',
              'fuel_cost_proxy_cents_kwh','gas_generation_million_kwh','generation_million_kwh','residential_sales_million_kwh','nominal_budget100_kwh','real2023_budget100_kwh']
    trends={c:dict(first=float(d.loc[2001,c]),last=float(d.loc[2023,c]),change_pct=float(100*(d.loc[2023,c]/d.loc[2001,c]-1))) for c in selected}
    outcomes=[
        dict(id='PRED-MICRO-01',result_status='FORMALLY_CONSISTENT',specificity_status='NON_DISCRIMINATING',
             reason='At fixed gas price, lower heat rate lowers the constructed fuel-cost proxy by definition; heat-rate trends are not a direct test of Economic Work.'),
        dict(id='PRED-MICRO-02',result_status='NOT_IDENTIFIABLE',specificity_status='NON_DISCRIMINATING',
             reason='No total cost, unit profit or matched retail quality observed; sector regression does not test conditional one-for-one pass-through.'),
        dict(id='PRED-MICRO-03',result_status='NOT_IDENTIFIABLE',specificity_status='NON_DISCRIMINATING',
             reason='Near-stable price and declining fuel proxy can be screened; total cost and profit retention cannot be determined.'),
        dict(id='PRED-MICRO-04',result_status='FORMALLY_CONSISTENT',specificity_status='NON_DISCRIMINATING',
             reason='Fixed-budget/fixed-quantity arithmetic computed in nominal and CPI-deflated terms; actual household gain, quality-adjusted surplus and Money unobserved.'),
        dict(id='PRED-MICRO-05',result_status='NOT_IDENTIFIABLE',specificity_status='NON_DISCRIMINATING',
             reason='T, cp, task-speed and Utility not independently measured; physical efficiency cannot supply the missing quadratic test.')]
    result=dict(case='US electricity, gas generation cost context and residential service',period=[2001,2023],N_levels=23,N_changes=22,
                metadata=metadata,missing=missing,regression=reg,trends=trends,predictions=outcomes,
                branch_years={b:[int(y) for y in d.index[d.screening_branch==b]] for b in sorted(d.screening_branch.unique())},
                nominal_gain_years=[int(y) for y in d.index[d.nominal_gain_fixed1000kwh_usd>0]],
                real_gain_years=[int(y) for y in d.index[d.real_gain_fixed1000kwh_usd2023>0]],
                quality=dict(N=10,period=[2014,2023],first=quality.iloc[0].to_dict(),last=quality.iloc[-1].to_dict(),
                             result_status='EMPIRICALLY_QUALIFIED',utility_status='UTILITY_NOT_IDENTIFIABLE',
                             note='IEEE method separated with/without major events; reporting population and weather not held constant'),
                money_identification='NOT_IDENTIFIED',chain_result_status='NOT_IDENTIFIABLE',specificity_status='NON_DISCRIMINATING',
                margin_identification='NOT_IDENTIFIABLE',actual_consumer_surplus='NOT_IDENTIFIABLE',
                total_generation_energy_NOT_COMPUTED=True,global_theory_verdict=None)
    return result,d.reset_index(),quality

def equal(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:equal(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):equal(x,y)
    elif isinstance(a,float):assert np.isclose(a,b,rtol=1e-10,atol=1e-10),(a,b)
    else:assert a==b,(a,b)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result,panel,quality=compute();path=OUT/'results.json'
    if args.check or path.exists():
        equal(result,json.loads(path.read_text()))
        for name,frame in [('panel.csv',panel),('quality.csv',quality)]:
            pd.testing.assert_frame_equal(frame,pd.read_csv(OUT/name),check_exact=False,rtol=1e-10,atol=1e-10)
    else:
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        panel.to_csv(OUT/'panel.csv',index=False);quality.to_csv(OUT/'quality.csv',index=False)
    print('PASS: micro numerical computation/comparison; WARNING: full chain and Money NOT_IDENTIFIED')
    print(json.dumps(result['regression'],indent=2));print(json.dumps(result['trends'],indent=2));print(result['branch_years'])
if __name__=='__main__':main()
