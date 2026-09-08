# Évaluation retrieval réellement exécutée

| Méthode | Recall@1 | Recall@3 | Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|
| legacy | 0.2348 | 0.5530 | 0.5833 | 0.3838 |
| tfidf | 0.4621 | 0.6667 | 0.7727 | 0.5740 |
| bm25 | 0.4924 | 0.6818 | 0.8030 | 0.6121 |

66 questions de développement (60 anglais, 6 français), sur les pages examinées. Corpus indexé inchangé : 564 chunks, 3 documents. Aucune réponse de LLM. Pertinence = document ET page attendus ET passage exact normalisé. Recall est la proportion des pages attendues retrouvées ; MRR est tronqué à 5.

BM25 (k1=1,2, b=0,75) est le meilleur sur ce jeu et devient le défaut ; legacy et cosinus TF-IDF restent disponibles. Aucun réglage de paramètres ni de synonymes sur les erreurs. Les embeddings ne sont pas implémentés : aucune pile vectorielle présente, benchmark lexical sans dépendance choisi à ce stade ; impossibilité matérielle non alléguée.

Limites : pertinence non exhaustive (répétitions ailleurs possibles), questions construites à partir des claims, pas de jeu tenu à l’écart, faible échantillon français, chapitres tardifs non couverts. Les scores ne certifient pas la qualité sur les 562 pages. Résultats individuels et par langue dans `results.json`.

Le texte intégral du chunk est maintenant renvoyé ; un préfixe arbitraire de 500 caractères pouvait cacher le passage justificatif. Les citations inter-pages restent représentées par plusieurs attentes paginées.

## Limite linguistique observée

- legacy : Recall@5 français = 0.0833, anglais = 0.6333.
- tfidf : Recall@5 français = 0.0000, anglais = 0.8500.
- bm25 : Recall@5 français = 0.0000, anglais = 0.8833.

Le choix BM25 améliore le score global mais ne résout pas les requêtes françaises. Aucun résultat français satisfaisant n’est revendiqué.
