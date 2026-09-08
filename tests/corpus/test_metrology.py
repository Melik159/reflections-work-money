import copy,json,unittest
from pathlib import Path
from analysis.run_metrology_checks import compute
ROOT=Path(__file__).resolve().parents[2]
MET=ROOT/'research_questions/operationalization'
STATUSES={'DIRECTLY_OBSERVABLE','DERIVABLE_FROM_OBSERVABLES','IDENTIFIABLE_WITH_ASSUMPTIONS','PROXY_ONLY','LATENT','NOT_OPERATIONALIZED','AMBIGUOUS'}
def validate_variables(vs):
    assert len({v['id'] for v in vs})==len(vs)
    for v in vs:
        assert v['measurement_status'] in STATUSES
        assert v['measurement_level'] in range(6)
        assert v['pages'] and all(1<=p<=562 for p in v['pages'])
        assert v['necessary_assumptions'] and v['dimension'] and v['source_unit']
        assert not(v['measurement_level']<=1 and v['empirical_measurement_claimed'])
        if v['measurement_status']=='PROXY_ONLY':assert v['proxy_explicit'] and 'PROXY' in v['proxy_or_procedure']
        if v['measurement_level']>=4:assert (ROOT/v['available_data_artifact']).is_file()
class MetrologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vs=json.loads((MET/'variables.json').read_text());cls.byname={v['name']:v for v in cls.vs}
        cls.exps=json.loads((MET/'experiments.json').read_text())
    def test_variable_schema_and_maturity(self):validate_variables(self.vs)
    def test_low_maturity_cannot_be_observed(self):
        bad=copy.deepcopy(self.vs);bad[0]['empirical_measurement_claimed']=True
        with self.assertRaises(AssertionError):validate_variables(bad)
    def test_proxy_must_remain_explicit(self):
        bad=copy.deepcopy(self.vs);next(v for v in bad if v['measurement_status']=='PROXY_ONLY')['proxy_explicit']=False
        with self.assertRaises(AssertionError):validate_variables(bad)
    def test_experiment_variables_levels_and_execution(self):
        byid={v['id']:v for v in self.vs}
        self.assertTrue(5<=len(self.exps)<=10)
        for e in self.exps:
            self.assertTrue(e['variables'] and e['prediction'] and e['alternative_prediction'])
            for v in e['variables']:self.assertEqual(v['measurement_level'],byid[v['id']]['measurement_level'])
            self.assertIn(e['execution_status'],{'EXECUTED_FORMAL','DESIGNED_NOT_EXECUTED'})
            self.assertFalse(e['independent_law_test'])
    def test_formal_results_reproduced_not_law_evidence(self):
        r=compute();self.assertEqual(r,json.loads((MET/'formal_results.json').read_text()))
        self.assertFalse(r['empirical_validation']);self.assertFalse(r['circularity']['admissible_independent_law_test'])
        self.assertNotEqual(*r['utility']['implied_yields'])
    def test_utility_admission_exact_on_page(self):
        p={r['page_pdf']:r['text'] for r in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
        self.assertIn("If it's possible to measure need, the same cannot be said for Utility.",' '.join(p[109].split()))
        self.assertEqual(self.byname['Utility']['measurement_status'],'NOT_OPERATIONALIZED')
        self.assertEqual(self.byname['Utility']['candidate_proxy_level'],2)
        self.assertEqual(self.byname['Money']['measurement_level'],1)
    def test_ten_question_links_and_history_preserved(self):
        m=json.loads((MET/'manifest.json').read_text());g=json.loads((ROOT/'research_questions/question_graph.json').read_text());qs={q['id']:q for q in g['nodes']}
        self.assertEqual(len(m['questions']),10)
        old=json.loads((ROOT/'research_questions/history/third_pass_before/research_questions/question_graph.json').read_text())
        self.assertEqual(old['edges'],g['edges'])
        for q in m['questions']:
            self.assertTrue(qs[q]['third_pass']);self.assertTrue((ROOT/'research_questions'/q/'metrology.md').is_file())
            self.assertTrue(qs[q]['measurement_variables'])
    def test_coverage_snapshot_and_no_new_claims(self):
        m=json.loads((MET/'manifest.json').read_text());c=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
        self.assertEqual(m['coverage_after']-m['coverage_before'],len(m['new_pages']))
        self.assertLessEqual(m['coverage_after'],sum(p['examined'] for p in c))
        self.assertEqual(m['new_claims'],0)
