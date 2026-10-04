#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_pelote_doigt.py — LA PELOTE SOUS LE DOIGT, SUR LA CARTE GRAPHIQUE (v126, Tom, C-029, Q383).

« Le creux sous le doigt passe lui aussi à la carte graphique, comme la rotation et la lumière. Cible au banc : image p95 ≤ 22 ms
pendant qu'on caresse la Pelote. C'est un geste : validation de Tom sur iPhone obligatoire. »
Banc WebKit, @3x, doigt posé puis glissé pendant ~2,5 s (souris, bouton enfoncé), deux passes :
  1 · l'image, pendant le geste : p95 ≤ 22 ms (décidé) — l'intervalle entre deux images du navigateur ;
  2 · le dessin : doigt posé, vue figée, le rendu de la carte graphique est celui du peintre d'origine — ΔE00 moyen ≤ 2 (décidé en v125),
      et le creux EXISTE (l'image diffère du repos sous le doigt) ;
  3 · aucun poil n'est déplacé par le processeur pendant le geste (le compte publié par le peintre : un pointeur).
Preuve : avec `window._peloteEmpCPU=true` (le chemin de v125 : le contact calculé par le processeur) le contrôle 1 rougit (25 à 42 ms),
et sur la version d'avant v125 (peintre seul) : 156 à 175 ms. `--temoin` joue ce chemin.
"""
import sys, json
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
TEMOIN = '--temoin' in sys.argv
P95_MAX, DE_MAX = 22.0, 2.0
src = open('scratchpad/v125/compare.py', encoding='utf-8').read()
CMP = src[src.index('JS = r"""') + 9:src.index('}"""') + 1]
RAF = r"""()=>{ window.__T=[]; let av=performance.now(); window.__go=true; (function f(t){ __T.push(t-av); av=t; if(window.__go) requestAnimationFrame(f); })(av); }"""
FIN = r"""()=>{ window.__go=false; const T=__T.slice(2); T.sort((a,b)=>a-b); const q=p=>+T[Math.min(T.length-1,Math.floor(T.length*p))].toFixed(1); return {images:T.length, p50:q(.5), p95:q(.95), max:q(1), touches:document.getElementById('auBoule').__ntch, gl:document.getElementById('auBoule').__gl||0}; }"""
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){};" + ("window._peloteEmpCPU=true;" if TEMOIN else ""))
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4500)
    bo = pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left+r.width*0.4, r.top+r.height*0.5]}")
    if TEMOIN: print('TÉMOIN : le contact calculé par le processeur (chemin de v125)')
    for passe in range(2):
        pg.mouse.move(bo[0], bo[1]); pg.mouse.down(); pg.evaluate(RAF)
        for i in range(60): pg.mouse.move(bo[0] + i * 1.2, bo[1] + (i % 7)); pg.wait_for_timeout(40)
        r = pg.evaluate(FIN); pg.mouse.up(); pg.wait_for_timeout(1500)
        juge('1 · [passe %d] pendant qu\'on caresse la Pelote : image p95 ≤ %.0f ms' % (passe + 1, P95_MAX), r['p95'] <= P95_MAX, 'p50 %.1f · p95 %.1f · %d images' % (r['p50'], r['p95'], r['images']))
        juge('3 · [passe %d] aucun poil déplacé par le processeur' % (passe + 1), r['touches'] == 0 and r['gl'] > 0, '%s poil(s) · %d image(s) de la carte' % (r['touches'], r['gl']))
    # 2 · le dessin, doigt posé, vue figée
    pg.evaluate("()=>{_aura.fige(true); _aura.vue(3.1,0.32)}"); pg.wait_for_timeout(500)
    repos = pg.evaluate("()=>{ _aura.pelote(); const c=document.getElementById('auBoule'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; window.__repos=new Uint8ClampedArray(d); return c.width; }")
    pg.mouse.move(bo[0], bo[1]); pg.mouse.down(); pg.wait_for_timeout(1400)
    c = pg.evaluate(CMP, 'doigt')
    creux = pg.evaluate("()=>{ _aura.pelote(); const c=document.getElementById('auBoule'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data, a=window.__repos; let n=0, t=0; for(let i=0;i<d.length;i+=4){ if(!d[i+3]) continue; t++; if(Math.abs(d[i]-a[i])>14||Math.abs(d[i+1]-a[i+1])>14||Math.abs(d[i+2]-a[i+2])>14) n++; } return 100*n/t; }")
    pg.mouse.up()
    juge('2 · doigt posé : le rendu de la carte graphique est celui du peintre (ΔE00 moyen ≤ %.0f)' % DE_MAX, c['moyenne'] <= DE_MAX and c['gl'] > 0, 'ΔE00 moyen %.2f · %.1f %% des pixels au-delà de 2 · par blocs %.2f' % (c['moyenne'], c['part>2'], c['blocs']['moyenne']))
    juge('2 · le creux existe : sous le doigt, l\'image n\'est plus celle du repos', creux > 3, '%.1f %% des pixels de la Pelote changent' % creux)
    juge('aucune erreur de page', not er and not pg.evaluate("()=>window._peloteGLErreur||null"), '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:8]))
sys.exit(1 if ko else 0)
