"""Versionable editorial question catalog; render tree BEFORE individual dossiers.
Run --tree first, then --dossiers. Existing divergent files require an explicit
archived revision: never overwrite an earlier question/conclusion silently.
"""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions'
# Stable NEW namespace: RQ-01.01 is distinct from legacy chapter question RQ-01-01.
FAMILIES=[
('01','Quel phénomène historique et environnemental faut-il expliquer ?'),
('02','Quel changement constitue une richesse nouvelle dans le périmètre retenu ?'),
('03','Economic Work fournit-il une grandeur économique définie et mesurable ?'),
('04','Sous quelles conditions une transformation améliore-t-elle la productivité ?'),
('05','Comment un gain productif se répartit-il entre coût, prix, qualité et profit ?'),
('06','Quand les variations de Cash et de sa valeur constituent-elles une variation de Money ?'),
('07','Comment les interactions entre agents créent-elles ou redistribuent-elles les gains ?'),
('08','À quelles conditions les relations locales deviennent-elles des relations agrégées ?'),
('09','Quel pont mesurable relie énergie physique et transformation économique ?'),
('10','Comment les gains disponibles deviennent-ils une abondance effectivement consommée ?'),
('11','Par quelles voies cette consommation produit-elle des dommages environnementaux ?'),
('12','Quels maillons permettraient une explication causale spécifique de la transition ?')]
# id | question | claims | prerequisite question IDs | classification
ROWS='''01.01|Le domaine annoncé couvre-t-il réellement les dommages environnementaux de la question racine ?|1,3,30,31,42,65| |BLOCKING,HIGH_VALUE
01.02|Quels indicateurs distinguent niveau de vie, revenu réel et bien-être dans la comparaison historique ?|1,48,65,127|01.01|BLOCKING,EMPIRICAL
01.03|La subsistance et l’abondance sont-elles des états mesurables, et la stabilité historique alléguée est-elle défendable ?|18,29,37|01.02|EMPIRICAL,OPEN
01.04|Quels dommages, territoires et horizons sont explicitement inclus ou laissés hors champ ?|31,120|01.01|EMPIRICAL,OPEN
02.01|La richesse définie comme Money exclut-elle patrimoine, services non marchands et richesse matérielle ?|48,65,6,49|01.01|BLOCKING,HIGH_VALUE,EASY_WIN
02.02|Quel critère distingue création nette, transfert, redistribution et simple réévaluation ?|7,9,14,22,24,100|02.01|BLOCKING,HIGH_VALUE
02.03|Le principe selon lequel seul Work crée un changement économique est-il une définition ou une restriction réfutable ?|9,22,30,36|02.02,03.01|HIGH_VALUE,FORMAL,OPEN
03.01|Quelle distinction textuelle sépare Economic Work, labour, effort physique et travail socialement utile ?|40,41,51,52,64,94,95,123|02.01|BLOCKING,HIGH_VALUE,EASY_WIN
03.02|Quelles conventions réconcilient T, dT, Work restant, travail accumulé et signes ?|23,40,45,62,63,121|03.01|BLOCKING,FORMAL,OPEN
03.03|Peut-on mesurer T, Force et complexité sans les reconstruire depuis les résultats à tester ?|39,43,44,52,54,66,68|03.01,03.02|BLOCKING,HIGH_VALUE,EMPIRICAL,FORMAL
03.04|La conservation ou destruction de Work est-elle une identité de bilan ou une hypothèse économique ?|23,39,43,121,122|03.02,03.03|FORMAL,HIGH_VALUE
04.01|Quand accélérer une tâche constante réduit-il effectivement les intrants nécessaires par produit ?|17,19,52,94,110,112|03.01|HIGH_VALUE,EMPIRICAL
04.02|Le résultat +78% découle-t-il d’une hypothèse quadratique particulière plutôt que d’une loi générale mesurée ?|35,96|03.03,04.01|HIGH_VALUE,FORMAL,EASY_WIN
04.03|Comment machines, complexité et substitution au salarié modifient-elles les gains et leurs coûts ?|54,66,105,106,111|04.01|EMPIRICAL,HIGH_VALUE
04.04|Quelles contraintes et conventions de signe rendent les rendements et optima des cycles définis ?|32,33,38,101,102,103,104,108|03.02,03.04|FORMAL,HIGH_VALUE,OPEN
05.01|Quelles conditions distinguent baisse de prix, prix maintenu et gain retenu après baisse du coût ?|19,20,21,97,98,105,110|04.01|BLOCKING,HIGH_VALUE,EMPIRICAL
05.02|Comment concurrence, négociation, monopole et brevet répartissent-ils productivité et rente ?|21,60,113,124,125|05.01,02.02|EMPIRICAL,HIGH_VALUE
05.03|Utility peut-elle être mesurée indépendamment du prix et de la quantité pour comparer les scénarios ?|34,55,56,57,58,59,76,77,78,79,113|02.01|BLOCKING,HIGH_VALUE,EMPIRICAL
06.01|Quelles unités et frontières distinguent Cash, Money, n, u et pouvoir d’achat ?|2,10,11,41,46,50,53|02.01|BLOCKING,HIGH_VALUE,EASY_WIN
06.02|Dans quels scénarios M=n·u s’accompagne-t-il d’une compensation immédiate, différée ou absente ?|5,12,25,26,69,70,71,72,73,74,75,80,81,82,83,86,88,90|06.01|BLOCKING,HIGH_VALUE,FORMAL
06.03|Comment création, destruction et émission accompagnatrice se distinguent-elles sans double compter le gain ?|15,16,71,72,73,99,107|06.01,05.01,05.03|HIGH_VALUE,FORMAL
06.04|Après traduction du vocabulaire, quelle restriction sur le crédit bancaire reste réellement contestable ?|13,14,27,28,50,85|06.02,02.02|EMPIRICAL,HIGH_VALUE
07.01|Quels bilans distinguent les rôles du producteur, salarié, consommateur, État et intermédiaire ?|7,60,61,62,63,108,123|02.02,03.02|FORMAL,HIGH_VALUE
07.02|Une transaction ou décision non neutre entre acteurs implique-t-elle une création globale ?|24,84,87,93,100,124,125|07.01,06.03|BLOCKING,HIGH_VALUE,FORMAL
07.03|Quels bouclages de crédit, intérêt et profit exigent Work supplémentaire, transfert ou dévaluation ?|38,91,92,101,102,103,104|07.01,06.02,04.04|FORMAL,HIGH_VALUE
08.01|Quelles unités, frontières et pondérations autorisent l’addition des contributions sans double compte ?|37,89,111,114,126|03.03,06.01,07.01|BLOCKING,FORMAL,HIGH_VALUE
08.02|Un grand nombre de produits suffit-il à stabiliser K malgré des coefficients et compositions hétérogènes ?|43,44,109,116,117,118|08.01,05.03|HIGH_VALUE,FORMAL,EMPIRICAL
08.03|Les potentiels locaux sont-ils des fonctions d’état intégrables et sommables sous leurs contraintes ?|4,47,115,116|03.02,03.04|FORMAL,OPEN
08.04|Le champ labour-prix et les normalisations locales/globales sont-ils invariants aux changements d’unités ?|89,112,116,126|08.01|FORMAL,HIGH_VALUE
09.01|L’énergie bon marché est-elle une condition nécessaire, suffisante ou seulement favorable à la productivité ?|17,18,29,105,106|04.01,01.03|EMPIRICAL,HIGH_VALUE
09.02|Quel critère et quelle conversion séparent énergie consommée, travail physique utile et Work économique ?|3,17,39,42,67,119,122|03.03,05.03|BLOCKING,HIGH_VALUE,FORMAL
09.03|GDP=K·W est-il testable indépendamment du PIB et avec des rendements, pertes et frontières explicites ?|67,108,117,118,119|09.02,08.02|EMPIRICAL,HIGH_VALUE
10.01|Sous quelles conditions un gain de prix améliore-t-il le pouvoir d’achat réel plutôt qu’un simple indicateur nominal ?|15,16,53,76,77,78,79|05.01,05.03,06.01|EMPIRICAL,HIGH_VALUE
10.02|Quelle fraction du gain est épargnée, dépensée plus tard, consommée davantage ou affectée à la qualité ?|8,84,99,127|10.01,07.02|BLOCKING,HIGH_VALUE,EMPIRICAL
10.03|L’abondance peut-elle progresser sans augmentation des flux physiques d’énergie et de matière ?|18,65,118,127|10.02,09.03|EMPIRICAL,HIGH_VALUE,OPEN
11.01|Quels maillons sourcés relient gains productifs, flux physiques et dommages, et lesquels restent manquants ?|1,18,31,120,127|10.02,09.02,01.04|BLOCKING,HIGH_VALUE,EMPIRICAL
11.02|L’usage du gain produit-il un rebond direct, indirect ou global, et dans quelles limites ?|84,99,120,127|10.02,09.01|EMPIRICAL,HIGH_VALUE
11.03|Quelle empreinte marginale attribuer aux matières, transports, énergie et externalités du panier supplémentaire ?|18,31,120,127|11.01,11.02|EMPIRICAL,OPEN
12.01|Quelles observations départageraient Campergue des explications concurrentes à conditions comparables ?|3,68,117,118,119|03.03,05.01,08.02,09.02|HIGH_VALUE,EMPIRICAL,FORMAL
12.02|Quels mécanismes établis ou postulés sont nécessaires, suffisants ou substituables dans la transition historique ?|1,9,18,29,118,120|01.03,09.01,10.03,11.01|HIGH_VALUE,OPEN
12.03|Quelle réponse limitée à la question racine résiste aux lacunes, contre-exemples et changements de périmètre ?|1,3,31,48,120,127|12.01,12.02,11.03|HIGH_VALUE,OPEN'''

