"""Rebuild derived research artifacts from explicitly reviewed editorial records.

No sentence mining or keyword match constitutes analytical reading.
Run from any directory; Python standard library only.
"""
import csv
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = 'Reflections_PierreCampergue.pdf'
SHA = '7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827'

def norm(text):
    return ' '.join(text.split())

def dump(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def archive():
    for path in ['analysis/data/claims.jsonl', 'analysis/data/concepts.json',
                 'analysis/data/argument_graph.json', 'analysis/02_root_question.md',
                 'rag/query.py', 'rag/build_index.py', 'rag/index/manifest.json', 'verify.sh']:
        dest = ROOT / 'analysis/history/phase1' / path
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, dest)

# page, type, criticality, concept IDs, French reconstruction, literal anchor, dependencies.
# IDs preserve the three original propositions; references use record numbers.
RECORDS = [
([2,3], 'OPEN_QUESTION', 'CORE', 'growth environment living', 'Comprendre le passage de la subsistance à l’abondance et les dommages environnementaux associés à la hausse du niveau de vie.', 'The key question is therefore to understand how the increase in living standards has led to these environmental damages, or how we have moved from a subsistence society to an affluent society.', ''),
(3, 'CONCEPTUAL', 'MAJOR', 'unit money', 'La valeur de l’unité monétaire varie dans le temps.', 'the economy dispenses with this constraint and appropriates the prerogative to modify the value of the unit over time.', ''),
(2, 'ANALOGICAL', 'CORE', 'work money energy transformation', 'L’étude compare la transformation du travail en monnaie à celle de la chaleur en travail, en les distinguant.', 'similar, but not identical, to the energy transformations of heat into work.', ''),
(4, 'ASSUMPTION', 'MAJOR', 'transformation', 'Le formalisme suppose des comportements suffisamment lents et réguliers.', 'sufficiently slow and regular behaviours of systems of appropriately defined variables.', ''),
(12, 'HYPOTHESIS', 'CORE', 'unit money wealth accounting', 'Changer le nombre d’unités monétaires ne change pas la richesse globale du système.', 'any variation in the number of monetary units can only derive from a human will and induces absolutely no overall change in the wealth of the system.', '9 11'),
(12, 'DEFINITION', 'MAJOR', 'product production', 'Product englobe biens et services produits par l’être humain.', 'the “Product” is defined as everything that is manufactured, elabourated, realized, accomplished, by Human and can therefore be a good or a service.', ''),
(13, 'CONCEPTUAL', 'MAJOR', 'creation distribution use', 'La création et l’usage relèvent des lois naturelles ; la distribution relève de décisions humaines.', 'points 1 (creation) and 3 (use) undeniably belong to the “Natural Sciences” and that point 2 (distribution) is systematically related to the “Human Sciences”.', ''),
(13, 'CONCEPTUAL', 'SUPPORTING', 'creation use production', 'La production précède la consommation.', 'production being, of course, always prior to consumption.', ''),
(14, 'AXIOM', 'CORE', 'work transformation', 'Seul le travail engendre un changement.', 'only work generates change, all other criteria are inoperative.', ''),
(15, 'DEFINITION', 'CORE', 'money unit', 'Money est défini comme le nombre d’unités multiplié par la valeur de l’unité.', 'M=n.u', ''),
(15, 'DERIVED', 'MAJOR', 'money unit', 'Le différentiel du produit M=n.u est dM=n.du+u.dn.', 'dM=n.du+u.dn', '10'),
(17, 'HYPOTHESIS', 'CORE', 'money unit', 'Toute variation du nombre d’unités entraîne une variation inverse de leur valeur, empêchant de créer Money.', 'any variation in the number of monetary units automatically and inexorably generates the same inverse variation in the value of the unit, implying the impossibility of creating money.', '9 10'),
(18, 'DERIVED', 'MAJOR', 'money unit accounting', 'Le crédit non couvert par des dépôts ne crée pas Money au sens de l’auteur.', 'the increase in the number of monetary units (granting of a loan not covered by deposits) doesn’t create money', '5 12'),
(18, 'DERIVED', 'MAJOR', 'distribution accounting wealth', 'Sans dépense de Work, une politique ne fait que redistribuer Money dans le système.', 'Any economic policy measure that doesn’t involve Work expenditure leaves the existing quantity of Money in the system constant', '5 9'),
(19, 'DEFINITION', 'CORE', 'money price purchasing', 'Money créé désigne le supplément détenu par le consommateur après une baisse de prix.', 'The Money is what a consumer holds in addition after a price drop.', ''),
(19, 'MECHANISM', 'CORE', 'work productivity price unit money purchasing', 'Le mécanisme proposé relie travail supplémentaire, productivité, baisse de prix, hausse de l’unité et supplément de Money.', 'Additional work of the supplier ⇒ increased productivity ⇒ price decline ⇒ increase of monetary unit ⇒ creation of money ⇒ additional money of the consumer.', '15 17'),
(19, 'HYPOTHESIS', 'CORE', 'work productivity energy', 'Une hausse de productivité exige nécessairement un travail supplémentaire assimilé ici à une énergie.', 'this increase in productivity necessarily requires the execution of additional Work', ''),
(20, 'HYPOTHESIS', 'MAJOR', 'energy work growth living', 'Les sources artificielles d’énergie peu coûteuses auraient permis le passage à l’abondance.', "It seems that it's the availability of these low-cost artificial sources of energy over the last two centuries that has made the transition possible:", '16 17'),
(20, 'DEFINITION', 'MAJOR', 'productive unproductive work price', 'Le travail productif est défini par sa capacité à réduire le coût de revient.', 'Work (energy) that allows a reduction in the cost price can be described as “productive Work”, while work that doesn’t allow a reduction in price can be defined as “unproductive work”.', ''),
(20, 'CONCEPTUAL', 'MAJOR', 'cost price accounting', 'Une baisse du coût peut coexister avec un prix de vente constant.', 'if the selling price is kept constant despite this drop in cost price', ''),
(21, 'CONCEPTUAL', 'MAJOR', 'price cost', 'Le prix de vente relève du choix de l’entrepreneur sous contraintes de concurrence et de réglementation.', 'They are the sole judge and person responsible for selling prices, but always subject to the external constraints (competition, regulations, etc.) to which they are subject.', ''),
(22, 'HYPOTHESIS', 'CORE', 'work money transformation', 'L’auteur postule la transformation du travail supplémentaire du fournisseur en Money supplémentaire du consommateur.', 'SUPPLEMENTARY WORK performed by the supplier is TRANSFORMED into SUPPLEMENTARY MONEY held by the consumer.', '16'),
(22, 'AXIOM', 'CORE', 'remaining work money transformation', 'Dans un système isolé, la baisse du travail restant à faire compense la hausse de Money créé.', 'the decrease (destruction) of the Work to be done is compensated by the increase (creation) of the Money generated and vice versa', ''),
(22, 'CONCEPTUAL', 'MAJOR', 'transformation accounting', 'Une transformation physique est distinguée du flux comptable.', 'a transformation, which is relative to physics, and no longer a flow, which is relative to accounting', ''),
(24, 'HYPOTHESIS', 'SUPPORTING', 'inflation unit purchasing', 'Dans le cas inflationniste décrit, le consommateur s’enrichit si la valeur unitaire baisse moins que le nombre d’unités ne croît.', 'because the value decreases less as the number increases, the consumer gets richer.', '10'),
(25, 'HYPOTHESIS', 'SUPPORTING', 'deflation unit purchasing', 'Dans le cas déflationniste décrit, la baisse du nombre d’unités domine leur appréciation et appauvrit le consommateur.', 'because the value increases less as the number decreases, the consumer becomes poorer.', '10'),
(26, 'NORMATIVE', 'SUPPORTING', 'inflation deflation distribution', 'L’auteur préconise un équilibre entre politiques d’offre et de demande.', 'only the balance between supply and demand policy is to be sought', ''),
(28, 'CONCEPTUAL', 'SUPPORTING', 'accounting money', 'L’incapacité attribuée aux banques à créer Money n’implique pas leur inutilité sociale.', "it's never written here that bankers, in their actions, cannot be useful for the smooth running of society", '13'),
(29, 'EMPIRICAL', 'MAJOR', 'living energy growth', 'Le manuscrit affirme un niveau de vie constant du Néolithique au XVIIIe siècle sous sources naturelles limitées.', 'purchasing power and, incidentally, the standard of living remained constant from the Neolithic period until the 18th century.', ''),
(29, 'METHODOLOGICAL', 'MAJOR', 'creation money', 'La recherche de la genèse de Money exclut selon l’auteur toute référence à l’être humain.', 'any study whose aim is solely the creation of Money must be free of any reference to the Human Being.', '7'),
(29, 'METHODOLOGICAL', 'MAJOR', 'environment energy', 'Le préambule limite explicitement son propos économique en excluant les répercussions environnementales.', 'in no way about the effects, impacts, repercussions or other environmental impacts of the plethora of energy', ''),
(31, 'AXIOM', 'CORE', 'work money constraints', 'L’économie de travail augmente vers un maximum sous contraintes externes.', 'the Economy of Work naturally always increases towards a maximum, limited by external constraints', ''),
(31, 'AXIOM', 'CORE', 'money constraints', 'L’économie de Money augmente vers un maximum sous contraintes externes.', 'the Economy of Money naturally always increases towards a maximum, limited by external constraints.', ''),
(31, 'AXIOM', 'MAJOR', 'barter utility money', 'Le troc est présenté comme un échange sans Money entre produits d’utilités égales.', 'in a barter, there is no Money exchanged.', ''),
(32, 'HYPOTHESIS', 'CORE', 'work productivity energy', 'L’exemple 8 heures vers 6 heures prétend nécessiter environ 78 % de travail supplémentaire.', 'The second hypothesis therefore requires more Work than the first (about 78% more).', '17'),
(33, 'CONCEPTUAL', 'MAJOR', 'work product price', 'La variation de Work servirait exclusivement à varier le prix, non à fabriquer le produit.', 'a WORK VARIATION is never used to manufacture a Product but exclusively to VARY its price.', '17'),
(34, 'DEFINITION', 'MAJOR', 'supply production', 'L’offre est définie comme un nombre de cycles de fabrication par unité de temps.', 'The offer of a Product can be defined as the number of times the manufacturing cycle is performed per unit of time.', ''),
(34, 'ANALOGICAL', 'MAJOR', 'cycle transformation', 'Le cycle économique est mis en correspondance avec quatre étapes thermodynamiques.', 'the steps of the thermodynamic cycle in accordance:', '3'),
(35, 'ASSUMPTION', 'CORE', 'work money energy', 'Economic Work et Money sont posés comme deux formes d’énergie économique.', 'Economic Work and Money are logically considered two different forms of Economic Energy', ''),
(35, 'METHODOLOGICAL', 'CORE', 'remaining work', 'Le modèle doit compter le travail à effectuer et non le travail déjà effectué.', 'only the Work to be done must be taken into account and not the Work performed.', ''),
(35, 'DEFINITION', 'CORE', 'product work cash money', 'Product supporte Work et Cash supporte Money.', 'the Product as the vector-support of the economic Work,', ''),
(36, 'METHODOLOGICAL', 'MAJOR', 'entropy energy', 'L’emploi du formalisme thermodynamique exclut ici les variables physiques et notamment l’entropie.', "entropy doesn’t have to be used in this context.", '3'),
(36, 'AXIOM', 'CORE', 'money work coefficient', 'Le principe d’équivalence est écrit M=g.T.', 'M=g.T', ''),
(36, 'ASSUMPTION', 'MAJOR', 'coefficient', 'La constance du coefficient g n’est pas garantie en économie.', "the transformation coefficient g should be a constant, which isn't necessarily the case in Economics", ''),
(36, 'DEFINITION', 'CORE', 'money force price', 'Le différentiel de Money est défini par dM=-F.dp.', 'dM=−F.dp', ''),
(184, 'DEFINITION', 'CORE', 'cash money', 'Money est la valeur de Cash, lequel en est le support.', 'Money as the value of Cash,', ''),
(185, 'ASSUMPTION', 'MAJOR', 'transformation price', 'Les variations doivent être assez petites et proches dans le temps pour être traitées comme continues.', 'small enough and close enough in time to be judged as continuous.', ''),
(185, 'DEFINITION', 'CORE', 'wealth money', 'Wealth désigne exclusivement la quantité de Money, sans inclure les actifs patrimoniaux.', 'It never takes into account the assets that an economic agent', ''),
(187, 'DEFINITION', 'MAJOR', 'product work', 'Product est défini par sa capacité à être acquis, transformé ou vendu et comme support de Work.', 'the Product represents any object, merchandise, product, good or service that an economic agent', ''),
(187, 'DEFINITION', 'MAJOR', 'cash money accounting', 'Une ligne de crédit bancaire est Cash, pas Money dans ce vocabulaire.', 'the inscription of a line of bank credit should not be considered as Money but only as Cash.', '46'),
([187,188], 'DEFINITION', 'CORE', 'labour work', 'Labour désigne la tâche, constante pour un produit et une méthode de fabrication donnés.', 'labour (l) must be understood as the thing to be done, the task, the job to be done. It is constant for a given Product and manufacturing method.', ''),
(188, 'DEFINITION', 'CORE', 'work labour productivity force', 'Pour une tâche constante, Work dépend de sa vitesse d’exécution.', 'for a constant labour, the Work varies according to its speed of execution.', ''),
(188, 'DEFINITION', 'CORE', 'money cash', 'Money mesure la valeur de Cash ; cette valeur varie dans le temps et selon le lieu.', 'the Money (M) is defined as the measure of the value of Cash', ''),
(189, 'DEFINITION', 'MAJOR', 'complexity product labour', 'La complexité désigne l’inertie du produit face au changement de vitesse d’exécution de la tâche.', 'the complexity (c) must be understood as the inertia that a Product presents at the change in speed of execution of the labour.', ''),
(189, 'DEFINITION', 'MAJOR', 'utility product', 'L’utilité peut être objective, subjective, exacte ou erronée et concerne les échanges.', 'which can be both objective and subjective, accurate and erroneous', ''),
(189, 'METHODOLOGICAL', 'MAJOR', 'utility', 'Le manuscrit écarte l’utilité marginale et revendique le sens de Walras.', 'Utility should be taken, in this study, in the sense of Walras', ''),
(190, 'CONCEPTUAL', 'SUPPORTING', 'utility product', 'L’utilité varie selon l’agent et le moment ; l’exemple de l’air distingue abondance et manque.', 'this Utility is variable according to the agents considered', '55'),
(191, 'HYPOTHESIS', 'SUPPORTING', 'utility price', 'Le manuscrit déduit une absence de baisse du prix des œuvres d’art de leur utilité presque constante.', 'since its Utility is almost constant over time, its price will not decrease.', '55'),
(192, 'HYPOTHESIS', 'MAJOR', 'utility cash purchasing', 'L’utilité de Cash est donnée comme d’autant plus élevée que le revenu est bas.', "the lower an agent's income is, the higher the Utility of the Cash will be.", ''),
(192, 'DEFINITION', 'MAJOR', 'agent utility', 'Le terme manufacturer inclut fournisseur et revendeur, même sans modification du produit.', "A manufacturer can therefore be a wholesaler, a trader, etc., although it doesn't necessarily modify a Product.", ''),
(193, 'DEFINITION', 'MAJOR', 'agent transformation', 'Le Transformer est interne au système ; Seller et Acquirer sont externes.', 'the Transformer is considered to be placed within the system,', ''),
(193, 'CONCEPTUAL', 'MAJOR', 'agent utility', 'Le signe des variations d’utilité dépend de la position de l’observateur dans la chaîne.', 'this is a function of the position of the observer', '55 61'),
(194, 'DEFINITION', 'MAJOR', 'transformation agent', 'Les flux entrants du Transformer sont comptés positivement, les sortants négativement.', 'everything that enters the system, that is to say, everything that the Transformer receives will be counted positively;', '61'),
]

