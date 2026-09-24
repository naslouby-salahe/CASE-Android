"""P4 IoT decisive POC: 8 Raspberry Pi device clients (SciDB 10.57760/sciencedb.25380, 32d-feature data/device/*.csv).
Exact-duplicate windows (x5 replication) are collapsed BEFORE splitting. Binary: label 0 benign vs 1..8 malware.
Usage: python p4_iot_v1.py NTR seeds [std]"""
import numpy as np, pandas as pd, sys, json, time
from p3_engine import *
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/iot/'
NTR=int(sys.argv[1]); SEEDS=[int(s) for s in sys.argv[2].split(',')]; STD=len(sys.argv)>3 and sys.argv[3]=='std'
dev=[pd.read_csv(SP+f'dev{i}.csv') for i in range(8)]; F=[c for c in dev[0].columns if c!='label']
U=[]
for d in dev:
    d=d.copy(); d['k']=d[F].round(10).apply(tuple,axis=1); d=d.drop_duplicates('k').drop(columns='k').reset_index(drop=True); U.append(d)
res=[]
for seed in SEEDS:
    t=time.time(); rng=np.random.RandomState(seed); C=[]; tr_all=[]
    for d in U:
        X=d[F].values.astype(np.float32); y=(d.label.values>0).astype(np.int8); ii=rng.permutation(len(d)); n=len(ii); a,b=int(.6*n),int(.75*n)
        tr=ii[:a][:NTR]; va=ii[a:b][:max(60,min(1500,NTR//3))]; te=ii[b:]
        C.append(dict(Xtr=X[tr],ytr=y[tr],Xva=X[va],yva=y[va],Xte=X[te],yte=y[te])); tr_all.append(X[tr])
    if STD:
        A=np.concatenate(tr_all); mu,sd=A.mean(0),A.std(0)+1e-6
        for c in C:
            for k in ['Xtr','Xva','Xte']: c[k]=((c[k]-mu)/sd).astype(np.float32)
    E,logit,T,lab=run_arms(C,seed,cfg=json.load(open('p4_final_config.json'))['iot']); out=evaluate(C,logit); pol,choice=policies(C,logit); out.update(pol)
    res.append(dict(seed=seed,names=[f'dev{i}' for i in range(8)],T=T.tolist(),cluster=lab.tolist(),choice=choice,H={**hetero_stats(C,T),**extra_stats(C,logit)},res=out,nte=[len(c['yte']) for c in C],prev_tr=[float(c['ytr'].mean()) for c in C]))
    print('seed',seed,round(time.time()-t),flush=True)
tag='_std' if STD else ''
json.dump(res,open(f'p4_iot_v3_n{NTR}{tag}.json','w'))
for a in ['local|local','local|fixed','central|local','fedavg|fixed','fedavg|local','fedprox|local','fedavg_ft|local','cluster|local','shrink|local','tgraph|local','policy_valselect|local','oracle_arm|local']:
    M=lambda k:np.mean([[r[k] for r in s['res'][a]] for s in res]); W=np.mean([min(r['ba'] for r in s['res'][a]) for s in res]); WF=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res])
    print(f'{a:26s} BA {M("ba"):.3f} worstBA {W:.3f} F1 {M("f1"):.3f} worstFPR {WF:.3f}')
