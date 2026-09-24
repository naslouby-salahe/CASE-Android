"""Client builders reused by Phase-4 scripts (same construction as p3_lamda_v2.py / p4_iot_v1.py)."""
import numpy as np, pandas as pd, hashlib
SPD='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
_L=None; _I=None
def mobile(cfg,NTR,seed):
    global _L
    if _L is None:
        D=np.load(SPD+'lamda.npz'); _L=(D['X'],D['y'],D['year'],D['mk'],D['nm'],D['pkg'])
    X,y,year,mk,nm,pkg=_L; CL=np.full(len(y),'',dtype=object)
    for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
    P=(mk=='play.google.com')&(nm==1)
    if cfg=='A': CL[P]='play'
    else:
        for a,b in [(2013,2014),(2016,2016),(2017,2017),(2018,2018),(2019,2021)]: CL[P&(year>=a)&(year<=b)]=f'play{a}-{b}'
    names=sorted(set(CL)-{''})
    def gs(p,sd):
        h=int(hashlib.md5((p+str(sd)).encode()).hexdigest()[:8],16)/2**32; return 0 if h<.6 else (1 if h<.75 else 2)
    rng=np.random.RandomState(seed); grp=np.array([gs(p if p else str(i),seed) for i,p in enumerate(pkg)]); C=[]
    for nv in names:
        idx=np.where(CL==nv)[0]; parts=[]
        for s,cap in [(0,NTR),(1,max(60,min(1500,NTR//3))),(2,4000)]:
            ii=idx[grp[idx]==s]
            if len(ii)>cap: ii=rng.choice(ii,cap,replace=False)
            parts.append(ii)
        C.append(dict(Xtr=X[parts[0]].astype(np.float32),ytr=y[parts[0]],Xva=X[parts[1]].astype(np.float32),yva=y[parts[1]],Xte=X[parts[2]].astype(np.float32),yte=y[parts[2]]))
    return C,names
def iot(NTR,seed,std=True):
    global _I
    if _I is None:
        dev=[pd.read_csv(SPD+f'iot/dev{i}.csv') for i in range(8)]; F=[c for c in dev[0].columns if c!='label']; U=[]
        for d in dev:
            d=d.copy(); d['k']=d[F].round(10).apply(tuple,axis=1); U.append(d.drop_duplicates('k').drop(columns='k').reset_index(drop=True))
        _I=(U,F)
    U,F=_I; rng=np.random.RandomState(seed); C=[]; tr_all=[]
    for d in U:
        X=d[F].values.astype(np.float32); y=(d.label.values>0).astype(np.int8); ii=rng.permutation(len(d)); n=len(ii); a,b=int(.6*n),int(.75*n)
        tr=ii[:a][:NTR]; va=ii[a:b][:max(60,min(1500,NTR//3))]; te=ii[b:]
        C.append(dict(Xtr=X[tr],ytr=y[tr],Xva=X[va],yva=y[va],Xte=X[te],yte=y[te])); tr_all.append(X[tr])
    if std:
        A=np.concatenate(tr_all); mu,sd=A.mean(0),A.std(0)+1e-6
        for c in C:
            for k in ['Xtr','Xva','Xte']: c[k]=((c[k]-mu)/sd).astype(np.float32)
    return C,[f'dev{i}' for i in range(8)]
