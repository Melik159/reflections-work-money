# Reproduction empirique et tests accessibles

> Révision monétaire : FORM-002 ne réfute pas le corpus; son cas n croissant à u constant est explicitement admis dans la possibilité4a lorsqu’il accompagne une création productive. Voir [analyse24](24_money_compensation_scenarios.md). L’arithmétique reste inchangée.

Le code source original est exécuté sans modification dans des sorties temporaires. Les fichiers du dépôt ne sont pas écrasés.

- EMP-001 : smoke test synthétique, beta log-log=1,5, R²>0,999999, assertions originales exécutées.
- EMP-002 : 204 observations, 1990–2023 ; 18 régressions (6 zones × 3 modèles) ; 3 CSV reproduits : données fusionnées, régressions et fenêtres glissantes. Comparaison de toutes les colonnes avec rtol=1e-8 et atol=1e-10.
- FORM-001 : (8/6)^2−1=77,777… %, calcul conditionnel.
- FORM-002 : M=n.u ne suffit pas à imposer dM=0, contre-exemple algébrique hors hypothèse de compensation.

Les deux derniers sont des contrôles formels, **pas des observations empiriques**. HYP-0006 est EASY pour son calcul ; sa loi physique n’est pas validée. HYP-0001 et 0003 : DIFFICULT ; HYP-0002 : MODERATE ; HYP-0004, 0005 et 0007 : NOT_OPERATIONAL_YET.

## Résultats et portée

Le monde donne beta log-log 1,6052 et R² 0,9909 ; en variations annuelles beta 0,8089 et R² 0,6609. L’Allemagne a beta log-log −1,2700 ; la France R² log-log 0,0124. Ces résultats concordent avec le tableau p5 de l’article de Lemariey.

L’énergie est reconstruite par PIB-PPA / PIB-PPA-par-énergie. La cohérence dimensionnelle n’assure ni indépendance de mesure ni causalité ; le numérateur commun ne rend pas non plus la corrélation automatiquement tautologique si le ratio restitue effectivement une mesure énergétique. Une série physique indépendante est le prochain contrôle. Les séries diff sont contiguës ici ; le code ne vérifie pas les trous temporels pour un futur échantillon.

Les régressions OLS n’offrent pas de test de causalité, de cointégration ou d’erreurs HAC. R² élevé n’est pas une significativité statistique générale. Les explications par délocalisation, énergie incorporée et tertiarisation ne sont pas départagées par ce dispositif. Les graphiques ont été générés mais ne font pas l’objet d’une comparaison pixel à pixel.

Résultats, empreintes des inputs, versions et logs dans `analysis/empirical/iteration1/`.