# Explicit concept records: contextual mentions do not become formal definitions.
CONCEPTS = [
('supply','supply',['offer'],37,'Définie ici comme cycles de fabrication par unité de temps ; pas une courbe de marché.'),
('work','Economic Work',['Work','T'],52, 'Ne pas confondre travail mécanique W, Work T, travail accompli et restant.'),
('labour','labour',['l','task'],51,'Tâche constante seulement à produit et méthode donnés.'),
('money','Money',['M'],53,'Pages 19 et 188 : supplément après baisse de prix versus mesure de valeur de Cash ; articulation à poursuivre.'),
('cash','Cash',[],50,'Inclut supports physiques et inscription de crédit ; ne signifie pas seulement espèces.'),
('product','Product',[],49,'Page 12 insiste sur fabrication humaine ; page 187 inclut matières premières et échangeabilité.'),
('production','production',['manufacturing'],8,'Emploi contextuel ; définition indépendante non établie ici.'),
('productivity','productivity',['speed of production'],17,'Lien nécessaire à énergie supplémentaire affirmé, pas démontré par le calcul de prix.'),
('price','price',['selling price','p'],21,'Prix de vente et coût de revient doivent être distingués.'),
('cost','cost price',[],20,'Emploi contextuel du coût de revient.'),
('unit','value of the monetary unit',['u'],10,'Panier de référence et dimensions de n et u à spécifier.'),
('purchasing','purchasing power',[],15,'Associé au supplément de biens accessible après baisse de prix.'),
('creation','creation',[],7,'Distinction de portée revendiquée entre physique et décision humaine.'),
('distribution','distribution',[],7,'Redistribution interne, à distinguer de variation globale.'),
('use','use',['consumption'],8,'Postérieur à la création dans le préambule.'),
('energy','energy',['Economic Energy'],39,'Les formes économiques sont postulées distinctes des grandeurs physiques.'),
('wealth','wealth',['Rm','monetary wealth'],48,'Exclusion explicite du patrimoine p185 ; tension avec money supply à préciser.'),
('growth','growth',[],18,'Terme de programme historique ; pas de définition formelle examinée.'),
('living','standard of living',['subsistence society','affluent society'],29,'États historiques invoqués sans indicateur fixé ici.'),
('environment','environmental damage',[],31,'Question racine p2–3, mais préambule exclut les impacts p29.'),
('transformation','transformation',[],24,'Différente du transfert comptable dans le passage examiné.'),
('productive','productive Work',[],19,'Critère de réduction de coût ; ne pas étendre sans source à toute productive operation.'),
('unproductive','unproductive work',[],19,'Absence de réduction de prix dans la définition p20.'),
('accounting','accounting flow',['accounting procedure'],24,'N’implique pas une création globale selon l’auteur.'),
('remaining','Work to be done',[],40,'À distinguer de Work performed ; distinction nécessaire au signe de conservation.'),
('constraints','external constraints',[],32,'Limites des principes d’économie de Work et Money.'),
('barter','barter',[],34,'Principe d’égalité des utilités affirmé ; pas un résultat empirique établi.'),
('utility','Utility',['UP','UA'],55,'Relative à l’agent ; marginal utility explicitement exclue.'),
('cycle','cycle',[],38,'Quatre étapes analogiques ; calculs ultérieurs non examinés.'),
('entropy','entropy',[],42,'Exclue dans le résumé p36 ; section Entropy annoncée p463 à examiner.'),
('coefficient','transformation coefficient',['g'],44,'Constance conditionnelle ; dimensions requises pour conservation.'),
('force','Force',['F'],45,'Pression consommateur ; opérationnalisation encore requise.'),
('complexity','complexity',['c'],54,'Inertie économique par rapport à la vitesse de la tâche.'),
('agent','economic agent',['Seller','Transformer','Acquirer','manufacturer'],60,'Rôles et observateur ; manufacturer ne signifie pas nécessairement fabrication.'),
]

