# iteration_report_001 — premier lot de recherche continue

Date : 2026-09-08. Branche : research/corpus-validation. **Dix cycles terminés; arrêt du lot. Baseline inchangée, aucun push.** Les dix décisions QUALIFY portent sur des propositions séparées. Aucune découverte n'a été intégrée dans les127claims,53questions, synthèse ou statut académique.

## CYCLES — completed

10/10 cycles ITER001-C01..C10, chacun avec une tâche principale, sources, rapport spécialisé, revue adversariale, contrôle de traçabilité, décision et candidat. Les trois cycles historiques CYCLE-001..003 existaient au démarrage : conservés et non recomptés. État initial [archivé](history/iteration001_start/), [registre de lecture baseline](iteration001/baseline_read_register.json).

| Cycle | Tâche principale | Découverte classée | Décision | Candidat |
|---|---|---|---|---|
| ITER001-C01 | Money / référents / PIB / valeur ajoutée | CONFIRMS_EXISTING | QUALIFY | [ITER001-C01.json](../candidate_changes/empirical/ITER001-C01.json) |
| ITER001-C02 | T et cp : mesure indépendante | CONFIRMS_EXISTING | QUALIFY | [ITER001-C02.json](../candidate_changes/formalism/ITER001-C02.json) |
| ITER001-C03 | Utility : échelle et observabilité | NEW_SCENARIO | QUALIFY | [ITER001-C03.json](../candidate_changes/concepts/ITER001-C03.json) |
| ITER001-C04 | K : stabilité et agrégation | NEW_SCENARIO | QUALIFY | [ITER001-C04.json](../candidate_changes/formalism/ITER001-C04.json) |
| ITER001-C05 | Energy → useful work → Economic Work | NEW_SCENARIO | QUALIFY | [ITER001-C05.json](../candidate_changes/empirical/ITER001-C05.json) |
| ITER001-C06 | Innovation → productivity → growth | NEW_LITERATURE_PARALLEL | QUALIFY | [ITER001-C06.json](../candidate_changes/questions/ITER001-C06.json) |
| ITER001-C07 | Destination des gains productifs | NEW_SCENARIO | QUALIFY | [ITER001-C07.json](../candidate_changes/empirical/ITER001-C07.json) |
| ITER001-C08 | Consommation marginale → énergie / matière | NEW_SCENARIO | QUALIFY | [ITER001-C08.json](../candidate_changes/empirical/ITER001-C08.json) |
| ITER001-C09 | Dommages environnementaux | NEW_MEASUREMENT_ISSUE | QUALIFY | [ITER001-C09.json](../candidate_changes/concepts/ITER001-C09.json) |
| ITER001-C10 | Programme épistémologique et cohérence interne | CONFIRMS_EXISTING | QUALIFY | [ITER001-C10.json](../candidate_changes/questions/ITER001-C10.json) |

La préparation RAG et l'extraction de C02–C10 ont été mutualisées en amont; elles ne comptent ni comme cycles ni comme lectures. Les sources et revues scientifiques ont ensuite été traitées par tâche. Les attestations de préparation restent distinctes des lectures consignées dans les rapports. Rôles successifs du même orchestrateur pour C03–C10; sous-agent spécialiste pour C01/C02, rôle code pour calculs et dépôt, adversaire distinct pour C01 et revue finale ciblée. **Pas dix experts indépendants ni certification institutionnelle.**

## TASKS — done / blocked / open

- Tâches principales du lot : **10 DONE**,0 BLOCKED,0 OPEN au sens revue/proposition documentaire accomplie.
- Expériences proposées : **8 BLOCKED**,2 DESIGN,0 READY,0 COMPLETED empiriquement. Les cinq diagnostics formels exécutés restent séparés de la collecte économique à faire.
- Prochain lot : **10 OPEN** (ITER002-P0-01..10), non lancé.
- Historique préexistant conservé séparément :3DONE,2BLOCKED,8OPEN. Aucun suivi historique n'est réputé exécuté par simple recouvrement de thème.

Les questions scientifiques ne deviennent pas résolues parce que leur tâche de conception est DONE. [File des tâches](NEXT_ACTIONS.yaml), [file des expériences](EXPERIMENT_QUEUE.yaml).

## CLAIMS — candidate changes

**10 candidats auditables**, reliés à33claims existants; **0claim canonique créé ou modifié**. Les cibles sont les notes/conclusions proposées, jamais une réécriture automatique. Chaque JSON contient target,current_state,proposed_state,evidence,counterevidence,reviewers,confidence,reason,impact, les pages et limites. current_state reprend les IDs/statuts de référence et empreintes des fichiers cibles.

