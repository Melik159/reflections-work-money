"""Synthetic diagnostics of measurement, not new empirical regressions."""
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions/operationalization/formal_results.json'
def compute():
    def agg(k,t,q):return sum(a*b*c for a,b,c in zip(k,t,q))/sum(a*b for a,b in zip(t,q))
    composition=[]
    for k,t,q0,q1 in [([.5,2],[2,5],[10,3],[20,2]),([.5,2,4],[2,5,1],[10,3,8],[20,2,1])]:
        a=agg(k,t,q0);rep=agg(k,t,[100*x for x in q0]);b=agg(k,t,q1)
        assert math.isclose(a,rep) and not math.isclose(a,b)
        composition.append(dict(products=len(k),K_local=k,T_local=t,quantities_initial=q0,quantities_changed=q1,K_fixed=a,K_replicated=rep,K_changed=b))
    alpha=math.pi/8;eta=(1-math.tan(alpha))**2
    derivative=-2*(1-math.tan(alpha))/(math.cos(alpha)**2)
    assert math.isclose(eta,(2-math.sqrt(2))**2) and not math.isclose(derivative,0)
    # Ordinally equivalent positive scales do not preserve ratios.
    u1,u2=4,2;yield1=1-u2/u1;yield2=1-u2**2/u1**2
    assert u1>u2 and u1*u1>u2*u2 and yield1!=yield2
    # Constructed T: zero residual is true by construction, explicitly barred as law evidence.
    cp=2;omega=[1,2,3];T=[.5*cp*w*w for w in omega]
    residual=[t-.5*cp*w*w for t,w in zip(T,omega)]
    assert residual==[0,0,0]
    return dict(synthetic=True,empirical_validation=False,composition=composition,
        optimum=dict(source_pages=[388,389,390],alpha=alpha,value=eta,derivative=derivative,status='CONDITIONAL_VALUE_REPRODUCED; CONSTRAINED_OPTIMUM_NOT_ESTABLISHED_BY_THIS_DIAGNOSTIC'),
        utility=dict(initial=[u1,u2],transformed=[u1*u1,u2*u2],implied_yields=[yield1,yield2],status='ORDINAL_ORDER_DOES_NOT_IDENTIFY_CARDINAL_RATIO'),
        circularity=dict(T=T,omega=omega,residuals=residual,status='CIRCULAR',admissible_independent_law_test=False),
        limits=['K aggregation assumes additive comparable T and M; no Utility summed','Synthetic scaling test not a measurement of economic T','Nonzero free derivative does not exclude constrained optimum','No empirical regression or new dataset'])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();r=compute()
    if args.check or OUT.exists():assert json.loads(OUT.read_text())==r
    else:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('PASS: metrology synthetic diagnostics; no empirical validation')
if __name__=='__main__':main()
