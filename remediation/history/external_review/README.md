# External review

Entrée: [final_external_review.md](final_external_review.md). Findings et corrections sont des propositions, non modifications de la synthèse.

Reproduction locale:

```sh
.venv-research/bin/python external_review/independent_checks.py
.venv-research/bin/python external_review/audit_tests.py
.venv-research/bin/python external_review/build_review.py
.venv-research/bin/python external_review/final_check.py
```

Ne pas relancer freeze pour effacer la baseline. Les sept références sont vérifiées sur passages sélectionnés; les verdicts sont des jugements argumentés, non des sorties statistiques.
