"""Run assertions and write exact counts, including unmet scientific exit criteria."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

class RecordedResult(unittest.TextTestResult):
    def startTestRun(self):
        super().startTestRun(); self.passed=[]
    def addSuccess(self,test):
        super().addSuccess(test); self.passed.append(test.id())

suite=unittest.defaultTestLoader.discover(str(ROOT/'tests/corpus'))
result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
report=dict(tests_run=result.testsRun,passed=len(result.passed),failed=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),passed_tests=result.passed,
    failures=[dict(test=t.id(),traceback=msg) for t,msg in result.failures+result.errors],status='PASS' if result.wasSuccessful() else 'FAIL')
coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
report['coverage']={'examined':sum(p['examined'] for p in coverage),'total':len(coverage)}
report['warnings']=['COVERAGE_IN_PROGRESS','LITERATURE_PARTIAL','CHAPTERS_IN_PROGRESS','HYPOTHESES_NOT_ALL_TESTED']
(ROOT/'validation').mkdir(exist_ok=True)
(ROOT/'validation/phase2_regression_results.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(0 if result.wasSuccessful() else 1)
