# Passe productive — rapport final

Statut : **QUALIFIED_TARGETED_RECONSTRUCTION**. Pas de verdict global. Source HEAD a697345c427fca8de0521108a17aa2b76f267654, branche research/corpus-validation; PDF original inchangé.

## PRODUCTIVE MECHANISMS FOUND

20 mécanismes documentés, PM-01 àPM-20 : tâche/vitesse; stabilité sans Work supplémentaire; accélération à coût horaire fixe; marge/prix maintenu; chaîne à profit absolu fixe; création avant usage; différence d’Utility; branches T→M; branches M→T; adiabatique; cycles/rendements; coût énergétique; substitution machine-salarié; émission accompagnatrice; pertes utiles; coefficients variables; ralentissement/stabilité/accélération; addition entre moyens; prix temporel versus comparaison de copies; Utility/négociation/complexité.

## ECONOMIC WORK

La tâche restante l et sa vitesse ω ne sont pas T. Le formalisme relie variation de vitesse, Force et complexité à dT. À cP constant : dT=cP.ω.dω puis T=cP.ω²/2 avec référence nulle. Vitesse constante donne dT=0, sans abolir labour, production ou énergie physique. L’emploi e inclut les machines, pas seulement les personnes. L’addition des contributions est postulée; l’agrégation macro n’est pas ainsi entièrement construite.

## PRODUCTIVITY/COST/PRICE

Transmission intégrale conditionnelle, prix maintenu/gain retenu, chaîne à profit absolu constant, effets entre acteurs, coûts énergétiques et complexité changeants identifiés. Aucune loi explicite de transmission partielle ou de délai coût→prix trouvée dans les passages examinés; le délai d’usage du supplément est un autre objet. Voir [rapport26](26_cost_price_transmission.md).

## PRODUCTIVE CREATION

Deux représentations centrales doivent être articulées : accélération→temps/coût→prix sous conditions→supplément consommateur; différences d’Utility et intégrales au long des transformations/cycles. L’émission de Cash est une variante accompagnatrice, non le mécanisme productif par défaut. Le financement du capital reste moins opérationnalisé que l’opposition dévaluation/Work supplémentaire pour les intérêts.

## CH-06 / CH-07

- [CH-06](chapters/CH06_constitutive_transformations.md) : **UNCERTAIN**, lois proposées et dérivations conditionnelles, mesures indépendantes manquantes.
- [CH-07](chapters/CH07_cycles_yields.md) : **UNCERTAIN**, cycles et rendements reconstruits; signes, égalités et domaine de l’optimum à réconcilier.

## FORMULAS

20 fiches :5 définitions,4 lois proposées,11 dérivations conditionnelles. Six fiches contrôlées visuellement sur cinq pages; les autres portent explicitement le statut transcription manuelle du texte extrait. Variables, dimensions inférées, hypothèses, étapes et limites conservées dans `data/productive_formulas.json`.

## +78%

ARITHMETICALLY_REPRODUCED; FORMALLY_DERIVED sous les prémisses; ASSUMPTION_DEPENDENT; NOT_EMPIRICALLY_TESTED. (8/6)²−1=77,777…%; coût160→120 à20$/h. Le formalisme économique suppose une transposition quadratique; ni consommation physique totale ni validation empirique n’en découlent automatiquement.

## ENERGY

Sept axes structurants séparés : énergie bon marché et niveau de vie; Work utile versus W; analogie quadratique; chaîne de rendements/conservation; coûts relatifs; pertes utiles; dommages environnementaux. Préparation deCH09, pas validation de ses lois. Voir `data/productive_energy_map.json`.

## EMPIRICAL

Trois protocoles : vitesse–Work; transmission coût–prix; couplage chaleur–Money. Tous NOT_IDENTIFIABLE_WITH_CURRENT_DATA. Diagnostic réellement exécuté sur204 observations : énergie reconstruite par PIB_PPA/intensité inverse, erreur relative maximale2,22×10⁻¹⁶. Monde : R² log-log0,99086; en différences logarithmiques0,66086. Ces résultats ne constituent ni causalité ni mesure indépendante de Money.

Cinq calculs formels exécutés. Le coefficient de prix doit être traité avec e=cPω : p∝1/√T à cP,l,Ch fixes. Valeur34,3146% reproduite, maximum universel non démontré par cette seule substitution. Les sorties négatives de non-implication sont conservées.

## CLAIMS / COVERAGE / VERIFY

93→113 claims :20 MAJOR ajoutés,0 CORE ajouté. Les32 scénarios monétaires et les24 CORE précédents sont préservés. Couverture121→175/562 pages. HYP-0002 qualifiée avec journal old/new et sources.

`verify.sh` exécuté : **PASS,40 tests réussis,0 échec**, dont8 nouveaux. WARNING : recherche incomplète, ambiguïtés formelles, identification causale impossible avec les données actuelles. La réussite technique ne certifie pas la théorie.

## MAIN FINDINGS

1. Work nul à vitesse constante se reconstruit comme absence de variation/création, pas disparition du travail physique.
2. Le gain productif et sa transmission commerciale sont deux étapes distinctes dans le manuscrit lui-même.
3. Le profit absolu inchangé est une condition explicite des exemples tardifs.
4. Production supplémentaire, accélération, Utility et création de Money ne sont pas synonymes.
5. Le +78% a une dérivation interne, mais dépend des identifications économiques et du carré de la vitesse.
6. Les variables de la formule du prix ne sont pas indépendantes.
7. Les branches constitutives sont algébriquement exploitables mais exigent des mesures non circulaires.
8. Les rendements et les échanges externes doivent être distingués des variations internes et des conditions de réversibilité.
9. La série macro disponible n’identifie aucun des mécanismes causaux spécifiques.

## OPEN QUESTIONS / NEXT PRIORITIES

Réconcilier T/dT et les signes, mesurer cP/cA/Forces/Utility, expliciter l’optimum du cycle, distinguer les trajectoires de prix des comparaisons entre copies, opérationnaliser capital/intérêts et la conversion entre unités physiques et économiques. Priorité suivante : CH09 avec données énergétiques indépendantes, puis un panel produit/coût/prix. Rebond et distribution des gains restent à approfondir.

Deux références supplémentaires, métadonnées et résumés primaires vérifiés : Foster etal. (2005), Schwellnus etal. (2017). Associations précises dans [la revue formelle et bibliographique](25_formal_empirical_review.md); aucun nouveau désaccord global inventé. Aucun push ni commit.
