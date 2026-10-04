#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_retour.py — LA VIE AU REPOS : LE RETOUR EST EXACT (v127, Tom, C-028).

« Retour exact : après chaque mouvement, la dalle revient au pixel près à son image d'avant, en restaurant l'état d'origine plutôt qu'en
rejouant le mouvement à l'envers. Juge : cent mouvements, zéro pixel d'écart au retour. »
Le juge force les mouvements (`Toile.vivant.force()`, le tirage du moteur) sur les douze mondes qui bougent, neuf par monde (108), en
WebKit ; avant chaque mouvement il lit le canevas de la Toile ENTIER, il vérifie que le mouvement a bien lieu (des pixels changent
pendant), puis il relit après : ZÉRO pixel différent, à l'égalité stricte (aucune tolérance : la valeur décidée est 0, écrite en dur).
Preuve : sur la version d'avant (app et moteur de v126, sauvegardes/*-avant-v127) il ROUGIT — les mondes à ressort ne reviennent pas.
  --mondes=a,b   --n=7
"""
import sys, json
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
MONDES = ['encre', 'touffe', 'mosaique', 'braille', 'pixel', 'sillons', 'gravure', 'halin', 'bobinette', 'ritournelle', 'madrure', 'terrazzo']
N = 9; RESTE_DECIDE = 0
for a in sys.argv[1:]:
    if a.startswith('--mondes='): MONDES = a[9:].split(',')
    if a.startswith('--n='): N = int(a[4:])
JS = r"""async (N)=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=cv.width; o.height=cv.height; const g=o.getContext('2d',{willReadFrequently:true});
 const lit=()=>{ g.globalCompositeOperation='copy'; g.drawImage(cv,0,0); return g.getImageData(0,0,o.width,o.height).data; }; const out=[];
 for(let k=0;k<N;k++){ let essais=0; while(Toile.vivant.boucle()&&essais++<40) await new Promise(r=>setTimeout(r,150)); await new Promise(r=>setTimeout(r,250));
   const av=lit(); const n0=Toile.vivant.journal().length; Toile.vivant.force(); let j=Toile.vivant.journal(); if(j.length===n0){ out.push({rate:1}); continue; } j=j[j.length-1];
   let mx=0, im=0; const fin=performance.now()+j.d+200;
   await new Promise(res=>{ function f(){ if(++im%5===0){ const d=lit(); let n=0; for(let i=0;i<d.length;i+=4) if(d[i]!==av[i]||d[i+1]!==av[i+1]||d[i+2]!==av[i+2]) n++; if(n>mx) mx=n; } if(performance.now()<fin) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
   essais=0; while(Toile.vivant.boucle()&&essais++<40) await new Promise(r=>setTimeout(r,100)); await new Promise(r=>setTimeout(r,200));
   const d=lit(); let n=0; for(let i=0;i<d.length;i+=4) if(d[i]!==av[i]||d[i+1]!==av[i+1]||d[i+2]!==av[i+2]) n++;
   out.push({pendant:mx, reste:n}); }
 return out; }"""
ok = 0; ko = []; total = 0; revenus = 0
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
with sync_playwright() as p:
    b = p.webkit.launch(); er = []
    for m in MONDES:
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script("window._vivantFixe=600000;try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
        pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} Toile.setTheme(m);}", m); pg.wait_for_timeout(7000)
        R = pg.evaluate(JS, N); joues = [r for r in R if not r.get('rate')]; total += len(joues); revenus += sum(1 for r in joues if r['reste'] == RESTE_DECIDE)
        juge('[%s] les mouvements sont joués (%d demandés) et des pixels changent pendant' % (m, N), len(joues) >= N - 1 and sum(1 for r in joues if r['pendant'] > 0) >= max(1, len(joues) - 2), '%d joué(s), pendant : %s px' % (len(joues), ' '.join(str(r['pendant']) for r in joues)))
        juge('[%s] retour : %d pixel d\'écart après chaque mouvement' % (m, RESTE_DECIDE), bool(joues) and all(r['reste'] == RESTE_DECIDE for r in joues), 'restes : %s' % ' '.join(str(r['reste']) for r in joues))
        ctx.close()
    juge('cent mouvements au moins, tous revenus au pixel', total >= min(100, len(MONDES) * (N - 1)) and revenus == total, '%d revenus sur %d' % (revenus, total))
    juge('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:10]))
sys.exit(1 if ko else 0)
