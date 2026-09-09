# Décisions

DEC-0001 — Baseline conservée. Ancien état: pas de registre itératif. Nouvel état: registre séparé; aucun claim ni statut RQ modifié. Sources: clôture et dossiers RQ. Tests: manifeste gelé et validation de chaque cycle. Confiance HIGH sur la séparation documentaire.


DEC-0002 — CYCLE-001; date 2026-09-08T20:36:29.582117+00:00. Target: TASK-001. Old IN_PROGRESS → DONE. No claim/RQ status change. Reason: La conservation du total est conditionnée par un système sans pertes (256–257); 468–469 relient M à une différence puis à un transfert entre composantes. Conserver les référents séparés. Un bilan de composantes peut tester une hypothèse de clôture sans mesurer Money. Sources: [204, 205, 206, 207, 208, 254, 255, 256, 257, 258, 466, 467, 468, 469]; tests: CYCLE-001/results.json, verify.log. Confidence: HIGH conditional / LOW empirical.


DEC-0003 — CYCLE-002; date 2026-09-08T20:37:36.324509+00:00. Target: TASK-002. Old IN_PROGRESS → DONE. No claim/RQ status change. Reason: Le changement d’unité était déjà traité dans EXP-09. La nouveauté de ce cycle est un filtre de protocole: exclure T construit par la loi testée, exiger étalonnage indépendant, unité de tâche et échantillon de contrôle. Ce filtre ne fournit aucun capteur. Sources: [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]; tests: CYCLE-002/results.json, verify.log. Confidence: HIGH conditional / LOW empirical.


DEC-0004 — CYCLE-003; date 2026-09-08T20:38:25.267326+00:00. Target: TASK-003. Old IN_PROGRESS → DONE. No claim/RQ status change. Reason: EXP-02 identifiait déjà le problème de comparabilité. La nouveauté documentaire est un filtre refusant une entrée ordinale ou des échelles de rapport non raccordées pour estimer le rendement p386. Aucun rendement économique n’est estimé. Sources: [108, 109, 110, 111, 384, 385, 386, 387]; tests: CYCLE-003/results.json, verify.log. Confidence: HIGH conditional / LOW empirical.


DEC-0005 — 2026-09-08T20:40:13.482430+00:00. Target: suivi de série. Ancien état: trois tâches documentaires seules. Nouvel état: protocoles de mesure manquants TASK-011/012 et benchmark TASK-013 explicités; sept cycles thématiques restent OPEN. Motif: ne pas assimiler DONE documentaire à mesure résolue. Sources: EXP-09/EXP-02, résultats des trois cycles; confiance HIGH sur le suivi, empirique LOW.

## ITER001-C01 — QUALIFY

Quatre portes de raccord Money–VA–PIB précisées; diagnostic ancien prolongé par registre transaction/production et gain séparés, sans nouvelle mesure.

Classe: CONFIRMS_EXISTING. Négatifs: ['AMBIGUOUS', 'NOT_IDENTIFIABLE', 'NON_DISCRIMINATING']. Candidat: candidate_changes/empirical/ITER001-C01.json. Revues: {'specialist': 'agents/reports/ITER001-C01/specialist.md', 'adversarial': 'agents/reports/ITER001-C01/adversarial.md', 'evidence': 'agents/reports/ITER001-C01/evidence.md'}. Réserves adversariales incorporées dans la proposition; absence de désaccord substantiel à trancher. Les quatre portes sont nécessaires dans le modèle de collecte, pas suffisantes à identité PIB/Money.

## ITER001-C02 — QUALIFY

Protocole T/cp prolongé: exposant en vitesse normalisée, origine et observations de niveau/variation séparées; liberté de cp ne doit pas absorber les échecs.

Classe: CONFIRMS_EXISTING. Négatifs: ['NOT_IDENTIFIABLE', 'REQUIRES_INDEPENDENT_T', 'NON_DISCRIMINATING']. Candidat: candidate_changes/formalism/ITER001-C02.json. Revues: {'specialist': 'agents/reports/ITER001-C02/specialist.md', 'adversarial': 'agents/reports/ITER001-C02/adversarial.md', 'evidence': 'agents/reports/ITER001-C02/evidence.md'}. Réserves adversariales intégrées; extension du protocole déjà existant, pas nouvelle découverte du blocage T.

## ITER001-C03 — QUALIFY

Ajout d’un diagnostic de fermeture pour trois raccords multiplicatifs indépendants; cohérence algébrique nécessaire, comparabilité Utility non établie.

Classe: NEW_SCENARIO. Négatifs: ['NOT_IDENTIFIABLE', 'NON_DISCRIMINATING']. Candidat: candidate_changes/concepts/ITER001-C03.json. Revues: {'specialist': 'agents/reports/ITER001-C03/specialist.md', 'adversarial': 'agents/reports/ITER001-C03/adversarial.md', 'evidence': 'agents/reports/ITER001-C03/evidence.md'}. Scénario formel additionnel; obstacle métrologique déjà connu. Réserves intégrées; aucun désaccord tranché.

## ITER001-C04 — QUALIFY

Décomposition exacte de ΔK en composition, coefficients et interaction; exemple où K stable masque changements compensés.

