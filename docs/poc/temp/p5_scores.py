"""P5 stage: cache frozen federated-AE scores per client so policy experiments are cheap.
Reuses poc2 c1_common (client builders + fed AE). Usage: python p5_scores.py DOMAIN seeds"""
import sys, numpy as np
sys.path.insert(0,'/home/naslouby/Projects/CASE-Android/docs/poc2/temp')
from c1_common import *
from sklearn.metrics import roc_auc_score
DOM=sys.argv[1]
for seed in [int(s) for s in sys.argv[2].split(',')]:
    C,names,binary,prev=build(DOM,seed); g=train_fed_ae(C,binary,seed); d={}
    for i,c in enumerate(C):
        for k,src in [('cb','Xcb'),('cm','Xcm'),('tb','Xtb'),('tm','Xtm'),('trb','Xtr')]: d[f'{i}_{k}']=rec_err(g,c[src],binary)
    d['names']=np.array(names); d['prev']=np.array(prev)
    np.savez(f'p5_scores/{DOM}_s{seed}.npz',**d)
    auc=[roc_auc_score(np.r_[np.zeros(len(d[f'{i}_tb'])),np.ones(len(d[f'{i}_tm']))],np.r_[d[f'{i}_tb'],d[f'{i}_tm']]) for i in range(len(C))]
    print(DOM,seed,np.round(auc,2),flush=True)
