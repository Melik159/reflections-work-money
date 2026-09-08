import json
import unittest
from pathlib import Path
from analysis.run_second_pass_formal import compute
from analysis.verify_research_questions import validate

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'research_questions'
class SecondQuestionPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=json.loads((OUT/'question_graph.json').read_text());cls.man=json.loads((OUT/'second_pass_manifest.json').read_text())
        cls.q=[q for q in cls.g['nodes'] if q.get('second_pass')]

    def test_ten_dossiers_and_last_discrimination(self):
        self.assertEqual(len(self.q),10)
        self.assertEqual(sorted(self.q,key=lambda q:q['second_pass_order'])[-1]['id'],'RQ-12.01')
        for q in self.q:
            t=(OUT/q['id']/'reconstruction.md').read_text()
            self.assertLess(t.index('## PREMISES'),t.index('## INTERNAL REVIEW'))
            for head in ['DEFINITIONS','MECHANISM','DERIVATION','CONDITIONS','EXCEPTIONS','DOMAIN']:self.assertIn('## '+head,t)

    def test_source_fidelity_and_explicit_counterevidence(self):
        self.assertEqual(validate(self.g)['status'],'PASS')
        for q in self.q:
            e=[e for e in self.g['evidence'] if e['question']==q['id']]
            self.assertTrue(any(x.get('direct_corpus') for x in e))
            self.assertTrue(any(x.get('counter_kind') for x in e))
            self.assertTrue(all(x['limit'] for x in e))

    def test_utility_nonadditive_is_a_source_distinction(self):
        s=json.loads((OUT/'second_pass_sources.json').read_text())
        self.assertTrue(any(x['question']=='RQ-08.01' and x['page']==108 for x in s))
        self.assertFalse(compute()['three_products']['Utility_summed'])
        self.assertIn('explicitement', (OUT/'RQ-08.01/aggregation_tests.md').read_text())

    def test_formal_snapshot_and_three_product_weights(self):
        r=compute();self.assertEqual(r,json.loads((OUT/'second_pass_formal_results.json').read_text()))
        x=r['three_products'];self.assertEqual(x['direct_index'],x['normalized_weighted_index'])
        self.assertNotEqual(x['direct_index'],x['equal_weight_index'])
        self.assertNotEqual(*x['K_aggregate'])
        self.assertIsNone(r['global_theory_verdict'])

    def test_potential_and_metric_conditions(self):
        r=compute();self.assertEqual(*r['potential']['exact_paths']);self.assertNotEqual(*r['potential']['nonexact_paths'])
        self.assertNotEqual(r['metric']['substituted_squared'],r['metric']['printed_squared'])
        self.assertIn('IF_SAME_VARIABLES',r['metric']['status'])
        self.assertEqual(*r['metric']['normalised_slopes'])
        self.assertIn('dcp',r['T']['variable_cp_missing_term'])

    def test_money_ledger_retains_all_original_conditions(self):
        a=json.loads((ROOT/'analysis/data/money_compensation_scenarios.json').read_text())['scenarios']
        b=json.loads((OUT/'RQ-06.04/scenario_balances.json').read_text())
        self.assertEqual(len(a),32);self.assertEqual(len(b),32)
        for old,new in zip(a,b):
            self.assertEqual(old['id'],new['id']);self.assertEqual(old['conditions'],new['conditions'])
            self.assertEqual(old['sources'],new['sources']);self.assertTrue(new['horizon'])

    def test_confidence_literature_and_status_history(self):
        hist=json.loads((OUT/'history.json').read_text())
        central={s['id'] for s in json.loads((ROOT/'bibliography/initial_research_library.json').read_text())}
        for q in self.q:
            self.assertEqual(len(q['confidence_components']),4)
            self.assertTrue(set(q['confidence_components'].values())<={'LOW','MEDIUM','HIGH'})
            self.assertGreaterEqual(len(q['literature']),3);self.assertLessEqual(len(q['literature']),8)
            self.assertTrue({b['id'] for b in q['literature']}<=central)
            h=next(h for h in hist if h.get('action')=='SECOND_PASS' and h['id']==q['id'])
            self.assertEqual(h['old_status'],'OPEN');self.assertEqual(h['new_status'],q['status'])
            self.assertEqual(h['old_statement'],h['new_statement'])

    def test_coverage_and_claims_not_inflated(self):
        coverage=json.loads((ROOT/'analysis/data/page_coverage.json').read_text())
        self.assertEqual(self.man['coverage_before'],247)
        # A completed pass is an immutable historical snapshot, not a coverage ceiling.
        self.assertLessEqual(self.man['coverage_after'],sum(p['examined'] for p in coverage))
        self.assertEqual(self.man['coverage_after']-247,len(self.man['new_pages']))
        self.assertTrue(set(self.man['new_pages'])<=set(self.man['read_pages']))
        self.assertEqual(self.man['new_claims'],0)
        self.assertEqual(len((ROOT/'analysis/data/claims.jsonl').read_text().splitlines()),127)
        self.assertFalse(self.man['exhaustive_source_search'])
