import json,glob,os,numpy as np,itertools,sys
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeClassifier
DOMS={'mobile_A':('p4_lamda_v5_A_n{}.json',[100,300,1000,5000]),'mobile_B':('p4_lamda_v5_B_n{}.json',[100,300,1000,5000]),'iot':('p4_iot_v3_n{}_std.json',[100,300,1000,99999])}
def load(d):
    pat,sup=DOMS[d]; out={}
    for n in sup:
        f=pat.format(n)
        if os.path.exists(f): out[n]=json.load(open(f))
    return out
ALL={d:load(d) for d in DOMS}
def sname(n): return 'full' if n==99999 else str(n)
def cs(res,a,k,fn):  # seed-level stat of client array
    return np.array([fn([r[k] for r in s['res'][a]]) for s in res])
ARMS=['local|local','central|local','fedavg|local','fedprox|local','fedavg_ft|local','cluster|local','shrink|local','tgraph|local','policy_valselect|local','oracle_arm|local']
print('# 1. MAIN TABLE (local-threshold scope): meanBA / macroF1 / worstBA / worstFPR / worstFNR / BA-CV / Brier')
for d,S in ALL.items():
    for n,res in S.items():
        print(f'\n## {d} support={sname(n)} seeds={len(res)} clients={len(res[0]["names"])}')
        for a in ARMS+['fedavg|fixed','local|fixed']:
            ba=cs(res,a,'ba',np.mean).mean(); f1=cs(res,a,'f1',np.mean).mean(); wb=cs(res,a,'ba',np.min).mean(); wf=cs(res,a,'fpr',np.max).mean(); wn=cs(res,a,'fnr',np.max).mean()
            cv=np.mean([np.std([r['ba'] for r in s['res'][a]])/np.mean([r['ba'] for r in s['res'][a]]) for s in res]); br=cs(res,a,'brier',np.mean).mean() if 'brier' in res[0]['res'][a][0] else float('nan')
            print(f'{a:26s} BA {ba:.3f} F1 {f1:.3f} wBA {wb:.3f} wFPR {wf:.3f} wFNR {wn:.3f} CV {cv:.3f} Brier {br:.3f}')
print('\n# 2. CONTRASTS (mean over clients of BA difference, seed-level mean ± se)')
for d,S in ALL.items():
    for n,res in S.items():
        line=f'{d:9s} {sname(n):>5s}'
        for a,b in [('fedavg|local','local|local'),('shrink|local','local|local'),('shrink|local','fedavg|local'),('central|local','fedavg|local'),('fedavg_ft|local','local|local'),('fedavg|local','fedavg|fixed'),('cluster|local','fedavg|local')]:
            x=cs(res,a,'ba',np.mean)-cs(res,b,'ba',np.mean); line+=f' | {a.split("|")[0]}-{b.split("|")[0]}{"(fix)" if "fixed" in b else ""} {x.mean():+.3f}±{x.std(ddof=1)/np.sqrt(len(x)):.3f}'
        print(line)
print('\n# 3. THRESHOLD SCOPES (arm: shrink and fedavg) BA / F1 / FPR / FNR / wFPR / wFNR / FPR-CV / thr-sd / val-n')
for d,S in ALL.items():
    for n,res in S.items():
        for arm in ['fedavg','shrink']:
            line=f'{d:9s} {sname(n):>5s} {arm:7s}'
            for sc in ['fixed','global','local','shrunk']:
                a=f'{arm}|{sc}'; R=lambda k,fn=np.mean:cs(res,a,k,fn).mean()
                fcv=np.mean([np.std([r['fpr'] for r in s['res'][a]])/(np.mean([r['fpr'] for r in s['res'][a]])+1e-9) for s in res]); ts=np.mean([np.std([r['thr'] for r in s['res'][a]]) for s in res]) if 'thr' in res[0]['res'][a][0] else float('nan')
                line+=f' | {sc}: {R("ba"):.3f}/{R("f1"):.3f}/{R("fpr"):.3f}/{R("fnr"):.3f}/{R("fpr",np.max):.3f}/{R("fnr",np.max):.3f}/{fcv:.2f}/{ts:.3f}'
            print(line)
