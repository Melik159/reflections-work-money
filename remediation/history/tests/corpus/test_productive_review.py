import hashlib,json,math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'analysis'))
from run_productive_checks import compute
def load(p):return json.loads((ROOT/p).read_text())

class ProductiveReview(unittest.TestCase):
    def test_01_mechanisms_sources_conditions(self):
        rows=load('analysis/data/productive_mechanisms.json')['mechanisms']
        pages={p['page_pdf']:' '.join(p['text'].split()) for p in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
        self.assertEqual(len(rows),20)
        self.assertEqual({m['id']:m['conditions'] for m in rows},load('analysis/data/productive_invariant_snapshot.json')['conditions'])
        for m in rows:
            for key in ['conditions','exceptions','time_horizon','level','testability']:self.assertTrue(m[key])
            self.assertIn(m['source']['quotation'],pages[m['source']['page']])

    def test_02_work_level_not_increment(self):
        c,w=2,3;T=.5*c*w*w;dT=c*w*0
        self.assertEqual(dT,0);self.assertGreater(T,0)
        self.assertIn('work',next(c for c in load('analysis/data/concepts.json') if c['id']=='labour')['distinguished_from'])

    def test_03_transmission_not_automatic(self):
        ms={m['id']:m for m in load('analysis/data/productive_mechanisms.json')['mechanisms']}
        self.assertIn('Profits par opération inchangés',ms['PM-05']['conditions'])
        self.assertIn('prix de vente fixé',ms['PM-04']['conditions'])
        text=(ROOT/'analysis/26_cost_price_transmission.md').read_text()
        self.assertIn('NOT_ESTABLISHED_IN_REVIEWED_PASSAGES',text)

    def test_04_formulas_epistemic_separation(self):
        fs=load('analysis/data/productive_formulas.json');self.assertEqual(len(fs),20)
        self.assertEqual(len({f['id'] for f in fs}),len(fs))
        for f in fs:
            self.assertTrue(f['necessary_assumptions']);self.assertTrue(f['boundary_cases'])
            self.assertEqual(f['empirical_status'],'NOT_EMPIRICALLY_TESTED')
        self.assertEqual(sum(f['transcription_method']=='VISUAL_CHECKED' for f in fs),6)

    def test_05_productive_calculations_reproduced(self):
        actual=compute();stored=load('analysis/empirical/productive/results.json')
        self.assertEqual(actual,stored)
        self.assertEqual(len(actual['formal_checks']),5)
        self.assertTrue(all(c['passed'] for c in actual['formal_checks']))
        self.assertAlmostEqual(actual['formal_checks'][0]['result'],7/9)

    def test_06_data_not_identifying_causality(self):
        r=load('analysis/empirical/productive/results.json')
        self.assertEqual(len(r['empirical_protocols']),3)
        self.assertTrue(all(t['status']=='NOT_IDENTIFIABLE_WITH_CURRENT_DATA' for t in r['empirical_protocols']))
        for p,sha in r['input_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),sha)
        self.assertLess(r['empirical_protocols'][2]['energy_reconstruction_max_relative_error'],1e-10)

    def test_07_chapters_and_claim_links(self):
        chapters=load('analysis/data/research_chapters.json')
        for id in ['CH-06','CH-07']:
            c=next(c for c in chapters if c['id']==id)
            self.assertTrue(c['claims']);self.assertEqual(c['analysis_status'],'UNCERTAIN');self.assertTrue((ROOT/c['analysis_file']).is_file())
        known={c['id'] for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
        for m in load('analysis/data/productive_mechanisms.json')['mechanisms']:self.assertTrue(set(m['claims'])<=known)

    def test_08_monetray_and_new_rules_retained(self):
        self.assertEqual(len(load('analysis/data/money_compensation_scenarios.json')['scenarios']),32)
        rules=load('analysis/data/semantic_invariants.json');self.assertEqual(len(rules),13)
        for id in ['INV-001','INV-002','INV-005','INV-009','INV-010','INV-011','INV-012','INV-013']:self.assertIn(id,{i['id'] for i in rules})
        refs=load('bibliography/productive_library.json');self.assertEqual(len(refs),2)
        for r in refs:self.assertTrue(r['access']);self.assertTrue(r['url'])

if __name__=='__main__':unittest.main()
