"""Aggregate p5_budget results: headline table per domain, k-sweep, clean-client harm, recovered fraction."""
import json,sys,numpy as np
DOMS=sys.argv[1].split(',') if len(sys.argv)>1 else ['mobsup','nbaiot','scidb']; A=sys.argv[2] if len(sys.argv)>2 else '0.05'
PO=['LOCAL','GLOBAL','CLEAN-K','PEER-TRIM','LAB-LOCAL','LAB-POOL','LAB-EB','PEER+LAB','LAB-EB-ALLOC','LAB-EB-V','LAB-EB-TAU','LAB-EB-VTAU','ORACLE-TRUE']
def sel(R,ct,scens,k): return [r for r in R if r['ctype'] in ct and r['k']==k and (scens is None or r['scen'] in scens)]
def mean(rs,p,key): return float(np.mean([r['pol'][p][key] for r in rs if p in r['pol']]))
for dom in DOMS:
    R=json.load(open(f'p5_budget_{dom}_a{A}.json')); print(f'\n##### {dom} alpha={A}  (mean over 5 seeds x ctype{{rand,top}} x contaminated scenarios hom.05/.10/.20/het)')
    dirty=[s for s in set(r['scen'] for r in R) if s!='hom0']
    for k in [5,10,20,50]:
        rs=sel(R,['rand','top'],dirty,k); 
        print(f'-- k={k}  policy: tpr  wtpr  | fpr  wfpr  fdev  | succ  | recTPR recWTPR')
        L=mean(rs,'LOCAL','tpr'); LW=mean(rs,'LOCAL','wtpr'); O=mean(rs,'ORACLE-TRUE','tpr'); OW=mean(rs,'ORACLE-TRUE','wtpr')
        for p in PO:
            if p not in rs[0]['pol']: continue
            if p in('CLEAN-K','LAB-LOCAL','LAB-POOL','LAB-EB','PEER+LAB','LAB-EB-ALLOC') or True:
                print(f'   {p:13s} {mean(rs,p,"tpr"):.3f} {mean(rs,p,"wtpr"):.3f} | {mean(rs,p,"fpr"):.3f} {mean(rs,p,"wfpr"):.3f} {mean(rs,p,"fdev"):.3f} | {mean(rs,p,"succ"):.2f} | {(mean(rs,p,"tpr")-L)/(O-L):.2f} {(mean(rs,p,"wtpr")-LW)/(OW-LW):.2f}')
    rs=sel(R,['rand','top','stealth'],['hom0'],10); print('-- clean (eps=0) k=10: harm vs LOCAL: dTPR dwFPR dfdev')
    for p in ['GLOBAL','CLEAN-K','PEER-TRIM','LAB-POOL','LAB-EB','PEER+LAB']:
        print(f'   {p:13s} {mean(rs,p,"tpr")-mean(rs,"LOCAL","tpr"):+.3f} {mean(rs,p,"wfpr")-mean(rs,"LOCAL","wfpr"):+.3f} {mean(rs,p,"fdev")-mean(rs,"LOCAL","fdev"):+.3f}')
