#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_evol.py — LA TOILE NE SACCADE PAS QUAND UNE DALLE APPARAÎT OU DISPARAÎT ; LA PELOTE NE SACCADE PAS SOUS LE DOIGT (v144, Tom, 12 oct. 2026 — C-112, C-113).

« Quand on plante ou qu'on retire une parole, la Toile saccade image par image. Mesure sur banc_tom (planter, puis retirer, sous cinq mondes),
  nomme ce qui bloque, et sors-le de l'animation. Cible : aucune image au-delà de 20 ms pendant l'apparition et la disparition. »
« La fluidité de la Pelote quand on la touche est saccadée : à corriger et remettre comme avant, fluide. »

Par banc_tom (WebKit, 390 × 844, @3x, Toile vide, paroles plantées par l'app). Chaque rappel de la page (minuteur, image, observateur, écouteur)
est chronométré : c'est le TRAVAIL qu'on juge. ⚠ L'intervalle entre deux images ne peut pas tenir un seuil de 20 ms sur ce banc (page au repos,
il donne déjà des images de 21 à 27 ms, v124 ; un simulateur ouvert à côté en donne de 30 à 60) : il est RELEVÉ et affiché, et borné plus large
(aucune image au-delà de 80 ms ; v143 : 90 à 220).
  LA TOILE, sous cinq mondes, du toucher qui plante (puis qui retire) à 3,5 s :
    1 · aucun rappel au-delà de 20 ms de travail (valeur décidée) PENDANT LE MOUVEMENT — du toucher jusqu'à ce que la Toile soit posée (`_evol()`) ;
        ce qui attend la fin (la passe de lisibilité, les polices, le cache des dalles) est relevé, pas jugé : « sors-le de l'animation » ;
        la boucle d'images du moteur est jugée à part (p95 ≤ 20 ms, jamais 33,4 ms), le toucher lui-même n'est pas « le mouvement » ;
    2 · aucune image au-delà de 80 ms ;
    3 · le recadrage ne passe pas à chaque image (au plus six fois pendant l'apparition).
  LA PELOTE, une caresse lente (2,3 s) puis une caresse vive, au vrai toucher (rayon de contact) :
    4 · l'écouteur du doigt ne recalcule plus un poil : aucun `pointermove` au-delà de 3 ms ;
    5 · l'inscription de la trace tient ENTRE deux images : aucune tâche d'inscription au-delà de 12 ms, au plus une toutes les 60 ms, et la
        boucle d'images de la Pelote ne dépasse jamais 8 ms (les images au-delà de 20 ms sont relevées : 0 à 1 machine au calme, 5 à 17 sur v143) ;
    6 · la trace se forme toujours sous le doigt : des segments sont inscrits AVANT le lever.
Rouge sur v143 (`zz-av144.html`). Usage : python3 redteam_evol.py [fichier.html] [--mondes=encre,touffe,…]
"""
import sys, collections; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
MONDES = next((a.split('=')[1] for a in sys.argv if a.startswith('--mondes=')), 'encre,touffe,mosaique,ritournelle,brouillamini').split(',')
TRAVAIL_MAX, IMAGE_MAX, RECADRES_MAX = 20.0, 80.0, 6
MOTEUR_P95, MOTEUR_MAX = 20.0, 33.4   # la boucle d'images du moteur elle-même : p95 ≤ 20 ms, jamais deux images (33,4 ms)
def hors(P):
    """ce qu'on peut SORTIR du mouvement : tout rappel compté pendant le mouvement, sauf la boucle d'images du moteur (jugée à part) et le toucher
    lui-même (le clic qui plante ou qui retire, dans ses 60 premières millisecondes : c'est la réponse au doigt, avant que rien ne bouge)"""
    return [e for e in P if e[3] and 'image | frame' not in e[2] and not (e[0] < 60 and 'écouteur' in e[2])]
def moteur(P):
    L = sorted(e[1] for e in P if 'image | frame' in e[2]); return (L[min(len(L) - 1, int(len(L) * .95))] if L else 0, L[-1] if L else 0, len(L))
PROF = r"""(function(){ var R=window.__P=[], on=false; window.__Pon=function(v){ on=v; if(v) R.length=0; };
  function nom(f,typ){ var s=''; try{ s=(f.name||'')+' · '+(''+f).replace(/\s+/g,' ').slice(0,110); }catch(e){} return typ+' | '+s; }
  function env(f,typ){ if(typeof f!=='function') return f; var w=function(){ if(!on) return f.apply(this,arguments); var t=performance.now(); try{ return f.apply(this,arguments); } finally { var d=performance.now()-t; if(d>=1.5){ var ev=0; try{ ev=(window._evol?(window._evol()?1:0):((window.Toile_state&&Toile_state().running)||window._tirageActive?1:0)); }catch(e){} R.push([Math.round(t),Math.round(d*10)/10,nom(f,typ),ev]); } } }; return w; }
  var st=window.setTimeout; window.setTimeout=function(f,ms){ var a=[].slice.call(arguments); a[0]=env(f,'minuteur '+(ms|0)); return st.apply(window,a); };
  var si=window.setInterval; window.setInterval=function(f,ms){ var a=[].slice.call(arguments); a[0]=env(f,'intervalle '+(ms|0)); return si.apply(window,a); };
  var rf=window.requestAnimationFrame; window.requestAnimationFrame=function(f){ return rf.call(window, env(f,'image')); };
  var MO=window.MutationObserver; window.MutationObserver=function(f){ return new MO(env(f,'observateur')); }; window.MutationObserver.prototype=MO.prototype;
  var ael=EventTarget.prototype.addEventListener; EventTarget.prototype.addEventListener=function(t,f,o){ if(typeof f==='function' && /^(touch|pointer|click|mouse|transitionend)/.test(t)){ var w=f.__w||(f.__w=env(f,'écouteur '+t)); return ael.call(this,t,w,o); } return ael.call(this,t,f,o); };
  window.__F=[]; (function b(t){ window.__F.push(Math.round(performance.now()*10)/10); if(window.__F.length>4000) window.__F.shift(); rf.call(window,b); })();
})();"""
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def releve(pg, duree=3500):
    r = pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice()})"); t0 = r['t0']
    I = [r['F'][i + 1] - r['F'][i] for i in range(len(r['F']) - 1) if t0 <= r['F'][i] <= t0 + duree]
    P = [(e[0] - t0, e[1], e[2], e[3]) for e in r['P'] if 0 <= e[0] - t0 <= duree]
    return I, P
