"""Render research dossiers from curated questions and existing evidence.
Templates organize evidence; they do not manufacture a scientific resolution.
"""
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research_questions'

# Each first-pass entry is a local editorial assessment, not a new Campergue claim.
# answer, derived, qualification, unknown, test, alternative, literature, artifact
REVIEWS={
'RQ-01.01':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='La racine est historique et environnementale, mais le préambule p.29 restreint son objet économique. Les développements p.460 réintroduisent un lien environnemental. Il faut donc évaluer séparément richesse et dommages, sans effacer cette différence de périmètre.',
 derived='Une explication de Money seule ne suffit pas logiquement à répondre à la question environnementale.',
 qualification='La restriction locale p.29 ne prouve pas que tout le manuscrit ignore l’environnement ; CPC-0120 interdit cette conclusion.',
 unknown='Étendue des dommages couverts et raccord historique quantifié.',
 test='CONSISTENCY_TEST : confronter les passages de cadrage p.2–3/29 aux liaisons p.460 ; variable : portée de chaque proposition ; données : texte. Incompatible avec une couverture complète : maillon de dommage sans source ou sans mécanisme.',
 alternative='Une théorie de production peut avoir un objet plus étroit qu’une histoire de la transition ou qu’une théorie des externalités.',
 bib=[('BIB-0004','QUALIFIES','Cadre externe des facteurs d’émissions ; pas une validation du mécanisme de Money.')],artifact='analysis/data/environmental_chain.json'),
'RQ-02.01':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='Wealth est restreint p.185 à la quantité de Money, hors patrimoine. P.204 reconnaît des richesses culturelles et activités socialement utiles sans création de cette richesse technique. Le mot richesse ne peut donc servir de mesure universelle de bien-être.',
 derived='Une exclusion définitionnelle du patrimoine n’est ni sa disparition économique ni une preuve qu’il ne contribue pas au niveau de vie.',
 qualification='La proximité des mots richesse et agrégat monétaire ne justifie pas un mapping comptable automatique.',
 unknown='Comment comparer la grandeur restreinte à des indicateurs de patrimoine, consommation réelle et distribution ?',
 test='COMPARATIVE_TEST : établir trois bilans séparés Money, patrimoine et consommation ; variables : frontières et unités ; données : définitions et comptes. Contre-exemple à une équivalence générale : même Money avec patrimoines ou accès aux services différents.',
 alternative='Comptabilité nationale des stocks/flux et indicateurs multidimensionnels décrivent des objets plus larges.',
 bib=[('BIB-0003','QUALIFIES','Stocks patrimoniaux et flux comptables ne sont pas une seule grandeur.')],artifact='analysis/data/concepts.json'),
'RQ-03.01':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='Labour est une tâche définie pour un Product et une méthode ; Economic Work vise sa transformation dynamique, notamment la variation de vitesse. P.203, vitesse constante implique absence de Work supplémentaire dans ce sens, malgré effort physique. Cela ne signifie pas inutilité sociale.',
 derived='dω=0 annule le terme cp·ω·dω ; cela ne fixe pas le niveau de sa primitive T ni la chaleur consommée.',
 qualification='T comme réserve et T comme travail réalisé restent à réconcilier ; une distinction sémantique fidèle ne valide pas le choix de mesure.',
 unknown='Référent commun et mesure indépendante de Force/complexité pour des tâches hétérogènes.',
 test='CONSISTENCY_TEST : comparer même tâche à vitesse constante puis accélérée ; variables l,ω,dT,T ; données : équations et cas p.188/203. Incompatible avec la reconstruction : assimiler dT nul à effort physique nul ou T nul sans condition initiale.',
 alternative='La productivité usuelle rapporte production et facteurs ; elle n’adopte pas nécessairement cette définition différentielle.',
 bib=[('BIB-0002','QUALIFIES','Mesure de productivité distincte de la définition de Work.')],artifact='analysis/25_productive_mechanism.md'),
