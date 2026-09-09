# Retrieval du premier lot

Depuis le dépôt, utiliser Python disposant des dépendances du dépôt :

```bash
python3 research_state/iteration001/query.py --collection SOURCE_CORPUS --level PAGE -k 3 --query "Money value added"
python3 research_state/iteration001/query.py --collection DERIVED_ANALYSIS -k 3 --query "Money GDP"
python3 research_state/iteration001/query.py --collection EXTERNAL_LITERATURE -k 3 --query "innovation process product"
```

Le wrapper utilise `rag.iterative.search` en BM25 sur une collection explicite. SOURCE_CORPUS et DERIVED_ANALYSIS sont lus dans `rag/index/iterative.json` ; EXTERNAL_LITERATURE dans `external_literature_index.json`. Aucun index n’est reconstruit. Un index absent, un filtre vide ou une provenance incohérente produit une erreur ; aucune autre collection ne sert de repli.

Chaque résultat JSONL conserve document, page, section, chunk, score et source_type. Le score indique un classement lexical, pas une qualité de preuve. Les six blocs externes actuellement enregistrés constituent un petit index documentaire ciblé, sans évaluation indépendante de pertinence.

RAG = localisation. La page source originale et son contexte sont la preuve documentaire à contrôler ; les analyses dérivées ne remplacent jamais le manuscrit ni les publications externes. Les tests smoke vérifient seulement exécution et métadonnées, pas pertinence ni conclusions scientifiques.
