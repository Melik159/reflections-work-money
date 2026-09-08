# Première reconstruction des dix chapitres — passe terminale

8 septembre2026. Dépôt local `/home/ubuntu/reflections-work-money`, branche `research/corpus-validation`, HEAD source `a697345c427fca8de0521108a17aa2b76f267654`. PDF original inchangé ; aucun push ni commit effectué.

## CH-08 / CH-09 / CH-10

| Chapitre | Statut local | Résultat principal |
|---|---|---|
| CH-08 Agrégation | UNCERTAIN | Six opérations distinctes ; potentiels locaux et carte de vecteurs ne démontrent pas l’agrégation ; stabilisation de K hypothétique |
| CH-09 Énergie/conservation | UNCERTAIN | Pont travail physique utile/T économique explicite et conditionnel ; vraie généralisation forte GDP=K·W p.559 ; énergie supplémentaire non créatrice reconnue |
| CH-10 Agents/marchés | UNCERTAIN | Taxonomie propre, transferts et pertes utiles ; monopole sans changement et brevet productif doivent rester deux branches |

Dix chapitres possèdent désormais une première analyse, à profondeurs inégales. Ce n’est pas un statut de validation globale.

## ENERGY DATA / GDP–ENERGY

Ancienne série : PIB-PPA divisé par PIB-PPA/kg équivalent pétrole. Construction dérivée confirmée, mais circularité non automatique : le ratio source peut restituer un bilan IEA. Millésimes historiques à réconcilier. Reproduction conservée.

Nouvelle série : OWID/EI/EIA2025 figée, énergie primaire TWh par substitution, acquise sans PIB dans la construction de la colonne utilisée. Source et traitements archivés avec SHA. Ce n’est pas une variable statistiquement exogène.

Trois expériences exécutées et numériquement revérifiées : E1 niveau/log-log/Δlog ; E2 par habitant ; E3 stabilité. Six zones, 1990–2023, 204 observations, pas de données manquantes ni interpolation. Les IC sont HAC(3), asymptotiques ; les tendances communes ne sont pas éliminées.

| Zone | βlog-log [IC95%], N34 | R² | βΔlog, N33 | R²Δlog |
|---|---|---:|---:|---:|
| Monde | 1,535 [1,458 ; 1,611] | 0,992 | 0,865 | 0,786 |
| France | −0,662 [−1,321 ; −0,004] | 0,115 | 0,306 | 0,284 |
| Allemagne | −1,728 [−2,462 ; −0,994] | 0,543 | 0,331 | 0,222 |

Les autres pays et modèles figurent dans `27_energy_results.md`. France : β avant2007≈1,956, après≈−0,473 ; différence≈−2,429, IC[-3,017 ; −1,841]. Le résultat global français est fragile et varie avec la série énergétique ; aucune causalité négative n’est inférée. Monde : PIB/énergie augmente d’environ45% entre1990 et2023, malgré un R² élevé.

## IDENTIFICATION

Association mondiale : compatible avec le rôle énergétique de Campergue **et** des explications standard. Pas de validation du pont T/M, des rendements ou de la théorie complète. La restriction à K macro constant de la p.559, avec nos proxies fixés, est défavorisée par les trajectoires. C’est une confrontation d’une restriction précise, pas un test de toutes les versions à K variable. Aucune relation causale ni performance prédictive hors échantillon identifiée.

## ENVIRONMENTAL CHAIN / AGGREGATION / AGENTS

Sept liaisons documentées : six SOURCE_EXPLICIT, une RESEARCH_INTERPRETATION. Subsistance→cycles plus rapides→abondance ; Work/prix→surplus et achats ; énergie bon marché→mobilité ; accélération/pertes→combustibles→dommages. Manquent le panier marginal, les matières, le mix et une fonction de dommages. Rebond : PARTIAL_PARALLEL, pas Jevons attribué automatiquement.

Agrégation : homogénéité des produits, pondérations, absence de double compte, intégrabilité, normalisation des axes, coefficients et composition stables sont à expliciter. Agents : création productive alléguée, paiement, transfert, redistribution et pertes utiles gardent des catégories distinctes.

## T / dT