'RQ-03.03':dict(status='AMBIGUOUS',confidence='MEDIUM',
 answer='Les dimensions peuvent être exprimées symboliquement, mais aucune calibration indépendante de cp, Force et T n’est disponible dans le cas micro. Calculer T depuis ω puis vérifier la même équation serait circulaire.',
 derived='Sous cp constant et référent fixé, intégrer cp·ω·dω donne une différence quadratique ; cela ne produit pas une observation indépendante.',
 qualification='Le cas électrique ne mesure ni tâche homogène ni Utility ; son efficacité thermique ne comble pas ces lacunes.',
 unknown='Procédure de mesure indépendante, invariance au choix d’unité de tâche et éventuel coefficient variable.',
 test='EMPIRICAL_TEST/FORMAL_TEST : mesurer tâche, temps, coût, qualité et une force/complexité indépendamment ; prévoir ΔT avant le résultat. Incompatible : ΔT indépendant hors prédiction à conditions satisfaites. Actuellement NOT_IDENTIFIABLE.',
 alternative='Production standard, composition du parc et substitution capital/travail peuvent produire la même efficacité sans T.',
 bib=[('BIB-0002','QUALIFIES','Les conventions de mesure des facteurs doivent être explicitées.')],artifact='analysis/32_dimensional_consistency.md'),
'RQ-04.02':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='Le +78% est le résultat arrondi de (8/6)²−1=7/9 sous tâche, coefficient et référent constants. Le coût horaire20 donne160→120. Calcul arithmétique reproduit ; origine économique de l’hypothèse quadratique non testée.',
 derived='La vitesse est multipliée par4/3 ; son carré par16/9. Un changement de cp ou de constante d’intégration change la comparaison de niveaux.',
 qualification='Une relation d’énergie cinétique en physique n’établit pas la calibration économique de T.',
 unknown='Observation indépendante imposant cette puissance plutôt qu’une autre relation productive.',
 test='FORMAL_TEST : recalcul exact7/9 et coût20×durée ; EMPIRICAL_TEST ultérieur : comparer ΔT indépendant à plusieurs vitesses, cp fixe. Incompatible avec généralité : coefficients variables ou mesures indépendantes non quadratiques.',
 alternative='Le coût de durée à taux horaire fixe s’explique sans loi quadratique de Work.',
 bib=[('BIB-0002','DOES_NOT_TEST','Le manuel ne teste pas cette loi quadratique propre au manuscrit.')],artifact='analysis/run_productive_checks.py'),
'RQ-05.01':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='Deux branches sont explicites : prix maintenu malgré baisse du coût p.20–21, et transmission à profit absolu constant p.503–506. L’auteur ne doit pas être réduit à une transmission automatique. Un taux universel ou délai chiffré n’est pas identifié.',
 derived='À profit unitaire absolu constant, P=C+profit transmet une variation de coût total à prix ; à P constant, le profit augmente si C total baisse.',
 qualification='Le proxy combustible et le prix résidentiel ont des frontières différentes : ni profit ni transmission structurelle identifiés.',
 unknown='Conditions observables sélectionnant une branche avant de voir les prix, autres coûts, qualité et délais.',
 test='EMPIRICAL_TEST : panel produit/producteur, coût total et prix transactionnel, profit unitaire, qualité fixe ; estimer une transmission prédéfinie. Incompatible : prix contraire à la branche malgré conditions indépendamment établies.',
 alternative='Concurrence, pouvoir de marché, contrat ou régulation donnent aussi transmission ou rétention.',
 bib=[('BIB-0002','QUALIFIES','Mesure des coûts et productivité nécessite des facteurs et frontières comparables.')],artifact='analysis/empirical/micro_electricity/results.json'),
'RQ-05.03':dict(status='AMBIGUOUS',confidence='MEDIUM',
 answer='Utility dépend de l’agent et du moment p.189–192 ; p.291 elle ordonne notamment la priorité des besoins satisfaits. Une Utility décroissante peut y accompagner un enrichissement. Elle n’est donc pas simplement une performance technique croissante.',
 derived='Prix moindre et Utility croissante ne signifient pas automatiquement enrichissement dans les quatre possibilités p.291.',
 qualification='Le jouet à deux produits montre la dépendance d’une somme de qualités à leur échelle ; il ne prouve pas que Campergue autorise toute normalisation.',
 unknown='Échelle cardinale commune, comparabilité interpersonnelle et lien entre besoin, performance et coefficient rP.',
 test='COUNTEREXAMPLE/EMPIRICAL_TEST : préférences et caractéristiques indépendantes du prix ; conserver produit et agent ; tester invariance aux échelles. Incompatible avec agrégat univoque : signe global changeant sous normalisations également admissibles.',
 alternative='Indices hédoniques et préférences ordinales ne mesurent pas automatiquement Utility Campergue.',
 bib=[('BIB-0008','QUALIFIES','Correction de qualité des prix distincte d’une Utility commune.')],artifact='analysis/empirical/micro_electricity/two_product_results.json'),
