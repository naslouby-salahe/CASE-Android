"""Fairness/sensitivity: does local-only performance depend on the local epoch budget and on input scaling? IoT n=1000 and mobile A n=1000."""
import numpy as np, json, sys
from p3_engine import *
import p4_data
out=[]
for dom,std in [('iot',True),('iot',False),('A',None)]:
    for seed in [0,1,2]:
        C,names=p4_data.iot(1000,seed,std) if dom=='iot' else p4_data.mobile('A',1000,seed); E=Eng(C,seed,3,30); K=len(C)
        for ep in [20,60,150]:
            bas=[]
            for c in range(K):
                m=E.fit(E.mlp(),*E.tr[c],ep); pv=E_sig(E.logit(m,E.va[c])); pt=E_sig(E.logit(m,E.te[c])); bas.append(bal(C[c]['yte'],pt,best_thr(C[c]['yva'],pv))['ba'])
            out.append(dict(dom=dom,std=std,seed=seed,ep=ep,ba=float(np.mean(bas)),wba=float(np.min(bas))))
    for ep in [20,60,150]:
        r=[o for o in out if o['dom']==dom and o['std']==std and o['ep']==ep]; print(dom,std,'local epochs',ep,'BA',round(np.mean([o['ba'] for o in r]),3),'worst',round(np.mean([o['wba'] for o in r]),3),flush=True)
json.dump(out,open('p4_epoch_sens_results.json','w'))
