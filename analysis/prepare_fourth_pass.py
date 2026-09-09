"""Freeze prospective extensions; no experimental arithmetic in this script."""
import csv,hashlib,io,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_questions/experiments'
SPECS={
'EXP-02':dict(questions=['RQ-05.03'],claims=['CPC-0055','CPC-0056','CPC-0057','CPC-0076','CPC-0077','CPC-0078','CPC-0079','CPC-0113'],variables=['VAR-06','VAR-26'],pages=[108,109,283,291,347,349,385,386,415],
 prediction='Les classements de Utility et les formules utilisant niveaux, différences et rapports doivent être distingués. Les relations sources sont données; leur invariance est une question de l’analyste, non une citation de Campergue.',
 alternative='Un ordre seul suffit aux signes et égalités, tandis qu’une échelle d’intervalle ou de rapport peut être nécessaire aux résultats numériques.',
 method='Tester identité, U→3U, U→3U+5 et U→U² sur valeurs positives [1,2,4]. Comparer ordre, égalité, différences, ratios, 1−U2/U1; puis covariance des coefficients dans FA p=rU et M=r ΔU/(1−γ). Coefficients figés sauf test explicitement covariant.',
 success='Une propriété déclarée ordinale doit être invariante sous les transformations croissantes testées et sa justification doit couvrir toute transformation strictement croissante commune.',
 qualification='Un résultat numérique dépend de l’échelle; déclarer le groupe de transformations autorisé et la transformation des coefficients.',
 contradiction='Contre-exemple à une suffisance ordinale supposée; ne pas attribuer au manuscrit l’affirmation non sourcée que toutes ses formules sont ordinales.',
 nonident='Échelle cardinale/rapport non calibrée; aucune mesure de Utility ou Money.',
 limitations='Tests synthétiques et preuve d’invariance locale; une transformation commune suppose même agent, usage et contexte. Ne pas sommer Utility.',
 delta='Extension du diagnostic antérieur: différences, ratios, origine et covariance des coefficients, pas répétition du seul exemple U².'),
'EXP-03':dict(questions=['RQ-08.02'],claims=['CPC-0044','CPC-0109','CPC-0117','CPC-0118'],variables=['VAR-01','VAR-07','VAR-11'],pages=[202,559],
 prediction='PDF559 suppose que davantage de Products stabilisent K. Tester précisément quelles restrictions de composition rendent possible la stabilité; ne pas postuler stabilité ou variation universelle.',
 alternative='K agrégé est une moyenne pondérée de Ki seulement si M et T additifs et unités/frontières compatibles. Ki identiques peuvent rendre K indépendant des proportions; Ki différents permettent aussi compensations particulières.',
 method='Calcul rationnel exact. Trois produits Ki=[1,2,3], Ti=[1,2,1]; toutes quantités qi dans {1,2,3}. Comparer deux et trois produits, coefficients identiques, réplication par7, changement de poids, composition [1,1,1]→[2,1,2]. Tester normalisation Ti’=siTi et Ki’=Ki/si, si=[2,3,5], avec retour à l’unité commune avant agrégation; tester changement commun d’unité.',
 success='Invariance sous réplication commune; invariance à toute composition positive si tous Ki égaux; condition nécessaire/suffisante pour deux compositions: somme (wi’−wi)Ki=0, sous Ki fixes et poids normalisés.',
 qualification='Composition variable peut préserver K par compensation; nombre de produits seul ne garantit pas convergence sans hypothèses de distribution/pondérations.',
 contradiction='Exemple qui contredit l’affirmation inconditionnelle de stabilité par simple multiplication du nombre de produits; conclusion limitée à cette généralisation, pas aux couplages conditionnels.',
 nonident='Ti et Mi synthétiques ne sont pas des mesures économiques; ni loi empirique ni calibration de K.',
 limitations='Ti>0 et dénominateur non nul dans le test. Signes mixtes excluent la lecture convexe. Utility non additive jamais agrégée.',
 delta='Extension: condition analytique de stabilité, compensation avec recomposition, énumération, coefficients identiques et normalisation covariante.'),
'EXP-09':dict(questions=['RQ-03.02','RQ-03.03'],claims=['CPC-0040','CPC-0052','CPC-0054','CPC-0066','CPC-0068','CPC-0121'],variables=['VAR-01','VAR-02','VAR-03','VAR-04'],pages=[197,203,207,471,472],
 prediction='PDF207 donne une primitive quadratique; PDF471 écrit T comme différence entre deux instants; PDF472 compense cinétique et réserve potentielle. Comparer ces usages sans imposer un sens unique à toutes les occurrences.',
 alternative='MODEL-A état E=½cpω²; MODEL-B réserve potentielle R, dR=−dE dans un bilan isolé; MODEL-C transfert sur intervalle T[a,b]=E(b)−E(a), suggéré PDF471. Réserve accumulée monotone distincte et non présumée par MODEL-B.',
 method='cp=2; trajectoire ω=[1,3,2,1], réserve initiale100. Tester différences signées, retour au point initial, télescopage, cumul positif non signé. Comparer cp variable, ω=2 constante et cp=1→3: différentielle totale vs intégrale cpωdω. Unit change l’=s l impose cp’=cp/s² pour T invariant.',
 success='Chaque lecture doit conserver les relations et conventions de signe dans son domaine; pas de sélection du modèle qui semble le plus favorable.',
 qualification='Un même symbole recouvre état, réserve et transfert; indices explicites proposés uniquement comme MINIMAL_RECONSTRUCTION.',
 contradiction='Interpréter la même quantité simultanément comme primitive absolue et transfert fini sans référence produit des égalités incompatibles. Modèle réserve identifiée directement à E incompatible avec conservation sauf variation nulle.',
 nonident='Calcul de T depuis la relation quadratique ne constitue jamais test indépendant de cette relation: REQUIRES_INDEPENDENT_T.',
 limitations='Unités économiques non calibrées; cp variable n’est pas présenté comme domaine effectivement annoncé pour toutes les intégrations. Aucun test empirique.',
 delta='Nouveau ID: sous-problème formel promu DO_NOW. EXP-01 demeure NEEDS_DEFINITION; il n’est pas renommé ni déclaré exécuté.')}
