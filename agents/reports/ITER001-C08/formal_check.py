"""Synthetic analyst model: delta_F = -S + s*G*m with other effects Z=0.

S: avoided physical flow for fixed service, a hypothetical assumption.
G: monetary gain on a reference basket; s: re-spending share in [0,1].
m: constant marginal intensity in ONE physical unit per monetary unit.
No claim that the source establishes these assumptions; no empirical measurement.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def flow_change(S, G, m, s):
    assert S >= 0 and G >= 0 and m >= 0
    assert F(0) <= s <= F(1)
    return -S+s*G*m


def threshold(S, G, m):
    assert S > 0 and G >= 0 and m >= 0
    if G*m == 0:
        return None
    return S/(G*m)


def main():
    S,G,m=F(4),F(10),F(1)
    critical=threshold(S,G,m)
    assert critical == F(2,5)
    cases=[]
    for s,expected in [(F(1,5),F(-2)),(F(2,5),F(0)),(F(3,5),F(2))]:
        result=flow_change(S,G,m,s)
        assert result == expected
        cases.append({'s':str(s),'delta_F':str(result)})
    assert threshold(S,G,F(0)) is None
    assert flow_change(S,G,F(0),F(1)) == -S
    unreachable=threshold(S,G,F(1,10))
    assert unreachable == F(4) and unreachable > 1
    assert flow_change(S,G,F(1,10),F(1)) == F(-3)
    result={'cycle':'ITER001-C08','category':'FORMAL','origin':'ANALYST_SYNTHETIC_MODEL',
            'formula':'delta_F = -S + s*G*m; Z=0',
            'parameters':{'S':'4','G':'10','m':'1'},'threshold_s':str(critical),'cases':cases,
            'zero_intensity':{'m':'0','threshold_s':None,'reason':'No finite threshold for positive S; G*m=0'},
            'low_intensity':{'m':'1/10','threshold_s':str(unreachable),'attainable_with_s_in_0_1':False},
            'units':{'S':'physical_unit','G':'currency_unit','s':'dimensionless','m':'physical_unit/currency_unit','delta_F':'physical_unit'},
            'assumptions':['Fixed-service avoided flow S is hypothetical, not established by source.',
                           'One physical measurand only; energy, mass and damage are not added.',
                           'Constant marginal intensity m on the same boundary and period.',
                           '0 <= s <= 1 is imposed for this toy model, not a universal spending bound.',
                           'All other effects Z equal zero; no induced investment, income or equilibrium responses.'],
            'assertions':'PASS','empirical_observation':False,'source_attribution':False,
            'scientific_decision':None}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
