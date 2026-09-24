"""Shared engine for Phase-3 POCs: collaboration-scope arms, thresholds, gating diagnostics, robust aggregation,
cold start, abstention. Clients are dicts of numpy arrays: Xtr,ytr,Xva,yva,Xte,yte. Outputs are aggregate only."""
import numpy as np, torch
from sklearn.metrics import roc_auc_score
dev='cuda'
def tt(a): return torch.tensor(a,device=dev)
def bal(yv,pr,thr):
    yh=pr>=thr; tp=((yh)&(yv==1)).sum(); tn=((~yh)&(yv==0)).sum(); P=(yv==1).sum(); N=(yv==0).sum()
    tpr=tp/max(P,1); tnr=tn/max(N,1); prec=tp/max(yh.sum(),1)
    f1m=2*prec*tpr/max(prec+tpr,1e-9); yh0=~yh; prec0=tn/max(yh0.sum(),1); f10=2*prec0*tnr/max(prec0+tnr,1e-9)
    return dict(ba=float((tpr+tnr)/2),fpr=float(1-tnr),fnr=float(1-tpr),f1=float((f1m+f10)/2))
def best_thr(yv,pr):
    ts=np.unique(np.quantile(pr,np.linspace(0.01,0.99,99)))
    return ts[int(np.argmax([bal(yv,pr,t)['ba'] for t in ts]))]
