#!/usr/bin/env python3
"""redteam_veille_60.py — ⚑ v179a (Tom, C-232) : « la veille démarre après 60 s sans toucher ; sur mon iPhone elle part au bout de quelques secondes ».

LA CAUSE : sur l'iPhone (http, pas de Wake Lock) l'écran se verrouille seul ; Safari gèle la page ; au déverrouillage le premier tour de minuterie comptait
le temps passé écran éteint comme du calme, et la veille partait aussitôt rentré.
Banc WebKit sur l'état exporté de Tom, veille rétablie, temps lus DANS la page :
  D · `?veille=5` dans l'adresse : départ à 5 s ± 1 ; puis la même page SANS le paramètre : il n'est pas mémorisé (A).
  A · sans toucher depuis la fin du chargement (l'app affichée) : rien avant 59 s, départ à 60 s ± 1 (le délai déclaré : 60 000 en dur).
  B · un toucher (qui quitte la veille) : le départ suivant à 60 s ± 1 de ce toucher.
  C · la page cachée puis gelée deux minutes (son horloge saute, aucun tour de minuterie), puis rendue visible : rien avant 59 s, départ à 60 s ± 1 du retour.
Rouge sur v178 (`--fichier=zz-v178.html`) : 45 s, et départ immédiat au retour.
"""
import sys, time; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
SONDE = """()=>{ if(window.__vp) return; window.__vp=1; window.__va=[]; window.__vq=[]; var a=false;
  setInterval(function(){ var v=window._veille&&window._veille(); if(!v) return; if(v.active&&!a){ window.__va.push(performance.now()); } if(!v.active&&a){ window.__vq.push(performance.now()); } a=v.active; }, 40); }"""
def attend_depart(pg, n, s_max):
    t0 = time.time()
    while time.time() - t0 < s_max:
        if pg.evaluate("()=>window.__va.length") >= n: return pg.evaluate("()=>window.__va[%d]" % (n - 1))
        pg.wait_for_timeout(200)
    return None
def touche(pg):
    return pg.evaluate("""()=>{ var t=performance.now(); var o={bubbles:true,cancelable:true,pointerId:7,pointerType:'touch',isPrimary:true,clientX:200,clientY:400};
      document.body.dispatchEvent(new PointerEvent('pointerdown',o)); document.body.dispatchEvent(new PointerEvent('pointerup',o)); return t; }""")
with sync_playwright() as p:
    b = p.webkit.launch(); ctx, d = B.contexte_tom(b)
    if not ctx: print('pas d\'état exporté'); sys.exit(2)
    print('  état :', d['_fichier'], '·', F)
    pg = B.ouvre(ctx, F, 300); pg.evaluate("()=>localStorage.removeItem('promi_veille_off')")
    # D · ?veille=5, puis l'adresse sans paramètre
    pg.goto('http://127.0.0.1:8752/' + F + '?veille=5'); pg.evaluate(SONDE)
    di = pg.evaluate("()=>performance.getEntriesByType('navigation')[0].loadEventStart")
    t = attend_depart(pg, 1, 20)
    juge('D · `?veille=5` dans l\'adresse : départ à 5 s ± 1', t is not None and abs((t - di) / 1000 - 5) <= 1, None if t is None else '%.2f s' % ((t - di) / 1000))
    pg.goto('http://127.0.0.1:8752/' + F); pg.evaluate(SONDE)
    di = pg.evaluate("()=>performance.getEntriesByType('navigation')[0].loadEventStart")
    dl = pg.evaluate("()=>window._veilleRegle.DELAI")
    t = attend_depart(pg, 1, 75)
    s = None if t is None else (t - di) / 1000
    juge('A · sans toucher : rien avant 59 s, départ à 60 s ± 1 (et `?veille` non mémorisé)', s is not None and 59 <= s <= 61 and dl == 60000, 'départ %s · délai %s' % ('—' if s is None else '%.2f s' % s, dl))
    # B · un toucher quitte la veille ; le départ suivant à 60 s du toucher
    tt = touche(pg); pg.wait_for_timeout(300)
    act = pg.evaluate("()=>window._veille().active")
    t = attend_depart(pg, 2, 75)
    s = None if t is None else (t - tt) / 1000
    juge('B · un toucher quitte la veille ; départ suivant à 60 s ± 1 du toucher', (not act) and s is not None and 59 <= s <= 61, 'quittée %s · départ %s' % (not act, '—' if s is None else '%.2f s' % s))
    # C · la page cachée et gelée 2 min, puis visible
    touche(pg); pg.wait_for_timeout(400)
    tr = pg.evaluate("""()=>{ var real=performance.now.bind(performance);
      Object.defineProperty(document,'visibilityState',{get:()=>'hidden',configurable:true}); Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});
      document.dispatchEvent(new Event('visibilitychange'));
      performance.now=function(){ return real()+120000; };
      Object.defineProperty(document,'visibilityState',{get:()=>'visible',configurable:true}); Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});
      document.dispatchEvent(new Event('visibilitychange')); return performance.now(); }""")
    n0 = pg.evaluate("()=>window.__va.length")
    t = attend_depart(pg, n0 + 1, 75)
    s = None if t is None else (t - tr) / 1000
    juge('C · gelée 2 min puis rendue visible : rien avant 59 s, départ à 60 s ± 1 du retour', s is not None and 59 <= s <= 61, 'départ %s après le retour' % ('—' if s is None else '%.2f s' % s))
    juge('aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
