"""Audit: same package_name across client markets with conflicting verdicts (repackaging-like), feature similarity of conflict pairs."""
import numpy as np, pandas as pd
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
D=np.load(SP+'lamda.npz'); X,y,mk,nm,pkg=D['X'],D['y'],D['mk'],D['nm'],D['pkg']
top=['play.google.com','anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']
m=(nm==1)&np.isin(mk,top)&(pkg!=''); idx=np.where(m)[0]; df=pd.DataFrame(dict(i=idx,mk=mk[idx],pkg=pkg[idx],y=y[idx]))
g=df.groupby('pkg'); multi=g.mk.nunique(); pk=multi[multi>1].index; d2=df[df.pkg.isin(pk)]
print('packages in >=2 markets',len(pk),'rows',len(d2))
cf=d2.groupby('pkg').y.agg(lambda s:s.nunique()>1); print('cross-market packages with conflicting labels:',int(cf.sum()),f'({cf.mean():.1%})')
# direction: benign in play, malware elsewhere
pv=d2.pivot_table(index='pkg',columns='mk',values='y',aggfunc='max')
tp=[c for c in top if c!='play.google.com']
n_play_ben_other_mal=int(((pv['play.google.com']==0)&(pv[tp].max(axis=1)==1)).sum()); n_play_mal_other_ben=int(((pv['play.google.com']==1)&(pv[tp].min(axis=1)==0)).sum())
print('Play benign & other-market malware:',n_play_ben_other_mal,'| Play malware & other-market benign:',n_play_mal_other_ben)
# feature similarity: pairs (benign row, malware row) same pkg different market vs (same-label pairs)
rng=np.random.RandomState(0); conf=[];same=[]
for p,s in d2.groupby('pkg'):
    b=s[s.y==0]; a=s[s.y==1]
    for _,rb in b.head(2).iterrows():
        for _,ra in a.head(2).iterrows():
            if rb.mk!=ra.mk: conf.append((rb.i,ra.i))
    if len(s[s.y==0])>=2:
        r=s[s.y==0].head(2); 
        if r.mk.nunique()==2: same.append(tuple(r.i))
def cos(a,b):
    A=X[a].astype(float);B=X[b].astype(float); return float(A@B/(np.linalg.norm(A)*np.linalg.norm(B)+1e-9))
c=[cos(a,b) for a,b in conf[:3000]]; s_=[cos(a,b) for a,b in same[:3000]]
rand=[cos(*rng.choice(len(y),2)) for _ in range(3000)]
print('pairs benign-vs-malware same pkg:',len(conf),' mean cosine',round(np.mean(c),3),'| benign-benign same pkg:',len(same),round(np.mean(s_),3),'| random pairs',round(np.mean(rand),3))
print('conflict pair counts by (benign market -> malware market):'); 
cnt={}
for a,b in conf: k=(mk[a],mk[b]); cnt[k]=cnt.get(k,0)+1
print(sorted(cnt.items(),key=lambda x:-x[1])[:8])
