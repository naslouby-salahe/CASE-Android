"""Optimization-budget sensitivity for central and FedAvg (both domains, n=1000, seeds 0-2). local-only fixed at 150 epochs for reference."""
import numpy as np, json
from p3_engine import *
import p4_data
def ev(E,C,g_or_list):
    bas=[]
    for c in range(len(C)):
        m=g_or_list[c] if isinstance(g_or_list,list) else g_or_list
        pv=E_sig(E.logit(m,E.va[c])); pt=E_sig(E.logit(m,E.te[c])); bas.append(bal(C[c]['yte'],pt,best_thr(C[c]['yva'],pv))['ba'])
    return float(np.mean(bas)),float(np.min(bas))
out=[]
for dom in ['iot','A']:
    for seed in [0,1,2]:
        C,names=p4_data.iot(1000,seed,True) if dom=='iot' else p4_data.mobile('A',1000,seed); E=Eng(C,seed,3,30); K=len(C)
        X=torch.cat([t[0] for t in E.tr]); Y=torch.cat([t[1] for t in E.tr])
        for ep in [20,100,300]: out.append(dict(dom=dom,seed=seed,arm='central',budget=ep,r=ev(E,C,E.fit(E.mlp(),X,Y,ep))))
        for FR,FE in [(30,3),(100,3),(300,3)]: out.append(dict(dom=dom,seed=seed,arm='fedavg',budget=f'{FR}x{FE}',r=ev(E,C,E.fed(FR=FR,FE=FE))))
        for ep in [20,150,400]: out.append(dict(dom=dom,seed=seed,arm='local',budget=ep,r=ev(E,C,[E.fit(E.mlp(),*E.tr[c],ep) for c in range(K)])))
        print(dom,seed,'done',flush=True)
json.dump(out,open('p4_budget_sens_results.json','w'))
for dom in ['iot','A']:
    for arm in ['local','central','fedavg']:
        for b in sorted(set(str(o['budget']) for o in out if o['dom']==dom and o['arm']==arm),key=lambda x:int(x.split('x')[0])*(int(x.split('x')[1]) if 'x' in x else 1)):
            r=[o['r'] for o in out if o['dom']==dom and o['arm']==arm and str(o['budget'])==b]; print(f'{dom:4s} {arm:8s} budget {b:>7s} BA {np.mean([x[0] for x in r]):.3f} worst {np.mean([x[1] for x in r]):.3f}')
