# Phase 2 — audit de départ (2026-09-08)

HEAD source confirmé : `a697345c427fca8de0521108a17aa2b76f267654`.
Branche : `research/corpus-validation`. SHA-256 du manuscrit confirmé :
`7981eca40bca1c5ce54d96b3c840eda34d0e7d01fdc89fe9748c3c047c6f3827`.
Les fichiers de recherche sont non suivis par Git ; aucun push.

## État observé avant modification

- 562 lignes d'extraction paginée ; 564 chunks : manuscrit et deux Markdown.
- 3 claims, 5 entrées conceptuelles, 3 nœuds et 2 arêtes.
- Les 5 concepts sont tous `SOURCE_PENDING_REVIEW` : ce ne sont pas encore des définitions sourcées.
- Les deux autres PDF et la documentation du code ne sont pas indexés.
- Aucun golden set, aucun test pytest, aucun benchmark retrieval.
- Le moteur est TF brut × IDF avec fréquence documentaire par sous-chaîne.
  Le nom « TF-IDF » ne décrit donc pas un cosinus TF-IDF normalisé.
- Les extraits retournés sont les 500 premiers caractères, même si le passage pertinent est plus loin.

## Vérification réellement exécutée

Commande : `./verify.sh`.
Résultat : **FAIL**, code 127, `./verify.sh: line 3: python: command not found`.
`python3` existe sous `/usr/bin/python3`. Aucun contrôle interne n'a été exécuté
par cette invocation. Le PASS du tour précédent n'est pas un PASS de cet environnement.

Le script initial implémente seulement : nombre de lignes égal à 562,
nombre de chunks supérieur ou égal à 562, présence de source_document et page
pour chaque claim. Il ne vérifie ni empreintes, ni citations, ni pages uniques,
ni intégrité du graphe, ni distinctions conceptuelles, ni qualité du retrieval.

## Corrections de provenance nécessaires

- CPC-0001 : la question commence **page PDF 2**, se poursuit **page PDF 3**.
  L'attribution de toute la citation à la seule page 3 est incorrecte.
- CPC-0002 : `...` remplace des mots dans la citation prototype ; il faut
  restaurer un passage continu vérifiable.
- CPC-0003 : le lien depuis une question est une motivation, pas une prémisse logique démontrée.
- Les huit axes initiaux n'ont pas été établis par une lecture intégrale.
- La lecture intégrale du README, des articles et du manuscrit n'est pas attestée
  par les artefacts existants.

## Règle de continuité

Les prototypes modifiés sont archivés avant migration dans `analysis/history/phase1/`.
Les IDs CPC-0001 à CPC-0003 sont préservés. Une page ne devient pas « examinée »
par simple ingestion, indexation ou détection automatique de titres.
