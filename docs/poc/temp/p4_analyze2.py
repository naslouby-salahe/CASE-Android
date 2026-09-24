import json,os,numpy as np,pandas as pd
from sklearn.linear_model import Ridge
from collections import Counter
DOMS={'mobile_A':('p4_lamda_v5_A_n{}.json',[100,300,1000,5000]),'mobile_B':('p4_lamda_v5_B_n{}.json',[100,300,1000,5000]),'iot':('p4_iot_v3_n{}_std.json',[100,300,1000,99999])}
KARMS=['local','bk30','bk100','bk300','shrink','bk1000','bk3000','fedavg']; KV={'local':0,'bk30':30,'bk100':100,'bk300':300,'shrink':500,'bk1000':1000,'bk3000':3000,'fedavg':1e9}
HET=['prev_gap','feat_shift','cc_port','score_w1','disagree']; TR=['T_in','T_gap','T_diag']
rows=[]; ALL={}
for d,(pat,sup) in DOMS.items():
    ALL[d]={}
    for n in sup:
        if not os.path.exists(pat.format(n)): continue
        res=json.load(open(pat.format(n))); ALL[d][n]=res
        for s in res:
            H=s['H']; K=len(H['n'])
            for c in range(K):
                r=dict(dom=d,sup=n,seed=s['seed'],client=s['names'][c],logn=np.log(H['n'][c]),prev_gap=H['prev_gap'][c],feat_shift=H['feat_shift'][c],cc_port=-H['cc_port'][c],score_w1=H['score_w1'][c],disagree=H['disagree'][c],T_in=-H['T_in'][c],T_gap=H['T_gap'][c],T_diag=-H['T_diag'][c])
                for a in KARMS+['blend_val','fedavg_ft','cluster']: r['ba_'+a]=s['res'][a+'|local'][c]['ba']; r['fpr_'+a]=s['res'][a+'|local'][c]['fpr']; r['fnr_'+a]=s['res'][a+'|local'][c]['fnr']
                rows.append(r)
DF=pd.DataFrame(rows); DF.to_csv('p4_dial_dataset.csv',index=False)
def sn(n): return 'full' if n==99999 else str(n)
print('# COLLABORATION DIAL: mean BA / worst-client BA / worst FPR by k (w=n/(n+k)); k=0 local, k=inf FedAvg')
for d,S in ALL.items():
    for n,res in S.items():
        line=f'{d:9s} {sn(n):>5s}'
        for a in KARMS+['blend_val','cluster','fedavg_ft']:
            ba=np.mean([[r['ba'] for r in s['res'][a+'|local']] for s in res]); wb=np.mean([min(r['ba'] for r in s['res'][a+'|local']) for s in res]); line+=f' {a}:{ba:.3f}/{wb:.3f}'
        print(line)
print('\n# BEST FIXED k PER DOMAIN x SUPPORT (hindsight) and best-fixed vs shrink(k=500)')
for d,S in ALL.items():
    for n in S:
        D=DF[(DF.dom==d)&(DF.sup==n)]; m={a:D['ba_'+a].mean() for a in KARMS}; b=max(m,key=m.get); print(f'{d:9s} {sn(n):>5s} best {b}({m[b]:.3f}) shrink {m["shrink"]:.3f} local {m["local"]:.3f} fedavg {m["fedavg"]:.3f} val-blend {D.ba_blend_val.mean():.3f}')
FS={'het_only':HET,'support_only':['logn'],'het+support':['logn']+HET,'transfer_only':TR,'het+support+transfer':['logn']+HET+TR}
def fitpol(tr,cols,inter,alpha=3.0):
    X=tr[cols].values.astype(float); mu=X.mean(0); sd=X.std(0)+1e-9; Z=(X-mu)/sd
    if inter:
        l=(tr[['logn']].values-tr.logn.mean())/(tr.logn.std()+1e-9); Z=np.hstack([Z,Z*l])
    M={a:Ridge(alpha=alpha).fit(Z,tr['ba_'+a].values) for a in KARMS}; return cols,mu,sd,M,tr.logn.mean(),tr.logn.std()+1e-9,inter
