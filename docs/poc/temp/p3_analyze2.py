import json,glob,numpy as np
from collections import defaultdict
print('## threshold scope (config A, mean over 5 seeds): meanBA / worstFPR / FPR-sd   [arm fedavg_ft]')
for cfg in ['A','B']:
  for n in [100,300,1000,5000]:
    res=json.load(open(f'p3_lamda_v2_{cfg}_n{n}.json')); line=f'{cfg} n={n:5d} '
    for sc in ['fixed','global','local','shrunk']:
        a=f'fedavg_ft|{sc}'; ba=np.mean([[r['ba'] for r in s['res'][a]] for s in res]); wf=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res]); sd=np.mean([np.std([r['fpr'] for r in s['res'][a]]) for s in res])
        line+=f'| {sc}: {ba:.3f}/{wf:.3f}/{sd:.3f} '
    print(line)
print('## same for fedavg')
for cfg in ['A']:
  for n in [100,300,1000,5000]:
    res=json.load(open(f'p3_lamda_v2_{cfg}_n{n}.json')); line=f'{cfg} n={n:5d} '
    for sc in ['fixed','global','local','shrunk']:
        a=f'fedavg|{sc}'; ba=np.mean([[r['ba'] for r in s['res'][a]] for s in res]); wf=np.mean([max(r['fpr'] for r in s['res'][a]) for s in res]); sd=np.mean([np.std([r['fpr'] for r in s['res'][a]]) for s in res])
        line+=f'| {sc}: {ba:.3f}/{wf:.3f}/{sd:.3f} '
    print(line)
print('## transfer matrix (config A, n=5000, mean over seeds) & negative transfer')
res=json.load(open('p3_lamda_v2_A_n5000.json')); names=res[0]['names']; T=np.mean([s['T'] for s in res],0)
print(names); print(np.round(T,2)); neg=[(names[i],names[j],round(T[i,j],2)) for i in range(len(names)) for j in range(len(names)) if i!=j and T[i,j]<0.6]; print('pairs AUC<0.6:',neg)
off=[T[i,j] for i in range(len(names)) for j in range(len(names)) if i!=j]; print('off-diag AUC min/median/max',np.min(off),np.median(off),np.max(off), 'diag mean',np.mean(np.diag(T)))
print('## per-client fedavg_ft - local BA gain (A, n=1000) mean over seeds')
res=json.load(open('p3_lamda_v2_A_n1000.json'))
for c,nm in enumerate(names): print(nm, 'ft-local',round(np.mean([s['res']['fedavg_ft|local'][c]['ba']-s['res']['local|local'][c]['ba'] for s in res]),3),'fedavg-local',round(np.mean([s['res']['fedavg|local'][c]['ba']-s['res']['local|local'][c]['ba'] for s in res]),3),'shrink-local',round(np.mean([s['res']['shrink|local'][c]['ba']-s['res']['local|local'][c]['ba'] for s in res]),3),'central-fedavg',round(np.mean([s['res']['central|local'][c]['ba']-s['res']['fedavg|local'][c]['ba'] for s in res]),3))
# extras
ex=json.load(open('p3_extras_results_s1-4.json'))
print('\n## abstention (fedavg/local, seeds 1-4): scope, cov target -> mean coverage, mean err, worst-client err')
agg=defaultdict(list)
for r in ex['abstain']: agg[(r['arm'],r['target_cov'],r['scope'])].append(r['per_client'])
for k in sorted(agg):
    if k[0] in('fedavg','fedavg_ft'):
        errs=[[c['err'] for c in pc] for pc in agg[k]]; covs=[[c['cov'] for c in pc] for pc in agg[k]]
        print(k,'cov',round(np.mean(covs),3),'covsd',round(np.mean([np.std(c) for c in covs]),3),'err',round(np.mean(errs),3),'worst-client err',round(np.mean([max(e) for e in errs]),3))
print('\n## robust aggregation (seeds 1-4): mean honest BA, worst honest BA, per-client flags')
agg=defaultdict(list)
for r in ex['robust']: agg[(r['agg'],r['attacker'])].append(r)
for k in sorted(agg,key=lambda x:(x[0],str(x[1]))):
    rs=agg[k]; atk=k[1]; idx=None if atk is None else names.index(atk)
    hon=[[b for i,b in enumerate(r['ba']) if i!=idx] for r in rs]
    print(k,'honestBA',round(np.mean(hon),3),'worst',round(np.mean([min(h) for h in hon]),3),'flags',np.round(np.mean([r['flags'] for r in rs],0),2).tolist() if k[0] in('median','trimmed','krum') else '')
print('\n## cold start (seeds 1-4), mean BA / worst-client BA / mean FPR by method and k')
agg=defaultdict(lambda:defaultdict(list))
for r in ex['cold']:
    for m,v in r['R'].items(): agg[(r['k'],m)][r['seed']].append((v['ba'],v['fpr'],r['client']))
for k in sorted(agg):
    ba=np.mean([np.mean([x[0] for x in v]) for v in agg[k].values()]); w=np.mean([min(x[0] for x in v) for v in agg[k].values()]); f=np.mean([np.mean([x[1] for x in v]) for v in agg[k].values()])
    print(k,f'BA {ba:.3f} worst {w:.3f} FPR {f:.3f}')
