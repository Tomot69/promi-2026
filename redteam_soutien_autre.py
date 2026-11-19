#!/usr/bin/env python3
"""
redteam_soutien_autre.py — v213 (Tom, 19 nov. 2026, C-313) : « Soutenir Promi », l'option « Autre montant ».

Décisions portées EN DUR :
  · la rangée d'avant ne change pas : 5 · 10 · 25 · 50 · 100 € ;
  · « Autre montant » à sa suite, dans le même style (2 px, rayon = h ÷ 2, même police) ;
  · au toucher, il déroule en douceur (C-271) les paliers 15 · 20 · 30 · 40 · 75 · 150 · 200 · 250 · 300 · 500 · 750 · 1 000 € ;
    au second toucher, il les replie de même ; rien n'apparaît ni ne disparaît d'une image à l'autre, la suite (le merci) glisse avec la boîte ;
  · aucun chevauchement, rien hors de l'écran, aux échelles 1 (430 × 932) et 0,79 (330 × 714), clair et sombre ;
  · un palier touché montre le merci, visible à l'écran.
Le mouvement est relevé DANS la page, à chaque image (requestAnimationFrame), jamais par des captures espacées.
`--sonde` : la transition retirée (la boîte change de taille d'un coup) — B et E rougissent.
"""
import sys, re
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B

RANGEE = ['5 €', '10 €', '25 €', '50 €', '100 €']
PALIERS = ['15 €', '20 €', '30 €', '40 €', '75 €', '150 €', '200 €', '250 €', '300 €', '500 €', '750 €', '1 000 €']
SONDE = '--sonde' in sys.argv
OK = []; KO = []
def juge(nom, cond, det=''):
    (OK if cond else KO).append(nom); print(('  ✅ ' if cond else '  ❌ ') + nom + ('' if cond else '  — ' + str(det)))

RELEVE = """()=>{ window.__soR=[]; var s=document.getElementById('soutienScreen'), a=s.querySelector('.so-autres'), b=s.querySelector('.so-autre'), m=s.querySelector('.so-merci'), t0=performance.now();
  (function f(){ var ra=a.getBoundingClientRect(), rb=b.getBoundingClientRect(), rm=m.getBoundingClientRect(), k=ra.width/(a.offsetWidth||1);
    window.__soR.push({t:performance.now()-t0, h:ra.height/k, top:ra.top/k, bas:ra.bottom/k, autre:rb.bottom/k, merci:rm.top/k});
    if(performance.now()-t0<900) requestAnimationFrame(f); })(); }"""
GEO = """()=>{ var s=document.getElementById('soutienScreen'), d=document.getElementById('device').getBoundingClientRect(), co=s.querySelector('.so-corps').getBoundingClientRect();
  var L=[].slice.call(s.querySelectorAll('.so-m')).map(function(e){ var r=e.getBoundingClientRect(); var a=e.closest('.so-autres'); var vis=!a || a.getBoundingClientRect().height>1;
     return {t:e.textContent.replace(/\\s+/g,' ').trim(), l:r.left, r:r.right, h:r.top, b:r.bottom, vis:vis, bw:getComputedStyle(e).borderTopWidth, rad:getComputedStyle(e).borderTopLeftRadius, ff:getComputedStyle(e).fontFamily, fs:getComputedStyle(e).fontSize}; });
  return {d:[d.left,d.top,d.right,d.bottom], co:[co.top,co.bottom], L:L}; }"""

def mouvement(R, nom, ouvre):
    hs = [r['h'] for r in R]; total = max(hs) - min(hs)
    juge(nom + ' : la boîte change de taille (%.0f pt)' % total, total > 200, hs[:3])
    pas = [abs(hs[i+1] - hs[i]) for i in range(len(hs)-1)]
    inter = [h for h in hs if min(hs) + 2 < h < max(hs) - 2]
    juge(nom + ' : en douceur — au moins 6 images entre les deux tailles (%d)' % len(inter), len(inter) >= 6, len(inter))
    juge(nom + ' : aucun saut — le plus grand pas fait %.0f pt (≤ 45 %% du mouvement)' % max(pas), max(pas) <= 0.45 * total, max(pas))
    mono = all((hs[i+1] - hs[i]) * (1 if ouvre else -1) >= -0.5 for i in range(len(hs)-1))
    juge(nom + ' : un seul sens, jamais d\'aller-retour', mono)
    ec = [r['merci'] - r['bas'] for r in R]
    juge(nom + ' : la suite (le merci) glisse avec la boîte (écart constant à 1 pt)', max(ec) - min(ec) <= 1, (min(ec), max(ec)))

