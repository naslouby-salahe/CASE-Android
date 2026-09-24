import json,glob,sys,numpy as np
n=sys.argv[1]
fs=sorted(glob.glob(f'p6_unseen_family_s*_n{n}_a0.05.json')); R=[json.load(open(f)) for f in fs]
print(len(R),'seeds n=',n)
arms=list(R[0]['res'])
def agg(a,key,fn):
    return [fn([x[key] for x in r['res'][a] if not np.isnan(x[key])]) for r in R]
loc=None
print(f"{'arm':24s} unseenMean  worstClient  knownRec  FPR   gapRecov(mean) gapRecov(worst)")
M={a:np.array(agg(a,'unseen_recall',np.mean)) for a in arms}; W={a:np.array(agg(a,'unseen_recall',np.min)) for a in arms}
for a in arms:
    k=np.array(agg(a,'known_recall',np.mean)); f=np.array(agg(a,'fpr',np.mean))
    g=(M[a]-M['local'])/(M['oracle_central_exposed']-M['local']); gw=(W[a]-W['local'])/(W['oracle_central_exposed']-W['local'])
    print(f"{a:24s} {M[a].mean():.3f}±{M[a].std():.3f}  {W[a].mean():.3f}±{W[a].std():.3f}  {k.mean():.3f}  {f.mean():.3f}  {g.mean():.2f}  {gw.mean():.2f}")
for a in ['central','fedavg_ft','blend_central50','fedprox']:
    print(a,'beats local mean unseen in',int((M[a]>M['local']).sum()),'/',len(R),'seeds; worst',int((W[a]>W['local']).sum()))
