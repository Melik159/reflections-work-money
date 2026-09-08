"""Four scoped algebra diagnostics; stdlib only, not empirical tests."""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'

def compute():
    return {
      'protocol_sha256':hashlib.sha256((OUT/'formal_check_protocol.md').read_bytes()).hexdigest(),
      'type':'FORMAL_SYNTHETIC_NOT_EMPIRICAL',
      'checks':[
        {'id':'GC-CHECK-01','pages':[525,526],
         'conditions':'r=g=1; dimensionless p=exp(z), z in {2,3}; g fixed',
         'normalized_derivatives':[{'log_p':z,'from_differential':-1.,'from_printed_primitive':-1./(z*z)} for z in (2,3)],
         'result':'FORMALLY_INCONSISTENT_LOCAL_DERIVATION'},
        {'id':'GC-CHECK-02','pages':[523,528],
         'conditions':'Mc=2-x, Md=x, x in [0,1]; 2-2x>=0 analytically',
         'levels':[{'x':x,'Mc':2-x,'Md':x} for x in (0,.25,.5,.75,1)],
         'derivatives':{'Mc':-1,'Md':1},
         'result':'LEVEL_INEQUALITY_DOES_NOT_IMPLY_DERIVATIVE_INEQUALITY'},
        {'id':'GC-CHECK-03','pages':[523,528],
         'conditions':'gTM=gMT=1, Td=2t,Tc=t,Mc=2t,Md=t,t>0',
         'coefficient_product':1.,'dTc_over_dTd':.5,
         'result':'EQUALITY_REQUIRES_ADDITIONAL_CONDITION'},
        {'id':'GC-CHECK-04','pages':[435,439],
         'conditions':'r,V,B held fixed; U>0',
         'values':[{'U':u,'TM_definition_and_final':-1/u,'TM_printed_intermediate':1/u,
                    'MT_definition_and_final':1/u,'MT_printed_intermediate':-1/u} for u in (2,5)],
         'result':'INTERMEDIATE_CONFLICT_FINAL_LOCALLY_RECOVERABLE'}
      ]}

def validate(result):
    checks=result['checks'];assert len(checks)==4
    assert all(not math.isclose(x['from_differential'],x['from_printed_primitive']) for x in checks[0]['normalized_derivatives'])
    assert all(x['Mc']>=x['Md'] for x in checks[1]['levels'])
    assert checks[1]['derivatives']['Mc']<checks[1]['derivatives']['Md']
    assert checks[2]['coefficient_product']!=checks[2]['dTc_over_dTd']
    for row in checks[3]['values']:
        assert row['TM_definition_and_final']==-row['TM_printed_intermediate']
        assert row['MT_definition_and_final']==-row['MT_printed_intermediate']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=compute();validate(result);p=OUT/'formal_checks.json'
    if args.check:assert json.loads(p.read_text())==result, 'Result/protocol changed; preserve history before revision'
    elif p.exists():raise SystemExit('Existing result: use --check')
    else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: four local formal diagnostics; NOT an empirical or full-corpus validation')

if __name__=='__main__':main()
