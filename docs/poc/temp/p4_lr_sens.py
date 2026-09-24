"""Learning-rate sensitivity for convergence (IoT and mobile A, n=1000, seeds 0-2): local 20/60 epochs, central 20, FedAvg 30x3."""
import numpy as np, json
from p3_engine import *
import p4_data
def ev(E,C,ms):
    bas=[]
    for c in range(len(C)):
        m=ms[c] if isinstance(ms,list) else ms
        pv=E_sig(E.logit(m,E.va[c])); pt=E_sig(E.logit(m,E.te[c])); bas.append(bal(C[c]['yte'],pt,best_thr(C[c]['yva'],pv))['ba'])
    return float(np.mean(bas)),float(np.min(bas))
out=[]
for dom in ['iot','A']:
    for lr in [1e-3,3e-3,1e-2]:
        for seed in [0,1,2]:
            C,names=p4_data.iot(1000,seed,True) if dom=='iot' else p4_data.mobile('A',1000,seed); E=Eng(C,seed,3,30); E.lr=lr; K=len(C)
            X=torch.cat([t[0] for t in E.tr]); Y=torch.cat([t[1] for t in E.tr])
            out.append(dict(dom=dom,lr=lr,seed=seed,arm='local20',r=ev(E,C,[E.fit(E.mlp(),*E.tr[c],20) for c in range(K)])))
            out.append(dict(dom=dom,lr=lr,seed=seed,arm='local60',r=ev(E,C,[E.fit(E.mlp(),*E.tr[c],60) for c in range(K)])))
            out.append(dict(dom=dom,lr=lr,seed=seed,arm='central20',r=ev(E,C,E.fit(E.mlp(),X,Y,20))))
            out.append(dict(dom=dom,lr=lr,seed=seed,arm='fedavg30x3',r=ev(E,C,E.fed(FR=30,FE=3))))
        for arm in ['local20','local60','central20','fedavg30x3']:
            r=[o['r'] for o in out if o['dom']==dom and o['lr']==lr and o['arm']==arm]; print(f'{dom:4s} lr={lr:g} {arm:11s} BA {np.mean([x[0] for x in r]):.3f} worst {np.mean([x[1] for x in r]):.3f}',flush=True)
json.dump(out,open('p4_lr_sens_results.json','w'))
