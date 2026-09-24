"""Baseline tuning on VALIDATION data only (train-side): lr and budget per arm, per domain. n=1000, seeds 0-2. Writes p4_tuned_config.json."""
import numpy as np, json, itertools
from p3_engine import *
import p4_data
def vba(E,C,ms):
    b=[]
    for c in range(len(C)):
        m=ms[c] if isinstance(ms,list) else ms; pv=E_sig(E.logit(m,E.va[c])); b.append(bal(C[c]['yva'],pv,best_thr(C[c]['yva'],pv))['ba'])
    return float(np.mean(b))
LRS=[1e-3,3e-3,1e-2]; res={}
for dom in ['iot','A']:
    R={}
    for seed in [0,1,2]:
        C,names=p4_data.iot(1000,seed,True) if dom=='iot' else p4_data.mobile('A',1000,seed); K=len(C)
        for lr in LRS:
            E=Eng(C,seed,3,30); E.lr=lr; X=torch.cat([t[0] for t in E.tr]); Y=torch.cat([t[1] for t in E.tr])
            for ep in [20,60]:
                R.setdefault(('local',lr,ep),[]).append(vba(E,C,[E.fit(E.mlp(),*E.tr[c],ep) for c in range(K)]))
                R.setdefault(('central',lr,ep),[]).append(vba(E,C,E.fit(E.mlp(),X,Y,ep)))
            for FR in [30,100]:
                R.setdefault(('fedavg',lr,FR),[]).append(vba(E,C,E.fed(FR=FR,FE=3)))
        print(dom,'seed',seed,flush=True)
    best={}
    for arm in ['local','central','fedavg']:
        cand={k:np.mean(v) for k,v in R.items() if k[0]==arm}; b=max(cand,key=cand.get); best[arm]=dict(lr=b[1],budget=b[2],val_ba=cand[b]); 
        print(dom,arm,'best',b,round(cand[b],4),'| all',{f'{k[1]:g}/{k[2]}':round(v,3) for k,v in cand.items()})
    res[dom]=best
json.dump(res,open('p4_tuned_config.json','w'),indent=1)
