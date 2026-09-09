# Contrôles locaux — critères fixés avant exécution du script

Ces contrôles portent sur des implications algébriques imprimées, pas sur des données économiques ni sur le système entier. Ils ne remplacent aucune expérience antérieure.

## GC-CHECK-01 — Primitive p525→526

SOURCE_FORMALISM : dP=−(rP/gTM)dp/p, puis P=rP/ln(p). Le rendu PDF confirme l'inverse de logarithme, ce n'est pas une faute d'extraction. Branche constante : rP,gTM non nuls, p>0, p≠1, origine normalisée p0=1.

MINIMAL_RECONSTRUCTION : P(p)−P(p0)=−(rP/gTM)ln(p/p0). Sa dérivée vaut −rP/(gTM p). Celle de la formule imprimée vaut −rP/[p ln(p)^2]. L'égalité exigerait ln(p)^2=gTM ponctuellement; elle ne tient pas sur un intervalle à gTM constant. Même diagnostic pour A et l. Une constante additive ne répare pas cette différence de fonction.

Contrôle numérique à rP=gTM=1, ln(p)=2 puis 3 : dérivées normalisées p·P' différentes. Résultat attendu FORMALLY_INCONSISTENT_LOCAL_DERIVATION. Une définition différente de P ou g variable serait une modification du modèle local, non réparation silencieuse.

## GC-CHECK-02 — Inégalité de niveaux p523→528

SOURCE_FORMALISM : Mc≥Md utilisé pour écrire dMc≥dMd. Contre-exemple analytique x∈[0,1], Mc=2−x, Md=x : Mc≥Md partout, mais Mc'=−1<Md'=1. Les fonctions sont des constructions synthétiques, pas des agents observés. Résultat attendu : implication non valide sans restriction d'évolution.

## GC-CHECK-03 — Constance g et égalité p528

SOURCE_FORMALISM : gTM,gMT constants transforment l'inégalité25-09 en égalité25-10. Contre-exemple positif t>0, gTM=gMT=1, Td=2t, Tc=t, Mc=2t, Md=t. L'inégalité et les deux équivalences tiennent, mais dTc/dTd=1/2≠gTMgMT. La thésaurisation est admise p523. Il manque une saturation ou restriction supplémentaire; ce test n'invalide pas l'égalité dans ce cas supplémentaire.

## GC-CHECK-04 — Étapes réciproques de beta p435 et439

À r,V ou r,B constants et U>0, la définition initiale donne betaTM=−1/U et betaMT=+1/U. Les étapes imprimées utilisent au contraire la dérivée de 1/U après multiplication par U, donnant respectivement +1/U et −1/U. Contrôle à U=2 et 5.

Les résultats finaux encadrés retrouvent les définitions initiales; verdict : intermédiaires incompatibles, résultat final localement récupérable. Ne pas conclure « toutes les formules des coefficients sont fausses ».

## Limites

Pas de mesure indépendante, pas de nouvelle corrélation, pas de changement de claims canoniques. Les lacunes18-05/18-07 et le mauvais indice17-10 sont des inspections visuelles, pas des résultats de ces quatre calculs. Le protocole et les résultats demeurent versionnés séparément.
