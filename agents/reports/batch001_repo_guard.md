# Contrôle dépôt — premier lot

Branche constatée : `research/corpus-validation`. État Git initial : `?? rag/iterative.py` et `?? research_state/`. Aucun fichier AGENTS.md applicable trouvé dans le dépôt ou ses parents. Aucun push, commit, suppression ni écriture de baseline effectué.

`./verify.sh` a été exécuté dans une copie temporaire complète du dépôt (`/tmp/campergue-verify-66yxqrfk/repo`). Cette isolation est nécessaire parce que le script réécrit index, résultats de retrieval, contrôles productifs et scoreboards. Il ne fallait pas prendre le risque de réécrire la baseline originale, même à contenu identique. La copie réutilise l’environnement Python local par lien, sans le modifier.

Résultat : 128/128 PASS ; 109 STRUCTURAL, 17 FORMAL locaux, 2 EMPIRICAL_REPRODUCTION, 0 INDEPENDENT_DISCRIMINATING. Ceci est une vérification structurelle et de reproduction, pas une découverte scientifique. Les avertissements sont conservés intégralement dans `agents/logs/batch001/verify.log`.

Le manifeste SHA-256 de 961 entrées passe avant contrôle dans l’original et après contrôle dans la copie. Les empreintes avant/après des 961 fichiers originaux sont strictement identiques. Détails : `agents/logs/batch001/integrity_summary.json`, `baseline_before.json`, `baseline_after.json`. Le script original n’a pas été lancé dans l’original. Une vérification finale du manifeste reste nécessaire après les ajouts du lot.

Les 18 fichiers directement présents dans research_state au début de session sont copiés sans récursion dans `research_state/history/iteration001_start/`, avec `snapshot_sha256.json`. Les anciens cycles et artefacts restent à leur emplacement.

## Retrieval disponible

`python3 -m rag.iterative query --collection SOURCE_CORPUS --level PAGE -k 5 "Money saving"`

`python3 -m rag.iterative query --collection DERIVED_ANALYSIS -k 5 "Money GDP"`

Index existant : SOURCE_CORPUS 1473 chunks ; DERIVED_ANALYSIS 5222 ; EXTERNAL_LITERATURE 0 ; 629 fichiers d’entrée empreintés. Retour : document, page, section, chunk, score et source_type. Sections PDF non détectées : UNDETECTED, sans invention. PARAGRAPH correspond aux blocs d’extraction, CLAIM_WINDOW reprend une page source complète. Méthodes lexicales BM25/TF-IDF/hybride ; pas d’embeddings sémantiques disponibles.

La collection externe est vide et le constructeur n’implémente pas l’enregistrement de textes externes : des notes internes bibliographiques ne deviennent pas des sources primaires. Toute recherche web externe doit être journalisée séparément et consultée dans son document original. L’index n’est pas une preuve ; lire les pages sources retrouvées.

Ne pas réexécuter `research_state/cycle.py` pour la nouvelle série : il contient trois anciennes configurations avec conclusions pré-écrites et un appel verify dans l’original. Le wrapper research_state/verify.sh appelle également ce verify. Les nouveaux tests structurels devront être lancés explicitement à la fin sans attribuer de statut scientifique.