def pick(te,P):
    cols,mu,sd,M,lm,ls,inter=P; Z=(te[cols].values.astype(float)-mu)/sd
    if inter: Z=np.hstack([Z,Z*((te[['logn']].values-lm)/ls)])
    return np.array(KARMS)[np.stack([M[a].predict(Z) for a in KARMS],1).argmax(1)]
def real(te,ch): return np.array([te.iloc[i]['ba_'+ch[i]] for i in range(len(te))])
print('\n# POLICY OVER THE DIAL (arms local,k=30..3000,fedavg), leave-one-client-out; value = mean test BA (not gain)')
pv={}
for d in ALL:
    D=DF[DF.dom==d].copy(); cl=D.client.unique(); out={}
    ref={a:D['ba_'+a].mean() for a in KARMS+['blend_val','cluster','fedavg_ft']}; orc=D[['ba_'+a for a in KARMS]].max(1).mean()
    out['always local']=ref['local']; out['always shrink(k=500)']=ref['shrink']; out['always fedavg']=ref['fedavg']; out['val-selected weight']=ref['blend_val']; out['oracle k (test)']=orc
    # LOCO-tuned global k
    v=[];ch=Counter()
    for c in cl:
        tr=D[D.client!=c]; te=D[D.client==c]; best=max(KARMS,key=lambda a:tr['ba_'+a].mean()); v.append(te['ba_'+best].values); ch[best]+=1
    out['LOCO-tuned global k']=np.concatenate(v).mean(); tuned=dict(ch)
    # per-support lookup
    v=[]
    for c in cl:
        tr=D[D.client!=c]; te=D[D.client==c]
        for n in te.sup.unique():
            best=max(KARMS,key=lambda a:tr[tr.sup==n]['ba_'+a].mean()); v.append(te[te.sup==n]['ba_'+best].values)
    out['support lookup (LOCO)']=np.concatenate(v).mean()
    for nm,cols in FS.items():
        for inter in [False,True]:
            if inter and nm in('support_only',): continue
            v=[]; cc=Counter()
            for c in cl:
                tr=D[D.client!=c]; te=D[D.client==c]; P=fitpol(tr,cols,inter); ch_=pick(te,P); v.append(real(te,ch_)); cc.update(ch_)
            out[f'ridge {nm}{" x support" if inter else ""}']=np.concatenate(v).mean()
    pv[d]=out; print(f'\n## {d}  (LOCO-tuned k choices {tuned})')
    for k,v in out.items(): print(f'   {k:36s} {v:.4f}')
print('\n# CROSS-DOMAIN: fixed k tuned on one domain, applied to the other (mean BA)')
for a_,b_ in [('mobile_A','iot'),('iot','mobile_A'),('mobile_B','iot'),('iot','mobile_B')]:
    tr=DF[DF.dom==a_]; te=DF[DF.dom==b_]; best=max(KARMS,key=lambda a:tr['ba_'+a].mean()); print(f'{a_}->{b_}: tuned k arm={best} BA {te["ba_"+best].mean():.4f} | target best fixed {max(KARMS,key=lambda a:te["ba_"+a].mean())} {max(te["ba_"+a].mean() for a in KARMS):.4f} | target shrink {te.ba_shrink.mean():.4f} | target val-blend {te.ba_blend_val.mean():.4f}')
print('\n# WORST-CLIENT COMPARISON (mean over seeds of min client BA / max client FPR / max client FNR) at each support')
for d,S in ALL.items():
    for n,res in S.items():
        line=f'{d:9s} {sn(n):>5s}'
        for a in ['local','shrink','blend_val','fedavg','cluster']:
            wb=np.mean([min(r['ba'] for r in s['res'][a+'|local']) for s in res]); wf=np.mean([max(r['fpr'] for r in s['res'][a+'|local']) for s in res]); wn=np.mean([max(r['fnr'] for r in s['res'][a+'|local']) for s in res]); line+=f' | {a}: {wb:.3f}/{wf:.3f}/{wn:.3f}'
        print(line)
