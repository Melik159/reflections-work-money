import copy
import unittest
from analysis.verify_synthesis import validate,load,OUT

class SynthesisTests(unittest.TestCase):
    def test_synthesis_current_inputs_and_coverage(self):
        r=validate();self.assertEqual(r['status'],'PASS');self.assertEqual(r['questions'],53)

    def test_missing_question_fails(self):
        with self.assertRaises(AssertionError):validate(questions=load('questions.json')[:-1])

    def test_missing_core_fails(self):
        with self.assertRaises(AssertionError):validate(cores=load('core_claims.json')[:-1])

    def test_source_and_interpretation_not_interchangeable(self):
        q=load('questions.json');q[0]['epistemic_kind']='SOURCE'
        with self.assertRaises(AssertionError):validate(questions=q)

    def test_claim_quote_cannot_change_silently(self):
        c=load('core_claims.json');c[0]['source']['quotation']='Invented quotation'
        with self.assertRaises(AssertionError):validate(cores=c)

    def test_global_qualification_cannot_disappear(self):
        c=load('core_claims.json');c[0]['global_qualification']=''
        with self.assertRaises(AssertionError):validate(cores=c)

    def test_result_without_provenance_fails(self):
        r=load('results.json');r[0]['sources']=[]
        with self.assertRaises(AssertionError):validate(results=r)

    def test_internal_external_distinctive_all_required(self):
        for field in ['internal_coherence','external_compatibility','distinctive_explanation']:
            r=load('results.json');r[0][field]=''
            with self.assertRaises(AssertionError):validate(results=r)

    def test_no_global_validation_certificate(self):
        m=load('manifest.json');m['global_validation']=True
        with self.assertRaises(AssertionError):validate(manifest=m)

    def test_no_novelty_without_evidence(self):
        c=load('contributions.json');c[0]['originality_asserted']=True
        with self.assertRaises(AssertionError):validate(candidates=c)

    def test_no_candidate_without_literature(self):
        c=load('contributions.json');c[0]['literature']=[]
        with self.assertRaises(AssertionError):validate(candidates=c)

    def test_root_locator_preserves_two_pages(self):
        m=load('manifest.json');m['source_root_question_pages']=[3]
        with self.assertRaises(AssertionError):validate(manifest=m)

    def test_open_questions_do_not_fail(self):
        r=validate();self.assertEqual(r['question_statuses']['OPEN'],29)
        self.assertIn('SCIENTIFIC_QUESTIONS_OPEN',r['warnings'])

    def test_no_silent_question_promotion(self):
        q=load('questions.json');q[0]['status']='RESOLVED_WITHIN_SCOPE'
        with self.assertRaises(AssertionError):validate(questions=q)
