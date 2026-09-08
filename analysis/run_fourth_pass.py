"""Prospectively specified formal extensions. --check never rewrites results."""
import argparse,hashlib,itertools,json
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions/experiments'
def check_protocols():
    m=json.loads((OUT/'fourth_pass_protocol_manifest.json').read_text())
    for eid,h in m['protocol_sha256'].items():
        assert hashlib.sha256((OUT/eid/'protocol.md').read_bytes()).hexdigest()==h,'protocol changed without amendment'
    return m
def utility():
    base=[F(1),F(2),F(4)]; transforms={'identity':lambda u:u,'ratio':lambda u:3*u,'affine':lambda u:3*u+5,'nonlinear':lambda u:u*u}
    results={}
    for name,f in transforms.items():
        u=list(map(f,base));r=F(6)
        results[name]=dict(values=u,order=u[0]<u[1]<u[2],equality=f(base[1])==f(base[1]),
            difference=u[2]-u[1],ratio=u[1]/u[2],yield_value=1-u[1]/u[2],
            ratio_of_differences=(u[1]-u[0])/(u[2]-u[1]),level_product=r*u[2],
            compensating_r_at_2=r*base[1]/u[1],compensating_r_at_4=r*base[2]/u[2])
    assert all(x['order'] and x['equality'] for x in results.values())
    assert results['ratio']['ratio']==results['identity']['ratio']!=results['affine']['ratio']
    assert results['affine']['ratio_of_differences']==results['identity']['ratio_of_differences']!=results['nonlinear']['ratio_of_differences']
    assert results['ratio']['compensating_r_at_2']==results['ratio']['compensating_r_at_4']
    assert results['affine']['compensating_r_at_2']!=results['affine']['compensating_r_at_4']
    # r transforms inversely under affine changes when only differences enter.
    assert (F(6)/3)*((3*base[2]+5)-(3*base[1]+5))==F(6)*(base[2]-base[1])
    return dict(status=['FORMALLY_SUPPORTED','FORMALLY_QUALIFIED','BLOCKED_BY_MEASUREMENT'],
        findings=['Order/equality/sign of change survive common strictly increasing recoding',
                  'Numerical differences need interval structure; their ratios are affine invariant',
                  'Utility ratios need a common ratio scale, not merely an ordinal or interval scale',
                  'Core Law level product covaries under U→aU,r→r/a; arbitrary shifts cannot retain one r across states',
                  'r ΔU covaries under affine recoding with r→r/a; an absolute origin is not needed for this difference-only expression'],
        transformed=results,independent_Utility_measured=False,Money_observed=False)
def aggregation():
    def kbar(ks,ts,qs):return sum(k*t*q for k,t,q in zip(ks,ts,qs))/sum(t*q for t,q in zip(ts,qs))
    k=list(map(F,[1,2,3]));t=list(map(F,[1,2,1]));cases=[]
    for size in [2,3]:
        records=[]
        for rawq in itertools.product([1,2,3],repeat=size):
            q=list(map(F,rawq));kb=kbar(k[:size],t[:size],q);rep=kbar(k[:size],t[:size],[7*x for x in q]);hom=kbar([F(2)]*size,t[:size],q)
            assert kb==rep and hom==2
            records.append(dict(q=q,K=kb,replicated_K=rep,homogeneous_K=hom))
        cases.append(dict(products=size,cases=records,range=[min(r['K'] for r in records),max(r['K'] for r in records)]))
    q0=list(map(F,[1,1,1]));q1=list(map(F,[2,1,2]));a=kbar(k,t,q0);b=kbar(k,t,q1);assert a==b
    weights=lambda q:[ti*qi/sum(x*y for x,y in zip(t,q)) for ti,qi in zip(t,q)]
    delta=sum((v-u)*ki for u,v,ki in zip(weights(q0),weights(q1),k));assert delta==0
    scales=list(map(F,[2,3,5]));tn=[s*x for s,x in zip(scales,t)];kn=[ki/s for ki,s in zip(k,scales)]
    raw=kbar(kn,tn,q0);restored=kbar([ki*s for ki,s in zip(kn,scales)],[x/s for x,s in zip(tn,scales)],q0)
    assert restored==a and raw!=a
    common_scale=F(7);common=kbar([ki/common_scale for ki in k],[common_scale*x for x in t],q0);assert common*common_scale==a
    return dict(status=['FORMALLY_SUPPORTED','FORMALLY_QUALIFIED'],cases=cases,
        compensation=dict(q0=q0,q1=q1,weights0=weights(q0),weights1=weights(q1),K0=a,K1=b,weighted_delta=delta),
        normalization=dict(scales=scales,raw_incommensurate_K=raw,restored_common_unit_K=restored,common_unit_K=common,common_scale=common_scale),
        assumptions=['Ti strictly positive','Mi=KiTi and additive within same boundary','No double counting','Common units before aggregation','Ki fixed for composition theorem','No Utility sum'],
        stability_condition='Σ_i (w_i_new−w_i_old) Ki = 0; w_i=qiTi/Σj qjTj',
        arbitrary_composition_condition='All active Ki equal is necessary and sufficient for invariance over all positive compositions, with fixed positive Ti.',
        note='For varying Ki use ΔKbar=Σ_i w_i_new ΔKi + Σ_i Δwi Ki_old; neither fixed composition nor a large count suffices alone.',
        economic_K_measured=False)
