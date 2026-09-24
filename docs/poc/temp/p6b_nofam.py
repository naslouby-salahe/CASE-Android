"""P6 candidate B: complementary threat knowledge / unseen-family asymmetry across Android clients (LAMDA x AndroZoo).
Clients: play_e (Play<=2018), play_l (Play>=2019), anzhi, appchina (all single-market apps, package-grouped 60/20/20 split).
Family exposure is controlled: each client c hides the malware of family group G_c from its own training data; other clients keep it.
Unseen-family recall of client c: recall on test malware of families in G_c at the threshold set on c's own validation benign scores (FPR=alpha).
Aggregate outputs only. usage: p6_unseen_family.py SEED [N_TRAIN] [ALPHA]"""
import sys, json, hashlib, numpy as np, torch
sys.path.insert(0, '/home/naslouby/Projects/CASE-Android/docs/poc/temp')
from p3_engine import Eng, E_sig
SP = '/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/08b08ff8-6ce7-464d-95b4-658f18f24d2f/scratchpad/'
seed = int(sys.argv[1]); NT = int(sys.argv[2]) if len(sys.argv) > 2 else 6000; ALPHA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
rng = np.random.default_rng(seed)
d = np.load(SP + 'lamda.npz', allow_pickle=True)
X, y, yr, mk, nm, pkg, fam = d['X'], d['y'], d['year'], d['mk'], d['nm'], d['pkg'], d['fam']
CL = ['play_e', 'play_l', 'anzhi', 'appchina']
cl = np.full(len(y), -1)
one = nm == 1
cl[one & (mk == 'play.google.com') & (yr <= 2018)] = 0; cl[one & (mk == 'play.google.com') & (yr > 2018)] = 1
cl[one & (mk == 'anzhi')] = 2; cl[one & (mk == 'appchina')] = 3
h = np.array([int(hashlib.md5((p or str(i)).encode()).hexdigest()[:8], 16) % 100 for i, p in enumerate(pkg)])
part = np.where(h < 60, 0, np.where(h < 80, 1, 2))  # train/val/test by package
FAMS = ['dowgin', 'kuguo', 'airpush', 'smsreg', 'dnotua', 'gappusin', 'adwo', 'leadbolt', 'revmob', 'inmobi', 'youmi', 'plankton', 'zdtad', 'hiddad', 'domob', 'ewind']
# eligible (client, family) pairs: hidden family must have >=150 training malware in other clients, >=50 test malware overall
def cnt(f, c, p): return int(((cl == c) & (fam == f) & (y == 1) & (part == p)).sum())
perm = list(rng.permutation(FAMS)); G = [perm[i::4] for i in range(4)]
K = 4; C = []; hidden = []
def sub(idx, n):
    return idx if len(idx) <= n else rng.choice(idx, n, replace=False)
for c in range(K):
    tr = np.where((cl == c) & (part == 0))[0]; tr = tr[~((y[tr] == 1) & np.isin(fam[tr], G[c]))]   # family exposure control
    trfull = np.where((cl == c) & (part == 0))[0]
    va = sub(np.where((cl == c) & (part == 1) & (y == 0))[0], 3000); te_b = sub(np.where((cl == c) & (part == 2) & (y == 0))[0], 3000)
    tr = sub(tr, NT); trfull = sub(trfull, NT)
    C.append(dict(tr=tr, trfull=trfull, va=va, teb=te_b))
elig = {}
for c in range(K):
    elig[c] = [f for f in G[c] if sum(cnt(f, o, 0) for o in range(K) if o != c) >= 150 and sum(cnt(f, o, 2) for o in range(K)) >= 50]
def fam_test(c):   # unseen-family malware test rows (all clients' test split), <=1500 per family
    idx = []
    for f in elig[c]:
        r = np.where((cl >= 0) & (fam == f) & (y == 1) & (part == 2))[0]; idx.append(sub(r, 1500))
    return np.concatenate(idx) if idx else np.array([], int)
def known_test(c):
    r = np.where((cl == c) & (y == 1) & (part == 2) & ~np.isin(fam, G[c]))[0]; return sub(r, 3000)
def mkc(key):  # Eng client dicts
    out = []
    for c in range(K):
        i = C[c][key]; out.append(dict(Xtr=X[i].astype(np.float32), ytr=y[i], Xva=X[C[c]['va']].astype(np.float32), yva=y[C[c]['va']], Xte=X[C[c]['teb']].astype(np.float32), yte=y[C[c]['teb']]))
    return out
def run(key, arms):
    Cd = mkc(key); E = Eng(Cd, seed, FE=3, FR=30); P = {}
    E.lr = 1e-3
    LM = [E.fit(E.mlp(), *E.tr[c], 20) for c in range(K)]
    G_ = E.fed(); GP = E.fed(mu=0.05)
    cen = E.fit(E.mlp(), torch.cat([t[0] for t in E.tr]), torch.cat([t[1] for t in E.tr]), 20)
    FT = []
    for c in range(K):
        m = E.mlp(); E.setflat(m, E.flat(G_)); E.fit(m, *E.tr[c], 3, lr=5e-4); FT.append(m)
    return E, LM, G_, GP, cen, FT
def score(E, m, idx): return E.logit(m, torch.tensor(X[idx].astype(np.float32), device='cuda'))
def thr_from(E, m, c):  # client's own validation benign -> FPR=alpha threshold
    s = score(E, m, C[c]['va']); return np.quantile(s, 1 - ALPHA)

res = {}
def train_pair(remove):   # pooled + FedAvg where family set `remove` is removed from EVERY client (no client has it)
    Cd = []
    for c in range(K):
        i = C[c]['trfull']; i = i[~((y[i] == 1) & np.isin(fam[i], remove))]
        Cd.append(dict(Xtr=X[i].astype(np.float32), ytr=y[i], Xva=X[C[c]['va']].astype(np.float32), yva=y[C[c]['va']], Xte=X[C[c]['teb']].astype(np.float32), yte=y[C[c]['teb']]))
    E = Eng(Cd, seed, FE=3, FR=30); E.lr = 1e-3
    cen = E.fit(E.mlp(), torch.cat([t[0] for t in E.tr]), torch.cat([t[1] for t in E.tr]), 20)
    return E, cen, E.fed()
def score(E, m, idx): return E.logit(m, torch.tensor(X[idx].astype(np.float32), device='cuda'))
out = {'central_nofam': [], 'fedavg_nofam': [], 'central_peers1': [], 'central_peers_all': []}
for c in range(K):
    E, cen, fa = train_pair(G[c])
    ft = fam_test(c); kn = known_test(c)
    for nm_, m in [('central_nofam', cen), ('fedavg_nofam', fa)]:
        t = np.quantile(score(E, m, C[c]['va']), 1 - ALPHA)
        out[nm_].append(dict(unseen_recall=float((score(E, m, ft) > t).mean()) if len(ft) else float('nan'), known_recall=float((score(E, m, kn) > t).mean())))
    # dose-response: family visible only at ONE peer (the peer with most samples) vs at all peers
    for f_ in []: pass
res = out
json.dump(dict(seed=seed, N=NT, alpha=ALPHA, res=res), open(f'p6b_nofam_s{seed}_n{NT}.json', 'w'))
print({k: round(float(np.nanmean([x['unseen_recall'] for x in v])), 3) for k, v in res.items() if v})
