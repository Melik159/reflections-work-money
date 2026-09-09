# Corrections de lecture, non réécriture des équations sources

Recalculs exécutables: external_review/independent_checks.py; les résultats originaux restent archivés.

| id | pages | equation | current | objection | recalculation | result | condition |
|---|---|---|---|---|---|---|---|
| FORMAL-REMED-01 | [285, 301, 303] | Fp=rU; F=(p/r)U imprimé | Dérivation/postulat insuffisamment séparés | Limite à U fixe et inversion | r=2,U=3,p=4: F=rU/p=1.5, formule imprimée6 | LOCAL_ERROR | La relation de p301 reste une hypothèse proposée, non une démonstration |
| FORMAL-REMED-02 | [538, 559] | T=½cpω² et vitesse moyenne | K pondéré sous additivité | Moyenne quadratique ≠ carré de moyenne | cp=2,ω=[1,3]: mean(T)=5, T(meanω)=4; écart=variance1 | CORRECT_WITH_CONDITION | Conserver variance et composition; K peut absorber sans constance structurelle |
| FORMAL-REMED-03 | [207] | T=½cpω² | Primitive à cp fixe | cp variable | dT=cpωdω+½ω²dcp; cp2→3 à ω2: variation2 | CORRECT_WITH_CONDITION | cp fixe pour primitive à un seul terme |
| FORMAL-REMED-04 | [15] | M=nu | Différentielle | Ne pas confondre variation finie | ΔM=uΔn+nΔu+ΔnΔu | CORRECT_AS_STATED | dM infinitésimal; compensation exige u dn+n du=0 |
| FORMAL-REMED-05 | [249, 250, 467, 470] | Rapports0/0 et Force constante | Égalités locales généralisées | Limite dépendante du chemin; constante≠nulle | 2ε/ε=2; F2×Δt3=6 | LOCAL_ERROR | Une égalité peut être postulée séparément; impulsion nulle exige Force nette nulle |
| FORMAL-REMED-06 | [32, 197, 207] | (8/6)²−1 | +78% | Universalité revendiquée non testée | 7/9=0.777777… | CORRECT_WITH_CONDITION | Tâche, cp et hypothèse quadratique fixes; NOT_GENERALIZED_EMPIRICALLY |