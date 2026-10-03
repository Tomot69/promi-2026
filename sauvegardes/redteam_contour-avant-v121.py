#!/usr/bin/env python3
"""
redteam_contour.py — RIEN NE DÉPASSE DE LA SILHOUETTE DE LA PELOTE (v116, Tom : « rien ne dépasse jamais du contour »).
On rend l'Aura deux fois, boule visible puis boule cachée, rotation figée : toute différence au-delà de la silhouette + 4 pt (les pointes du poil natif, mesurées à 2,8) est une
matière qui déborde (la couronne de v115 en était une). L'ombre n'est pas en cause : elle est peinte par un autre nœud, présent dans
les deux rendus. Clair et sombre. Rougi : python3 redteam_contour.py sauvegardes/app-avant-v116.html (la couronne de v115).
(La respiration, elle, se jugera quand son option sera choisie — planche v116.)
"""
import sys, os, io, math, shutil
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
S=2; CX=195
ARG=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); tmp=None
if '/' in ARG: shutil.copy(ARG,'zz-contour.html'); ARG=tmp='zz-contour.html'
def cap(pg): return Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
ok=True
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=S)
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(7000)
    for d in (0,1):
        ouvre(pg,d); pg.wait_for_timeout(3000); pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); pg.wait_for_timeout(300)
        g=pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(),s=dv.width/390,r=document.getElementById('auBoule').getBoundingClientRect();return {cy:(r.top-dv.top)/s+r.height/s/2}}")
        CY=g['cy']; RS=116.032+5.5   # la silhouette lue à 50 % d'opacité (poil compris)
        # ⚑ REPRIS EN v119 (§7). LA RÈGLE QUE CE CONTRÔLE ENCODE : aucune MATIÈRE (poil, fibre) ne dépasse de la silhouette — intacte.
        #   LA DÉCISION QUI S'AJOUTE (Tom, v119) : un MINI HALO prolonge la lumière de la Pelote, borné à 0,08 D (18,6 pt). Le juge lit
        #   donc deux fois : halo ÉTEINT (crochet `_peloteSansHalo`), rien ne dépasse, comme avant ; halo allumé, RIEN au-delà de 0,08 D.
        #   Original : sauvegardes/redteam_contour-avant-v119.py
        pg.evaluate("()=>{window._peloteSansHalo=true}"); pg.wait_for_timeout(500)
        A=cap(pg)
        pg.evaluate("()=>{[...document.querySelectorAll('#auraScreen .au-bo, #auPeloteCouronne')].forEach(e=>e.style.visibility='hidden')}"); B=cap(pg)
        pg.evaluate("()=>{[...document.querySelectorAll('#auraScreen .au-bo, #auPeloteCouronne')].forEach(e=>e.style.visibility='')}")
        dd=ImageChops.difference(A,B).convert('L').point(lambda v:255 if v>6 else 0); px=dd.load(); hors=0; rmax=0
        for y in range(dd.height):
            for x in range(dd.width):
                if px[x,y]:
                    r=math.hypot(x/S-CX,y/S-CY); rmax=max(rmax,r)
                    if r>RS+4: hors+=1   # + 4 : les POINTES du poil natif, mesurées à 124,1–124,3 depuis toujours ; la couronne de v115 allait à 147
        pg.evaluate("()=>{window._peloteSansHalo=false}"); pg.wait_for_timeout(500); A2=cap(pg)
        d2=ImageChops.difference(A2,B).convert('L').point(lambda v:255 if v>2 else 0); p2=d2.load(); loin=0; rh=0
        for y in range(d2.height):
            for x in range(d2.width):
                if p2[x,y]:
                    r=math.hypot(x/S-CX,y/S-CY); rh=max(rh,r)
                    if r>121.0+0.08*232.064+1.0: loin+=1
        bon = hors==0 and loin==0
        print('   [%s] avec le halo : la lumière s\'arrête à %.1f du centre (borne %.1f) · pixels au-delà : %d'%('sombre' if d else 'clair',rh,121.0+0.08*232.064,loin))
        print('%s [%s] la Pelote s\'arrête à %.1f du centre (silhouette %.1f) · pixels au-delà : %d'%('OK' if bon else '✗','sombre' if d else 'clair',rmax,RS,hors)); ok=ok and bon
    b.close()
if tmp: os.remove(tmp)
print('✅ rien ne dépasse du contour' if ok else '❌ une matière dépasse de la silhouette'); sys.exit(0 if ok else 1)
