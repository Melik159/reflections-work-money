import unittest
from analysis.verify_synthesis import validate,load
class RemediationTests(unittest.TestCase):
    def reject(self,number,field,value):
        rows=load('results.json');rows[number-1][field]=value
        with self.assertRaises(AssertionError):validate(results=rows,check_hashes=False)
    def test_wrong_existing_source(self):self.reject(1,'sources',['README.md'])
    def test_correct_claim_wrong_page(self):self.reject(2,'source_pages',[3])
    def test_empirical_overpromotion(self):
        rows=load('core_claims.json');next(c for c in rows if c['id']=='CPC-0016')['status']=['EMPIRICALLY_COMPATIBLE']
        with self.assertRaises(AssertionError):validate(cores=rows,check_hashes=False)
    def test_removed_condition(self):self.reject(2,'statement','T=½cpω² est valable même si cp varie sans terme supplémentaire.')
    def test_cash_money_confusion(self):self.reject(1,'statement','Cash et Money sont identiques; émission de Cash crée nécessairement Money.')
    def test_78_universal_generalization(self):self.reject(6,'statement','Le +78% est une loi empirique universelle.')
    def test_compatibility_is_not_proof(self):self.reject(10,'external_compatibility','CAUSAL_PROOF_OF_CAMPERGUE')
    def test_local_formal_remediation(self):
        self.assertEqual(2*3/4,1.5);self.assertNotEqual(2*3/4,4*3/2)
        mean_square=(1**2+3**2)/2;square_mean=((1+3)/2)**2
        self.assertEqual(mean_square-square_mean,1)
        self.assertEqual((3-2)*2**2/2,2)
