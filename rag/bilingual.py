"""Small auditable vocabulary expansion, without page IDs or expected answers."""
import re
import unicodedata
WORDS={
 'quelle':'','quel':'','quelles':'','quels':'','comment':'','pourquoi':'why','entre':'between',
 'difference':'difference distinguish','distinguer':'distinguish','question':'question','initiale':'key initial',
 'relie':'links','niveau':'standards','vie':'living','abondance':'affluent abundance',
 'dommages':'damages','environnementaux':'environmental','environnement':'environment',
 'productivite':'productivity','cree':'creates creation','creer':'create','creation':'creation',
 'pouvoir':'power','achat':'purchasing consumer','critere':'criterion definition',
 'distingue':'distinguish','travail':'work labour','productif':'productive','improductif':'unproductive',
 'place':'role','auteur':'author','accorde':'use','entropie':'entropy','monnaie':'money cash',
 'energie':'energy','prix':'price','cout':'cost','richesse':'wealth','tache':'task labour',
 'vitesse':'speed','unite':'unit','monetaire':'monetary','billet':'banknote','consommateur':'consumer',
 'fournisseur':'supplier','production':'production','distribution':'distribution',
 'rendement':'yield efficiency','contraintes':'constraints','conservation':'conservation',
 'reel':'real','reelle':'real','physique':'physical','economique':'economic','mesure':'measure',
}
STOP={'le','la','les','un','une','des','du','de','d','l','a','au','aux','et','en','il','elle','t','se','ce','est'}
def normalized(query):
    return ''.join(c for c in unicodedata.normalize('NFKD',query.lower()) if not unicodedata.combining(c))
def expand(query):
    words=re.findall(r'\w+',normalized(query))
    if not any(w in WORDS and WORDS[w]!=w for w in words):return query
    return ' '.join(WORDS.get(w,w) for w in words if w not in STOP)
