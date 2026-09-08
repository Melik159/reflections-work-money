"""Current reports and metrics; keep previous reports as historical evidence."""
import csv
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,t):
    dest=ROOT/p; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t+'\n')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2))
def main():
    if (ROOT/'analysis/data/money_compensation_scenarios.json').exists():
        raise SystemExit('Historical generator: monetary revision exists; do not overwrite it.')
    chapters=read('analysis/data/research_chapters.json')
    files=['CH01_scope_wealth.md','CH02_monetary_measurement.md','CH03_objects_tasks.md','CH04_productivity_prices.md','CH05_principles.md']
    statuses=['PARTIALLY_SUPPORTED','UNCERTAIN','COHERENT','PLAUSIBLE','UNCERTAIN']
    for i,ch in enumerate(chapters):
        ch['analysis_status']=statuses[i] if i<5 else 'NOT_TESTED'
        ch['analysis_file']='analysis/chapters/'+files[i] if i<5 else None
    dump('analysis/data/research_chapters.json',chapters)
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    core=read('analysis/data/core_claims.json')
    for c in claims:
        if c['criticality'] in ['CORE','MAJOR'] and not any(r['id']==c['id'] for r in core):
            core.append(dict(id=c['id'],criticality=c['criticality'],statement=c['statement'],reason='New directed-reading qualification of existing reasoning.'))
    dump('analysis/data/core_claims.json',core)
    snapshot=read('analysis/data/regression_snapshot.json')
    entry=dict(old_status='INCOMPLETE blocks verify',new_status='SUFFICIENT_FOR_ITERATIVE_RESEARCH',new_evidence='Explicit user instruction to allow iterative research; coverage still measured.',justification='Only infrastructure errors block; scientific incompleteness becomes warning.')
    if entry not in snapshot['change_log']:snapshot['change_log'].append(entry)
    dump('analysis/data/regression_snapshot.json',snapshot)
    graph=read('analysis/data/argument_graph.json'); graph['status']='ITERATIVE_PARTIAL';dump('analysis/data/argument_graph.json',graph)
    connected={e[k] for e in graph['edges'] for k in ['source','target']}
    ga=read('analysis/data/graph_audit.json');ga.update(nodes=len(graph['nodes']),edges=len(graph['edges']),orphans=[n['id'] for n in graph['nodes'] if n['id'] not in connected]);dump('analysis/data/graph_audit.json',ga)
    rag=read('rag/evaluation/results.json'); relations=read('analysis/data/literature_map.json')['relations']
    empirical=read('analysis/empirical/iteration1/results.json'); counts=Counter(r['relation'] for r in relations)
    report=dict(phase2_status='SUFFICIENT_FOR_ITERATIVE_RESEARCH',core_claims_reviewed=24,chapters_analysed=5,
        manuscript_pages_examined=61,manuscript_pages_total=562,claims=len(claims),
        verified_sources=7,partially_verified_sources=1,literature_relations=dict(counts),
        empirical_checks=empirical['tests'],rag=rag['methods']['bm25_bilingual']['metrics'],
        french_rag=rag['methods']['bm25_bilingual']['by_language']['fr'],
        no_global_theory_verdict=True)
    tests=read('validation/phase2_regression_results.json');report['verify']=tests
    dump('validation/iteration1_scoreboard.json',report)
    write('analysis/21_empirical_iteration1.md', '# Reproduction empirique et tests accessibles\n\nLe code source original est exécuté sans modification dans des sorties temporaires. Les fichiers du dépôt ne sont pas écrasés.\n\n- EMP-001 : smoke test synthétique, beta log-log=1,5, R²>0,999999, assertions originales exécutées.\n- EMP-002 : 204 observations, 1990–2023 ; 18 régressions (6 zones × 3 modèles) ; 3 CSV reproduits : données fusionnées, régressions et fenêtres glissantes. Comparaison de toutes les colonnes avec rtol=1e-8 et atol=1e-10.\n- FORM-001 : (8/6)^2−1=77,777… %, calcul conditionnel.\n- FORM-002 : M=n.u ne suffit pas à imposer dM=0, contre-exemple algébrique hors hypothèse de compensation.\n\nLes deux derniers sont des contrôles formels, **pas des observations empiriques**. HYP-0006 est EASY pour son calcul ; sa loi physique n’est pas validée. HYP-0001 et 0003 : DIFFICULT ; HYP-0002 : MODERATE ; HYP-0004, 0005 et 0007 : NOT_OPERATIONAL_YET.\n\n## Résultats et portée\n\nLe monde donne beta log-log 1,6052 et R² 0,9909 ; en variations annuelles beta 0,8089 et R² 0,6609. L’Allemagne a beta log-log −1,2700 ; la France R² log-log 0,0124. Ces résultats concordent avec le tableau p5 de l’article de Lemariey.\n\nL’énergie est reconstruite par PIB-PPA / PIB-PPA-par-énergie. La cohérence dimensionnelle n’assure ni indépendance de mesure ni causalité ; le numérateur commun ne rend pas non plus la corrélation automatiquement tautologique si le ratio restitue effectivement une mesure énergétique. Une série physique indépendante est le prochain contrôle. Les séries diff sont contiguës ici ; le code ne vérifie pas les trous temporels pour un futur échantillon.\n\nLes régressions OLS n’offrent pas de test de causalité, de cointégration ou d’erreurs HAC. R² élevé n’est pas une significativité statistique générale. Les explications par délocalisation, énergie incorporée et tertiarisation ne sont pas départagées par ce dispositif. Les graphiques ont été générés mais ne font pas l’objet d’une comparaison pixel à pixel.\n\nRésultats, empreintes des inputs, versions et logs dans `analysis/empirical/iteration1/`.')
    table='| Méthode/périmètre | Recall@1 | Recall@3 | Recall@5 | MRR@5 |\n|---|---:|---:|---:|---:|\n'
    for method,r in rag['methods'].items():table+='| '+method+' | '+' | '.join(f"{r['metrics'][k]:.4f}" for k in ['Recall@1','Recall@3','Recall@5','MRR'])+' |\n'
    write('analysis/22_rag_iteration1.md','# RAG — comparaison conservée\n\n'+table+'\nLes trois premières méthodes utilisent le corpus initial de trois documents : elles restent directement comparables à la phase précédente. Les variantes extended, normalized et bilingual utilisent cinq documents, 590 chunks (26 pages secondaires ajoutées). La normalisation seule n’apporte pas de gain. L’expansion de vocabulaire français–anglais améliore le résultat global et le français.\n\nFrançais : Recall@5 passe de 0 à 0,3333, MRR@5 à 0,20 sur seulement six questions. La résolution n’est donc que partielle. Le dictionnaire ne contient ni IDs, ni pages, ni réponses. Il a été élaboré après inspection des erreurs du jeu de développement : **gain en échantillon**, à confirmer sur des questions françaises nouvelles. Certaines pages des articles secondaires sont pertinentes mais ne figurent pas dans les jugements initiaux, qui restent inchangés.\n\nBM25 reste le moteur par défaut avec expansion légère ; `--no-expansion` conserve le comportement lexical. Les variantes et résultats sont enregistrés, sans écraser le benchmark pré-itération archivé. Aucune API ni embedding distant.')
    write('analysis/23_iteration1_report.md', '# Itération 1\n\nPHASE_2_STATUS = SUFFICIENT_FOR_ITERATIVE_RESEARCH\n\nCORE CLAIMS REVIEWED : 24 / 24\n\nCHAPTERS ANALYSED : 5 / 10 (CH-01 à CH-05 ; statuts locaux dans les fiches).\n\nLITERATURE : 7 sources vérifiées à des profondeurs d’accès explicites ; 1 référence partiellement vérifiée. Relations : '+json.dumps(dict(counts),ensure_ascii=False)+'. Les contradictions visent une implication forte explicitement indiquée, pas un verdict global.\n\nEMPIRICAL : smoke test et reproduction des 3 CSV réussis ; deux contrôles formels distincts.\n\nRAG : BM25 bilingue, 590 chunks, 5 documents ; '+json.dumps(report['rag'])+'.\n\nCORPUS COVERAGE : 61 / 562, WARNING / COVERAGE_IN_PROGRESS.\n\nVERIFY : '+tests['status']+f" ; {tests['passed']} tests passent, {tests['failed']} échecs, {tests['errors']} erreurs."+'\n\n## Résultats intellectuels\n\n1. Money et Cash doivent être traduits avant toute comparaison à la création bancaire.\n2. M=n.u est une identité ; la neutralité exige une restriction supplémentaire.\n3. Une baisse de coût ne garantit pas une baisse du prix de vente.\n4. Le supplément individuel de pouvoir d’achat n’établit pas seul l’enrichissement agrégé.\n5. T économique est explicitement nul à vitesse constante p203, même si W est important.\n6. Le 78 % est reproduit arithmétiquement, sous loi quadratique supposée.\n7. La richesse monétaire n’épuise pas les richesses reconnues par l’auteur p204.\n8. cP et cA sont distincts malgré une notation commune p202.\n9. L’entropie est réintroduite p463–464 dans un lien physique informatif ; la portée reste à contrôler.\n10. Les relations PIB–énergie reproduites sont fortement hétérogènes entre pays.\n11. Les régressions ne valident pas une explication causale par délocalisation.\n12. La mesure indépendante de g et F est nécessaire pour une prédiction non tautologique.\n\n## Questions ouvertes et priorités\n\nMesurer T, F, c et g indépendamment ; examiner cycles et rendement ; contrôler les séries énergétiques indépendantes ; expliciter le panier de u ; étudier transmission coût/prix ; étendre le test français hors échantillon ; lire le lien chaleur–Money complet. Les notes nouvelles augmentent progressivement la couverture sans bloquer ces travaux.\n\nLa distinction WARNING/FAIL résulte de l’instruction explicite de l’utilisateur. Aucun verdict global sur la théorie. Les rapports 10–19 sont historiques ; ce rapport et les fichiers iteration1 décrivent l’état courant.')
    print(json.dumps(dict(tests=tests['tests_run'],passed=tests['passed'],failures=tests['failed'],relations=counts)))
if __name__=='__main__':main()