Classe: NEW_SCENARIO. Négatifs: ['NOT_IDENTIFIABLE', 'NON_DISCRIMINATING']. Candidat: candidate_changes/formalism/ITER001-C04.json. Revues: {'specialist': 'agents/reports/ITER001-C04/specialist.md', 'adversarial': 'agents/reports/ITER001-C04/adversarial.md', 'evidence': 'agents/reports/ITER001-C04/evidence.md'}. Deux calculs synthétiques exécutés et contrôle omission interaction; nouvel outil local du programme, non preuve économique ni nouveauté historique.

## ITER001-C05 — QUALIFY

Plan local à deux interventions séparé du test du pont économique; même identification de réponses énergie/procédé ne suffit pas à départager H1/H2/H3.

Classe: NEW_SCENARIO. Négatifs: ['NOT_IDENTIFIABLE', 'NON_DISCRIMINATING', 'REQUIRES_INDEPENDENT_T', 'REQUIRES_EXOGENOUS_VARIATION']. Candidat: candidate_changes/empirical/ITER001-C05.json. Revues: {'specialist': 'agents/reports/ITER001-C05/specialist.md', 'adversarial': 'agents/reports/ITER001-C05/adversarial.md', 'evidence': 'agents/reports/ITER001-C05/evidence.md'}. Protocole clarifie identification locale versus comparaison des théories; pas de prédiction numérique nouvelle ni exclusivité H3.

## ITER001-C06 — QUALIFY

Romer1990 et Oslo2018 ajoutent un comparateur explicite de décisions techniques, réemploi, adoption et types innovation; vitesse seule ne distingue pas leurs causes.

Classe: NEW_LITERATURE_PARALLEL. Négatifs: ['NON_DISCRIMINATING', 'REQUIRES_EXOGENOUS_VARIATION']. Candidat: candidate_changes/questions/ITER001-C06.json. Revues: {'specialist': 'agents/reports/ITER001-C06/specialist.md', 'adversarial': 'agents/reports/ITER001-C06/adversarial.md', 'evidence': 'agents/reports/ITER001-C06/evidence.md'}. Sources externes exactes acquises et pages pertinentes lues après retrieval distinct; lecture ciblée des introductions/définitions, pas revue historique complète.

## ITER001-C07 — QUALIFY

Bilan à deux mondes et plusieurs dates: une économie temporairement épargnée puis dépensée n’est comptée qu’une fois; perte de revenu peut compenser le gain de panier.

Classe: NEW_SCENARIO. Négatifs: ['NOT_IDENTIFIABLE', 'NON_DISCRIMINATING', 'REQUIRES_EXOGENOUS_VARIATION']. Candidat: candidate_changes/empirical/ITER001-C07.json. Revues: {'specialist': 'agents/reports/ITER001-C07/specialist.md', 'adversarial': 'agents/reports/ITER001-C07/adversarial.md', 'evidence': 'agents/reports/ITER001-C07/evidence.md'}. Diagnostic de double comptage temporel et contreparties exécuté; résultats synthétiques sans allocation économique mesurée.

## ITER001-C08 — QUALIFY

Seuil conditionnel s*=S/(Gm) précise annulation d’une économie physique hypothétique; effets omis Z et horizons empêchent un verdict global.

Classe: NEW_SCENARIO. Négatifs: ['NON_DISCRIMINATING', 'NOT_IDENTIFIABLE']. Candidat: candidate_changes/empirical/ITER001-C08.json. Revues: {'specialist': 'agents/reports/ITER001-C08/specialist.md', 'adversarial': 'agents/reports/ITER001-C08/adversarial.md', 'evidence': 'agents/reports/ITER001-C08/evidence.md'}. Trois signes autour du seuil et deux limites calculés exactement; paramètres purement synthétiques, pas preuves de la loi de pertes du corpus.

## ITER001-C09 — QUALIFY

Pour la formulation forte p112, taux de dommage et dommage par tâche peuvent se situer de part et d’autre du carré de vitesse; préciser grandeur/horizon avant test.

Classe: NEW_MEASUREMENT_ISSUE. Négatifs: ['NOT_IDENTIFIABLE', 'AMBIGUOUS', 'NON_DISCRIMINATING']. Candidat: candidate_changes/concepts/ITER001-C09.json. Revues: {'specialist': 'agents/reports/ITER001-C09/specialist.md', 'adversarial': 'agents/reports/ITER001-C09/adversarial.md', 'evidence': 'agents/reports/ITER001-C09/evidence.md'}. Précise un obstacle opérationnel de la fonction dommage déjà reconnue; aucune fonction empirique introduite.

## ITER001-C10 — QUALIFY

Contrat de test par sous-énoncé reliant source, type, métrologie, construction/calibration/test et prédiction concurrente; intention méthodologique et réussite restent séparées.

Classe: CONFIRMS_EXISTING. Négatifs: ['NON_DISCRIMINATING']. Candidat: candidate_changes/questions/ITER001-C10.json. Revues: {'specialist': 'agents/reports/ITER001-C10/specialist.md', 'adversarial': 'agents/reports/ITER001-C10/adversarial.md', 'evidence': 'agents/reports/ITER001-C10/evidence.md'}. Opérationnalise limites déjà établies pour prochaines tâches; aucune nouvelle évaluation académique globale.
