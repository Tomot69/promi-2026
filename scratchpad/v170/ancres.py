import sys, math; sys.path.insert(0,'scratchpad/v146/trace')
import numpy as np, squelette as S, squelettes_promilate as SP
from fontTools.ttLib import TTFont
F=TTFont('Polices Promi/PromiLate-Regular.otf'); cm=F.getBestCmap()
for ch in sys.argv[1]:
    D=SP.DESSINS[ch]; cts=S.contours(F,cm[ord(ch)]); img,x0,y1=S.image(cts); U=S.U; H,W=img.shape
    def dans(p):
        xi,yi=int(round((p[0]-x0)/U)),int(round((y1-p[1])/U)); return 0<=yi<H and 0<=xi<W and img[yi,xi]
    def bord(p,v,mx=500):
        if not dans(p): return 0
        d=0
        while d<mx and dans(p+v*(d+1)): d+=1
        return d
    lists=[[D['n'][a]]+list(m)+[D['n'][b]] for a,m,b in D.get('e',[])] if 'e' in D else [D['boucle']]
    for L in lists:
        out=[]
        for i,p in enumerate(L):
            p=np.array(p,float); a=np.array(L[max(0,i-1)],float); b=np.array(L[min(len(L)-1,i+1)],float); t=b-a; t/=max(np.hypot(*t),1e-9); n=np.array([-t[1],t[0]])
            out.append('%s%d,%d:%s%d/%d'%('' ,p[0],p[1],'' if dans(p) else 'HORS ',bord(p,n),bord(p,-n)))
        print(ch,' | '.join(out))
