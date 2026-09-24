"""P54: is the local-threshold gain explained by label-prior shift alone? Compare thr=.5, prior-corrected logit (known train prevalence), local val-tuned thr."""
import numpy as np, sys, json, hashlib
sys.argv=['x','A','1000','0']  # reuse builder pieces
from p3_engine import *
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
D=np.load(SP+'lamda.npz'); X,y,year,mk,nm,pkg=D['X'],D['y'],D['year'],D['mk'],D['nm'],D['pkg']
CL=np.full(len(y),'',dtype=object)
for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
CL[(mk=='play.google.com')&(nm==1)]='play'; names=sorted(set(CL)-{''})
def gsplit(p,seed):
    h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32
    return 0 if h<.6 else (1 if h<.75 else 2)
out=[]
for NTR in [300,1000,5000]:
  for seed in range(5):
    rng=np.random.RandomState(seed); grp=np.array([gsplit(p if p else str(i),seed) for i,p in enumerate(pkg)]); C=[]
    for nv in names:
        idx=np.where(CL==nv)[0]; parts=[]
        for s,cap in [(0,NTR),(1,max(60,min(1500,NTR//3))),(2,4000)]:
            ii=idx[grp[idx]==s]
            if len(ii)>cap: ii=rng.choice(ii,cap,replace=False)
            parts.append(ii)
        C.append(dict(Xtr=X[parts[0]].astype(np.float32),ytr=y[parts[0]],Xva=X[parts[1]].astype(np.float32),yva=y[parts[1]],Xte=X[parts[2]].astype(np.float32),yte=y[parts[2]]))
    E,logit,T,lab=run_arms(C,seed); K=len(C)
    pool=np.concatenate([c['ytr'] for c in C]).mean(); lo=lambda p:np.log(p/(1-p))
    for arm in ['fedavg','fedavg_ft','central']:
        r={'fixed':[],'prior':[],'local':[]}
        for c in range(K):
            zt=logit[arm][c][1]; zv=logit[arm][c][0]; yt=C[c]['yte']; yv=C[c]['yva']; pc=C[c]['ytr'].mean()
            r['fixed'].append(bal(yt,E_sig(zt),.5))
            r['prior'].append(bal(yt,E_sig(zt+lo(pc)-lo(pool)),.5))
            r['local'].append(bal(yt,E_sig(zt),best_thr(yv,E_sig(zv))))
        out.append(dict(NTR=NTR,seed=seed,arm=arm,**{k:v for k,v in r.items()}))
json.dump(out,open('p3_prior_shift_results.json','w'))
for NTR in [300,1000,5000]:
  for arm in ['fedavg','fedavg_ft','central']:
    line=f'n={NTR} {arm:10s}'
    for k in ['fixed','prior','local']:
        rs=[o[k] for o in out if o['NTR']==NTR and o['arm']==arm]
        line+=f' | {k}: BA {np.mean([[x["ba"] for x in r] for r in rs]):.3f} worstFPR {np.mean([max(x["fpr"] for x in r) for r in rs]):.3f}'
    print(line)
