"""Synthetic dimensional/aggregation diagnostic, NOT an empirical Campergue test."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/empirical/micro_electricity/two_product_results.json'

def compute():
    p0,p1,c0,c1,q0,q1,u0,u1=map(lambda x:list(map(F,x)),
        ([10,20],[8,24],[8,12],[6,14],[10,3],[20,2],[4,9],[5,8]))
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    base=dot(p0,q0); fixed=dot(p1,q0)
    weights=[p*q/base for p,q in zip(p0,q0)]
    weighted=dot(weights,[a/b for a,b in zip(p1,p0)])
    assert weighted==fixed/base
    pack_p=[p1[0],2*p1[1]];pack_q=[q0[0],q0[1]/2]
    assert dot(pack_p,pack_q)==fixed
    assert dot([100*p for p in p1],q0)/dot([100*p for p in p0],q0)==weighted
    t=[F(2),F(5)];k=[F(1,2),F(2)];m=[a*b for a,b in zip(t,k)]
    kt0=dot(m,q0)/dot(t,q0);kt1=dot(m,q1)/dot(t,q1)
    assert dot(m,[1000*q for q in q0])/dot(t,[1000*q for q in q0])==kt0
    return dict(synthetic=True,source_context=dict(document='Reflections_PierreCampergue.pdf',
        pages=[210,406,441,536,537,538,558,559],claims=['CPC-0111','CPC-0116','CPC-0126']),
        assumptions=['Prices/costs share currency per physical copy; fixed boundary, no double counts.',
                     'Synthetic utility points have NO calibrated inter-product equivalence.',
                     'Synthetic local M_i=K_i*T_i and additive totals are conditional assumptions, not measured corpus quantities.'],
        inputs={n:[float(v) for v in a] for n,a in zip(['p0','p1','c0','c1','q0','q1','U0','U1'],[p0,p1,c0,c1,q0,q1,u0,u1])},
        expenditure=dict(base=float(base),fixed_base_quantity=float(fixed),actual_final=float(dot(p1,q1)),
                         base_basket_saving=float(base-fixed),final_basket_saving=float(dot(p0,q1)-dot(p1,q1))),
        prices=dict(direct_Laspeyres=float(fixed/base),normalized_correct_weights=float(weighted),
                    normalized_equal_weights=float(sum(a/b for a,b in zip(p1,p0))/2),
                    final_quantity_weights=float(dot(p1,q1)/dot(p0,q1)),
                    currency_conversion_invariant=True,physical_pack_conversion_invariant=True),
        utility=dict(raw_fixed_basket=[float(dot(u0,q0)),float(dot(u1,q0))],
                     rescaled_B_100=[float(dot([u0[0],100*u0[1]],q0)),float(dot([u1[0],100*u1[1]],q0))],
                     interpretation='Opposite aggregate directions without common metric; not a claim that Campergue authorizes arbitrary rescaling.'),
        coefficients=dict(local=[float(x) for x in k],aggregate=[float(kt0),float(kt1)],
                          replication_1000_does_not_fix_composition=True,
                          interpretation='Composition alone changes T-weighted aggregate K despite fixed local K.'),
        result_status='FORMALLY_CONSISTENT',specificity_status='NON_DISCRIMINATING',
        unique_Money_aggregation='NOT_IDENTIFIABLE',global_theory_verdict=None)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    r=compute()
    if args.check or OUT.exists():assert json.loads(OUT.read_text())==r
    else:OUT.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('PASS: synthetic two-product calculations; no empirical validation or calibrated Money aggregation')
if __name__=='__main__':main()