def safe_write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=text.encode('utf-8'):raise RuntimeError(f'Explicit archived revision required: {path}')
    else:path.write_text(text)

def catalog():
    claims={c['id']:c for c in map(json.loads,(ROOT/'analysis/data/claims.jsonl').read_text().splitlines())}
    chapters=json.loads((ROOT/'analysis/data/research_chapters.json').read_text())
    qs=[]
    for line in ROWS.splitlines():
        id,title,ids,deps,tags=line.split('|')
        tags=tags.split(',');ids=[f'CPC-{int(i):04}' for i in ids.split(',')]
        qs.append(dict(id='RQ-'+id,question=title,parent='RQ-'+id[:2],level=2,
            importance='FOUNDATIONAL' if 'BLOCKING' in tags else 'CORE' if 'HIGH_VALUE' in tags else 'MAJOR',
            claims=ids,dependencies=['RQ-'+i for i in deps.strip().split(',') if i],classification=tags,
            status='OPEN',first_pass=False,testability=['FORMAL_TEST' if t=='FORMAL' else 'EMPIRICAL_TEST' for t in tags if t in ['FORMAL','EMPIRICAL']] or ['CONSISTENCY_TEST']))
    for id,title in FAMILIES:
        children=[q for q in qs if q['parent']=='RQ-'+id]
        qs.append(dict(id='RQ-'+id,question=title,parent='RQ-ROOT',level=1,importance='CORE',
            claims=sorted({c for q in children for c in q['claims']}),dependencies=[q['id'] for q in children],
            classification=['HIGH_VALUE'],status='OPEN',first_pass=False,testability=['COMPARATIVE_TEST']))
    source=claims['CPC-0001']['source']
    qs.append(dict(id='RQ-ROOT',question=source['quotation'],parent=None,level=0,importance='FOUNDATIONAL',
        claims=['CPC-0001','CPC-0003','CPC-0031','CPC-0120'],dependencies=['RQ-12.03'],classification=['HIGH_VALUE'],
        status='OPEN',first_pass=False,testability=['COMPARATIVE_TEST'],source=source,
        associated_sentence='This essay should only be understood as a proposed answer to this question.',associated_page=3))
    for q in qs:
        q['chapters']=[c['id'] for c in chapters if set(q['claims'])&set(c['claims'])]
        q['concepts']=sorted({x for cid in q['claims'] for x in claims[cid]['concepts']})
        q['scope']=q['question']+' Périmètre : passages et conditions référencés, sans verdict global.'
        q['out_of_scope']='Validation de la théorie entière, causalité déduite d’une corrélation ou équivalence automatique des proxies.'
        q['interpretive']=True
        q['corpus_completeness']='TARGETED_EXISTING_EVIDENCE_NOT_EXHAUSTIVE'
    return sorted(qs,key=lambda q:('0' if q['id']=='RQ-ROOT' else q['id'])),claims

