#!/usr/bin/env python3
"""redteam_clavier_onb.py — ⚑ v153 (Tom, C-164) : LE CLAVIER APRÈS LE PRÉNOM.

« Dans l'onboarding, une fois le prénom validé, le clavier reste ouvert et gêne l'apparition du texte de la page suivante. Au moment de la validation,
le clavier se ferme (le champ perd le focus). La page suivante ne commence à tracer son texte qu'une fois le clavier entièrement redescendu (fin du
redimensionnement de visualViewport). Juge : après validation, aucun clavier ; le premier trait de lettre commence après la fermeture. »

Banc comme Tom (WebKit, 390 × 844, échelle 3, doigt), stockage vierge, le vrai parcours : toucher la phrase, taper le prénom, Retour.
Le clavier d'iOS est SIMULÉ là où le banc n'en a pas : `visualViewport` est remplacé par un objet qui se comporte comme celui de Safari — quand le
champ prend le focus, sa hauteur descend de 336 pt en 280 ms (des `resize` à chaque image) ; quand il le perd, elle remonte de même.
  A · après Retour, le champ n'a plus le focus (aucun clavier) dans les 100 ms ;
  B · le premier tracé de lettre de la page suivante (« [Prénom], donc. ») commence APRÈS le dernier redimensionnement (le clavier redescendu) ;
  C · tant que le clavier redescend, aucun texte de la page suivante n'est visible (ni le texte réel, ni un canevas de tracé) ;
  D · sans clavier (le banc nu), rien n'attend : le tracé part dans les 250 ms ;
  E · la parole se saisit ensuite en touchant la phrase (le champ reprend le focus au toucher).
Preuve : `--fichier=sauvegardes/app-cloture-v152.html` rougit (A, B, C).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
CLAVIER = """(()=>{ const H=844, K=336, D=280; let h=H; const vv=new EventTarget(); Object.defineProperty(vv,'height',{get:()=>h}); Object.defineProperty(vv,'width',{get:()=>390});
  Object.defineProperty(vv,'scale',{get:()=>1}); Object.defineProperty(vv,'offsetTop',{get:()=>0}); Object.defineProperty(vv,'pageTop',{get:()=>0});
  try{ Object.defineProperty(window,'visualViewport',{get:()=>vv, configurable:true}); }catch(e){}
  window.__kb={resize:[], cible:H}; let anim=0;
  function vers(c){ const h0=h, t0=performance.now(); window.__kb.cible=c; cancelAnimationFrame(anim);
    (function f(){ const u=Math.min(1,(performance.now()-t0)/D); h=Math.round(h0+(c-h0)*(1-Math.pow(1-u,3))); window.__kb.resize.push([performance.now(), h]); vv.dispatchEvent(new Event('resize')); if(u<1) anim=requestAnimationFrame(f); })(); }
  document.addEventListener('focusin', e=>{ if(e.target && e.target.id==='onbIn') setTimeout(()=>vers(H-K), 40); }, true);
  document.addEventListener('focusout', e=>{ if(e.target && e.target.id==='onbIn') setTimeout(()=>vers(H), 30); }, true);
})()"""
SONDE = """()=>{ window.__tr=[]; const T=window.TraceLettres; if(T && !T.__j){ const tr=T.trace; T.trace=function(c){ window.__tr.push([performance.now(), c.id||c.className]); return tr.apply(this, arguments); }; T.__j=1; }
  window.__vis=[]; (function f(){ const ids=['onbDit','onbQuid','onbSous']; let v=false; ids.forEach(i=>{ const e=document.getElementById(i); if(!e) return; const c=getComputedStyle(e); if(c.display!=='none' && c.visibility!=='hidden' && (c.clipPath==='none'||!c.clipPath) && (e.textContent||'').trim()) v=true; });
    if(document.querySelector('#onbV canvas[data-trace]')) v=true; window.__vis.push([performance.now(), v]); if(window.__vis.length<900) requestAnimationFrame(f); })(); }"""
def parcours(b, clavier):
    ctx = B.contexte(b, onb=False, guide=False)
    if clavier: ctx.add_init_script(CLAVIER)
    pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(500)
    pg.evaluate(SONDE)
    t_ret = pg.evaluate("()=>performance.now()"); pg.keyboard.press('Enter')
    pg.wait_for_timeout(100); foc = pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.id==='onbIn'); }")
    pg.wait_for_timeout(2600)
    d = pg.evaluate("()=>({tr:window.__tr, kb:window.__kb||null, vis:window.__vis, dit:(document.getElementById('onbDit')||{}).textContent})")
    # E · la parole au toucher de la phrase
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500)
    foc2 = pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.id==='onbIn'); }")
    pg.keyboard.type('marcher une heure', delay=25); pg.wait_for_timeout(400)
    ph = pg.evaluate("()=>(document.getElementById('onbPh')||{}).textContent||''")
    err = [e for e in pg.erreurs if 'version.json' not in e]; ctx.close()
    return t_ret, foc, d, foc2, ph, err
with sync_playwright() as p:
    b = p.webkit.launch()
    print('── avec un clavier simulé (visualViewport)')
    t_ret, foc, d, foc2, ph, err = parcours(b, True)
    juge('A · après Retour, le champ n\'a plus le focus : le clavier se ferme', not foc, 'focus encore sur le champ' if foc else '')
    tr = [x for x in d['tr'] if x[1] == 'onbDit']; rz = [x[0] for x in (d['kb'] or {}).get('resize', []) if x[0] > t_ret]
    fin_kb = max(rz) if rz else None; t_tr = tr[0][0] if tr else None
    juge('B · le premier tracé de « %s » commence APRÈS le clavier redescendu' % (d['dit'] or '?'), bool(tr) and bool(rz) and t_tr > fin_kb,
         'clavier redescendu à +%s ms ; premier tracé à +%s ms' % (round(fin_kb - t_ret) if fin_kb else '—', round(t_tr - t_ret) if t_tr else '—'))
    pend = [v for t, v in d['vis'] if fin_kb and t <= fin_kb and t > t_ret]
    juge('C · pendant que le clavier redescend, aucun texte de la page suivante n\'est visible', bool(pend) and not any(pend), '%d images relevées pendant la descente, %d avec du texte' % (len(pend), sum(1 for v in pend if v)))
    juge('E · la parole se saisit en touchant la phrase', foc2 and 'marcher une heure' in ph, 'focus %s · phrase « %s »' % (foc2, ph[:60]))
    juge('aucune erreur de page', not err, str(err[:2]))
    print('── sans clavier (le banc nu)')
    t_ret, foc, d, foc2, ph, err = parcours(b, False)
    tr = [x for x in d['tr'] if x[1] == 'onbDit']
    juge('D · sans clavier, le tracé part sans attendre (≤ 250 ms après Retour)', bool(tr) and tr[0][0] - t_ret <= 250, 'premier tracé à +%s ms' % (round(tr[0][0] - t_ret) if tr else '—'))
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
