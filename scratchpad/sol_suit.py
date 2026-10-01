# -*- coding: utf-8 -*-
"""LE SOL SUIT LA PALETTE, LES ÎLES ET LES ÉTATS NON — mesuré sur l'IMAGE, vue figée.
   On rend la sphère sous trois palettes et on compare :
     · la couleur moyenne du SOL (sans les îles)  → doit BOUGER
     · l'empreinte des dalles                      → ne doit PAS bouger
     · les pastilles et les arcs                   → ne doivent PAS bouger"""
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.path.insert(0,'.')
from col import lab, dE, r2h
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
PALS=['signal','irascible','allegre']
ETATS = r"""()=>{var o={};
 var lg=document.querySelectorAll('#auraScreen .au-lg i');
 o.pastilles=[].map.call(lg,function(e){return getComputedStyle(e).backgroundColor;}).join(' ');
 var A=[]; document.querySelectorAll('#auraScreen .au-nb path').forEach(function(p){var s=p.getAttribute('stroke');if(s)A.push(s);});
 o.arcs=A.slice(0,8).join(' ');
 var D=[]; document.querySelectorAll('#auraScreen .au-c canvas').forEach(function(c){
   try{var g=c.getContext('2d'),d=g.getImageData(0,0,c.width,c.height).data,h=2166136261;
       for(var k=0;k<d.length;k+=331){h^=d[k];h=Math.imul(h,16777619);} D.push((h>>>0).toString(16));}catch(e){D.push('x');}});
 o.dalles=D.join(' ');
 return o;}"""
def moyenne(p):
    im=Image.open(p).convert('RGB'); W,H=im.size; px=im.load()
    fond=px[3,3]; s=[0,0,0]; n=0
    for y in range(0,H,3):
        for x in range(0,W,3):
            c=px[x,y]
            if abs(c[0]-fond[0])+abs(c[1]-fond[1])+abs(c[2]-fond[2])>26:
                s[0]+=c[0];s[1]+=c[1];s[2]+=c[2];n+=1
    return tuple(v/max(1,n) for v in s), n
res={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for k in PALS:
        pg.evaluate("(p)=>{window.Toile.setPalette(p);}", k); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4200)
        pg.evaluate("()=>{try{window._aura.fige(true);window._aura.vue(0,0);}catch(e){}}"); pg.wait_for_timeout(900)
        e=pg.evaluate(ETATS)
        pg.evaluate("()=>{try{window._aura.sansIles(true);}catch(e){}}"); pg.wait_for_timeout(1600)
        pg.locator('#auBoule').screenshot(path='cap/sol-%s.png'%k)
        pg.evaluate("()=>{try{window._aura.sansIles(false);}catch(e){}}"); pg.wait_for_timeout(600)
        m,n=moyenne('cap/sol-%s.png'%k)
        res[k]={'sol':m,'n':n,'e':e}
    b.close()
print('%-13s %-10s  %s'%('palette','sol moyen','ΔE au sol de « signal »'))
base=res[PALS[0]]['sol']
for k in PALS:
    m=res[k]['sol']
    print('%-13s %-10s  %.1f'%(k, r2h(m), dE(tuple(int(v) for v in m), tuple(int(v) for v in base))))
print()
for champ,att in (('pastilles','FIXE'),('arcs','FIXE'),('dalles','FIXE')):
    vals={res[k]['e'][champ] for k in PALS}
    print('%-10s attendu %-5s  →  %s  (%d valeur%s distincte%s sur %d palettes)'
          %(champ, att, 'FIXE ✓' if len(vals)==1 else 'BOUGE ✗', len(vals), '' if len(vals)==1 else 's', '' if len(vals)==1 else 's', len(PALS)))
