"""C1: threshold-scope policies under (heterogeneous) calibration-pool contamination. Frozen federated AE scorer.
Usage: python c1_run.py DOMAIN(mobile|nbaiot|scidb) seeds"""
import numpy as np, json, sys, time
from c1_common import *
from sklearn.cluster import KMeans
from sklearn.metrics import roc_auc_score
DOM=sys.argv[1]; SEEDS=[int(s) for s in sys.argv[2].split(',')]
N={'mobile':200,'nbaiot':200,'scidb':60}[DOM]; R=30; ALPHAS=[0.05,0.01]; EBARS=[0.05,0.10,0.20,0.30]
def q(x,p): return float(np.quantile(x,p,method='higher'))
def scenarios(K,prev,rng):
    S=[]
    for e in [0,.02,.05,.10,.20]: S.append(('hom',f'eps{e}',np.full(K,e)))
    if DOM=='mobile':
        for r in [.1,.3]: S.append(('hetnat',f'prev*{r}',np.clip(np.array(prev)*r,0,.4)))
    S.append(('hetlin','lin0-0.3',rng.permutation(np.linspace(0,.3,K)))); return S
def policies(P,eps,alpha,rng):
    K=len(P); out={}
    tl=np.array([q(p,1-alpha) for p in P]); out['LOCAL']=tl; out['GLOBAL']=np.full(K,tl.mean()); out['GLOBAL-MED']=np.full(K,np.median(tl))
    fp=np.array([[np.log10(q(p,.5)+1e-12),np.log10(q(p,.9)+1e-12),np.log10(q(p,.99)+1e-12)] for p in P]); lab=KMeans(2,n_init=5,random_state=0).fit_predict(fp)
    out['CLUSTER']=np.array([tl[lab==lab[c]].mean() for c in range(K)])
    tt=np.array([q(np.sort(p)[:len(p)-int(np.ceil(len(p)*e))] if e>0 else p,1-alpha) for p,e in zip(P,eps)]); out['TRIM-ORACLE']=tt; out['TRIM-ORACLE-GLOBAL']=np.full(K,tt.mean())
    for eb in EBARS:
        tp=np.array([q(p,1-alpha*(1-eb)) for p in P]); out[f'PI-LOCAL@{eb}']=tp; out[f'PI-GLOBAL@{eb}']=np.full(K,tp.mean())
    U=[p/(q(p,.5)+1e-12) for p in P]; eh=np.zeros(K); pt=np.zeros(K)
    for c in range(K):
        ref=np.concatenate([U[j] for j in range(K) if j!=c]); tau=q(ref,.9); tc=np.mean(U[c]>tau); eh[c]=max(0.0,(tc-.1)/.9)
        pool=np.sort(P[c]); pt[c]=q(pool[:len(pool)-int(np.ceil(len(pool)*eh[c]))] if eh[c]>0 else pool,1-alpha)
    out['PEER-TRIM']=pt; out['_epshat']=eh
    e2=np.zeros(K); p2=np.zeros(K)
    for c in range(K):
        ref=np.concatenate([U[j] for j in range(K) if j!=c]); best=0.0
        for pq in [.5,.7,.8,.9,.95]:
            tau=q(ref,pq); tr_=1-pq; tc=np.mean(U[c]>tau); se=np.sqrt(tr_*(1-tr_)/len(U[c])); best=max(best,(tc-tr_-1.0*se)/(1-tr_))
        e2[c]=min(max(best,0.0),.35); pool=np.sort(P[c]); p2[c]=q(pool[:len(pool)-int(np.ceil(len(pool)*e2[c]))] if e2[c]>0 else pool,1-alpha)
    out['PEER-TRIM2']=p2; out['_epshat2']=e2
    e3=np.zeros(K); p3=np.zeros(K)
    for c in range(K):
        others=[U[j] for j in range(K) if j!=c]; best=0.0
        for pq in [.7,.8,.9,.95]:
            tr_=1-pq; tref=np.median([np.mean(u>q(np.concatenate(others),pq)) for u in others]); tc=np.mean(U[c]>q(np.concatenate(others),pq)); se=np.sqrt(tr_*(1-tr_)/len(U[c]))
            best=max(best,(tc-tref-2.0*se)/(1-tref))
        e3[c]=min(max(best,0.0),.35); pool=np.sort(P[c]); p3[c]=q(pool[:len(pool)-int(np.ceil(len(pool)*e3[c]))] if e3[c]>0 else pool,1-alpha)
    out['PEER-TRIM3']=p3; out['_epshat3']=e3
    out['PEER-ADMIT']=np.where(e3>=0.05,np.median(tl),tl)
    sh=np.array([np.log((q(p,.95)+1e-12)/(q(p,.5)+1e-12)) for p in P]); med=np.median(sh); mad=1.4826*np.median(np.abs(sh-med))+1e-6; z=(sh-med)/mad
    for kap in [2.0,3.0]:
        fl=z>kap; keep=tl[~fl] if (~fl).any() else tl
        out[f'GATE-MEDIAN@{kap}']=np.where(fl,np.median(keep),tl); out[f'GATE-MEAN@{kap}']=np.where(fl,keep.mean(),tl)
        out[f'_flags@{kap}']=fl.astype(float)
    return out
