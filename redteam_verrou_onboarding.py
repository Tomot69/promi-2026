# -*- coding: utf-8 -*-
"""redteam_verrou_onboarding.py — E0, point 1 (ENGAGEMENT.md) : LE VERROU DE L'ONBOARDING.

« Playwright : stockage vierge → l'onboarding s'affiche ; le terminer ; recharger deux fois → il ne s'affiche plus. »
Chromium, au vrai doigt (CDP), stockage VIERGE (contexte neuf, rien n'est posé). On termine l'onboarding par son vrai chemin — le prénom,
la parole, le trait, le message de fin, le compte remis à plus tard — avec les poignées que `redteam_onboarding.py` utilise déjà.
Usage : python3 redteam_verrou_onboarding.py [fichier.html] [--sonde]   (--sonde retire le verrou avant de recharger : il doit rougir)
"""
import sys
from playwright.sync_api import sync_playwright
from redteam_onboarding import POIGNEE, toucher, tracer, PRENOM, PAROLE
F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'
ok = [0]; ko = []
def t(nom, c, d=''):
    if c: ok[0] += 1
    else: ko.append(nom)
    print('%s  %-74s %s' % ('OK' if c else 'KO', nom, str(d)[:200]))
VU = "()=>{ const o=document.getElementById('promiOnb'); if(!o) return false; const c=getComputedStyle(o), r=o.getBoundingClientRect(); return !o.classList.contains('gone') && c.display!=='none' && c.visibility!=='hidden' && +c.opacity>0.05 && r.width>100 && r.height>100; }"
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
    t('1 · stockage vierge : aucune clé au départ du contexte', pg.evaluate("()=>localStorage.getItem('promi_onb')") is None, pg.evaluate("()=>Object.keys(localStorage).join(', ')"))
    t('2 · stockage vierge : l\'onboarding s\'affiche', pg.evaluate(VU))
    # le terminer, par son vrai chemin
    pr = pg.evaluate(POIGNEE, '[data-onb="prenom"]')
    if pr:
        toucher(cdp, pr['x'], pr['y']); pg.wait_for_timeout(300); pg.keyboard.type(PRENOM, delay=30); pg.wait_for_timeout(200)
        s = pg.evaluate(POIGNEE, '[data-onb="suite"]')
        if s: toucher(cdp, s['x'], s['y'])
        else: pg.keyboard.press('Enter')
        pg.wait_for_timeout(1400)
    # ⚑ E2 (v140, C-075) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_verrou_onboarding-avant-v140.py) : le « vrai chemin » de l'onboarding est
    # maintenant le prénom, le principe, puis la VRAIE page + (un toucher sur la phrase fantôme, le trait qui plante). Le verrou garde sa règle.
    q = pg.evaluate(POIGNEE, '[data-onb="e2-suite"]')
    if q: toucher(cdp, q['x'], q['y'])
    try: pg.wait_for_function("()=>{const s=document.getElementById('createSheet'); return s&&s.classList.contains('show')&&s.classList.contains('pp-promi')&&!s.classList.contains('acc-passe')&&!!document.querySelector('#csPhrase [data-ph=titre]')}", timeout=9000)
    except Exception: pass
    pg.wait_for_timeout(1200)
    f = pg.evaluate("()=>{ const e=document.querySelector('#csPhrase [data-ph=titre]'); if(!e) return null; const r=e.getClientRects()[0]||e.getBoundingClientRect(); return r.width>4 ? {x:r.left+r.width/2, y:r.top+r.height/2} : null; }")
    if f: toucher(cdp, f['x'], f['y']); pg.wait_for_timeout(1300)
    P = pg.evaluate("()=>{ const e=window._ppEcran&&window._ppEcran(), cv=document.getElementById('csTrameCv'); if(!e||!cv||!e.base) return null; const r=cv.getBoundingClientRect(), k=r.width/390, f=window._onde.onde(e.base,e.amp), P=[]; for(let x=30;x<=360;x+=11) P.push([r.left+x*k, r.top+f(x)*k]); return P; }")
    z = bool(P)
    if P:
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': P[0][0], 'y': P[0][1]}]}); pg.wait_for_timeout(120)
        for (x, y) in P[1:]: cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(22)
        pg.wait_for_timeout(120); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(4500)
    pg.wait_for_timeout(2500)
    if '--dbg' in sys.argv:
        pg.screenshot(path='scratchpad/e0/verrou-fin.png')
        print(pg.evaluate("()=>{const o=document.getElementById('promiOnb'); return [...o.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);return r.width>4&&c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.05&&e.children.length===0}).map(e=>(e.id||e.className||e.tagName)+':'+(e.textContent||'').slice(0,30)+':'+(e.getAttribute('data-onb')||'')).slice(0,14)}"))
    e = pg.evaluate("()=>({onb:localStorage.getItem('promi_onb'), n:((typeof promises!=='undefined'&&promises)||[]).filter(p=>!p.draft).length})")
    t('3 · le parcours a été joué jusqu\'au bout (prénom, principe, phrase fantôme, trait qui plante)', bool(pr and q and f and z), 'prénom %s · principe %s · fantôme %s · trait %s' % (bool(pr), bool(q), bool(f), bool(z)))
    t('4 · terminé : l\'onboarding n\'est plus à l\'écran', not pg.evaluate(VU))
    t('5 · terminé : le verrou est posé (promi_onb = 1), un Promi est planté', e['onb'] == '1' and e['n'] == 1, e)
    if '--sonde' in sys.argv: pg.evaluate("()=>localStorage.removeItem('promi_onb')")   # la preuve : sans le verrou, les contrôles 6 et 7 doivent rougir
    for k in (1, 2):
        pg.reload(); pg.wait_for_timeout(6800)
        t('%d · rechargement n° %d : l\'onboarding ne s\'affiche plus' % (5 + k, k), not pg.evaluate(VU), 'promi_onb = %s' % pg.evaluate("()=>localStorage.getItem('promi_onb')"))
    t('8 · le Promi planté est toujours là après les rechargements', pg.evaluate("()=>((typeof promises!=='undefined'&&promises)||[]).filter(p=>!p.draft).length") == 1)
    t('9 · aucune erreur de page', not er, er[:2])
    b.close()
print('\nverrou de l\'onboarding : %d/%d' % (ok[0], ok[0] + len(ko)))
if ko: sys.exit(1)
