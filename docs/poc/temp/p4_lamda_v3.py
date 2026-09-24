"""LAMDA/AndroZoo market clients (config A: 7 markets; B: 6 markets + 5 Play era cohorts). Usage: python p3_lamda_v2.py CFG NTR seeds"""
import numpy as np, sys, json, hashlib, os, time
from p3_engine import *
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
CFG=sys.argv[1]; NTR=int(sys.argv[2]); SEEDS=[int(s) for s in sys.argv[3].split(',')]
D=np.load(SP+'lamda.npz'); X,y,year,mk,nm,pkg=D['X'],D['y'],D['year'],D['mk'],D['nm'],D['pkg']
CL=np.full(len(y),'',dtype=object)
for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
P=(mk=='play.google.com')&(nm==1)
if CFG=='A': CL[P]='play'
else:
    for a,b in [(2013,2014),(2016,2016),(2017,2017),(2018,2018),(2019,2021)]: CL[P&(year>=a)&(year<=b)]=f'play{a}-{b}'
names=sorted(set(CL)-{''})
def gsplit(p,seed):
    h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32
    return 0 if h<.6 else (1 if h<.75 else 2)
res=[]
for seed in SEEDS:
    t=time.time(); rng=np.random.RandomState(seed)
    grp=np.array([gsplit(p if p else str(i),seed) for i,p in enumerate(pkg)])
    C=[]
    for nv in names:
        idx=np.where(CL==nv)[0]; parts=[]
        for s,cap in [(0,NTR),(1,max(60,min(1500,NTR//3))),(2,4000)]:
            ii=idx[grp[idx]==s]
            if len(ii)>cap: ii=rng.choice(ii,cap,replace=False)
            parts.append(ii)
        C.append(dict(Xtr=X[parts[0]].astype(np.float32),ytr=y[parts[0]],Xva=X[parts[1]].astype(np.float32),yva=y[parts[1]],Xte=X[parts[2]].astype(np.float32),yte=y[parts[2]]))
    E,logit,T,lab=run_arms(C,seed); out=evaluate(C,logit); pol,choice=policies(C,logit); out.update(pol)
    H=hetero_stats(C,T); H.update(extra_stats(C,logit))
    res.append(dict(seed=seed,names=names,T=T.tolist(),cluster=lab.tolist(),choice=choice,H=H,res=out)); print('seed',seed,round(time.time()-t),'s',flush=True)
json.dump(res,open(f'p4_lamda_v3_{CFG}_n{NTR}.json','w'))
def summ(res,arms):
    for a in arms:
        M=lambda k:np.mean([[r[k] for r in s['res'][a]] for s in res]); W=np.mean([min(r['ba'] for r in s['res'][a]) for s in res])
        WF=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res]); SD=np.mean([np.std([r['fpr'] for r in s['res'][a]]) for s in res])
        print(f'{a:26s} BA {M("ba"):.3f} worstBA {W:.3f} F1 {M("f1"):.3f} FPR {M("fpr"):.3f} FPRsd {SD:.3f} worstFPR {WF:.3f} FNR {M("fnr"):.3f}')
summ(res,sorted(res[0]['res']))
