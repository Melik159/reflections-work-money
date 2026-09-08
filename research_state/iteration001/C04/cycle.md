# ITER001-C04

CYCLE: ITER001-C04
TASK: ITER001-P0-04 — Comment décomposer une dérive de K entre recomposition et variation des coefficients ?
ROLES: AGENT-CORPUS, AGENT-FORMAL, AGENT-MEASUREMENT, AGENT-ADVERSARIAL, AGENT-EVIDENCE; rôles IA, pas certification indépendante.
SOURCES: {'specialist': 'agents/reports/ITER001-C04/specialist.md', 'adversarial': 'agents/reports/ITER001-C04/adversarial.md', 'evidence': 'agents/reports/ITER001-C04/evidence.md'}; source primaire et provenance détaillées dans specialist.md.
PAGES: [36, 526, 558, 559] (repères; pages effectivement lues dans le rapport spécialiste).
CLAIMS: ['CPC-0043', 'CPC-0044', 'CPC-0109', 'CPC-0117', 'CPC-0118'] — aucun modifié.
QUESTIONS: ['RQ-08.02', 'RQ-09.03'] — statuts canoniques inchangés.
FINDINGS: Décomposition exacte de ΔK en composition, coefficients et interaction; exemple où K stable masque changements compensés.
COUNTEREVIDENCE: Représentation additive elle-même conditionnelle; g, coefficients source et K macro non identifiés. Produits entrants et changements base compliquent raccord. Source p558 refuse déjà corrélation→causalité.
DISPUTES: DISPUTE-0001 hérité reste OPEN; voir OPEN_DISPUTES.md pour divergences nouvelles éventuelles.
TESTS: FORMAL: deux exemples exacts PASS; omission interaction rejetée (tests locaux, pas les sept mutations historiques).
CANDIDATE_CHANGES: candidate_changes/formalism/ITER001-C04.json — QUALIFY
VERIFY: suite baseline 128/128 dans copie isolée au démarrage; contrôle final après modifications structurantes, voir agents/logs/batch001/ et iteration_report_001.md. Ce champ n'atteste pas une exécution par cycle.
NEXT_TASK: ITER001-P0-05
