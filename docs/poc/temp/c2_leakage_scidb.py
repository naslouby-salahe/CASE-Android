"""C2: effect of exact-duplicate windows on evaluation of a federated AE detector (SciDB Pi devices). raw-row random split (leaky) vs de-duplicated split."""
import numpy as np, pandas as pd, json
from c1_common import *
from c1_common import _split
from sklearn.metrics import roc_auc_score
def build_raw(seed,dedup):
    rng=np.random.RandomState(seed); C=[]
    for i in range(8):
        d=pd.read_csv(SPD+f'iot/dev{i}.csv'); F=[c for c in d.columns if c!='label']
        if dedup: d['k']=d[F].round(10).apply(tuple,axis=1); d=d.drop_duplicates('k').drop(columns='k')
        X=d[F].values.astype(np.float32); y=d.label.values; C.append(_split(X[y==0],X[y>0],rng))
    A=np.concatenate([c['Xtr'] for c in C]); mu,sd=A.mean(0),A.std(0)+1e-6
    for c in C:
        for k in c: c[k]=((c[k]-mu)/sd).astype(np.float32)
    return C
out=[]
for seed in range(5):
    for dedup in [False,True]:
        C=build_raw(seed,dedup); g=train_fed_ae(C,False,seed); a=[];fp=[];tp=[]
        for c in C:
            cb=rec_err(g,c['Xcb'],False); tb=rec_err(g,c['Xtb'],False); tm=rec_err(g,c['Xtm'],False); t=np.quantile(cb,.95,method='higher')
            a.append(roc_auc_score(np.r_[np.zeros(len(tb)),np.ones(len(tm))],np.r_[tb,tm])); fp.append(np.mean(tb>t)); tp.append(np.mean(tm>t))
        # exact-duplicate leakage: share of test rows whose exact vector is in the same device's train rows
        out.append(dict(seed=seed,dedup=dedup,auc=float(np.mean(a)),fpr=float(np.mean(fp)),tpr=float(np.mean(tp)),wtpr=float(np.min(tp)),n=int(sum(len(c['Xtr'])+len(c['Xtb']) for c in C))))
        print(out[-1],flush=True)
json.dump(out,open('c2_leakage_scidb_results.json','w'))
for dd in [False,True]:
    r=[o for o in out if o['dedup']==dd]; print('dedup',dd,{k:round(np.mean([o[k] for o in r]),3) for k in ['auc','fpr','tpr','wtpr','n']})
