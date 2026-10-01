# -*- coding: utf-8 -*-
import re,io,json,sys
sys.path.insert(0,'scratchpad/s26')
from palettes import interne, dist
S=io.open('app.html',encoding='utf-8').read()
m=re.search(r'var PALS=(\{.*?\});',S,re.S)
P=json.loads(re.sub(r'(\w+):',r'"\1":',m.group(1)).replace("'",'"'))
EX={k:P[k]['cols'] for k in P}

CAND={
 'A rouge-neon/cyan/uv/soufre': [[255,62,0],[0,229,255],[86,0,214],[246,255,0]],
 'B magenta/lime/indigo/peche': [[255,0,144],[190,255,0],[35,0,120],[255,196,140]],
 'C corail/turquoise/uv/os'   : [[255,94,77],[0,232,200],[124,0,255],[240,235,205]],
 'D anis/klein/bonbon/acide'  : [[176,255,48],[0,71,255],[255,92,190],[250,255,200]],
 'E uv/orange/menthe/noir'    : [[138,43,255],[255,120,0],[64,255,170],[10,0,30]],
 'F jaune-fluo/violet/sang/ciel':[[238,255,0],[122,0,255],[214,0,60],[168,230,255]],
 'G orange/rose/turquoise/prune':[[255,106,0],[255,0,110],[0,214,198],[58,0,80]],
 'H vert-neon/framboise/bleu/ivoire':[[0,255,140],[230,0,115],[0,64,255],[255,247,222]],
 'I cyan/jaune/magenta/encre' :[[0,240,255],[255,236,0],[255,0,170],[18,0,36]],
 'J tangerine/uv/vert/rose'   :[[255,138,0],[104,0,224],[0,200,90],[255,170,200]],
 'K rose-fluo/bleu/jaune/vert':[[255,46,158],[0,120,255],[255,222,0],[0,190,120]],
 'L peche/aubergine/menthe/or':[[255,150,110],[60,0,70],[110,255,200],[255,205,60]],
}
rows=[]
for nom,c in CAND.items():
    it=interne(c)
    ds=sorted(((dist(c,EX[k]),k) for k in EX))
    # + distance aux autres candidats
    rows.append((nom,it,ds[0][0],ds[0][1],ds[1][0],ds[1][1]))
rows.sort(key=lambda r:-r[2])
print("%-34s %6s %6s %-14s %6s %s"%("candidat","int","dmin","(à)","d2","(à)"))
for r in rows: print("%-34s %6.1f %6.1f %-14s %6.1f %s"%r)

print("\n--- entre candidats ---")
ks=list(CAND)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        d=dist(CAND[ks[i]],CAND[ks[j]])
        if d<14: print("  %.1f  %s  <->  %s"%(d,ks[i],ks[j]))
