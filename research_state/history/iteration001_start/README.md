# Boucle de recherche — état partagé

La baseline Git `583a4a29e9928d224359a96a14585408bc455b98` reste la référence. Aucun claim, statut RQ, synthèse ou certificat gelé n'est automatiquement réécrit.

Lire `NEXT_ACTIONS.yaml`, les dossiers de questions et les sources avant de sélectionner une tâche. Les rôles sont des perspectives de relecture, pas des chercheurs indépendants ni des votes. Toute divergence non tranchée va dans `OPEN_CONTRADICTIONS.md`.

## Commandes

Depuis la racine, utiliser `.venv-research/bin/python` si disponible, sinon `python3` avec les dépendances du dépôt :

```bash
python -m rag.iterative build
python -m rag.iterative query --collection SOURCE_CORPUS --level PAGE "Money saved"
python -m rag.iterative query --collection DERIVED_ANALYSIS "Money referents"
python -m rag.iterative benchmark
python -m research_state.cycle prepare 1
# Lire réellement les pages et le contexte : aucune lecture n'est attestée par le script.
python -m research_state.cycle finish 1
```

`finish` exécute le diagnostic local, `./verify.sh`, les nouveaux tests et le contrôle du manifeste gelé avant de marquer DONE. Les protocoles préparés ne sont pas réécrits ; chaque cycle conserve ses sorties et son journal. Ne pas réexécuter un cycle DONE. Les scripts fournis prennent en charge les trois premiers protocoles ; les cycles suivants nécessitent une analyse et un protocole propres.

Les collections ne sont jamais fusionnées implicitement. Une note bibliographique rédigée par l'assistant reste DERIVED_ANALYSIS, pas EXTERNAL_LITERATURE. Cette dernière est vide tant qu'aucun texte externe vérifié n'est enregistré. PAGE, blocs PARAGRAPH issus de l'extraction, SECTION Markdown et CLAIM_WINDOW coexistent. Les sections PDF non identifiées portent UNDETECTED. Les fenêtres de claims sources contiennent le texte de page, pas la reformulation du claim.

Le benchmark compare BM25 et fusion BM25/TF-IDF locale. Aucun modèle d'embeddings sémantiques n'est disponible dans l'environnement ; cette extension reste OPEN. Ni les notes de recherche ni une réponse RAG ne sont une preuve primaire. Les diagnostics synthétiques ne sont pas des observations économiques.