def tree(qs):
    lines=['# Arbre de recherche — version initiale','',
        '53 questions hors racine : 12 de niveau1 et41 de niveau2. Les familles sont des problèmes de synthèse ; elles ne reprennent pas les dix chapitres. Leur nombre résulte de41 questions opérationnelles et12 problèmes auxquels leurs réponses contribuent.','',
        'L’arbre a été écrit AVANT les dossiers. Son état initial OPEN est conservé dans history/001_initial_questions.md ; les statuts ci-dessous sont ceux de la première passe, synchronisés avec le graphe et les dossiers.','',
        'RQ-ROOT : citation du manuscrit, pages PDF2–3 ; phrase associée page3. Les autres questions sont RESEARCH_INTERPRETATION, jamais des citations inventées.','',
        'Les anciens RQ-01-01…RQ-10-01 restent dans analysis/data/research_questions.json. Les nouveaux RQ-01.01 utilisent un point et un espace de noms distinct ; aucune suppression ni réaffectation implicite.','']
    for q in qs:
        lines += [('## ' if q['level']<2 else '### ')+q['id']+' — '+q['question'],'',
            f"Parent : {q['parent'] or 'aucun'} ; importance : {q['importance']} ; statut : {q['status']}.",
            f"[Dossier]({q['id']}/README.md)",
            'Claims : '+', '.join(q['claims'])+'.', 'Chapitres : '+', '.join(q['chapters'])+'.',
            'Dépendances : '+(', '.join(q['dependencies']) or 'aucune prerequisite dans cette décomposition')+'.',
            'Testabilité : '+', '.join(q['testability'])+'. Classification : '+', '.join(q['classification'])+'.','']
    safe_write(OUT/'questions.md','\n'.join(lines)+'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--tree',action='store_true');p.add_argument('--dossiers',action='store_true');a=p.parse_args()
    qs,claims=catalog()
    if a.tree:
        graph=OUT/'question_graph.json'
        tree(json.loads(graph.read_text())['nodes'] if graph.exists() else qs)
    if a.dossiers:
        assert (OUT/'questions.md').exists(),'Write tree before dossiers'
        from research_question_dossiers import render
        render(qs,claims,safe_write)
    print(f'Catalog: {len(qs)-1} questions + root')
if __name__=='__main__':main()
