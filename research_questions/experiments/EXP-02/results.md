# EXP-02 — Quelles opérations survivent au classement ordinal ?

Statuts : FORMALLY_SUPPORTED (invariances conditionnelles), FORMALLY_QUALIFIED, BLOCKED_BY_MEASUREMENT pour les résultats numériques économiques. Aucun Utility ni Money observé. Protocole figé et résultats exacts en JSON.

## SOURCE

PDF108–109: Utility non additive; classement proposé en l’absence de mesure. PDF283: `FA p=rP UP`; préférences `UA>UP` et inverse. PDF291: scénarios selon signes d’évolution de prix/Utility. PDF347, relation12-03: `M=rP UP ln(pf/pi)` dans le domaine isopheles. PDF349, relation12-04: `M=rP(UPf−UPi)/(1−γTM)`. PDF385 garde une inégalité; PDF386 donne l’égalité de rendement pour le cas réversible. PDF415: `dETM^L=P dUP+FA dp`. Transcriptions locales, signes et domaines conservés.

## INTERPRETATION — table des exigences

| FORMULA / opération | OPERATION_ON_UTILITY | ORDINAL_SUFFICIENT? | CARDINAL_REQUIRED? | RATIO_SCALE_REQUIRED? | SOURCE_PAGE |
|---|---|---|---|---|---|
| UP>UA pour un même agent | comparaison | Oui, échelle ordinale commune aux options | Non | Non |283|
| UPf=UPi; signe de ΔUP | égalité / orientation | Oui sous transformation croissante commune | Non | Non |291,349|
| Classement d’objets | ordre | Oui | Non | Non |109|
| Valeur numérique ΔUP | différence | Non | Structure d’intervalle, unité fixée | Non |349|
| M=rP ΔUP/(1−γTM) | différence pondérée | Non pour valeur de M; égalité ΔUP=0 reste définie | Oui; rP doit se transformer avec l’unité | Non si seuls écarts entrent |349|
| η=1−UP2/UP1 | ratio | Non | Oui, plus qu’un simple intervalle | Oui, UP1≠0 et origine significative |386|
| η≥1−UP2/UP1 | borne numérique | Non | Oui | Oui; ne pas remplacer ≥ par = |385|
| FA p=rP UP | produit avec niveau | Non pour forme à coefficient constant | Oui | Échelle de rapport si rP est seul coefficient multiplicatif fixe |283|
| M=rP UP ln(pf/pi) | niveau multiplicatif | Non | Oui | Oui sous même forme et coefficient constant; contexte isopheles |347|
| P dUP dans un potentiel | différentiel pondéré | Non pour sa valeur numérique | Échelle différentiable et transformation du coefficient conjugué | Pas nécessairement: translation disparaît dans dUP |415|

« Cardinal » est ici précisé par opérations, pas utilisé comme synonyme de « rapport ». Une origine significative n’est pas un zéro physique arbitrairement importé. Comparer plusieurs agents sur des échelles indépendantes ajoute un problème de comparabilité non résolu par un classement individuel.

## Résultats

Sous U→aU, a>0, ratios inchangés. Sous U→aU+b, les différences sont multipliées par a et les rapports de différences inchangés, mais les rapports de niveaux changent généralement. Sous une transformation croissante non affine, seuls ordre, égalités et signes de différences sont garantis.

Une nuance importante: la formule de différences PDF349 reste covariante sous U→aU+b si rP→rP/a, γ fixé et différent de1. Elle n’exige pas une origine absolue. En revanche, un coefficient rP multiplicatif unique ne compense généralement pas une translation dans `rP UP` pour plusieurs états. Réajuster rP séparément à chaque état sauverait une identité comptable, pas le même modèle local à coefficient constant.

Pour le différentiel PDF415, une reparamétrisation différentiable inversible U'=f(U) permet formellement P'=P/f'(U); cela conserve le produit mais change la loi du coefficient conjugué. Ce n’est pas une preuve que le corpus possède cette covariance générale. Aucune somme de Utility n’a été utilisée.

## Portée

REQUIRES_CARDINAL_UTILITY pour les résultats quantitatifs concernés. Les classifications des scénarios fondées uniquement sur les signes peuvent rester formulées, sans devenir vraies empiriquement par cette seule invariance. Le test qualifie les besoins de mesure, pas toutes les propositions où Utility apparaît.

Méthode complémentaire: [JCGM VIM3, quantité ordinale](https://jcgm.bipm.org/vim/en/1.26.html), entrée officielle vérifiée; elle distingue classement et opérations algébriques. La classification précise des formules ci-dessus est une analyse nouvelle, non un résultat attribué au JCGM.
