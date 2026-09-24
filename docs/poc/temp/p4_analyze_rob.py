import json,numpy as np
from collections import defaultdict
for dom in ['A','iot']:
    R=json.load(open(f'p4_robust_{dom}_n1000.json')); names=R['names']; K=len(names); runs=R['runs']
    print(f'\n## P44 domain={dom} clients={names} seeds={sorted(set(r["seed"] for r in runs))}')
    base={}
    for agg in ['mean','median','trimmed','krum']:
        b=[r for r in runs if r['agg']==agg and r['attack'] is None]; base[agg]=(np.mean([np.mean(r['ba']) for r in b]),np.mean([np.min(r['ba']) for r in b]),np.mean([np.mean(r['fnr']) for r in b]))
    print('no attack: '+' | '.join(f'{a}: BA {v[0]:.3f} wBA {v[1]:.3f} FNR {v[2]:.3f}' for a,v in base.items()))
    print('no-attack outlier score (dist to median update) per client, mean over seeds (mean aggregator):')
    d0=np.mean([r['dist'] for r in runs if r['agg']=='mean' and r['attack'] is None],0); print('  '+' '.join(f'{n}:{v:.2f}' for n,v in zip(names,d0)))
    t0=np.mean([r['flags'] for r in runs if r['agg']=='trimmed' and r['attack'] is None],0); print('trim-share no attack: '+' '.join(f'{n}:{v:.2f}' for n,v in zip(names,t0)))
    for attack in ['flip','target','sign']:
        print(f' attack={attack}')
        for agg in ['mean','median','trimmed','krum']:
            rs=[r for r in runs if r['agg']==agg and r['attack']==attack]; hon=[];rk=[];sep=[];fnr=[];trimr=[]
            for r in rs:
                a=names.index(r['attacker']); h=[i for i in range(K) if i!=a]; hon.append((np.mean([r['ba'][i] for i in h]),np.min([r['ba'][i] for i in h]))); fnr.append(np.mean([r['fnr'][i] for i in h]))
                dist=np.array(r['dist']); rk.append((dist<dist[a]).sum()/(K-1)); sep.append(dist[a]/max(dist[h].max(),1e-9))
                fl=np.array(r['flags']); trimr.append((fl<fl[a]).sum()/(K-1) if agg=='trimmed' else np.nan)
            print(f'   {agg:8s} honestBA {np.mean([h[0] for h in hon]):.3f} (Δ{np.mean([h[0] for h in hon])-base[agg][0]:+.3f}) honestWorst {np.mean([h[1] for h in hon]):.3f} honestFNR {np.mean(fnr):.3f} | attacker dist-rank {np.mean(rk):.2f} (1=top outlier) attacker/maxHonest dist {np.mean(sep):.2f} trim-rank {np.nanmean(trimr) if agg=="trimmed" else float("nan"):.2f}')

from sklearn.metrics import roc_auc_score
print('\n## Attack detection from update-distance statistic S = max_i dist_i / median_i dist_i (positive = attacked run, negative = no-attack run), AUC by aggregator/attack')
for dom in ['A','iot']:
    R=json.load(open(f'p4_robust_{dom}_n1000.json')); runs=R['runs']; K=len(R['names'])
    for agg in ['mean','median','trimmed','krum']:
        neg=[max(r['dist'])/np.median(r['dist']) for r in runs if r['agg']==agg and r['attack'] is None]
        line=f'{dom:4s} {agg:8s} no-attack S mean {np.mean(neg):.2f} |'
        for attack in ['flip','target','sign']:
            pos=[max(r['dist'])/np.median(r['dist']) for r in runs if r['agg']==agg and r['attack']==attack]
            line+=f' {attack}: S {np.mean(pos):.2f} AUC {roc_auc_score([0]*len(neg)+[1]*len(pos),neg+pos):.2f} |'
        print(line)
    # honest false alarm of a fixed rule S>tau tuned so that flip-attack recall=0.9
    for attack in ['flip']:
        pos=[max(r['dist'])/np.median(r['dist']) for r in runs if r['agg']=='mean' and r['attack']==attack]; neg=[max(r['dist'])/np.median(r['dist']) for r in runs if r['agg']=='mean' and r['attack'] is None]
        tau=np.percentile(pos,10); print(f'{dom}: rule S>{tau:.2f} (recall .9 on label-flip) false-alarm rate on no-attack runs = {np.mean(np.array(neg)>tau):.2f} (n_neg={len(neg)})')
print('\n## calibrated AUC of honest clients (mean over honest) by aggregator, no attack vs attacks')
for dom in ['A','iot']:
    R=json.load(open(f'p4_robust_{dom}_n1000.json')); runs=R['runs']; names=R['names']; K=len(names)
    for agg in ['mean','median','trimmed','krum']:
        line=f'{dom:4s} {agg:8s}'
        for attack in [None,'flip','target','sign']:
            v=[]
            for r in runs:
                if r['agg']==agg and r['attack']==attack:
                    a=names.index(r['attacker']) if attack else -1; v.append(np.mean([r['auc'][i] for i in range(K) if i!=a]))
            line+=f' {attack or "none"}: {np.mean(v):.3f}'
        print(line)