def dit(I, P):
    mo = moteur(P); P = hors(P) or [(0, 0, '', 1)]
    pire = max(P, key=lambda e: e[1]) if P else (0, 0, '')
    return 'moteur : p95 %.0f, pire %.0f ms (%d images) · ' % mo + '%d images · %d au-delà de 20 ms · la plus longue %.0f ms · rappel le plus long PENDANT le mouvement %.1f ms à %d ms (%s)' % (len(I), sum(1 for x in I if x > 20), max(I or [0]), pire[1], pire[0], pire[2][:70])
with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MONDES:
        ctx = B.contexte(b); ctx.add_init_script(PROF); pg = B.ouvre(ctx, F)
        pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(1500)
        for t in ['rendre le livre', 'écrire à Lou', 'arroser le ficus']: B.plante(pg, t)
        pg.wait_for_timeout(3200)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{document.getElementById('fTitle').value='courir dimanche';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(4000)
        I, P = releve(pg); n1 = pg.evaluate("()=>promises.length")
        juge('1 · [%s] planter : aucun rappel au-delà de %d ms de travail pendant le mouvement' % (m, TRAVAIL_MAX), n1 == 4 and bool(I) and all(e[1] <= TRAVAIL_MAX for e in hors(P)) and moteur(P)[0] <= MOTEUR_P95 and moteur(P)[1] <= MOTEUR_MAX, dit(I, P))
        juge('2 · [%s] planter : aucune image au-delà de %d ms' % (m, IMAGE_MAX), bool(I) and max(I) <= IMAGE_MAX, 'la plus longue %.0f ms' % max(I or [0]))
        rec = [e for e in P if 'autoView' in e[2]]
        juge('3 · [%s] planter : le recadrage ne passe pas à chaque image (au plus %d fois)' % (m, RECADRES_MAX), len(rec) <= RECADRES_MAX, '%d fois, %.0f ms en tout' % (len(rec), sum(e[1] for e in rec)))
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); B.tap_sel(pg, '.v16-oui'); pg.wait_for_timeout(4000)
        I, P = releve(pg); n2 = pg.evaluate("()=>promises.length")
        juge('1 · [%s] retirer : aucun rappel au-delà de %d ms de travail pendant le mouvement' % (m, TRAVAIL_MAX), n2 == 3 and bool(I) and all(e[1] <= TRAVAIL_MAX for e in hors(P)) and moteur(P)[0] <= MOTEUR_P95 and moteur(P)[1] <= MOTEUR_MAX, dit(I, P))
        juge('2 · [%s] retirer : aucune image au-delà de %d ms' % (m, IMAGE_MAX), bool(I) and max(I) <= IMAGE_MAX, 'la plus longue %.0f ms' % max(I or [0]))
        ctx.close()
    # la Pelote
    ctx = B.contexte(b); ctx.add_init_script(PROF); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{closeAll();document.getElementById('souffleBtn').click()}"); pg.wait_for_timeout(5000)
    bo = pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}"); cx, cy = bo[0] + bo[2] / 2, bo[1] + bo[3] / 2
    for nom, pts, pas in (('caresse lente', [[cx - 50 + i * 1.6, cy - 10 + (i % 9)] for i in range(70)], 33), ('caresse vive', [[cx - 60 + i * 4, cy + 20 - i * 1.2] for i in range(30)], 16)):
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); window.__seg=-1; document.addEventListener('pointerup',function h(){ document.removeEventListener('pointerup',h,true); try{ window.__seg=_aura.tracesGeo().length; window.__segT=(window.__segT0!=null)?window.__segT0:null; }catch(e){} },true); window.__n0=_aura.tracesGeo().length; }")
        B.glisse(pg, pts, pas=pas, appareil=False, rx=11, ry=9)
        fin = pg.evaluate("()=>performance.now()-window.__t0"); I, P = releve(pg, fin); seg = pg.evaluate("()=>[window.__n0, window.__seg]")
        mv = [e for e in P if 'pointermove' in e[2]]
        juge('4 · [Pelote, %s] l\'écouteur du doigt ne recalcule plus un poil (aucun pointermove au-delà de 3 ms)' % nom, all(e[1] <= 3 for e in mv), '%d appel(s) de 1,5 ms ou plus · le plus long %.1f ms' % (len(mv), max([e[1] for e in mv] or [0])))
        ins = [e for e in P if 'videFile' in e[2]]; bo_ = [e[1] for e in P if 'image | boucle' in e[2]]
        juge('5 · [Pelote, %s] l\'inscription tient entre deux images (tâche ≤ 12 ms, au plus une par 60 ms, boucle ≤ 8 ms)' % nom, bool(ins) and max(e[1] for e in ins) <= 12 and len(ins) <= fin / 60.0 + 1 and max(bo_ or [0]) <= 8,
             '%d inscription(s) de 1,5 ms ou plus, la plus longue %.1f ms · boucle au pire %.1f ms · %d images, %d au-delà de 20 ms, la plus longue %.0f ms' % (len(ins), max([e[1] for e in ins] or [0]), max(bo_ or [0]), len(I), sum(1 for x in I if x > 20), max(I or [0])))
        juge('6 · [Pelote, %s] la trace se forme sous le doigt : des segments sont inscrits avant le lever' % nom, seg[1] > seg[0], '%d segment(s) avant le geste, %d au lever' % (seg[0], seg[1]))
        pg.wait_for_timeout(1500)
    juge('aucune erreur de page', not pg.erreurs and not pg.evaluate("()=>window._auraErreur||null"), str(pg.erreurs[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:10]))
sys.exit(1 if ko else 0)