# ---------- policy dataset
ARMSP=['local','fedavg','cluster','shrink','fedavg_ft']
rows=[]
for d,S in ALL.items():
    for n,res in S.items():
        for s in res:
            H=s['H']; K=len(H['n'])
            for c in range(K):
                r=dict(dom=d,sup=n,seed=s['seed'],client=s['names'][c],logn=np.log(H['n'][c]),prev_gap=H['prev_gap'][c],feat_shift=H['feat_shift'][c],cc_port=-H['cc_port'][c],score_w1=H['score_w1'][c],disagree=H['disagree'][c],T_in=-H['T_in'][c],T_gap=H['T_gap'][c],T_diag=-H['T_diag'][c])
                for a in ARMSP: r['ba_'+a]=s['res'][a+'|local'][c]['ba']
                rows.append(r)
import pandas as pd
DF=pd.DataFrame(rows); DF.to_csv('p4_policy_dataset.csv',index=False)
HET=['prev_gap','feat_shift','cc_port','score_w1','disagree']; TR=['T_in','T_gap','T_diag']
def feats(df,names,inter=False):
    X=df[names].values.astype(float)
    return X
def design(df,fs,mu=None,sd=None):
    X=df[fs['base']].values.astype(float)
    if mu is None: mu=X.mean(0); sd=X.std(0)+1e-9
    Z=(X-mu)/sd
    if fs['inter']:
        li=df[['logn']].values; lz=(li-fs['lmu'])/fs['lsd']
        Z=np.hstack([Z,Z*lz])
    return Z,mu,sd
SETS={'het_only':dict(base=HET,inter=False),'support_only':dict(base=['logn'],inter=False),'het+support':dict(base=['logn']+HET,inter=False),'het x support':dict(base=['logn']+HET,inter=True),
      'transfer_only':dict(base=TR,inter=False),'het+support+transfer':dict(base=['logn']+HET+TR,inter=False),'het x support+transfer':dict(base=['logn']+HET+TR,inter=True),
      'CASE-like(cc_port,feat_shift)+support':dict(base=['logn','cc_port','feat_shift'],inter=False),'score_w1+disagree+support':dict(base=['logn','score_w1','disagree'],inter=False)}
def fit_policy(tr,fs,alpha=3.0):
    fs=dict(fs); fs['lmu']=tr[['logn']].values.mean(); fs['lsd']=tr[['logn']].values.std()+1e-9
    Z,mu,sd=design(tr,fs); M={}
    for a in ARMSP[1:]: M[a]=Ridge(alpha=alpha).fit(Z,(tr['ba_'+a]-tr['ba_local']).values)
    return fs,mu,sd,M
def choose(te,fs,mu,sd,M):
    Z,_,_=design(te,fs,mu,sd); P=np.stack([np.zeros(len(te))]+[M[a].predict(Z) for a in ARMSP[1:]],1); return np.array(ARMSP)[P.argmax(1)]
def realized(te,ch): return np.array([te.iloc[i]['ba_'+ch[i]] for i in range(len(te))])
def evalpol(train_df,test_df,fs,split_by_client=True):
    f,mu,sd,M=fit_policy(train_df,fs); ch=choose(test_df,f,mu,sd,M); return realized(test_df,ch),ch
print('\n# 5. POLICY SELECTION, leave-one-client-out within domain. mean realized BA gain vs LOCAL (per client-run) ; fixed policies for reference')
res_pol={}
for d in DOMS:
    D=DF[DF.dom==d]; cl=D.client.unique()
    ref={a:(D['ba_'+a]-D['ba_local']).mean() for a in ARMSP[1:]}; orc=(D[['ba_'+a for a in ARMSP]].max(1)-D['ba_local']).mean()
    print(f'\n## {d}: rows={len(D)} | always: '+' '.join(f'{a} {v:+.4f}' for a,v in ref.items())+f' | oracle {orc:+.4f}')
    for nm,fs in SETS.items():
        g=[];cnt={a:0 for a in ARMSP}
        for c in cl:
            tr=D[D.client!=c]; te=D[D.client==c]; r,ch=evalpol(tr,te,fs); g.append(r-te['ba_local'].values)
            for a in ch: cnt[a]+=1
        g=np.concatenate(g); res_pol[(d,nm)]=g.mean(); print(f'  {nm:38s} {g.mean():+.4f}   choices '+' '.join(f'{a}:{v}' for a,v in cnt.items() if v))
