"""Small synthetic counterexamples, not empirical confirmation of Campergue."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions/second_pass_formal_results.json'
def compute():
    # Constant coefficient primitive/increment vs variable coefficient omitted term.
    cp=F(2);w0=F(3);w1=F(4)
    state0=cp*w0*w0/2;state1=cp*w1*w1/2
    assert state0==9 and state1-state0==7
    # Three heterogeneous products: extend archived two-product experiment with C.
    p0=[F(10),F(20),F(5)];p1=[F(8),F(24),F(4)]
    q0=[F(10),F(3),F(8)];q1=[F(20),F(2),F(1)]
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    base=dot(p0,q0);weights=[p*q/base for p,q in zip(p0,q0)]
    price_index=dot(p1,q0)/base;normalized=dot(weights,[a/b for a,b in zip(p1,p0)])
    assert price_index==normalized==F(23,25)
    T=[F(2),F(5),F(1)];K=[F(1,2),F(2),F(4)];M=[a*b for a,b in zip(T,K)]
    k0=dot(M,q0)/dot(T,q0);k1=dot(M,q1)/dot(T,q1)
    assert k0==F(72,43) and k1==F(44,51)
    # Potential positive example exact d(x*y)=y dx+x dy, negative example y dx.
    # (0,0)->(1,0)->(1,1) and (0,0)->(0,1)->(1,1).
    exact_paths=[F(1),F(1)];nonexact_paths=[F(0),F(1)]
    assert exact_paths[0]==exact_paths[1] and nonexact_paths[0]!=nonexact_paths[1]
    # Ref 26-17 (p554) coefficients versus substitution of e=cp*w, a=-ca*v.
    ca=F(3);e=F(4);a=F(9)
    metric_squared=e*e/(cp*cp)+a*a/(ca*ca)
    printed_squared=e*e/cp+a*a/ca
    assert metric_squared==13 and printed_squared==35
    # Currency rescaling changes an unnormalised slope, but not dimensionless axes.
    slope=F(2,4);slope_cents=F(200,4)
    normalized_slope=(F(2)/2)/(F(4)/4)
    normalized_cents=(F(200)/200)/(F(4)/4)
    assert normalized_slope==normalized_cents
    # Finite product changes: cross term is not optional.
    n,u,dn,du=F(100),F(2),F(10),F(1,10)
    delta=(n+dn)*(u+du)-n*u;linear=n*du+u*dn
    assert delta==31 and linear==30
    # Same speed increase can have different process-loss laws; explicit toy, not data.
    return dict(synthetic=True,source_pages=[207,208,413,414,415,427,548,553,554,559],
        T=dict(state_initial=float(state0),state_final=float(state1),increment=float(state1-state0),
               fixed_speed_increment=0,variable_cp_missing_term='0.5*omega**2*dcp',status='LOCALLY_CONSISTENT'),
        three_products=dict(prices_initial=[float(x) for x in p0],prices_final=[float(x) for x in p1],
            quantities_initial=[float(x) for x in q0],quantities_final=[float(x) for x in q1],
            base_expenditure=float(base),fixed_basket_expenditure=float(dot(p1,q0)),
            direct_index=float(price_index),normalized_weighted_index=float(normalized),
            equal_weight_index=float(sum(a/b for a,b in zip(p1,p0))/3),
            K_local=[float(x) for x in K],T_local=[float(x) for x in T],
            K_aggregate=[float(k0),float(k1)],Utility_summed=False),
        potential=dict(exact_paths=[float(x) for x in exact_paths],nonexact_paths=[float(x) for x in nonexact_paths],
            note='No losses label alone does not impose equality of mixed partials; toy is not a fitted corpus potential.'),
        metric=dict(substituted_squared=float(metric_squared),printed_squared=float(printed_squared),
            status='INCONSISTENT_IF_SAME_VARIABLES_NO_HIDDEN_NORMALIZATION',
            unnormalised_slopes=[float(slope),float(slope_cents)],normalised_slopes=[float(normalized_slope),float(normalized_cents)]),
        money=dict(finite_change=float(delta),first_order=float(linear),cross_term=float(dn*du)),
        limits=['Synthetic examples only','Utility explicitly nonadditive in manuscript p108',
                'No causal identification','No new empirical data','Existing two-product and energy checks remain separate'],
        global_theory_verdict=None)
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();r=compute()
    if a.check or OUT.exists():assert r==json.loads(OUT.read_text())
    else:OUT.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('PASS: five second-pass formal diagnostics; synthetic, not empirical validation')
if __name__=='__main__':main()
