# Livraison publique de la baseline

Le propriétaire a explicitement remplacé la demande de publication privée par une publication publique. Seule la branche `research/corpus-validation` est destinée au push ; `main` et les PDF sources restent inchangés.

Le premier contrôle de livraison a révélé que `analysis/run_empirical_iteration1.py` réécrivait les journaux et la commande enregistrée avec des chemins temporaires variables. Les trois empreintes concernées étaient devenues différentes du certificat de clôture. Les résultats tabulaires restent contrôlés contre les sorties scientifiques de référence.

La livraison ajoute un mode `--check` : les reproductions sont exécutées dans un répertoire temporaire, comparées aux tables, résultats et empreintes d'entrée enregistrés, sans réécrire les artefacts de baseline. `verify.sh` utilise désormais ce mode. Aucun résultat économique ni PDF n'est modifié par cette correction.

Le certificat et les scripts antérieurs sont conservés dans `history/private_delivery_20260908/`. Le manifeste courant est actualisé explicitement pour la livraison ; `delivery_manifest_changes.json` dans ce dossier historique conserve les anciennes et nouvelles empreintes. Les anciens octets des trois sorties écrasées par la première vérification ne sont pas récupérables depuis Git (fichiers alors non suivis) ; leurs anciennes empreintes restent conservées.

Les environnements locaux, secrets `.env` et le cache RAG reconstruisible sont exclus. Les journaux scientifiques nécessaires à la traçabilité restent inclus. Le contrôle de secrets est heuristique et ne constitue pas une garantie absolue. Les tests vérifient l'infrastructure, des propriétés formelles locales et des reproductions, pas une validité économique globale.
