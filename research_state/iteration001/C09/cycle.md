# ITER001-C09

CYCLE: ITER001-C09
TASK: ITER001-P0-09 — Quelles observations distinguent pression physique et dommage selon lieu et horizon ?
ROLES: AGENT-CORPUS, AGENT-ENVIRONMENT, AGENT-MEASUREMENT, AGENT-ADVERSARIAL, AGENT-EVIDENCE; rôles IA, pas certification indépendante.
SOURCES: {'specialist': 'agents/reports/ITER001-C09/specialist.md', 'adversarial': 'agents/reports/ITER001-C09/adversarial.md', 'evidence': 'agents/reports/ITER001-C09/evidence.md'}; source primaire et provenance détaillées dans specialist.md.
PAGES: [68, 69, 112, 460] (repères; pages effectivement lues dans le rapport spécialiste).
CLAIMS: ['CPC-0001', 'CPC-0031', 'CPC-0120'] — aucun modifié.
QUESTIONS: ['RQ-01.04', 'RQ-11.01', 'RQ-11.03'] — statuts canoniques inchangés.
FINDINGS: Pour la formulation forte p112, taux de dommage et dommage par tâche peuvent se situer de part et d’autre du carré de vitesse; préciser grandeur/horizon avant test.
COUNTEREVIDENCE: Modèle β−1 suppose taux constant intégré et tâche proportionnelle au débit; dégâts réels peuvent être non linéaires/différés. P112 ne spécifie pas une élasticité log-log ni un mesurande.
DISPUTES: DISPUTE-0001 hérité reste OPEN; voir OPEN_DISPUTES.md pour divergences nouvelles éventuelles.
TESTS: FORMAL: taux32>16, durée1/4 et dommage intégré8<16 vérifiés; unités/horizon conditionnels, aucun résultat empirique.
CANDIDATE_CHANGES: candidate_changes/concepts/ITER001-C09.json — QUALIFY
VERIFY: suite baseline 128/128 dans copie isolée au démarrage; contrôle final après modifications structurantes, voir agents/logs/batch001/ et iteration_report_001.md. Ce champ n'atteste pas une exécution par cycle.
NEXT_TASK: ITER001-P0-10
