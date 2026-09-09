import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(p):return json.loads((ROOT/p).read_text())

class MoneyReview(unittest.TestCase):
    def setUp(self):
        self.review=load('analysis/data/money_compensation_scenarios.json');self.scenarios=self.review['scenarios']
        self.pages={p['page_pdf']:' '.join(p['text'].split()) for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}

    def test_scenario_inventory_locked(self):
        expected={'1','2a','2b','3a','3b','4a','4b','2a1','2a2','2b1','2b2','U1','U2','U3','U4','DENOM','REDIST','CREDIT','LAG','CONF','HYPER','HOARD','FX','MIX','SPEC','EXCLUDED','MARGIN','AGG','SPEC_UP','INTEREST_D','INTEREST_T','RECIP'}
        self.assertEqual({s['author_label'] for s in self.scenarios},expected)
        self.assertEqual(len(self.scenarios),32);self.assertEqual(len({s['id'] for s in self.scenarios}),32)

    def test_scenario_provenance_and_levels(self):
        for s in self.scenarios:
            for k in ['conditions','identity_or_definition','behavioral_assumption','causal_mechanism','derived_consequence','generalization','boundary_cases']:self.assertTrue(s[k])
            for source in s['sources']:
                self.assertIn(source['quotation'],self.pages[source['page']]);self.assertEqual(source['document'],'Reflections_PierreCampergue.pdf');self.assertTrue(source['argument_function'])
            self.assertEqual(s['boundary_cases']['epistemic_status'],'ANALYST_HYPOTHETICAL_NOT_EMPIRICAL')

    def test_no_identity_to_general_neutrality_shortcut(self):
        g=load('analysis/data/argument_graph.json');self.assertEqual(g['dependency_direction'],'premise_to_dependent')
        for e in g['edges']:
            self.assertFalse(e['source'] in ['CPC-0010','CPC-0011'] and e['target']=='CPC-0005')
            self.assertFalse(e['source']=='CPC-0010' and e['target']=='CPC-0012')
            if e['target'] in ['CPC-0005','CPC-0012','CPC-0013','CPC-0014']:self.assertTrue(e['conditions'])
        self.assertTrue({s['id'] for s in self.scenarios}<={n['id'] for n in g['nodes']})

    def test_definition_not_automatic_external_mapping(self):
        concepts={c['id']:c for c in load('analysis/data/concepts.json')};self.assertIn('money',concepts['cash']['distinguished_from'])
        for r in load('analysis/data/literature_map.json')['relations']:
            if r['claim_id'] in ['CPC-0005','CPC-0012']:
                self.assertTrue(r['conceptual_translation_required'])
                self.assertTrue(r['scope']) # a future sourced contradiction remains allowed
        self.assertTrue((ROOT/'analysis/24_money_literature_translation.md').is_file())

    def test_finding_and_claim_change_history(self):
        self.assertEqual(self.review['previous_finding']['status'],'OVER_SIMPLIFIED')
        log=load('analysis/data/money_claim_revision_log.json')
        current={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
        for r in log['reviewed']:
            self.assertEqual(r['new_statement'],current[r['claim_id']]['statement'])
            if r['action']!='KEEP':self.assertNotEqual(r['old_statement'],r['new_statement']);self.assertTrue(r['new_sources']);self.assertTrue(r['reason'])
        for s in self.scenarios:self.assertTrue(set(s['claims'])<=set(current))

    def test_conditional_algebra_not_empirical_validation(self):
        for n in [50,90,100,110,200]:self.assertAlmostEqual(n*(100/n),100)
        self.assertEqual(110*1,110) # 4a, not refutation of the corpus
        self.assertGreater(110*1.1,100) # identity permits same-sign changes
        self.assertAlmostEqual(110*.95,104.5)
        self.assertNotAlmostEqual(110-100,1-100/110)
        u,n,du,dn=1,100,-.1,10
        self.assertAlmostEqual((u+du)*(n+dn)-u*n,u*dn+n*du+dn*du)

    def test_visual_and_textual_discrepancies_not_erased(self):
        text=(ROOT/'analysis/24_money_compensation_scenarios.md').read_text()
        for marker in ['531','532','171','173','177','Constant Money','inflation','n,N']:self.assertIn(marker,text)
        visual=load('analysis/data/money_visual_checks.json')
        self.assertEqual(len(visual['analyst_corrections']),2)
        rows=[r for r in visual['checks'] if r.get('region')=='lower M→T table,2b2']
        self.assertEqual(rows[0]['directions'][0],'DOWN')
        self.assertTrue((ROOT/'analysis/history/pre_money_review/analysis/data/claims.jsonl').is_file())

if __name__=='__main__':unittest.main()
