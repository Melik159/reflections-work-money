"""Build a new, versionable synthesis from authored judgments and frozen evidence.

Refuses to overwrite an existing synthesis. No source or scientific status changes.
"""
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from synthesis_catalog import QUESTIONS, CORE, FAMILY_SOURCES, FAMILY_ARTIFACTS
from synthesis_narrative import RESULTS, MINIMAL, ROOT_ANSWER, OPEN, FUTURE, LIMITATIONS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research_questions/synthesis'
inputs = set()

def read(path):
    inputs.add(path)
    return (ROOT/path).read_text()

def load(path):
    return json.loads(read(path))

def link(path, label=None):
    assert (ROOT/path).exists(), path
    return f'[{label or path}](../../{path})'

def save(name, data):
    (OUT/name).write_text(data.rstrip()+'\n')

def js(name, data):
    save(name, json.dumps(data, ensure_ascii=False, indent=2))

def table(name, rows):
    s=io.StringIO(); w=csv.DictWriter(s, fieldnames=list(rows[0]));w.writeheader()
    w.writerows({k: '; '.join(map(str,v)) if isinstance(v,list) else v for k,v in r.items()} for r in rows)
    save(name,s.getvalue())

def md_table(rows):
    keys=list(rows[0]); escape=lambda v:str(v).replace('|',' / ').replace('\n',' ')
    return '| '+' | '.join(keys)+' |\n|'+'|'.join('---' for _ in keys)+'|\n'+ '\n'.join('| '+' | '.join(escape(r[k]) for k in keys)+' |' for r in rows)

