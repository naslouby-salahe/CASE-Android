# P3-A: join LAMDA hashes with AndroZoo markets; aggregate counts only.
import pandas as pd, gzip, json, collections
R='/home/naslouby/Projects/datp-shared-data/raw/'
m=pd.read_csv(R+'LAMDA/metadata.csv',usecols=['sha256','label','year','family'])
m['sha256']=m.sha256.str.upper()
S=set(m.sha256)
rows=[]
for ch in pd.read_csv(R+'AndroZoo/latest.csv.gz',usecols=['sha256','pkg_name','markets','dex_date','apk_size'],chunksize=500000):
    ch['sha256']=ch.sha256.str.upper()
    rows.append(ch[ch.sha256.isin(S)])
z=pd.concat(rows).drop_duplicates('sha256')
z.to_parquet('/tmp/claude-1000/-home-naslouby-Projects-CASE-Android/ad3912f9-9f1e-4eb3-8f67-ccf1d892f2ed/scratchpad/lamda_markets.parquet')
j=m.merge(z,on='sha256',how='left')
print(len(m),len(z),j.markets.notna().sum())
j['mk']=j.markets.fillna('NA').str.split('|')
ex=j.explode('mk')
t=ex.groupby('mk').agg(n=('label','size'),mal=('label','mean')).sort_values('n',ascending=False)
print(t.head(25))
single=j[j.mk.str.len()==1].copy(); single['mk1']=single.mk.str[0]
print(single.groupby('mk1').agg(n=('label','size'),mal=('label','mean'),y0=('year','min'),y1=('year','max')).sort_values('n',ascending=False))
json.dump({'n':len(m),'joined':int(j.markets.notna().sum())},open('p3_lamda_markets_summary.json','w'))