Claims liés : CPC-0001, CPC-0003, CPC-0009, CPC-0010, CPC-0015, CPC-0016, CPC-0017, CPC-0031, CPC-0035, CPC-0042, CPC-0043, CPC-0044, CPC-0046, CPC-0051, CPC-0052, CPC-0054, CPC-0055, CPC-0057, CPC-0062, CPC-0066, CPC-0068, CPC-0084, CPC-0099, CPC-0104, CPC-0106, CPC-0109, CPC-0112, CPC-0117, CPC-0118, CPC-0119, CPC-0120, CPC-0122, CPC-0127. Un lien de recherche ne signifie pas que le claim contient toutes les propositions du candidat. C09 utilise directement PDF112 comme source complémentaire, sans inventer un claim canonique pour cette phrase.

## QUESTIONS — affected

23questions reliées aux candidats : RQ-01.01, RQ-01.04, RQ-02.03, RQ-03.03, RQ-04.01, RQ-04.02, RQ-04.03, RQ-04.04, RQ-05.03, RQ-06.01, RQ-06.03, RQ-07.02, RQ-08.02, RQ-09.01, RQ-09.02, RQ-09.03, RQ-10.02, RQ-11.01, RQ-11.02, RQ-11.03, RQ-12.01, RQ-12.02, RQ-12.03. **Statuts canoniques inchangés.** Les questions plus précises sont dans NEXT_ACTIONS et les candidats, pas dans le graphe gelé.

## NEW EVIDENCE

Aucune nouvelle observation économique, énergétique ou environnementale. Les pages du corpus ont été relues pour attribution et contexte : ce sont des contrôles ciblés de sources existantes, pas une nouvelle preuve historique ni une nouvelle couverture globale.

Deux textes primaires externes acquis avec empreintes et pages vérifiées pour C06. Leurs apports sont documentaires : mécanismes comparables et catégories de collecte. Cinq diagnostics formels conditionnels supplémentaires sont exécutés ci-dessous; leur portée ne dépasse pas les hypothèses déclarées.

## NEW COUNTEREVIDENCE

Les nouveaux exemples contestent des **inférences de l'analyste**, pas une proposition économique du corpus déjà identifiée sans ambiguïté : cohérence des raccords ne prouve pas une échelle Utility; stabilité agrégée ne prouve pas stabilité des composantes; gain panier ne prouve pas gain total de ressources; épargne temporaire et dépense ultérieure ne sont pas deux usages finals; taux et dommage par tâche ne sont pas la même grandeur.

Contre-évidence source conservée : PDF205 restreint à valeur ajoutée; PDF190 admet des utilités différentes; PDF198 sépare vitesse et cause; PDF523 autorise thésaurisation; PDF455 impose Utility au pont physique; PDF558 refuse de déduire causalité de corrélation. Ces qualifications sont héritées, non des découvertes attribuées à ce lot.

## NEW DISPUTES / DISPUTES RESOLVED

0nouvelle dispute,0résolue. DISPUTE-0001 hérité demeure OPEN; [registre](OPEN_DISPUTES.md), ancien OPEN_CONTRADICTIONS.md conservé. Pas d'arbitrage par vote. La [revue finale distincte](../agents/reports/batch001_final_adversarial.md) ne relève pas d'opposition substantielle constituée; ses réserves sont reprises dans la [réponse](iteration001/final_review_response.md).

## FORMAL RESULTS

Tous **FORMAL / ANALYST_SYNTHETIC**, aucune nouvelle mesure de T,Money ou Utility.

| Cycle | Diagnostic exécuté | Résultat et limite |
|---|---|---|
| C03 | Trois raccords multiplicatifs | Produits1 et6/5; fermeture nécessaire sous mesurande commun, non preuve de comparabilité. Condition réversible source fin385, équation386. |
| C04 | Coefficient agrégé proposé K=Σwk | ΔK=composition+coefficients+interaction;3/4=−1/2+3/2−1/4. Stabilité0 possible par compensation. Ce tableau de pondérations n'est pas fourni p559. |
| C07 | Budget contrefactuel, deux périodes | Gain10 épargné puis dépensé : usage final10, pas20; perte revenu−10 peut compenser gain panier10 dans le solde. |
| C08 | Sous-modèle physique Z=0 | Seuil réemploi2/5 et signes−2/0/+2; intensité nulle sans seuil, autre seuil4 hors domaine[0,1]. **Sensibilité Z proposée, non exécutée.** |
| C09 | Taux/durée/dommage par tâche | Ratio taux32, durée1/4, intégrale8;32>16 et8<16. Exemple conditionnel, pas réfutation de p112. |

