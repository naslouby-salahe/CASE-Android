"""POC: does linking the same package across markets (anchor features from another market) improve malware detection in the querying market?
Rows with a counterpart in another client market; pkg-grouped 5-fold CV. Variants: LOCAL x | +anchor features (diff) | +anchor verdict."""
import numpy as np, pandas as pd, json
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
D=np.load(SP+'lamda.npz'); X,y,mk,nm,pkg=D['X'],D['y'],D['mk'],D['nm'],D['pkg']
top=['play.google.com','anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']
m=(nm==1)&np.isin(mk,top)&(pkg!=''); idx=np.where(m)[0]; df=pd.DataFrame(dict(i=idx,mk=mk[idx],pkg=pkg[idx],y=y[idx]))
nmk=df.groupby('pkg').mk.nunique(); df=df[df.pkg.isin(nmk[nmk>1].index)].reset_index(drop=True)
rows=[]
for p,s in df.groupby('pkg'):
    for _,r in s.iterrows():
        o=s[s.mk!=r.mk]; a=o.iloc[0]; rows.append((r.i,a.i,r.pkg,r.y,a.y,r.mk))
R=pd.DataFrame(rows,columns=['i','a','pkg','y','ya','mk']); print('query rows with a cross-market anchor:',len(R),' conflict share',round(float((R.y!=R.ya).mean()),3),' malware share',round(float(R.y.mean()),3))
xi=X[R.i.values].astype(np.float32); xa=X[R.a.values].astype(np.float32); yy=R.y.values; ya=R.ya.values; grp=R.pkg.values
sets={'LOCAL x':np.hstack([xi]),'x + anchor diff':np.hstack([xi,xi-xa]),'x + anchor diff + anchor verdict':np.hstack([xi,xi-xa,ya[:,None].astype(np.float32)]),'anchor verdict only':ya[:,None].astype(np.float32)}
conf=(R.y!=R.ya).values
res={}
for name,F in sets.items():
    for mname,mk_ in [('logreg',lambda:LogisticRegression(C=0.3,max_iter=300)),('hgb',lambda:HistGradientBoostingClassifier(max_iter=150,learning_rate=0.1))]:
        oof=np.zeros(len(yy))
        for tr,te in GroupKFold(5).split(F,yy,grp):
            mdl=mk_().fit(F[tr],yy[tr]); oof[te]=mdl.predict_proba(F[te])[:,1]
        res[(name,mname)]=(roc_auc_score(yy,oof),roc_auc_score(yy[conf],oof[conf]) if len(set(yy[conf]))>1 else np.nan)
        print(f'{name:34s} {mname:6s} AUC all {res[(name,mname)][0]:.3f} | conflict subset {res[(name,mname)][1]:.3f}',flush=True)
# per-market local AUC
print('per-market malware share:',R.groupby('mk').y.mean().round(2).to_dict())
