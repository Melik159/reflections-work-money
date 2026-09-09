"""Controlled append-only first-series runner. No global synthesis or push."""
import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml
from rag.iterative import load_claims,search,INDEX,ROOT

S=ROOT/'research_state'
PDF='Reflections_PierreCampergue.pdf'
CONFIG=[
 dict(id='CYCLE-001',topic='Money / référents',rq=['RQ-06.01','RQ-06.04','RQ-09.03'],
      pages=[204,205,206,207,208,254,255,256,257,258,466,467,468,469],
      roles=['AGENT-CORPUS','AGENT-MONEY','AGENT-FORMAL','AGENT-ADVERSARIAL'],query='Money kinetic potential saving total money',
      source_page=256,quote='(in a lossless system)',
      finding='La conservation du total est conditionnée par un système sans pertes (256–257); 468–469 relient M à une différence puis à un transfert entre composantes. Conserver les référents séparés. Un bilan de composantes peut tester une hypothèse de clôture sans mesurer Money.',
      hypothesis='RESEARCH_INTERPRETATION: si C+P est un total fermé, ΔC+ΔP=0. Avec entrées I et pertes L explicitement ajoutées par le chercheur, ΔC+ΔP=I−L. Les pages ne constituent pas une mesure de I ou L.',
      criterion='Somme inchangée seulement dans le bilan fermé ou si I=L; le changement des composantes ne suffit pas à identifier un gain réel. Aucun test de causalité.',
      alternatives='Identité de bilan usuelle; une conservation postulée ne distingue pas un mécanisme économique.',
      gap='Mesurer séparément composantes, entrées, pertes, frontière et horizon; éviter de baptiser un résidu Money.',
      existing=['remediation/money_referents.md','remediation/money_gdp_bridge.md','external_review/02_formal_review.md']),
 dict(id='CYCLE-002',topic='T / cp : changement de l’unité de tâche',rq=['RQ-03.02','RQ-03.03'],
      pages=list(range(201,211)),roles=['AGENT-CORPUS','AGENT-FORMAL','AGENT-MEASUREMENT','AGENT-ADVERSARIAL'],query='complexity constant speed Economic Work cp',
      source_page=201,quote='the climbing of a single rung',
      finding='Le choix de l’opération élémentaire p201 impose de distinguer reparamétrage et changement réel de productivité. Sous T=½cpω², conserver T quand ω devient sω exige cp→cp/s²; garder cp numérique fixe crée artificiellement un facteur s².',
      hypothesis='MINIMAL_RECONSTRUCTION, non notation source: l′=s l, ω′=sω, T′=T, cp′=cp/s² et F′=F/s. Pas une preuve que le manuscrit fournit cet étalonnage.',
      criterion='Pour s>0, invariance numérique de T sous transformation conjointe; non-invariance si cp reste numériquement fixe. Force et cp ne deviennent pas observés.',
      alternatives='Covariance dimensionnelle générale; n’est pas une restriction empirique propre à Campergue.',
      gap='Définir l’unité physique de tâche et une calibration indépendante avant comparaison interprocédés.',
      existing=['research_questions/RQ-03.03/conclusion.md','research_questions/experiments/EXP-09/results.md']),
 dict(id='CYCLE-003',topic='Utility : comparabilité entre référents',rq=['RQ-05.03','RQ-08.01','RQ-12.02'],
      pages=[108,109,110,111,384,385,386,387],roles=['AGENT-CORPUS','AGENT-MEASUREMENT','AGENT-FORMAL','AGENT-ADVERSARIAL'],query='Utility measurement order ratio yield',
      source_page=109,quote="in the absence of measurement, it's always possible to",
      finding='Le besoin d’une échelle de rapport ne suffit pas à lui seul : comparer deux référents requiert aussi une calibration commune. Une multiplication commune laisse 1−U2/U1 inchangé; deux calibrations indépendantes peuvent même faire changer son signe.',
      hypothesis='RESEARCH_INTERPRETATION: le rendement réversible p386 utilise un quotient sur un domaine 0≤U2≤U1, U1>0. Tester recodage commun et recodages indépendants; ne pas attribuer ces derniers comme autorisés par Campergue.',
      criterion='Une échelle commune conserve le rendement; deux échelles indépendantes ne le déterminent pas. Un résultat hors domaine après recodage ne réfute pas le résultat conditionnel source.',
      alternatives='Problème général de comparabilité des mesures; pas de signature économique indépendante.',
      gap='Vérifier si Utility désigne un même étalon selon produits/agents/étapes avant d’estimer un rendement.',
      existing=['research_questions/RQ-05.03/conclusion.md','research_questions/experiments/EXP-02/results.md'])]

