"""Reviewer-assigned primary categories, one per discovered test method."""
import ast,csv,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'external_review'
TAGS={'I':'INTEGRITY_TEST','P':'PROVENANCE_TEST','L':'LOGIC_TEST','F':'FORMAL_TEST','E':'EMPIRICAL_REPRODUCTION_TEST','S':'SCIENTIFIC_VALIDITY_TEST'}
# Ordered by source definition, following inspection of every method and key helpers.
CLASSIFICATION={
 'test_contribution.py':'P L L L P P',
 'test_fourth_pass.py':'P F L F F F F P',
 'test_global_corpus_pass.py':'I I L P P I F P P P P P',
 'test_metrology.py':'I L L P F P P P',
 'test_micro_review.py':'E L F F P L F F',
 'test_money_review.py':'I P L P P F P',
 'test_phase2.py':'I I P I P L P P P P L P P L P I L P L I I P I I P',
 'test_productive_review.py':'P F P P F P P P',
 'test_research_questions.py':'L L L L P P P P',
 'test_second_question_pass.py':'P P P F F P P P',
 'test_synthesis.py':'I L L L P P P L L L P P L L',
 'test_terminal_review.py':'I P E P P P P P',
}
RATIONALE={
 'I':'Fichiers, schémas, empreintes, effectifs, déterminisme ou snapshot; ne prouve pas le contenu économique.',
 'P':'Citation, lien, condition, historique ou statut conservé; présence/égalité contrôlée, non suffisance de la preuve.',
 'L':'Contrôle logique du pipeline et de ses règles de rejet; pas démonstration des implications économiques du corpus.',
 'F':'Calcule une identité, un contre-exemple ou une invariance synthétique; portée mathématique locale seulement.',
 'E':'Recalcule des résultats numériques de données archivées; ni identification ni nouveau test comportemental indépendant.',
 'S':'Confronterait une prédiction économique à une mesure indépendante sous design discriminant.'}
def main():
    rows=[]
    for file,tags in CLASSIFICATION.items():
        path=ROOT/'tests/corpus'/file;tree=ast.parse(path.read_text());methods=[]
        for cls in (x for x in tree.body if isinstance(x,ast.ClassDef)):
            for f in cls.body:
                if isinstance(f,ast.FunctionDef) and f.name.startswith('test_'):methods.append((cls.name,f))
        assert len(methods)==len(tags.split()),file
        for (cls,f),tag in zip(methods,tags.split()):
            comment=RATIONALE[tag]
            if f.name=='test_24_empirical_results_reproduced_and_inputs_intact':
                comment+=' Malgré son nom, cette méthode lit quatre passed=True et des hashes, sans recomputation propre; le script amont est séparé.'
            if f.name=='test_06_physical_economic_and_actor_distinctions':
                comment+=' Hybride: inclut aussi le contre-exemple arithmétique2×3≠0; catégorie primaire provenance.'
            rows.append(dict(test=f'{path.stem}.{cls}.{f.name}',file=str(path.relative_to(ROOT)),line=f.lineno,
                 primary_category=TAGS[tag],reason=comment,
                 tests_economic_claim_against_independent_observation=False,
                 tests_local_mathematical_property=tag=='F'))
    baseline=json.loads((OUT/'baseline.json').read_text())['verification']['tests']
    assert len(rows)==120 and {r['test'] for r in rows}==set(baseline['passed_tests'])
    with (OUT/'test_audit.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    counts={v:sum(r['primary_category']==v for r in rows) for v in TAGS.values()}
    summary=dict(total=120,primary_counts=counts,artifact_tests=sum(counts[TAGS[k]] for k in ['I','P','L']),
       local_mathematical_tests=counts[TAGS['F']],empirical_reproduction_tests=counts[TAGS['E']],
       scientific_validity_tests=counts[TAGS['S']],classification_is_reviewer_judgment=True)
    (OUT/'test_audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    text='# Audit des120tests\n\nCatégories primaires exclusives, méthode par méthode; unités de comptage = méthodes unittest, pas assertions ni modèles estimés. Les tests hybrides sont signalés.\n\n'
    text+='| Catégorie | Nombre |\n|---|---:|\n'+'\n'.join(f'|{k}|{v}|' for k,v in counts.items())
    text+=f"\n\n{summary['artifact_tests']} contrôlent principalement les artefacts et la logique du pipeline; {summary['local_mathematical_tests']} des propriétés mathématiques locales; {summary['empirical_reproduction_tests']} la reproduction numérique de données. Zéro test SCIENTIFIC_VALIDITY_TEST au sens étroit d'une prédiction économique indépendante et discriminante. Cela n'enlève pas la valeur scientifique des diagnostics mathématiques négatifs.\n"
    text+='''\n## Ce que PASS ne signifie pas

La citation peut être présente mais insuffisante; le graphe peut être acyclique sans implication valide; un statut peut être verrouillé tout en étant erroné. Les14tests de synthèse sont des contrôles d'infrastructure/provenance/logique, pas14preuves économiques.

Deux contre-épreuves réellement exécutées dans independent_checks.py, sans changer les fichiers, montrent que validate accepte SYN-01 avec une phrase erronée affirmant une neutralité causale autonome, et accepte README.md comme source de ce résultat. Il teste l'existence du chemin, non son entailment. Le rapport interne annonce déjà cette limite générale, mais la garantie « aucune conclusion sans source » doit être lue au sens structurel, non sémantique.

Les calculs énergétiques et électriques sont bien réexécutés dans verify et dans des méthodes dédiées. Plusieurs tests au nom empirique ne font cependant que comparer des drapeaux. Les reconstitutions de tableaux et le smoke test amont ne constituent pas de nouvelles observations. Le golden set RAG mesure la récupération de passages annotés, pas leur vérité ni une performance externe à la sélection de questions.

Remédiation proposée : associer des rôles de preuve à chaque lien, ajouter des cas de mauvaise source pertinente en apparence, isoler les attestations documentaires des évaluations scientifiques et conserver un holdout de retrieval. Ne pas remplacer ces contrôles utiles par un score global de justesse.

## Inventaire complet

Voir test_audit.csv pour120lignes avec fichier et numéro de ligne. Toutes les méthodes y figurent, y compris les contrôles de l'audit global et de la synthèse. Le dénombrement est comparé à la liste réellement exécutée dans baseline.json.
'''
    (OUT/'03_test_audit.md').write_text(text)
    print(json.dumps(summary))
if __name__=='__main__':main()
