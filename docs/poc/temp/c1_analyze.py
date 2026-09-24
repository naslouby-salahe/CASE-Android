import json,numpy as np,os,sys
from collections import defaultdict
PO=['LOCAL','GLOBAL','GLOBAL-MED','CLUSTER','TRIM-ORACLE','PI-LOCAL@0.1','PI-GLOBAL@0.1','PI-LOCAL@0.2','PI-GLOBAL@0.2']
def agg(rs,pol,key):
    v=[np.mean(r['pol'][pol][key]) if key not in('wdev','wfpr','wtpr') else r['pol'][pol][key] for r in rs]; return float(np.mean(v))
for dom in ['mobile','nbaiot','scidb']:
    f=f'c1_results_{dom}.json'
    if not os.path.exists(f): continue
    R=json.load(open(f)); sc=[r for r in R if r.get('kind')=='scorer']; R=[r for r in R if r.get('kind')!='scorer']
    print(f'\n######## {dom}  seeds={len(sc)} clients={len(sc[0]["names"])}')
    print('scorer AUC per client (mean over seeds):',dict(zip(sc[0]['names'],np.round(np.mean([s["auc"] for s in sc],0),2))))
    print('true malware prevalence:',dict(zip(sc[0]['names'],np.round(sc[0]['prev'],2))),' cal-benign n:',sc[0]['n_cal_benign'])
    for alpha in [0.05]:
        for ctype in ['rand','stealth','top']:
            print(f'\n== alpha={alpha} contamination={ctype}: policy -> meanFPRdev / worstFPRdev / macroTPR / worstTPR / FPRsd / ctrl(FPR<=a+.01)')
            groups=defaultdict(list)
            for r in R:
                if r['alpha']==alpha and r['ctype']==ctype: groups[(r['pattern'],r['label'])].append(r)
            for (pat,lab),rs in groups.items():
                eps=np.mean([r['eps'] for r in rs],0); print(f'-- {pat} {lab} (mean eps {eps.mean():.3f}, max {eps.max():.2f})')
                for p in PO:
                    print(f'   {p:16s} {agg(rs,p,"dev"):.3f} / {agg(rs,p,"wdev"):.3f} / {agg(rs,p,"tpr"):.3f} / {agg(rs,p,"wtpr"):.3f} / {agg(rs,p,"fsd"):.3f} / {agg(rs,p,"ctrl"):.2f}')
