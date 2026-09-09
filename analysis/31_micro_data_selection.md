# Choix des séries après protocole, avant calcul des résultats

Le protocole31 a été écrit avant la première recherche externe. Des prévisualisations de tables ont ensuite servi à sélectionner les sources ; ce document n'affirme pas que toute valeur source était masquée pendant cette sélection.

Cas maintenu : électricité américaine,2001–2023. Sous-ensemble technique : génération au gaz naturel. Le coût calculé sera **un proxy faible de coût combustible gaz**, et non le coût total d'un kWh vendu aux ménages.

Sources choisies : EIA MER9.8 `ESRCUUS` (prix résidentiel),9.9 `NGERDUS` (coût des réceptions de gaz),A6 `NGETKUS` (heat rate gaz),7.2b (production gaz et totale du secteur électrique),7.6 `ESRCPUS` (ventes résidentielles). Le heat rate concerne des centrales hors cogénération ; la production sectorielle et les réceptions ne constituent pas nécessairement le même échantillon. Ne pas multiplier le heat rate par toute cette production pour fabriquer une consommation totale prétendument mesurée.

Le produit de **deux moyennes** prix combustible et heat rate n'est pas nécessairement la moyenne pondérée des coûts individuels : une covariance et des poids manquent. Il sera donc qualifié WEAK_PROXY au niveau empirique. La seule régression prévue conserve Δlog(prix résidentiel) sur Δlog(de ce proxy), sans interprétation structurelle de son coefficient.

Le déflateur visé est BLS CPI-U général non désaisonnalisé, série CPIAUCNS diffusée par FRED ; moyenne des12 mois et base2023. Les années incomplètes seront exclues, pas interpolées. Il s'agit du prix relatif à ce panier, pas d'un indice de Money.

Qualité partielle : EIA Electric Power Annual11.1, SAIDI selon méthode IEEE avec et sans jours d'événements majeurs ; fenêtre commune2014–2023. Le nombre et le profil des distributeurs déclarants peuvent évoluer. Pas de régression supplémentaire ni de fusion rétroactive de méthodes. Aucun indice composite de qualité n'est construit.

Sources consultées mais non retenues : coût d'exploitation des grands opérateurs privés (EPA8.4, périmètre encore différent) ; MER7.3 sans suffixe renvoie un tableau vide ; 7.4b inclut la chaleur utile de cogénération et ne résout pas notre appariement. L'absence d'une base appariée n'est pas masquée par un changement de secteur.

Conséquence annoncée avant estimation : PRED-MICRO-02,03 et05 ne pourront pas être considérées comme tests identifiés de la chaîne complète avec ces seules séries. Les observations décriront des configurations compatibles, sans reconnaître automatiquement un régime Campergue à partir du seul signe coût/prix.
