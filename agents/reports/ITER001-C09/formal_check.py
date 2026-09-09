"""Analyst synthetic horizon diagnostic, not a source law or empirical result.

Two constant-speed scenarios complete the same task quantity. A normalized speed
ratio of four is paired with an illustrative damage-rate ratio x**(5/2).
Integrated damage = constant damage rate times task duration in each scenario.
The damage-rate function and an independent damage measure are not supplied.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def main():
    speed_ratio=F(4)
    sqrt_speed_ratio=F(2)
    assert sqrt_speed_ratio**2 == speed_ratio
    damage_rate_ratio=speed_ratio**2*sqrt_speed_ratio
    duration_ratio=F(1)/speed_ratio
    integrated_damage_ratio=damage_rate_ratio*duration_ratio
    quadratic_ratio=speed_ratio**2
    assert damage_rate_ratio == F(32)
    assert duration_ratio == F(1,4)
    assert integrated_damage_ratio == F(8)
    assert integrated_damage_ratio == speed_ratio*sqrt_speed_ratio
    assert damage_rate_ratio > quadratic_ratio
    assert integrated_damage_ratio < quadratic_ratio
    result={
        'cycle':'ITER001-C09','category':'FORMAL','origin':'ANALYST_SYNTHETIC_HORIZON_DIAGNOSTIC',
        'ratios':{'normalized_speed':str(speed_ratio),'damage_rate':str(damage_rate_ratio),
                  'task_duration':str(duration_ratio),'integrated_task_damage':str(integrated_damage_ratio),
                  'quadratic_comparison':str(quadratic_ratio)},
        'checks':{'rate_ratio_exceeds_quadratic':True,'integrated_ratio_below_quadratic':True},
        'units':{'damage_rate':'damage_unit/time_unit','duration':'time_unit',
                 'integrated_damage':'damage_unit','all_reported_ratios':'dimensionless'},
        'assumptions':['Same fixed task quantity in both scenarios.',
                       'Constant speed and damage rate within each scenario.',
                       'Illustrative normalized damage-rate function x^(5/2).',
                       'Comparable damage units and physical boundaries.',
                       'No post-task, delayed or cumulative effects beyond the specified integration horizon.'],
        'limitations':['Rate and accumulated damage have different dimensions; only their separately normalized ratios are compared with 16.',
                       'An independently supported damage function and measurement are not supplied.',
                       'The example shows horizon sensitivity under assumptions; no source claim is refuted.'],
        'assertions':'PASS','empirical_observation':False,'source_law_attribution':False,
        'claim_refuted':False,'scientific_decision':None}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
