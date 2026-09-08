# ITER001-C07

CYCLE: ITER001-C07
TASK: ITER001-P0-07 — Comment suivre le gain sans compter épargne et dépense ultérieure deux fois ?
ROLES: AGENT-CORPUS, AGENT-MONEY, AGENT-ENVIRONMENT, AGENT-ADVERSARIAL, AGENT-EVIDENCE; rôles IA, pas certification indépendante.
SOURCES: {'specialist': 'agents/reports/ITER001-C07/specialist.md', 'adversarial': 'agents/reports/ITER001-C07/adversarial.md', 'evidence': 'agents/reports/ITER001-C07/evidence.md'}; source primaire et provenance détaillées dans specialist.md.
PAGES: [19, 33, 400, 468, 523] (repères; pages effectivement lues dans le rapport spécialiste).
CLAIMS: ['CPC-0015', 'CPC-0084', 'CPC-0099', 'CPC-0127'] — aucun modifié.
QUESTIONS: ['RQ-10.02', 'RQ-07.02'] — statuts canoniques inchangés.
FINDINGS: Bilan à deux mondes et plusieurs dates: une économie temporairement épargnée puis dépensée n’est comptée qu’une fois; perte de revenu peut compenser le gain de panier.
COUNTEREVIDENCE: Liquidités fongibles, contrefactuel absent; parts signées non bornées; effets change/reclassification exclus ou corrigés. Source523 interdit obligation dépense, pas empreinte épargne nulle.
DISPUTES: DISPUTE-0001 hérité reste OPEN; voir OPEN_DISPUTES.md pour divergences nouvelles éventuelles.
TESTS: FORMAL: bilan deux périodes et compensation revenu PASS; double compte20 rejeté; données synthétiques uniquement.
CANDIDATE_CHANGES: candidate_changes/empirical/ITER001-C07.json — QUALIFY
VERIFY: suite baseline 128/128 dans copie isolée au démarrage; contrôle final après modifications structurantes, voir agents/logs/batch001/ et iteration_report_001.md. Ce champ n'atteste pas une exécution par cycle.
NEXT_TASK: ITER001-P0-08
