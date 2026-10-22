#!/usr/bin/env python3
"""redteam_achat_valide.py — ⚑ v159 (Tom, C-170 complément) : NET DÈS LA VALIDATION DU PAIEMENT.

« C'est bon, mais la règle est plus large. À partir de l'écran de validation du paiement, TOUT ce qui est derrière est net, sur tous les écrans qui suivent,
pas seulement sur “Garder ton achat”. Avant la validation, le flou en flaques reste. Juge : chaque écran à partir de la validation du paiement est sans
aucun flou ni voile. »

Dans le prototype, la validation du paiement est le toucher qui achète (« Acheter sans compte » sur l'encart « Avant d'acheter ») : l'achat part de là.
Banc comme Tom (WebKit, la fenêtre de Safari : 390 × 692, l'appareil réduit à ≈ 0,79, ×3, doigt, Toile de 25 paroles, AUCUN compte) :
  A · AVANT : l'encart « Avant d'acheter » pose bien son flou (le flou en flaques reste) ;
  B · un monde du Studio acheté : image par image, de la validation à 4 s après (le déverrouillage, « Design débloqué », « Garder ton achat »), aucune
      couche floutée ni voile à l'écran — ni le fond du premier encart, ni un passage en flaques qui porte une image floutée (le déverrouillage compris),
      ni un élément à filtre ou à flou d'arrière-plan, ni le flou du verrou, ni voile sur l'hôte des encarts ;
  C · puis « Plus tard », le Studio refermé : l'accueil, 1,5 s image par image, sans flou ;
  D · l'offre Ma Parole ! achetée (« Bon, allez d'accord » → « Acheter sans compte ») : de même, 4 s après la validation.
Preuve : `--fichier=zz-v158.html` rougit (B : le passage flouté du déverrouillage et la sortie en flaques floutée du premier encart).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
ESPION = """()=>{ window.__F=[]; window.__val=0; window.__avant=[];
  document.addEventListener('click', e=>{ const t=e.target&&e.target.closest&&e.target.closest('#accRappelCompte .tard'); const h=document.getElementById('accRappelCompte');
    if(t && h && /Avant/.test(h.textContent||'') && !window.__val) window.__val=performance.now(); }, true);
  function flous(){ const D=document.getElementById('device').getBoundingClientRect(); const fl=[];
    document.querySelectorAll('#achatFond, canvas.passage-flaques, #stDeverrou').forEach(c=>{ const r=c.getBoundingClientRect(); if(!c.isConnected||r.width<2||r.bottom<D.top||r.top>D.bottom) return; const z=getComputedStyle(c); if(z.display==='none'||z.visibility==='hidden') return; if(c.id==='achatFond'||c.hasAttribute('data-flou')) fl.push(c.id||'passage flouté'); });
    document.querySelectorAll('#device *, .frame *').forEach(e=>{ const s=getComputedStyle(e); const bf=s.backdropFilter||s.webkitBackdropFilter; if((bf&&bf!=='none')||(s.filter&&/blur/.test(s.filter))){ const r=e.getBoundingClientRect(); let vu=r.width>2&&r.height>2&&r.right>D.left&&r.left<D.right&&r.bottom>D.top&&r.top<D.bottom; for(let q=e;vu&&q&&q.nodeType===1;q=q.parentElement){ const z=getComputedStyle(q); if(z.display==='none'||z.visibility==='hidden'||+z.opacity<0.02) vu=false; } if(vu) fl.push((e.id||e.className||e.tagName).toString().slice(0,30)+' '+(bf&&bf!=='none'?bf:s.filter)); } });
    const h=document.getElementById('accRappelCompte'); if(h && getComputedStyle(h).display!=='none'){ const v=getComputedStyle(h).backgroundColor; if(v!=='rgba(0, 0, 0, 0)' && v!=='transparent') fl.push('voile '+v); }
    return fl; }
  window.__flous=flous;
  (function f(){ const now=performance.now(); if(!window.__val){ const h=document.getElementById('accRappelCompte'); if(h && /Avant/.test(h.textContent||'')) window.__avant.push(flous().length); }
    else if(now-window.__val<(window.__duree||4000)) window.__F.push([Math.round(now-window.__val), flous().join(' ; ')]);
    requestAnimationFrame(f); })(); }"""
def contexte(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 692}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');}}catch(e){}")
    B.toile_pleine(ctx, 25); return ctx
def tard(pg, motif):
    for _ in range(40):
        t = pg.evaluate("m=>{ const h=document.getElementById('accRappelCompte'); if(!h||!new RegExp(m).test(h.textContent||'')) return null; const e=h.querySelector('.tard'); if(!e) return null; const r=e.getBoundingClientRect(); return r.width?[r.left+r.width/2, r.top+r.height/2]:null; }", motif)
        if t: pg.touchscreen.tap(t[0], t[1]); return True
        pg.wait_for_timeout(100)
    return False
def verdict(T, Fr, av=None):
    floues = [f for f in Fr if f[1]]
    if av is not None: juge('[%s] A · avant la validation, l\'encart « Avant d\'acheter » pose son flou' % T, av and max(av) > 0, 'images avec flou : %d / %d' % (sum(1 for x in av if x), len(av)))
    juge('[%s] B · de la validation à 4 s : aucune couche floutée ni voile (%d images)' % (T, len(Fr)), Fr and not floues, floues[:3])
with sync_playwright() as p:
    b = p.webkit.launch()
    for saut in (0, 9):
        ctx = contexte(b); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); }"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{ document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
        vus = 0
        for i in range(30):
            if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"):
                if vus >= saut: break
                vus += 1
            B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500)
        w = pg.evaluate("()=>window._lockedWorld"); T = 'Studio · %s' % w
        pg.evaluate(ESPION)
        c = pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
        pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1800)
        tard(pg, 'Avant'); pg.wait_for_timeout(4300)
        verdict(T, pg.evaluate("()=>window.__F"), pg.evaluate("()=>window.__avant"))
        tard(pg, 'Garder'); pg.wait_for_timeout(1200)
        B.tap_sel(pg, '#studioScreen .closeb')
        pg.evaluate("()=>{ window.__G=[]; const t0=performance.now(); (function f(){ if(performance.now()-t0<1500){ window.__G.push(window.__flous().join(' ; ')); requestAnimationFrame(f); } })(); }"); pg.wait_for_timeout(1800)
        G = pg.evaluate("()=>window.__G"); juge('[%s] C · « Plus tard », le Studio refermé : l\'accueil sans flou (%d images)' % (T, len(G)), G and not [g for g in G if g], [g for g in G if g][:2])
        er = [e for e in pg.erreurs if 'version.json' not in e]; juge('[%s] aucune erreur de page' % T, not er, er[:2]); ctx.close()
    # D · l'offre Ma Parole !
    ctx = contexte(b); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); var pl=document.getElementById('plusScreen'); if(pl) pl.classList.add('show'); try{ if(typeof buildCercleHero==='function') buildCercleHero(); }catch(e){} }"); pg.wait_for_timeout(1500)
    pg.evaluate(ESPION)
    bt = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#buyYear, #buyMonth')].find(x=>x.getBoundingClientRect().width>4); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]; }")
    if bt:
        pg.touchscreen.tap(bt[0], bt[1]); pg.wait_for_timeout(1800); ok = tard(pg, 'Avant'); pg.wait_for_timeout(4300)
        verdict('Ma Parole !', pg.evaluate("()=>window.__F"))
    else: juge('[Ma Parole !] D · le bouton d\'achat est à l\'écran', False, 'absent')
    er = [e for e in pg.erreurs if 'version.json' not in e]; juge('[Ma Parole !] aucune erreur de page', not er, er[:2]); ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
