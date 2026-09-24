"""P44 extension: honest heterogeneous clients vs malicious clients, both domains. attacks: flip (all labels), target (malware->benign), sign (reversed x3 update).
Outlier score = mean distance of client update to coordinate-median update (aggregator-independent), plus trimmed-mean trim share.
Usage: python p4_robust.py DOMAIN(A|B|iot) NTR seeds"""
import numpy as np, sys, json, time
from p3_engine import *
import p4_data
CFG=json.load(open('p4_final_config.json'))['iot' if sys.argv[1]=='iot' else 'mobile']
DOM=sys.argv[1]; NTR=int(sys.argv[2]); SEEDS=[int(s) for s in sys.argv[3].split(',')]
out=[]
for seed in SEEDS:
    C,names=p4_data.mobile(DOM,NTR,seed) if DOM in('A','B') else p4_data.iot(NTR,seed); K=len(C); E=Eng(C,seed,CFG['fed'][2],CFG['fed'][1]); E.lr=CFG['fed'][0]; t=time.time()
    atk_clients=[names.index('1mobile'),names.index('appchina'),names.index('play')] if DOM=='A' else ([0,3,6] if DOM=='iot' else [0,4,8])
    for agg in ['mean','median','trimmed','krum']:
        for attack,atk in [(None,None)]+[(a,c) for a in ['flip','target','sign'] for c in atk_clients]:
            g,fl=E.fed(agg=agg,poison=atk,attack=attack or 'flip',ret_flags=True,FR=60)
            bas=[]
            for c in range(K):
                pv=E_sig(E.logit(g,E.va[c])); pt=E_sig(E.logit(g,E.te[c])); b=bal(C[c]['yte'],pt,best_thr(C[c]['yva'],pv)); b['auc']=auc(C[c]['yte'],pt); bas.append(b)
            out.append(dict(seed=seed,agg=agg,attack=attack,attacker=None if atk is None else names[atk],ba=[b['ba'] for b in bas],fnr=[b['fnr'] for b in bas],fpr=[b['fpr'] for b in bas],auc=[b['auc'] for b in bas],flags=list(map(float,fl)),dist=list(map(float,E.last_dist))))
    print('seed',seed,round(time.time()-t),flush=True)
json.dump(dict(names=names,runs=out),open(f'p4_robust_{DOM}_n{NTR}.json','w'))
