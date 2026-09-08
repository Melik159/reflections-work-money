"""Executed arithmetic and data-identifiability checks, not theory validation."""
import hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/empirical/productive'

def compute():
    path=ROOT/'articles/campergue_energy_gdp_code/output_macro/merged_energy_gdp.csv'
    df=pd.read_csv(path);world=df[df['Country Code']=='WLD']
    def fit(x,y):
        xy=pd.DataFrame({'x':x,'y':y}).dropna();X=np.column_stack([np.ones(len(xy)),xy.x]);b=np.linalg.lstsq(X,xy.y,rcond=None)[0]
        return dict(n=len(xy),beta=float(b[1]),r2=float(1-np.sum((xy.y-X@b)**2)/np.sum((xy.y-xy.y.mean())**2)))
    q=(8/6)**2-1;assert math.isclose(q,7/9)
    t0,t1,c,l,ch=8,6,2,1,20
    w0,w1=l/t0,l/t1;T0,T1=c*w0*w0/2,c*w1*w1/2;e0,e1=c*w0,c*w1
    prices=[.5*e*ch*l/T for e,T in [(e0,T0),(e1,T1)]]
    assert np.allclose(prices,[160,120])
    eta=(2-math.sqrt(2))**2
    assert math.isclose(eta,.3431457505076198)
    # The square expression on p389 is not maximized at pi/8 on [0,pi/4].
    square_at_zero=(1-math.tan(0))**2
    assert square_at_zero>eta
    # A lower bound alone does not force zero yield at equal utilities.
    candidate=.2;assert candidate>=1-1 and 0<=candidate<=1
    errors=np.abs(df.energy-df.gdp_ppp_real/df.gdp_per_energy)/df.energy
    forms=[dict(id='PCALC-01',kind='CONDITIONAL_ARITHMETIC',result=q,passed=True,status=['ARITHMETICALLY_REPRODUCED','FORMALLY_DERIVED','ASSUMPTION_DEPENDENT','NOT_EMPIRICALLY_TESTED'],conditions='Same task, constant cP, zero reference, T proportional to speed squared.'),
      dict(id='PCALC-02',kind='COUPLED_VARIABLE_SUBSTITUTION',prices=prices,work_ratio=T1/T0,speed_ratio=w1/w0,passed=True,conclusion='With cP fixed e changes: p∝1/sqrt(T), not 1/T with all other variables silently fixed.'),
      dict(id='PCALC-03',kind='CONDITIONAL_YIELD_ARITHMETIC',eta=eta,square_expression_at_zero=square_at_zero,passed=True,conclusion='Value reproduced. Global maximum of this square expression not established by substitution; reconcile table392 and domain restrictions.'),
      dict(id='PCALC-04',kind='LOGICAL_NONIMPLICATION',utility_ratio=1,candidate_yield=candidate,passed=True,conclusion='Lower bound eta>=0 does not by itself imply eta=0. Does not refute a separately imposed zero-yield condition.'),
      dict(id='PCALC-05',kind='ILLUSTRATIVE_COST_ARITHMETIC',initial_ratio=.6,final_ratio=5.1/5.5,passed=True,conclusion='Page461 illustration reproduced; explicitly not a historical estimate.')]
    tests=[
      dict(id='PTEST-01',hypotheses=['HYP-0001','HYP-0006'],mechanisms=['PM-01','PM-02','PM-03'],question='Is useful Work quadratic in speed at fixed task and complexity?',observable='Matched-process throughput and independently metered physical/useful energy',prediction='Conditional exponent2 for T, not necessarily total Q',alternative='Fixed overhead, variable efficiency or technology gives another energy-speed curve',required=['task identity','cycle duration','independent useful energy','complexity','efficiency'],available=list(df.columns),status='NOT_IDENTIFIABLE_WITH_CURRENT_DATA',refutation='Exponent incompatible with2 for independently operationalized T under fixed stated conditions',nonconclusion='Only annual GDP/derived energy or different technologies observed'),
      dict(id='PTEST-02',hypotheses=['HYP-0002'],mechanisms=['PM-03','PM-04','PM-05','PM-20'],question='Does a cost gain reach the transaction price under unchanged absolute profit?',observable='Matched product cost, price, margin amount and quality before/after productivity shock',prediction='Fixed absolute profit: price reduction equals cost reduction; fixed price: retained gain',alternative='Variable markups, demand and quality alter transmission',required=['unit cost','transaction price','profit per unit','quality','productivity shock'],available=list(df.columns),status='NOT_IDENTIFIABLE_WITH_CURRENT_DATA',refutation='A violation of the declared branch after observing its fixed variables, not failure of a universal transmission rule never posited here',nonconclusion='No product-level cost/price data; no independent shock'),
      dict(id='PTEST-03',hypotheses=['HYP-0001'],mechanisms=['PM-12','PM-15','PM-16'],question='Does repository energy/GDP evidence identify heat→Money transmission?',status='NOT_IDENTIFIABLE_WITH_CURRENT_DATA',diagnostic_executed=True,n=len(df),energy_reconstruction_max_relative_error=float(errors.max()),world_loglog=fit(world.log_energy,world.log_gdp),world_dlog=fit(world.dlog_energy,world.dlog_gdp),prediction='Conditional proportionality with fixed efficiencies and matched Q/M, not GDP automatically',alternative='Common trends, reconstructed energy, changing efficiencies and common causes',refutation='Requires independent Q,M and efficiencies; covariance alone does not test the law',nonconclusion='Shared construction of energy; GDP is not independently operationalized Money')]
    return dict(scope='Formal reproduction and identifiability only',input_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()},formal_checks=forms,empirical_protocols=tests)

def main():
    result=compute();OUT.mkdir(parents=True,exist_ok=True);(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 5 productive formal checks and data diagnostic; WARNING: 3 causal protocols NOT_IDENTIFIABLE_WITH_CURRENT_DATA')
if __name__=='__main__':main()