print('\n## cross-domain transfer of the fitted policy (train domain -> test domain)')
for a_,b_ in [('mobile_A','iot'),('iot','mobile_A'),('mobile_B','iot'),('iot','mobile_B')]:
    tr=DF[DF.dom==a_]; te=DF[DF.dom==b_]; ref={a:(te['ba_'+a]-te['ba_local']).mean() for a in ARMSP[1:]}
    print(f'{a_}->{b_} always: '+' '.join(f'{a} {v:+.4f}' for a,v in ref.items()))
    for nm in ['support_only','het only'.replace(' ','_'),'het+support','het x support','het+support+transfer']:
        r,ch=evalpol(tr,te,SETS[nm]); from collections import Counter; print(f'   {nm:26s} {(r-te["ba_local"].values).mean():+.4f} {dict(Counter(ch))}')
print('\n## depth-2 tree on best arm (interpretable), LOCO, features het+support+transfer')
for d in DOMS:
    D=DF[DF.dom==d].copy(); D['best']=D[['ba_'+a for a in ARMSP]].values.argmax(1); fs=['logn']+HET+TR; gains=[]
    for c in D.client.unique():
        tr=D[D.client!=c]; te=D[D.client==c]; t=DecisionTreeClassifier(max_depth=2,min_samples_leaf=15,random_state=0).fit(tr[fs],tr['best']); ch=np.array(ARMSP)[t.predict(te[fs])]
        gains.append(realized(te,ch)-te['ba_local'].values)
    t=DecisionTreeClassifier(max_depth=2,min_samples_leaf=15,random_state=0).fit(D[fs],D['best'])
    from sklearn.tree import export_text
    print(f'{d} tree LOCO gain {np.concatenate(gains).mean():+.4f}\n'+export_text(t,feature_names=fs))
print('\n# 6. HETEROGENEITY x SUPPORT: mean benefit (BA_arm - BA_local) by support level x score_w1 tercile (terciles within support)')
for d in DOMS:
    D=DF[DF.dom==d].copy(); print(f'\n## {d}')
    for a in ['fedavg','shrink']:
        print(f'  arm {a}: rows=support, cols=score_w1 tercile low/mid/high (n per cell ~{len(D)//12})')
        for n in sorted(D.sup.unique()):
            S=D[D.sup==n]; q=S.score_w1.rank(pct=True); b=pd.cut(q,[0,1/3,2/3,1.0001],labels=['low','mid','high'],include_lowest=True)
            print(f'   {sname(n):>5s}: '+' '.join(f'{k}: {((S["ba_"+a]-S["ba_local"])[b==k]).mean():+.3f}' for k in ['low','mid','high']))
    for a in ['fedavg','shrink']:
        y=(D['ba_'+a]-D['ba_local']).values; Z=np.column_stack([np.ones(len(D)),(D.logn-D.logn.mean())/D.logn.std(),(D.score_w1-D.score_w1.mean())/D.score_w1.std()]); Z=np.column_stack([Z,Z[:,1]*Z[:,2]])
        rng=np.random.RandomState(0); cl=D.client.values; ucl=np.unique(cl); B=[]
        for _ in range(500):
            pick=rng.choice(ucl,len(ucl)); idx=np.concatenate([np.where(cl==c)[0] for c in pick]); B.append(np.linalg.lstsq(Z[idx],y[idx],rcond=None)[0])
        B=np.array(B); co=np.linalg.lstsq(Z,y,rcond=None)[0]
        print(f'  OLS {a}-local ~ logn + w1 + logn*w1 (z-scored; client-bootstrap 95% CI): '+' '.join(f'{n}={c:+.3f}[{np.percentile(B[:,i],2.5):+.3f},{np.percentile(B[:,i],97.5):+.3f}]' for i,(n,c) in enumerate(zip(['b0','logn','w1','logn*w1'],co))))
print('\n# 7. SINGLE-MEASURE spearman with benefit (blend-local, fedavg-local); per domain; measures are oriented so larger = more mismatch')
for d in DOMS:
    D=DF[DF.dom==d]; print(f'## {d}')
    for m in ['logn']+HET+TR:
        print(f'  {m:10s} blend {spearmanr(D[m],D.ba_shrink-D.ba_local)[0]:+.2f}  global {spearmanr(D[m],D.ba_fedavg-D.ba_local)[0]:+.2f}')
