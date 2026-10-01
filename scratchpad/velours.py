# -*- coding: utf-8 -*-
"""LE VELOURS — mesuré sur l'image rendue, à VUE FIGÉE (§7 : on compare à l'angle, jamais à l'instant).
   Trois grandeurs, et chacune a la forme du défaut (§7) :
     1 · l'ÉTENDUE de la rampe : écart de clarté entre le haut et le bas du sol
     2 · la SATURATION EN HAUT : part des pixels du sol dont la chroma s'écroule (< 8 en CIELAB)
     3 · l'ÉCRÊTAGE : part des pixels du sol au-dessus de L* 92 (la rampe bute sur le blanc)"""
import sys, math
from playwright.sync_api import sync_playwright
from PIL import Image
sys.path.insert(0,'.')
from col import lab, L255
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
NOM = sys.argv[2] if len(sys.argv)>2 else 'velours'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5500)
    # vue FIGÉE au même angle, sans îles : on mesure LE SOL seul
    pg.evaluate("()=>{try{window._aura.fige(true);window._aura.vue(0,0);}catch(e){}}"); pg.wait_for_timeout(1200)
    et=pg.evaluate("()=>{try{var e=window._aura.etat();return {palier:e.palier,ms:e.ms};}catch(x){return {}}}")
    pg.wait_for_selector('#auBoule', timeout=20000)
    el=pg.locator('#auBoule')
    el.screenshot(path='cap/%s.png'%NOM)
    # sans les îles : on isole LE SOL
    pg.evaluate("()=>{try{window._aura.sansIles(true);}catch(e){}}"); pg.wait_for_timeout(1800)
    el.screenshot(path='cap/%s-sol.png'%NOM)
    b.close()
im=Image.open('cap/%s-sol.png'%NOM).convert('RGB')
W,H=im.size
px=im.load()
# le disque : on cherche les pixels non-fond
fond=px[3,3]
pts=[]
for y in range(0,H,2):
    for x in range(0,W,2):
        c=px[x,y]
        if abs(c[0]-fond[0])+abs(c[1]-fond[1])+abs(c[2]-fond[2])>26: pts.append((x,y,c))
if not pts:
    print('aucun pixel de sphère'); sys.exit(0)
xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2; R=(max(xs)-min(xs))/2
# on ne garde que le cœur (0,82 R) pour éviter le limbe
coeur=[p for p in pts if (p[0]-cx)**2+(p[1]-cy)**2 < (0.82*R)**2]
def Ls(c): return lab(tuple(c))[0]
def C(c):
    l=lab(tuple(c)); return math.hypot(l[1],l[2])
haut=[p for p in coeur if p[1] < cy-0.35*R]
bas =[p for p in coeur if p[1] > cy+0.35*R]
Lh=sum(Ls(p[2]) for p in haut)/max(1,len(haut))
Lb=sum(Ls(p[2]) for p in bas )/max(1,len(bas))
Ch=sum(C(p[2]) for p in haut)/max(1,len(haut))
Cb=sum(C(p[2]) for p in bas )/max(1,len(bas))
plats=sum(1 for p in haut if C(p[2])<8)/max(1,len(haut))
ecr  =sum(1 for p in coeur if Ls(p[2])>92)/max(1,len(coeur))
print('%s · palier %s · %s px de sphère, R=%.0f'%(NOM, et.get('palier'), len(coeur), R))
print('  1 · étendue de la rampe   L* haut %.1f → bas %.1f   =  %.1f'%(Lh,Lb,Lh-Lb))
print('  2 · chroma                C* haut %.1f → bas %.1f   ·  %.1f %% du haut sous C* 8'%(Ch,Cb,100*plats))
print('  3 · écrêtage vers le blanc                           %.1f %% du cœur au-dessus de L* 92'%(100*ecr))
