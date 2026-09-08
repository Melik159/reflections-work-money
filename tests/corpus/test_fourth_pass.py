import copy,hashlib,json,unittest
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path
from analysis.run_fourth_pass import check_protocols,compute,encode
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'research_questions/experiments'
def validate_operations(rows):
    for r in rows:
        assert r['source_page'] and r['condition']
        if r['operation']=='RATIO':assert r['ratio_scale_required'] and not r['ordinal_sufficient']
class FourthPassTests(unittest.TestCase):
    def test_protocols_frozen_before_execution(self):
        m=check_protocols();e=json.loads((OUT/'fourth_pass_execution.json').read_text())
        self.assertEqual(set(m['selected']),{'EXP-02','EXP-03','EXP-09'})
        self.assertLess(datetime.fromisoformat(m['frozen_at']),datetime.fromisoformat(e['executed_at']))
        self.assertEqual(e['protocol_manifest_sha256'],hashlib.sha256((OUT/'fourth_pass_protocol_manifest.json').read_bytes()).hexdigest())
        self.assertFalse(m['amendments'])
        for eid in m['selected']:
            s=(OUT/eid/'protocol.md').read_text()
            for h in ['SUCCESS_CRITERION','QUALIFICATION_CRITERION','CONTRADICTION_CRITERION','NON_IDENTIFICATION_CRITERION','MEASUREMENT_LEVELS']:self.assertIn('## '+h,s)
    def test_result_snapshots(self):
        for eid,r in json.loads(json.dumps(compute(),default=encode)).items():self.assertEqual(r,json.loads((OUT/eid/'results.json').read_text()))
    def test_ratio_requirements_and_negative_control(self):
        rows=json.loads((OUT/'EXP-02/operation_requirements.json').read_text());validate_operations(rows)
        bad=copy.deepcopy(rows);next(r for r in bad if r['operation']=='RATIO')['ordinal_sufficient']=True
        with self.assertRaises(AssertionError):validate_operations(bad)
    def test_utility_covariance_not_just_ordinals(self):
        r=compute()['EXP-02']['transformed']
        self.assertEqual(r['identity']['ratio'],r['ratio']['ratio'])
        self.assertNotEqual(r['identity']['ratio'],r['affine']['ratio'])
        self.assertEqual(r['identity']['ratio_of_differences'],r['affine']['ratio_of_differences'])
        self.assertNotEqual(r['affine']['compensating_r_at_2'],r['affine']['compensating_r_at_4'])
    def test_K_composition_conditions(self):
        r=compute()['EXP-03'];self.assertTrue(r['assumptions'])
        self.assertEqual([len(c['cases']) for c in r['cases']],[9,27])
        for group in r['cases']:
            self.assertNotEqual(*group['range'])
            for c in group['cases']:self.assertEqual(c['K'],c['replicated_K']);self.assertEqual(c['homogeneous_K'],2)
        c=r['compensation'];self.assertNotEqual(c['weights0'],c['weights1']);self.assertEqual(c['K0'],c['K1'])
    def test_K_normalization_covariant(self):
        n=compute()['EXP-03']['normalization']
        self.assertNotEqual(n['raw_incommensurate_K'],n['restored_common_unit_K'])
        self.assertEqual(n['common_unit_K']*n['common_scale'],n['restored_common_unit_K'])
    def test_T_models_no_independent_measurement(self):
        r=compute()['EXP-09'];self.assertEqual(len(r['models']),3)
        self.assertEqual(r['signed_accumulation'],0);self.assertGreater(r['positive_accumulation'],0)
        self.assertNotEqual(r['variable_cp']['delta_state'],r['variable_cp']['omega_only_integral'])
        self.assertFalse(r['independent_T_measured']);self.assertFalse(compute()['EXP-02']['Money_observed'])
        self.assertFalse(json.loads((OUT/'fourth_pass_execution.json').read_text())['Money_observed'])
    def test_scoped_evidence_and_preserved_claims(self):
        m=json.loads((OUT/'fourth_pass_integration.json').read_text());g=json.loads((ROOT/'research_questions/question_graph.json').read_text());old=json.loads((ROOT/'research_questions/history/fourth_pass_before/research_questions/question_graph.json').read_text())
        self.assertEqual(g['edges'],old['edges']);self.assertEqual(m['new_claims'],0)
        self.assertEqual(m['new_empirical_experiments'],0)
        self.assertEqual(len(m['questions']),4)
        cs={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
        for i in json.loads((OUT/'fourth_pass_claim_impacts.json').read_text()):
            self.assertEqual(i['new_statement'],cs[i['id']]['statement']);self.assertTrue(i['source_unchanged'])
        exps=json.loads((ROOT/'research_questions/operationalization/experiments.json').read_text());first=next(e for e in exps if e['id']=='EXP-01')
        self.assertEqual(first['feasibility'],'NEEDS_DEFINITION');self.assertEqual(first['execution_status'],'DESIGNED_NOT_EXECUTED')
