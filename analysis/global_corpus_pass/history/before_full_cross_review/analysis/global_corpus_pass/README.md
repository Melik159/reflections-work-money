# Consolidation globale — travail à poursuivre

[Rapport](final_report.md) · [baseline](00_baseline.md) · [matrice](page_matrix.csv) · [findings sourcés](findings.json) · [claims](claim_rechecks.json) · [formules](formula_inventory.md).

**90/562 pages relues dans cette passe.** Couverture analytique historique cumulée300/562. Ne pas confondre ces métriques. La colonne historical_analytically_reviewed décrit l'état antérieur, scan_status décrit cette passe; UNREVIEWED n'annule pas un travail antérieur.

## Reprendre sans recommencer

1. Choisir les pages encore UNREVIEWED de page_matrix.csv. Les derniers blocs500–562 et426–450 ont été parcourus, ainsi que20 et349. Les figures signalées « à contrôler » ne sont pas DEEP_REVIEWED.
2. Lire réellement les pages; pour une extraction presque vide ou une formule ambiguë, inspecter le rendu du PDF. Les occurrences de labels dans formula_candidates.json sont uniquement des indices automatiques, pas la preuve qu'une formule est présente intégralement ou comprise.
3. Archiver matrice, manifeste, notes et dossiers affectés avant extension. Ne pas relancer les générateurs d'initialisation: ils refusent l'écrasement. Le catalogue global_pass_catalog.py conserve la rédaction des notes; une extension demande réconciliation explicite des artefacts.
4. Ajouter les sources et la portée de révision des claims. local_review_status n'est pas global_review_status. Un claim n'est revérifié contre tout le corpus qu'après confrontation aux qualifications et exceptions restantes.
5. Mettre à jour les trois métriques de lecture, le catalogue des formules et les liens de questions. Les nouveaux claims potentiels ont des IDs GC-CAND, pas CPC: aucune insertion silencieuse dans les127 claims canoniques.
6. N'accorder le certificat complet qu'après les critères du manifeste et du validateur. Exécuter ./verify.sh. La synthèse finale n'est pas autorisée automatiquement.

## Contrôles

```bash
.venv-research/bin/python analysis/run_global_local_checks.py --check
.venv-research/bin/python analysis/verify_global_corpus_pass.py
./verify.sh
```

Les quatre diagnostics formels supplémentaires ne sont ni expériences économiques ni mesures des variables propres du système. Les contrôles ne qualifient pas les contradictions textuelles ouvertes de FAIL informatique. Un faux certificat de lecture intégrale, un lien cassé ou un résultat modifié sans trace échouent.

## Sources et traces

PDF original intact; sa SHA figure dans baseline.json. Les analyses antérieures modifiées sont archivées sous history/baseline. Les rendus d'inspection ont été créés en répertoire temporaire, pas ajoutés comme copies binaires inutiles au dépôt. Les méthodes, pages et transcriptions sont enregistrées; un rendu peut être reproduit localement à partir du PDF.
