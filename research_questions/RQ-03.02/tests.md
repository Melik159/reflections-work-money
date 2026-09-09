# RQ-03.02 — tests de deuxième passe

Exécuté : cp=2, ω3→4 donne niveau9→16, variation7. DESIGNED_NOT_EXECUTED : mesurer cp et Force indépendamment sur une tâche réelle.

Hypothèse/prédiction : MINIMAL_RECONSTRUCTION : distinguer S_T(t)=cp·ω(t)²/2+C, ΔS_T=S_T(t2)−S_T(t1), réserve R_T et quantité transmise τ12. Poser τ12=ΔS_T=−ΔR_T uniquement dans le bilan sans pertes indiqué. Aucun remplacement dans SOURCE_FORMALISM.

Variables et données : p207 : primitive T=cp·ω²/2 à constante nulle ; p471 : T désigne une intégrale entre deux instants ; p553 : Tpos accompli, Tneg restant.

Conditions : cp constant pour la primitive affichée ; même tâche, unité et frontière ; indices de position et origine du niveau explicites.

Résultat incompatible ou contre-exemple : Avec cp=2, ω=3, S_T=9 mais variation nulle à vitesse constante : la phrase Work is zero ne peut désigner simultanément ce niveau. C’est une limite à la lecture littérale non indexée.

Explications concurrentes / domaine : cp variable ajoute ω²·dcp/2 au différentiel du niveau ; vitesse constante annule ΔS_T, pas S_T. Les rôles de Money p255–257 ne sont pas une calibration de T.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.

## Quatrième passe — EXP-09

État E, réserve R et transfert T[a,b] ont des compatibilités locales distinctes. Le transfert signé télescope; cumul positif et réserve ne sont pas la primitive. cp variable exige un terme supplémentaire; aucune mesure indépendante de T.

Preuve formelle EVID-FOURTH-EXP-09-RQ-03.02, relation QUALIFIES. [Protocole figé](../experiments/EXP-09/protocol.md), [résultats et limites](../experiments/EXP-09/results.md). Calcul exécuté, non observation de T/Utility/Money.

Statut de la question conservé: AMBIGUOUS; confiance dans le calcul local HIGH, identification empirique LOW. Conditions manquantes et objections antérieures restent ouvertes.
