"""One-shot targeted bibliography and numerical report. Preserve earlier reviews."""
import json
import shutil
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):(ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    if (ROOT/'bibliography/energy_aggregation_library.json').exists():raise SystemExit('Already finalized; append a documented revision instead.')
    refs=[
        dict(id='BIB-0011',authors='World Bank',title='GDP per unit of energy use (constant 2021 PPP $ per kg of oil equivalent): metadata',year=2026,doi=None,url='https://databank.worldbank.org/metadataglossary/world-development-indicators/series/EG.GDP.PUSE.KO.PP.KD',status='VERIFIED',access='Full official metadata read and HTML archived; historical vintage consistency not verified',locator='Long definition; methodology; limitations'),
        dict(id='BIB-0012',authors='Our World in Data',title='Energy dataset, pinned 2025 release',year=2025,doi=None,url='https://github.com/owid/energy-data/tree/4249f7c21c2c833d76741e757be92a639517caa3',status='VERIFIED',access='CSV, codebook, README archived; upstream processing inspected at pinned ETL revision',locator='primary_energy_consumption; README Data sources and processing'),
        dict(id='BIB-0013',authors='David I. Stern',title='The role of energy in economic growth',year=2011,doi='10.1111/j.1749-6632.2010.05921.x',url='https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/4535717f-80cb-429d-88d6-f7bc90c5f946/content',status='VERIFIED',access='Author institutional full PDF accessible; abstract and opening sections inspected, not exhaustive reading',locator='Annals of the New York Academy of Sciences 1219, 26–51; abstract and pp26–28'),
        dict(id='BIB-0014',authors='Steve Sorrell',title='The Rebound Effect: An Assessment of the Evidence for Economy-wide Energy Savings from Improved Energy Efficiency',year=2007,doi=None,url='https://ukerc.rl.ac.uk/publications/research_report/The_Rebound_Effect_An_Assessment_of_the_Evidence_for_Economy-wide_Energy_Savings_from_Improved_Energy_Efficiency.pdf',status='VERIFIED',access='UKERC metadata and report PDF inspected; sections1.1, boxes1.1–1.2, not entire report',locator='PDF15–18 / printed1–4; no DOI minted according to official catalog'),
        dict(id='BIB-0015',authors='David Baqaee and Emmanuel Farhi',title='The Microeconomic Foundations of Aggregate Production Functions',year=2018,doi='10.3386/w25293',url='https://www.nber.org/papers/w25293',status='PARTIALLY_VERIFIED',access='Official indexed title, authors, DOI and abstract verified; direct page/PDF fetch failed403; no detailed theorem attributed',locator='NBER working paper25293 indexed abstract only'),
        dict(id='BIB-0016',authors='Samuel J. Ling and William Moebs and Jeff Sanny',title='University Physics Volume 2, section 4.6 Entropy',year=2016,doi=None,url='https://openstax.org/books/university-physics-volume-2/pages/4-6-entropy',status='VERIFIED',access='Official section and metadata inspected',locator='State function and Example4.5: reversible path for irreversible cooling')]
    save('bibliography/energy_aggregation_library.json',refs)
    lib=load('bibliography/initial_research_library.json');lib+=refs;save('bibliography/initial_research_library.json',lib)
    lit=load('analysis/data/literature_map.json');lit['sources']+=refs
    relations=[('BIB-0011','CPC-0118','DOES_NOT_TEST','Data provenance only; ratio can recover a physical energy input, not identify causality.'),
               ('BIB-0012','CPC-0118','DOES_NOT_TEST','Dataset for E1–E3; primary energy is not independently measured Campergue Money or Work.'),
               ('BIB-0013','CPC-0018','SUPPORTS','Broad enabling role of fossil energy; not exclusive explanation of living standards.'),
               ('BIB-0013','CPC-0118','QUALIFIES','Energy/output linkage can vary with technology, composition and substitution; no constant Money/joule equivalence established.'),
               ('BIB-0013','CPC-0119','DOES_NOT_TEST','No independent measurement of Tused=−Wcreated in Campergue units.'),
               ('BIB-0014','CPC-0127','PARALLELS','Partial parallel: use of cost savings can increase demand elsewhere; not automatic backfire or exact same definition of productivity.'),
               ('BIB-0014','CPC-0120','QUALIFIES','Rebound need not erase all efficiency savings; horizon and counterfactual matter.'),
               ('BIB-0015','CPC-0117','QUALIFIES','Methodological parallel only: aggregation depends on micro structure; no detailed theorem used from inaccessible PDF.'),
               ('BIB-0016','CPC-0067','QUALIFIES','Entropy equation requires reversible-path or entropy-production accounting for actual irreversibility.')]
    for b,c,rel,scope in relations:lit['relations'].append(dict(source_id=b,claim_id=c,relation=rel,scope=scope,assessment_status='TARGETED_TERMINAL_REVIEW',interpretive=True))
    save('analysis/data/literature_map.json',lit)
    (ROOT/'bibliography/energy_aggregation_library.bib').write_text('\n'.join('@misc{'+r['id']+',\n  author = {'+r['authors']+'},\n  title = {'+r['title']+'},\n  year = {'+str(r['year'])+'},\n  url = {'+r['url']+'}'+(',\n  doi = {'+r['doi']+'}' if r['doi'] else '')+'\n}\n' for r in refs))
    result=load('analysis/empirical/independent_energy/results.json')
    lines=['# Résultats indépendants PIB–énergie','',
           'Source et protocole : rapport27. Fenêtre1990–2023 ; régression PIB sur énergie, pas sens causal. IC95% HAC(3) asymptotiques. Tests exécutés ; aucune interpolation. Les niveaux sont en milliards USD constants2015 par TWh.','',
           '| Expérience / modèle | Zone | N | Période | Coefficient énergie | IC95% | R² |','|---|---|---:|---|---:|---|---:|']
    for r in result['results']:
        if r['experiment']=='TEST-E3':continue
        lo,hi=r['ci95'][1]
        lines.append(f"| {r['experiment']} / {r['model']} | {r['country']} | {r['N']} | {r['start']}–{r['end']} | {r['coefficients'][1]:.4f} | [{lo:.4f}, {hi:.4f}] | {r['R2']:.4f} |")
    lines+=['','## E3 — Stabilité descriptive','',
            'Découpage fixé à2007 avant estimation, deux sous-échantillons de17 observations chacun. Modèle joint avec intercept et pente propres à chaque période. IC de la différence : HAC(3) du coefficient interaction. Pas de correction pour comparaisons multiples ; résultats exploratoires.','',
            '| Zone | β1990–2006 | β2007–2023 | Δβ | IC95% Δβ |','|---|---:|---:|---:|---|']
    for r in result['results']:
        if r['experiment']!='TEST-E3':continue
        lo,hi=r['ci95'][3]
        lines.append(f"| {r['country']} | {r['periods'][0]['coefficients'][1]:.4f} | {r['periods'][1]['coefficients'][1]:.4f} | {r['coefficients'][3]:.4f} | [{lo:.4f}, {hi:.4f}] |")
    panel=pd.read_csv(ROOT/'analysis/empirical/independent_energy/analysis_panel.csv')
    ratios=[]
    for code,d in panel.groupby('Country Code'):
        k=d.gdp_real/d.primary_energy_consumption
        ratios.append(dict(country=code,experiment='TEST-E3',quantity='observed GDP_real / primary_energy_TWh',
                           ratio_2023_over_1990=float(k.iloc[-1]/k.iloc[0]),coefficient_of_variation=float(k.std(ddof=1)/k.mean()),
                           energy_2023_over_1990=float(d.primary_energy_consumption.iloc[-1]/d.primary_energy_consumption.iloc[0]),
                           gdp_2023_over_1990=float(d.gdp_real.iloc[-1]/d.gdp_real.iloc[0]),
                           status='DESCRIPTIVE_PROXY_CONSTANT_K_NOT_MAINTAINED',causal_identified=False))
    save('analysis/empirical/independent_energy/stability_ratios.json',ratios)
    lines+=['','### Restriction GDP=K·W à K constant','',
            'Diagnostic supplémentaire **du même E3**, sans quatrième expérience : le ratio observé devrait être stable si cette opérationnalisation forte était exacte. Sa variation n’est pas une mesure directe de K économique ; elle documente le coût empirique de cette identification.','',
            '| Zone | PIB2023/1990 | Énergie2023/1990 | (PIB/E)2023/1990 | CV(PIB/E) |','|---|---:|---:|---:|---:|']
    for r in ratios:lines.append(f"| {r['country']} | {r['gdp_2023_over_1990']:.3f} | {r['energy_2023_over_1990']:.3f} | {r['ratio_2023_over_1990']:.3f} | {r['coefficient_of_variation']:.3f} |")
    lines+=['','## Interprétation','',
            'Monde : forte association positive en niveaux et co-mouvement annuel. France/Allemagne : tendances de niveau opposées, mais co-mouvements annuels positifs. La France change de signe entre sous-périodes. La pente française globale est fragile (IC proche de zéro), pas une estimation robuste d’un effet négatif de l’énergie. Les tendances incluent chocs, mutations sectorielles et échanges internationaux.','',
            'Les associations sont non spécifiques. La version strictement constante de GDP=K·W, avec nos proxies, ne décrit pas ces trajectoires ; cela distingue une restriction particulière d’une explication standard autorisant découplage et coefficients variables. Ce n’est pas une confirmation positive du formalisme Campergue et ne rejette pas toutes ses branches. E1/E2 : ASSOCIATION ou TEMPORAL_CO_MOVEMENT ; E3 : ASSOCIATION/stabilité ; causalité et prévision hors échantillon NOT_IDENTIFIABLE / NOT_TESTED.']
    (ROOT/'analysis/27_energy_results.md').write_text('\n'.join(lines)+'\n')
    rules=load('analysis/data/terminal_regression_rules.json')
    rules['aggregation_conditions']={a['id']:a['conditions'] for a in load('analysis/data/aggregation_mechanisms.json')}
    save('analysis/data/terminal_regression_rules.json',rules)
    summary=dict(old_claims=113,new_claims=127,examined_pages=247,chapters_reviewed=['CH-08','CH-09','CH-10'],
                 new_experiments=['TEST-E1','TEST-E2','TEST-E3'],literature_added=6,literature_verified=5,literature_partially_verified=1,
                 relation_counts={k:sum(r[2]==k for r in relations) for k in ['SUPPORTS','QUALIFIES','PARALLELS','CONTRADICTS','DOES_NOT_TEST']},
                 status='ITERATIVE_REVIEW_QUALIFIED',global_theory_verdict=None)
    save('analysis/data/terminal_review_summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
