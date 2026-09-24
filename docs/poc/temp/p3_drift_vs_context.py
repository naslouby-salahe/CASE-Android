"""P38: does a standard feature-drift score confuse stable client (market) heterogeneity with temporal drift? Benign-only covariate stats, LAMDA+markets."""
import numpy as np, json
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
D=np.load(SP+'lamda.npz'); X,y,year,mk,nm=D['X'],D['y'],D['year'],D['mk'],D['nm']
def jsd(a,b):
    a=np.clip(a,1e-6,1-1e-6);b=np.clip(b,1e-6,1-1e-6);m=(a+b)/2
    kl=lambda p,q:(p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))); return float(np.mean(.5*kl(a,m)+.5*kl(b,m)))
rng=np.random.RandomState(0)
def prof(mask,cap=3000):
    ii=np.where(mask)[0]
    if len(ii)<300: return None
    ii=rng.choice(ii,min(cap,len(ii)),replace=False); return X[ii].mean(0)
out={}
for cls,name in [(0,'benign'),(1,'malware')]:
    base=(nm==1)&(y==cls); res={}
    # temporal drift within Play year->year+1 (and 2-yr), and Anzhi/AppChina
    for m in ['play.google.com','anzhi','appchina']:
        for lag in [1,2]:
            v=[]
            for t in range(2013,2025):
                a=prof(base&(mk==m)&(year==t)); b=prof(base&(mk==m)&(year==t+lag))
                if a is not None and b is not None: v.append(jsd(a,b))
            res[f'temporal_{m}_lag{lag}']=dict(n=len(v),mean=float(np.mean(v)) if v else None,max=float(np.max(v)) if v else None)
    # same-year cross-market
    for t in range(2013,2025):
        pr={m:prof(base&(mk==m)&(year==t)) for m in ['play.google.com','anzhi','appchina','slideme','PlayDrone','1mobile','angeeks']}
        for m1,m2 in [('play.google.com','anzhi'),('play.google.com','appchina'),('anzhi','appchina'),('play.google.com','slideme'),('play.google.com','PlayDrone')]:
            if pr[m1] is not None and pr[m2] is not None: res.setdefault(f'cross_{m1}_vs_{m2}',[]).append((t,jsd(pr[m1],pr[m2])))
    out[name]=res
# alarm calibration: alarm level = 95th pct of Play benign 1-yr temporal drift; fraction of same-year cross-market pairs above level
lv=[]
for t in range(2013,2025):
    a=prof((nm==1)&(y==0)&(mk=='play.google.com')&(year==t)); b=prof((nm==1)&(y==0)&(mk=='play.google.com')&(year==t+1))
    if a is not None and b is not None: lv.append(jsd(a,b))
lvl=float(np.max(lv)); out['alarm_level_max_play_benign_1yr']=lvl; out['play_benign_1yr_series']=lv
cr=[v for k,vs in out['benign'].items() if k.startswith('cross_') for _,v in vs]
out['frac_cross_market_pairs_above_alarm']=float(np.mean([v>lvl for v in cr])); out['n_cross_pairs']=len(cr)
# variance decomposition (benign, features' per-cell means): client vs year share
cells=[];lab=[]
for m in ['play.google.com','anzhi','appchina']:
    for t in range(2016,2019):
        p=prof((nm==1)&(y==0)&(mk==m)&(year==t))
        if p is not None: cells.append(p); lab.append((m,t))
cells=np.array(cells); G=cells.mean(0); ss=((cells-G)**2).sum(0)
mm={m:cells[[l[0]==m for l in lab]].mean(0) for m in set(l[0] for l in lab)}; tm={t:cells[[l[1]==t for l in lab]].mean(0) for t in set(l[1] for l in lab)}
ssm=sum(((mm[l[0]]-G)**2) for l in lab).sum(); sst=sum(((tm[l[1]]-G)**2) for l in lab).sum()
out['eta2_market_2016_2018']=float(ssm/ss.sum()); out['eta2_year_2016_2018']=float(sst/ss.sum()); out['cells']=[list(map(str,l)) for l in lab]
json.dump(out,open('p3_drift_vs_context_results.json','w'),indent=1)
print({k:v for k,v in out.items() if not isinstance(v,dict)})
for cls in ['benign','malware']:
    for k,v in out[cls].items():
        if k.startswith('temporal'): print(cls,k,v)
        else: print(cls,k,'mean',round(float(np.mean([b for _,b in v])),4) if v else None,'n',len(v))
