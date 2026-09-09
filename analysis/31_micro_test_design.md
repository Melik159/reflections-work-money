# 31 — Protocole préalable : électricité aux États-Unis

Écrit avant recherche externe, téléchargement ou analyse de nouvelles données pour cette passe, le 8 septembre 2026. Les références au corpus proviennent des analyses déjà conservées. Statut du protocole : prospectif pour cette acquisition ; pas un préenregistrement externe.

## Cas choisi et critère d'arrêt

Un cas principal : **électricité américaine**, avec production électrique et prix payé par les ménages. Fenêtre visée : 2001–2023, annuelle ; utiliser la fenêtre commune effectivement disponible, sans interpolation. Les séries institutionnelles EIA sont prioritaires. Le secteur agrégé n'est pas une entreprise ni un produit parfaitement homogène : ce cas peut examiner des maillons observables, pas à lui seul une chaîne micro causale. Cette restriction sera conservée même si les corrélations sont fortes.

Proxy de coût envisagé : coût du combustible utilisé pour produire l'électricité ; rendement thermique pour convertir un prix énergétique en coût par kWh lorsque périmètres compatibles. Si seuls un combustible/une technologie sont disponibles, ne pas en faire le coût moyen du système électrique. Un prix de gros ne sera pas appelé coût de production. Aucun spread détail–combustible ne sera appelé profit ou markup observé.

Qualité : fiabilité du service, si une série comparable est accessible sur la fenêtre ; sinon UTILITY_NOT_IDENTIFIABLE. Quantité physique en kWh n'est pas une mesure de qualité. Rendement de conversion n'est pas Utility. Pas de deuxième secteur pour compenser une absence d'identification.

## Variables définies avant acquisition

| Variable Campergue | Donnée/proxy recherché | Unité | Classe | Justification et limite |
|---|---|---|---|---|
| T | Aucun niveau directement mesuré | UNRESOLVED | NOT_OBSERVABLE | Primitive/Work restant selon référent ; ni kWh ni heures ne suffisent |
| dT / Economic Work | Variation d'efficacité technique éventuellement documentée | Indice sans dimension pour le proxy seulement | WEAK_PROXY | Rendement technique ne mesure pas Force, complexité ou Utility Campergue |
| Energy | Intrant combustible physique de génération ; chaleur par kWh | Btu, MMBtu ; Btu/kWh | DIRECT_MEASURE | Mesure statistique physique agrégée, pas énergie économique |
| Cost | Prix combustible × consommation combustible par kWh | cents courants/kWh | PROXY | Coût combustible seul ; capital, personnel, réseau, taxes et mix omis |
| Price | Recettes résidentielles / ventes résidentielles | cents courants/kWh | PROXY | Prix moyen réalisé, pas tarif marginal ni panel à consommation fixe |
| Utility / quality | Fiabilité/interruptions si disponible | minutes/client/an ou indicateur documenté | WEAK_PROXY | Qualité partielle du service, pas préférence subjective ni Utility définie par l'auteur |
| Production | Production nette d'électricité | kWh/an | DIRECT_MEASURE | Production physique ; ne pas l'identifier à la création de richesse |
| Quantity | Ventes résidentielles et éventuellement par client | kWh/an ; kWh/client/an | DIRECT_MEASURE | Quantité vendue, pas demande contrefactuelle |
| Purchasing power | Quantité accessible avec un budget nominal fixe | kWh pour100USD | PROXY | Pouvoir d'achat pour un seul service ; pas pouvoir d'achat général |
| Consumer gain | Économie pour un panier électrique fixe si prix baisse | USD pour1000kWh | PROXY | Coût évité conditionnel, pas surplus compensatoire ni Money directement mesuré |
| Money | Pas de mesure indépendante | UNRESOLVED | NOT_OBSERVABLE | Requiert traductions de u, Utility, référent et prix comparables |

En l'absence d'un déflateur indépendant acquis, les résultats resteront nominaux. Si un CPI général officiel est accessible, calculer séparément prix réel en année de base fixe et gain réel à panier fixe, sans attribuer au CPI la mesure de u de Campergue. Le prix, la quantité ou le résidu d'une régression ne serviront jamais à reconstruire Utility.

## Cinq prédictions conditionnelles à examiner

### PRED-MICRO-01 — Efficacité et coût combustible

Source : CPC-0019,0096 ; PDF32 et460–462. Si moins d'intrant énergétique permet le même kWh et si le prix de cet intrant est fixe, le coût combustible unitaire baisse. Horizon : comparaison annuelle de procédés comparables. Alternative : prix combustible en hausse ou composition des centrales modifiée. Observation incompatible avec cette identité/proxy : coût calculé augmente à prix et périmètre effectivement fixes. Ce n'est pas encore une prédiction quantitative de T.