def work():
    cp=F(2);omega=list(map(F,[1,3,2,1]));state=[cp*w*w/2 for w in omega];inc=[b-a for a,b in zip(state,state[1:])];reserve=[F(100)+state[0]-x for x in state]
    positive=sum(max(x,0) for x in inc);signed=sum(inc)
    assert signed==state[-1]-state[0]==0 and positive!=signed
    assert all(e+r==state[0]+100 for e,r in zip(state,reserve))
    variable_cp_delta=(F(3)-1)*F(2)**2/2;omega_only=F(0);assert variable_cp_delta!=omega_only
    scale=F(3);assert all((cp/scale**2)*(scale*w)**2/2==e for w,e in zip(omega,state))
    return dict(status=['FORMALLY_SUPPORTED','FORMALLY_QUALIFIED','NOT_IDENTIFIABLE'],
        omega=omega,state_A=state,transfer_C=inc,reserve_B=reserve,signed_accumulation=signed,positive_accumulation=positive,
        variable_cp=dict(delta_state=variable_cp_delta,omega_only_integral=omega_only,missing_term='0.5 omega² dcp'),
        models=[dict(id='MODEL-A',interpretation='state E',compatible_pages=[207],qualified_pages=[203,471],condition='T on p471 must mean ΔE; work zero at constant speed means transfer, not state'),
                dict(id='MODEL-B',interpretation='potential reserve R',compatible_pages=[471,472],qualified_pages=[207],condition='R+E fixed in isolated balance; R is not the same 0.5 cp omega²; accumulated positive work is another quantity'),
                dict(id='MODEL-C',interpretation='interval transfer T[a,b]',compatible_pages=[203,471],qualified_pages=[207],condition='T[a,b]=E(b)−E(a); p207 primitive requires chosen reference. Intervals telescope; same units, different object')],
        units='[T]=[cp][labour]²/[time]²; dT and reserve share this formal unit, not calibrated joules',
        independent_T_measured=False,diagnostic='REQUIRES_INDEPENDENT_T',source_rewritten=False)
def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x))
def compute():return {'EXP-02':utility(),'EXP-03':aggregation(),'EXP-09':work()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();m=check_protocols()
    r=json.loads(json.dumps(compute(),default=encode))
    for eid,result in r.items():
        p=OUT/eid/'results.json'
        if args.check or p.exists():assert json.loads(p.read_text())==result,eid+' result mismatch'
        else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    log=OUT/'fourth_pass_execution.json'
    if not log.exists():
        assert not args.check
        log.write_text(json.dumps(dict(executed_at=datetime.now(timezone.utc).isoformat(),protocol_manifest_sha256=hashlib.sha256((OUT/'fourth_pass_protocol_manifest.json').read_bytes()).hexdigest(),executed=list(r),new_empirical_experiments=0,protocol_amendments=[],Money_observed=False),indent=2)+'\n')
    print('PASS: three fourth-pass formal extensions; protocol hashes intact; no new empirical experiment')
if __name__=='__main__':main()
