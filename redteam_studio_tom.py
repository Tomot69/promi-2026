#!/usr/bin/env python3
"""
redteam_studio_tom.py — LES MURS DU STUDIO, AU VRAI TOUCHER, PAR LE CHEMIN DE TOM (v142, Tom, 11 oct. 2026 — C-100, RÉCIDIVE).

« Refais l'essai au vrai toucher tactile, dans WebKit, sur chaque zone floutée du Studio, par le chemin réel (Studio ouvert depuis l'accueil,
en gratuit, sur un monde de Ma Parole !) : la phrase doit apparaître sur le flou touché, dès le premier toucher, vingt fois sur vingt, et
rester lisible. »

POURQUOI LE JUGE DE v141 (redteam_murs_toucher) ÉTAIT VERT : il jouait dans Chromium (CDP), et ne touchait que le PANNEAU du bas. La plus grande
zone floutée du Studio — la Toile elle-même, floutée à 1,4 px sur un monde de Ma Parole ! — n'était pas un mur : touchée, elle ne répondait
jamais. Et dans WebKit un toucher ne produisait aucun évènement de pointeur : le mur, qui n'écoutait qu'eux, n'entendait rien.

Banc « comme Tom » (banc_tom.py) : WebKit, 390 × 844 ×3, tactile (`touchscreen.tap` : touchstart / touchend), gratuit, Studio ouvert en touchant
STUDIO sur l'accueil, monde changé en glissant jusqu'au premier monde de Ma Parole !. Trois zones : la Toile floutée, le panneau du bas, le
panneau des palettes. Vingt touchers chacune, répartis sur toute la zone ; après chacun : la phrase est levée, SON CENTRE EST DANS LA ZONE
TOUCHÉE, l'offre ne s'est pas ouverte. Lisible : sur le panneau, rien d'autre que la phrase (ses bandes sont retirées le temps de la
lecture) ; sur la Toile, la phrase est cernée du fond du mode (9 px, en dur) et le nom du monde s'efface.

Usage : python3 redteam_studio_tom.py [fichier.html] [--planche]
"""
import sys, time
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = 20
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
ETAT = """()=>{ const m=document.getElementById('murPhrase'), dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; const r=m&&m.getBoundingClientRect(); const c=m?getComputedStyle(m):null;
  const vis=s=>[...document.querySelectorAll(s)].some(e=>{const q=getComputedStyle(e); return q.visibility!=='hidden'&&q.display!=='none'&&e.getBoundingClientRect().height>1;});
  return {leve:!!(m&&m.classList.contains('leve')), offre:!!document.querySelector('#plusScreen.show'), cy:r?(r.top+r.height/2-dv.top)/k:null, cx:r?(r.left+r.width/2-dv.left)/k:null,
    cerne:c?parseFloat(c.webkitTextStrokeWidth||'0'):0, bandes:vis('#stpTons, #stpVue, #stpLab'), nom:vis('#studioScreen .stp-m'), pastilles:vis('#stpPals .st3-p'), texte:m?m.textContent:''}; }"""
ZONES = """()=>{ const dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; const R=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), c=getComputedStyle(e); if(r.height<8||c.display==='none'||c.visibility==='hidden') return null; return [(r.left-dv.left)/k,(r.top-dv.top)/k,(r.right-dv.left)/k,(r.bottom-dv.top)/k];};
  const fl=s=>{const e=document.querySelector(s); return e?getComputedStyle(e).filter:''};
  return {panneau:R('#studioScreen #stpBas'), pals:R('#studioScreen #stpPals'), achat:R('#stLockBuy'), flouToile:fl('#stBg'), cls:document.getElementById('studioScreen').className}; }"""