def main():
    if OUT.exists():
        raise SystemExit('Refusing to overwrite existing synthesis: archive and review changes explicitly.')
    graph=load('research_questions/question_graph.json')
    nodes={n['id']:n for n in graph['nodes'] if n['id']!='RQ-ROOT'}
    claims={c['id']:c for c in map(json.loads,read('analysis/data/claims.jsonl').splitlines())}
    rechecks={c['id']:c for c in load('analysis/global_corpus_pass/claim_rechecks.json')}
    comparisons={c['id']:c for c in load('research_questions/contribution/core_comparisons.json')}
    concepts=load('research_questions/contribution/concepts.json')
    variables=load('research_questions/operationalization/variables.json')
    lit={b['id']:b for b in load('research_questions/contribution/literature.json')+load('research_questions/operationalization/measurement_literature.json')}
    findings=load('analysis/global_corpus_pass/findings.json')
    cc_review={c['id']:c for c in load('research_questions/contribution/global_corpus_review.json')}
    # Read current final inputs, not history snapshots; their hashes disclose provenance.
    required=['analysis/global_corpus_pass/final_report.md','research_questions/questions.md',
       'research_questions/evidence_matrix.csv','analysis/data/concepts.json','analysis/data/argument_graph.json',
       'analysis/25_productive_review_report.md','analysis/30_terminal_iteration_report.md',
       'analysis/global_corpus_pass/root_question_chain.md','analysis/02_root_question.md',
       'analysis/34_micro_empirical_results.md','analysis/empirical/micro_electricity/results.json',
       'analysis/empirical/independent_energy/results.json','analysis/global_corpus_pass/formula_families.json']
    required += [f'research_questions/{p}_pass_report.md' for p in ['first','second','third','fourth','fifth']]
    required += [str(p.relative_to(ROOT)) for directory in ['research_questions/contribution','research_questions/operationalization']
                 for p in (ROOT/directory).iterdir() if p.is_file() and p.suffix in {'.md','.json','.csv'}]
    for path in sorted(set(required)):read(path)
    for paths in FAMILY_ARTIFACTS.values():
        for path in paths:read(path)
    OUT.mkdir()

    qs=[]
    for line in QUESTIONS.strip().splitlines():
        qid,answer,formal,empirical,counter,impact=line.split('|')
        n=nodes[qid]; family=qid[3:5]; bids,lit_summary=FAMILY_SOURCES[family]
        assert all(b in lit for b in bids)
        pages=sorted({p for cid in n['claims'] for p in claims[cid]['source'].get('pages',[claims[cid]['source']['page']])})
        related_findings=[f for f in findings if qid in f['questions']]
        sources=[f'research_questions/{qid}/global_consolidation.md',f'research_questions/{qid}/conclusion.md',*FAMILY_ARTIFACTS[family]]
        for path in sources:read(path)
        maturity=[f"{v['id']} {v['name']}: L{v['measurement_level']} {v['measurement_status']}" for v in variables if qid in v['dependent_questions']]
        q=dict(id=qid,question=n['question'],status=n['status'],confidence=n['confidence'],
          main_corpus_answer=answer,formal_status=formal,empirical_status=empirical,
          literature_status=lit_summary,literature=bids,counterevidence=counter,
          remaining_uncertainty=counter,root_question_impact=impact,claims=n['claims'],source_pages=pages,
          sources=sources,global_findings=[f['id'] for f in related_findings],
          global_qualifications=[f['INTERPRETATION'] for f in related_findings],
          internal_coherence=formal,external_compatibility=empirical+' '+lit_summary,
          distinctive_explanation='Aucune différence empirique indépendante établie pour cette réponse; voir les restrictions locales CC-01–04.',
          measurement_maturity=maturity or ['Non attribué à la question entière; consulter les variables et les claims liés.'],
          epistemic_kind='INTERPRETATION',status_policy='RETAIN_CURRENT_GRAPH_STATUS',
          confidence_scope='Confiance héritée du dossier, pas probabilité de vérité ni de causalité globale.')
        qs.append(q)
    assert set(nodes)=={q['id'] for q in qs} and len(qs)==53
    js('questions.json',qs)
    table('question_synthesis.csv',[{k:q[k] for k in ['id','question','status','confidence','main_corpus_answer','formal_status','empirical_status','literature_status','literature','counterevidence','remaining_uncertainty','root_question_impact','claims','source_pages','sources','global_findings','internal_coherence','external_compatibility','distinctive_explanation','measurement_maturity']} for q in qs])
    text=['# Synthèse des53questions hors racine','Les statuts sont ceux du graphe courant. Les réponses éditoriales intègrent les qualifications de la lecture complète; elles ne sont pas des citations. Les pages ci-dessous localisent les claims associés, les constats globaux apportent les extensions. Une absence de résolution n’est pas une absence de lecture. Aucun statut n’est promu par le passage de verify.']
    for status in ['RESOLVED_WITHIN_SCOPE','PARTIALLY_RESOLVED','AMBIGUOUS','OPEN','CONTRADICTED','NOT_TESTABLE']:
        group=[q for q in qs if q['status']==status];text += [f'## {status} — {len(group)}']
        if not group:text+=['Aucune question dans cette catégorie.']
        for q in group:
            text += [f"### {q['id']} — {q['question']}",f"Status: {q['status']}; Confidence: {q['confidence']} ({q['confidence_scope']}).",
            '**INTERPRETATION — Main corpus answer** : '+q['main_corpus_answer'],
            'SOURCE : PDF pages '+', '.join(map(str,q['source_pages']))+'; claims '+', '.join(q['claims'])+'. '+ ' ; '.join(link(p) for p in q['sources']),
            'LEVEL A — INTERNAL / Formal status : '+q['formal_status'],
            'LEVEL B — EXTERNAL / Empirical status : '+q['empirical_status'],
            'Literature status : '+q['literature_status']+' IDs: '+', '.join(q['literature'])+' ([registre](source_register.md)).',
            'LEVEL C — DISTINCTIVE EXPLANATION : '+q['distinctive_explanation'],
            'Counterevidence / Remaining uncertainty : '+q['counterevidence'],
            'Qualifications globales : '+'; '.join(q['global_qualifications'] or ['Voir les recontrôles des claims liés.']),
            'Measurement maturity : '+'; '.join(q['measurement_maturity']),
            'Impact on root question : '+q['root_question_impact']]
    save('question_synthesis.md','\n\n'.join(text))

    cores=[];ct=['# Synthèse des24CORE','La formulation française est la reconstruction canonique; la citation anglaise est SOURCE. La revue globale doit se lire avec elle. Les catégories sont non exclusives; «définitionnel» ne signifie pas vrai empiriquement. Pour CPC-0001, NOT_IDENTIFIED concerne la réponse causale recherchée, pas la présence de la question.']
    for line in CORE.strip().splitlines():
        num,status,role,formal,confidence=line.split('|');cid=f'CPC-{int(num):04d}'
        c=claims[cid];review=rechecks[cid];comp=comparisons[cid]
        qids=[q['id'] for q in qs if cid in q['claims']]
        empirical='Aucune mesure indépendante confirmant ce claim spécifique. '+('Compatibilité indirecte non exclusive des mécanismes voisins.' if 'EMPIRICALLY_COMPATIBLE' in status else 'Les définitions et contrôles formels ne sont pas des observations économiques.')
        core=dict(id=cid,statement=c['statement'],source=c['source'],role=role,status=status.split(','),
          global_review_status=review['global_review_status'],global_qualification=review['reason'],
          formal_support=formal,empirical_support=empirical,literature=comp['sources'],
          literature_support=comp['closest_existing_framework']+'; '+comp['difference'],
          objections=review['reason']+' '+comp['different_observable_consequence'],confidence=confidence,
          questions=qids,internal_coherence=formal,external_compatibility=empirical,
          distinctive_explanation=comp['contribution_status']+'; '+comp['different_observable_consequence'],
          source_artifacts=['analysis/data/claims.jsonl','analysis/global_corpus_pass/claim_rechecks.json','research_questions/contribution/core_comparisons.json'],
          epistemic_kind='INTERPRETATION',global_validation=False)
        cores.append(core)
        src=c['source'];pages=src.get('pages',[src['page']])
        ct += [f'## {cid}',c['statement'],f"Rôle : {role}\n\nSOURCE : {src['document']}, pages {pages}. Citation (normalisation de l’extraction conservée) :",'> '+src['quotation'],
           f"Statuts : {status}. Confiance : {confidence} dans la reconstruction limitée.",
           'Revue actuelle : '+review['global_review_status']+' — '+review['reason'],
           'LEVEL A / support formel : '+formal,'LEVEL B / support empirique : '+empirical,
           'Support bibliographique : '+core['literature_support']+' IDs: '+', '.join(comp['sources'])+' ([registre](source_register.md)).',
           'LEVEL C / spécificité : '+core['distinctive_explanation'],
           'Objections : '+core['objections'],'Questions : '+', '.join(qids),
           'Traçabilité : '+'; '.join(link(p) for p in core['source_artifacts'])]
    assert {c['id'] for c in cores}=={c['id'] for c in claims.values() if c['criticality']=='CORE'}
    js('core_claims.json',cores);save('core_claims.md','\n\n'.join(ct))

    results=[]
    for line in RESULTS.strip().splitlines():
        rid,statement,path,rqstr,pagestr,a,b,c=line.split('|');read(path)
        qids=rqstr.split(',');cids=sorted({cid for q in qs if q['id'] in qids for cid in q['claims']})
        results.append(dict(id=rid,statement=statement,sources=[path],source_document='Reflections_PierreCampergue.pdf',
          source_pages=list(map(int,pagestr.split(','))),questions=qids,claims=cids,
          internal_coherence=a,external_compatibility=b,distinctive_explanation=c,
          status=[a,b,c],confidence='MEDIUM',confidence_scope='Conclusion locale de synthèse; pas confiance causale globale.',
          epistemic_kind='INTERPRETATION_OF_EXISTING_RESULTS',global_validation=False))
    js('results.json',results)
    save('strongest_results.md','# STRONGEST_RESULTS\n\nRésultats locaux et limites ayant résisté; pas dix claims empiriquement confirmés.\n\n'+'\n\n'.join(f"## {r['id']}\n\n{r['statement']}\n\nA: {r['internal_coherence']}; B: {r['external_compatibility']}; C: {r['distinctive_explanation']}. SOURCE: "+link(r['sources'][0]) for r in results if r['id'] in ['SYN-01','SYN-02','SYN-04','SYN-05','SYN-06','SYN-07','SYN-09','SYN-10','SYN-13','SYN-14']))
    negative=[r for r in results if r['id'] in ['SYN-03','SYN-04','SYN-07','SYN-08','SYN-09','SYN-11','SYN-12','SYN-13','SYN-14']]
    save('negative_results.md','# Résultats négatifs et non identifiables\n\nNe pas effacer ces diagnostics lors d’une nouvelle synthèse. NOT_IDENTIFIED n’est pas une contradiction; une erreur locale n’est pas un rejet global.\n\n'+'\n\n'.join(f"## {r['id']}\n\n{r['statement']}\n\nPérimètre : {r['external_compatibility']}. Source : "+link(r['sources'][0]) for r in negative))
    save('weakest_points.md','# WEAKEST_POINTS\n\nNeuf points limitant la portée quantitative actuelle, non neuf réfutations.\n\n'+'\n\n'.join(f"{i}. {r['statement']} ([{r['id']}](negative_results.md)). Source : "+link(r['sources'][0]) for i,r in enumerate(negative,1)))

    candidates=[]
    defs=[('CC-01','Séparer paiement, transformation et destination du gain','DISTINCT_DECOMPOSITION','REFORMULATION',['CPC-0015','CPC-0022','CPC-0046'],['BIB-0001','BIB-0003','CBIB-04','CBIB-10'],['RQ-02.02','RQ-06.04','RQ-10.01'],'Classement conditionnel et audit de frontières; les comptes usuels et le surplus représentent déjà plusieurs de ces distinctions.','MODERATE','Pas de chiffre nouveau; supériorité pédagogique ou décisionnelle non testée.'),
      ('CC-02','Tâche, vitesse et Work additionnel','DISTINCT_FORMAL_RESTRICTION','NOVELTY_UNRESOLVED',['CPC-0040','CPC-0051','CPC-0052'],['BIB-0002','CBIB-11','BIB-0017'],['RQ-03.02','RQ-03.03'],'cp et primitive quadratique ne sont pas simplement des heures, de la TFP ou de la valeur ajoutée.','POSSIBLE','T indépendant manque; primitive peut être une définition plutôt qu’une prédiction.'),
      ('CC-03','Exigences d’échelle de Utility','DISTINCT_FORMAL_RESTRICTION','NOVELTY_UNRESOLVED',['CPC-0100','CPC-0104','CPC-0113'],['CBIB-03','CBIB-07','MET-BIB-02'],['RQ-05.03'],'Diagnostic de l’étude: mêmes préférences ordinales, rendements de ratios différents; ce n’est pas une invention historique attribuée à Campergue.','MODERATE','Exigence métrologique connue; peut constituer un obstacle plutôt qu’un gain empirique.'),
      ('CC-04','Condition Utility dans le pont physique','DISTINCT_DECOMPOSITION','NOVELTY_UNRESOLVED',['CPC-0017','CPC-0039'],['CBIB-02','BIB-0013','BIB-0021'],['RQ-09.02','RQ-09.03'],'Le travail physique utile reçoit une condition économique supplémentaire; ni chaque joule ni toute efficacité physique ne crée Money.','POSSIBLE','Utility/T sans étalon; aucune observable exclusive démontrée.')]
    contribution_text=['# Contributions potentielles après consolidation','Les catégories comparent des constructions, non leur priorité historique. Quatre pistes survivent avec qualifications. Zéro prédiction empirique indépendante nouvelle établie; zéro nouvelle mesure opérationnelle démontrée. KNOWN_EQUIVALENT, PARTIAL_PARALLEL et REFORMULATION demeurent utiles comme classes, sans rabaisser ni surestimer leur intérêt.']
    for cid,title,classification,secondary,cids,bids,qids,difference,clarity,limit in defs:
        review=cc_review[cid]
        item=dict(id=cid,title=title,classifications=[classification,secondary],claims=cids,questions=qids,
          source_document='Reflections_PierreCampergue.pdf',source_pages=review['pages'],literature=bids,
          difference=difference,limit=limit,current_evidence=review['reason'],global_review_status=review['status'],
          source_artifacts=['research_questions/contribution/candidate_contributions.md','research_questions/contribution/global_corpus_review.json'],
          historical_novelty_status='HISTORICAL_NOVELTY_UNRESOLVED',originality_asserted=False,
          different_testable_prediction_established=False,new_measurement_established=False,
          conceptual_clarity=clarity,measurement_value='POSSIBLE' if cid in ['CC-01','CC-03'] else 'UNDETERMINED',
          empirical_value='UNDETERMINED',decision_value='POSSIBLE' if cid=='CC-01' else 'UNDETERMINED',
          internal_coherence='QUALIFIED',external_compatibility='PARTIAL_PARALLEL',distinctive_explanation=classification,
          status='POTENTIALLY_DISTINCT',confidence='MEDIUM',epistemic_kind='REVIEW_INTERPRETATION')
        candidates.append(item)
        contribution_text += [f'## {cid} — {title}',f"Source : PDF {review['pages']}; claims {', '.join(cids)}; questions {', '.join(qids)}.",
          'Littérature comparable : '+', '.join(bids)+' ([registre](source_register.md)).',
          'Différence et utilité possible : '+difference,'Preuve actuelle : '+review['reason'],
          'Limite / contre-argument : '+limit,
          'Classement : '+classification+' / '+secondary+'. Nouveauté historique : HISTORICAL_NOVELTY_UNRESOLVED.',
          f"Clarté {clarity}; mesure {item['measurement_value']}; empirique UNDETERMINED; décision {item['decision_value']}. Confiance MEDIUM pour distinction locale, LOW pour supériorité empirique.",
          'A — qualification interne; B — parallèle partiel; C — différence formelle ou de décomposition, pas prédiction indépendante établie. '+link(item['source_artifacts'][1])]
    contribution_text += ['## Comparaison des21concepts — catégories non synonymes',md_table([{'Concept':c['term'],'Classement antérieur':c['contribution_status'],'Différence conservée':c['difference'],'Sources':', '.join(c['sources'])} for c in concepts]),
      '## CONCEPTUAL-ONLY CONTRIBUTIONS','CC-01–04 restent conceptuelles, classificatoires ou formelles. K variable et les limites du PIB relèvent aussi de problèmes généraux déjà étudiés. Aucun gain de mesure indépendante ni contribution empirique spécifique n’est obtenu par simple renommage.']
    js('contributions.json',candidates);save('contributions.md','\n\n'.join(contribution_text))

    save('minimal_model.md',MINIMAL);save('root_question_answer.md',ROOT_ANSWER)
    save('open_questions.md',OPEN);save('future_research.md',FUTURE)
    register=['# Registre des sources utilisées','Les vérifications sont héritées des passes bibliographiques, non renouvelées par la synthèse. VERIFIED porte sur le périmètre lu; PARTIALLY_VERIFIED ne signifie pas lecture du texte complet. Aucune nouvelle référence ni DOI inventé. Les publications historiques ne sont pas présentées comme normes actuelles.']
    for b in lit.values():
        register += [f"## {b['id']}",f"{b.get('authors',b.get('author',''))}. {b['title']} ({b['year']}). [{b['title']}]({b['url']}).",
          'Statut : '+b['status']+'. Périmètre : '+b.get('access',b.get('verification_scope','Voir registre source')),
          'Résultat mobilisé : '+b.get('summary',b.get('result','')),
          'Limite : '+b.get('limit',b.get('verification','Ne pas étendre au-delà du passage identifié.'))]
    save('source_register.md','\n\n'.join(register));js('literature.json',list(lit.values()))

    matrix=[]
    def row(item,kind,source,qs,cids,a,formal,b,lit,counter,distinct,maturity,status,confidence):
        return dict(Item=item,Type=kind,Source=source,Question=qs,Claim=cids,**{'Internal coherence':a,'Formal support':formal,'Empirical support':b,'Literature support':lit,'Counterevidence':counter,'Distinctiveness':distinct,'Measurement maturity':maturity,'Status':status,'Confidence':confidence})
    for q in qs:
        matrix.append(row(q['id'],'QUESTION',q['sources'],q['id'],q['claims'],q['internal_coherence'],q['formal_status'],q['empirical_status'],q['literature'],q['counterevidence'],q['distinctive_explanation'],q['measurement_maturity'],q['status'],q['confidence']))
    for c in cores:
        matrix.append(row(c['id'],'CORE',c['source_artifacts'],c['questions'],c['id'],c['internal_coherence'],c['formal_support'],c['empirical_support'],c['literature'],c['objections'],c['distinctive_explanation'],'Voir variables liées, pas niveau uniforme du claim',c['status'],c['confidence']))
    for c in candidates:
        matrix.append(row(c['id'],'CONTRIBUTION',c['source_artifacts'],c['questions'],c['claims'],c['internal_coherence'],c['difference'],c['external_compatibility'],c['literature'],c['limit'],c['distinctive_explanation'],'Aucune nouvelle mesure indépendante',c['status'],c['confidence']))
    for r in results:
        matrix.append(row(r['id'],'SYNTHESIS_RESULT',r['sources'],r['questions'],r['claims'],r['internal_coherence'],r['internal_coherence'],r['external_compatibility'],'Voir questions et registre',r['statement'],r['distinctive_explanation'],'Proxy ou construction selon résultat; voir variables',r['status'],r['confidence']))
    table('master_matrix.csv',matrix)

    # The eleven source links are not eleven established causal results.
    chain_specs=[('Subsistance → énergie bon marché / transformations',[20,29,62,72],['SUPPORTED_BY_CORPUS','PARTIALLY_SUPPORTED'],'Contexte historique proposé, contrefactuel non testé.'),
      ('Énergie physique → transformation Utility',[159,455,456],['SUPPORTED_BY_CORPUS'],'Condition économique explicite, étalon manquant.'),
      ('Accélération productive → coût',[19,20,32,196,207,361,364],['SUPPORTED_BY_CORPUS','FORMALLY_DERIVED'],'Seulement sous tâche, cp et frontière du modèle local.'),
      ('Coût → prix / partage du gain',[20,21,363,364,504,508],['SUPPORTED_BY_CORPUS','PARTIALLY_SUPPORTED'],'Ni automatique ni total.'),
      ('Prix / Utility → pouvoir d’achat / Money',[19,291,349,400],['SUPPORTED_BY_CORPUS'],'Construction de Money non indépendamment mesurée.'),
      ('Gain → possibilités de consommation',[52,180,400,468,523],['SUPPORTED_BY_CORPUS'],'Possibilité, avec épargne et autres destinations.'),
      ('Production / usages → flux physiques',[72,112,163,164,165,454,460],['SUPPORTED_BY_CORPUS','EMPIRICALLY_COMPATIBLE'],'Mix, composition et périmètre à fixer.'),
      ('Carburants / déchets → dommages',[72,112,454,460],['SUPPORTED_BY_CORPUS','EMPIRICALLY_COMPATIBLE'],'Pressions générales, pas fonction de dommage complète.'),
      ('Allocation marginale exacte du gain → panier',[],['MISSING'],'Pas de fermeture comportementale précise.'),
      ('Panier hétérogène → dommage quantifié',[],['MISSING'],'Pas de fonction physique/exposition complète.'),
      ('Relations locales → GDP=K·W macro',[538,558,559],['SUPPORTED_BY_CORPUS','CONTESTED'],'Affirmation source; composition, étalons et stabilité non déduits.')]
    chain=[dict(id=f'LINK-{i:02d}',link=s,source_pages=p,status=st,qualification=lim,
      source='analysis/global_corpus_pass/root_question_chain.md',questions=['RQ-12.01','RQ-11.03'],claims=['CPC-0001'],causal_identification='NOT_IDENTIFIED') for i,(s,p,st,lim) in enumerate(chain_specs,1)]
    js('root_question_chain.json',chain)
    save('root_question_chain.md','# Chaîne vers la question racine\n\nSUPPORTED_BY_CORPUS atteste la présence du lien, pas sa vérité causale. FORMALLY_DERIVED ne vaut que dans le domaine indiqué.\n\n'+md_table([{'Lien':r['link'],'Pages':r['source_pages'],'Statuts':', '.join(r['status']),'Condition / manque':r['qualification']} for r in chain])+'\n\nSource : '+link('analysis/global_corpus_pass/root_question_chain.md'))
    counts=Counter(q['status'] for q in qs)
    core_counts=Counter(s for c in cores for s in c['status'])
    manifest=dict(status='SYNTHESIS_WRITTEN_PENDING_VERIFICATION',questions=53,question_statuses=dict(counts),core_claims=24,
      core_classification_counts=dict(core_counts),classification_counts_are_nonexclusive=True,contributions=4,
      source_pages=562,scanned_pages=562,analytically_reviewed_cumulative=447,
      source_commit='a697345c427fca8de0521108a17aa2b76f267654',
      source_root_question_pages=[2,3],global_validation=False,ready_for_external_review=False,
      readiness_scope='Documentary and reproducibility review readiness, not empirical resolution.',
      scientific_status_changes=[],canonical_claim_changes=[],new_empirical_experiments=0,
      input_policy='Current graph statuses + canonical source quotations + full-corpus qualifications; historic targeted absences superseded.',
      literature_policy='Inherited verification scopes; no new external verification claimed.')
    # Source checksum is copied from the actual baseline, never from a constructed measure.
    manifest['source_sha256']=hashlib.sha256((ROOT/'Reflections_PierreCampergue.pdf').read_bytes()).hexdigest()
    js('manifest.json',manifest)
    main_sections=[
      ('Executive summary','Le corpus propose un système de distinctions et de relations conditionnelles, pas un ensemble à juger en bloc. Les effets productifs sont reliés aux possibilités de consommation et aux dommages, mais plusieurs variables de la conversion économique restent non mesurées. La synthèse sépare cohérence interne, compatibilité externe et pouvoir explicatif distinctif. 53questions: '+str(dict(counts))+'. Aucun statut scientifique promu. [Vue complète](question_synthesis.md); [matrice](master_matrix.csv).'),
      ('Root question','La question exacte commence page PDF2 et se termine page3. Le manuscrit se présente comme une réponse proposée, non comme preuve déjà acquise. [Citation et réponse](root_question_answer.md); CPC-0001.'),
      ('Minimal reconstruction of Campergue’s framework',MINIMAL.split('\n',1)[1]),
      ('Core concepts','Cash support, Money valeur/gain dans le corpus; Product support, Utility contextuelle; labour/tâche distinct de Work; création distincte de transfert; énergie physique distincte de sa conversion économique. Les définitions originales et leurs ambiguïtés restent accessibles dans '+link('analysis/data/concepts.json')+' et le [comparatif](contributions.md).'),
      ('Core claims','24CORE présentés individuellement avec citation, rôle, recontrôle global, objections et sources. Les classifications sont non exclusives : '+str(dict(core_counts))+'. Une définition peut être précise sans donnée qui la mesure. [Fiches](core_claims.md).'),
      ('Money / Cash','SYN-01 : M=n·u ne prouve pas une neutralité générale. 32scénarios séparent compensation, changement de valeur, création productive, ajustement nominal et redistribution. La littérature sur les dépôts bancaires parle d’une catégorie institutionnelle qui ne se mappe pas directement sur Money. Aucun montant observé de Money n’a été fabriqué. [CORE](core_claims.md); '+link('research_questions/contribution/cash_money_crosswalk.md')+'.'),
      ('Economic Work / productivity','SYN-02/03/06 : distinguer tâche, vitesse et variation. La primitive quadratique est conditionnelle à cp; l’absence de dT n’efface pas l’effort humain ou physique. Le +78% est arithmétiquement reproduit, dépend d’une relation quadratique et ne constitue pas sa vérification indépendante. '+link('research_questions/experiments/EXP-09/results.json')+'.'),
      ('Utility / measurement','SYN-04 : les ordres conservent certaines comparaisons; différences et ratios exigent des structures supplémentaires. U=4,2 donne 1−U₂/U₁=0,5, contre0,75 après recodage carré conservant l’ordre. Ce diagnostic ne signifie pas que toutes les équations requièrent une origine absolue. 26variables: L0=0,L1=10,L2=6,L3=9,L4=0,L5=1. L3 décrit une procédure, pas une collecte. '+link('research_questions/operationalization/variables.md')+'.'),
      ('Cost / price / gains','SYN-05/12 : gains transmis, retenus, partagés, épargnés ou employés ailleurs. Un gain de panier q₀(p₀−p₁) n’est pas automatiquement surplus du consommateur, hausse réelle de revenu ou Money. Le corpus tardif interdit une lecture de transmission intégrale automatique. '+link('analysis/global_corpus_pass/findings.json')+'.'),
      ('Aggregation','SYN-07/11 : avec unités communes, additivité et coefficients fixes, K=ΣwᵢKᵢ. ΔK=ΣΔwᵢKᵢ; composition fixe suffit, mais des changements peuvent se compenser. Tous les mélanges sont invariants seulement si les coefficients actifs sont identiques. Changer les unités requiert une covariation; changer arbitrairement les normalisations n’est pas une découverte économique. La transposition au K macro de p559 demeure conditionnelle. '+link('research_questions/experiments/EXP-03/results.json')+'.'),
      ('Energy / environment','SYN-09/10/13/14 : données énergétiques indépendantes ≠ énergie exogène causalement. Le pont économique dépend de Utility. Le corpus relie explicitement carburants/déchets et dommages, mais ni allocation marginale des gains ni fonction de dommage hétérogène ne clôt la chaîne. [Chaîne](root_question_chain.md).'),
      ('Agents / transfers','Une opération peut combiner transformation et rente, ou changement de valeur et transfert. Le transport effectif, les services et les brevets exigent des frontières précises. L’antagonisme des gains par copie ne s’étend pas automatiquement aux revenus par heure. La conservation de flux comptables consolidés ne démontre pas celle du Money propre au corpus. '+link('analysis/global_corpus_pass/internal_counterexamples.md')+'; SYN-01/05/13.'),
      ('Empirical results','Aucun nouveau modèle estimé pour cette synthèse. Les tests antérieurs sont repris avec leurs limites. Monde1990–2023, logPIB sur logénergie primaire: N34, β1,5349, IC95%HAC(3)[1,4585;1,6114], R²0,9918. France β−0,6624, Allemagne−1,7282 en niveaux logarithmiques, mais co-mouvements annuels positifs. Les signes ne sont pas des effets causaux. PIB/énergie mondial augmente d’environ45%, incompatible avec l’identification strictement constante choisie. '+link('analysis/27_energy_results.md')+'. Cas électrique US: coût du combustible gaz versus prix résidentiel global, N20 variations, β0,01428, IC95%HAC(2)[−0,00716;0,03572], R²0,03190; frontières différentes, pas de pass-through structurel identifié. '+link('analysis/34_micro_empirical_results.md')+'.'),
      ('Formal results','Les tests de recodage Utility, composition de K, lectures T/dT et +78% donnent des conclusions locales reproductibles. Ils ne sont pas des preuves comportementales. Des erreurs intermédiaires de signes, limites, primitives et équivalence force constante/nulle restent localisées, même lorsqu’une expression finale peut être reconstruite sous conditions. [Résultats](results.json), SYN-02/03/04/06/07/08.'),
      ('Comparison with existing economics','Comptes nationaux, surplus, incidence des coûts, productivité, utilité et travail physique utile donnent des comparateurs nécessaires. Ils n’impliquent ni identité complète de vocabulaire ni nouveauté par simple différence de notation. Les vérifications partielles restent partielles. [Registre](source_register.md); [comparaisons](contributions.md).'),
      ('Candidate contributions','CC-01 séparation paiement/transformation/destination; CC-02 tâche/vitesse/Work additionnel; CC-03 exigences d’échelle de Utility (diagnostic de la revue); CC-04 condition économique du pont physique. Zéro prédiction spécifique indépendamment établie et zéro nouvelle mesure opérationnelle démontrée. [Fiches et contre-arguments](contributions.md).'),
      ('Strongest results','Dix résultats résistants comprennent des distinctions et des limites établies dans leur périmètre, non dix succès empiriques. [STRONGEST_RESULTS](strongest_results.md); SYN-01/02/04/05/06/07/09/10/13/14.'),
      ('Weakest points','T/cp non étalonnés, cardinalité Utility, Money non observé, contraintes d’agrégation, problèmes locaux de dérivation, pont économique de l’énergie, coût/prix non appariés et fermeture environnementale manquante. [WEAKEST_POINTS](weakest_points.md); [résultats négatifs](negative_results.md).'),
      ('Remaining open questions','Les15priorités regroupées concernent référents formels, étalons, données appariées, composition, destination du gain, dommage marginal et spécificité. Elles ne remplacent ni ne renumérotent les53questions. [Liste](open_questions.md).'),
      ('Provisional answer to the root question',ROOT_ANSWER.split('## PROVISIONAL_ANSWER\n\n')[1].split('## CONFIDENCE')[0]+'\n\nConfiance MEDIUM dans la reconstruction conditionnelle, LOW dans une attribution causale propre et quantitative. [Réponse structurée complète](root_question_answer.md).'),
      ('Future research','Huit travaux priorisés : étalonT/cp, échelleUtility, micro apparié, K hors calibration, destination du gain, impacts du panier, dérivations locales, audit comparatif. Ils sont proposés, non exécutés ici. [Protocoles](future_research.md).'),
      ('Limitations',LIMITATIONS)]
    save('final_synthesis.md','# Synthèse générale — système Campergue\n\nStatut documentaire : synthèse pour examen externe; aucun verdict binaire global. SOURCE / INTERPRETATION / FORMAL_RESULT / EMPIRICAL_RESULT restent distincts.\n\n'+'\n\n'.join(f'## {i}. {title}\n\n{body}' for i,(title,body) in enumerate(main_sections,1)))
    save('README.md','# Synthèse navigable\n\nCommencer par [le rapport principal](final_synthesis.md), puis [la réponse racine](root_question_answer.md).\n\n[53questions](question_synthesis.md) · [24CORE](core_claims.md) · [matrice maître](master_matrix.csv) · [contributions](contributions.md) · [sources](source_register.md) · [résultats négatifs](negative_results.md) · [programme futur](future_research.md).\n\nLes conclusions sont éditoriales et sourcées. A = interne; B = compatibilité externe; C = explication distinctive. Le périmètre du certificat externe est documentaire, pas résolution des questions. Aucun nouveau calcul empirique. Reproduction : `./verify.sh` depuis la racine. Les générateurs refusent un écrasement silencieux.\n\nLes fichiers machine sont les miroirs des fiches; le manifeste et les empreintes d’entrée permettent de détecter les modifications qui exigent une nouvelle revue.')
    for p in ['analysis/synthesis_catalog.py','analysis/synthesis_narrative.py','analysis/build_final_synthesis.py']:read(p)
    js('input_manifest.json',[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in sorted(inputs)])
    print(json.dumps(dict(questions=53,core=24,master_rows=len(matrix),status_counts=dict(counts),core_counts=dict(core_counts)),ensure_ascii=False))

if __name__=='__main__':main()
