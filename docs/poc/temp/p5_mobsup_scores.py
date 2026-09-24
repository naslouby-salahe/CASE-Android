"""P5: supervised FedAvg MLP scorer for LAMDA app-market clients (score = malware logit). Same threshold-calibration mechanism as AE domains.
Client = single-market app (natural site key). Package-grouped 60/15/25 splits. Saves cb/cm/tb/tm scores in p5_scores/mobsup_s{seed}.npz"""
import numpy as np, hashlib, torch, sys
from sklearn.metrics import roc_auc_score
SPD='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'; dev='cuda'
D=np.load(SPD+'lamda.npz'); X,y,mk,nm,pkg=D['X'],D['y'],D['mk'],D['nm'],D['pkg']
CL=np.full(len(y),'',dtype=object)
for m in ['anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']: CL[(mk==m)&(nm==1)]=m
CL[(mk=='play.google.com')&(nm==1)]='play'; names=sorted(set(CL)-{''})
class MLP(torch.nn.Module):
    def __init__(s,d): super().__init__(); s.f=torch.nn.Sequential(torch.nn.Linear(d,128),torch.nn.ReLU(),torch.nn.Linear(128,1))
    def forward(s,x): return s.f(x).squeeze(-1)
def sc(m,A):
    with torch.no_grad(): return m(torch.tensor(A.astype(np.float32),device=dev)).cpu().numpy()
for seed in [int(s) for s in sys.argv[1].split(',')]:
    def gs(p):
        h=int(hashlib.md5((p+str(seed)).encode()).hexdigest()[:8],16)/2**32; return 0 if h<.6 else (1 if h<.75 else 2)
    grp=np.array([gs(p if p else str(i)) for i,p in enumerate(pkg)]); rng=np.random.RandomState(seed); C=[]; prev=[]
    def pick(ii,cap): return rng.choice(ii,cap,replace=False) if len(ii)>cap else ii
    for nv in names:
        idx=np.where(CL==nv)[0]; prev.append(float(y[idx].mean())); f=lambda s,l:idx[(grp[idx]==s)&(y[idx]==l)]
        tr=np.r_[pick(f(0,0),3000),pick(f(0,1),3000)]
        C.append(dict(tr=tr,cb=pick(f(1,0),600),cm=pick(f(1,1),600),tb=pick(f(2,0),2000),tm=pick(f(2,1),2000)))
    torch.manual_seed(seed); g=MLP(X.shape[1]).to(dev); data=[(torch.tensor(X[c['tr']].astype(np.float32),device=dev),torch.tensor(y[c['tr']].astype(np.float32),device=dev)) for c in C]
    for r in range(30):
        sts=[];ws=[]
        for Xc,yc in data:
            m=MLP(X.shape[1]).to(dev); m.load_state_dict(g.state_dict()); opt=torch.optim.Adam(m.parameters(),lr=2e-3)
            for _ in range(2):
                perm=torch.randperm(len(Xc),device=dev)
                for i in range(0,len(Xc),128):
                    b=perm[i:i+128]; l=torch.nn.functional.binary_cross_entropy_with_logits(m(Xc[b]),yc[b]); opt.zero_grad(); l.backward(); opt.step()
            sts.append({k:v.detach().clone() for k,v in m.state_dict().items()}); ws.append(len(Xc))
        w=np.array(ws)/sum(ws); g.load_state_dict({k:sum(wi*s[k] for wi,s in zip(w,sts)) for k in sts[0]})
    d={}; auc=[]
    for i,c in enumerate(C):
        for k in ['cb','cm','tb','tm']: d[f'{i}_{k}']=sc(g,X[c[k]])
        auc.append(roc_auc_score(np.r_[np.zeros(len(d[f'{i}_tb'])),np.ones(len(d[f'{i}_tm']))],np.r_[d[f'{i}_tb'],d[f'{i}_tm']]))
    d['names']=np.array(names); d['prev']=np.array(prev); np.savez(f'p5_scores/mobsup_s{seed}.npz',**d); print(seed,np.round(auc,3),flush=True)
