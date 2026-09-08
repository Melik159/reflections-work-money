"""Editorial compilation after targeted human reading; guarded against overwrite."""
import json, shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def write(p,t):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t)
pages={x['page_pdf']:' '.join(x['text'].split()) for x in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
def source(page,anchor):
    t=pages[page];i=t.index(anchor);end=min(len(t),i+480)
    if end<len(t):end=t.rfind(' ',i,end)
    return dict(document='Reflections_PierreCampergue.pdf',page=page,pages=[page],quotation=t[i:end],normalization='whitespace',context_before=t[max(0,i-160):i],context_after=t[end:end+160])

# name, page, anchor, conditions, mechanism, exception, chapter, epistemic kind
MECHANISMS=[
('Tâche fixe, vitesse variable',196,'for the realization of a given Product','Même Product et méthode; cP défini','Labour fixe; Work varie avec la vitesse, pas avec les seules heures','Changement de méthode ou de complexité interdit comparaison toutes choses égales','CH-03','CONCEPTUAL'),
('Vitesse constante sans Work supplémentaire',203,"if the speed of execution of the labour doesn't vary",'ω constante; mesure de variation dT, pas suppression du travail physique','dω=0 conduit à dT=0; labour et W physique peuvent rester importants','T=cpω²/2 peut rester non nul; le texte appelle aussi Work nul cette absence de création','CH-04','CONCEPTUAL'),
('Accélération et coût horaire inchangé',32,'Let us suppose that the manufacturing','Même tâche; coût horaire20$, autres facteurs constants','8h→6h : coût160→120; T relatif augmente sous loi quadratique','Coût horaire, capital et énergie supplémentaires peuvent absorber le gain','CH-04','HYPOTHESIS'),
('Prix de vente maintenu, gain retenu',20,'if the selling price is kept constant','Coût réduit, prix de vente fixé par entrepreneur','Baisse productive puis hausse comptable dans la reconstruction de l’auteur','Deux étapes analytiques ne prouvent pas deux prix effectivement observés','CH-04','CONCEPTUAL'),
('Transmission en chaîne à profit absolu constant',504,'these segments have the same length','Profits par opération inchangés; Seller puis Transformer; variations régulières','Coûts moindres donnent prix de vente moindres; gains amont et aval','Profit constant en montant ≠ taux de marge constant; règle absente si profit varie','CH-04','HYPOTHESIS'),
('Création puis usage ultérieur du supplément',33,'The consumer can therefore use this Money','Baisse de prix préalable; même achat; supplément conservé','Le gain existe avant sa dépense ultérieure, laquelle n’est pas sa création','Délai d’usage n’est pas un délai démontré de transmission coût/prix','CH-07','CONCEPTUAL'),
('Création via différence d’Utility',349,'If the Final Utility is equal','Transformation spécifiée; utilités initiale/finale, rP et gamma','Différence d’Utility associée à Money; intermédiaire sans variation : transfert seul','Sens de Utility dépend du point de vue; pas qualité ou satisfaction standard automatique','CH-06','HYPOTHESIS'),
('Trois transformations T→M à caractéristique constante',293,'three particular cases of transformations','rP fixe; FA ou p ou UP constant','Isobare, isoaxiale et isophèle donnent des branches différentes','Négociation non conclue : inégalité; rP variable change les ratios','CH-06','CONCEPTUAL'),
('Trois transformations M→T symétriques',300,'three particular cases of transformations','rA fixe; FP ou labour ou UA constant','Isobare, isoergue et isophèle; Utility de Cash, pas du Product','Ne pas confondre FP/FA, UP/UA et les deux supports','CH-06','CONCEPTUAL'),
('Transformation adiabatique et frontière du système',347,'During an adiabatic transformation','Pas de transfert avec Buyer/Seller; évolution quasi statique','Utility évolue; intégration interne de FA.dp malgré absence de transfert externe','Échange de Work nul ne signifie pas toutes les variations internes nulles','CH-07','HYPOTHESIS'),
('Cycles couplés et rendements',388,'the two transformations','Deux transformations appréhendées ensemble; conventions de signe et réversibilité','ηglobal défini comme produit; optimum annoncé à angles égaux','Passage des rendements irréversibles aux égalités et domaine d’optimisation à justifier','CH-07','HYPOTHESIS'),
('Coût d’énergie absorbant les gains relatifs',461,'At time t2','Exemple stylisé France/Chine; seul prix d’énergie multiplié par10','Rapport des coûts .60 devient5.10/5.50; avantage salarial relatif réduit','Auteur limite expressément la validité à l’illustration, pas aux nombres historiques','CH-09','HYPOTHESIS'),
('Substitution machine–salarié',212,'if the labour to be performed by an employee','Labour réparti entre moyens; coûts comparés','Emploi salarié peut baisser tandis que contribution mécanique augmente','Emploi e du modèle inclut machines; ne pas assimiler directement aux personnes employées','CH-04','HYPOTHESIS'),
('Création productive avec émission de Cash calibrée',204,'The State (or any other issuer)','Baisse de prix et création déjà identifiées; émission calibrée','Variante4 : n varie, u reste constant; ne pas ajouter deux fois le même gain','Émettre sans transformation ne constitue pas automatiquement le même scénario','CH-04','CONCEPTUAL'),
('Pertes utiles et inutiles',479,'losses useful to the Society','Pertes distinguées selon fonction sociale','Prélèvements utiles aux infrastructures : optimum recherché; pertes inutiles : minimum','Destruction de Money au sens du modèle ne signifie pas absence d’utilité sociale','CH-09','CONCEPTUAL'),
('Coefficients de transformation variables',526,'the transformation coefficients are therefore no longer constant','Branches incohérentes, coefficients gTM/gMT variables','Même Work peut être associé à Money différent; compensation par g','Le régime cohérent suppose g constant mais cette constance n’est pas universelle','CH-07','HYPOTHESIS'),
('Ralentissement, stabilité, accélération entre exemplaires',502,'if the production speed decreases','Deux copies comparables; coût temporel constant','Trois signes d’évolution de la vitesse : prix monte, reste, baisse','Volume de production supplémentaire n’est pas identique à accélération à tâche fixe','CH-04','HYPOTHESIS'),
('Addition entre moyens productifs',210,'these characteristics being additive','Même convention de mesure, individus/salariés/animaux/machines','Labour, T et emploi e déclarés additifs entre contributeurs','L’addition des T ne donne pas le carré de la somme des vitesses; pas de règle macro complète','CH-03','ASSUMPTION'),
('Prix formé pendant fabrication versus prix entre copies',198,'they only give a measure of these speeds','Trajectoire d’un exemplaire distinguée de comparaison de copies','ω et varpi mesurent des vitesses sans stipuler leurs causes','Prix final moindre ne détermine pas seul la pente temporelle; pp459/504 à réconcilier','CH-04','METHODOLOGICAL'),
('Utility, négociation et complexité',283,'If the consumer is fooled by advertising','Utility peut être subjective/erronée; rP dépend de complexité/quantité','Prix et quantités peuvent changer via appréciation/complexité, pas seulement coût','Pas de taux de transmission universel; identification circulaire si Force définie par UP/p','CH-06','HYPOTHESIS')]

# Formula transcription is explicitly separate from verbatim prose.
FORMULAS=[
('ω = −dl/dt',197,'04-01','DEFINITION','l labour restant; t temps; ω productivité','[ω]=[l]/temps','Définition de la vitesse; signe de la tâche restante','Même convention de labour','l constant → ω=0; méthode changeante exige recalibrage'),
('ϖ = dp/dt',198,'04-02','DEFINITION','p prix; ϖ tachyaxis','[ϖ]=[p]/temps','Définition de pente, pas théorie causale du prix','Trajectoire temporelle définie','Prix discontinu : représentation élémentaire/continue discutée'),
('F_P = c_P γ_ω',201,'04-05','PROPOSED_LAW','cP complexité; γω=dω/dt; FP Force','[FP]=[cP][l]/temps², inféré','Analogie de F=mγ; application économique postulée','cP mesurable indépendamment','Même notation ne prouve pas loi physique transférée'),
('dT = F_P dl',203,'04-07','DEFINITION','T Economic Work; FP Force; l labour','[T]=[FP][l], inféré','Définition proposée; signe adapté à B au04-09','Acteur et orientation fixés','Ne pas remplacer dl par heures de travail'),
('dM = −F_A dp',204,'04-08','DEFINITION','M Money; FA Force; p prix','[M]=[FA][p], inféré','Définition; signe différent avec V et point de vue interne','FA spécifié','dp=0 implique dM=0, pas M absolu nul'),
('T = (1/2)c_P ω²',207,'04-15','DERIVATION','T; cP; ω','[T]=[cP][l]²/temps², pas joules automatiquement','dT=cpωdω; intégrer cP constant; constante choisie nulle','Loi de Force admise; cP constant; référence zéro','ω constante implique dT=0, non T=0'),
('M = −(1/2)c_A ϖ²',207,'04-16','DERIVATION','M; cA complexité de Cash; varpi','[M]=[cA][p]²/temps², inféré','dM=−cA varpi dvarpi; intégrer à cA constant, référence zéro','Signes et cA distinct de cP','Mesure différentielle versus encaisse absolue'),
('e = c_P ω ; a = −c_A ϖ',208,'04-17/04-18','PROPOSED_LAW','e emploi du modèle; a purchasing power; complexités/vitesses','[e]=[cP][ω]; [a]=[cA][ϖ], inféré','Identification proposée aux variables dites emploi et pouvoir d’achat','Product et complexités constants','e inclut machines; a pas salaire réel statistique automatique'),
('F_A p = r_P U_P',283,'08-04','PROPOSED_LAW','UP Utility Product; rP fonction complexité/quantité; FA,p','[rP][UP]=[FA][p], inféré','C=UP/p, identification C=FA, introduction rP','rP calibré; échange effectif','Refus d’achat : inégalité explicite p284'),
('F_P l = r_A U_A',299,'08-12','PROPOSED_LAW','UA Utility Cash; rA complexité/quantité Cash; FP,l','[rA][UA]=[FP][l], inféré','Construction symétrique de08-04','UA≠UP; FP≠FA','Refus d’échange et ratio marginal non démontré'),
('p₁/U_P₁ = p₂/U_P₂',294,'08-06','DERIVATION','Deux états prix/utilité, même rP et FA','Ratio [p]/[UP]','Diviser08-04 parFA.UP dans les deux états','FA et rP constants; UP non nul','rP changeant : ratio non constant'),
('F_A₁/U_P₁ = F_A₂/U_P₂',294,'08-07','DERIVATION','Deux états Force/utilité','Ratio [FA]/[UP]','Diviser08-04 parp.UP','p et rP constants; UP non nul','Changement de quantité/complexité change rP'),
('F_A₁ p₁ = F_A₂ p₂',295,'08-08','DERIVATION','Deux états Force/prix','[FA][p]','Même rP.UP dans08-04','UP et rP constants','Une Utility variable quitte la branche'),
('M = r_P U_P ln(p_f/p_i)',347,'12-03','DERIVATION','M variation sur trajectoire; pi,pf prix; UP,rP','Logarithme de ratio sans dimension; [rP][UP]','Intégrer dM=rP.UP.dp/p à UP et rP constants','pi,pf positifs; point de vue interne','pf=pi → zéro; signe dépend orientation, pas rejet automatique'),
('M = r_P/(1−γ_TM) (U_Pf−U_Pi)',349,'12-04','DERIVATION','gammaTM exposant adiabatique; autres variables précédentes','[rP][UP], gamma sans dimension','FA.p^gamma=k; intégrer k.p^(−gamma)dp; substituer Core Law','Quasi statique; gamma,rP constants; gamma≠1','gamma=1 exige branche logarithmique; pas substitution dans dénominateur nul'),
('η_TM = −M/T₁',384,'definition yield','DEFINITION','T1 Work entrant; M sortant signé; eta rendement','Sans dimension seulement si unités compatibles/g incorporé','Définition du rapport sortant/entrant','T1 non nul; même base de conversion','Conventions de signe indispensables'),
('η_TM ≥ 1−U_P₂/U_P₁',385,'14-01','DERIVATION','etaTM et utilités aux bornes','Rapport d’utilités sans dimension','Premier et second principes, division avec signe de T1 explicité','Hypothèses du cycle; UP1 positif; T1 selon orientation','Borne inférieure seule ne prouve pas η=0 quand UP2=UP1'),
('η_gmax = (2−√2)² ≈ 0.3431',389,'14-07','DERIVATION','eta global; α=β=π/8','Sans dimension','Substitution tan(π/8)=√2−1 dans la valeur annoncée','Optimum à angles égaux imposé/à justifier; ne pas optimiser une autre expression','Arithmétique correcte; expression carrée14-06 et tableau392 à réconcilier hors équilibre'),
('p = (1/2)(e C_h)(l T⁻¹)',501,'24-03','DERIVATION','Ch coût horaire; e=cpω; l tâche; T=cpω²/2','Après substitution p=Ch.l/ω, unité prix','p=Ch.t; T=eω/2; ω=l/t en valeur absolue','Ne pas garder e constant tout en variant ω à cP constant','p∝1/T seulement si e fixé; à cP,l,Ch fixes p∝1/√T'),
('Q_consumed = −M_created / (∏η_i(QW) ∏η_i(TM))',456,'19-01','DERIVATION','Q chaleur; M signé; rendements physiques/économiques','Compatibilité des unités physiques/économiques à établir, non donnée en SI','Chaîner les rapports de rendements et identification du Work utile','Coefficients compatibles; rendements non nuls; chaîne délimitée','Chaleur supplémentaire non créatrice explicitement possible; rendements variables empêchent proportionnalité globale fixe')]

def main():
    if (ROOT/'analysis/data/productive_mechanisms.json').exists():raise SystemExit('Already compiled; use explicit revision history.')
    paths=['analysis/data/claims.jsonl','analysis/data/argument_graph.json','analysis/data/research_chapters.json','analysis/data/concepts.json','analysis/data/page_coverage.json','analysis/data/phase2_progress.json','analysis/data/hypotheses.json']
    for p in paths:
        dest=ROOT/'analysis/history/pre_productive_review'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
    claims=[json.loads(l) for l in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()];old=len(claims)
    chapters=load('analysis/data/research_chapters.json');g=load('analysis/data/argument_graph.json');mechanisms=[]
    for i,(name,page,anchor,conditions,transformation,exceptions,ch,typ) in enumerate(MECHANISMS,1):
        sid=f'PM-{i:02d}';cid=f'CPC-{len(claims)+1:04d}';s=source(page,anchor)
        c=dict(id=cid,statement=name+' : '+transformation+'.',source=s,source_document=s['document'],page=page,quotation=s['quotation'],type=typ,epistemic_status='SOURCE',interpretive=True,
          concepts=['work','productivity','price','money','transformation'],depends_on=['CPC-0052'],supports=[],contradicts=[],criticality='MAJOR',testability='CONDITIONAL_NOT_EMPIRICALLY_VALIDATED',
          root_question_relevance='Préciser le mécanisme productif du passage à l’abondance, sans valider son exclusivité.',interpretation_notes='Reconstruction ciblée; conditions et exceptions dans '+sid,confidence_in_reconstruction=.8)
        claims.append(c);next(x for x in chapters if x['id']==ch)['claims'].append(cid)
        m=dict(id=sid,name=name,source=s,pages=[page],claims=[cid],initial_state=conditions,transformation=transformation,variables=['T','ω','l','p','M'],conditions=conditions,
          intermediates=transformation,result=transformation,exceptions=exceptions,time_horizon='Transformation ou comparaison entre exemplaires; délai chiffré non fourni.',level='MICRO; agrégation non automatique',testability='Mesures indépendantes requises; pas de validation causale dans cette passe.',epistemic_type=typ,interpretive=True,chapter=ch)
        mechanisms.append(m);g['nodes'] += [dict(id=cid,kind=typ),dict(id=sid,kind='PRODUCTIVE_MECHANISM',conditions=conditions)]
        for a,b,r in [('CPC-0052',sid,'QUALIFIES'),(sid,cid,'EXEMPLIFIES')]:g['edges'].append(dict(source=a,target=b,relation=r,evidence=s,conditions=conditions,interpretive=True))
    # Preserve alternative monetary branches via cross-links, no identity proof.
    g['edges'].append(dict(source='SC-MONEY-06',target='PM-14',relation='EXEMPLIFIES',evidence=mechanisms[13]['source'],conditions=mechanisms[13]['conditions'],interpretive=True))
    write('analysis/data/claims.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in claims));save('analysis/data/argument_graph.json',g)
    save('analysis/data/productive_mechanisms.json',dict(status='QUALIFIED_TARGETED_RECONSTRUCTION',mechanisms=mechanisms,limitations=['Targeted reading, not exhaustive','Partial/delayed pass-through not assigned to author without source']))
    save('analysis/data/productive_claim_revision_log.json',dict(old_total=old,new_total=len(claims),existing_statements_changed=[],new_claims=[c['id'] for c in claims[old:]],reason='Add separately sourced productive branches without rewriting the monetary review.'))
    fs=[]
    for i,(formula,p,label,status,variables,units,steps,conditions,limits) in enumerate(FORMULAS,3):
        fs.append(dict(id=f'FORM-{i:02d}',formula_exact_transcription=formula,page=p,source_document='Reflections_PierreCampergue.pdf',manuscript_label=label,status=status,
          variables=variables,dimensions=units,dimension_status='ANALYST_INFERENCE_UNLESS_EXPLICIT',derivation_steps=steps,necessary_assumptions=conditions,announced_domain='Transformation spécifiée, pas loi macro automatiquement',boundary_cases=limits,
          transcription_method='VISUAL_CHECKED' if p in [207,385,389,501,456] else 'TEXT_EXTRACTION_MANUAL_TRANSCRIPTION',raw_extracted_page=pages[p],empirical_status='NOT_EMPIRICALLY_TESTED'))
    save('analysis/data/productive_formulas.json',fs)
    for ch in chapters:
        if ch['id'] in ['CH-06','CH-07']:
            ch.update(analysis_status='UNCERTAIN',analysis_file='analysis/chapters/'+('CH06_constitutive_transformations.md' if ch['id']=='CH-06' else 'CH07_cycles_yields.md'),productive_review='analysis/25_productive_mechanism.md')
    save('analysis/data/research_chapters.json',chapters)
    write('analysis/data/claim_chapter_matrix.csv','claim_id,chapter_id\n'+''.join(f"{cid},{ch['id']}\n" for ch in chapters for cid in ch['claims']))
    cs=load('analysis/data/concepts.json')
    for c in cs:
        c['used_in_claims']=[x['id'] for x in claims if c['id'] in x['concepts']]
        if c['id']=='work':c['ambiguities'].append('Productive review: distinguish T level from dT creation; additive means p210; fixed speed p203/208 does not imply no labour or physical W. See FORM-08 and PM-02.')
    save('analysis/data/concepts.json',cs)
    examined=set(range(195,213))|set(range(281,286))|set(range(293,301))|set(range(345,351))|set(range(383,393))|set(range(454,463))|set(range(477,480))|set(range(500,507))
    coverage=load('analysis/data/page_coverage.json')
    for row in coverage:
        if row['page'] in examined and not row['examined']:row.update(examined=True,reading_note='productive_targeted_review.md',reason='TARGETED_ANALYTICAL_READING')
        row['claims']=[c['id'] for c in claims if row['page'] in c['source']['pages']]
    save('analysis/data/page_coverage.json',coverage)
    state=load('analysis/data/phase2_progress.json');state.update(pages_examined=sum(x['examined'] for x in coverage),claims=len(claims),productive_review_status='QUALIFIED');save('analysis/data/phase2_progress.json',state)
    write('analysis/reading_notes/productive_targeted_review.md','# Lecture productive dirigée\n\nPages lues intégralement : 195–212,281–285,293–300,345–350,383–392,454–462,477–479,500–506. Relecture32–36; renvois aux pages déjà examinées20–21,33,204,344,526.\n\n195–212 : définition, vitesse, Forces, quadratique, intégration, emploi additif. 281–300 : lois constitutives, négociation et branches à variables constantes. 345–350 : transferts versus évolution interne, intégrales et singularités. 383–392 : rendements et couplage, signe et domaine de l’optimum. 454–462 : chaîne énergétique et coûts relatifs stylisés. 477–479 : Makers/Workers et pertes utiles. 500–506 : composition temporelle du prix, profit inchangé, transmission en chaîne.\n\nFormules inspectées visuellement : pages207,385,389,501,456. Les autres transcriptions portent le statut TEXT_EXTRACTION_MANUAL_TRANSCRIPTION, non VISUAL_CHECKED. Voir productive_formulas.json pour les textes exacts extraits et le rapport25 pour les interprétations.\n')
    report=['# Mécanismes productifs — reconstruction ciblée\n\nStatut : QUALIFIED. Aucun verdict global;20 mécanismes à plusieurs niveaux.\n']
    for m in mechanisms:report.append(f"\n## {m['id']} — {m['name']}\n\nClaim {m['claims'][0]}; chapitre {m['chapter']}; type {m['epistemic_type']}.\n\nSOURCE_TEXT, page PDF {m['source']['page']} :\n\n> {m['source']['quotation']}\n\nContexte : {m['source']['context_before']} / {m['source']['context_after']}\n\nINTERPRETATION — État/conditions : {m['conditions']}.\n\nTransformation/intermédiaires/résultat : {m['transformation']}.\n\nExceptions : {m['exceptions']}.\n\nHorizon : {m['time_horizon']} Niveau : {m['level']}. Testabilité : {m['testability']}\n")
    report.append('\n## Formules examinées\n\nLes transcriptions sont séparées des citations; dimensions non fournies par l’auteur signalées comme inférences.\n')
    for f in fs:report.append(f"\n### {f['id']} — {f['manuscript_label']} (PDF {f['page']})\n\n`{f['formula_exact_transcription']}`\n\nStatut : {f['status']}; contrôle : {f['transcription_method']}. Variables : {f['variables']}.\n\nDimensions : {f['dimensions']}. Étapes : {f['derivation_steps']}.\n\nHypothèses : {f['necessary_assumptions']}. Limites : {f['boundary_cases']}. Validation : {f['empirical_status']}.\n")
    write('analysis/25_productive_mechanism.md',''.join(report))
    save('analysis/data/productive_review_summary.json',dict(status='QUALIFIED',mechanisms=len(mechanisms),formulas=len(fs),formula_types={k:sum(f['status']==k for f in fs) for k in {f['status'] for f in fs}},old_claims=old,new_claims=len(claims),added_major=len(claims)-old,added_core=0,coverage=state['pages_examined']))
    from rag.retrieval import Retriever
    r=Retriever(load('rag/index/chunks.json'))
    qs=['Economic Work constant speed labour acceleration','productive transformation cost selling price profit margin','cycle yield efficiency interest quadratic work']
    save('analysis/data/productive_search_audit.json',dict(queries=[dict(query=q,hits=[dict(document=h['document'],page=h['page'],score=h['score']) for h in r.search(q,k=15)]) for q in qs],reading_pages=sorted(examined),scope='All indexed documents searched; targeted return to primary pages; no new extraction.'))

if __name__=='__main__':main()