def geometrie(g, nom, ouvert):
    L = [x for x in g['L'] if x['vis']]
    noms = [x['t'] for x in L]
    att = RANGEE + ['Autre montant'] + (PALIERS if ouvert else [])
    juge(nom + ' : les montants, dans l\'ordre', [n for n in noms] == att, noms)
    ch = []
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            A, Bx = L[i], L[j]
            if min(A['r'], Bx['r']) - max(A['l'], Bx['l']) > 0.5 and min(A['b'], Bx['b']) - max(A['h'], Bx['h']) > 0.5: ch.append((A['t'], Bx['t']))
    juge(nom + ' : aucun chevauchement', not ch, ch[:4])
    d = g['d']; hors = [x['t'] for x in L if x['l'] < d[0] - 0.5 or x['r'] > d[2] + 0.5]
    juge(nom + ' : rien ne sort de l\'écran en largeur', not hors, hors)
    au = [x for x in g['L'] if x['t'] == 'Autre montant'][0]; m5 = [x for x in g['L'] if x['t'] == '5 €'][0]
    juge(nom + ' : « Autre montant » dans le même style (trait, rayon = h ÷ 2, police, taille)',
         au['bw'] == m5['bw'] and au['ff'] == m5['ff'] and au['fs'] == m5['fs'] and abs(float(au['rad'][:-2]) - (au['b'] - au['h']) / 2 / ((d[2]-d[0])/390)) < 1.5, (au, m5))
    if ouvert:
        der = [x for x in L if x['t'] == PALIERS[-1]][0]
        juge(nom + ' : le dernier palier est à l\'écran, dans le corps', der['b'] <= min(g['co'][1], d[3]) + 0.5, (der['b'], g['co'], d))

with sync_playwright() as p:
    b = p.webkit.launch()
    # « avec la Toile » : la page telle que sur l'iPhone quand la Toile de l'écran « Ma Parole ! » y est recopiée (le corps commence plus bas : il faut défiler)
    for sombre, vw, vh, ech, toile in ((False, 430, 932, '1', 0), (True, 430, 932, '1', 0), (False, 330, 714, '0,79', 0), (True, 330, 714, '0,79', 0), (False, 430, 932, '1', 1), (True, 330, 714, '0,79', 1)):
        th = 'sombre' if sombre else 'clair'; tag = '%s, échelle %s%s' % (th, ech, ', avec la Toile' if toile else '')
        print('— ' + tag)
        ctx = B.contexte(b, sombre=sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, 'app.html'); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
        if SONDE: pg.add_style_tag(content='#soutienScreen .so-autres{transition:none!important}')
        pg.evaluate("()=>{closeAll(); document.getElementById('settingsBtn').click(); setTimeout(()=>window._soutienPage(),600)}"); pg.wait_for_timeout(1700)
        if toile: pg.evaluate("()=>document.getElementById('soutienScreen').classList.remove('so-sans')"); pg.wait_for_timeout(200)
        geometrie(pg.evaluate(GEO), tag + ' · replié', False)
        juge(tag + ' · replié : les paliers ne se voient pas (boîte de hauteur 0)', pg.evaluate("()=>document.querySelector('#soutienScreen .so-autres').getBoundingClientRect().height") < 0.5)
        pg.evaluate(RELEVE); B.tap_sel(pg, '#soutienScreen .so-autre'); pg.wait_for_timeout(1100)
        mouvement(pg.evaluate("()=>window.__soR"), tag + ' · ouverture', True)
        juge(tag + ' · ouvert : aria-expanded vrai', pg.evaluate("()=>document.querySelector('#soutienScreen .so-autre').getAttribute('aria-expanded')") == 'true')
        geometrie(pg.evaluate(GEO), tag + ' · ouvert', True)
        pg.evaluate(RELEVE); B.tap_sel(pg, '#soutienScreen .so-autre'); pg.wait_for_timeout(1100)
        mouvement(pg.evaluate("()=>window.__soR"), tag + ' · fermeture', False)
        geometrie(pg.evaluate(GEO), tag + ' · refermé', False)
        # choisir un palier
        B.tap_sel(pg, '#soutienScreen .so-autre'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ var x=[].slice.call(document.querySelectorAll('#soutienScreen .so-autres .so-m')).filter(e=>/750/.test(e.textContent))[0]; x.scrollIntoView({block:'nearest'}); }"); pg.wait_for_timeout(300)
        B.tap_sel(pg, '#soutienScreen .so-autres .so-m:nth-child(11)'); pg.wait_for_timeout(1500)
        mv = pg.evaluate("()=>{ var m=document.querySelector('#soutienScreen .so-merci'), r=m.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return [getComputedStyle(m).visibility, r.top, r.bottom, d.bottom]; }")
        juge(tag + ' · un palier touché : le merci paraît, à l\'écran', mv[0] == 'visible' and mv[2] <= mv[3] + 0.5, mv)
        # rouvrir l'écran : replié
        pg.evaluate("()=>{ document.querySelector('#soutienScreen .closeb').click(); setTimeout(()=>window._soutienPage(),500); }"); pg.wait_for_timeout(1200)
        juge(tag + ' · rouvert : replié, en haut', pg.evaluate("()=>[document.querySelector('#soutienScreen .so-autres').getBoundingClientRect().height, document.querySelector('#soutienScreen .so-corps').scrollTop]") == [0, 0])
        juge(tag + ' : aucune erreur de page', not err, err[:2])
        ctx.close()
    b.close()
print('\n%d/%d' % (len(OK), len(OK) + len(KO)))
sys.exit(1 if KO else 0)
