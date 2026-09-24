"""P6 candidate: membership-inference leakage of federated Android malware detectors, by client (LAMDA markets). Loss-threshold MIA (Yeom), AUC members vs same-client non-members.
usage: p6_mia.py SEED N_TRAIN. Aggregate only."""
import sys,json,hashlib,numpy as np,torch
sys.path.insert(0,'.')
from p3_engine import Eng
from sklearn.metrics import roc_auc_score
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/08b08ff8-6ce7-464d-95b4-658f18f24d2f/scratchpad/'
seed=int(sys.argv[1]); NT=int(sys.argv[2]); rng=np.random.default_rng(seed)
d=np.load(SP+'lamda.npz',allow_pickle=True); X,y,yr,mk,nm,pkg=d['X'],d['y'],d['year'],d['mk'],d['nm'],d['pkg']
cl=np.full(len(y),-1); one=nm==1
cl[one&(mk=='play.google.com')&(yr<=2018)]=0; cl[one&(mk=='play.google.com')&(yr>2018)]=1; cl[one&(mk=='anzhi')]=2; cl[one&(mk=='appchina')]=3
C=[];mem=[];non=[]
for c in range(4):
    idx=rng.permutation(np.where(cl==c)[0]); tr=idx[:NT]; ho=idx[NT:NT+NT]  # non-members: same-market held-out draws
    C.append(dict(Xtr=X[tr].astype(np.float32),ytr=y[tr],Xva=X[ho[:200]].astype(np.float32),yva=y[ho[:200]],Xte=X[ho[:200]].astype(np.float32),yte=y[ho[:200]])); mem.append(tr); non.append(ho)
E=Eng(C,seed,FE=3,FR=30); E.lr=1e-3
def loss(m,idx):
    Xt=torch.tensor(X[idx].astype(np.float32),device='cuda'); yt=torch.tensor(y[idx].astype(np.float32),device='cuda')
    with torch.no_grad(): return torch.nn.functional.binary_cross_entropy_with_logits(m(Xt).squeeze(1),yt,reduction='none').cpu().numpy()
def mia(m,c):
    lm,ln=loss(m,mem[c]),loss(m,non[c]); return float(roc_auc_score(np.r_[np.ones(len(lm)),np.zeros(len(ln))],-np.r_[lm,ln]))
LM=[E.fit(E.mlp(),*E.tr[c],20) for c in range(4)]; GA=E.fed(); cen=E.fit(E.mlp(),torch.cat([t[0] for t in E.tr]),torch.cat([t[1] for t in E.tr]),20)
res={'local':[mia(LM[c],c) for c in range(4)],'fedavg':[mia(GA,c) for c in range(4)],'central':[mia(cen,c) for c in range(4)]}
# DP-flavoured cheap defence: weight decay-free noise on output is skipped; report generalisation gap too
res['n_train']=NT; res['seed']=seed
json.dump(res,open(f'p6_mia_s{seed}_n{NT}.json','w')); print(NT,seed,{k:np.round(v,3).tolist() for k,v in res.items() if isinstance(v,list)})
