# Amendement de disponibilité — avant estimation

Le8 septembre2026, après lecture des métadonnées et acquisition partielle, **avant calcul des tendances et régressions** :

1. Le téléchargement FRED du CPI renvoie HTTP404. Remplacement par l'API directe BLS, série CUUR0000SA0 (CPI-U général non désaisonnalisé), trois fenêtres de dix ans maximum. Moyennes annuelles des12 mois et base2023 inchangées. Pas de substitution de concept.
2. Les notes EIA MER9.9 documentent des changements de couverture en2002 et2013. Le panneau descriptif reste2001–2023. L'unique régression en différences exclura les transitions vers2002 et2013, afin de ne pas traiter ces changements connus comme chocs économiques ordinaires. Aucun deuxième modèle de comparaison n'est ajouté. La covariance HAC(2) utilisera les écarts de **calendrier**, pas seulement les positions dans les observations conservées.
3. Les réceptions de combustible restent un proxy du coût consommé ; changement d'inventaire, poids et échantillons distincts ne sont pas observés. La régression n'est pas une estimation du pass-through structurel.

Preuve de disponibilité et rupture : [EIA MER section9, notes tableau9.9](https://www.eia.gov/totalenergy/data/monthly/pdf/sec9.pdf), page PDF13. Les moyennes de coût sont pondérées en Btu ; la couverture passe des seules utilities à d'autres producteurs en2002 et change encore par seuil de puissance en2013. Aucune correction numérique de niveau n'est imposée.

Le protocole initial reste intact et son SHA est conservé dans le manifeste. Cet amendement ne change ni les cinq prédictions ni leurs conditions.