def metrics(th,tb,tm,alpha):
    fpr=np.array([np.mean(b>t) for b,t in zip(tb,th)]); tpr=np.array([np.mean(m>t) for m,t in zip(tm,th)])
    return dict(dev=float(np.mean(np.abs(fpr-alpha))),wdev=float(np.max(np.abs(fpr-alpha))),fpr=float(fpr.mean()),wfpr=float(fpr.max()),fsd=float(fpr.std()),tpr=float(tpr.mean()),wtpr=float(tpr.min()),ctrl=float(np.mean(fpr<=alpha+0.01)),ok=float(np.mean(fpr<=alpha)),fpr_c=fpr.tolist(),tpr_c=tpr.tolist())
res=[]
for seed in SEEDS:
    t0=time.time(); C,names,binary,prev=build(DOM,seed); g=train_fed_ae(C,binary,seed); K=len(C); rng=np.random.RandomState(seed)
    sc=[dict(cb=rec_err(g,c['Xcb'],binary),cm=rec_err(g,c['Xcm'],binary),tb=rec_err(g,c['Xtb'],binary),tm=rec_err(g,c['Xtm'],binary)) for c in C]
    auc=[float(roc_auc_score(np.r_[np.zeros(len(s['tb'])),np.ones(len(s['tm']))],np.r_[s['tb'],s['tm']])) for s in sc]
    tb=[s['tb'] for s in sc]; tm=[s['tm'] for s in sc]
    for ctype in ['rand','stealth','top']:
        for pat,lab,eps in scenarios(K,prev,rng):
            for alpha in ALPHAS:
                acc={}
                for r in range(R):
                    P=[]
                    for c in range(K):
                        k=int(round(N*eps[c])); cb=sc[c]['cb']; cm=np.sort(sc[c]['cm']); half=max(len(cm)//2,1)
                        pool=cm[:half] if ctype=='stealth' else (cm[-half:] if ctype=='top' else cm)
                        cl=rng.choice(cb,N-k,replace=len(cb)<N-k); ct=rng.choice(pool,k,replace=len(pool)<k) if k>0 else np.array([])
                        P.append(np.concatenate([cl,ct]))
                    pols=policies(P,eps,alpha,rng)
                    for name,th in pols.items():
                        if name in('_epshat','_epshat2','_epshat3'):
                            acc.setdefault(name,{}).setdefault('abs_err',[]).append(float(np.mean(np.abs(th-eps)))); acc[name].setdefault('bias',[]).append(float(np.mean(th-eps))); continue
                        if name.startswith('_flags'):
                            fl=th; dirty=(eps>=0.1)
                            acc.setdefault(name,{}).setdefault('flag_rate',[]).append(float(fl.mean())); acc[name].setdefault('flag_dirty',[]).append(float(fl[dirty].mean()) if dirty.any() else np.nan); acc[name].setdefault('flag_clean',[]).append(float(fl[~dirty].mean()) if (~dirty).any() else np.nan); continue
                        m=metrics(th,tb,tm,alpha)
                        for kk,v in m.items(): acc.setdefault(name,{}).setdefault(kk,[]).append(v)
                res.append(dict(dom=DOM,seed=seed,ctype=ctype,pattern=pat,label=lab,alpha=alpha,eps=list(map(float,eps)),pol={n:{k:np.nanmean(v,0).tolist() for k,v in d.items()} for n,d in acc.items()}))
    res.append(dict(dom=DOM,seed=seed,kind='scorer',names=names,auc=auc,prev=prev,n_cal_benign=[len(s['cb']) for s in sc],n_test=[(len(s['tb']),len(s['tm'])) for s in sc]))
    print(DOM,'seed',seed,round(time.time()-t0),'s',flush=True)
json.dump(res,open(f'c1_results_{DOM}.json','w'))
