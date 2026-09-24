"""C1 (calibration contamination) shared code: client builders (LAMDA markets, N-BaIoT devices, SciDB Pi devices), federated AE, scoring.
Clients: dict(Xtr benign train, Xcb benign calibration, Xcm malware calibration, Xtb benign test, Xtm malware test). Aggregate outputs only."""
import numpy as np, pandas as pd, hashlib, torch, os
SPD='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
dev='cuda'
def mobile(seed,cap_tr=3000,cap_cal=600,cap_te=2000):
    D=np.load(SPD+'lamda.npz'); X,y,mk,nm,pkg=D['X'],D['y'],D['mk'],D['nm'],D['pkg']
    CL=np.full(len(y),'',dtype=object)
    for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
    CL[(mk=='play.google.com')&(nm==1)]='play'; names=sorted(set(CL)-{''})
    def gs(p):
        h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32; return 0 if h<.6 else (1 if h<.75 else 2)
    grp=np.array([gs(p if p else str(i)) for i,p in enumerate(pkg)]); rng=np.random.RandomState(seed); C=[]; prev=[]
    def pick(ii,cap): return rng.choice(ii,cap,replace=False) if len(ii)>cap else ii
    for nv in names:
        idx=np.where(CL==nv)[0]; prev.append(float(y[idx].mean())); f=lambda s,l:idx[(grp[idx]==s)&(y[idx]==l)]
        C.append(dict(Xtr=X[pick(f(0,0),cap_tr)].astype(np.float32),Xcb=X[pick(f(1,0),cap_cal)].astype(np.float32),Xcm=X[pick(f(1,1),cap_cal)].astype(np.float32),Xtb=X[pick(f(2,0),cap_te)].astype(np.float32),Xtm=X[pick(f(2,1),cap_te)].astype(np.float32)))
    return C,names,True,prev
def _split(Xb,Xm,rng,cap_tr=None):
    ib=rng.permutation(len(Xb)); im=rng.permutation(len(Xm)); nb=len(ib); nm_=len(im)
    a,b=int(.6*nb),int(.75*nb); c,d=int(.6*nm_),int(.75*nm_)
    return dict(Xtr=Xb[ib[:a]],Xcb=Xb[ib[a:b]],Xtb=Xb[ib[b:]],Xcm=Xm[im[c:d]],Xtm=Xm[im[d:]])
def nbaiot(seed):
    D=np.load(SPD+'nbaiot.npz'); names=sorted(k[:-2] for k in D.files if k.endswith('_X')); rng=np.random.RandomState(seed); C=[]; prev=[]
    for n in names:
        X=D[n+'_X']; y=D[n+'_y']; X=np.sign(X)*np.log1p(np.abs(X)); Xb=np.unique(X[y==0],axis=0); Xm=X[y==1]; Xm=Xm[rng.permutation(len(Xm))[:8000]]; Xb=Xb[rng.permutation(len(Xb))[:8000]]
        C.append(_split(Xb,Xm,rng)); prev.append(float(D[n+'_prev']))
    A=np.concatenate([c['Xtr'] for c in C]); mu,sd=A.mean(0),A.std(0)+1e-6
    for c in C:
        for k in c: c[k]=((c[k]-mu)/sd).astype(np.float32)
    return C,names,False,prev
def scidb(seed):
    rng=np.random.RandomState(seed); C=[]; names=[]; prev=[]
    for i in range(8):
        d=pd.read_csv(SPD+f'iot/dev{i}.csv'); F=[c for c in d.columns if c!='label']; d['k']=d[F].round(10).apply(tuple,axis=1); d=d.drop_duplicates('k').drop(columns='k')
        X=d[F].values.astype(np.float32); y=d.label.values; C.append(_split(X[y==0],X[y>0],rng)); names.append(f'pi{i}'); prev.append(float((y>0).mean()))
    A=np.concatenate([c['Xtr'] for c in C]); mu,sd=A.mean(0),A.std(0)+1e-6
    for c in C:
        for k in c: c[k]=((c[k]-mu)/sd).astype(np.float32)
    return C,names,False,prev
def build(domain,seed): return {'mobile':mobile,'nbaiot':nbaiot,'scidb':scidb}[domain](seed)
class AE(torch.nn.Module):
    def __init__(s,d):
        super().__init__(); s.f=torch.nn.Sequential(torch.nn.Linear(d,128),torch.nn.ReLU(),torch.nn.Linear(128,32),torch.nn.ReLU(),torch.nn.Linear(32,128),torch.nn.ReLU(),torch.nn.Linear(128,d))
    def forward(s,x): return s.f(x)
def rec_err(m,X,binary):
    with torch.no_grad():
        X=torch.tensor(X,device=dev); o=m(X)
        e=torch.nn.functional.binary_cross_entropy_with_logits(o,X,reduction='none').mean(1) if binary else ((o-X)**2).mean(1)
    return e.cpu().numpy()
def train_fed_ae(C,binary,seed,rounds=40,ep=2,lr=2e-3,bs=128):
    torch.manual_seed(seed); d=C[0]['Xtr'].shape[1]; g=AE(d).to(dev); Xs=[torch.tensor(c['Xtr'],device=dev) for c in C]
    for r in range(rounds):
        sts=[];ws=[]
        for X in Xs:
            m=AE(d).to(dev); m.load_state_dict(g.state_dict()); opt=torch.optim.Adam(m.parameters(),lr=lr)
            for _ in range(ep):
                perm=torch.randperm(len(X),device=dev)
                for i in range(0,len(X),bs):
                    b=X[perm[i:i+bs]]; o=m(b); l=torch.nn.functional.binary_cross_entropy_with_logits(o,b) if binary else torch.nn.functional.mse_loss(o,b)
                    opt.zero_grad(); l.backward(); opt.step()
            sts.append({k:v.detach().clone() for k,v in m.state_dict().items()}); ws.append(len(X))
        w=np.array(ws)/sum(ws); g.load_state_dict({k:sum(wi*s[k] for wi,s in zip(w,sts)) for k in sts[0]})
    return g
