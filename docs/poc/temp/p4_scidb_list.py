"""List SciDB dataset tree (metadata only). Usage: p4_scidb_list.py PATH"""
import sys,json,urllib.request
ID='0151eff3132541e2852a10ed65e0991f'
def ls(path,last=0,n=200):
    req=urllib.request.Request('https://www.scidb.cn/api/gin-sdb-filetree/public/file/childrenFileListByPath',data=json.dumps(dict(dataSetId=ID,version='V2',path=path,lastIndex=last,pageSize=n)).encode(),headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(req,timeout=60))['data']
if __name__=='__main__':
    d=ls(sys.argv[1]); print(len(d))
    for f in d: print({k:f[k] for k in ('label','path','dir','size') if k in f}, f.get('id'))
