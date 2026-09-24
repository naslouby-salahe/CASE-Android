"""P3 POC: heterogeneity-aware collaboration on natural app-market clients (LAMDA + AndroZoo markets).
Arms: central, local, FedAvg, FedProx, FedAvg+FT (personalized), cluster-FL, val-selected policy, threshold scopes.
Aggregate outputs only. Usage: python p3_lamda_collab_poc.py [A|B] [seeds]"""
import numpy as np, torch, json, sys, hashlib, time
from sklearn.metrics import roc_auc_score
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
CFG=sys.argv[1] if len(sys.argv)>1 else 'A'
SEEDS=[int(s) for s in (sys.argv[2].split(',') if len(sys.argv)>2 else ['0','1','2'])]
import os
FE=int(os.environ.get('FE',3)); FR=int(os.environ.get('FR',30)); NTR=int(os.environ.get('NTR',5000))
dev='cuda'
D=np.load(SP+'lamda.npz'); X,y,year,mk,nm,pkg=D['X'],D['y'],D['year'],D['mk'],D['nm'],D['pkg']
def client_of(i_mask):
    cl=np.full(len(y),'',dtype=object)
    for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']:
        cl[(mk==m)&(nm==1)]=m
    P=(mk=='play.google.com')&(nm==1)
    if CFG=='A': cl[P]='play'
    else:
        for a,b in [(2013,2014),(2016,2016),(2017,2017),(2018,2018),(2019,2021)]:
            cl[P&(year>=a)&(year<=b)]=f'play{a}-{b}'
    return cl
CL=client_of(None); names=sorted(set(CL)-{''}); K=len(names)
def gsplit(p,seed):  # package-grouped split, shared across clients
    h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32
    return 0 if h<.6 else (1 if h<.75 else 2)
def bal(yv,pr,thr):
    yh=pr>=thr; tp=((yh)&(yv==1)).sum(); tn=((~yh)&(yv==0)).sum(); P=(yv==1).sum(); N=(yv==0).sum()
    tpr=tp/max(P,1); tnr=tn/max(N,1); prec=tp/max(yh.sum(),1)
    f1m=(2*prec*tpr/max(prec+tpr,1e-9)); yh0=~yh; prec0=tn/max(yh0.sum(),1); f10=2*prec0*tnr/max(prec0+tnr,1e-9)
    return dict(ba=(tpr+tnr)/2,fpr=1-tnr,fnr=1-tpr,f1=(f1m+f10)/2)
def best_thr(yv,pr):
    ts=np.unique(np.quantile(pr,np.linspace(0.01,0.99,99)))
    return ts[int(np.argmax([bal(yv,pr,t)['ba'] for t in ts]))]
def mlp(): return torch.nn.Sequential(torch.nn.Linear(X.shape[1],128),torch.nn.ReLU(),torch.nn.Linear(128,1)).to(dev)
def tt(a): return torch.tensor(a,device=dev)
def fit(m,Xt,yt,ep,lr=1e-3,prox=None,gen=None):
    opt=torch.optim.Adam(m.parameters(),lr=lr); n=len(yt)
    g0=[p.detach().clone() for p in prox[0]] if prox else None
    for _ in range(ep):
        perm=torch.randperm(n,device=dev,generator=gen)
        for i in range(0,n,256):
            b=perm[i:i+256]; l=torch.nn.functional.binary_cross_entropy_with_logits(m(Xt[b]).squeeze(1),yt[b])
            if prox: l=l+prox[1]/2*sum(((p-q)**2).sum() for p,q in zip(m.parameters(),g0))
            opt.zero_grad(); l.backward(); opt.step()
    return m
def prob(m,Xt):
    with torch.no_grad(): return torch.sigmoid(m(Xt).squeeze(1)).cpu().numpy()
def avg(states,w):
    w=np.array(w)/sum(w); return [sum(wi*s[k] for wi,s in zip(w,states)) for k in range(len(states[0]))]
def setp(m,ps):
    for p,q in zip(m.parameters(),ps): p.data.copy_(q)
