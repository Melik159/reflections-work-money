"""Analyst synthetic budget identities, not a measurement of source Money.

All deltas compare a treatment world to an explicit counterfactual world over
matching periods. delta_b is the difference between their changes in liquid
balances, not the difference between their balance levels. L is new borrowing received (principal repayments excluded),
A is net acquisition of non-liquid assets, R principal repayment, Tr net outgoing
transfers. Income y excludes these separately recorded flows. G is spending freed
on the fixed reference basket; X is additional spending beyond that basket.
Revaluation and nontransactional stock changes are excluded from this toy model.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def balance_change(y=F(0), L=F(0), G=F(0), X=F(0), A=F(0), R=F(0), Tr=F(0)):
    return y+L+G-X-A-R-Tr


def main():
    gains=[F(10),F(0)]
    expenditures=[F(0),F(10)]
    db=[balance_change(G=g,X=x) for g,x in zip(gains,expenditures)]
    assert db == [F(10),F(-10)]
    total_uses=sum(db)+sum(expenditures)
    assert total_uses == sum(gains) == F(10)
    erroneous_uses=sum(max(b,F(0)) for b in db)+sum(expenditures)
    assert erroneous_uses == F(20)
    assert erroneous_uses != total_uses
    income_offset=balance_change(y=F(-10),G=F(10))
    assert income_offset == F(0)
    result={'cycle':'ITER001-C07','category':'FORMAL','origin':'ANALYST_SYNTHETIC_BUDGET_IDENTITY',
            'periods':[{'G':str(g),'X':str(x),'delta_b':str(b)} for g,x,b in zip(gains,expenditures,db)],
            'sum_delta_b_plus_X':str(total_uses),
            'erroneous_intermediate_saving_plus_later_spending':str(erroneous_uses),
            'double_count_rejected':True,
            'income_offset_case':{'delta_y':'-10','G':'10','delta_b':str(income_offset)},
            'assertions':'PASS','empirical_observation':False,'Money_measurement':False,
            'scientific_decision':None,
            'scope':'Matched two-world cash budget. Not an aggregate income or welfare identity.',
            'assets':'Non-liquid asset purchases are separate cash uses delta_A, set to zero here; their asset value is not additional spending or income. Revaluation and other nontransactional stock changes excluded.',
            'limits':['G assumes a fixed reference basket and explicit counterfactual price.',
                      'A zero liquid-balance difference does not imply zero welfare change.',
                      'Income-offset case does not estimate economy-wide income effects.']}
    Path(__file__).with_name('results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
