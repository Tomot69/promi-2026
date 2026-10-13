import sys, io, json; sys.argv=['banc_rendu.py','--monde=chamade']; sys.path.insert(0,'.')
import banc_rendu as B
R=[]
for i in range(5):
    res, errs = B.passe(B.URL, ['chamade'])
    f={k:(v or {}).get('fnv') for k,v in res['chamade']['images'].items()}; R.append((res['chamade']['stable'], f)); print('passe', i, 'stable', res['chamade']['stable'], sorted(set(f.values()))[:3], flush=True)
d=[(i,k) for i in range(1,5) for k in R[0][1] if R[i][1][k]!=R[0][1][k]]
print('5 PASSES :', 'IDENTIQUES' if not d else '%d image(s) différente(s) %s' % (len(d), d[:8]), '· stables', [r[0] for r in R])