### PRED-MICRO-02 — Transmission à profit absolu constant

Source : CPC-0098, PDF503–506. À produit comparable, profit unitaire absolu et autres coûts constants, baisse du coût total → baisse égale du prix. Variables nécessaires : coût total et prix au même stade. Horizon annuel exploratoire, aucun délai de transmission spécifique attribué au manuscrit. Alternative : branche prix maintenu, variation des autres coûts ou qualité. Observation incompatible : prix ne suit pas alors que toutes les conditions sont indépendamment observées constantes. Sans coût total/profit, statut NOT_IDENTIFIABLE, même si une corrélation combustible–prix est estimée.

### PRED-MICRO-03 — Prix maintenu et gain retenu

Source : CPC-0020,0021,0097 ; PDF20–21. Coût total inférieur et prix inchangé peuvent accroître l'écart prix–coût, sans gain de prix immédiat au consommateur. Horizon annuel. Alternative : coûts de réseau/capital ou qualité absorbent la baisse combustible. Observation incompatible avec la branche à autres éléments fixes : coût total baisse, prix reste fixe, mais écart prix–coût n'augmente pas. Le profit n'est pas assimilé au spread détail–combustible. Pour classifier descriptivement une stabilité, seuil fixé ici à |Δprix/prix précédent|≤1% ; afficher aussi les variations exactes.

### PRED-MICRO-04 — Gain du consommateur et usage possible

Source : CPC-0015,0099,0127 ; PDF19,33,400. À revenu/budget et qualité fixes, baisse du prix → panier identique moins cher et davantage de kWh accessibles. Aucun accroissement effectif des achats n'est nécessaire : le gain peut être conservé ou dépensé ailleurs. Horizon même année pour l'arithmétique ; usage ultérieur non testé. Observation incompatible : coût du panier fixe augmente malgré prix unitaire inférieur à définition identique. Alternatives standard : effet prix/revenu, mêmes conséquences.

### PRED-MICRO-05 — Signature spécifique Work/Money

Source : CPC-0095,0096,0119 ; PDF203,207,455. La branche quadratique demande dT=cp·ω·dω, cp fixé et travail utile à l'évolution d'Utility. Il faut cp, ω et T indépendamment mesurés, pas un T construit depuis ω pour ensuite tester l'identité. Horizon : transformation comparable, non simple somme annuelle de secteurs. Observation incompatible : une mesure indépendante de T ne suit pas la formule lorsque ses conditions sont remplies. Sans ces mesures : NOT_IDENTIFIABLE. Alternatives : progrès technique, substitution capital/travail, mix et rendements techniques classiques.

## Explications concurrentes fixées à l'avance

01 : rendement thermique, prix d'intrant et mix technologique. 02 : répercussion des coûts, concurrence ou régulation tarifaire. 03 : pouvoir de marché, coûts fixes, investissements et décalages tarifaires. 04 : arithmétique budgétaire et effets revenu/substitution. 05 : modèles de production standard sans la définition de Work Campergue. Aucun résultat commun ne sera appelé confirmation spécifique.

## Analyse parcimonieuse prévue

1. Inventaire des séries, unités, lacunes et frontières. Acquisition figée avec SHA ; aucune imputation.
2. Tendances et variations annuelles de prix, coût combustible/proxy et quantités ; ratios physiques seulement à périmètre cohérent.
3. **Une régression descriptive** : Δlog(prix résidentiel) sur Δlog(proxy combustible), avec constante, si N≥15 années consécutives. IC95% HAC(2), asymptotiques ; pas de sélection par significativité, pas de causalité. Si frontière incompatible, résultat seulement contexte sectoriel, non test direct de transmission micro.
4. Gain à1000kWh et budget100USD ; quantité effectivement vendue séparée. Comparaison prix nominal/réel si déflateur disponible.
5. Qualité et Money : documenter explicitement les variables absentes. Aucun modèle supplémentaire pour les « retrouver ».

Statuts de résultat : FORMALLY_CONSISTENT, EMPIRICALLY_COMPATIBLE, EMPIRICALLY_QUALIFIED, EMPIRICALLY_CONTRADICTED, NON_DISCRIMINATING, NOT_IDENTIFIABLE. Money : DIRECTLY_OBSERVED, INDIRECTLY_INFERRED, COMPATIBLE ou NOT_IDENTIFIED, dans son champ séparé.

## Expérience à deux produits, distincte des données

Créer deux produits fictifs avec prix, coût, quantité et Utility **stipulée** différents ; faire évoluer prix et quantités différemment. Comparer sommes pondérées, normalisation cohérente et changements de poids. Tester notamment l'invariance à une unité de compte commune et la non-invariance d'une moyenne d'utilités arbitrairement normalisées. Les nombres sont synthétiques, non des observations Campergue et non une calibration de Money.
