# RAG — comparaison conservée

| Méthode/périmètre | Recall@1 | Recall@3 | Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|
| legacy | 0.2348 | 0.5530 | 0.5833 | 0.3838 |
| tfidf | 0.4621 | 0.6667 | 0.7727 | 0.5740 |
| bm25 | 0.4924 | 0.6818 | 0.8030 | 0.6121 |
| bm25_extended | 0.4924 | 0.7273 | 0.7879 | 0.6121 |
| bm25_normalized | 0.4924 | 0.7273 | 0.7879 | 0.6121 |
| bm25_bilingual | 0.5000 | 0.7424 | 0.8182 | 0.6303 |

Les trois premières méthodes utilisent le corpus initial de trois documents : elles restent directement comparables à la phase précédente. Les variantes extended, normalized et bilingual utilisent cinq documents, 590 chunks (26 pages secondaires ajoutées). La normalisation seule n’apporte pas de gain. L’expansion de vocabulaire français–anglais améliore le résultat global et le français.

Français : Recall@5 passe de 0 à 0,3333, MRR@5 à 0,20 sur seulement six questions. La résolution n’est donc que partielle. Le dictionnaire ne contient ni IDs, ni pages, ni réponses. Il a été élaboré après inspection des erreurs du jeu de développement : **gain en échantillon**, à confirmer sur des questions françaises nouvelles. Certaines pages des articles secondaires sont pertinentes mais ne figurent pas dans les jugements initiaux, qui restent inchangés.

BM25 reste le moteur par défaut avec expansion légère ; `--no-expansion` conserve le comportement lexical. Les variantes et résultats sont enregistrés, sans écraser le benchmark pré-itération archivé. Aucune API ni embedding distant.
