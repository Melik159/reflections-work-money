import copy,csv,json,unittest
from pathlib import Path
from analysis.verify_contribution import validate
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'research_questions/contribution'
class ContributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads((OUT/'concepts.json').read_text());cls.k=json.loads((OUT/'core_comparisons.json').read_text());cls.s=json.loads((OUT/'literature.json').read_text())
    def test_core_complete_and_original_source_preserved(self):self.assertEqual(validate(self.c,self.k,self.s)['core_compared'],24)
    def test_originality_needs_historical_evidence(self):
        bad=copy.deepcopy(self.c);bad[0]['originality_asserted']=True
        with self.assertRaises(AssertionError):validate(bad,self.k,self.s)
    def test_conceptual_difference_not_empirical_prediction(self):
        bad=copy.deepcopy(self.c);bad[0]['different_prediction']=True
        with self.assertRaises(AssertionError):validate(bad,self.k,self.s)
        self.assertTrue(any(r['contribution_status']=='DISTINCT_FORMAL_RESTRICTION' for r in self.c))
        self.assertFalse(any(r['empirical_contribution_established'] for r in self.c))
    def test_terminology_not_substantive_automatically(self):
        bad=copy.deepcopy(self.c);next(r for r in bad if r['contribution_status']=='KNOWN_WITH_DIFFERENT_TERMINOLOGY')['substantive_difference']='YES_IN_SPECIFIED_CONSTRUCTION'
        with self.assertRaises(AssertionError):validate(bad,self.k,self.s)
    def test_matrix_and_scenario_crosswalk(self):
        with (OUT/'contribution_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(self.c)+len(self.k));self.assertEqual({r['ID'] for r in rows},{r['id'] for r in self.c+self.k})
        old=json.loads((ROOT/'analysis/data/money_compensation_scenarios.json').read_text())['scenarios'];new=json.loads((OUT/'money_scenario_comparisons.json').read_text())
        self.assertEqual(len(new),32)
        for a,b in zip(old,new):
            self.assertEqual(a['id'],b['id']);self.assertEqual(a['sources'],b['sources']);self.assertEqual(a['conditions'],b['conditions']);self.assertFalse(b['automatic_money_mapping']);self.assertFalse(b['theoretical_contradiction_inferred_from_terms'])
    def test_question_scope_and_partial_sources(self):
        g=json.loads((ROOT/'research_questions/question_graph.json').read_text());old=json.loads((ROOT/'research_questions/history/fifth_pass_before/research_questions/question_graph.json').read_text());ob={q['id']:q for q in old['nodes']}
        links=json.loads((OUT/'question_links.json').read_text());self.assertEqual(len(links),21)
        self.assertEqual(g['edges'],old['edges'])
        for q in g['nodes']:
            self.assertEqual(q['status'],ob[q['id']]['status']);self.assertEqual(q['question'],ob[q['id']]['question']);self.assertEqual(q['evidence'],ob[q['id']]['evidence'])
            if 'contribution_review' in q:self.assertEqual(set(q['contribution_review']),{'EXISTING_FRAMEWORKS','CAMPERGUE_DIFFERENCE','POTENTIAL_ADDED_VALUE','NOVELTY_STATUS'})
        self.assertTrue(any(s['status']=='PARTIALLY_VERIFIED' for s in self.s))
