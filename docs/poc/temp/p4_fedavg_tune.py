import numpy as np, json
from p3_engine import *
import p4_data
def vt(E,C,m):
    v=[];t=[]
    for c in range(len(C)):
        pv=E_sig(E.logit(m,E.va[c])); pt=E_sig(E.logit(m,E.te[c])); v.append(bal(C[c]['yva'],pv,best_thr(C[c]['yva'],pv))['ba']); t.append(bal(C[c]['yte'],pt,best_thr(C[c]['yva'],pv))['ba'])
    return np.mean(v),np.mean(t),np.min(t)
out=[]
for dom in ['iot','A']:
    for FR,FE,lr in [(100,3,3e-3),(200,1,3e-3),(300,1,3e-3),(150,1,1e-2),(200,2,3e-3),(400,1,3e-3)]:
        r=[]
        for seed in [0,1]:
            C,_=p4_data.iot(1000,seed,True) if dom=='iot' else p4_data.mobile('A',1000,seed); E=Eng(C,seed,3,30); E.lr=lr; r.append(vt(E,C,E.fed(FR=FR,FE=FE)))
        r=np.mean(r,0); out.append(dict(dom=dom,FR=FR,FE=FE,lr=lr,val=r[0],test=r[1],worst=r[2])); print(dom,f'FR={FR} FE={FE} lr={lr:g}: val {r[0]:.3f} test {r[1]:.3f} worst {r[2]:.3f}',flush=True)
json.dump(out,open('p4_fedavg_tune_results.json','w'))
