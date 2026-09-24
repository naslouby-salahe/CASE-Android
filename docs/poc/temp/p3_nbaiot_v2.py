"""N-BaIoT device clients (9 devices, natural prevalence) with the same collaboration-scope engine. Usage: python p3_nbaiot_v2.py NTR seeds"""
import numpy as np, pandas as pd, glob, os, sys, json, time
from p3_engine import *
R='/home/naslouby/Projects/datp-shared-data/raw/N-BaIoT/'
NTR=int(sys.argv[1]); SEEDS=[int(s) for s in sys.argv[2].split(',')]
devs=sorted(d for d in os.listdir(R) if os.path.isdir(R+d))
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
cache=SP+'nbaiot.npz'
if not os.path.exists(cache):
    D={}
    for d in devs:
        rng=np.random.RandomState(0); B=pd.read_csv(R+d+'/benign_traffic.csv').values.astype(np.float32); A=[]
        for f in glob.glob(R+d+'/*_attacks/*.csv'):
            a=pd.read_csv(f).values.astype(np.float32); A.append(a[rng.choice(len(a),min(len(a),4000),replace=False)])
        A=np.concatenate(A); nb=len(B); na=sum(len(pd.read_csv(f,usecols=[0])) for f in glob.glob(R+d+'/*_attacks/*.csv'))
        B=B[rng.choice(len(B),min(len(B),20000),replace=False)]; A=A[rng.choice(len(A),min(len(A),40000),replace=False)]
        D[d+'_X']=np.concatenate([B,A]); D[d+'_y']=np.r_[np.zeros(len(B)),np.ones(len(A))].astype(np.int8); D[d+'_prev']=na/(na+nb)
        print(d,nb,na,round(na/(na+nb),3),flush=True)
    np.savez_compressed(cache,**D)
D=np.load(cache); res=[]
for seed in SEEDS:
    t=time.time(); rng=np.random.RandomState(seed); C=[]
    allX=np.concatenate([D[d+'_X'] for d in devs]); mu=np.log1p(np.abs(allX)).mean(0); sd=np.log1p(np.abs(allX)).std(0)+1e-6
    for d in devs:
        X=D[d+'_X'];y=D[d+'_y']; X=(np.sign(X)*np.log1p(np.abs(X))-0)/1.0; X=(X-mu)/sd
        prev=float(D[d+'_prev']); n1=int(round(6000*prev)); n0=6000-n1
        i0=rng.permutation(np.where(y==0)[0])[:n0]; i1=rng.permutation(np.where(y==1)[0])[:n1]
        ii=rng.permutation(np.r_[i0,i1]); n=len(ii); a,b=int(.6*n),int(.75*n)
        tr=ii[:a][:NTR]; va=ii[a:b][:max(60,min(1500,NTR//3))]; te=ii[b:]
        C.append(dict(Xtr=X[tr].astype(np.float32),ytr=y[tr],Xva=X[va].astype(np.float32),yva=y[va],Xte=X[te].astype(np.float32),yte=y[te]))
    E,logit,T,lab=run_arms(C,seed); out=evaluate(C,logit); pol,choice=policies(C,logit); out.update(pol)
    res.append(dict(seed=seed,names=devs,T=T.tolist(),cluster=lab.tolist(),choice=choice,H=hetero_stats(C,T),res=out)); print('seed',seed,round(time.time()-t),flush=True)
json.dump(res,open(f'p3_nbaiot_v2_n{NTR}.json','w'))
for a in sorted(res[0]['res']):
    M=lambda k:np.mean([[r[k] for r in s['res'][a]] for s in res]); W=np.mean([min(r['ba'] for r in s['res'][a]) for s in res]); WF=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res])
    print(f'{a:26s} BA {M("ba"):.3f} worstBA {W:.3f} FPR {M("fpr"):.3f} worstFPR {WF:.3f} FNR {M("fnr"):.3f}')
