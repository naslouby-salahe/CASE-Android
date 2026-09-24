"""P5 family A/F: calibration contamination + small trusted-label budget. Frozen-scorer, score-level simulation on cached scores (p5_scores/).
Usage: python p5_budget.py DOMAIN seeds [alpha]. Contamination is INJECTED (rand/top/stealth); market prevalence (mobile hetnat) is natural.
Verification model: client k_c items of its calibration pool are verified by a trusted oracle (true label revealed)."""
import sys, json, numpy as np
DOM=sys.argv[1]; SEEDS=[int(s) for s in sys.argv[2].split(',')]; ALPHA=float(sys.argv[3]) if len(sys.argv)>3 else .05
N={'mobile':200,'mobsup':200,'nbaiot':200,'scidb':60}[DOM]; R=30; KS=[0,5,10,20,50]
def q(x,p): return float(np.quantile(x,min(max(p,0),1),method='higher'))
def trim_q(pool,eh,a):
    s=np.sort(pool); n=len(s); cut=int(np.ceil(n*eh)) if eh>0 else 0; s=s[:max(n-cut,1)]; return q(s,1-a)
def peer_eps(P):
    K=len(P); U=[p/(q(p,.5)+1e-12) for p in P]; eh=np.zeros(K)
    for c in range(K):
        ref=np.concatenate([U[j] for j in range(K) if j!=c]); tau=q(ref,.9); tc=np.mean(U[c]>tau); eh[c]=max(0.0,(tc-.1)/.9)
    return eh
def eb_post(m,k,pbar_fallback=0.):
    m=np.asarray(m,float); k=np.asarray(k,float); ok=k>0
    if ok.sum()==0: return np.zeros(len(m)),0
    pbar=m[ok].sum()/k[ok].sum(); r=m[ok]/k[ok]; kbar=k[ok].mean(); v=max(r.var()-pbar*(1-pbar)/kbar,1e-4)
    n0=float(np.clip(pbar*(1-pbar)/v-1,1,200)); return np.where(ok,(m+n0*pbar)/(k+n0),pbar),n0
def scenarios(K,prev,rng):
    S=[(f'hom{e}',np.full(K,e)) for e in [0,.05,.10,.20]]
    S.append(('hetlin',rng.permutation(np.linspace(0,.3,K))))
    if DOM in('mobile','mobsup'): S.append(('hetnat',np.clip(np.array(prev)*.3,0,.4)))
    return S
