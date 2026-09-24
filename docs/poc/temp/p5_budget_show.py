import json,sys,numpy as np
dom=sys.argv[1]; R=json.load(open(f'p5_budget_{dom}_a0.05.json'))
PO=['LOCAL','GLOBAL','CLEAN-K','PEER-TRIM','LAB-LOCAL','LAB-POOL','LAB-EB','PEER+LAB','LAB-EB-ALLOC','ORACLE-TRIM','ORACLE-TRUE']
def show(ct,sc,ks):
    for k in ks:
        rs=[r for r in R if r['ctype']==ct and r['scen']==sc and r['k']==k]
        print(f'-- {dom} {ct} {sc} k={k}  (tpr / worst-tpr / fdev / worst-fpr)')
        for p in PO:
            if p not in rs[0]['pol']: continue
            f=lambda key:np.mean([r['pol'][p][key] for r in rs])
            print(f'   {p:13s} {f("tpr"):.3f} {f("wtpr"):.3f} {f("fdev"):.3f} {f("wfpr"):.3f}')
if __name__=='__main__':
    for ct,sc,ks in [('rand','hom0.1',[10]),('rand','hetlin',[5,20]),('top','hetlin',[10]),('rand','hom0',[10])]: show(ct,sc,ks)