Scripts et sorties dans agents/reports/ITER001-C03,C04,C07,C08,C09/. Les rejets locaux de double compte ou omission de terme ne sont pas les sept mutations ciblées historiques. Le +78% antérieur n'est pas présenté comme nouvelle expérience.

## MEASUREMENT RESULTS

C01 impose registres transaction/production et gain séparés, dates/stocks/frontières et déflateur; C02 fixe origine, vitesse normalisée et calibration indépendante avant exposant; C03 ajoute un contrôle des raccords; C09 distingue grandeur et horizon du dommage. **Aucun instrument nouveau validé, aucun étalon indépendant obtenu.**

## EMPIRICAL RESULTS

**0nouveau résultat empirique. 0prédiction économique indépendante discriminante établie.** Aucun panel, aucune régression énergie/PIB, aucune collecte de dépenses ou dommages exécutés dans ce lot. Les deux reproductions de verify restent celles de baseline.

## NEGATIVE RESULTS

NOT_IDENTIFIABLE, REQUIRES_INDEPENDENT_T, REQUIRES_EXOGENOUS_VARIATION, AMBIGUOUS, NON_DISCRIMINATING sont conservés dans décisions/candidats. C02 compare un modèle libre incluant le carré : pas nécessairement de prédictions différentes. C05 distingue interventions sans établir primauté d'une théorie. C08 laisse signe global inconnu si Z non borné. C09 ne choisit pas arbitrairement un sens opérationnel du carré p112. Aucun résultat positif forcé.

## LITERATURE FINDINGS

