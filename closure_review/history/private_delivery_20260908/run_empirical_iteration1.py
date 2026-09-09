"""Reproduce unchanged original code in temporary directories; keep textual outputs."""
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'articles/campergue_energy_gdp_code'
OUT=ROOT/'analysis/empirical/iteration1'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,MPLBACKEND='Agg')
    report={'scope':'Reproduction of repository outputs, not validation of the theory','tests':[]}
    with tempfile.TemporaryDirectory(prefix='campergue-reproduce-') as work:
        work=Path(work)
        for folder in ['src','tests']:
            shutil.copytree(SRC/folder,work/folder,ignore=shutil.ignore_patterns('__pycache__','smoke_output'))
        smoke=subprocess.run([sys.executable,str(work/'tests/smoke_test.py')],env=env,capture_output=True,text=True)
        (OUT/'smoke.log').write_text(smoke.stdout+smoke.stderr)
        report['tests'].append(dict(id='EMP-001',kind='SYNTHETIC_SMOKE',passed=smoke.returncode==0,expected='loglog beta=1.5, R2>0.999999; code asserts these conditions.'))
        if smoke.returncode:raise RuntimeError('Smoke test failed; see smoke.log')
        target=work/'macro'
        cmd=[sys.executable,str(SRC/'src/energy_gdp_analysis.py'),
             '--gdp-file',str(SRC/'data/code/API_NY.GDP.MKTP.KD.csv'),
             '--gdp-ppp-file',str(SRC/'data/code/API_NY.GDP.MKTP.PP.KD.csv'),
             '--gdp-per-energy-file',str(SRC/'data/code/API_EG.GDP.PUSE.KO.PP.KD.csv'),
             '--countries','WLD,USA,FRA,DEU,CHN,IND','--start-year','1965','--end-year','2023','--out',str(target)]
        run=subprocess.run(cmd,env=env,capture_output=True,text=True)
        (OUT/'macro.log').write_text(run.stdout+run.stderr)
        if run.returncode:raise RuntimeError('Macro execution failed; see macro.log')
        comparisons=[]
        for name in ['merged_energy_gdp.csv','regression_summary.csv','rolling_loglog_elasticity.csv']:
            expected=pd.read_csv(SRC/'output_macro'/name); actual=pd.read_csv(target/name)
            pd.testing.assert_frame_equal(actual,expected,check_dtype=False,check_exact=False,rtol=1e-8,atol=1e-10)
            comparisons.append(dict(file=name,rows=len(actual),passed=True,rtol=1e-8,atol=1e-10))
            shutil.copy2(target/name,OUT/name)
        shutil.copy2(target/'run_metadata.json',OUT/'run_metadata.json')
        report['tests'].append(dict(id='EMP-002',kind='REPOSITORY_REPRODUCTION',passed=True,comparisons=comparisons,command=cmd,
            limitations=['Energy reconstructed as PPP GDP divided by PPP GDP per energy.','No independent energy series or causal identification.','Plots executed but not compared pixel by pixel; only tabular outputs compared.']))
    # These are formal checks, deliberately not labelled empirical evidence.
    ratio=(8/6)**2-1
    assert math.isclose(ratio,7/9,rel_tol=1e-12)
    report['tests'].append(dict(id='FORM-001',kind='CONDITIONAL_ARITHMETIC',hypothesis='HYP-0006',passed=True,result=ratio,
        interpretation='77.78% follows from an assumed square-speed law. The arithmetic does not establish that law or measure energy.'))
    n0,u0,n1,u1=100,1,110,1
    assert n1*u1!=n0*u0
    report['tests'].append(dict(id='FORM-002',kind='LOGICAL_NONIMPLICATION',passed=True,
        result={'M0':n0*u0,'M1':n1*u1},interpretation='M=n.u alone does not imply neutrality. This arithmetic is compatible with Campergue possibility 4a when calibrated issuance accompanies productive creation; not a refutation of his multiple-scenario framework. See analysis/24_money_compensation_scenarios.md.'))
    inputs=[SRC/'src/energy_gdp_analysis.py',SRC/'tests/smoke_test.py']+sorted((SRC/'data/code').glob('*.csv'))
    report['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    report['environment']=dict(python=sys.version,numpy=np.__version__,pandas=pd.__version__)
    (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: synthetic smoke, 3 reproduced CSV tables, 2 separate formal checks')
if __name__=='__main__':main()
