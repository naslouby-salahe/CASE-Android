"""P6 CASE extension: calibration-only selective scoping (deferred claim D) + heterogeneity-scope check.
Package-grouped train/cal/test (60/20/20), 5 seeds, both directions. Policy: keep claims with score>=t; t chosen on CAL to reach target non-recurrence risk r*.
Scopes: pooled threshold vs per-indicator thresholds (local) vs shrunk. Compares persistence vs rich pooled logistic. Aggregate only."""
import sys, json, numpy as np, pandas as pd
sys.argv=[sys.argv[0],'/home/naslouby/Projects/datp-shared-data/raw/SELENE']
sys.path.insert(0,'.')
import selene_poc as S
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
a10,a14=S.load_pair(); ids=sorted(set(a10.sha256)&set(a14.sha256))
p10=a10[a10.sha256.isin(ids)].set_index('sha256').loc[ids].reset_index(); p14=a14[a14.sha256.isin(ids)].set_index('sha256').loc[ids].reset_index()
BOOLS=S.BOOLS
def build(src,tgt):
    g=src.package_name.fillna('<m>').astype(str).to_numpy(); Y=tgt[BOOLS].fillna(0).astype(int).to_numpy()
    xb=src[BOOLS].fillna(0).astype(float).to_numpy(); cc=list(dict.fromkeys(S.COUNT_MAP.values()))
    xc=np.log1p(src[cc].fillna(0).clip(lower=0).astype(float)).to_numpy(); xv=np.log1p(src[S.VOLUME].fillna(0).clip(lower=0).astype(float)).to_numpy()
    ci=np.argwhere(src[BOOLS].fillna(0).astype(int).to_numpy()==1); a,j=ci[:,0],ci[:,1]
    X=np.concatenate([np.eye(len(BOOLS))[j],xb[a],xc[a],xv[a]],1); return X,Y[a,j],j,g[a]
def pol_thr(s,y,target,minn=30):  # largest coverage with cal risk<=target (scores high=likely recurs); returns threshold
    o=np.argsort(-s); ys=y[o]; risk=np.cumsum(1-ys)/np.arange(1,len(ys)+1); ok=np.where((risk<=target)&(np.arange(1,len(ys)+1)>=minn))[0]
    return s[o][ok.max()] if len(ok) else np.inf
def ev(s,y,t): k=s>=t; return (float((1-y[k]).mean()) if k.any() else float('nan')), float(k.mean()), float(y[k].sum()/max(y.sum(),1))
out={}
for name,(src,tgt) in {'10to14':(p10,p14),'14to10':(p14,p10)}.items():
    X,y,j,g=build(src,tgt); out[name]={}
    for seed in range(5):
        gss=GroupShuffleSplit(1,test_size=.2,random_state=seed); tv,te=next(gss.split(X,y,g)); gss2=GroupShuffleSplit(1,test_size=.25,random_state=seed+100); tr_,ca_=next(gss2.split(X[tv],y[tv],g[tv])); tr,ca=tv[tr_],tv[ca_]
        m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=250,solver='liblinear')).fit(X[tr],y[tr])
        pi=np.array([(y[tr][j[tr]==k].sum()+1)/((j[tr]==k).sum()+2) for k in range(len(BOOLS))])
        sc={'persistence':(pi[j[ca]],pi[j[te]]),'rich':(m.predict_proba(X[ca])[:,1],m.predict_proba(X[te])[:,1])}
        for tgt_r in [.05,.10]:
            for mth,(sca,ste) in sc.items():
                # pooled
                t=pol_thr(sca,y[ca],tgt_r); r,cv,ret=ev(ste,y[te],t)
                # per-indicator
                keep=np.zeros(len(te),bool)
                for k in range(len(BOOLS)):
                    mc=j[ca]==k; mt=j[te]==k
                    if mc.sum()>=50: keep[mt]=ste[mt]>=pol_thr(sca[mc],y[ca][mc],tgt_r,minn=10)
                # worst-indicator realized risk (indicators with >=30 kept test claims)
                def worst(kp):
                    rs=[(1-y[te][(j[te]==k)&kp]).mean() for k in range(len(BOOLS)) if ((j[te]==k)&kp).sum()>=30]; return float(max(rs)) if rs else float('nan')
                kp_pool=ste>=t
                rl=float((1-y[te][keep]).mean()) if keep.any() else float('nan')
                out[name].setdefault(f'{mth}|r{tgt_r}',[]).append(dict(pool=dict(risk=r,cov=cv,ret=ret,worst=worst(kp_pool)),local=dict(risk=rl,cov=float(keep.mean()),ret=float(y[te][keep].sum()/y[te].sum()),worst=worst(keep))))
json.dump(out,open('p6_case_calibrated_policy_results.json','w'))
for d,v in out.items():
    print(d)
    for k,rows in v.items():
        f=lambda sc,q: np.nanmean([r[sc][q] for r in rows]); 
        print(f" {k:18s} pooled risk {f('pool','risk'):.3f} cov {f('pool','cov'):.3f} worstInd {f('pool','worst'):.3f} | local risk {f('local','risk'):.3f} cov {f('local','cov'):.3f} worstInd {f('local','worst'):.3f}")