PARTIALLY_RESOLVED localement, AMBIGUOUS globalement. T est utilisé comme primitive quadratique, intégrale entre deux instants ou Work restant selon les pages ; p.553–554 explicite des référents. dT=0 ne fixe pas T. L’implication Force constante non nulle→a/e constants est localement inconsistante avec l’équation qui la précède ; cela ne constitue pas un verdict sur toute la théorie.

## CLAIMS / COVERAGE / VERIFY

- Claims :113→127 ; 14 nouveaux MAJOR ; 24 CORE,96 MAJOR,7 SUPPORTING,0 PERIPHERAL. Les113 claims préexistants sont inchangés, historique conservé.
- Concepts :36 ; mécanismes productifs et formules de la passe précédente conservés.
- Graphe :180 nœuds,220 arêtes ; dépendances contrôlées ; pas de cycle dans les arêtes DEPENDS_ON.
- Couverture :175→247/562, soit72 nouvelles pages. Exhaustivité non revendiquée.
- Bibliographie ajoutée :6 sources,5 VERIFIED,1 PARTIALLY_VERIFIED ; accès NBER limité explicite. Relations :1 SUPPORTS,4 QUALIFIES,1 PARALLELS,3 DOES_NOT_TEST,0 CONTRADICTS.
- `./verify.sh` : **PASS —48/48 tests, zéro échec, zéro erreur**. Huit nouveaux tests. Warnings : couverture, bibliographie, hypothèses et ambiguïtés scientifiques. Premier essai47/48 conservé : métrique de couverture non synchronisée, corrigée sans désactiver le test.

## MAIN FINDINGS

1. L’ancienne reconstruction énergétique n’est pas automatiquement une corrélation tautologique.
2. Les nouvelles associations macro restent non causales et largement non spécifiques.
3. Un grand R² mondial ne démontre pas un coefficient de proportionnalité constant.
4. P.559 contient bien une généralisation forte, distincte de la prudence p.538 et de la réserve causale p.558.
5. Les coefficients locaux et un champ d’entreprises ne sont pas encore une règle d’agrégation.
6. Le couplage physique/économique vise du travail utile ; toute chaleur consommée n’est pas créatrice de Money.
7. L’usage possible du surplus existe dans le texte ; son empreinte et un rebond quantifié restent non mesurés.
8. La branche productive du brevet empêche d’aplatir la discussion des monopoles.
9. Non-création technique de Money n’implique pas inutilité sociale des services.
10. T/dT et certains signes nécessitent un référent local explicite, non une correction automatique.

## OPEN QUESTIONS

1. Quelle mesure indépendante de T/M permettrait de calibrer le pont avec l’énergie physique ?
2. Sous quelles pondérations K deviendrait-il réellement stable ?
3. Comment concilier la critique du PIB avec son identification à Money dépensé p.559 ?
4. Quelles conventions énergétiques et frontières rendent le test le plus fidèle ?
5. Quel panier supplémentaire est financé par les gains, et avec quelle empreinte ?
6. Quelle métrique rend le champ labour-prix invariant aux unités ?
7. Quelle convention unifie T, ΔT, Tpos/Tneg et la réserve potentielle ?
8. Quel domaine contraint justifie l’optimum annoncé des cycles ?
9. Comment traiter les services et biens publics dans les critères de création ?
10. Quels faits sépareraient composante productive et rente d’un monopole innovant ?

## NEXT PRIORITIES

1. Formaliser un exemple à deux produits hétérogènes et tester K/pondérations sans ajustement ad hoc.
2. Réconcilier unités, frontières physiques et données énergétiques IEA/EI.
3. Construire un protocole micro mesurant coût, qualité, prix, énergie et gains clients séparément.
4. Relire les passages nécessaires à T/dT et aux rendements optimaux avec audit visuel des tableaux.
5. Quantifier l’usage du gain et son empreinte avant de conclure sur rebond et dommages.

## Fichiers et état Git

Nouveaux rapports27–30, CH08/09/10, note de lecture, données d’agrégation/environnement/agents/problèmes, bibliothèque ciblée, scripts d’acquisition/expériences/intégration, archive énergétique et huit tests. Mises à jour : claims, graphe, chapitres, concepts/liens, matrice claim×chapitre, couverture/progression, bibliothèque commune, verify et README. Les états avant révision sont dans `analysis/history/pre_energy_review/`.

Git : les artefacts de recherche restent non suivis dans le dépôt, comme avant cette passe ; aucun changement aux fichiers source suivis. Aucune publication distante.
