# Formalisme — périmètre limité aux problèmes connus

| id | source | ORIGINAL_ISSUE | REMEDIATION | CURRENT_STATUS | RESIDUAL_RISK |
|---|---|---|---|---|---|
| FORMAL-REMED-01 | [285, 301, 303] | Limite à U fixe et inversion | r=2,U=3,p=4: F=rU/p=1.5, formule imprimée6 | LOCAL_ERROR | La relation de p301 reste une hypothèse proposée, non une démonstration |
| FORMAL-REMED-02 | [538, 559] | Moyenne quadratique ≠ carré de moyenne | cp=2,ω=[1,3]: mean(T)=5, T(meanω)=4; écart=variance1 | CORRECT_WITH_CONDITION | Conserver variance et composition; K peut absorber sans constance structurelle |
| FORMAL-REMED-03 | [207] | cp variable | dT=cpωdω+½ω²dcp; cp2→3 à ω2: variation2 | CORRECT_WITH_CONDITION | cp fixe pour primitive à un seul terme |
| FORMAL-REMED-04 | [15] | Ne pas confondre variation finie | ΔM=uΔn+nΔu+ΔnΔu | CORRECT_AS_STATED | dM infinitésimal; compensation exige u dn+n du=0 |
| FORMAL-REMED-05 | [249, 250, 467, 470] | Limite dépendante du chemin; constante≠nulle | 2ε/ε=2; F2×Δt3=6 | LOCAL_ERROR | Une égalité peut être postulée séparément; impulsion nulle exige Force nette nulle |
| FORMAL-REMED-06 | [32, 197, 207] | Universalité revendiquée non testée | 7/9=0.777777… | CORRECT_WITH_CONDITION | Tâche, cp et hypothèse quadratique fixes; NOT_GENERALIZED_EMPIRICALLY |

Utility: ordre insuffisant à certains ratios; coefficients peuvent covarier dans d’autres opérations. Potentiels/agrégation: exactitude, unité et frontière sont des conditions, pas résultats empiriques. T/dT: niveau, transfert et réserve séparés, pas un référent global imposé. +78%: arithmétique, hypothèse quadratique et non-généralisation empirique conservées. Les sept mutants ciblés vérifient la conservation de ces énoncés, non leur vérité universelle.
