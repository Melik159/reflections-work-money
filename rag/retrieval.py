"""Three deterministic lexical baselines, with no external dependencies."""
import math
import re
from collections import Counter

def tokenize(text):
    return re.findall(r'\w+', text.lower())

class Retriever:
    def __init__(self, rows):
        self.rows=rows
        self.counts=[Counter(tokenize(r['text'])) for r in rows]
        self.df=Counter()
        for counts in self.counts:
            self.df.update(counts.keys())
        self.n=len(rows)
        self.lengths=[sum(c.values()) for c in self.counts]
        self.avg=sum(self.lengths)/self.n if self.n else 1
        self.idf={t:math.log((self.n+1)/(df+1))+1 for t,df in self.df.items()}
        self.norms=[math.sqrt(sum(((1+math.log(v))*self.idf[t])**2 for t,v in c.items())) for c in self.counts]

    def search(self, query, method='bm25', k=5):
        if method not in ['legacy','tfidf','bm25']:
            raise ValueError(method)
        terms=Counter(tokenize(query))
        if method=='legacy':
            idfs={t:math.log((self.n+1)/(1+sum(t in r['text'].lower() for r in self.rows))) for t in terms}
        else:
            idfs=self.idf
        qnorm=math.sqrt(sum(((1+math.log(v))*idfs[t])**2 for t,v in terms.items() if t in idfs)) if method=='tfidf' else 1
        result=[]
        for i,counts in enumerate(self.counts):
            score=0
            for t,qt in terms.items():
                tf=counts.get(t,0)
                if not tf:
                    continue
                if method=='legacy':
                    score+=qt*tf*idfs[t]
                elif method=='tfidf':
                    score+=(1+math.log(tf))*(1+math.log(qt))*idfs[t]**2
                else:
                    idf=math.log(1+(self.n-self.df[t]+.5)/(self.df[t]+.5))
                    score+=qt*idf*(tf*2.2)/(tf+1.2*(.25+.75*self.lengths[i]/self.avg))
            if method=='tfidf':
                score=score/(self.norms[i]*qnorm) if self.norms[i] and qnorm else 0
            if score>0:
                result.append((score,i))
        result.sort(key=lambda pair:(-pair[0],pair[1]))
        return [dict(self.rows[i],score=score) for score,i in result[:k]]