CHAPTERS = [
('Origine de la richesse et périmètre explicatif', 'Comment la question historique est-elle traduite en un problème de richesse monétaire ?', [[1,4],[12,37],[184,186]], ['growth','living','environment','wealth'], [1,3,7,8,18,28,29,30,31,48]),
('Mesure monétaire et neutralité du nombre d’unités', 'Quelles hypothèses s’ajoutent à M=n.u pour obtenir la neutralité monétaire ?', [[12,30],[168,184]], ['money','unit','inflation','deflation'], [2,5,10,11,12,13,14,25,26,27]),
('Objets, supports, tâches et points de vue', 'Quelles grandeurs et quels observateurs rendent les définitions cohérentes ?', [[184,194]], ['product','cash','labour','work','agent','utility','complexity'], [6,41,46,49,50,51,52,53,54,55,56,57,59,60,61,62,63]),
('Productivité, énergie et transmission aux prix', 'Quand une accélération de production exige-t-elle plus de Work et réduit-elle le prix payé ?', [[19,22],[32,34],[194,215]], ['productivity','work','price','cost','productive'], [9,15,16,17,19,20,21,35,36,58]),
('Principes, conservation et domaine du formalisme', 'Quelles hypothèses permettent les équivalences et la conservation économiques ?', [[30,37],[216,257]], ['transformation','remaining','coefficient','constraints'], [4,22,23,24,32,33,34,39,40,42,43,44,45,47]),
('Lois constitutives et transformations élémentaires', 'Quelles lois relient les variables avant le calcul des cycles ?', [[258,344]], ['transformation','utility','complexity'], []),
('Cycles, création et rendements', 'Sous quelles conditions un cycle crée-t-il Money ou Work ?', [[345,401]], ['cycle','money','work','supply'], [37,38]),
('Agrégation, potentiels et coefficients', 'Comment le formalisme local est-il agrégé et différencié ?', [[402,453],[536,559]], ['coefficient','supply','utility'], []),
('Couplage énergétique et conservation', 'Quel lien mesurable est proposé entre chaleur consommée et monnaie créée ?', [[454,472]], ['energy','entropy','money'], []),
('Agents, marchés et applications', 'Comment les résultats changent-ils selon les agents et les structures de marché ?', [[473,535],[560,562]], ['agent','price','cycle'], []),
]

