"""Infrastructure and non-confusion checks; no assertion of theory validation."""
import json
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from analysis.run_micro_electricity import compute, equal, OUT, ALLOWED
from analysis.run_two_product_aggregation import compute as aggregate

ROOT=Path(__file__).resolve().parents[2]

class MicroReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result,cls.panel,cls.quality=compute()

    def test_raw_integrity_design_and_numerical_snapshot(self):
        # compute checks every source hash and the immutable pre-acquisition design.
        equal(self.result,json.loads((OUT/'results.json').read_text()))
        for name,frame in [('panel.csv',self.panel),('quality.csv',self.quality)]:
            pd.testing.assert_frame_equal(frame,pd.read_csv(OUT/name),check_exact=False,rtol=1e-10,atol=1e-10)

    def test_sample_breaks_and_causal_limits(self):
        r=self.result['regression']
        self.assertEqual(r['N'],20)
        self.assertEqual(r['years'],list(range(2003,2013))+list(range(2014,2024)))
        self.assertFalse(r['causal_identified'])
        self.assertFalse(r['structural_pass_through_identified'])
        self.assertFalse(any(self.result['missing'].values()))

    def test_dimensions_and_non_equivalence(self):
        d=self.panel
        np.testing.assert_allclose(d.fuel_cost_proxy_cents_kwh,d.gas_usd_mmbtu*d.gas_heat_btu_kwh/10000)
        self.assertEqual(self.result['margin_identification'],'NOT_IDENTIFIABLE')
        self.assertTrue(self.result['total_generation_energy_NOT_COMPUTED'])
        self.assertIn('retail_minus_fuel_proxy_NOT_MARGIN',d.columns)
        selection=(ROOT/'analysis/31_micro_data_selection.md').read_text()
        self.assertIn('WEAK_PROXY',selection)

    def test_budget_gain_is_not_surplus_or_Money(self):
        d=self.panel
        np.testing.assert_allclose(d.real2023_budget100_kwh,10000/d.retail_real2023_cents_kwh)
        np.testing.assert_allclose(d.real_gain_fixed1000kwh_usd2023.iloc[1:],-10*d.retail_real2023_cents_kwh.diff().iloc[1:])
        self.assertEqual(self.result['money_identification'],'NOT_IDENTIFIED')
        self.assertEqual(self.result['actual_consumer_surplus'],'NOT_IDENTIFIABLE')
        self.assertEqual(self.result['quality']['utility_status'],'UTILITY_NOT_IDENTIFIABLE')

    def test_conditional_predictions_preserved(self):
        p=self.result['predictions']
        self.assertEqual([x['id'] for x in p],[f'PRED-MICRO-{i:02}' for i in range(1,6)])
        for row in p:
            self.assertIn(row['result_status'],ALLOWED)
            self.assertEqual(row['specificity_status'],'NON_DISCRIMINATING')
        for i in [1,2,4]:self.assertEqual(p[i]['result_status'],'NOT_IDENTIFIABLE')
        report=(ROOT/'analysis/34_micro_empirical_results.md').read_text()
        self.assertIn('profit absolu unitaire constant',report)
        self.assertIn('CPC-0097',report)
        self.assertIn('CPC-0098',report)
        self.assertIn('CPC-0119',report)
        self.assertIsNone(self.result['global_theory_verdict'])

    def test_screening_is_not_identified_pass_through(self):
        branches=self.result['branch_years']
        # This observed A year is a known coverage break, explicitly retained as such.
        self.assertEqual(branches['A_PROXY_COST_DOWN_PRICE_DOWN'],[2002])
        self.assertIn(2002,self.result['regression']['excluded_changes'])
        self.assertEqual(branches['B_PROXY_COST_DOWN_PRICE_NEAR_STABLE'],[2016])
        self.assertEqual(self.result['chain_result_status'],'NOT_IDENTIFIABLE')

    def test_two_product_consistent_normalization(self):
        r=aggregate()
        self.assertEqual(r,json.loads((OUT/'two_product_results.json').read_text()))
        self.assertTrue(r['synthetic'])
        self.assertEqual(r['prices']['direct_Laspeyres'],r['prices']['normalized_correct_weights'])
        self.assertNotEqual(r['prices']['direct_Laspeyres'],r['prices']['normalized_equal_weights'])
        self.assertTrue(r['prices']['currency_conversion_invariant'])
        self.assertTrue(r['prices']['physical_pack_conversion_invariant'])

    def test_utility_scale_and_composition_conditions(self):
        r=aggregate()
        self.assertGreater(r['utility']['raw_fixed_basket'][1],r['utility']['raw_fixed_basket'][0])
        self.assertLess(r['utility']['rescaled_B_100'][1],r['utility']['rescaled_B_100'][0])
        self.assertNotEqual(*r['coefficients']['aggregate'])
        self.assertEqual(r['unique_Money_aggregation'],'NOT_IDENTIFIABLE')
        self.assertIsNone(r['global_theory_verdict'])
