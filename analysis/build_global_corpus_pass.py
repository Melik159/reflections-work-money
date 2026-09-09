"""Publish a resumable PARTIAL consolidation; never infer reading from keyword hits."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path
from global_pass_catalog import NOTES, ANALYTICAL, VISUAL, CLAIM_RECHECKS, FINDINGS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/global_corpus_pass'
DOC='Reflections_PierreCampergue.pdf'

def load(path): return json.loads((ROOT/path).read_text())
def write(path, text):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_text()!=text: raise RuntimeError(f'Refusing overwrite: {p}')
    p.write_text(text)
def jwrite(path,data): write(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def csvwrite(path,rows,fields):
    import io
    s=io.StringIO(); w=csv.DictWriter(s,fieldnames=fields);w.writeheader();w.writerows(rows);write(path,s.getvalue())
def norm(s): return ' '.join(s.split())
def append_once(path,addition):
    p=ROOT/path
    if addition not in p.read_text(): p.write_text(p.read_text()+addition)

# Formula transcriptions are editorial, not OCR generated assertions.
FORMULAS=[
('17-01',431,'alphaTM=-(1/V)(∂V/∂UP)_FA','FORMULA_NEW','DEFINITION','V≠0, dérivées locales et contraintes fixes','RQ-08.03'),
('17-02',431,'betaTM=-(1/FA)(∂FA/∂UP)_V','FORMULA_NEW','DEFINITION','FA≠0; ne pas dériver son réciproque','RQ-08.03'),
('17-03',431,'chiTM=(1/V)(∂V/∂FA)_UP','FORMULA_NEW','DEFINITION','V≠0; branche TM','RQ-08.03'),
('17-04',433,'FA=-alphaTM/(betaTM chiTM)','FORMULA_NEW','DERIVATION','Inversibilité locale, dénominateurs non nuls; pas conclusion de préférence autonome','RQ-08.03'),
('17-05',434,'alphaTM=-1/UP','FORMULA_NEW','DERIVATION','rP et FA constants; UP≠0','RQ-05.03'),
('17-06',435,'betaTM=-1/UP','FORMULA_CONFLICT','DERIVATION','Résultat final compatible avec définition; intermédiaire réciproque incompatible','RQ-08.03'),
('17-07',435,'chiTM=-1/FA','FORMULA_NEW','DERIVATION','Core Law, UP constant, FA≠0','RQ-08.03'),
('17-08',436,'alphaMT=(1/B)(∂B/∂UA)_FP','FORMULA_NEW','DEFINITION','B≠0, FP constant','RQ-08.03'),
('17-09',436,'betaMT=(1/FP)(∂FP/∂UA)_B','FORMULA_NEW','DEFINITION','FP≠0, B constant','RQ-08.03'),
('17-10',436,'chiTM=(1/V)(∂V/∂FA)_UP','FORMULA_CONFLICT','PRINTED_DEFINITION','Source imprime TM dans section MT; ligne suivante chiMT,B,FP,UA avec signe moins','RQ-08.03'),
('17-11',437,'FP=alphaMT/(betaMT chiMT)','FORMULA_NEW','DERIVATION','Convention chiMT de la ligne de substitution, non de17-10 imprimée','RQ-08.03'),
('17-12',439,'alphaMT=1/UA','FORMULA_NEW','DERIVATION','rA,FP constants; UA≠0','RQ-05.03'),
('17-13',439,'betaMT=1/UA','FORMULA_CONFLICT','DERIVATION','Résultat final compatible; intermédiaire imprimé au signe opposé','RQ-08.03'),
('17-14',440,'chiMT=1/FP','FORMULA_NEW','DERIVATION','Convention chiMT=-∂B/∂FP/B; pas équivalence silencieuse avec17-10','RQ-08.03'),
('18-03',443,'dT=PhiV dUP+lTM dV','FORMULA_NEW','DERIVATION','Potentiel differentiable, paire UP,V et domaine commun','RQ-08.03'),
('18-04',444,'dT=PhiFA dUP+hTM dFA','FORMULA_NEW','DERIVATION','Paire UP,FA; mêmes conventions','RQ-08.03'),
('18-05',444,'dUP=(∂UP/∂FA)_V dFA+(∂UP/∂V)','FORMULA_CONFLICT','PRINTED_DERIVATION','dV et contrainte finale manquent sur ligne imprimée, reviennent plus bas','RQ-08.03'),
('18-07',445,'dT=lambdaTM dFA+[PhiV (∂UP/∂V)','FORMULA_CONFLICT','PRINTED_DERIVATION','Formule imprimée inachevée; ne pas compléter comme citation','RQ-08.03'),
('18-10',445,'dT=lambdaTM dFA+muTM dV','FORMULA_NEW','DERIVATION','Compatibilité des deux représentations et coefficients','RQ-08.03'),
('18-17',449,'dM=PhiB dUA+lMT dB','FORMULA_NEW','DERIVATION','EMT differentiable, paire UA,B','RQ-08.03'),
('18-18',450,'dM=PhiFP dUA+hMT dFP','FORMULA_NEW','DERIVATION','Potentiel L differentiable, paire UA,FP','RQ-08.03'),
('24-03',501,'p=(1/2)e Ch l/T','FORMULA_REINTERPRETED','DERIVATION','Labour accompli, signe changé explicitement; coût moyen, trajectoire régulière; T≠0','RQ-03.02'),
('24-04',511,'p2≤p1(rP2/rP1)(UP2/UP1)','FORMULA_NEW','PROPOSED_RESTRICTION','Core Law, critère Choice, signes autorisant division et ratios Utility','RQ-05.03'),
('24-08',513,'l2≤l1(rA2/rA1)(UA2/UA1)','FORMULA_NEW','PROPOSED_RESTRICTION','Cash: ratios UA et facteurs rA, même observateur et domaine','RQ-05.03'),
('24-12',519,'pl=(rP/FA(c))UP1(c)-(rP/FA(f))UP2(f)','FORMULA_NEW','DERIVATION','Deux agents, deux instants et frontière location','RQ-07.03'),
('24-13',520,'pl=(rP/FA)(UP1(c)-UA2(c))','FORMULA_NEW','DERIVATION','Égalité Forces et correspondance Product/Cash postulées; échelles compatibles','RQ-05.03'),
('24-17',522,'pl=(r/FA)(UP-UA)','FORMULA_NEW','PROPOSED_RESTRICTION','Emprunteur, indices abrégés; exception spéculation','RQ-07.03'),
('25-01',524,'Mcreated/Mspent≥1','FORMULA_REINTERPRETED','PROPOSED_RESTRICTION','Frontière et horizon, stock antérieur; denominator non nul','RQ-10.02'),
('25-02',524,'Tcreated/Tspent≤1','FORMULA_NEW','PROPOSED_RESTRICTION','Passage depuis ≤gTMgMT requiert borne du produit, pas seules unités communes','RQ-08.02'),
('25-03',526,'P=rP/ln(p)','FORMULA_CONFLICT','PRINTED_DERIVATION','Différentiel p525 dP=-(rP/gTM)dp/p, g/r constants; origine et référence logarithme','RQ-08.03'),
('25-04',526,'A=rA/ln(l)','FORMULA_CONFLICT','PRINTED_DERIVATION','Différentiel p525 dA=-(rA/gMT)dl/l; même défaut local','RQ-08.03'),
('25-05',526,'G=A+P','FORMULA_NEW','PROPOSED_DEFINITION','Addition A,P suppose commensurabilité; Egoism non moral','RQ-08.01'),
('25-07',527,'dMc=gTM dTd+Td dgTM','FORMULA_NEW','DERIVATION','Règle du produit, g variable permis','RQ-08.02'),
('25-08',527,'dMd=(gMT dTc-Tc dgMT)/gMT^2','FORMULA_NEW','DERIVATION','gMT≠0; règle du quotient','RQ-08.02'),
('25-09',528,'gTM dTd+Td dgTM≥(gMT dTc-Tc dgMT)/gMT^2','FORMULA_CONFLICT','PROPOSED_DERIVATION','Mc≥Md ne donne pas automatiquement dMc≥dMd','RQ-08.02'),
('25-10',528,'gTM gMT=dTc/dTd','FORMULA_CONFLICT','PROPOSED_DERIVATION','Constance g ne convertit pas inégalité en égalité; dTd≠0','RQ-08.02'),
('26-01',537,'(∂M)_(n,N)=(n/N)∂u','FORMULA_ALREADY_COVERED','PROPOSED_NORMALIZATION','N ajouté, unité de M changée à préciser','RQ-08.04'),
('26-08',550,'Omega^2=omega^2+varpi^2','FORMULA_ALREADY_COVERED','DEFINITION','Métrique commune pour axes labour/prix','RQ-08.04'),
('26-17',554,'Omega=sqrt(2(M/cA-T/cP))=sqrt(a^2/cA+e^2/cP)','FORMULA_CONFLICT','PRINTED_DERIVATION','Coefficients non unitaires; exposants et conventions pos/neg','RQ-08.04'),
('GDP-final',559,'GDP=K Wconsumed','FORMULA_ALREADY_COVERED','PROPOSED_MACRO_RELATION','Composition, stocks, rendement, pertes, unités; pas causalité établie','RQ-09.03'),
]

def main():
    if (OUT/'manifest.json').exists(): raise SystemExit('Consolidation tranche exists; extend with history, do not rerun initialization.')
    baseline=load('analysis/global_corpus_pass/baseline.json')
    pages={p['page_pdf']:p for p in [json.loads(s) for s in (ROOT/'corpus/extracted'/f'{DOC[:-4]}.pages.jsonl').read_text().splitlines()]}
    claims=[json.loads(s) for s in (ROOT/'analysis/data/claims.jsonl').read_text().splitlines()]
    concepts=load('analysis/data/concepts.json'); graph=load('research_questions/question_graph.json')
    coverage=load('analysis/data/page_coverage.json')
    source_pages=lambda c:set(c['source'].get('pages',[]))|{c['source']['page']}
    qbyclaim=collections.defaultdict(set)
    for q in graph['nodes']:
        for c in q['claims']:qbyclaim[c].add(q['id'])
    findings=[]
    for ident,pp,cc,qq,kind,anchor,interpretation in FINDINGS:
        found=None
        for p in pp:
            t=norm(pages[p]['text']); pos=t.lower().find(norm(anchor).lower())
            if pos>=0:
                found=dict(document=DOC,page=p,quotation=t[max(0,pos-50):min(len(t),pos+len(norm(anchor))+250)],normalization='whitespace')
                break
        if found is None: raise ValueError((ident,anchor))
        findings.append(dict(id=ident,pages=pp,claims=cc,questions=qq,type=kind,SOURCE=found,
            INTERPRETATION=interpretation,full_corpus_reviewed=False))
    jwrite('analysis/global_corpus_pass/findings.json',findings)
    formula_rows=[]
    for i,(label,p,expression,status,kind,conditions,q) in enumerate(FORMULAS,1):
        formula_rows.append(dict(id=f'GC-FORM-{i:03}',label=label,page=p,document=DOC,
            expression=expression,transcription='MANUAL_VISUAL' if p in VISUAL else 'MANUAL_FROM_EXTRACTION',
            status=status,epistemic_type=kind,conditions=conditions,questions=[q],
            variables='Variables et contraintes dans expression et conditions; noms conservés, pas unités SI attribuées.',
            derivation_review=NOTES[p],subsequent_use='Voir contexte et labels; suivi exhaustif non terminé.',
            source_page_sha256=hashlib.sha256(pages[p]['text'].encode()).hexdigest()))
    jwrite('analysis/global_corpus_pass/formulas.json',formula_rows)
    # Formula-label occurrences can be citations of equations, not equations themselves.
    candidates=[]
    for p,row in pages.items():
        for label in sorted(set(re.findall(r'‹(\d{2}-\d{2})›',row['text']))):
            candidates.append(dict(page=p,label=label,method='AUTOMATED_LABEL_OCCURRENCE_NOT_READING',
                editorial_entry=next((f['id'] for f in formula_rows if f['page']==p and f['label']==label),None)))
    jwrite('analysis/global_corpus_pass/formula_candidates.json',candidates)
    # Map editorial relevance by inspected section, never by a machine hit alone.
    def questions(p):
        if p in (20,349): return ['RQ-02.02','RQ-05.01','RQ-05.03']
        if 426<=p<=450:return ['RQ-08.03','RQ-03.03','RQ-05.03']
        if 500<=p<=508:return ['RQ-05.01','RQ-03.02','RQ-07.02']
        if 509<=p<=517:return ['RQ-05.02','RQ-05.03']
        if 518<=p<=522:return ['RQ-07.03','RQ-05.03','RQ-08.01']
        if 523<=p<=533:return ['RQ-08.02','RQ-08.03','RQ-10.02','RQ-06.02']
        if 534<=p<=535:return ['RQ-02.02','RQ-07.01','RQ-05.03']
        if 536<=p<=540:return ['RQ-08.04','RQ-02.01','RQ-12.01']
        if 541<=p<=545:return ['RQ-08.03','RQ-09.02']
        if 546<=p<=547:return ['RQ-08.03','RQ-03.02','RQ-05.03']
        if 548<=p<=558:return ['RQ-08.04','RQ-03.02']
        if p==559:return ['RQ-08.02','RQ-09.03','RQ-10.02']
        if p>=560:return ['RQ-12.01','RQ-12.02']
        return []
    structure=load('analysis/data/manuscript_structure.json')
    matrix=[]
    for p in range(1,563):
        cc=[c['id'] for c in claims if p in source_pages(c)]
        cids=[c['id'] for c in concepts if p in c['source_pages']]
        local_findings=[f for f in findings if p in f['pages']]
        cc=sorted(set(cc)|{c for f in local_findings for c in f['claims']})
        qs=sorted(set(questions(p))|{q for f in local_findings for q in f['questions']}) if p in NOTES else []
        sections=[s for s in structure if len(s['pages'])==2 and s['pages'][0]<=p<=s['pages'][1]]
        section=min(sections,key=lambda s:s['pages'][1]-s['pages'][0])['title'] if sections else 'Front matter / annexe / section à préciser'
        matrix.append(dict(page=p,section=section,scan_status='ANALYTICALLY_REVIEWED' if p in ANALYTICAL else 'SCANNED' if p in NOTES else 'UNREVIEWED',
            questions=';'.join(qs),claims=';'.join(cc),concepts=';'.join(cids),
            formulas=';'.join(f['id'] for f in formula_rows if f['page']==p),
            importance='HISTORICAL_CONTEXT' if p in (561,562) else 'ILLUSTRATIVE' if p in (430,531,541,542,543,544,545) else 'STRUCTURAL' if p in NOTES else 'PENDING',
            notes=NOTES.get(p,'Non relue dans cette passe. Liens de claims/concepts hérités, non certification sémantique.'),
            historical_analytically_reviewed=coverage[p-1]['examined'],visual_checked=p in VISUAL))
    csvwrite('analysis/global_corpus_pass/page_matrix.csv',matrix,list(matrix[0]))
    # Every planned block exists, but pending blocks explicitly contain NO reading claim.
    for start in range(1,563,25):
        end=min(start+24,562); viewed=[r for r in matrix if start<=r['page']<=end and r['scan_status']!='UNREVIEWED']
        partial=len(viewed)<end-start+1
        status='REQUIRES_REVIEW' if partial else 'POTENTIAL_CONTRADICTION'
        text=f'# Bloc PDF {start:03}–{end:03}\n\nStatut : {status}. Pages effectivement parcourues : {len(viewed)}/{end-start+1}.\n\n'
        text+='SOURCE : texte extrait par page, et rendu PDF pour les pages indiquées. Les notes ci-dessous sont INTERPRETATION. Aucune lecture déduite des recherches automatiques.\n\n'
        if not viewed:text+='Bloc non commencé. Sections, formules et exceptions restent à examiner; aucune conclusion NO_NEW_MATERIAL.\n'
        for r in viewed:text+=f"## PDF {r['page']} — {r['scan_status']}\n\n{r['notes']}\n\nQuestions : {r['questions']}. Claims liés : {r['claims'] or 'aucun claim canonique; voir candidats et questions'}. Formules : {r['formulas'] or 'voir texte/figures, inventaire détaillé non terminé'}. Visuel : {r['visual_checked']}.\n\n"
        text+='\nConflits, exceptions, exemples et références : voir entrées paginées ci-dessus et `../findings.json`. Les étiquettes de section héritées ne valent pas reconstruction nouvelle de la table des matières.\n'
        write(f'analysis/global_corpus_pass/blocks/p{start:03}_p{end:03}.md',text)
    rechecks=[]
    for c in claims:
        status,pp,reason=CLAIM_RECHECKS.get(c['id'],(None,[],'Relecture transversale non terminée; contrôle de citation automatique distinct.'))
        rechecks.append(dict(id=c['id'],criticality=c['criticality'],old_statement=c['statement'],new_statement=c['statement'],
            local_review_status=status,pages_reviewed=pp,reason=reason,canonical_action='UNCHANGED',
            global_review_status=None,full_corpus_reviewed=False,
            history_action='LOCAL_RECHECK_ONLY' if status else 'PENDING',
            source_unchanged=c['source']))
    jwrite('analysis/global_corpus_pass/claim_rechecks.json',rechecks)
    # Preserve old notices before fixing a genuine positive/negative copy error and stale audit text.
    amendments=[]
    replacements={
      'unproductive': ('definition_by_campergue','Le passage appelle « unproductive work » le travail qui ne permet pas de réduction du prix; ne pas effacer l’alternance coût/prix dans cette phrase.'),
      'cycle': ('ambiguities',['Quatre étapes analogiques; cycles examinés dans les passes productive et formelle. Le suivi intégral des usages et signes reste inachevé.']),
      'entropy': ('ambiguities',['Exclue du formalisme économique p36; section physique informative p463–464 examinée dans la passe terminale. Ne pas confondre ces périmètres.']),
    }
    for c in concepts:
        if c['id'] in replacements:
            field,value=replacements[c['id']]
            amendments.append(dict(id=c['id'],field=field,old_value=c[field],new_value=value,
                reason='Erreur de copie pour unproductive (source p20 relue); statut d’examen vieilli pour cycles/entropie, pas nouvelle définition attribuée.',
                source_pages=c['source_pages'],source_review='NEW_PAGE_REVIEW' if c['id']=='unproductive' else 'EXISTING_RESEARCH_RECONCILIATION'))
            c[field]=value
    (ROOT/'analysis/data/concepts.json').write_text(json.dumps(concepts,ensure_ascii=False,indent=2)+'\n')
    jwrite('analysis/global_corpus_pass/concept_amendments.json',amendments)
    # Previous examined flags never disappear. New analytical coverage has per-page notes.
    for row in coverage:
        p=row['page']
        if p in ANALYTICAL:
            if not row['examined']:
                row['examined']=True
                row['reason']='GLOBAL_PASS_LOCAL_ANALYTICAL_NOTE'
                row['reading_note']=f'../global_corpus_pass/blocks/p{((p-1)//25)*25+1:03}_p{min(((p-1)//25)*25+25,562):03}.md'
            row['global_pass_note']=f'analysis/global_corpus_pass/blocks/p{((p-1)//25)*25+1:03}_p{min(((p-1)//25)*25+25,562):03}.md'
    (ROOT/'analysis/data/page_coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    questions_review=[]
    for q in graph['nodes']:
        pp=[r['page'] for r in matrix if q['id'] in r['questions'].split(';')]
        questions_review.append(dict(id=q['id'],pages_this_pass=pp,full_corpus_coverage_verified=False,status_unchanged=q['status']))
    jwrite('analysis/global_corpus_pass/question_rechecks.json',questions_review)
    for q in questions_review:
        if not q['pages_this_pass']:continue
        fs=[f for f in findings if q['id'] in f['questions']]
        content=f"# Consolidation partielle — {q['id']}\n\nStatut scientifique conservé : {q['status_unchanged']}. Pas de revue du manuscrit complet acquise.\n\nPages de cette passe : {q['pages_this_pass']}.\n\nSOURCE et INTERPRETATION séparées dans [le registre paginé](../../analysis/global_corpus_pass/findings.json).\n\n"
        for f in fs:content+=f"- {f['id']} ({f['type']}), PDF {f['pages']} : {f['INTERPRETATION']}\n"
        content+='\nCe supplément ne remplace ni evidence.md ni conclusion.md. Les nouvelles tensions restent à intégrer après examen des sources antérieures et des dépendances; aucun statut promu automatiquement.\n'
        write(f"research_questions/{q['id']}/global_consolidation.md",content)
    candidates=[
        dict(id='GC-CAND-01',statement='La substitution concurrentielle est régie par un rapport de Utility/price et r sous Core Law.',pages=[511,512,513],questions=['RQ-05.02','RQ-05.03'],action='CANDIDATE_NOT_CANONICAL'),
        dict(id='GC-CAND-02',statement='Location et crédit sont reconstruits par achat/revente et différence entre Utility de Product et de Cash.',pages=[518,519,520,521,522],questions=['RQ-07.03','RQ-05.03'],action='CANDIDATE_NOT_CANONICAL'),
        dict(id='GC-CAND-03',statement='Les services sont largement exclus de création globale, avec critère final Utility et exception d’efficacité des intermédiaires.',pages=[534,535,540],questions=['RQ-02.02','RQ-07.01'],action='SPLIT_SCOPE_CANDIDATE_NOT_CANONICAL'),
        dict(id='GC-CAND-04',statement='La fréquence des cas satisfaisant Core Law sert de classement de richesse par tranches de vingt pour cent.',pages=[529,530],questions=['RQ-01.02','RQ-02.01'],action='CANDIDATE_NOT_CANONICAL'),
        dict(id='GC-CAND-05',statement='La chaîne offre→prix→demande est affirmée directe, avec retour demande→offre et hétérogénéité de Utility.',pages=[509,510,514,515,516,517],questions=['RQ-05.02'],action='CANDIDATE_NOT_CANONICAL'),
    ]
    jwrite('analysis/global_corpus_pass/claim_candidates.json',candidates)
    report=dict(status='GLOBAL_CORPUS_PASS_INCOMPLETE',pages_scanned=len(NOTES),pages_total=562,
        analytical_this_pass=len(ANALYTICAL),deep_this_pass=0,historical_analytical_before=baseline['historical_analytically_reviewed'],
        cumulative_analytical_after=sum(r['examined'] for r in coverage),
        pending_pages=[p for p in range(1,563) if p not in NOTES],
        claims_total=len(claims),new_canonical_claims=0,claim_candidates=len(candidates),
        locally_rechecked_claims=len(CLAIM_RECHECKS),globally_rechecked_core=0,globally_rechecked_major=0,
        questions_existing=53,questions_added=0,questions_deprecated=0,
        question_tree_sufficiency='NOT_YET_ASSESSED_AGAINST_FULL_CORPUS',
        formula_editorial_entries=len(formula_rows),formula_label_candidates=len(candidates),
        formulas_exhaustive=False,known_new_findings=len(findings),
        ready_for_synthesis=False,verification_status='PENDING_EXECUTION')
    report['formula_label_candidates']=len(load('analysis/global_corpus_pass/formula_candidates.json'))
    jwrite('analysis/global_corpus_pass/manifest.json',report)
    write('analysis/global_corpus_pass/formula_inventory.md','# Formules — inventaire partiel\n\n'+
        'Les occurrences automatiques de labels ne sont ni une lecture ni un inventaire exhaustif des formules structurantes. Les fiches antérieures sont conservées dans analysis/data/productive_formulas.json et les passes formelles. FORMULA_NEW signifie ajout à cette tranche éditoriale, pas nouveauté historique.\n\n'+
        '| ID | PDF | Label | Statut | Conditions / diagnostic |\n|---|---|---|---|---|\n'+''.join(f"| {f['id']} | {f['page']} | {f['label']} | {f['status']} | {f['conditions']} |\n" for f in formula_rows))
    write('research_questions/global_question_coverage.md','# Couverture transversale des questions — INCOMPLETE\n\n'+
        f"53 questions conservées. {len(NOTES)}/562 pages parcourues dans cette passe; 562 lignes de matrice ne signifient pas 562 pages examinées.\n\n"+
        'Les passages importants inspectés sont rattachés à des questions; cadres RQ-05.02 et RQ-07.03 peuvent accueillir les nouveaux exemples concurrence/location sans créer de questions artificielles. La suffisance des 53 questions ne peut pas encore être certifiée sur le manuscrit complet. Ni SUFFICIENT ni REQUIRES_RESTRUCTURING ne sont établis à ce stade.\n\n'+
        '[Matrice paginée](../analysis/global_corpus_pass/page_matrix.csv) · [Révisions locales](../analysis/global_corpus_pass/question_rechecks.json) · [Candidats claims](../analysis/global_corpus_pass/claim_candidates.json).\n\n'+
        'Les dossiers concernés reçoivent global_consolidation.md, sans réécriture ni résolution de leur conclusion. Les questions sans nouvelle page restent en attente, pas orphelines par défaut.\n')
    append_once('research_questions/README.md','\n## Consolidation transversale — tranche incomplète\n\n[Rapport](../analysis/global_corpus_pass/final_report.md) · [couverture réelle](global_question_coverage.md). Les pages non relues restent UNREVIEWED; aucun certificat de lecture intégrale ni synthèse finale.\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
