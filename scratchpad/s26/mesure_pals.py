# -*- coding: utf-8 -*-
"""LES TROIS PALETTES NEUVES, MESUREES COMME LES VINGT ET UNE AUTRES.
   · ecart perceptuel entre les quatre tons : le plus petit DeltaE 2000 des six paires
   · distance a chaque palette existante : moyenne symetrique des plus proches (DeltaE 2000)"""
import re,io,json,sys,statistics as st
sys.path.insert(0,'scratchpad/s26')
from palettes import interne, dist
S=io.open('app.html',encoding='utf-8').read()
P=json.loads(re.sub(r'(\w+):',r'"\1":',re.search(r'var PALS=(\{.*?\});',S,re.S).group(1)).replace("'",'"'))
NEUVES=['truculent','petulant','fantasque']
ANC=[k for k in P if k not in NEUVES]
print("%d palettes (%d anciennes + %d neuves)\n"%(len(P),len(ANC),len(NEUVES)))

ints=[interne(P[k]['cols']) for k in ANC]
dmins=[min(dist(P[k]['cols'],P[o]['cols']) for o in ANC if o!=k) for k in ANC]
print("LE JEU DE REFERENCE (les 21)")
print("  ecart interne      : min %.1f · mediane %.1f · max %.1f"%(min(ints),st.median(ints),max(ints)))
print("  distance au voisin : min %.1f · mediane %.1f · max %.1f"%(min(dmins),st.median(dmins),max(dmins)))
print("     (le plancher du jeu : Signal <-> Candide, %.1f)\n"%min(dmins))

for k in NEUVES:
    c=P[k]['cols']
    ds=sorted(((dist(c,P[o]['cols']),o) for o in P if o!=k))
    hexs=' '.join('#%02X%02X%02X'%tuple(x) for x in c)
    print("── %-10s %s"%(P[k]['name'],hexs))
    print("   ecart interne (min des 6 paires) : %.1f   [jeu : 13,0 a 37,8]"%interne(c))
    print("   distance a la plus proche        : %.1f  (%s)   [jeu : 9,2 a 20,7]"%(ds[0][0],ds[0][1]))
    print("   3 plus proches                   : "+" · ".join("%s %.1f"%(o,d) for d,o in ds[:3]))
    print("   la plus lointaine                : %s %.1f"%(ds[-1][1],ds[-1][0]))
    print()
import itertools
print("entre les trois neuves :")
for a,b in itertools.combinations(NEUVES,2):
    print("   %-10s <-> %-10s  %.1f"%(a,b,dist(P[a]['cols'],P[b]['cols'])))