# Existing algebra was found in fourth-pass artifacts; do not execute it anew.
CONFIG[1].update(
    topic='T / cp : admissibilité d’un protocole indépendant',
    finding='Le changement d’unité était déjà traité dans EXP-09. La nouveauté de ce cycle est un filtre de protocole: exclure T construit par la loi testée, exiger étalonnage indépendant, unité de tâche et échantillon de contrôle. Ce filtre ne fournit aucun capteur.',
    hypothesis='RESEARCH_INTERPRETATION: un protocole ne peut prétendre tester indépendamment T∝ω² si T est construit uniquement par cette relation. Les champs de provenance sont déclaratifs et doivent être audités.',
    criterion='Le protocole synthétique circulaire doit être refusé; un schéma renseignant les exigences peut être admissible sur la forme, sans établir sa faisabilité ni son indépendance réelle.')
CONFIG[2].update(
    topic='Utility : admissibilité de la calibration d’un rendement',
    finding='EXP-02 identifiait déjà le problème de comparabilité. La nouveauté documentaire est un filtre refusant une entrée ordinale ou des échelles de rapport non raccordées pour estimer le rendement p386. Aucun rendement économique n’est estimé.',
    hypothesis='RESEARCH_INTERPRETATION: un protocole pour le quotient de Utility doit déclarer échelle de rapport, calibration commune, contexte compatible et dénominateur positif. Ces critères ne prouvent pas une mesure.',
    criterion='Refuser un classement ordinal et des échelles indépendantes; accepter seulement la complétude déclarative du schéma commun. Faisabilité empirique reste BLOCKED_BY_MEASUREMENT.')

