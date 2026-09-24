import json,glob,numpy as np,sys
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
KEY=['local|local','local|fixed','central|local','fedavg|fixed','fedavg|local','fedprox|local','fedavg_ft|local','cluster|local','shrink|local','policy_valselect|local','oracle_arm|local']
def stat(res,a):
    ba=np.mean([[r['ba'] for r in s['res'][a]] for s in res]); w=np.mean([min(r['ba'] for r in s['res'][a]) for s in res])
    wf=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res]); return ba,w,wf
def boot_ci(res,a,b,n=2000):  # seed-level paired diff of mean BA
    d=np.array([np.mean([r['ba'] for r in s['res'][a]])-np.mean([r['ba'] for r in s['res'][b]]) for s in res]); return d.mean(),d.std(ddof=1)/np.sqrt(len(d))
rows=[]
for pre in ['p3_lamda_v2_A','p3_lamda_v2_B','p3_nbaiot_v2']:
    for f in sorted(glob.glob(pre+'_n*.json'),key=lambda s:int(s.split('_n')[-1][:-5])):
        res=json.load(open(f)); n=int(f.split('_n')[-1][:-5]); print(f'\n### {f}  seeds={len(res)} clients={len(res[0]["names"])}')
        print(f'{"arm":26s} meanBA  worstBA  worstFPR')
        for a in KEY:
            b,w,wf=stat(res,a); print(f'{a:26s} {b:.3f}  {w:.3f}   {wf:.3f}')
        for a,b in [('fedavg_ft|local','local|local'),('fedavg|local','local|local'),('policy_valselect|local','fedavg_ft|local'),('shrink|local','local|local'),('cluster|local','fedavg|local')]:
            m,se=boot_ci(res,a,b); print(f'  diff {a} - {b}: {m:+.4f} (se {se:.4f})')
        from collections import Counter
        print('  valselect choices',dict(Counter(c for s in res for c in s['choice'])))
# RQ3: gating features vs gain
for pre in ['p3_lamda_v2_A','p3_lamda_v2_B','p3_nbaiot_v2']:
    X=[];g=[];sd=[];NN=[]
    for f in sorted(glob.glob(pre+'_n*.json')):
        for s in json.load(open(f)):
            H=s['H']; K=len(H['n'])
            for c in range(K):
                gain=s['res']['fedavg_ft|local'][c]['ba']-s['res']['local|local'][c]['ba']
                X.append([np.log(H['n'][c]),H['T_gap'][c],H['jsd_pool'][c],H['prev_gap'][c],H['T_diag'][c]]);g.append(gain);sd.append(s['seed'])
    X=np.array(X);g=np.array(g);sd=np.array(sd)
    print(f'\n### gating analysis {pre}: {len(g)} client-runs, frac(ft>local)={np.mean(g>0):.2f}')
    for i,nm in enumerate(['log_n','T_gap','jsd_pool','prev_gap','T_diag']): print(f'  spearman gain~{nm}: {spearmanr(X[:,i],g)[0]:+.2f}')
    pred=np.zeros(len(g),bool)
    for s0 in set(sd):
        tr=sd!=s0; Z=(X-X[tr].mean(0))/(X[tr].std(0)+1e-9)
        if len(set(g[tr]>0))>1: pred[sd==s0]=LogisticRegression(C=1.0).fit(Z[tr],g[tr]>0).predict(Z[sd==s0])
    print(f'  gate (LOSO-seed logistic) mean gain when routed {np.mean(np.where(pred,g,0)):+.4f} ; always-ft {g.mean():+.4f}; always-local 0; oracle {np.mean(np.maximum(g,0)):+.4f}; routed frac {pred.mean():.2f}')
