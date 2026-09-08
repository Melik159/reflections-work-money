# Recherche continue — session ITER001 terminée

Baseline documentaire1.0 figée; manifeste closure_review/BASELINE_MANIFEST_SHA256.txt autorité d'intégrité. Aucun push/merge/publication ni nouvelle baseline. Rapport courant : iteration_report_001.md. Ancien état copié dans history/iteration001_start/, artefacts originaux non déplacés.

Lire RESEARCH_LEDGER.md puis NEXT_ACTIONS.yaml. Dix cycles ITER001 clos; dix tâches ITER002 en attente d'une prochaine session. Chaque cycle comprend pages source, spécialiste, adversaire, evidence review, décision et candidat séparé. Les statuts des tâches concernent le travail documentaire, ceux des expériences leur faisabilité.

Commandes sûres depuis racine :

```bash
python3 research_state/iteration001/validate_batch.py --complete
python3 research_state/iteration001/query.py --collection SOURCE_CORPUS --query 'Money added Value' --level PAGE -k 3
python3 research_state/iteration001/query.py --collection DERIVED_ANALYSIS --query 'Money GDP bridge' -k 3
python3 research_state/iteration001/query.py --collection EXTERNAL_LITERATURE --query 'innovation technological change' -k 3
```

Voir iteration001/RETRIEVAL.md. Les collections sont séparées; les hits localisent, les pages font preuve d'attribution. L'index externe ne contient que des blocs source, pas les notes de comparaison.

Les scripts historiques cycle.py/report.py et research_state/verify.sh sont conservés pour provenance, **pas utilisés pour piloter ce nouveau lot** : conclusions des trois cycles y sont pré-écrites et verify appelle un script régénérant des artefacts. ./verify.sh a donc été exécuté dans des copies isolées, avec128/128PASS et contrôles SHA256 de l'original; voir agents/logs/batch001/. Le validateur du nouveau lot est en lecture seule et ne prouve pas la vérité économique.

Candidats sous candidate_changes/ uniquement. DISCOVERY → SOURCE CHECK → SPECIALIST → ADVERSARIAL → EVIDENCE → décision → candidat. Préparation retrieval en amont distincte des lectures/revues; aucun rôle IA ne constitue une expertise institutionnelle indépendante. Une nouvelle baseline requiert instruction humaine explicite.
