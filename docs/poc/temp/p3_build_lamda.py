# Build market-annotated LAMDA cache (features var_thresh_0.01, 920 feats). Aggregate outputs only in repo; cache in scratchpad.
import pandas as pd, numpy as np, glob, os
R='/home/naslouby/Projects/datp-shared-data/raw/LAMDA/var_thresh_0.01/'
SP='/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/'
dfs=[]
for f in sorted(glob.glob(R+'*/*.parquet')):
    d=pd.read_parquet(f); d['split']='train' if 'train' in f else 'test'; dfs.append(d)
d=pd.concat(dfs,ignore_index=True)
fc=[c for c in d.columns if c.startswith('feat_')]
z=pd.read_parquet(SP+'lamda_markets.parquet'); z['hash']=z.sha256.str.upper()
d['hash']=d['hash'].str.upper()
d=d.merge(z[['hash','markets','pkg_name']],on='hash',how='left')
d['nm']=d.markets.fillna('NA').str.count(r'\|')+1
d['mk']=d.markets.str.split('|').str[0]
d['year']=d.year_month.str[:4].astype(int)
print(len(d),d.markets.notna().mean(),d.nm.value_counts().head())
X=d[fc].values.astype(np.uint8)
np.savez_compressed(SP+'lamda.npz',X=X,y=d.label.values.astype(np.int8),year=d.year.values,mk=d.mk.fillna('NA').values.astype(str),nm=d.nm.values,pkg=d.pkg_name.fillna('').values.astype(str),fam=d.family.fillna('').values.astype(str),ym=d.year_month.values.astype(str))
sub=d[d.nm==1]
print(sub.groupby(['mk']).apply(lambda g:pd.Series({'n':len(g),'mal':g.label.mean(),'nmal':g.label.sum(),'nben':(1-g.label).sum()})).sort_values('n',ascending=False).head(15))
print(pd.crosstab(sub[sub.mk=='play.google.com'].year,sub[sub.mk=='play.google.com'].label))