def fedtrain(tr,ep_loc,R,mu=0.0,clients=None,gen=None):
    clients=clients if clients is not None else list(range(K)); g=mlp()
    for r in range(R):
        sts=[];ws=[]
        for c in clients:
            m=mlp(); setp(m,list(g.parameters()))
            fit(m,tr[c][0],tr[c][1],ep_loc,prox=(list(g.parameters()),mu) if mu>0 else None,gen=gen)
            sts.append([p.detach().clone() for p in m.parameters()]); ws.append(len(tr[c][1]))
        setp(g,avg(sts,ws))
    return g
def run(seed):
    torch.manual_seed(seed); np.random.seed(seed); gen=torch.Generator(device=dev); gen.manual_seed(seed)
    rng=np.random.RandomState(seed)
    grp=np.array([gsplit(p if p else str(i),seed) for i,p in enumerate(pkg)])
    S={}
    for c,nmv in enumerate(names):
        idx=np.where(CL==nmv)[0]; out=[]
        for s,cap in [(0,NTR),(1,max(60,min(1500,NTR//3))),(2,4000)]:
            ii=idx[grp[idx]==s]
            if len(ii)>cap: ii=rng.choice(ii,cap,replace=False)
            out.append(ii)
        S[c]=out
    tr={c:(tt(X[S[c][0]].astype(np.float32)),tt(y[S[c][0]].astype(np.float32))) for c in range(K)}
    va={c:(tt(X[S[c][1]].astype(np.float32)),y[S[c][1]]) for c in range(K)}
    te={c:(tt(X[S[c][2]].astype(np.float32)),y[S[c][2]]) for c in range(K)}
    info={names[c]:dict(ntr=len(S[c][0]),nva=len(S[c][1]),nte=len(S[c][2]),prev_tr=float(y[S[c][0]].mean()),prev_te=float(y[S[c][2]].mean())) for c in range(K)}
    P={}  # arm -> {c:(val_probs,test_probs)}
    def store(arm,c,m): P.setdefault(arm,{})[c]=(prob(m,va[c][0]),prob(m,te[c][0]))
    # local
    LM={}
    for c in range(K):
        LM[c]=fit(mlp(),*tr[c],ep=20,gen=gen) if False else fit(mlp(),tr[c][0],tr[c][1],20,gen=gen); store('local',c,LM[c])
    # transfer matrix (AUC of local_i on val_j)
    T=np.zeros((K,K))
    for i in range(K):
        for j in range(K):
            pv=prob(LM[i],va[j][0]); T[i,j]=roc_auc_score(va[j][1],pv) if len(set(va[j][1]))>1 else np.nan
    # central
    Xc=torch.cat([tr[c][0] for c in range(K)]); yc=torch.cat([tr[c][1] for c in range(K)])
    cm=fit(mlp(),Xc,yc,20,gen=gen)
    for c in range(K): store('central',c,cm)
    G=fedtrain(tr,FE,FR,0,gen=gen)
    for c in range(K): store('fedavg',c,G)
    GP=fedtrain(tr,FE,FR,0.05,gen=gen)
    for c in range(K): store('fedprox',c,GP)
    # personalized: fedavg + local fine-tune
    for c in range(K):
        m=mlp(); setp(m,list(G.parameters())); fit(m,tr[c][0],tr[c][1],3,lr=5e-4,gen=gen); store('fedavg_ft',c,m)
    # cluster FL from train-only transfer matrix
    from scipy.cluster.hierarchy import linkage,fcluster
    from scipy.spatial.distance import squareform
    Ts=np.nan_to_num((T+T.T)/2,nan=.5); Dm=1-Ts; np.fill_diagonal(Dm,0)
    lab=fcluster(linkage(squareform(Dm,checks=False),'average'),t=2,criterion='maxclust')
    for g_ in set(lab):
        mem=[c for c in range(K) if lab[c]==g_]
        m=fedtrain(tr,FE,FR,0,clients=mem,gen=gen) if len(mem)>1 else LM[mem[0]]
        for c in mem: store('cluster',c,m)
    # ---- heterogeneity stats (train-only)
    pooled_prev=float(yc.mean().cpu()); prevs=np.array([info[n]['prev_tr'] for n in names])
    fm=np.array([X[S[c][0]].mean(0) for c in range(K)]); pm=fm.mean(0)
    def jsd(a,b):
        a=np.clip(a,1e-6,1-1e-6);b=np.clip(b,1e-6,1-1e-6); mm=(a+b)/2
        kl=lambda p,q:(p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q)))
        return float(np.mean(.5*kl(a,mm)+.5*kl(b,mm)))
    Jm=np.array([[jsd(fm[i],fm[j]) for j in range(K)] for i in range(K)])
    # ---- evaluation per arm/threshold scope
    def evalarm(arm,scope,shr=None):
        res=[]
        for c in range(K):
            pv,pt=P[arm][c]
            if scope=='fixed': thr=.5
            elif scope=='global': thr=best_thr(np.concatenate([va[k][1] for k in range(K)]),np.concatenate([P[arm][k][0] for k in range(K)]))
            elif scope=='local': thr=best_thr(va[c][1],pv)
            elif scope=='shrunk':
                tl=best_thr(va[c][1],pv); tg=best_thr(np.concatenate([va[k][1] for k in range(K)]),np.concatenate([P[arm][k][0] for k in range(K)]))
                w=len(pv)/(len(pv)+300); thr=w*tl+(1-w)*tg
            r=bal(te[c][1],pt,thr); r['auc']=roc_auc_score(te[c][1],pt); res.append(r)
        return res
    out={}
    for arm in P:
        for scope in (['fixed','global','local','shrunk'] if arm in('fedavg','central') else ['fixed','local']):
            out[f'{arm}|{scope}']=evalarm(arm,scope)
    # val-selected policy among collaboration arms (fixed thr .5 -> use val BA @best local thr)
    arms=['local','fedavg','fedavg_ft','cluster']
    sel=[];choice=[]
    for c in range(K):
        sc=[]
        for a in arms:
            pv=P[a][c][0]; sc.append(bal(va[c][1],pv,best_thr(va[c][1],pv))['ba'])
        a=arms[int(np.argmax(sc))]; choice.append(a)
        pv,pt=P[a][c]; r=bal(te[c][1],pt,best_thr(va[c][1],pv)); r['auc']=roc_auc_score(te[c][1],pt); sel.append(r)
    out['policy_valselect|local']=sel
    # oracle (test-best arm) for regret
    orc=[]
    for c in range(K):
        best=max((out[f'{a}|local'][c] for a in arms),key=lambda r:r['ba']); orc.append(best)
    out['oracle_arm|local']=orc
    return dict(seed=seed,names=names,info=info,T=T.tolist(),J=Jm.tolist(),prev=prevs.tolist(),cluster=lab.tolist(),choice=choice,res=out,pooled_prev=pooled_prev)
allr=[]
for s in SEEDS:
    t=time.time(); r=run(s); allr.append(r); print('seed',s,'done',round(time.time()-t),'s',flush=True)
json.dump(allr,open(f'p3_lamda_collab_poc_results_{CFG}_n{NTR}.json','w'))
# summary
arms=sorted(allr[0]['res'])
print(f'clients {allr[0]["names"]}')
print(f'{"arm|scope":28s} meanBA  worstBA  meanF1  meanFPR  FPRsd  worstFPR  meanFNR  AUC')
for a in arms:
    M=lambda k:np.mean([[r[k] for r in s['res'][a]] for s in allr])
    W=np.mean([min(r['ba'] for r in s['res'][a]) for s in allr]); WF=np.mean([max(r['fpr'] for r in s['res'][a]) for s in allr])
    SD=np.mean([np.std([r['fpr'] for r in s['res'][a]]) for s in allr])
    print(f'{a:28s} {M("ba"):.3f}  {W:.3f}   {M("f1"):.3f}   {M("fpr"):.3f}   {SD:.3f}  {WF:.3f}   {M("fnr"):.3f}  {M("auc"):.3f}')