[Romer1990, Endogenous Technological Change](https://web.stanford.edu/~klenow/Romer_1990.pdf), pagesS71–72 : décisions d'investissement technique et réemploi des connaissances, **PARTIAL_PARALLEL** avec transformation productive; aucune équivalence à T/Money ni élasticité énergétique attribuée. [Oslo Manual2018, OECD/Eurostat](https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/10/oslo-manual-2018_g1g9373b/9789264304604-en.pdf), pages70/72 : types produit/processus combinables et adoption, utilisés pour la collecte, pas preuve causale. **NOVELTY_UNRESOLVED** historique.

FULL_TEXT signifie acquisition complète; lecture ciblée des pages indiquées seulement. Recherche d'autres théories d'innovation, destruction créatrice et précédents historiques reste OPEN. Aucun DOI inventé.

## CANDIDATE CONTRIBUTIONS

Apports au programme : contrôles de raccord et de métrologie, décomposition conditionnelle, bilan longitudinal, seuil physique et distinction taux/intégrale, contrat de test. Utilité pratique non évaluée indépendamment. **Aucune contribution de Campergue promue et aucune originalité historique certifiée.** Les quatre contributions qualifiées de baseline restent inchangées.

## CANDIDATE DISCRIMINATING TESTS

0candidat prêt à une validation économique indépendante. C02 propose une voie de contraste de formes si T est mesuré et les prévisions gelées divergent; elle ne sépare pas H1/H2/H3. C09 pourrait recevoir une restriction concurrente après définition de dommage et lecture d'un comparateur primaire; elle n'en fournit pas encore. Les six champs prediction_campergue/prediction_alternative/observable_difference/required_data/identification_strategy/failure_condition sont explicités dans le protocole C01; pour les autres, les comparaisons et conditions sont dans candidats/EXPERIMENT_QUEUE, toutes avec limites non discriminantes.

## ENERGY / GROWTH — current state

Pas de préférence causale nouvelle pour H1,H2,H3. H1contrainte, H2demande issue de l'innovation, H3transformation productive peuvent coexister. Plan local à deux assignations proposé, données et exogénéité absentes. Énergie primaire, finale, utile physique et T restent séparés.

Tout prochain panel devra distinguer LEVEL RELATION,TIME TREND,WITHIN-COUNTRY VARIATION,BETWEEN-COUNTRY VARIATION,TEMPORAL ORDER,EXOGENOUS SHOCK,CAUSAL IDENTIFICATION; comparer monde,pays,périodes,structures. Ce lot n'a pas effectué ces comparaisons. Aucun R² causal.

## INNOVATION / GROWTH — current state

Registre proposé produit, procédé/coût, qualité, substitution, diffusion, entrées/sorties; décisions, mise en usage et résultats séparés. Une hausse d'output/heure ne suffit pas à mesurer Economic Work. L'amont des décisions techniques du comparateur C06 et la description de transformation du corpus ne constituent pas deux explications mutuellement exclusives.

## CAMPERGUE MECHANISM — current state

Transformation → coût/prix/répartition → possibilités de consommation → usages → flux physiques → dommages. Les conditions de mesure à chaque liaison sont mieux spécifiées; **chaîne toujours non identifiée intégralement**. Les assertions fortes du corpus (notamment112/454/460) sont conservées comme assertions; les conclusions de recherche conditionnelles ne les remplacent pas.

## ROOT QUESTION — new evidence only

Aucune nouvelle preuve sur la transition historique subsistance→abondance ni sur ses dommages quantifiés. Le progrès du lot est de rendre explicites les mesures, référents et contrefactuels à établir. **Aucune nouvelle réponse finale à la question racine.** La réponse de baseline reste gelée.

## RAG ET TRAÇABILITÉ

Trois collections interrogeables séparément via [query.py](iteration001/query.py), [instructions](iteration001/RETRIEVAL.md). SOURCE_CORPUS et DERIVED_ANALYSIS réutilisent l'index existant en lecture seule; EXTERNAL_LITERATURE dispose d'un index séparé de six blocs primaires et de résultats scorés. Le wrapper ne reconstruit aucun index baseline. L'ancien index externe vide est conservé, pas silencieusement rempli par des notes.

PAGE/PARAGRAPH/SECTION/CLAIM_WINDOW selon sources; sections PDF non détectées signalées, pas inventées. Aucun benchmark de pertinence externe ni nouvel embedding sémantique. Les sources pages sont la preuve d'attribution; le RAG seulement un moyen de localisation.

## VERIFY

./verify.sh exécuté au début puis après changements structurants **dans des copies isolées**, car il régénère des fichiers. Résultat final **128/128PASS** :109STRUCTURAL,17FORMAL,2EMPIRICAL_REPRODUCTION,0INDEPENDENT_DISCRIMINATING. **961empreintes originales inchangées**, manifeste copie conforme : [résultat](../agents/logs/batch001/final_integrity_summary.json), [log](../agents/logs/batch001/final_verify.log). Aucun rejeu séparé des7mutations historiques revendiqué.

Validateur overlay :10cycles/10tâches initiales/10expériences; provenance et schémas contrôlés en lecture seule. Échec de schéma initial conservé, adaptation aux deux formats de provenance existants sans transformer extraction en attestation de lecture. Le premier --complete a échoué car ce rapport n'existait pas encore; log intermédiaire conservé. Contrôle terminal `--complete` : **PASS**, 10 cycles, 10 tâches initiales, 10 expériences et 961 empreintes; [journal final](../agents/logs/batch001/overlay_validation_final.log). Ces contrôles ne prouvent ni implication sémantique générale ni vérité économique.

## NEXT 10 TASKS

P0, sélection future seulement; **arrêt du premier lot maintenant**.

| ID | Sujet | Sortie attendue | Statut |
|---|---|---|---|
| ITER002-P0-01 | Money : contrat comptable complet | Dictionnaire de colonnes et cas limites non exécutés auparavant | OPEN |
| ITER002-P0-02 | T/cp : candidats d’instruments | Liste admissible/rejetée avec raison, même si aucun instrument trouvé | OPEN |
| ITER002-P0-03 | Utility : ancrages et transformations | Protocole ancres et diagnostic affine/multiplicatif sans présumer comparabilité | OPEN |
| ITER002-P0-04 | K : produits entrants et sortants | Décomposition avec entrées/sorties et bornes explicites | OPEN |
| ITER002-P0-05 | Énergie : variation exogène exploitable | Étude faisabilité causalité; rejet si identification insuffisante | OPEN |
| ITER002-P0-06 | Innovation : données et modèles restreints | Contrastes numériques conditionnels ou NON_DISCRIMINATING motivé | OPEN |
| ITER002-P0-07 | Gains : contrefactuel budgétaire | Plan budget contrefactuel avec horizon et données manquantes | OPEN |
| ITER002-P0-08 | Empreinte : intensités marginales et Z | Sensibilité Z non encore exécutée et seuils robustes par grandeur | OPEN |
| ITER002-P0-09 | Dommages : sens opérationnel de p112 | Interprétations concurrentes et protocole; AMBIGUOUS si source ne tranche pas | OPEN |
| ITER002-P0-10 | Contrat : audit de la chaîne de preuves | Audit sémantique traçable sans score de vérité globale | OPEN |

Mémoire de reprise : [RESEARCH_LEDGER](RESEARCH_LEDGER.md), [LAST_CYCLE](LAST_CYCLE.md), [DECISIONS](DECISIONS.md), [EVIDENCE_GAPS](EVIDENCE_GAPS.md), [COVERAGE_GAPS](COVERAGE_GAPS.md). Aucune modification de baseline, suppression de référence, publication, fusion ou envoi GitHub.
