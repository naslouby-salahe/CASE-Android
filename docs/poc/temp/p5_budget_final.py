"""Final tables for candidate A/F: LAB-EB-TAU vs strongest simple baselines; seed stability; stealth; alpha=.01."""
import json,sys,numpy as np
PO=['LOCAL','GLOBAL','CLEAN-K','CLEAN-K-GLOBAL','CLEAN-K-SHRINK','PEER-TRIM','LAB-LOCAL','LAB-POOL','LAB-EB','LAB-EB-TAU','ORACLE-TRUE']
def cells(R,ct,scens,k,seed=None): return [r for r in R if r['ctype'] in ct and r['k']==k and r['scen'] in scens and (seed is None or r['seed']==seed)]
def m(rs,p,key): return float(np.mean([r['pol'][p][key] for r in rs]))
for A in ['0.05','0.01']:
  for dom in ['mobsup','nbaiot','scidb']:
    R=json.load(open(f'p5_budget_{dom}_a{A}.json')); dirty=[s for s in set(r['scen'] for r in R) if s!='hom0']
    print(f'\n### {dom} alpha={A}: contaminated (rand+top), k=10 and k=20: tpr wtpr | fpr wfpr | succ')
    for k in [10,20]:
        rs=cells(R,['rand','top'],dirty,k); print(f' k={k}')
        for p in PO: print(f'   {p:15s} {m(rs,p,"tpr"):.3f} {m(rs,p,"wtpr"):.3f} | {m(rs,p,"fpr"):.3f} {m(rs,p,"wfpr"):.3f} | {m(rs,p,"succ"):.2f}')
    if A=='0.05':
        for k in [10,20]:
            d=[m(cells(R,['rand','top'],dirty,k,s),'LAB-EB-TAU','succ')-m(cells(R,['rand','top'],dirty,k,s),'CLEAN-K','succ') for s in range(5)]
            dw=[m(cells(R,['rand','top'],dirty,k,s),'LAB-EB-TAU','wtpr')-m(cells(R,['rand','top'],dirty,k,s),'LAB-EB-TAU' if False else 'LOCAL','wtpr') for s in range(5)]
            print(f' seed-wise k={k}: succ(TAU-CLEANK) {np.round(d,2).tolist()} wins {sum(x>0 for x in d)}/5 ; wTPR gain vs LOCAL {np.round(dw,2).tolist()}')
        rs=cells(R,['stealth'],dirty,10); print(' stealth contaminants k=10: LOCAL tpr/wtpr %.3f/%.3f  TAU %.3f/%.3f  ORACLE %.3f/%.3f  TAU wfpr %.3f LOCAL wfpr %.3f'%(m(rs,'LOCAL','tpr'),m(rs,'LOCAL','wtpr'),m(rs,'LAB-EB-TAU','tpr'),m(rs,'LAB-EB-TAU','wtpr'),m(rs,'ORACLE-TRUE','tpr'),m(rs,'ORACLE-TRUE','wtpr'),m(rs,'LAB-EB-TAU','wfpr'),m(rs,'LOCAL','wfpr')))
        rs=cells(R,['rand','top','stealth'],['hom0'],10); print(' clean eps=0 k=10: TAU dTPR %+.3f dwFPR %+.3f'%(m(rs,'LAB-EB-TAU','tpr')-m(rs,'LOCAL','tpr'),m(rs,'LAB-EB-TAU','wfpr')-m(rs,'LOCAL','wfpr')))