def auc(yv,p): return float(roc_auc_score(yv,p)) if len(set(yv))>1 else float('nan')
class Eng:
    def __init__(s,C,seed,FE=3,FR=30,d=None):
        s.C=C;s.K=len(C);s.FE=FE;s.FR=FR;s.d=d or C[0]['Xtr'].shape[1];s.lr=1e-3
        s.gen=torch.Generator(device=dev); s.gen.manual_seed(seed); torch.manual_seed(seed)
        s.tr=[(tt(c['Xtr']),tt(c['ytr'].astype(np.float32))) for c in C]
        s.va=[tt(c['Xva']) for c in C]; s.te=[tt(c['Xte']) for c in C]
    def mlp(s): return torch.nn.Sequential(torch.nn.Linear(s.d,128),torch.nn.ReLU(),torch.nn.Linear(128,1)).to(dev)
    def fit(s,m,Xt,yt,ep,lr=None,prox=None):
        opt=torch.optim.Adam(m.parameters(),lr=lr or s.lr); n=len(yt); g0=[p.detach().clone() for p in prox[0]] if prox else None
        for _ in range(ep):
            perm=torch.randperm(n,device=dev,generator=s.gen)
            for i in range(0,n,256):
                b=perm[i:i+256]; l=torch.nn.functional.binary_cross_entropy_with_logits(m(Xt[b]).squeeze(1),yt[b])
                if prox: l=l+prox[1]/2*sum(((p-q)**2).sum() for p,q in zip(m.parameters(),g0))
                opt.zero_grad(); l.backward(); opt.step()
        return m
    def logit(s,m,X):
        with torch.no_grad(): return m(X).squeeze(1).cpu().numpy()
    @staticmethod
    def sig(z): return 1/(1+np.exp(-z))
    def flat(s,m): return torch.cat([p.detach().reshape(-1) for p in m.parameters()])
    def setflat(s,m,v):
        i=0
        for p in m.parameters(): n=p.numel(); p.data.copy_(v[i:i+n].view_as(p)); i+=n
    def fed(s,clients=None,mu=0.0,agg='mean',poison=None,ret_flags=False,FE=None,FR=None,attack='flip'):
        clients=list(range(s.K)) if clients is None else clients; g=s.mlp(); flags=np.zeros(len(clients)); dist=np.zeros(len(clients))
        for r in range(FR or s.FR):
            vs=[];ws=[]
            for c in clients:
                m=s.mlp(); s.setflat(m,s.flat(g)); Xt,yt=s.tr[c]
                if poison is not None and c==poison:
                    if attack=='flip': yt=1-yt
                    elif attack=='target': yt=torch.where(yt==1,torch.zeros_like(yt),yt)
                s.fit(m,Xt,yt,FE or s.FE,prox=(list(g.parameters()),mu) if mu>0 else None)
                v=s.flat(m)
                if poison is not None and c==poison and attack=='sign': v=s.flat(g)-3*(v-s.flat(g))
                vs.append(v); ws.append(len(yt))
            V=torch.stack(vs); dist+=(V-V.median(0).values).norm(dim=1).cpu().numpy()
            if agg=='mean': new=(V*torch.tensor(np.array(ws)/sum(ws),device=dev,dtype=torch.float32)[:,None]).sum(0)
            elif agg=='median': new=V.median(0).values; flags+=((V-new).abs().sum(1)).cpu().numpy()
            elif agg=='trimmed':
                k=1; S,idx=V.sort(0); new=S[k:len(vs)-k].mean(0)
                out=((idx<k)|(idx>=len(vs)-k)).float().mean(1).cpu().numpy(); flags+=out
            elif agg=='krum':
                D=torch.cdist(V,V)**2; f=max(1,(len(vs)-3)//2); sc=torch.stack([D[i][torch.arange(len(vs),device=dev)!=i].sort().values[:len(vs)-f-2].sum() for i in range(len(vs))])
                j=int(sc.argmin()); new=V[j]; flags[j]+=1  # krum selection count (lower flags = rejected more)
            s.setflat(g,new)
        s.last_dist=dist/(FR or s.FR)
        return (g,flags/(FR or s.FR)) if ret_flags else g
def run_arms(C,seed,FE=3,FR=30,k_blend=500,cfg=None):
    if cfg: FE=cfg['fed'][2]; FR=cfg['fed'][1]
    E=Eng(C,seed,FE,FR); K=E.K; P={}; logit={}
    lrL,epL=cfg['local'] if cfg else (1e-3,20); lrC,epC=cfg['central'] if cfg else (1e-3,20); lrF=cfg['fed'][0] if cfg else 1e-3
    def store(a,c,m): logit.setdefault(a,{})[c]=(E.logit(m,E.va[c]),E.logit(m,E.te[c]))
    E.lr=lrL; LM=[E.fit(E.mlp(),*E.tr[c],epL) for c in range(K)]
    for c in range(K): store('local',c,LM[c])
    T=np.zeros((K,K))
    for i in range(K):
        for j in range(K): T[i,j]=auc(C[j]['yva'],E.logit(LM[i],E.va[j]))
    LG={(j,i):(E.logit(LM[j],E.va[i]),E.logit(LM[j],E.te[i])) for j in range(K) for i in range(K)}
    for i in range(K):   # transferability-graph collaboration: logit ensemble of local models weighted by measured transfer to client i (self included)
        w=np.array([max(np.nan_to_num(T[j,i],nan=.5)-.5,0)**2 for j in range(K)]); w=w/w.sum() if w.sum()>0 else np.eye(K)[i]
        logit.setdefault('tgraph',{})[i]=(sum(w[j]*LG[(j,i)][0] for j in range(K)),sum(w[j]*LG[(j,i)][1] for j in range(K)))
    E.lr=lrC; cm=E.fit(E.mlp(),torch.cat([t[0] for t in E.tr]),torch.cat([t[1] for t in E.tr]),epC)
    for c in range(K): store('central',c,cm)
    E.lr=lrF; G=E.fed()
    for c in range(K): store('fedavg',c,G)
    GP=E.fed(mu=0.05)
    for c in range(K): store('fedprox',c,GP)
    for c in range(K):
        m=E.mlp(); E.setflat(m,E.flat(G)); E.fit(m,*E.tr[c],3,lr=0.5*lrF); store('fedavg_ft',c,m)
    from scipy.cluster.hierarchy import linkage,fcluster
    from scipy.spatial.distance import squareform
    Ts=np.nan_to_num((T+T.T)/2,nan=.5); Dm=1-Ts; np.fill_diagonal(Dm,0)
    lab=fcluster(linkage(squareform(Dm,checks=False),'average'),t=2,criterion='maxclust')
    for g_ in set(lab):
        mem=[c for c in range(K) if lab[c]==g_]; m=E.fed(clients=mem) if len(mem)>1 else LM[mem[0]]
        for c in mem: store('cluster',c,m)
    for c in range(K):   # shrinkage: logit blend local/fedavg, w=n/(n+k)
        n=len(C[c]['ytr']); w=n/(n+k_blend); lv,lt=logit['local'][c]; gv,gt=logit['fedavg'][c]
        logit.setdefault('shrink',{})[c]=(w*lv+(1-w)*gv,w*lt+(1-w)*gt)
    for k in [30,100,300,1000,3000]:   # collaboration dial: w=n/(n+k), k=0 local, k=inf FedAvg
        for c in range(K):
            n=len(C[c]['ytr']); w=n/(n+k); lv,lt=logit['local'][c]; gv,gt=logit['fedavg'][c]
            logit.setdefault(f'bk{k}',{})[c]=(w*lv+(1-w)*gv,w*lt+(1-w)*gt)
    for c in range(K):   # client-validated mixing weight
        lv,lt=logit['local'][c]; gv,gt=logit['fedavg'][c]; yv=C[c]['yva']; best=None
        for w in np.linspace(0,1,11):
            zv=w*lv+(1-w)*gv; pv=E_sig(zv); sc=bal(yv,pv,best_thr(yv,pv))['ba']-1e-4*w
            if best is None or sc>best[0]: best=(sc,w)
        w=best[1]; logit.setdefault('blend_val',{})[c]=(w*lv+(1-w)*gv,w*lt+(1-w)*gt)
    return E,logit,T,lab
def evaluate(C,logit,arms=None):
    K=len(C); out={}
    yv=[c['yva'] for c in C]; yt=[c['yte'] for c in C]
    for a in (arms or logit):
        pv={c:E_sig(logit[a][c][0]) for c in range(K)}; pt={c:E_sig(logit[a][c][1]) for c in range(K)}
        gthr=best_thr(np.concatenate(yv),np.concatenate([pv[c] for c in range(K)]))
        for scope in ['fixed','global','local','shrunk']:
            res=[]
            for c in range(K):
                tl=best_thr(yv[c],pv[c])
                thr={'fixed':.5,'global':gthr,'local':tl,'shrunk':(len(yv[c])/(len(yv[c])+300))*tl+(1-len(yv[c])/(len(yv[c])+300))*gthr}[scope]
                r=bal(yt[c],pt[c],thr); r['auc']=auc(yt[c],pt[c]); r['thr']=float(thr); r['brier']=float(np.mean((pt[c]-yt[c])**2)); res.append(r)
            out[f'{a}|{scope}']=res
    return out
def E_sig(z): return 1/(1+np.exp(-z))
def policies(C,logit):
    K=len(C); arms=['local','fedavg','fedavg_ft','cluster','shrink']; out={};choice=[]
    sel=[];orc=[]
    for c in range(K):
        yv=C[c]['yva']; yt=C[c]['yte']; sc=[]; tes=[]
        for a in arms:
            pv=E_sig(logit[a][c][0]); pt=E_sig(logit[a][c][1]); t=best_thr(yv,pv)
            sc.append(bal(yv,pv,t)['ba']); tes.append(bal(yt,pt,t))
        i=int(np.argmax(sc)); choice.append(arms[i]); sel.append(tes[i]); orc.append(max(tes,key=lambda r:r['ba']))
    out['policy_valselect|local']=sel; out['oracle_arm|local']=orc
    return out,choice
def hetero_stats(C,T):
    K=len(C); prev=np.array([c['ytr'].mean() for c in C]); pool=np.concatenate([c['ytr'] for c in C]).mean()
    fm=np.array([c['Xtr'].mean(0) for c in C]); pm=np.concatenate([c['Xtr'] for c in C]).mean(0)
    def jsd(a,b):
        a=np.clip(a,1e-6,1-1e-6);b=np.clip(b,1e-6,1-1e-6);m=(a+b)/2
        kl=lambda p,q:(p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q)))
        return float(np.mean(.5*kl(a,m)+.5*kl(b,m)))
    Jpool=[jsd(fm[i],pm) for i in range(K)]
    tin=[float(np.nanmean([T[j,i] for j in range(K) if j!=i])) for i in range(K)]
    return dict(n=[len(c['ytr']) for c in C],nvalpos=[int(c['yva'].sum()) for c in C],prev_gap=list(np.abs(prev-pool)),jsd_pool=Jpool,
                T_diag=[float(T[i,i]) for i in range(K)],T_in=tin,T_gap=[tin[i]-float(T[i,i]) for i in range(K)])

