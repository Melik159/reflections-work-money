"""Exact synthetic decomposition under an analyst-defined weighted-mean model.
Not attributed to Campergue; neither empirical evidence nor a scientific decision.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def decomposition(w0, w1, k0, k1):
    assert len(w0) == len(w1) == len(k0) == len(k1)
    assert sum(w0) == sum(w1) == 1
    assert all(w >= 0 for w in w0 + w1)
    dw = [b-a for a,b in zip(w0,w1)]
    dk = [b-a for a,b in zip(k0,k1)]
    composition = sum(d*k for d,k in zip(dw,k0))
    coefficients = sum(w*d for w,d in zip(w0,dk))
    interaction = sum(a*b for a,b in zip(dw,dk))
    initial = sum(w*k for w,k in zip(w0,k0))
    final = sum(w*k for w,k in zip(w1,k1))
    direct = final-initial
    assert composition+coefficients+interaction == direct
    return {'initial':initial, 'final':final, 'direct_change':direct,
            'composition':composition, 'coefficients':coefficients,
            'interaction':interaction,
            'omitting_interaction':composition+coefficients}


def main():
    w0,w1 = [F(1,2),F(1,2)],[F(3,4),F(1,4)]
    k0=[F(1),F(3)]
    changing=decomposition(w0,w1,k0,[F(2),F(5)])
    assert [changing[x] for x in ['direct_change','composition','coefficients','interaction']] == [F(3,4),F(-1,2),F(3,2),F(-1,4)]
    assert changing['omitting_interaction'] != changing['direct_change']
    compensation=decomposition(w0,w1,k0,[F(1),F(5)])
    assert compensation['direct_change'] == 0
    assert all(compensation[x] != 0 for x in ['composition','coefficients','interaction'])
    assert compensation['omitting_interaction'] != compensation['direct_change']
    result={'cycle':'ITER001-C04','category':'FORMAL','data_origin':'SYNTHETIC',
            'model_origin':'ANALYST_ASSUMPTION',
            'assumptions':['K_t=sum(w_it*k_it)', 'Comparable coefficient units',
                           'Same component set', 'Nonnegative weights summing to one'],
            'cases':{name:{key:str(value) for key,value in case.items()}
                     for name,case in [('changing',changing),('compensation',compensation)]},
            'assertions':'PASS','omission_of_interaction_rejected':True,
            'empirical_measurement':False,'source_identity_attribution':False,
            'scientific_decision':None,
            'limit':'An unchanged aggregate need not imply unchanged coefficients; applicability of this weighted mean to source K remains unestablished.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