def main():
    state=ROOT/'analysis/data/phase2_progress.json'
    if state.exists() and json.loads(state.read_text()).get('status')=='SUFFICIENT_FOR_ITERATIVE_RESEARCH':
        raise SystemExit('Historical generator disabled: it would overwrite later research. Use iteration scripts and preserve edits.')
    archive()
    pages = {r['page_pdf']: r['text'] for r in map(json.loads, (ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    assert sorted(pages) == list(range(1,563))
    assert hashlib.sha256((ROOT/DOC).read_bytes()).hexdigest() == SHA
    # Only remove a standalone leading printed page number for multi-page citations.
    texts = {p: norm(re.sub(r'^\s*'+str(p)+r'\s*\n', '', t)) for p,t in pages.items()}
    claims = []
    for number, (pp, typ, crit, concepts, statement, quotation, deps) in enumerate(RECORDS,1):
        pp = pp if isinstance(pp,list) else [pp]
        assert quotation in ' '.join(texts[p] for p in pp), (number,pp,quotation)
        claims.append(dict(id=f'CPC-{number:04}', statement=statement,
            source=dict(document=DOC, page=pp[0], pages=pp, quotation=quotation, normalization='whitespace; standalone leading page numbers removed'),
            source_document=DOC, page=pp[0], quotation=quotation, type=typ,
            epistemic_status='SOURCE', interpretive=True,
            concepts=concepts.split(), depends_on=[f'CPC-{int(n):04}' for n in deps.split()],
            supports=[], contradicts=[], criticality=crit,
            testability='TO_OPERATIONALIZE' if typ in ['HYPOTHESIS','EMPIRICAL','MECHANISM'] else 'CONCEPTUAL_OR_FORMAL_REVIEW',
            root_question_relevance='Étudier les conditions de création de richesse et le lien proposé avec le développement ; aucune validation causale déduite.',
            interpretation_notes='Énoncé français : reconstruction éditoriale. Citation anglaise : source. Liens logiques proposés par l’analyste, à contrôler dans les développements.',
            confidence_in_reconstruction=0.85))
    (ROOT/'analysis/data/claims.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims))
    concepts=[]
    # Terms encountered as categories in monetary developments.
    for key, term, variants, number, ambiguity in CONCEPTS + [('inflation','inflation',[],25,'Sens du cas 2a1, pas une substitution automatique au sens courant.'),('deflation','deflation',[],26,'Sens du cas 2b1.')]:
        c=claims[number-1]
        concepts.append(dict(id=key,preferred_term=term,variants=variants,
            definition_by_campergue=c['statement'] if c['type']=='DEFINITION' else None,
            contextual_use=c['statement'], definition_status='SOURCE_LINKED_INTERPRETATION' if c['type']=='DEFINITION' else 'CONTEXTUAL_NOT_FORMALIZED',
            source_pages=c['source']['pages'], quotations=[c['source']],
            related_terms=[x for x in c['concepts'] if x!=key],distinguished_from=[],depends_on=[],
            used_in_claims=[x['id'] for x in claims if key in x['concepts']],
            ambiguities=[ambiguity], definition_changes=[], full_manuscript_review=False))
    for a,b in [('cash','money'),('labour','work'),('creation','distribution'),('accounting','transformation'),('price','cost')]:
        next(c for c in concepts if c['id']==a)['distinguished_from'].append(b)
        next(c for c in concepts if c['id']==b)['distinguished_from'].append(a)
    dump('analysis/data/concepts.json',concepts)
    invariants=[]
    for i,(a,b,nums,importance) in enumerate([
        ('cash','money',[46,50,53],'Ne pas assimiler une émission de Cash à la création de Money définie par l’auteur.'),
        ('labour','work',[51,52],'Ne pas mesurer T par des heures de labour sans reconstruire la relation.'),
        ('creation','distribution',[7,14],'Conserver distinction entre variation globale et redistribution interne.'),
        ('accounting','transformation',[22,24],'Un déplacement comptable ne doit pas être étiqueté transformation productive sans passage source.'),
        ('price','cost',[20,21],'Une baisse de coût ne garantit pas la même baisse du prix de vente.'),
        ('remaining','work',[23,40],'Conserver la distinction travail restant / travail accompli dans les bilans.'),
        ('product','work',[41,49],'Ne pas confondre support et grandeur supportée.'),
        ('energy','entropy',[3,42],'L’analogie ne rend pas identiques variables économiques et physiques.')],1):
        invariants.append(dict(id=f'INV-{i:03}',formulation=importance,concepts=[a,b],sources=[claims[n-1]['source'] for n in nums],importance='CORE_FIDELITY',claims=[f'CPC-{n:04}' for n in nums],regression_type='OMISSION_OR_CONFLATION',scope='reviewed_passages_only'))
    dump('analysis/data/semantic_invariants.json',invariants)
    edges=[dict(source=d,target=c['id'],relation='DEPENDS_ON',interpretive=True,direction='premise_to_dependent',evidence=c['source']) for c in claims for d in c['depends_on']]
    edges += [dict(source='QUESTION_RACINE',target='CPC-0001',relation='DEFINES',interpretive=False,evidence=claims[0]['source'])]
    edges += [dict(source=f'CPC-{n:04}',target='QUESTION_RACINE',relation='ANSWERS',interpretive=True,evidence=claims[n-1]['source']) for n in [16,18]]
    # Explicitly qualified links; never confuse a qualification with an implication.
    for a,b,relation in [(2,10,'QUALIFIES'),(20,16,'QUALIFIES'),(21,16,'QUALIFIES'),
        (28,13,'QUALIFIES'),(31,1,'QUALIFIES'),(40,23,'ASSUMES'),(39,43,'ASSUMES'),
        (44,43,'QUALIFIES'),(42,3,'QUALIFIES'),(51,52,'DEFINES'),(49,41,'DEFINES'),
        (53,46,'DEFINES'),(47,4,'QUALIFIES'),(56,55,'QUALIFIES'),(60,61,'QUALIFIES'),
        (19,17,'QUALIFIES'),(29,18,'SUPPORTS'),(48,5,'DEFINES')]:
        edges.append(dict(source=f'CPC-{a:04}',target=f'CPC-{b:04}',relation=relation,
            interpretive=True,evidence=claims[a-1]['source']))
    dump('analysis/data/argument_graph.json',dict(status='INCOMPLETE',nodes=[{'id':'QUESTION_RACINE','kind':'ROOT_QUESTION'}]+[{'id':c['id'],'kind':c['type']} for c in claims],edges=edges))
    chapters=[]
    for i,(title,question,ranges,terms,nums) in enumerate(CHAPTERS,1):
        chapters.append(dict(id=f'CH-{i:02}',title=title,central_question=question,
            status='PROVISIONAL_INCOMPLETE',root_question_relation='RQ racine : '+question,
            page_ranges=ranges,claims=[f'CPC-{n:04}' for n in nums],concepts=[t for t in terms if any(c['id']==t for c in concepts)],
            dependencies=[],hypotheses=[],empirical_claims=[f'CPC-{n:04}' for n in nums if claims[n-1]['type']=='EMPIRICAL'],potential_tests=['Vérifier hypothèses et portée des relations sur les passages cités.'],bibliographic_domains=['À préciser après reconstruction intégrale'],major_uncertainties=['Couverture intégrale non atteinte ; plages issues en partie de la table des matières.']))
    dump('analysis/data/research_chapters.json',chapters)
    with (ROOT/'analysis/data/claim_chapter_matrix.csv').open('w') as f:
        writer=csv.writer(f); writer.writerow(['claim_id','chapter_id'])
        for ch in chapters:
            writer.writerows((c,ch['id']) for c in ch['claims'])
    core=[dict(id=c['id'],criticality=c['criticality'],statement=c['statement'],reason='Définition, prémisse ou mécanisme dont dépend la reconstruction locale ; criticité provisoire.') for c in claims if c['criticality'] in ['CORE','MAJOR']]
    dump('analysis/data/core_claims.json',core)
    dump('analysis/data/research_questions.json',[dict(id=f'RQ-{i:02}-01',chapter=ch['id'],question=ch['central_question'],claims=ch['claims'],status='OPEN',interpretive=True) for i,ch in enumerate(chapters,1)])
    examined=set(range(1,38))|set(range(184,195))
    coverage=[]
    for p in range(1,563):
        cs=[c['id'] for c in claims if p in c['source']['pages']]
        ns='p001_011.md' if p<12 else 'p012_025.md' if p<26 else 'p026_037.md' if p<38 else 'p184_194.md' if 184<=p<=194 else None
        coverage.append(dict(page=p,examined=p in examined,reading_note=ns,
            claims=cs,concepts=[c['id'] for c in concepts if p in c['source_pages']],
            excluded=False,reason='TITLE_OR_CONTENTS' if p==1 or 5<=p<=11 else 'ARGUMENT_CONTINUATION_OR_REPETITION' if p in examined and not cs else 'NOT_YET_READ' if p not in examined else 'SOURCE_LINKED'))
    dump('analysis/data/page_coverage.json',coverage)
    dump('analysis/data/phase2_progress.json',dict(status='INCOMPLETE',pages_total=562,pages_examined=len(examined),claims=len(claims),concepts=len(concepts),criticality=dict(Counter(c['criticality'] for c in claims)),types=dict(Counter(c['type'] for c in claims)),ready_for_bibliographic_adversarial_review=False))
    root=claims[0]['source']
    dump('analysis/data/root_question.json',dict(id='QUESTION_RACINE',source=root,associated_sentence=dict(document=DOC,page=3,quotation='This essay should only be understood as a proposed answer to this question.'),correction='Previously attributed exclusively to page 3; begins page 2.'))
    print(json.dumps(dict(claims=len(claims),concepts=len(concepts),pages_examined=len(examined))))

if __name__=='__main__':
    main()
