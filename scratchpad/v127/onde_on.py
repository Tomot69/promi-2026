#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_ramage_onde.py — RAMAGE : LE DISQUE DE LA POUSSE NE DOIT PAS SE VOIR COMME UNE ONDE (v126, Tom, C-009). ⚠ ROUGE : LE DÉFAUT EST OUVERT.

« Tom voit une onde ronde, par intermittence, au Studio et sur la Toile. […] Juge : il force le déclencheur et ne doit trouver aucune
structure concentrique. Il doit rougir sur l'état actuel. »
LE DÉCLENCHEUR, MESURÉ (v126) : l'ARRIVÉE d'une plume. Le film de la pousse est un DISQUE qui grandit autour d'elle (peint par un Worker,
pour l'état d'arrivée) ; le plumage autour du disque reste celui de l'état d'avant. Les deux ne se raccordent pas : un anneau de liserés
au bord du disque pendant qu'il avance, puis, à la dernière image, TOUT ce qui est hors du disque change d'un coup (5 à 16 % des pixels
de la Toile selon la plume : plus elle est grande, plus ça se voit — d'où « par intermittence »). Aucun monde ne bouge au repos : ce n'est
pas une ancienne vie au repos.
CE QUE LE JUGE MESURE, sur le canevas du Studio, image par image (WebKit), deux ouvertures : la part des pixels qui changent dans les
dernières images de l'événement quand ce changement couvre plus de 60 % de la Toile — le saut d'ensemble. Décidé : ≤ 2 % (aucune
structure hors du disque). État de v126 : 5 à 16 % → ROUGE. Trois corrections essayées en v126 (même genre de canevas, papier et
plumage de l'image d'ouverture) n'ont pas supprimé le saut : rien n'est changé dans le moteur.
"""
import sys, io, base64
from playwright.sync_api import sync_playwright
from PIL import Image
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
SAUT_MAX, PAPIER_TOL = 2.0, 3
JS = r"""async ()=>{ const cv=document.querySelector('#stBg'); const W=cv.width, H=cv.height; const o=document.createElement('canvas'); const k=Math.min(1, 400/W); o.width=Math.round(W*k); o.height=Math.round(H*k); const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; };
  const mode=(d)=>{ const h={}; for(let i=0;i<d.length;i+=16){ const kk=(d[i]>>1)+','+(d[i+1]>>1)+','+(d[i+2]>>1); h[kk]=(h[kk]||0)+1; } let b=null,m=0; for(const kk in h) if(h[kk]>m){ m=h[kk]; b=kk; } return b.split(',').map(v=>v*2); };
  let av=lit(), papierAvant=mode(av), ev=null, calme=0, t0=performance.now(), fini=false;
  await new Promise(res=>{ function f(t){ const d=lit(); let n=0, x0=1e9,x1=-1,y0=1e9,y1=-1;
      for(let i=0;i<d.length;i+=4){ if(Math.max(Math.abs(d[i]-av[i]),Math.abs(d[i+1]-av[i+1]),Math.abs(d[i+2]-av[i+2]))>12){ n++; const p=i/4, x=p%o.width, y=(p/o.width)|0; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
      const part=100*n/(d.length/4), boite=n?100*((x1-x0+1)*(y1-y0+1))/(d.length/4):0;
      if(n>30){ if(!ev) ev={im:[]}; ev.im.push([part,boite]); calme=0; } else if(ev && ++calme>14) fini=true;
      av=d; if(fini || t-t0>16000) res(); else requestAnimationFrame(f); } requestAnimationFrame(f); });
  return {ev, papierAvant, papierApres:mode(av)}; }"""
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail))
with sync_playwright() as p:
    b = p.webkit.launch()
    for passe in range(2):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(3000)
        pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(1500)
        r = pg.evaluate(JS); ev = r['ev']
        juge('[passe %d] le déclencheur est joué : une arrivée, au Studio, juste après l\'ouverture' % (passe + 1), bool(ev) and len(ev['im']) >= 8, '%d image(s)' % (len(ev['im']) if ev else 0))
        if ev:
            sauts = [i for i in ev['im'][-4:] if i[1] > 60]
            s = max([i[0] for i in sauts] or [0])
            print([ [round(a,1),round(c)] for a,c in ev['im']])
            juge('1 · [passe %d] pas de saut d\'ensemble à la fin de l\'événement (≤ %.0f %% des pixels)' % (passe + 1, SAUT_MAX), s <= SAUT_MAX, '%.1f %%' % s)
        juge('[passe %d] aucune erreur de page' % (passe + 1), not er, '; '.join(er[:2]))
        ctx.close()
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
sys.exit(1 if ko else 0)
