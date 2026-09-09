"""Scoped safeguards: infrastructure truth, not a vote for or against Campergue."""
import hashlib
import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
def load(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
spec=importlib.util.spec_from_file_location('independent_energy',ROOT/'analysis/run_independent_energy.py')
energy=importlib.util.module_from_spec(spec);spec.loader.exec_module(energy)

class TerminalReview(unittest.TestCase):
    def test_01_energy_and_audit_source_integrity(self):
        for name in ['manifest','upstream_audit']:
            m=load(f'analysis/empirical/independent_energy/source/{name}.json')
            for f in m['files']:
                self.assertEqual(hashlib.sha256((ROOT/f['file']).read_bytes()).hexdigest(),f['sha256'])
        self.assertEqual(load('analysis/empirical/independent_energy/source/manifest.json')['energy_column'],'primary_energy_consumption')

    def test_02_energy_not_constructed_from_gdp(self):
        r,p=energy.compute()
        raw=pd.read_csv(ROOT/'analysis/empirical/independent_energy/source/owid-energy-data.csv',usecols=['country','year','primary_energy_consumption'])
        for row in p.itertuples():
            value=raw[(raw.country==row.country)&(raw.year==row.year)].primary_energy_consumption.iloc[0]
            self.assertEqual(row.primary_energy_consumption,value)
        self.assertTrue(r['energy_independent_of_gdp_construction'])
        self.assertFalse(r['statistically_exogenous'])
        rules=load('analysis/data/terminal_regression_rules.json')
        self.assertFalse(rules['energy_gdp_derived_is_independent'])
        self.assertFalse(rules['energy_direct_is_statistically_exogenous'])

    def test_03_empirical_results_numerically_reproduced(self):
        actual,p=energy.compute(); expected=load('analysis/empirical/independent_energy/results.json')
        self.assertEqual(actual['rows'],204);self.assertEqual(actual['missing_observations'],[])
        self.assertEqual(actual['gdp_input_sha256'],expected['gdp_input_sha256'])
        self.assertEqual(len(actual['results']),len(expected['results']))
        for a,b in zip(actual['results'],expected['results']):
            self.assertEqual((a['country'],a['model'],a['N']),(b['country'],b['model'],b['N']))
            for k in ['coefficients','ci95','se_HAC','R2']:np.testing.assert_allclose(a[k],b[k],rtol=1e-9,atol=1e-9)
        pd.testing.assert_frame_equal(p.reset_index(drop=True),pd.read_csv(ROOT/'analysis/empirical/independent_energy/analysis_panel.csv'),check_exact=False,rtol=1e-10)
        for row in load('analysis/empirical/independent_energy/stability_ratios.json'):
            d=p[p['Country Code']==row['country']];k=d.gdp_real/d.primary_energy_consumption
            self.assertAlmostEqual(row['ratio_2023_over_1990'],k.iloc[-1]/k.iloc[0],places=10)

    def test_04_exactly_three_noncausal_experiments(self):
        r=load('analysis/empirical/independent_energy/results.json')
        self.assertEqual(r['experiments'],['TEST-E1','TEST-E2','TEST-E3'])
        for x in r['results']:
            self.assertFalse(x['causal_identified']);self.assertFalse(x['predictive_validated'])
            self.assertIn(x['classification'],['ASSOCIATION','TEMPORAL_CO_MOVEMENT'])
            self.assertNotIn('DISCRIMINATES_CAMPERGUE_FROM_ALTERNATIVES',x['specificity'])
        self.assertFalse(load('analysis/data/terminal_regression_rules.json')['correlation_implies_causation'])
        mapping=load('analysis/data/energy_empirical_claim_map.json')
        self.assertEqual([x['experiment'] for x in mapping['mappings']],r['experiments'])
        self.assertIsNone(mapping['global_theory_verdict'])
        ids={c['id'] for c in lines('analysis/data/claims.jsonl')}
        for m in mapping['mappings']:
            self.assertTrue(set(m['claims'])<=ids);self.assertFalse(m['causal_identified'])
        self.assertTrue(mapping['mappings'][2]['conditions'])

    def test_05_aggregation_keeps_all_conditions(self):
        a=load('analysis/data/aggregation_mechanisms.json');rules=load('analysis/data/terminal_regression_rules.json')
        self.assertEqual([x['id'] for x in a],rules['required_aggregation_ids'])
        self.assertEqual({x['id']:x['conditions'] for x in a},rules['aggregation_conditions'])
        self.assertTrue(all(x['conditions'] and x['pages'] and x['source'] for x in a))
        self.assertTrue(rules['aggregation_requires_conditions'])

    def test_06_physical_economic_and_actor_distinctions(self):
        rules=load('analysis/data/terminal_regression_rules.json')
        self.assertFalse(rules['physical_energy_equals_economic_variable_by_default'])
        self.assertFalse(rules['transfer_implies_global_creation'])
        agents=load('analysis/data/agent_transfers.json')
        self.assertTrue(all(not a['global_creation_from_transfer_alone'] and a['conditions'] for a in agents))
        claims={c['id']:c for c in lines('analysis/data/claims.jsonl')}
        for cid in rules['required_alternatives']:self.assertTrue(claims[cid]['conditions'])
        issues=load('analysis/data/terminal_review_issues.json')
        self.assertEqual(next(i for i in issues if i['id']=='TERM-03')['status'],'AMBIGUOUS')
        self.assertEqual(next(i for i in issues if i['id']=='TERM-01')['status'],'INCONSISTENT')
        self.assertNotEqual(2*(4-1),0,'A nonzero constant force over a nonzero interval is not zero impulse')

    def test_07_environment_source_interpretation_separated(self):
        env=load('analysis/data/environmental_chain.json');rules=load('analysis/data/terminal_regression_rules.json')
        pages={r['page_pdf']:' '.join(r['text'].split()) for r in lines('corpus/extracted/Reflections_PierreCampergue.pages.jsonl')}
        for e in env['edges']:
            self.assertIn(e['epistemic_level'],rules['environmental_levels'])
            self.assertFalse(e['causal_validated']);self.assertTrue(e['conditions'])
            self.assertIn(e['source']['quotation'],pages[e['source']['page']])
        self.assertEqual(next(e for e in env['edges'] if e['id']=='ENV-05')['epistemic_level'],'RESEARCH_INTERPRETATION')
        self.assertEqual(env['rebound_comparison'],'PARTIAL_PARALLEL')

    def test_08_history_chapters_and_references(self):
        old=lines('analysis/history/pre_energy_review/analysis/data/claims.jsonl');new=lines('analysis/data/claims.jsonl')
        # Original fields remain immutable; reviewed remediation adds explicit metadata.
        for previous,current in zip(old,new[:113]):
            for key,value in previous.items():self.assertEqual(current[key],value)
        self.assertEqual(len(old),113);self.assertGreaterEqual(len(new),127)
        journal=load('analysis/data/energy_review_revision_log.json')
        self.assertLessEqual(journal['new_examined'],sum(p['examined'] for p in load('analysis/data/page_coverage.json')))
        for ch in load('analysis/data/research_chapters.json')[7:]:
            self.assertEqual(ch['analysis_status'],'UNCERTAIN')
            self.assertTrue((ROOT/ch['analysis_file']).is_file());self.assertTrue(ch['claims'])
        refs=load('bibliography/energy_aggregation_library.json');lib=load('bibliography/initial_research_library.json')
        self.assertEqual(len(refs),6);self.assertTrue({r['id'] for r in refs}<={r['id'] for r in lib})
        self.assertEqual(next(r for r in refs if r['id']=='BIB-0015')['status'],'PARTIALLY_VERIFIED')
        progress=load('analysis/data/phase2_progress.json')
        self.assertEqual(progress['claims'],len(new))
        self.assertEqual(progress['criticality'],dict(Counter(c['criticality'] for c in new)))
        self.assertEqual(progress['types'],dict(Counter(c['type'] for c in new)))

if __name__=='__main__':unittest.main()