def main():
    if (OUT/'fourth_pass_protocol_manifest.json').exists():raise SystemExit('Protocols already frozen; amend explicitly, do not overwrite.')
    OUT.mkdir(parents=True,exist_ok=True)
    vars={v['id']:v for v in json.loads((ROOT/'research_questions/operationalization/variables.json').read_text())}
    proposals=json.loads((ROOT/'research_questions/operationalization/experiments.json').read_text())
    lines=['# Sélection de quatrième passe','', 'Cadrage: claims, relations, constructions et modèles locaux. Aucun verdict global. Les cas synthétiques L1/L2 ne sont pas présentés comme données empiriques. Leur sélection exceptionnelle répond aux tests formels explicitement demandés.','', '| EXP | Questions | Claims | Variables / niveaux | Données disponibles | Pouvoir | Coût | État / décision |','|---|---|---|---|---|---|---|---|']
    for e in proposals:
        lines.append('| '+' | '.join([e['id'],e['question'],', '.join(e['claims']),', '.join(f"{v['name']} L{v['measurement_level']}" for v in e['variables']),e['data'],e['discriminating_power'],e['cost_complexity'],e['feasibility']+('; extension retenue' if e['id'] in SPECS else '; non retenue')])+' |')
    lines+=['| EXP-09 | RQ-03.02, RQ-03.03 | CPC-0040,0052,0054,0066,0068,0121 | T,dT,cp L1; ω L3 | passages et calcul formel | local, pas empirique | faible | nouveau sous-problème DO_NOW |','', 'Sélection: EXP-02, EXP-03, EXP-09. EXP-04 a déjà son diagnostic de dérivée; rien à répéter. EXP-05/06/07 manquent de données appariées. EXP-08 est possible mais de faible spécificité: NO_NEW_ENERGY_TEST. Aucun nouveau test coût/prix; les données précédentes ne permettent pas marge complète ni qualité/Utility appariée. Les sorties de verify.sh sur ces anciens jeux sont des contrôles de reproduction, pas des expériences nouvelles.','']
    (OUT/'selection.md').write_text('\n'.join(lines))
    hashes={}
    for eid,s in SPECS.items():
        d=OUT/eid;d.mkdir(exist_ok=True)
        fields={'QUESTION':', '.join(s['questions']),'CLAIMS':', '.join(s['claims']),'CAMPERGUE_PREDICTION':s['prediction'],'ALTERNATIVE_PREDICTION':s['alternative'],'VARIABLES':', '.join(vars[v]['name'] for v in s['variables']),'MEASUREMENT_LEVELS':', '.join(v+':L'+str(vars[v]['measurement_level']) for v in s['variables']),'DATA':'Sources PDF '+str(s['pages'])+'; paramètres synthétiques déclarés ci-dessous. Aucun nouveau jeu empirique.','PREPROCESSING':'Aucun filtrage de données empiriques. Unités/référents déclarés; valeurs synthétiques non estimées.','MODEL / FORMAL_TEST':s['method'],'SUCCESS_CRITERION':s['success'],'QUALIFICATION_CRITERION':s['qualification'],'CONTRADICTION_CRITERION':s['contradiction'],'NON_IDENTIFICATION_CRITERION':s['nonident'],'LIMITATIONS':s['limitations'],'NOVELTY_AND_HISTORY':s['delta']}
        text='# '+eid+' — Protocole figé\n\n'+''.join('## '+k+'\n\n'+v+'\n\n' for k,v in fields.items())
        p=d/'protocol.md';assert not p.exists();p.write_text(text);hashes[eid]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'fourth_pass_protocol_manifest.json').write_text(json.dumps(dict(frozen_at=datetime.now(timezone.utc).isoformat(),protocol_sha256=hashes,selected=list(SPECS),prior_results_known=True,prior_knowledge='Third-pass diagnostics explicitly known; only new extensions frozen prospectively.',amendments=[]),indent=2)+'\n')
    print('FROZEN:',', '.join(SPECS),'; no experimental calculation executed')
if __name__=='__main__':main()
