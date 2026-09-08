# RQ-08.01 — tests de deuxième passe

Deux produits antérieurs recalculés ; extension à trois exécutée. DESIGNED_NOT_EXECUTED : inventaire de contributions machine/opérateur évitant double compte.

Hypothèse/prédiction : Sommes de prix×quantités invariantes à regroupement et changement cohérent des unités ; indices moyens seulement avec leurs poids. Le test antérieur de somme de qualités ne représente pas une règle Campergue.

Variables et données : l,T,e déclarés additifs p210 ; Laziness p307 et Avarice p309. Utility est explicitement intensive et NON ADDITIVE p108.

Conditions : Même unité, même tâche ou conversion explicitée, contribution non recouvrante, frontières production/consommation distinguées.

Résultat incompatible ou contre-exemple : Les trois produits A/B/C donnent indice pondéré0,92, moyenne égale0,9333 et K agrégé72/43→44/51. Poids modifiés changent le résultat sans incohérence de la somme.

Explications concurrentes / domaine : Utility ne se somme pas. Une entreprise qui pilote une machine et la machine ne doivent pas chacune recevoir toute sa contribution physique.

Les cinq diagnostics synthétiques figurent dans second_pass_formal_results.json ; les anciens résultats restent comparés par verify.sh. Les projets exigeant des données nouvelles sont DESIGNED_NOT_EXECUTED.