BAISSE = "()=>{ try{ _murBaisse(); }catch(e){} const c=document.querySelector('#plusScreen.show .closeb'); if(c) c.click(); }"
def studio(b, sombre, pals):
    ctx = contexte(b, sombre=sombre, stockage={'promi_murs': '{"n":3,"t":%d,"der":2,"decouvert":1}' % (time.time() * 1000)}); pg = ouvre(ctx, F)
    tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(6000)
    if pals: tap(pg, 75, 620); pg.wait_for_timeout(1500)
    for k in range(14):
        glisse(pg, droite((320, 300), (80, 300), 10), pas=16); pg.wait_for_timeout(1600)
        if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
    pg.wait_for_timeout(2500); return ctx, pg
def vingt(nom, pg, zone, attendu, cap=None):
    x0, y0, x1, y1 = zone; bons = 0; rates = []; lis = True; e = None
    for i in range(N):
        x = x0 + 14 + (x1 - x0 - 28) * ((i % 5) + 0.5) / 5.0; y = y0 + 10 + (y1 - y0 - 20) * ((i // 5) + 0.5) / 4.0
        tap(pg, x, y); pg.wait_for_timeout(650); e = pg.evaluate(ETAT)
        dedans = e['cy'] is not None and y0 - 2 <= e['cy'] <= y1 + 2
        if e['leve'] and not e['offre'] and dedans: bons += 1
        else: rates.append('(%d ; %d)%s%s' % (x, y, ' offre' if e['offre'] else '', '' if e['leve'] else ' rien') + ('' if dedans or not e['leve'] else ' phrase à y %s' % (e['cy'] and round(e['cy']))))
        if e['leve'] and not attendu(e): lis = False
        if cap and i == 7: capture(pg, cap)
        pg.evaluate(BAISSE); pg.wait_for_timeout(420)
    juge('%s : la phrase sur le flou touché, dès le premier toucher — %d sur %d' % (nom, bons, N), bons == N, ('ratés : ' + ' '.join(rates[:8])) if rates else 'zone %d → %d' % (y0, y1))
    return lis
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        th = 'sombre' if sombre else 'clair'
        ctx, pg = studio(b, sombre, False); z = pg.evaluate(ZONES)
        juge('[%s] le Studio est ouvert depuis l\'accueil, en gratuit, sur un monde de Ma Parole ! (Toile floutée)' % th, 'world-locked' in z['cls'] and 'blur' in (z['flouToile'] or ''), z['flouToile'])
        if z['panneau'] and z['achat']:
            cap = ('planche-v142/mur-%s-%s-toile.png' % (F.replace('.html', ''), th)) if '--planche' in sys.argv else None
            lis = vingt('[%s] la Toile floutée' % th, pg, [0, 108, 390, z['achat'][1] - 6], lambda e: e['cerne'] >= 8.5 and not e['nom'], cap)
            juge('[%s] la Toile floutée : la phrase reste lisible (cernée du fond du mode, le nom du monde effacé)' % th, lis)
            cap = ('planche-v142/mur-%s-%s-panneau.png' % (F.replace('.html', ''), th)) if '--planche' in sys.argv else None
            lis = vingt('[%s] le panneau du bas' % th, pg, z['panneau'], lambda e: not e['bandes'], cap)
            juge('[%s] le panneau du bas : la phrase reste lisible (seule sur le panneau)' % th, lis)
        else: juge('[%s] le panneau et le bouton d\'achat sont à l\'écran' % th, False, str(z))
        ctx.close()
        ctx, pg = studio(b, sombre, True); z = pg.evaluate(ZONES)
        if z['pals']:
            cap = ('planche-v142/mur-%s-%s-palettes.png' % (F.replace('.html', ''), th)) if '--planche' in sys.argv else None
            lis = vingt('[%s] le panneau des palettes' % th, pg, [z['pals'][0], z['pals'][1] + 60, z['pals'][2], z['pals'][3]], lambda e: not e['pastilles'], cap)
            juge('[%s] le panneau des palettes : la phrase reste lisible (seule sur le panneau)' % th, lis)
        else: juge('[%s] le panneau des palettes est ouvert' % th, False, str(z))
        ctx.close()
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
