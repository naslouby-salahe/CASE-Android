"""Dataset audit for the held-out-family study (LAMDA families per market, N-BaIoT attack files per device, SciDB conditions per device)."""
import numpy as np, pandas as pd, os, glob, json
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
out={}
D=np.load(SP+'lamda.npz'); mk,nm,y,fam,pkg,ym=D['mk'],D['nm'],D['y'],D['fam'],D['pkg'],D['ym']
top=['play.google.com','anzhi','appchina','PlayDrone','slideme','1mobile','angeeks']
m=(nm==1)&np.isin(mk,top)&(y==1); df=pd.DataFrame(dict(mk=mk[m],fam=fam[m]))
print('LAMDA malware rows in 7 markets',len(df),' distinct families',df.fam.nunique())
vc=df.fam.value_counts(); print('top 15 families:',vc.head(15).to_dict())
print('share SINGLETON/empty/unknown:',{k:round(float(vc.get(k,0)/len(df)),3) for k in ['SINGLETON','','unknown','none']}, ' top-5 concentration',round(float(vc.head(5).sum()/len(df)),3))
tab=pd.crosstab(df.fam,df.mk); tab=tab.loc[vc.index[:40]]
ok=tab[(tab>=150).sum(1)>=4]; print('families with >=150 samples in >=4 markets:',len(ok)); print(ok)
print('malware family purity check: rows with family=="benign" among label 1:',int((fam[(y==1)]=='benign').sum()))
out['lamda_families_multi_market']=ok.to_dict()
# N-BaIoT
R='/home/naslouby/Projects/datp-shared-data/raw/N-BaIoT/'
print('\nN-BaIoT files per device:')
for d in sorted(x for x in os.listdir(R) if os.path.isdir(R+x)):
    ty=sorted(os.path.basename(f)[:-4] for f in glob.glob(R+d+'/*_attacks/*.csv')); nb=sum(1 for _ in open(R+d+'/benign_traffic.csv'))-1
    print(f'  {d:42s} benign {nb:6d} attack types {len(ty)}: {ty}')
# SciDB
print('\nSciDB conditions per device (raw rows / unique windows):')
for i in range(8):
    d=pd.read_csv(SP+f'iot/dev{i}.csv'); F=[c for c in d.columns if c!='label']; d['k']=d[F].round(10).apply(tuple,axis=1); u=d.drop_duplicates('k')
    print(f'  dev{i}',dict(zip(sorted(d.label.unique()),[f"{int((d.label==l).sum())}/{int((u.label==l).sum())}" for l in sorted(d.label.unique())])))
