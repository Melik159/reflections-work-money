import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
import jsonschema
from rag.retrieval import Retriever
from rag.evaluation.evaluate import measure

ROOT=Path(__file__).resolve().parents[2]
def load(path): return json.loads((ROOT/path).read_text())
def lines(path): return [json.loads(l) for l in (ROOT/path).read_text().splitlines()]
def norm(text): return ' '.join(text.split())

class Reconstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={r['page_pdf']:r['text'] for r in lines('corpus/extracted/Reflections_PierreCampergue.pages.jsonl')}
        cls.claims=lines('analysis/data/claims.jsonl')
        cls.ids={c['id'] for c in cls.claims}
        cls.concepts=load('analysis/data/concepts.json')
        cls.cids={c['id'] for c in cls.concepts}
        cls.chapters=load('analysis/data/research_chapters.json')
        cls.rows=load('rag/index/chunks.json')
        cls.golden=lines('rag/evaluation/golden_questions.jsonl')

    def test_01_source_hashes(self):
        for path,h in {
            'Reflections_PierreCampergue.pdf':'7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827',
            'articles/economic_growth_energy_campergue.pdf':'77846978295e7e7fa689e90893a372a0b4f53a6c2f947d3bbea4b263543e28ed',
            'articles/hidden_materiality_of_growth.pdf':'1f257645d224777e7460de8016093141feeecd5ef4a49fe1ca1dd3d2174635b6'}.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h)

    def test_02_pages_unique_complete_nonempty(self):
        rows=lines('corpus/extracted/Reflections_PierreCampergue.pages.jsonl')
        self.assertEqual(len(rows),562)
        self.assertEqual(sorted(self.pages),list(range(1,563)))
        self.assertTrue(all(t.strip() for t in self.pages.values()))

    def assert_source(self,s):
        self.assertEqual(s['document'],'Reflections_PierreCampergue.pdf')
        ps=s.get('pages',[s['page']])
        text=' '.join(norm(re.sub(r'^\s*'+str(p)+r'\s*\n','',self.pages[p])) for p in ps)
        self.assertIn(s['quotation'],text)

    def test_03_root_cross_page_and_associated_sentence(self):
        root=load('analysis/data/root_question.json')
        self.assertEqual(root['source']['pages'],[2,3])
        self.assert_source(root['source']); self.assert_source(root['associated_sentence'])
        self.assertEqual(root['source']['quotation'],self.claims[0]['source']['quotation'])

    def test_04_claim_schemas_and_ids(self):
        schema=load('analysis/schemas/claim.schema.json')
        jsonschema.Draft202012Validator.check_schema(schema)
        for c in self.claims:
            jsonschema.validate(c,schema)
        self.assertEqual(len(self.ids),len(self.claims))
        self.assertTrue({'CPC-0001','CPC-0002','CPC-0003'}<=self.ids)

    def test_05_all_claim_quotations(self):
        for c in self.claims:
            self.assert_source(c['source'])
            self.assertEqual(c['page'],c['source']['page'])

    def test_06_dependencies_and_derived(self):
        for c in self.claims:
            for field in ['depends_on','supports','contradicts']:
                self.assertTrue(set(c[field])<=self.ids)
                self.assertNotIn(c['id'],c[field])
            if c['type']=='DERIVED':
                self.assertTrue(c['depends_on'])

    def test_07_concept_references(self):
        self.assertEqual(len(self.cids),len(self.concepts))
        for c in self.claims:
            self.assertTrue(set(c['concepts'])<=self.cids,c['id'])
        for c in self.concepts:
            self.assertTrue(set(c['used_in_claims'])<=self.ids)
            self.assertTrue(set(c['distinguished_from'])<=self.cids)
            for s in c['quotations']:
                self.assert_source(s)

    def test_08_all_current_claims_and_core_classified(self):
        covered={c for ch in self.chapters for c in ch['claims']}
        self.assertEqual(covered,self.ids)
        self.assertTrue(all(c['id'] in covered for c in self.claims if c['criticality']=='CORE'))

    def test_09_semantic_invariants_retained(self):
        current=load('analysis/data/semantic_invariants.json')
        lock=load('analysis/data/regression_snapshot.json')
        self.assertEqual({x['id']:x['formulation'] for x in current},lock['invariants'],
            'Semantic change requires a documented snapshot update, not silent removal.')
        for inv in current:
            self.assertTrue(set(inv['claims'])<=self.ids)
            for s in inv['sources']:
                self.assert_source(s)
        for a,b in [('cash','money'),('labour','work'),('creation','distribution'),('accounting','transformation')]:
            self.assertIn(b,next(c for c in self.concepts if c['id']==a)['distinguished_from'])

    def test_10_open_issues_retained(self):
        snapshot=load('analysis/data/regression_snapshot.json')
        issues=load('analysis/data/open_reconstruction_issues.json')
        self.assertEqual({i['id']:i['status'] for i in issues},snapshot['open_issues'],
            'Issue disposition requires old/new status, evidence and justification.')

    def test_11_graph_endpoints_and_acyclic_dependencies(self):
        graph=load('analysis/data/argument_graph.json')
        nodes={n['id'] for n in graph['nodes']}
        adjacency={n:[] for n in nodes}
        for e in graph['edges']:
            self.assertIn(e['source'],nodes); self.assertIn(e['target'],nodes)
            self.assert_source(e['evidence'])
            if e['relation']=='DEPENDS_ON': adjacency[e['source']].append(e['target'])
        active=set(); done=set()
        def visit(n):
            self.assertNotIn(n,active,'Dependency cycle detected; review and record rather than delete.')
            if n in done:return
            active.add(n)
            for other in adjacency[n]:visit(other)
            active.remove(n);done.add(n)
        for n in nodes: visit(n)

    def test_12_coverage_and_note_evidence(self):
        rows=load('analysis/data/page_coverage.json')
        self.assertEqual([r['page'] for r in rows],list(range(1,563)))
        for r in rows:
            if r['examined']:
                self.assertTrue((ROOT/'analysis/reading_notes'/r['reading_note']).is_file())
            else:
                self.assertEqual(r['reason'],'NOT_YET_READ')
            self.assertTrue(set(r['claims'])<=self.ids)

    def test_13_golden_sources(self):
        self.assertGreaterEqual(len(self.golden),40)
        self.assertEqual(len({q['id'] for q in self.golden}),len(self.golden))
        for q in self.golden:
            self.assertTrue(set(q['expected_claims'])<=self.ids)
            self.assertTrue(set(q['expected_concepts'])<=self.cids)
            for s in q['expected_passages']:
                self.assertIn(s['passage'],norm(self.pages[s['page']]))

    def test_14_wrong_passage_fails_retrieval(self):
        q=self.golden[0]
        fake=dict(document=q['expected_document'],page=q['expected_pages'][0],text='unrelated passage')
        self.assertEqual(measure([fake],q)['MRR'],0)
        fake['text']=q['expected_passages'][0]['passage']; fake['page']=562
        self.assertEqual(measure([fake],q)['MRR'],0)

    def test_15_index_source_fidelity(self):
        self.assertEqual(len(self.rows),load('rag/index/manifest.json')['chunks'])
        for r in self.rows:
            source=self.pages[r['page']] if r['page'] else (ROOT/r['document']).read_text()
            self.assertEqual(norm(r['text']),norm(source))

    def test_16_benchmark_current_and_nonregressing(self):
        result=load('rag/evaluation/results.json')
        for field,path in [('golden_sha256','rag/evaluation/golden_questions.jsonl'),('index_sha256','rag/index/chunks.json')]:
            self.assertEqual(result[field],hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
        baseline=load('analysis/data/regression_snapshot.json')['rag_metrics']
        for method,run in result['methods'].items():
            for key,value in run['metrics'].items():
                self.assertGreaterEqual(value+1e-12,baseline[method][key])
                self.assertTrue(0<=value<=1)

    def test_17_no_unsupported_empirical_validation(self):
        for c in self.claims:
            self.assertEqual(c['epistemic_status'],'SOURCE')
            self.assertTrue(c['interpretive'])
        for h in load('analysis/data/hypotheses.json'):
            self.assertEqual(h['status'],'PROPOSED_NOT_EXECUTED')
            self.assertIn(h['claim_source'],self.ids)

    def test_18_chapters_root_and_questions(self):
        self.assertTrue(8<=len(self.chapters)<=12)
        questions=load('analysis/data/research_questions.json')
        for ch in self.chapters:
            self.assertTrue(ch['root_question_relation'])
            self.assertTrue(any(q['chapter']==ch['id'] for q in questions))

    def test_19_schema_rejects_missing_source_and_bad_type(self):
        c=copy.deepcopy(self.claims[0]); del c['source']
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(c,load('analysis/schemas/claim.schema.json'))
        c=copy.deepcopy(self.claims[0]); c['type']='VALIDATED_THEORY'
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(c,load('analysis/schemas/claim.schema.json'))

    def test_20_retrieval_determinism(self):
        retriever=Retriever(self.rows)
        for method in ['legacy','tfidf','bm25']:
            self.assertEqual(retriever.search('Cash Money',method),retriever.search('Cash Money',method))
            self.assertEqual(retriever.search('',method),[])

    def test_21_phase2_exit_criteria(self):
        coverage=load('analysis/data/page_coverage.json')
        n=sum(r['examined'] for r in coverage)
        self.assertEqual(n,562,f'INCOMPLETE: {n}/562 pages examined; no global PASS permitted.')
        self.assertTrue(all(ch['status']=='COMPLETE' for ch in self.chapters))

if __name__=='__main__': unittest.main()
