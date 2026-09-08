"""Generate descriptive reports from reviewed data, retaining INCOMPLETE status."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text())
def write(p,t):
    dest=ROOT/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(t+'\n')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2))

SECTIONS=[('1','Preamble',12,37),('1.1','Monetary Developments',12,30),('1.2','Core Elements',30,37),
('2','Developments',38,559),('2.1','Prolegomena',38,167),('2.2','Value of the monetary unit',168,184),
('2.3','Basic Definitions',184,194),('2.4','Mechanics of exchanges',194,215),('2.5','Basic Principles',216,230),
('2.6','Internal Energies',231,257),('2.7','Flows and transformations',258,278),('2.8','Core Laws',279,301),
('2.9','Additional definitions',302,318),('2.10','Difficulties',319,334),('2.11','Structure of exchanges',335,344),
('2.12','Cycles',345,371),('2.13','Money and Work – Conditions of creation',372,383),('2.14','Processing yields',384,401),
('2.15','Product and Money – Supply and Demand',402,412),('2.16','Ecodynamic potentials',413,430),
('2.17','Ecoelastic coefficients',431,440),('2.18','Ecometric coefficient',441,453),('2.19','Link heat consumption to money created',454,464),
('2.20','Conservation Laws',465,472),('2.21','Discrimination of economic agents',473,485),('2.22','Monopoles',486,493),
('2.23','Cycles – Polar interpretation',494,499),('2.24','Miscellaneous observations',500,522),('2.25','Transformations coefficients',523,535),
('2.26','Micro – Macro link',536,559),('3','Annexes',560,560),('4','Bibliographic Note',560,560),('5','Introduction of the Author',561,562)]

HYPOTHESES=[
(17,'Une augmentation de vitesse d’une tâche inchangée exige une énergie mécanique supplémentaire.',
 'Vitesse d’exécution (tâches/h)','Énergie mécanique par tâche (J/tâche)',
 'Mesures appariées de machines exécutant le même produit et la même méthode à plusieurs vitesses.',
 'Estimer énergie par tâche en fonction de vitesse, avec instrumentation indépendante.',
 'Énergie croissante avec vitesse à périmètre identique.',
 'Accélération reproductible sans énergie supplémentaire dans le domaine défini.',
 'Changement de méthode, pertes fixes, qualité, périmètre énergétique, puissance versus énergie.'),
(16,'Une productivité accrue transmet une baisse de coût au prix payé par le consommateur.',
 'Productivité et coût unitaire','Prix de vente et quantité accessible à revenu fixé',
 'Panel produit-établissement avec coûts, volumes, prix, qualité et structure concurrentielle.',
 'Étude événementielle d’un changement technique ; vérifier tendances et chocs concomitants.',
 'Baisse de prix après baisse de coût, si les hypothèses de transmission sont satisfaites.',
 'Coût réduit sans baisse de prix : réfute transmission automatique, pas la seule possibilité productive.',
 'Marge, concurrence, salaires, qualité, demande, change, délai de transmission.'),
(29,'Le niveau de vie aurait été constant du Néolithique au XVIIIe siècle.',
 'Période et système énergétique','Panier réel de consommation par personne',
 'Séries historiques comparables ; données archéologiques et incertitudes de reconstruction.',
 'Comparer variations de niveaux de vie avant industrialisation avec intervalles d’incertitude.',
 'Pas de variation substantielle durable avant les moteurs selon la formulation forte.',
 'Variation substantielle documentée avant le XVIIIe siècle à définition constante.',
 'Sélection géographique, paniers incomparables, démographie, distribution, données manquantes.'),
(58,'Une utilité presque constante d’une œuvre d’art empêcherait une baisse de son prix.',
 'Utilité mesurée indépendamment et entretien','Prix réel de revente',
 'Ventes répétées d’œuvres, état, préférences et liquidité ; indicateur d’utilité indépendant du prix.',
 'Rechercher baisses de prix sous stabilité documentée des conditions pertinentes.',
 'Absence de baisse selon la formulation citée.',
 'Baisse robuste de prix à utilité indépendamment stable.',
 'Goûts, attribution, liquidité, monnaie, coûts de transaction ; utilité non observée.'),
(59,'L’utilité de Cash serait plus forte chez les agents de faible revenu.',
 'Revenu réel et patrimoine','Mesure comportementale indépendante de l’utilité d’une somme donnée',
 'Enquête ou protocole de choix avec revenu, besoins et préférences.',
 'Estimer relation revenu-utilité en déclarant explicitement la mesure choisie.',
 'Relation décroissante.',
 'Relation croissante robuste dans le périmètre et la métrique acceptés.',
 'Confusion avec utilité marginale pourtant exclue ; préférences, besoins, patrimoine, échelle interpersonnelle.'),
(35,'L’exemple 8 h→6 h est associé à environ 78 % de Work supplémentaire.',
 'Rapport de vitesses 8/6','Rapport de Work mesuré ou calculé',
 'Définition analytique de T, c et force ; mêmes tâche et méthode.',
 'Vérifier si la loi requise T proportionnel au carré de la vitesse est justifiée et applicable.',
 '(8/6)^2-1 = 0,777... sous cette hypothèse supplémentaire.',
 'Définition ultérieure de T incompatible avec ce rapport dans les conditions annoncées.',
 'Énergie et puissance confondues ; changements de complexité ; absence d’unité indépendante pour T.'),
(12,'L’émission d’unités aurait une compensation inverse de leur valeur, sans variation de Money global.',
 'Nombre d’unités à périmètre fixé','Valeur d’unité sur panier fixé et produit n.u',
 'Périmètre de n accepté par le modèle, panier stable, horizon et mécanisme d’émission.',
 'Mesurer conjointement n et u lors d’une variation isolable ; dissocier identité et hypothèse de neutralité.',
 'dM=0 pour la variation sans Work telle que définie par l’auteur.',
 'Variation de n.u incompatible avec la neutralité après contrôle des variations réelles.',
 'Identification du choc, simultanéité des prix, endogénéité du crédit, exclusion de M0/M1 dans le corpus.')]

def main():
    if read('analysis/data/phase2_progress.json').get('status')=='SUFFICIENT_FOR_ITERATIVE_RESEARCH':
        raise SystemExit('Historical reports frozen. Use current iteration reports; do not overwrite later hypotheses or bibliography.')
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    concepts=read('analysis/data/concepts.json'); chapters=read('analysis/data/research_chapters.json')
    coverage=read('analysis/data/page_coverage.json'); core=read('analysis/data/core_claims.json')
    structure=[]
    for sid,title,start,end in SECTIONS:
        complete=all(coverage[p-1]['examined'] for p in range(start,end+1))
        ids=[c['id'] for c in claims if any(start<=p<=end for p in c['source']['pages'])]
        structure.append(dict(id='MS-'+sid,title=title,pages=[start,end],
            descriptive_summary=('Voir notes de lecture.' if complete else 'Titre et plage annoncés par Summary ; corps non entièrement examiné.'),
            concepts=sorted({t for c in claims if c['id'] in ids for t in c['concepts']}),main_claims=ids,
            root_question_relation='Contribution au mécanisme travail→Money à établir section par section.',
            verification='BODY_EXAMINED' if complete else 'TOC_PROVISIONAL',parent='MS-'+sid.rsplit('.',1)[0] if '.' in sid else None))
    dump('analysis/data/manuscript_structure.json',structure)
    write('analysis/11_manuscript_structure.md','# Structure du manuscrit — INCOMPLETE\n\nLa structure ci-dessous distingue les titres de la table des matières et les parties effectivement lues. Les sections peuvent partager leur page frontière. Les sous-sections et transitions hors notes restent à reconstruire.\n\n'+ '\n'.join(f"- {s['id']} — {s['title']} — p{s['pages'][0]}–{s['pages'][1]} — {s['verification']}" for s in structure))
    with_claim=sum(bool(p['claims']) for p in coverage); examined=sum(p['examined'] for p in coverage)
    write('analysis/12_claim_coverage.md',f'# Couverture — INCOMPLETE\n\n562 pages présentes ; {examined} examinées ; {with_claim} avec claims ; {562-with_claim} sans claim. Aucune page exclue du programme.\n\nLes pages 1–37 et 184–194 ont une note. Les 514 autres sont NOT_YET_READ. Une page de titre ou de sommaire lue reste comptée comme examinée. Aucun titre détecté automatiquement ne fait monter ce compteur.\n\nLes raisons, concepts, claims et notes sont consignés page par page dans `analysis/data/page_coverage.json`. La couverture à 100 % n’est pas atteinte.')
    invariants=read('analysis/data/semantic_invariants.json')
    write('analysis/13_semantic_invariants.md','# Invariants documentés dans les passages examinés\n\nCes invariants vérifient la fidélité, pas la vérité des thèses. Leur portée ne peut être étendue aux pages non lues.\n\n'+'\n'.join(f"- {x['id']} : {x['formulation']} Sources : "+', '.join(f"p{s['page']}" for s in x['sources']) for x in invariants))
    write('analysis/14_argument_reconstruction.md', '# Reconstruction argumentative — INCOMPLETE\n\nQuestion racine → mécanisme proposé CPC-0016 → transition historique CPC-0018. Le calcul M=n.u (CPC-0010) donne son différentiel CPC-0011 ; la neutralité CPC-0012 exige en plus des restrictions sur n et u. Les principes CPC-0023, 0032, 0033 et 0043 sont enregistrés comme axiomes, pas comme résultats calculés.\n\nLes arêtes DEPENDS_ON vont de la prémisse au claim dépendant ; elles sont des reconstructions interprétatives et disposent de preuves textuelles. Les liens de motivation ne sont pas convertis en implication.\n\n## Obligations de reconstruction ouvertes\n\n- Justifier le passage identité différentielle → neutralité ; dimensions de |dn| et |du|.\n- Établir la loi vitesse→Work et distinguer puissance, énergie et tâche.\n- Suivre la transmission coût→prix malgré le choix du prix reconnu p21.\n- Concilier travail accompli/restant et les signes des bilans.\n- Articuler M=g.T, g variable et dT+dM=0.\n- Examiner le rôle subjectif d’Utility et l’exclusion des critères humains.\n- Suivre la section Entropy p463 avant de conclure à un changement de sens.\n- Retrouver une réponse au volet environnemental exclu localement p29.\n\nAucune contradiction n’est ici déclarée démontrée. Aucun graphe sans cycle ne constitue une preuve de cohérence. Les claims isolés et cycles sont calculés par les tests et le rapport métrique. Les sections non lues rendent le graphe incomplet.')
    write('analysis/15_research_chapter_classification.md','# Dix chapitres candidats — INCOMPLETE\n\nLe découpage sépare mesure, supports, transmission aux prix, principes, lois, cycles, agrégation, énergie et applications. Il reflète davantage la structure annoncée que les huit axes initiaux, mais **sa supériorité analytique n’est pas encore établie** : les lois, cycles et développements tardifs restent à lire. Quatre chapitres n’ont encore aucun claim.\n\n'+'\n'.join(f"- {ch['id']} : {ch['title']}\n  Question : {ch['central_question']}\n  Lien racine : {ch['root_question_relation']}" for ch in chapters))
    counts=Counter(c for ch in chapters for c in ch['claims']); orphan=[c['id'] for c in claims if not counts[c['id']]]
    write('analysis/16_claim_chapter_coverage.md',f'# Matrice claims × chapitres\n\nClaims : {len(claims)} ; classés : {len(counts)} ; multi-chapitres : {sum(v>1 for v in counts.values())} ; orphelins : {len(orphan)}. CORE : {sum(c["criticality"]=="CORE" for c in claims)}.\n\nCe résultat concerne uniquement les claims reconstruits, et ne mesure pas la couverture de tout le raisonnement. Les attributions sont provisoires. Matrice détaillée : `analysis/data/claim_chapter_matrix.csv`.')
    write('analysis/17_core_claims.md','# Claims structurants — sélection provisoire\n\nCriticité : impact d’un changement du claim sur la reconstruction, pas degré de vérité. L’identification finale attend le reste du manuscrit.\n\n'+'\n'.join(f"- {c['id']} [{c['criticality']}] {c['statement']}" for c in core))
    hypotheses=[]
    for i,(number,hyp,ind,dep,data,test,expected,incompatible,confounds) in enumerate(HYPOTHESES,1):
        hypotheses.append(dict(id=f'HYP-{i:04}',claim_source=f'CPC-{number:04}',hypothesis=hyp,
            epistemic_status='HYPOTHESIS',interpretive=True,independent_variable=ind,observable=dep,
            necessary_data=data,available_data='Non inspectées dans cette reconstruction ; aucune reproduction déclarée.',
            test=test,expected_according_to_campergue=expected,incompatible_result=incompatible,
            confounders=confounds,interpretation_limits='Une conséquence compatible ne valide pas le système ; des définitions opérationnelles indépendantes sont nécessaires.',
            non_conclusion_criterion='Mesure indépendante, périmètre ou identification causale insuffisants.',status='PROPOSED_NOT_EXECUTED'))
    dump('analysis/data/hypotheses.json',hypotheses)
    for ch in chapters:
        ch['hypotheses']=[h['id'] for h in hypotheses if h['claim_source'] in ch['claims']]
        ch['potential_tests']=[h['test'] for h in hypotheses if h['id'] in ch['hypotheses']]
    dump('analysis/data/research_chapters.json',chapters)
    results=read('rag/evaluation/results.json')
    table='| Méthode | Recall@1 | Recall@3 | Recall@5 | MRR@5 |\n|---|---:|---:|---:|---:|\n'
    for method,r in results['methods'].items():
        table+='| '+method+' | '+' | '.join(f'{r["metrics"][k]:.4f}' for k in ['Recall@1','Recall@3','Recall@5','MRR'])+' |\n'
    write('analysis/18_rag_evaluation.md','# Évaluation retrieval réellement exécutée\n\n'+table+'\n66 questions de développement (60 anglais, 6 français), sur les pages examinées. Corpus indexé inchangé : 564 chunks, 3 documents. Aucune réponse de LLM. Pertinence = document ET page attendus ET passage exact normalisé. Recall est la proportion des pages attendues retrouvées ; MRR est tronqué à 5.\n\nBM25 (k1=1,2, b=0,75) est le meilleur sur ce jeu et devient le défaut ; legacy et cosinus TF-IDF restent disponibles. Aucun réglage de paramètres ni de synonymes sur les erreurs. Les embeddings ne sont pas implémentés : aucune pile vectorielle présente, benchmark lexical sans dépendance choisi à ce stade ; impossibilité matérielle non alléguée.\n\nLimites : pertinence non exhaustive (répétitions ailleurs possibles), questions construites à partir des claims, pas de jeu tenu à l’écart, faible échantillon français, chapitres tardifs non couverts. Les scores ne certifient pas la qualité sur les 562 pages. Résultats individuels et par langue dans `results.json`.\n\nLe texte intégral du chunk est maintenant renvoyé ; un préfixe arbitraire de 500 caractères pouvait cacher le passage justificatif. Les citations inter-pages restent représentées par plusieurs attentes paginées.')
    graph=read('analysis/data/argument_graph.json'); connected={e[k] for e in graph['edges'] for k in ['source','target']}
    french='\n## Limite linguistique observée\n\n'
    for method,run in results['methods'].items():
        french+=f"- {method} : Recall@5 français = {run['by_language']['fr']['Recall@5']:.4f}, anglais = {run['by_language']['en']['Recall@5']:.4f}.\n"
    p=ROOT/'analysis/18_rag_evaluation.md'
    p.write_text(p.read_text()+french+'\nLe choix BM25 améliore le score global mais ne résout pas les requêtes françaises. Aucun résultat français satisfaisant n’est revendiqué.\n')
    adjacency={n['id']:[] for n in graph['nodes']}
    for edge in graph['edges']: adjacency[edge['source']].append(edge['target'])
    active=[]; done=set(); cycles=[]
    def visit(node):
        if node in active:
            cycles.append(active[active.index(node):]+[node]); return
        if node in done: return
        active.append(node)
        for other in adjacency[node]: visit(other)
        active.pop(); done.add(node)
    for node in adjacency: visit(node)
    dump('analysis/data/graph_audit.json',dict(nodes=len(graph['nodes']),edges=len(graph['edges']),cycles=cycles,cycle_detection='DFS back edges over all relation types; not enumeration of all simple cycles.',orphans=[n['id'] for n in graph['nodes'] if n['id'] not in connected],scope='Partial interpretive graph; absence of edges does not prove logical independence.'))
    p=ROOT/'analysis/14_argument_reconstruction.md'
    p.write_text(p.read_text()+ '\n## Cycles conservés\n\n'+ '\n'.join('- '+' → '.join(c) for c in cycles)+ '\n\nCes deux retours associent DEPENDS_ON et QUALIFIES : utilité des banques malgré absence de création de Money ; restriction sur l’entropie dans l’analogie thermodynamique. Ils ne constituent pas à eux seuls une preuve de circularité démonstrative. Le sous-graphe des dépendances seul est acyclique dans le test exécuté.\n')
    snapshot=ROOT/'analysis/data/regression_snapshot.json'
    if not snapshot.exists():
        dump('analysis/data/regression_snapshot.json',dict(version=1,
            change_log=[dict(old_status=None,new_status='INCOMPLETE',evidence='Page coverage and phase 2 source citations.',justification='First reconstruction baseline; not a scientific verdict.')],
            invariants={i['id']:i['formulation'] for i in invariants},
            open_issues={i['id']:i['status'] for i in read('analysis/data/open_reconstruction_issues.json')},
            rag_metrics={m:r['metrics'] for m,r in results['methods'].items()}))

if __name__=='__main__': main()