'RQ-06.02':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='M=n·u fixe une identité, pas un mécanisme unique. Les32 scénarios conservés incluent M constant, émission accompagnatrice, destruction, inertie, cas incohérents et combinaison d’effets. La compensation inverse n’est dérivée qu’à M constant.',
 derived='dM=n·du+u·dn ; à M constant et n non nul, u=M/n. À changements finis, conserver le terme croisé ou employer directement le produit.',
 qualification='Le classement de tout crédit non couvert dans la branche M constant est une restriction supplémentaire, non prouvée par cette dérivation.',
 unknown='Mécanisme et horizon d’ajustement indépendamment mesurables ; traitement des cas déclarés impossibles.',
 test='FORMAL_TEST puis COMPARATIVE_TEST : suivre n,u,M avec frontières fixes pour chaque scénario. Contre-exemple à neutralité autonome : choisir n et u variables avec M non constant ; cela ne réfute pas la branche explicitement conditionnée à M constant.',
 alternative='Création institutionnelle de dépôts et création de richesse réelle sont des objets différents.',
 bib=[('BIB-0001','QUALIFIES','La création de dépôts ne tranche pas, à elle seule, la variation de Money Campergue.')],artifact='analysis/data/money_compensation_scenarios.json'),
'RQ-07.02':dict(status='PARTIALLY_RESOLVED',confidence='MEDIUM',
 answer='La non-neutralité p.400 concerne des positions d’acteurs. P.349 l’intermédiaire sans variation pertinente transfère ; p.488–490 distingue rente monopolistique et brevet productif. Un gain individuel ne prouve pas un gain global.',
 derived='Un transfert fermé de montant x a des contreparties +x et−x dans un même bilan ; une création nette demande un terme distinct et une frontière commune.',
 qualification='L’addition de bilans nominaux ne suffit pas à agréger des valorisations hétérogènes de Money.',
 unknown='Contreparties complètes et séparation indépendante de rente, qualité et transformation productive.',
 test='CONSISTENCY_TEST : deux agents puis intermédiaire, bilans avant/après, prix/qualité/coût séparés. Incompatible avec création par transfert seul : bilan global inchangé malgré gain individuel. Données futures : transactions appariées.',
 alternative='Rente, surplus d’échange et transfert comptable peuvent évoluer différemment.',
 bib=[('BIB-0003','QUALIFIES','Bilans et contreparties imposent de distinguer stocks, flux et revalorisations.')],artifact='analysis/29_agents_markets_review.md'),
'RQ-08.02':dict(status='PARTIALLY_RESOLVED',confidence='HIGH',
 answer='La p.559 propose une stabilisation de K par multiplication des Products. Le jouet montre que des K locaux fixes donnent K agrégé40/35 puis40/50 lorsque les quantités changent. Répliquer les produits ne supprime pas cet effet de composition.',
 derived='Sous additivité stipulée, K agrégé est pondéré par les contributions T, non une moyenne arbitraire des K locaux.',
 qualification='C’est un contre-exemple à la suffisance du grand nombre seul, pas à toute agrégation avec poids stabilisés. Le PIB/énergie testé reste un proxy distinct.',
 unknown='Distribution, poids et frontières qui justifieraient une convergence stable et correspondance de T avec énergie consommée.',
 test='COUNTEREXAMPLE/FORMAL_TEST : maintenir K locaux et varier composition ; EMPIRICAL_TEST : coefficients fixés hors échantillon. Incompatible avec constance inconditionnelle : K agrégé change sans changement d’unité.',
 alternative='Composition sectorielle et hétérogénéité des fonctions de production expliquent des coefficients agrégés variables.',
 bib=[('BIB-0015','QUALIFIES','Les fondements micro de l’agrégation sont un problème distinct ; accès limité, aucun théorème détaillé imputé.')],artifact='analysis/empirical/micro_electricity/two_product_results.json'),
