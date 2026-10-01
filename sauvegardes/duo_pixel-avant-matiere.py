#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""duo_pixel.py — SUPERPOSER LE CADRE DU MOODBOARD ET LA CAPTURE DE L'APP, ET MESURER.

Les juges comparent des cotes et des couleurs. **Un trait à la bonne position avec la
mauvaise courbe passe à zéro.** Cet outil-ci ne compare rien d'autre que les pixels : il
capture le cadre de la planche et l'écran de l'app, les met l'un sur l'autre, et rend
la part de pixels qui diffèrent — plus une image de différence, à regarder.

Il ne dit pas ce qui ne va pas. Il dit OÙ, et combien. On regarde ensuite.

Usage :  python3 scratchpad/duo_pixel.py <sortie> [nom ...]
"""
import base64
import json
import os
import sys

from playwright.sync_api import sync_playwright

RACINE = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
APP = "http://127.0.0.1:8752/app.html"
MBH = "http://127.0.0.1:8752/promi-moodboard-H.html"
NUT = "http://127.0.0.1:8752/promi-nuee-toile.html"

MARQUE = """()=>{const isF=e=>{const s=e.getAttribute('style')||'';
  return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  [...document.querySelectorAll('div')].filter(isF).forEach((f,i)=>f.setAttribute('data-cadre',i));}"""

# ── LES ÉCRANS : nom, planche, n° de cadre (sombre, clair), mise en scène dans l'app ──
ECRANS = [
    ('index-2',   MBH, (72, 73), "()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
    ('index-3',   MBH, (74, 75), "()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
    ('fil',       MBH, (76, 77), "()=>{if(window.closeAll)closeAll(); setView('fil');}"),
    ('fiche-encours', MBH, (46, 47), "()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&!q.req&&!q.chiche&&q.status==='encours'&&(!q.who||q.who==='moi'))[0]; if(p)openDetail(p.id);}"),
    ('fiche-tenue',   MBH, (48, 49), "()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&q.status==='tenu')[0]; if(p)openDetail(p.id);}"),
    ('page-plus',     MBH, (2, 3),   "()=>{if(window.closeAll)closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
    # ⚠ LA NUÉE DE LA PLANCHE, PAS UNE NUÉE FABRIQUÉE. Les cadres 6/7 de
    #    `promi-nuee-toile.html` montrent « le potager » à TROIS éléments. On garde donc SES
    #    trois premiers Promi et on détache les autres — au lieu d'y verser trois promesses
    #    quelconques, ce qui comparait deux Nuées différentes (relevé : 100 % de différence
    #    sur toute la hauteur).
    ('nuee-3',        NUT, (6, 7),   "()=>{const k='potager'; const l=promises.filter(q=>q.nuee===k&&!q.draft); l.slice(3).forEach(q=>{q.nuee=null;}); openEssaim(k);}"),
]

DIFF = """(a)=>new Promise(res=>{
  const A=new Image(), B=new Image(); let n=0;
  function pret(){ if(++n<2) return;
    const W=390, H=844;
    const c1=document.createElement('canvas'); c1.width=W; c1.height=H;
    const c2=document.createElement('canvas'); c2.width=W; c2.height=H;
    c1.getContext('2d').drawImage(A,0,0,W,H);
    c2.getContext('2d').drawImage(B,0,0,W,H);
    const d1=c1.getContext('2d').getImageData(0,0,W,H).data;
    const d2=c2.getContext('2d').getImageData(0,0,W,H).data;
    const out=document.createElement('canvas'); out.width=W; out.height=H;
    const go=out.getContext('2d'); const im=go.createImageData(W,H); const dd=im.data;
    let diff=0, tot=0;
    /* par bandes de 20 px : où ça diffère, pas seulement combien */
    const bandes=new Array(Math.ceil(H/20)).fill(0);
    for(let i=0;i<d1.length;i+=4){
      const dr=Math.abs(d1[i]-d2[i]), dg=Math.abs(d1[i+1]-d2[i+1]), db=Math.abs(d1[i+2]-d2[i+2]);
      const e=(dr+dg+db)>a.seuil;
      tot++;
      const p=i/4, y=Math.floor(p/W);
      if(e){ diff++; bandes[Math.floor(y/20)]++;
             dd[i]=255; dd[i+1]=0; dd[i+2]=90; dd[i+3]=255; }
      else { const g=(d1[i]*0.3+d1[i+1]*0.6+d1[i+2]*0.1);
             dd[i]=dd[i+1]=dd[i+2]=Math.round(40+g*0.35); dd[i+3]=255; }
    }
    go.putImageData(im,0,0);
    res({part:Math.round(1000*diff/tot)/10, diff:diff, tot:tot,
         bandes:bandes.map((v,k)=>[k*20,Math.round(1000*v/(20*W))/10]).filter(b=>b[1]>2),
         png:out.toDataURL('image/png')});
  }
  A.onload=pret; B.onload=pret; A.src=a.a; B.src=a.b;
})"""


def main():
    sortie = sys.argv[1]
    voulus = sys.argv[2:]
    os.makedirs(sortie, exist_ok=True)
    res = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        # ── les cadres de la planche, capturés une fois ──
        cadres = {}
        for url in (MBH, NUT):
            pg = b.new_page(viewport={'width': 1400, 'height': 1000}, device_scale_factor=2)
            pg.goto(url)
            pg.wait_for_timeout(4500)
            pg.evaluate(MARQUE)
            for nom, u, (cs, cl), _ in ECRANS:
                if u != url:
                    continue
                for th, n in (('dark', cs), ('light', cl)):
                    el = pg.query_selector('[data-cadre="%d"]' % n)
                    if el:
                        cadres[(nom, th)] = base64.b64encode(el.screenshot()).decode()
            pg.close()

        # ── l'app ──
        app = {}
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th)
            pg.wait_for_timeout(400)
            for nom, u, _, js in ECRANS:
                if voulus and nom not in voulus:
                    continue
                pg.evaluate("()=>{if(window.closeAll)closeAll();}")
                pg.wait_for_timeout(400)
                try:
                    pg.evaluate(js)
                except Exception as e:
                    print('  ⚠ mise en scène %s : %s' % (nom, e))
                pg.wait_for_timeout(2000)
                app[(nom, th)] = base64.b64encode(
                    pg.query_selector('#device').screenshot()).decode()
        pg.close()

        # ── la différence, calculée en canvas ──
        pg = b.new_page(viewport={'width': 500, 'height': 900})
        pg.goto('about:blank')
        for (nom, th), img in sorted(app.items()):
            ref = cadres.get((nom, th))
            if not ref:
                print('  ⚠ pas de cadre pour %s [%s]' % (nom, th))
                continue
            r = pg.evaluate(DIFF, {'a': 'data:image/png;base64,' + ref,
                                   'b': 'data:image/png;base64,' + img,
                                   'seuil': 60})
            res.append((nom, th, r['part'], r['bandes']))
            for etq, data in (('mb', ref), ('app', img), ('diff', r['png'].split(',', 1)[1])):
                io = open(os.path.join(sortie, '%s_%s_%s.png' % (nom, th, etq)), 'wb')
                io.write(base64.b64decode(data))
                io.close()
        b.close()

    print('\n%-16s %-6s %8s   bandes qui diffèrent (y, %%)' % ('écran', 'thème', 'écart'))
    print('-' * 78)
    for nom, th, part, bandes in sorted(res, key=lambda x: -x[2]):
        b3 = ' '.join('%d:%.0f%%' % (y, p) for y, p in bandes[:8])
        print('%-16s %-6s %7.1f%%   %s' % (nom, th, part, b3))
    print('\nimages dans', sortie)


main()