def extra_stats(C,logit):
    """Training/calibration-side quantities for collaboration-benefit prediction (no test data used)."""
    from scipy.stats import wasserstein_distance
    K=len(C); Xs=[c['Xtr'] for c in C]; ys=[c['ytr'] for c in C]
    def cdiff(X,y): return X[y==1].mean(0)-X[y==0].mean(0) if 0<y.sum()<len(y) else np.zeros(X.shape[1])
    dis=[];w1=[];ccp=[];fsh=[]
    for c in range(K):
        oth=[j for j in range(K) if j!=c]; Xo=np.concatenate([Xs[j] for j in oth]); yo=np.concatenate([ys[j] for j in oth])
        d1=cdiff(Xs[c],ys[c]); d2=cdiff(Xo,yo); ccp.append(float(d1@d2/(np.linalg.norm(d1)*np.linalg.norm(d2)+1e-12)))
        m1=Xs[c].mean(0); m2=Xo.mean(0); fsh.append(float(1-np.corrcoef(m1,m2)[0,1]) if m1.std()>0 and m2.std()>0 else 1.0)
        pl=E_sig(logit['local'][c][0]); pg=E_sig(logit['fedavg'][c][0]); dis.append(float(np.mean((pl>=.5)!=(pg>=.5)))); w1.append(float(wasserstein_distance(pl,pg)))
    return dict(disagree=dis,score_w1=w1,cc_port=ccp,feat_shift=fsh)