'RQ-09.02':dict(status='AMBIGUOUS',confidence='MEDIUM',
 answer='P.455 pose un pont physique/économique, mais le restreint au travail faisant évoluer Utility. P.559 reconnaît de l’énergie non créatrice. Il faut respecter ce formalisme distinct sans supposer que tout joule est Money.',
 derived='La composition de rendements est calculable une fois unités, signes et frontières compatibles ; elle ne calibre pas les grandeurs économiques.',
 qualification='Une énergie acquise sans PIB dans sa construction n’est pas pour autant exogène causalement ; l’association macro ne mesure pas le pont T/M.',
 unknown='Mesure indépendante du travail utile, conversion d’unités et séparation pertes utiles/inutiles.',
 test='FORMAL_TEST/EMPIRICAL_TEST : bilan physique d’un processus et mesures séparées T/Utility ; énergie inutile en contrôle. Incompatible avec pont universel : énergie dépensée sans changement pertinent ; ce cas est déjà admis, donc ne réfute pas la version conditionnelle.',
 alternative='Énergie comme intrant de production, qualité technique et efficacité sans équivalence monétaire.',
 bib=[('BIB-0013','PARALLELS','Rôle productif de l’énergie ; pas une mesure de T ou Money.')],artifact='analysis/32_dimensional_consistency.md'),
'RQ-10.02':dict(status='PARTIALLY_RESOLVED',confidence='MEDIUM',
 answer='P.33 autorise un usage ultérieur ; p.400 davantage de produits ou une meilleure qualité ; p.523 exclut l’égalité obligatoire entre création et dépense. L’empreinte ne peut donc être déduite mécaniquement du gain disponible.',
 derived='Il faut distinguer budget libéré, épargne, panier acheté et empreinte de ce panier, avec un horizon explicite.',
 qualification='Un gain à panier fixe n’est ni surplus compensatoire ni consommation effectivement observée ; la passe électrique ne mesure pas leur affectation.',
 unknown='Propension et délai de dépense, composition marginale et effets de revenu/distribution.',
 test='EMPIRICAL_TEST : suivre ménages exposés à une baisse exogène de coût/prix et témoins, dépenses physiques et épargne ; prédiction de parts de gain préspécifiée. Incompatible avec consommation automatique : gain conservé sans achat supplémentaire ; cette possibilité reste admise par Campergue.',
 alternative='Effets revenu/substitution, épargne de précaution et report de consommation.',
 bib=[('BIB-0014','PARALLELS','Rebond indirect possible via dépenses réaffectées ; pas une égalité Money–énergie.')],artifact='analysis/data/environmental_chain.json'),
'RQ-11.01':dict(status='PARTIALLY_RESOLVED',confidence='MEDIUM',
 answer='Les liaisons archivées relient cycles accélérés, gains, usages possibles, énergie peu coûteuse, transports et pertes aux dommages. Elles n’offrent ni panier marginal, ni intensités matière/énergie par usage, ni fonction quantitative de dommages.',
 derived='Un surcroît de dépense ne fixe pas une empreinte sans quantité, composition et intensités ; énergie et dommage sont des étapes différentes.',
 qualification='L’existence textuelle d’une chaîne ne démontre pas sa causalité ; une même énergie peut avoir des dommages différents selon technique et lieu.',
 unknown='Externalités non énergétiques, importations, mix, exposition et attribution historique.',
 test='EMPIRICAL_TEST : panier marginal issu du gain, intensités physiques et impacts par filière ; comparer un contrefactuel sans gain. Incompatible avec dommage nécessairement croissant : empreinte moindre à service et frontière comparables ; conditions à fixer avant test.',
 alternative='Mix énergétique, politiques environnementales, commerce, composition et innovations propres modifient les dommages.',
 bib=[('BIB-0004','QUALIFIES','Facteurs d’émissions distincts ; émissions et totalité des dommages ne sont pas synonymes.'),('BIB-0014','PARALLELS','Réadaptation de consommation possible, ampleur non déduite du corpus.')],artifact='analysis/data/environmental_chain.json')}

