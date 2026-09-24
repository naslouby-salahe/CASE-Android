"""Extras on market clients (config A, NTR=1000): (1) abstention P36, (2) robust aggregation vs honest heterogeneity P44, (3) cold start P39.
Usage: python p3_extras.py seeds"""
import numpy as np, sys, json, hashlib, time
from p3_engine import *
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
SEEDS=[int(s) for s in sys.argv[1].split(',')]; NTR=1000
D=np.load(SP+'lamda.npz'); X,y,year,mk,nm,pkg=D['X'],D['y'],D['year'],D['mk'],D['nm'],D['pkg']
CL=np.full(len(y),'',dtype=object)
for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
CL[(mk=='play.google.com')&(nm==1)]='play'; names=sorted(set(CL)-{''})
def gsplit(p,seed):
    h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32
    return 0 if h<.6 else (1 if h<.75 else 2)
def build(seed):
    rng=np.random.RandomState(seed); grp=np.array([gsplit(p if p else str(i),seed) for i,p in enumerate(pkg)]); C=[]
    for nv in names:
        idx=np.where(CL==nv)[0]; parts=[]
        for s,cap in [(0,NTR),(1,max(60,min(1500,NTR//3))),(2,4000)]:
            ii=idx[grp[idx]==s]
            if len(ii)>cap: ii=rng.choice(ii,cap,replace=False)
            parts.append(ii)
        C.append(dict(Xtr=X[parts[0]].astype(np.float32),ytr=y[parts[0]],Xva=X[parts[1]].astype(np.float32),yva=y[parts[1]],Xte=X[parts[2]].astype(np.float32),yte=y[parts[2]]))
    return C
def sel_bal(yt,p,keep):
    r=bal(yt[keep],p[keep],.5); return r['ba'],float((~np.isin(np.arange(len(yt)),np.where(keep)[0])).mean())
out=dict(abstain=[],robust=[],cold=[])
for seed in SEEDS:
    C=build(seed); K=len(C); t0=time.time()
    # ---------- (1) abstention on FedAvg and FedAvg+FT probs
    E,logit,T,lab=run_arms(C,seed)
    for arm in ['fedavg','fedavg_ft','local']:
        conf=lambda z:np.abs(E_sig(z)-.5)
        for cov in [0.9,0.8,0.6]:
            allv=np.concatenate([conf(logit[arm][c][0]) for c in range(K)]); gcut=np.quantile(allv,1-cov)
            for scope in ['global','client']:
                rs=[]
                for c in range(K):
                    cut=gcut if scope=='global' else np.quantile(conf(logit[arm][c][0]),1-cov)
                    pt=E_sig(logit[arm][c][1]); keep=conf(logit[arm][c][1])>=cut; yt=C[c]['yte']
                    if keep.sum()<20 or len(set(yt[keep]))<2: rs.append(dict(cov=float(keep.mean()),err=float((( pt[keep]>=.5)!=yt[keep]).mean()) if keep.sum() else 1,ba=np.nan,fnr=np.nan)); continue
                    b=bal(yt[keep],pt[keep],.5); rs.append(dict(cov=float(keep.mean()),err=float(((pt[keep]>=.5)!=yt[keep]).mean()),ba=b['ba'],fnr=b['fnr']))
                out['abstain'].append(dict(seed=seed,arm=arm,target_cov=cov,scope=scope,per_client=rs))
    print('abstain done',round(time.time()-t0),flush=True)
    # ---------- (2) robust aggregation: no attacker / one label-flip attacker
    for agg in ['mean','median','trimmed','krum']:
        for atk in [None,names.index('1mobile'),names.index('appchina'),names.index('play')]:
            g,fl=E.fed(agg=agg,poison=atk,ret_flags=True,FR=20)
            bas=[bal(C[c]['yte'],E_sig(E.logit(g,E.te[c])),.5)['ba'] for c in range(K)]
            out['robust'].append(dict(seed=seed,agg=agg,attacker=None if atk is None else names[atk],ba=bas,flags=list(map(float,fl))))
    print('robust done',round(time.time()-t0),flush=True)
    # ---------- (3) cold start (leave-one-client-out)
    fm=np.array([c['Xtr'].mean(0) for c in C])
    def jsd(a,b):
        a=np.clip(a,1e-6,1-1e-6);b=np.clip(b,1e-6,1-1e-6);m=(a+b)/2
        kl=lambda p,q:(p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))); return float(np.mean(.5*kl(a,m)+.5*kl(b,m)))
    rng=np.random.RandomState(seed)
    for h in range(K):
        O=[c for c in range(K) if c!=h]; Gh=E.fed(clients=O,FR=20); yv=C[h]['yva']; yt=C[h]['yte']
        near=sorted(O,key=lambda j:jsd(fm[h],fm[j]))[:3]; Gn=E.fed(clients=near,FR=20)
        for k in [20,100]:
            pos=np.where(yv==1)[0]; neg=np.where(yv==0)[0]
            sh=np.r_[rng.choice(pos,min(k//2,len(pos)),replace=False),rng.choice(neg,min(k//2,len(neg)),replace=False)]
            Xs=E.va[h][sh]; ys=yv[sh]; R={}
            zt=lambda m:E.logit(m,E.te[h]); zs=lambda m:E.logit(m,Xs)
            R['global|fixed']=bal(yt,E_sig(zt(Gh)),.5)
            R['global|kshot_thr']=bal(yt,E_sig(zt(Gh)),best_thr(ys,E_sig(zs(Gh))))
            R['global|ft']=(lambda m:bal(yt,E_sig(zt(m)),.5))(E.fit((lambda m:(E.setflat(m,E.flat(Gh)),m)[1])(E.mlp()),Xs,torch.tensor(ys.astype(np.float32),device=dev),20,lr=5e-4))
            R['nearest3|fixed']=bal(yt,E_sig(zt(Gn)),.5)
            R['nearest3|kshot_thr']=bal(yt,E_sig(zt(Gn)),best_thr(ys,E_sig(zs(Gn))))
            # transferability routing: source local models scored on k shots
            LM=[E.fit(E.mlp(),*E.tr[j],20) for j in O]; sc=[auc(ys,E.logit(m,Xs)) for m in LM]
            top=[O[i] for i in np.argsort(sc)[::-1][:3]]; Gt=E.fed(clients=top,FR=20)
            R['route3|fixed']=bal(yt,E_sig(zt(Gt)),.5); R['route3|kshot_thr']=bal(yt,E_sig(zt(Gt)),best_thr(ys,E_sig(zs(Gt))))
            R['local_kshot']=bal(yt,E_sig(zt(E.fit(E.mlp(),Xs,torch.tensor(ys.astype(np.float32),device=dev),40))),.5)
            out['cold'].append(dict(seed=seed,client=names[h],k=k,route=[names[i] for i in top],near=[names[i] for i in near],R=R))
        print('cold',names[h],round(time.time()-t0),flush=True)
json.dump(out,open(f'p3_extras_results_s{sys.argv[1].replace(",","-")}.json','w'))
