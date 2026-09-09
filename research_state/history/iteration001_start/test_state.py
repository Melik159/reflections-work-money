"""Seven structural guards and one local formal diagnostic; no economic validation."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from research_state.cycle import CONFIG,S,ROOT,PDF,tasks,formal
from rag.iterative import INDEX

def validate_source(r):
    if r['collection']=='SOURCE_CORPUS':
        assert r['document'].endswith('.pdf') or r['document'] in ['README.md','articles/purpose.md']
        assert r['source_type']=='SOURCE_CORPUS'
        if r['document'].endswith('.pdf'):assert isinstance(r['page'],int) and r['page']>0
    if r['document'].startswith(('analysis/','research_questions/','remediation/','external_review/')):
        assert r['collection']=='DERIVED_ANALYSIS'

class IterationTests(unittest.TestCase):
    def test_task_links(self):
        ts=tasks();self.assertEqual(len(ts),len({t['id'] for t in ts}))
        claims={json.loads(l)['id'] for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()}
        qs={q['id'] for q in json.loads((ROOT/'research_questions/question_graph.json').read_text())['nodes']}
        for t in ts:
            self.assertTrue(set(t['related_claims'])<=claims);self.assertTrue(set(t['related_rq'])<=qs)
            self.assertIn(t['status'],['OPEN','IN_PROGRESS','BLOCKED','DONE','SUPERSEDED'])
    def test_collection_separation_and_mutation(self):
        rows=json.loads(INDEX.read_text())['rows']
        self.assertEqual(len(rows),len({r['chunk_id'] for r in rows}))
        for r in rows:validate_source(r)
        d=copy.deepcopy(next(r for r in rows if r['collection']=='DERIVED_ANALYSIS'))
        d['collection']='SOURCE_CORPUS'
        with self.assertRaises(AssertionError):validate_source(d)
    def test_source_text_not_claim_reformulation(self):
        pages={r['page_pdf']:r['text'] for r in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
        for r in json.loads(INDEX.read_text())['rows']:
            if r['document']==PDF and r['collection']=='SOURCE_CORPUS':self.assertIn(r['text'],pages[r['page']])
    def test_closed_cycle_requires_evidence(self):
        for i,t in enumerate(tasks()[:3]):
            if t['status']=='DONE':
                d=S/'cycles'/CONFIG[i]['id'];self.assertTrue((d/'results.json').exists())
                self.assertIn('Ran 128 tests',(d/'verify.log').read_text())
                self.assertEqual((d/'baseline_manifest.log').read_text(),'')
    def test_baseline_guard(self):
        guard=json.loads((S/'baseline_guard.json').read_text())
        self.assertEqual(guard['manifest_sha256'],hashlib.sha256((ROOT/'closure_review/BASELINE_MANIFEST_SHA256.txt').read_bytes()).hexdigest())
    def test_closed_balance(self):
        self.assertEqual([x['conserved'] for x in formal(1)],[True,False,False,True])
    def test_T_independence_gate(self):
        r=formal(2)
        self.assertTrue(r['proposed_design_accepted'])
        self.assertFalse(r['circular_design_accepted'])
        self.assertFalse(r['data_available'])
    def test_utility_common_calibration(self):
        r=formal(3);self.assertTrue(r['proposed_design_accepted'])
        self.assertFalse(r['independent_scales_accepted'])
        self.assertFalse(r['ordinal_accepted'])

if __name__=='__main__':unittest.main()
