# Historique des contre-calculs

La première exécution indépendante s'est arrêtée sur le modèle Chine/niveaux : différence maximale1,761196699590073e−8, au-dessus du seuil préfixé1e−8. Cette tentative n'est pas déclarée reproduite.

Diagnostic : la réimplémentation du reviewer calculait la covariance avec la pseudo-inverse de X'X, mal conditionnée lorsque l'échelle énergétique est grande. Correction de l'implémentation du reviewer : sandwich directement par la pseudo-inverse de X, sans former les équations normales. Aucun seuil, échantillon, modèle ou donnée modifié. La seconde exécution et ses écarts sont enregistrés dans independent_results.json.

L'outil pdftoppm n'était pas installé; contrôle visuel des pages207,303,559 réalisé par rendu PyMuPDF en fichiers temporaires. Aucun changement des PDF.
