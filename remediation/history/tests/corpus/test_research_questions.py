import copy
import csv
import json
import unittest
from pathlib import Path
from analysis.verify_research_questions import validate

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'research_questions'

class QuestionTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.g=json.loads((OUT/'question_graph.json').read_text())

    def test_tree_structure_dependencies_and_core_coverage(self):
        r=validate(self.g)
        self.assertEqual(r['core_covered'],r['core_total'])
        self.assertGreater(r['major_covered'],r['major_total']/2)
        self.assertEqual(r['questions'],53)

    def test_rejects_missing_parent_and_duplicate_id(self):
        for mutate in [lambda g:g['nodes'].append(g['nodes'][0]),lambda g:g['nodes'][1].update(parent=None)]:
            g=copy.deepcopy(self.g);mutate(g)
            with self.assertRaises(AssertionError):validate(g)

    def test_rejects_nonexistent_and_cyclic_dependency(self):
        g=copy.deepcopy(self.g);g['nodes'][1]['dependencies'].append('RQ-UNKNOWN')
        with self.assertRaises(AssertionError):validate(g)
        g=copy.deepcopy(self.g);q=g['nodes'][1];q['dependencies'].append(q['id'])
        with self.assertRaises(AssertionError):validate(g)

    def test_resolution_and_contradiction_require_evidence(self):
        g=copy.deepcopy(self.g);g['nodes'][1].update(status='RESOLVED_WITHIN_SCOPE',scope_of_resolution=None)
        with self.assertRaises(AssertionError):validate(g)
        g=copy.deepcopy(self.g);g['nodes'][1]['status']='CONTRADICTED'
        with self.assertRaises(AssertionError):validate(g)

    def test_dossiers_source_interpretation_status(self):
        for q in self.g['nodes']:
            f=OUT/q['id']
            for name in ['README','corpus','evidence','literature','tests','conclusion']:self.assertTrue((f/(name+'.md')).is_file())
            text=(f/'corpus.md').read_text()
            self.assertIn('### SOURCE',text);self.assertIn('### INTERPRETATION',text)
            self.assertIn('## STATUS\n\n'+q['status'],(f/'conclusion.md').read_text())
            self.assertIn('## Scope',(f/'README.md').read_text())

    def test_matrix_matches_graph_and_evidence(self):
        with (OUT/'claim_question_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual({(r['Claim'],r['Question']) for r in rows},{(c,q['id']) for q in self.g['nodes'] for c in q['claims']})
        with (OUT/'evidence_matrix.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual({r['Question'] for r in rows},{q['id'] for q in self.g['nodes']})
        for row in rows:
            q=next(q for q in self.g['nodes'] if q['id']==row['Question'])
            self.assertEqual(row['Status'],q['status'])
            self.assertEqual(int(row['External literature']),len(q['literature']))

    def test_history_and_legacy_namespaces_preserved(self):
        history=json.loads((OUT/'history.json').read_text())
        self.assertEqual(set(history[0]['ids']),{q['id'] for q in self.g['nodes']})
        changes={h['id']:h for h in history if h['action']=='FIRST_PASS'}
        latest={h['id']:h for h in history if h['action'] in {'FIRST_PASS','SECOND_PASS','THIRD_PASS','FOURTH_PASS'}}
        for q in self.g['nodes']:
            if q['first_pass']:
                self.assertEqual(changes[q['id']]['old_status'],'OPEN')
                # Initial events remain historical; current state follows the latest event.
                self.assertEqual(latest[q['id']]['new_status'],q['status'])
                self.assertEqual(latest[q['id']]['new_evidence'],q['evidence'])
                self.assertTrue(set(changes[q['id']]['new_evidence'])<=set(q['evidence']))
        old=json.loads((ROOT/'analysis/data/research_questions.json').read_text())
        self.assertTrue({q['id'] for q in old}.isdisjoint({q['id'] for q in self.g['nodes']}))

    def test_root_exact_and_open_not_failure(self):
        root=next(q for q in self.g['nodes'] if q['id']=='RQ-ROOT')
        self.assertEqual(root['question'],root['source']['quotation'])
        self.assertEqual(root['source']['pages'],[2,3])
        self.assertEqual(root['associated_sentence'],'This essay should only be understood as a proposed answer to this question.')
        r=validate(self.g)
        self.assertEqual(r['status'],'PASS');self.assertGreater(r['open'],0)
