#!/usr/bin/env python3
"""redteam_effacer_net.py — ⚑ v179a (Tom, C-233) : « TOUT EFFACER » SANS LATENCE.

« Après la confirmation, l'effacement est immédiat : on passe directement à « Toi, c'est … ? », sans jamais revoir l'ancienne Toile, même une image. »
Banc WebKit ×3, au doigt, sur l'état exporté de Tom, puis sur une Toile de 10 paroles en sombre :
  A · la feuille « Tout effacer ? » ; « Effacer » touché ;
  B · aucune image de l'ancien état après la confirmation : chaque image prise (≈ toutes les 60 à 150 ms) est soit l'aplat d'ouverture de l'onboarding
      (#DFCAA4, ≥ 98 % de l'appareil à ± 8), soit le nouveau chargement — jamais l'ancien document avec autre chose que l'aplat ;
  C · l'aplat (la première image de l'onboarding) au plus 500 ms après le toucher ; le nouveau chargement porte l'onboarding (« Toi, c'est … ? ») ;
  D · le stockage ne garde rien de l'ancien état (ni paroles, ni prénom) ; aucune erreur de page.
Rouge sur v178 (`--fichier=zz-v178.html`) : 5 s de l'ancienne Toile.
"""
import sys, time, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
def uni(png, R):
    im = Image.open(io.BytesIO(png)).convert('RGB'); x0, y0, w, h = [int(v * 3) for v in R]
    im = im.crop((x0 + 30, y0 + 60, x0 + w - 30, y0 + h - 60)).resize((60, 120)); px = list(im.getdata())
    return sum(1 for c in px if abs(c[0] - 223) <= 8 and abs(c[1] - 202) <= 8 and abs(c[2] - 164) <= 8) / len(px)
def cas(b, nom, ctx):
    pg = B.ouvre(ctx, F, 7000)
    B.tap_sel(pg, '#settingsBtn'); pg.wait_for_timeout(1800)
    pg.evaluate("()=>document.getElementById('resetData').scrollIntoView({block:'center'})"); pg.wait_for_timeout(500)
    B.tap_sel(pg, '#resetData'); pg.wait_for_timeout(900)
    f = pg.evaluate("()=>{ const v=document.getElementById('v16Conf'); return v ? [v.querySelector('.v16-conf-t').textContent, v.querySelector('.v16-oui').textContent] : null; }")
    juge('[%s] A · la feuille « Tout effacer ? », « Effacer »' % nom, f and 'Tout effacer' in f[0] and f[1] == 'Effacer', f)
    R = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    pg.evaluate("()=>{ window.__ancien=1; }")
    o = pg.evaluate("()=>{const r=document.querySelector('#v16Conf .v16-oui').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}")
    t0 = time.time(); pg.touchscreen.tap(o[0], o[1])
    vus = []; t_aplat = None; t_onb = None
    while time.time() - t0 < 7:
        t = time.time() - t0
        try: anc = pg.evaluate("()=>window.__ancien===1")
        except Exception: anc = None
        try: png = pg.screenshot()
        except Exception: continue
        u = uni(png, R); vus.append((round(t, 2), anc, round(u, 3)))
        if t_aplat is None and u >= 0.98: t_aplat = t
        if anc is False:
            try:
                if pg.evaluate("()=>!!document.getElementById('promiOnb') && /Toi, c/.test(document.getElementById('promiOnb').textContent)"): t_onb = t_onb or t
            except Exception: pass
        if t_onb and t > t_onb + 1.5: break
    ancien = [v for v in vus if v[1] is not False and v[2] < 0.98]
    juge('[%s] B · aucune image de l\'ancien état après la confirmation (%d images lues)' % (nom, len(vus)), not ancien and len(vus) >= 4, ancien[:4])
    juge('[%s] C · l\'aplat d\'ouverture de l\'onboarding au plus 500 ms après le toucher' % nom, t_aplat is not None and t_aplat <= 0.5, '%s s' % (None if t_aplat is None else round(t_aplat, 2)))
    juge('[%s] C · le nouveau chargement porte « Toi, c\'est … ? »' % nom, t_onb is not None, '%s s (document neuf)' % (None if t_onb is None else round(t_onb, 2)))
    pg.wait_for_timeout(1500)
    st = pg.evaluate("()=>{ var s=localStorage.getItem('promi_state')||''; return [localStorage.length, s.length, Object.keys(localStorage)]; }")
    juge('[%s] D · plus rien de l\'ancien état dans le stockage ; aucune erreur de page' % nom, st[1] < 400 and not pg.erreurs, [st, pg.erreurs[:2]])
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx, d = B.contexte_tom(b)
    if ctx: cas(b, 'état de Tom', ctx)
    ctx = B.contexte(b, sombre=True); B.toile_pleine(ctx, 10); cas(b, 'sombre · 10 paroles', ctx)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
