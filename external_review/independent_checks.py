"""Reviewer calculations, independent of the internal compute functions."""
import copy,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'external_review'
sys.path.insert(0,str(ROOT))

def fit(X,y,years,lag):
    X=np.asarray(X,float);y=np.asarray(y,float);years=np.asarray(years)
    design=np.column_stack([np.ones(len(y)),X])
    # Different implementation: pseudo-inverse and all ordered calendar pairs.
    beta=np.linalg.pinv(design)@y;err=y-design@beta;n,k=design.shape
    weight=np.maximum(0,1-np.abs(years[:,None]-years[None,:])/(lag+1))
    # Avoid normal equations: their condition number is squared, especially for TWh levels.
    inverse_design=np.linalg.pinv(design)
    variance=inverse_design@(err[:,None]*weight*err[None,:])@inverse_design.T*n/(n-k)
    se=np.sqrt(np.diag(variance))
    return dict(coefficients=beta.tolist(),se=se.tolist(),R2=float(1-np.dot(err,err)/np.sum((y-y.mean())**2)),N=n)

def run():
    d=pd.read_csv(ROOT/'analysis/empirical/independent_energy/analysis_panel.csv')
    old=json.loads((ROOT/'analysis/empirical/independent_energy/results.json').read_text())
    rows=[]
    for r in old['results']:
        s=d[d['Country Code']==r['country']].sort_values('year')
        e=s.primary_energy_consumption.to_numpy();g=s.gdp_real.to_numpy()/1e9;years=s.year.to_numpy()
        if r['model']=='level':x,y=e,g
        elif r['model']=='loglog':x,y=np.log(e),np.log(g)
        elif r['model']=='dlog':x,y=np.diff(np.log(e)),np.diff(np.log(g));years=years[1:]
        elif r['model']=='per_capita_loglog':x,y=np.log(e*1e9/s.population),np.log(s.gdp_ppp_real/s.population)
        else:
            x0=np.log(e);post=(years>=2007).astype(float)
            x,y=np.column_stack([x0,post,x0*post]),np.log(g)
        actual=fit(x,y,years,3)
        dif=max(np.max(np.abs(np.array(actual['coefficients'])-r['coefficients'])),
                np.max(np.abs(np.array(actual['se'])-r['se_HAC'])),abs(actual['R2']-r['R2']))
        assert dif<1e-8 and actual['N']==r['N'],(r['country'],r['model'],dif)
        rows.append(dict(country=r['country'],model=r['model'],max_absolute_difference=float(dif),result='RESULT_REPRODUCED'))
    micro=pd.read_csv(ROOT/'analysis/empirical/micro_electricity/panel.csv')
    micro=micro[~micro.year.isin([2001,2002,2013])]
    m=fit(micro.dlog_fuel_cost_proxy_cents_kwh,micro.dlog_retail_cents_kwh,micro.year,2)
    expected=json.loads((ROOT/'analysis/empirical/micro_electricity/results.json').read_text())['regression']
    assert abs(m['coefficients'][1]-expected['coefficient'])<1e-10
    assert abs(m['se'][1]-expected['se_HAC2'])<1e-10
    assert abs(m['R2']-expected['R2'])<1e-10
    formal=[]
    def case(id,premise,values,conclusion,pages):formal.append(dict(id=id,premise=premise,values=values,conclusion=conclusion,source_pages=pages,kind='FORMAL_COUNTEREXAMPLE_OR_IDENTITY_NOT_EMPIRICAL'))
    case('ERC-01','Produit fini : n=100,u=1,Δn=10,Δu=0.1',dict(exact=110*1.1-100,linear=100*.1+10,cross=10*.1),'ΔnΔu doit être conservé pour variation finie; pas une faute du différentiel exact du corpus.',[15,16])
    case('ERC-02','cp:2→3, ω=2 fixe',dict(delta_state=(3-2)*2**2/2,omega_only_integral=0),'La relation différentielle proposée et la primitive à cp variable ne coïncident pas sans terme supplémentaire.',[207])
    case('ERC-03','Utility positive4,2; recodage carré strictement croissant',dict(ratio_yield=1-2/4,recoded=1-4/16),'Ordinal seul insuffisant aux ratios; une échelle compatible est une hypothèse nécessaire.',[109,386])
    case('ERC-04','dA=ε,dB=2ε; chacun→0',dict(ratio=2,claimed_ratio=1),'Les limites nulles ne fixent pas le ratio à1; égalité peut être posée séparément, non dérivée ainsi.',[249,250,252])
    case('ERC-05','F=2 constant, Δt=3',dict(impulse=2*3,claimed_change=0),'F constant non nul implique variation6 dans la relation imprimée; F net nul est une autre hypothèse.',[467,470])
    case('ERC-06','F·p=r·U avec r=2,U=3,p=4',dict(correct_F=2*3/4,printed_F=4*3/2),'L’expression imprimée page303 inverse r et p. Correction algébrique locale possible, pas validation de Core Law.',[301,303])
    case('ERC-07','cp=2, deux vitesses1 et3; comparaison2 et2',dict(mean_speed=2,mean_square_first=5,square_mean=4,mean_square_second=4),'À vitesse moyenne identique, variance différente : le passage à une vitesse moyenne perd un terme. Le test K pondéré ne suffit pas à auditer ce passage.',[559])
    case('ERC-08','M=n·u n=u=1, ca=2,ϖ=1,C=0, même référent hypothétique',dict(balance_M=1,kinetic_M=-1),'Incompatible sous un référent unique positif. Les conventions de flux/énergie relative peuvent lever le conflit seulement par un dictionnaire explicite.',[15,207,455,467])
    case('ERC-09','Seule borne η≥1−U2/U1, ratio=0.5',dict(eta=1.5,lower_bound=.5),'Cette borne seule n’implique pas η≤1; vérifier conservation/signes ou ajouter restriction, ne pas rejeter le cycle entier.',[385,386])
    case('ERC-10','Deux stades production: intermédiaire100, final150, pas autres intrants',dict(gross_transactions=100+150,value_added=100+(150-100)),'Transactions brutes≠PIB. La lecture par valeurs ajoutées peut éviter le double compte, mais exige correspondance Money/V explicite.',[205,420,529,559])
    from analysis.verify_synthesis import validate,load
    semantic=load('results.json');semantic[0]['statement']='M=n.u démontre une neutralité causale générale sans conditions.'
    accepted_semantic=validate(results=semantic)['status']=='PASS'
    provenance=load('results.json');provenance[0]['sources']=['README.md']
    accepted_bad_source=validate(results=provenance)['status']=='PASS'
    assert accepted_semantic and accepted_bad_source
    out=dict(energy=rows,micro=dict(result='RESULT_REPRODUCED',actual=m,N=20),formal=formal,
      validator_challenges=dict(incorrect_semantic_statement_accepted=accepted_semantic,irrelevant_existing_source_accepted=accepted_bad_source,files_modified=False),
      no_scientific_global_verdict=True)
    (OUT/'independent_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(energy_models=len(rows),micro_models=1,formal_cases=len(formal),semantic_mutants_accepted=2),ensure_ascii=False))
if __name__=='__main__':run()
