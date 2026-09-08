# Protocole de contre-vérification — avant calcul

Périmètre : état figé par baseline.json. Aucune écriture dans la synthèse. Les calculs suivants sont des diagnostics locaux, pas une nouvelle estimation du système entier.

1. Recalcul indépendant des30 spécifications énergétiques archivées à partir du panel, par pseudo-inverse et covariance HAC écrite séparément. Comparer coefficients, R², erreurs-types et N à tolérance1e−8; aucune sélection selon résultat. Recalculer le seul modèle électrique avec distances calendaires et exclusions2002/2013. Un écart non expliqué serait une erreur de reproduction; une égalité ne garantit pas le design.
2. Vérifier dix propositions algébriques/cas limites : produit fini n·u; cp variable; recodage Utility; limite de deux infinitésimaux; force constante; inversion de Core Law; moyenne de carrés; M positif contre primitive signée; borne de rendement; valeur ajoutée contre transactions brutes. Les contre-exemples doivent préciser la prémisse visée, sans prétendre satisfaire toutes les hypothèses du manuscrit.
3. Tester, exclusivement sur des copies en mémoire, si le validateur de synthèse accepte un résultat textuel sémantiquement incorrect ou un chemin de source sans rapport. Aucune modification des fichiers internes. Acceptation = limite du contrôle sémantique, non corruption du dépôt.

Restrictions : régressions descriptives seulement; aucun test de causalité, aucun nouveau téléchargement de panel, pas de seuil de significativité transformé en décision de validité. Les exemples synthétiques n'ont aucune qualité de données économiques. Les comptages des tests seront établis méthode par méthode, avec une catégorie primaire exclusive et un commentaire de portée.
