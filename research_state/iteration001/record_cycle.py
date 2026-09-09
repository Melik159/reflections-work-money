"""Record an explicitly reviewed decision supplied by the orchestrator. No inference."""
import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
def record(n, *, decision, finding_class, finding, counterevidence, negative, proposed, reason, confidence, impact, domain, evidence_text, experiment, tests='Aucun nouveau test exécuté; protocole seulement.'):
    cycle=f'ITER001-C{n:02}'
    report=ROOT/'agents/reports'/cycle
    tasks=yaml.safe_load((ROOT/'research_state/NEXT_ACTIONS.yaml').read_text())
    task=next(t for t in tasks if t['id']==f'ITER001-P0-{n:02}')
    for role in ['specialist','adversarial']:
        if not (report/f'{role}.md').is_file():raise RuntimeError(f'Missing {role} review')
    (report/'evidence.md').write_text(f'# AGENT-EVIDENCE — {cycle}\n\nReviewer: orchestrateur /root, distinct role, not institutional independence.\n\n'+evidence_text+'\n\nConclusion → question → claims → pages source → limites/test → statut est contrôlé pour le candidat ci-dessous; aucun statut canonique modifié.\n')
    reviewers={r:str((report/f'{r}.md').relative_to(ROOT)) for r in ['specialist','adversarial','evidence']}
    candidate_path=f'candidate_changes/{domain}/{cycle}.json'
    candidate=dict(id=cycle,target=[f'research_questions/{q}/conclusion.md' for q in task['related_rq']],current_state='Baseline figée; statuts et qualifications inchangés. Voir graphe et conclusions canoniques ainsi que spécialiste pour état précis.',proposed_state=proposed,evidence=list(reviewers.values()),counterevidence=counterevidence,reviewers=reviewers,confidence=confidence,reason=reason,impact=impact,decision=decision,finding_class=finding_class,claims=task['related_claims'],questions=task['related_rq'],source_pages=task['pages_hint'],scientific_scope='Candidat de recherche séparé, aucune intégration baseline. Diagnostic/protocole analyste; aucune mesure empirique nouvelle.',negative_results=negative)
    (ROOT/candidate_path).write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n')
    exp=dict(id=f'ITER001-EXP-{n:02}',question=task['question'],claims=task['related_claims'],**experiment)
    exps=yaml.safe_load((ROOT/'research_state/EXPERIMENT_QUEUE.yaml').read_text())
    assert not any(e['id']==exp['id'] for e in exps)
    exps.append(exp)
    (ROOT/'research_state/EXPERIMENT_QUEUE.yaml').write_text(yaml.safe_dump(exps,sort_keys=False,allow_unicode=True))
    out=ROOT/f'research_state/iteration001/C{n:02}'
    out.mkdir(exist_ok=True)
    data=dict(id=cycle,task=task['id'],decision=decision,finding_class=finding_class,finding=finding,claims=task['related_claims'],questions=task['related_rq'],sources=list(reviewers.values()),reviewers=reviewers,candidate_path=candidate_path,negative_results=negative,scientific_scope=candidate['scientific_scope'],tests=tests,experiment=exp['id'])
    (out/'decision.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    next_task=f'ITER001-P0-{n+1:02}' if n<10 else 'STOP — lot terminé; consulter NEXT_ACTIONS pour session future'
    cycle_text=f'''# {cycle}

CYCLE: {cycle}
TASK: {task['id']} — {task['question']}
ROLES: {', '.join(task['roles'])}; rôles IA, pas certification indépendante.
SOURCES: {reviewers}; source primaire et provenance détaillées dans specialist.md.
PAGES: {task['pages_hint']} (repères; pages effectivement lues dans le rapport spécialiste).
CLAIMS: {task['related_claims']} — aucun modifié.
QUESTIONS: {task['related_rq']} — statuts canoniques inchangés.
FINDINGS: {finding}
COUNTEREVIDENCE: {counterevidence}
DISPUTES: DISPUTE-0001 hérité reste OPEN; voir OPEN_DISPUTES.md pour divergences nouvelles éventuelles.
TESTS: {tests}
CANDIDATE_CHANGES: {candidate_path} — {decision}
VERIFY: suite baseline 128/128 dans copie isolée au démarrage; contrôle final après modifications structurantes, voir agents/logs/batch001/ et iteration_report_001.md. Ce champ n'atteste pas une exécution par cycle.
NEXT_TASK: {next_task}
'''
    (out/'cycle.md').write_text(cycle_text)
    (ROOT/'research_state/LAST_CYCLE.md').write_text(cycle_text)
    task['status']='DONE'
    task['completion_scope']='Revue et proposition terminées; question scientifique non résolue automatiquement'
    task['result']=str((out/'decision.json').relative_to(ROOT))
    if n<10:next(t for t in tasks if t['id']==next_task)['status']='RUNNING'
    (ROOT/'research_state/NEXT_ACTIONS.yaml').write_text(yaml.safe_dump(tasks,allow_unicode=True,sort_keys=False))
    with (ROOT/'research_state/DECISIONS.md').open('a') as f:f.write(f'\n## {cycle} — {decision}\n\n{finding}\n\nClasse: {finding_class}. Négatifs: {negative}. Candidat: {candidate_path}. Revues: {reviewers}. {reason}\n')
    with (ROOT/'research_state/RESEARCH_LEDGER.md').open('a') as f:f.write(f'\n### {cycle} — {decision}\n{finding}\nNégatifs: {negative}. Candidat: {candidate_path}. Prochaine tâche: {next_task}.\n')
    print(cycle,decision,candidate_path)
