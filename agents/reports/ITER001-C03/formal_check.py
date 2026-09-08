"""Analyst diagnostic: multiplicative calibration consistency, not Utility data.

If positive scale factors s_A, s_B, s_C concern the same measurand/state,
r_AB=s_B/s_A, r_BC=s_C/s_B, r_CA=s_A/s_C imply a product of one.
This algebra is neither a source attribution nor historical novelty.
"""
from fractions import Fraction
import json
from pathlib import Path


def cycle_product(ratios):
    result = Fraction(1)
    for ratio in ratios:
        if ratio <= 0:
            raise ValueError('This diagnostic requires positive multiplicative ratios')
        result *= ratio
    return result


def main():
    cases = []
    for name, ratios, expected in [
        ('consistent', [Fraction(2), Fraction(3), Fraction(1, 6)], Fraction(1)),
        ('inconsistent', [Fraction(2), Fraction(3), Fraction(1, 5)], Fraction(6, 5)),
    ]:
        product = cycle_product(ratios)
        assert product == expected
        assert (product == 1) == (name == 'consistent')
        cases.append({'case': name, 'ratios': [str(r) for r in ratios],
                      'product': str(product), 'cycle_consistent': product == 1})
    # Independent representation by scale factors, validating the ratio orientation.
    s_A, s_B, s_C = Fraction(1), Fraction(2), Fraction(6)
    assert cycle_product([s_B/s_A, s_C/s_B, s_A/s_C]) == 1
    result = {
        'cycle': 'ITER001-C03', 'category': 'FORMAL',
        'origin': 'ANALYST_SYNTHETIC_DIAGNOSTIC',
        'assumptions': ['Same measurand and state', 'Positive multiplicative scales',
                        'No additive offsets', 'Exact ratios; no measurement uncertainty modeled'],
        'cases': cases,
        'assertions': 'PASS',
        'utility_measurement': False, 'empirical_result': False,
        'source_property_attribution': False, 'historical_novelty_claim': False,
        'scientific_decision': None,
        'limit': 'Cycle closure is necessary under assumptions; it does not establish a valid common Utility scale.'
    }
    Path(__file__).with_name('formal_results.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