def render(qs,claims,write):
    sources={s['id']:s for s in json.loads((ROOT/'analysis/data/literature_map.json').read_text())['sources']}
    evidences=[];relations=[]
    for q in qs:
        id=q['id'];r=REVIEWS.get(id);q['first_pass']=bool(r)
        if r:q['status']=r['status']
        q['confidence']=r['confidence'] if r else 'LOW'
        q['literature']=[];q['evidence']=[]
        for cid in q['claims']:
            c=claims[cid];s=c['source'];eid=f'EVID-{id}-{cid}'
            e=dict(id=eid,question=id,claim=cid,type='TEXTUAL',relation='SUPPORTS',source=s,
                content=c['statement'],interpretive=True,
                force='Atteste que la proposition figure dans le corpus, PAS sa vérité économique.',
                limit='Citation et contexte sélectionnés ; aucune exhaustivité des562 pages revendiquée.')
            evidences.append(e);q['evidence'].append(eid)
        if r:
            artifact=ROOT/r['artifact'];assert artifact.exists(),artifact
            eid=f'EVID-{id}-REVIEW'
            typ='COUNTEREXAMPLE' if id in ['RQ-08.02','RQ-05.03'] else 'FORMAL' if id in ['RQ-04.02','RQ-06.02','RQ-07.02'] else 'EMPIRICAL' if id=='RQ-05.01' else 'LOGICAL'
            e=dict(id=eid,question=id,claim=None,type=typ,relation='QUALIFIES',source={'artifact':r['artifact']},
                content=r['qualification'],force='Résultat local ; voir protocole et conditions de l’artefact.',
                limit=r['unknown'],interpretive=True)
            evidences.append(e);q['evidence'].append(eid)
            for bid,relation,comparison in r['bib']:
                assert bid in sources
                q['literature'].append(dict(id=bid,relation=relation,question=id,comparison=comparison,
                    verification=sources[bid]['status'],source=sources[bid],
                    limit='Réutilisation ciblée du registre existant ; ce lien ne prouve pas le formalisme complet.'))
        q['test_design']=r['test'] if r else (
            'CONSISTENCY_TEST préparatoire : '+q['question']+
            ' Hypothèse à examiner : la proposition des claims liés tient sous leurs seules conditions explicites. '
            'Variables : concepts liés ; unités et observables à opérationnaliser. Données : passages sourcés ci-dessous. '
            'Prédiction : reconstruire les conséquences avant observation ; seuil numérique non défini. '
            'Résultat incompatible : contre-exemple satisfaisant les prémisses mais pas la conclusion. '
            'Explications concurrentes : à sélectionner avant un test empirique. NOT_CURRENTLY_TESTABLE quantitativement dans ce dossier initial.')
        q['test_design_status']='DESIGNED_FIRST_PASS' if r else 'SCOPING_ONLY'
        q['conclusion']=r['answer'] if r else 'OPEN : dossier indexé, non examiné en profondeur dans cette passe. Le texte atteste les propositions liées ; il ne suffit pas à répondre à la question.'
        q['scope_of_resolution']=None # No question declared resolved in this initial research pass.
        for dep in q['dependencies']:relations.append(dict(source=id,target=dep,relation='DEPENDS_ON',meaning='source requires target; editorial prerequisite, not textual entailment'))
        if q['parent']:relations.append(dict(source=id,target=q['parent'],relation='PART_OF'))
    relations.append(dict(source='RQ-12.03',target='RQ-ROOT',relation='ANSWERS',meaning='Intended answer, currently OPEN'))
    byid={q['id']:q for q in qs}
    for q in qs:
        id=q['id'];r=REVIEWS.get(id);folder=OUT/id
        link=lambda x:f'[{x}](../{x}/README.md)'
        header=f"# {id} — {q['question']}\n\n"
        readme=header+'## Why it matters\n\n'+f"Parent : {link(q['parent']) if q['parent'] else 'aucun'}. Ce problème précise une condition de réponse à RQ-ROOT ; ses dépendances empêchent de sauter directement du gain à ses dommages.\n\n"
        readme+='## Scope\n\n'+q['scope']+'\n\n## Out of scope\n\n'+q['out_of_scope']+'\n\n'
        readme+='## Related claims\n\n'+', '.join(q['claims'])+'\n\n## Related concepts\n\n'+', '.join(q['concepts'])+'\n\n'
        readme+='## Dependencies\n\n'+(', '.join(link(x) for x in q['dependencies']) or 'Aucune prerequisite dans ce graphe.')+'\n\n'
        readme+='## Current status\n\n'+q['status']+' ; confiance '+q['confidence']+'.\n\n'
        readme+=f"Première passe approfondie ciblée : {'oui' if r else 'non'}. Complétude des passages : {q['corpus_completeness']}.\n\n"
        readme+='Chapitres transversaux : '+', '.join(q['chapters'])+'.\n\n[Corpus](corpus.md) · [Preuves](evidence.md) · [Littérature](literature.md) · [Tests](tests.md) · [Conclusion](conclusion.md)\n'
        write(folder/'README.md',readme)
        corpus=header+'Périmètre : tous les extraits des claims actuellement reliés ; **pas tous les passages potentiellement pertinents du manuscrit**. Les nouvelles lectures pourront modifier ce dossier par révision explicite.\n\n'
        for cid in q['claims']:
            c=claims[cid];s=c['source'];pages=s.get('pages',[s['page']])
            corpus+=f"## {cid}\n\n### SOURCE\n\n{s['document']} ; pages PDF {', '.join(map(str,pages))} ; normalisation : {s.get('normalization','voir claim original')}.\n\n> "+s['quotation'].replace('\n','\n> ')+'\n\n'
            corpus+='Contexte avant : '+s.get('context_before','Non enregistré dans ce claim ; consulter la page extraite.')+'\n\nContexte après : '+s.get('context_after','Non enregistré dans ce claim ; consulter la page extraite.')+'\n\n'
            corpus+='### INTERPRETATION\n\n'+c['statement']+'\n\nLien analytique : '+q['question']+' La citation atteste le propos, non sa validation.\n\n'
        if id=='RQ-ROOT':corpus+='### SOURCE — phrase associée\n\nPage PDF3 :\n\n> '+q['associated_sentence']+'\n\n### INTERPRETATION\n\nL’auteur présente une réponse proposée, non une démonstration préalablement acquise.\n'
        write(folder/'corpus.md',corpus)
        evidence=header+'Les preuves TEXTUAL soutiennent une attribution au corpus, jamais automatiquement une loi empirique.\n\n'
        for e in [e for e in evidences if e['question']==id]:
            loc=e['source'].get('artifact') or f"{e['source']['document']} PDF{e['source'].get('pages',[e['source']['page']])}"
            evidence+=f"## {e['id']}\n\nType : {e['type']} ; relation : {e['relation']}.\n\nSource : {loc} ; question : {id} ; claim : {e['claim'] or 'inférence de recherche, aucun nouveau claim source'}.\n\nContenu : {e['content']}\n\nForce : {e['force']}\n\nLimite : {e['limit']}\n\n"
        write(folder/'evidence.md',evidence)
        lit=header
        if not q['literature']:lit+='OPEN — aucune source externe examinée pour cette question dans la présente passe. Les références d’un chapitre voisin ne sont pas automatiquement des preuves de ce dossier.\n'
        for b in q['literature']:
            s=b['source'];lit+=f"## {b['id']}\n\n{s['authors']} ({s['year']}). [{s['title']}]({s['url']}).\n\nRelation : {b['relation']} ; question : {id}. Résultat pertinent : {b['comparison']}\n\nLocalisation et accès : {s.get('locator','voir registre')} ; {s.get('access','voir registre')}.\n\nVérification héritée : {s['status']}. Limite : {b['limit']}\n\n"
        write(folder/'literature.md',lit)
        test=header+'Types : '+', '.join(q['testability'])+'. Statut du protocole : '+q['test_design_status']+'.\n\n'+q['test_design']+'\n\n'
        if r:test+='Explication concurrente : '+r['alternative']+'\n\nArtefact déjà disponible (pas une nouvelle expérience exécutée ici) : `'+r['artifact']+'`.\n'
        test+='\nLes tests de cohérence de verify.sh vérifient ce dossier et ses liens ; ils ne résolvent pas sa question scientifique.\n'
        write(folder/'tests.md',test)
        conclusion=header+'## STATUS\n\n'+q['status']+'\n\n## WHAT_CAMPERGUE_CLAIMS\n\n'+ '\n\n'.join(cid+' : '+claims[cid]['statement'] for cid in q['claims'])+'\n\n'
        conclusion+='Reformulations ci-dessus : INTERPRETATION ; citations exactes séparées dans corpus.md.\n\n'
        for title,text in [
            ('WHAT_IS_DERIVED',r['derived'] if r else 'Aucune nouvelle dérivation examinée dans ce dossier initial.'),
            ('WHAT_EVIDENCE_SUPPORTS','Les extraits attestent les affirmations ; les conditions restent obligatoires.'),
            ('WHAT_EVIDENCE_QUALIFIES',r['qualification'] if r else 'Couverture ciblée et absence de revue approfondie ; pas une réfutation.'),
            ('WHAT_EVIDENCE_CONTRADICTS','Aucune contradiction globale établie. '+(r['qualification'] if r and id in ['RQ-08.02','RQ-05.03'] else 'Les tensions et données non discriminantes ne sont pas converties en contradiction.')),
            ('WHAT_REMAINS_UNKNOWN',r['unknown'] if r else 'Opérationnalisation, littérature contradictoire et critère de décision propres à cette question.'),
            ('PROVISIONAL_ANSWER',q['conclusion']),('CONFIDENCE',q['confidence'])]:
            conclusion+='## '+title+'\n\n'+text+'\n\n'
        write(folder/'conclusion.md',conclusion)
    graph=dict(version=1,root='RQ-ROOT',count_excluding_root=len(qs)-1,nodes=qs,edges=relations,evidence=evidences,
        counting_policy='53 questions outside root; level1 synthesis questions included; first-pass counts exclude root',
        epistemic_policy='New questions, prerequisite edges and conclusions are RESEARCH_INTERPRETATION; quotations alone SOURCE.',
        migration_policy='Stable IDs; archive old/new/reason/evidence for any edit; DEPRECATED and SPLIT_INTO recorded in history, never delete silently.')
    write(OUT/'question_graph.json',json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
    def table(path,head,rows):
        s=io.StringIO();w=csv.writer(s);w.writerow(head);w.writerows(rows);write(path,s.getvalue())
    table(OUT/'claim_question_matrix.csv',['Claim','Question','Criticality'],[(c,q['id'],claims[c]['criticality']) for q in qs for c in q['claims']])
    table(OUT/'evidence_matrix.csv',['Question','Corpus evidence','Formal evidence','Empirical evidence','External literature','Counterevidence','Tests available','Status'],
        [(q['id'],sum(e['type']=='TEXTUAL' for e in evidences if e['question']==q['id']),
          sum(e['type'] in ['FORMAL','LOGICAL'] for e in evidences if e['question']==q['id']),
          sum(e['type']=='EMPIRICAL' for e in evidences if e['question']==q['id']),len(q['literature']),
          sum(e['type']=='COUNTEREXAMPLE' for e in evidences if e['question']==q['id']),q['test_design_status'],q['status']) for q in qs])
    history=[dict(version=1,action='CREATE',ids=[q['id'] for q in qs],
        reason='Problem decomposition distinct from chapter classification; no legacy IDs removed.',
        legacy_file='analysis/data/research_questions.json',source_claims_unchanged=True)]
    history += [dict(version=1,action='FIRST_PASS',id=q['id'],old_statement=q['question'],new_statement=q['question'],
        old_status='OPEN',new_status=q['status'],reason=q['conclusion'],new_evidence=q['evidence'],
        note='Evidence attached to this dossier; not necessarily newly produced empirical evidence.') for q in qs if q['first_pass']]
    write(OUT/'history.json',json.dumps(history,ensure_ascii=False,indent=2)+'\n')
    # A current-status companion keeps the initial tree immutable and avoids stale navigation.
    write(OUT/'status.md','# Statuts actuels\n\nLe catalogue initial questions.md précède les dossiers ; cette table et question_graph.json portent les statuts après première passe.\n\n| Question | Première passe | Statut | Classes |\n|---|---|---|---|\n'+
        '\n'.join(f"| [{q['id']}]({q['id']}/README.md) | {q['first_pass']} | {q['status']} | {', '.join(q['classification'])} |" for q in qs)+'\n')