def run(seed):
    D=np.load(f'p5_scores/{DOM}_s{seed}.npz'); K=len(D['names']); rng=np.random.RandomState(seed*7+1)
    sc=[{k:D[f'{i}_{k}'] for k in ['cb','cm','tb','tm']} for i in range(K)]; tb=[s['tb'] for s in sc]; tm=[s['tm'] for s in sc]
    out=[]
    for ctype in ['rand','top','stealth']:
        for lab,eps in scenarios(K,D['prev'],rng):
            for k in KS:
                acc={}
                for r in range(R):
                    P=[];Z=[]
                    for c in range(K):
                        n1=int(round(N*eps[c])); cb=sc[c]['cb']; cm=np.sort(sc[c]['cm']); h=max(len(cm)//2,1)
                        pool=cm[:h] if ctype=='stealth' else (cm[-h:] if ctype=='top' else cm)
                        cl=rng.choice(cb,N-n1,replace=len(cb)<N-n1); ct=rng.choice(pool,n1,replace=len(pool)<n1) if n1>0 else np.array([])
                        x=np.concatenate([cl,ct]); z=np.r_[np.zeros(N-n1,bool),np.ones(n1,bool)]; pm=rng.permutation(N); P.append(x[pm]); Z.append(z[pm])
                    def verify(kc):
                        m=np.zeros(K); V=[]
                        for c in range(K):
                            if kc[c]==0: V.append(np.array([],int)); continue
                            ii=rng.choice(N,int(kc[c]),replace=False); V.append(ii); m[c]=Z[c][ii].sum()
                        return m,V
                    kc=np.full(K,k); m,V=verify(kc); ph=peer_eps(P); th={}
                    tl=np.array([q(p,1-ALPHA) for p in P]); th['LOCAL']=tl; th['GLOBAL']=np.full(K,tl.mean())
                    th['ORACLE-TRUE']=np.array([q(P[c][~Z[c]],1-ALPHA) if (~Z[c]).any() else tl[c] for c in range(K)])
                    th['ORACLE-TRIM']=np.array([trim_q(P[c],eps[c],ALPHA) for c in range(K)])
                    th['PEER-TRIM']=np.array([trim_q(P[c],ph[c],ALPHA) for c in range(K)])
                    if k>0:
                        cl_=[]
                        for c in range(K):
                            vb=P[c][V[c]][~Z[c][V[c]]]; cl_.append(q(vb,1-ALPHA) if len(vb) else tl[c])
                        th['CLEAN-K']=np.array(cl_)
                        th['CLEAN-K-GLOBAL']=np.full(K,th['CLEAN-K'].mean()); th['CLEAN-K-SHRINK']=.5*th['CLEAN-K']+.5*th['CLEAN-K'].mean()
                        th['LAB-LOCAL']=np.array([trim_q(P[c],m[c]/k,ALPHA) for c in range(K)])
                        pb=m.sum()/(k*K); th['LAB-POOL']=np.array([trim_q(P[c],pb,ALPHA) for c in range(K)])
                        eb,n0=eb_post(m,kc); th['LAB-EB']=np.array([trim_q(P[c],eb[c],ALPHA) for c in range(K)])
                        n0p=20.; ep_=(m+n0p*ph)/(k+n0p); th['PEER+LAB']=np.array([trim_q(P[c],ep_[c],ALPHA) for c in range(K)])
                        # refinements: drop verified malware + trim rest (V); tau-corrected trim (TAU: trimmed contaminants only partly sit above threshold)
                        def vpool(c):
                            keep=np.ones(N,bool); keep[V[c][Z[c][V[c]]]]=False; return P[c][keep]
                        eu=np.clip((eb*N-m)/np.maximum(N-k,1),0,None)
                        th['LAB-EB-V']=np.array([trim_q(vpool(c),eu[c],ALPHA) for c in range(K)])
                        t0=th['LAB-EB']; vm=[P[c][V[c]][Z[c][V[c]]] for c in range(K)]; nv=sum(len(v) for v in vm)
                        tau=(sum((v>t0[c]).sum() for c,v in enumerate(vm))/nv) if nv>=3 else 1.0
                        th['LAB-EB-TAU']=np.array([trim_q(P[c],eb[c]*tau,ALPHA) for c in range(K)])
                        th['LAB-EB-VTAU']=np.array([trim_q(vpool(c),eu[c]*tau,ALPHA) for c in range(K)])
                        th['HYB']=.5*th['LAB-EB-TAU']+.5*th['CLEAN-K-SHRINK']
                        th['CLEAN-K-SHRINK.75']=.25*th['CLEAN-K']+.75*th['CLEAN-K'].mean()
                        th['CLEAN-K-SHRINK.25']=.75*th['CLEAN-K']+.25*th['CLEAN-K'].mean()
                        # federated allocation of same total budget proportional to peer suspicion
                        w=ph+.05; ka=np.maximum(1,np.round(w/w.sum()*k*K)).astype(int); ka=np.minimum(ka,N); m2,V2=verify(ka); eb2,_=eb_post(m2,ka)
                        th['LAB-EB-ALLOC']=np.array([trim_q(P[c],eb2[c],ALPHA) for c in range(K)])
                        th['_eb_err']=np.abs(eb-eps); th['_loc_err']=np.abs(m/k-eps); th['_peer_err']=np.abs(ph-eps)
                    else: th['_peer_err']=np.abs(ph-eps)
                    ft={n:(np.array([np.mean(b>x) for b,x in zip(tb,t)]),np.array([np.mean(mm>x) for mm,x in zip(tm,t)])) for n,t in th.items() if not n.startswith('_')}
                    otpr=ft['ORACLE-TRUE'][1]
                    for name,t in th.items():
                        if name.startswith('_'): acc.setdefault(name,[]).append(float(np.mean(t))); continue
                        fpr,tpr=ft[name]; a=acc.setdefault(name,{})
                        succ=np.mean((fpr<=2*ALPHA)&(tpr>=.8*otpr)); fx=np.maximum(fpr-ALPHA,0).mean()
                        for kk,v in dict(tpr=tpr.mean(),wtpr=tpr.min(),fdev=np.abs(fpr-ALPHA).mean(),wfpr=fpr.max(),fpr=fpr.mean(),fsd=fpr.std(),succ=succ,fx=fx).items(): a.setdefault(kk,[]).append(float(v))
                        a.setdefault('tpr_c',[]).append(tpr); a.setdefault('fpr_c',[]).append(fpr)
                pol={}
                for n,v in acc.items():
                    if n.startswith('_'): pol[n]=float(np.mean(v)); continue
                    pol[n]={kk:(np.mean(vv,0).tolist() if kk.endswith('_c') else float(np.mean(vv))) for kk,vv in v.items()}
                out.append(dict(dom=DOM,seed=seed,ctype=ctype,scen=lab,k=k,alpha=ALPHA,eps=list(map(float,eps)),pol=pol))
    return out
res=[]
for s in SEEDS: res+=run(s); print(DOM,s,flush=True)
json.dump(res,open(f'p5_budget_{DOM}_a{ALPHA}.json','w'))