def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def js(p,value):write(p,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def tasks():return yaml.safe_load((S/'NEXT_ACTIONS.yaml').read_text())
def save_tasks(value):write(S/'NEXT_ACTIONS.yaml',yaml.safe_dump(value,allow_unicode=True,sort_keys=False))

def bootstrap():
    if (S/'NEXT_ACTIONS.yaml').exists():raise SystemExit('Existing research state: bootstrap refused')
    cs=load_claims(); ts=[]
    rest=[('K','RQ-08.02'),('Energy → Economic Work','RQ-09.02'),('Innovation / productivity','RQ-04.01'),('Destination des gains','RQ-10.02'),('Dommages environnementaux','RQ-11.01'),('Programme épistémologique','RQ-01.01'),('Review adversariale transversale','RQ-12.01')]
    valid={n['id'] for n in json.loads((ROOT/'research_questions/question_graph.json').read_text())['nodes']}
    for i in range(10):
        cfg=CONFIG[i] if i<3 else None
        rq=cfg['rq'] if cfg else [rest[i-3][1]]
        assert set(rq)<=valid
        nodes=json.loads((ROOT/'research_questions/question_graph.json').read_text())['nodes']
        ids=sorted({c for n in nodes if n['id'] in rq for c in n.get('claims',[])})
        ts.append(dict(id=f'TASK-{i+1:03}',priority=i+1,topic=cfg['topic'] if cfg else rest[i-3][0],
            question=next(n['question'] for n in nodes if n['id']==rq[0]),related_rq=rq,related_claims=ids,
            pages_hint=cfg['pages'] if cfg else [],required_sources=cfg['existing'] if cfg else ['closure_review/final_open_questions.md'],
            status='OPEN',created_from='Consolidated baseline and user initial priorities',notes='Priority provisional; no automatic scientific conclusion.'))
    save_tasks(ts)
    write(S/'DECISIONS.md','# Décisions\n\nDEC-0001 — Baseline conservée. Ancien état: pas de registre itératif. Nouvel état: registre séparé; aucun claim ni statut RQ modifié. Sources: clôture et dossiers RQ. Tests: manifeste gelé et validation de chaque cycle. Confiance HIGH sur la séparation documentaire.\n')
    write(S/'OPEN_CONTRADICTIONS.md','# Désaccords ouverts\n\nAucun désaccord nouveau tranché par vote. Les tensions de clôture restent ouvertes; ne pas les compter comme découvertes nouvelles.\n\nDISPUTE-0001 — OPEN, réenregistrement d’une ambiguïté existante\n\nPosition A (AGENT-MONEY, lecture charitable): p256 et 469 conservent un total et décrivent une conversion interne; le gain n’est pas une émission.\n\nPosition B (AGENT-MEASUREMENT): p204/207/468 ne suffisent pas à établir que le gain, la primitive et les deux composantes partagent un étalon indépendant.\n\nSources: PDF204–208,254–258,466–469; remediation/money_referents.md. RQ-06.01, RQ-09.03. Les claims associés sont listés dans CYCLE-001.\n\nTest de résolution: spécifier frontière/étalon/horizon, mesurer séparément les composantes et le gain, vérifier leur raccord sans définir la seconde composante comme résidu. Statut scientifique AMBIGUOUS; pas contradiction démontrée.\n')
    # Exact counts, not an invented claim of new analytical coverage.
    used={p for c in cs if c['source']['document']==PDF for p in c['source'].get('pages',[c['source']['page']])}
    gaps=[p for p in range(1,563) if p not in used]
    js(S/'coverage_gaps.json',dict(total_pages=562,pages_not_directly_cited_by_claim=gaps,meaning='No direct claim citation does not mean unread or unimportant; baseline already scanned all pages.',scope='Claims only; section/formula/RQ usage audit pending'))
    write(S/'COVERAGE_GAPS.md',f'# Couverture à approfondir\n\n562/562 pages déjà scannées, 447 analysées dans la baseline. {len(gaps)} pages sans citation directe dans les claims actuels. Liste complète: coverage_gaps.json. Ce n’est ni un manque de lecture démontré ni une raison de créer des claims.\n\nAudit restant: sections peu citées, fréquence des formules, exemples non rattachés aux RQ et définitions tardives. Ne pas les déclarer contrôlés depuis ce seul indicateur.\n')
    write(S/'RESEARCH_LEDGER.md','# Registre de recherche\n\nQuestions prioritaires: Money/référents et raccord PIB; mesure indépendante de T/cp; comparabilité de Utility; K/composition; énergie utile; allocation des gains; fonction de dommages. Référence: closure_review/final_open_questions.md.\n\nConcepts instables: T/dT, cp, Utility, Money et K. Claims à relire: ceux des tâches dans NEXT_ACTIONS.yaml; aucun nouveau statut de vérité.\n\nPreuves manquantes: étalonnages indépendants, mesures appariées coûts/prix/qualité, frontière de bilan, destination marginale et empreinte. Tests prioritaires: invariance des unités et conditions de comparaison; aucun R² causal.\n\nLittérature à chercher plus tard: invariance des mesures, comparabilité interpersonnelle, identification des réponses énergétiques et des chocs productifs. Pas de nouvelle source externe vérifiée dans cette série.\n\nDécouvertes et diagnostics: voir cycles/*/results.json et iteration_report.md; toujours distinguer SOURCE, INTERPRETATION et FORMAL_RESULT.\n')
    js(S/'baseline_guard.json',{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'manifest_sha256':hashlib.sha256((ROOT/'closure_review/BASELINE_MANIFEST_SHA256.txt').read_bytes()).hexdigest()})

def prepare(n):
    cfg=CONFIG[n-1];d=S/'cycles'/cfg['id'];ts=tasks();task=ts[n-1]
    if task['status']!='OPEN':raise SystemExit('Only OPEN task can be prepared')
    # Human caller must actually inspect source pages; output is a record, not reading automation.
    pages={r['page_pdf']:r for r in map(json.loads,(ROOT/'corpus/extracted/Reflections_PierreCampergue.pages.jsonl').read_text().splitlines())}
    assert cfg['quote'] in ' '.join(pages[cfg['source_page']]['text'].split())
    source='\n\n'.join(f"## SOURCE — PDF {p}\n\n{pages[p]['text']}" for p in cfg['pages'])
    write(d/'source_pages.md','# Pages sources et contexte\n\n'+source)
    linked=[c for c in load_claims() if c['id'] in task['related_claims']]
    js(d/'claims_before.json',linked)
    rows=[r for r in json.loads(INDEX.read_text())['rows'] if r['collection']=='SOURCE_CORPUS' and r['level']=='PAGE']
    js(d/'retrieval.json',dict(query=cfg['query'],hits=search(rows,cfg['query'],k=5)))
    write(d/'protocol.md',f"# {cfg['id']} — {cfg['topic']}\n\nQUESTION: {task['question']}\n\nROLES: {', '.join(cfg['roles'])}\n\nSOURCE: PDF pages {cfg['pages']}; contextes archivés dans source_pages.md. Images contrôlées: 207,386,468 selon pertinence.\n\nHYPOTHESIS\n\n{cfg['hypothesis']}\n\nCRITERIA BEFORE CALCULATION\n\n{cfg['criterion']}\n\nALTERNATIVE EXPLANATIONS\n\n{cfg['alternatives']}\n\nMEASUREMENT\n\nDonnées synthétiques seulement; T, cp, Utility et Money ne deviennent pas des observations.\n\nINTERPRETATION / CURRENT RECONSTRUCTION\n\n{cfg['finding']}\n\nEXISTING CLAIM CHECK\n\nAttribution et qualifications conservées, aucun claim changé. Dossiers relus: {cfg['existing']}.\n\nREMAINING UNCERTAINTY\n\n{cfg['gap']}\n")
    task['status']='IN_PROGRESS';save_tasks(ts)

def measurement_gate(record,kind):
    """A protocol acceptance guard, not a determination that measurements exist."""
    if kind=='T':
        return record.get('T_origin')=='INDEPENDENT_SENSOR' and record.get('cp_origin')=='INDEPENDENT_CALIBRATION' and bool(record.get('task_unit')) and record.get('holdout',False)
    return record.get('scale')=='RATIO' and record.get('common_calibration',False) and record.get('denominator_positive',False) and record.get('same_context',False)

def formal(n):
    if n==1:
        rows=[]
        for injection,loss in [(0,0),(3,0),(0,2),(2,2)]:
            c0,p0,transfer=8,12,4;c1=c0-transfer;p1=p0+transfer+injection-loss
            change=c1+p1-c0-p0;assert change==injection-loss
            rows.append(dict(injection=injection,loss=loss,total_change=change,conserved=change==0))
        return rows
    if n==2:
        proposed=dict(T_origin='INDEPENDENT_SENSOR',cp_origin='INDEPENDENT_CALIBRATION',task_unit='predefined',holdout=True)
        circular=dict(proposed,T_origin='HALF_CP_OMEGA_SQUARED')
        return dict(proposed_design_accepted=measurement_gate(proposed,'T'),circular_design_accepted=measurement_gate(circular,'T'),
                    data_available=False,empirical_status='BLOCKED_BY_MEASUREMENT',limitation='Self-declared metadata require audit; no independent T sensor has been identified.')
    proposed=dict(scale='RATIO',common_calibration=True,denominator_positive=True,same_context=True)
    independent=dict(proposed,common_calibration=False)
    ordinal=dict(proposed,scale='ORDINAL')
    return dict(proposed_design_accepted=measurement_gate(proposed,'Utility'),independent_scales_accepted=measurement_gate(independent,'Utility'),
                ordinal_accepted=measurement_gate(ordinal,'Utility'),data_available=False,empirical_status='BLOCKED_BY_MEASUREMENT',
                limitation='Protocol schema only. Shared ratio calibration has not been supplied by these flags.')

def finish(n):
    cfg=CONFIG[n-1];d=S/'cycles'/cfg['id'];ts=tasks()
    if ts[n-1]['status']!='IN_PROGRESS':raise SystemExit('Prepare first; DONE cycles immutable')
    result=dict(cycle=cfg['id'],kind='LOCAL_FORMAL_DIAGNOSTIC' if n==1 else 'PROTOCOL_METADATA_GUARD',status=['FORMALLY_QUALIFIED','NON_DISCRIMINATING'] if n==1 else ['BLOCKED_BY_MEASUREMENT','NON_DISCRIMINATING'],
                data_origin='SYNTHETIC',empirical_observation=False,result=formal(n),claims_changed=[],questions_changed=[],
                finding=cfg['finding'],confidence='HIGH for conditional calculation; LOW for empirical identification')
    js(d/'results.json',result)
    for name,cmd in [('verify',['bash','./verify.sh']),('state_tests',[sys.executable,'-m','unittest','research_state.test_state','-v']),('baseline_manifest',['sha256sum','--quiet','-c','closure_review/BASELINE_MANIFEST_SHA256.txt'])]:
        proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        write(d/(name+'.log'),proc.stdout+proc.stderr)
        if proc.returncode:raise SystemExit(f'{name} FAIL: see {d}; task remains IN_PROGRESS')
    ts[n-1]['status']='DONE';save_tasks(ts)
    new_tasks=[]
    if n in [2,3]:
        follow=dict(ts[n-1]);follow.update(id=f'TASK-{n+9:03}',priority=1,status='BLOCKED',
            topic='Étalonnage indépendant T/cp' if n==2 else 'Calibration commune de Utility',
            created_from=cfg['id'],required_sources=['research_state/calibration_protocols.md'],
            notes='NEEDS_DEFINITION: aucune mesure indépendante disponible; tâche scientifique distincte du contrôle documentaire terminé.')
        if not any(t['id']==follow['id'] for t in ts):ts.append(follow);new_tasks.append(follow['id']);save_tasks(ts)
    next_task=next((t['id'] for t in sorted(ts,key=lambda x:x['priority']) if t['status']=='OPEN'),None)
    summary=f"# {cfg['id']}\n\nROLE(S): {', '.join(cfg['roles'])}\n\nTASK: TASK-{n:03} — {cfg['topic']}\n\nSOURCES READ: {cfg['existing']}; source_pages.md, claims_before.json\n\nPAGES READ: {cfg['pages']}\n\nCLAIMS TOUCHED: none modified; consulted {ts[n-1]['related_claims']}\n\nQUESTIONS TOUCHED: {cfg['rq']} — statuses unchanged\n\nNEW FINDINGS: {cfg['finding']}\n\nDISPUTES: DISPUTE-0001 remains OPEN; no newly resolved disagreement.\n\nTESTS: conditional diagnostic and state guards; not independent economic evidence.\n\nVERIFY RESULT: PASS (128 baseline tests plus state tests); scientific WARNING retained.\n\nNEW TASKS CREATED: no additional task beyond initial queue; next task retains the measurement gap.\n\nNEXT RECOMMENDED TASK: {next_task}\n"
    if new_tasks:summary=summary.replace('no additional task beyond initial queue; next task retains the measurement gap.',str(new_tasks)+' — BLOCKED / NEEDS_DEFINITION; no empirical measurement supplied.')
    write(d/'cycle.md',summary);write(S/'LAST_CYCLE.md',summary)
    with (S/'DECISIONS.md').open('a') as f:f.write(f"\n\nDEC-{n+1:04} — {cfg['id']}; date {datetime.now(timezone.utc).isoformat()}. Target: TASK-{n:03}. Old IN_PROGRESS → DONE. No claim/RQ status change. Reason: {cfg['finding']} Sources: {cfg['pages']}; tests: {cfg['id']}/results.json, verify.log. Confidence: HIGH conditional / LOW empirical.\n")

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['bootstrap','prepare','finish']);p.add_argument('n',type=int,nargs='?');a=p.parse_args()
    if a.action=='bootstrap':bootstrap()
    else:globals()[a.action](a.n)
