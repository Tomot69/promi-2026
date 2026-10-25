#!/usr/bin/env python3
"""redteam_garde_index.py — ⚑ v163 (Tom, C-149 suite, Q579) : LE GARDÉ DE CÔTÉ SE RECONNAÎT DANS L'INDEX ; SON MESSAGE Y MÈNE.

« La carte d'Index d'un gardé de côté se reconnaît au premier coup d'œil : un contour pointillé de 3 pt, le violet « en cours » #291547 en clair (sa
variante claire en sombre). Aucun aplat plein, aucune transparence. Q579 : toucher le message « gardé de côté — dans l'Index » ouvre l'Index déjà filtré
sur les gardés de côté. »
Banc comme Tom (WebKit ×3, doigt), Toile de 5 paroles, le vrai chemin (le +, la nature, le titre au clavier, « garder de côté » au doigt) :
  A · clair et sombre : la carte garde son champ (la couleur de sa nature, opaque) et porte un pointillé de 3 pt, #291547 en clair, #A77CF7 en sombre —
      lu sur l'IMAGE (le long du bord de la carte, une alternance de traits de cette couleur et de son champ) ;
  B · les autres cartes n'ont aucun pointillé ;
  C · au doigt, le message ouvre l'Index ; il ne montre que les gardés de côté ; le menu ⇅ dit « Gardés de côté ».
Preuve : `--fichier=zz-v162.html` rougit (A : 2 pt dans la couleur de la nature ; C : le message ne mène nulle part).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def proche(a, b, t=40): return sum(abs(x - y) for x, y in zip(a, b)) <= t
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'; ATT = '#A77CF7' if sombre else '#291547'
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
        B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(600); pg.keyboard.type('ranger la cave', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ const cs=document.getElementById('createSheet'), g=cs.querySelector('.pp-garder'); if(g && window._garderEtat) _garderEtat(cs, g); }"); pg.wait_for_timeout(300)
        B.tap_sel(pg, '#createSheet .pp-garder'); pg.wait_for_timeout(900)
        msg = pg.evaluate("()=>{ const t=document.getElementById('_toast'); if(!t) return null; const s=t.querySelector('span'); const r=s.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {t:s.textContent, x:(r.left+r.width/2-D.left)/k, y:(r.top+r.height/2-D.top)/k}; }")
        if not msg or 'Index' not in msg['t']:
            juge('[%s] le message « gardé de côté — dans l\'Index » paraît' % T, False, msg); ctx.close(); continue
        B.tap(pg, msg['x'], msg['y']); pg.wait_for_timeout(2800)
        r = pg.evaluate("()=>({ouvert:document.getElementById('indexSheet').classList.contains('show'), cartes:[...document.querySelectorAll('#indexList .s4-carte')].map(c=>[c.getAttribute('data-etat'), (c.querySelector('.s4-ti')||{}).textContent||'']), menu:[...document.querySelectorAll('#ixMenu .ix-mi.on[data-filt]')].map(x=>x.textContent.replace(/[^\\p{L} ]/gu,'').trim())})")
        ok = r['ouvert'] and r['cartes'] and all(c[0] == 'garde' for c in r['cartes']) and any('ranger la cave' in c[1] for c in r['cartes']) and r['menu'] == ['Gardés de côté']
        juge('[%s] C · le message, touché au doigt, ouvre l\'Index filtré sur les gardés de côté' % T, ok, r)
        # A et B : toutes les cartes
        pg.evaluate("()=>{ window.ixFiltre='tous'; buildIndex(); window._s4Index&&_s4Index(); }"); pg.wait_for_timeout(1500)
        info = pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
          return [...document.querySelectorAll('#indexList .s4-carte')].map(c=>{ c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(), s=getComputedStyle(c);
            return {etat:c.getAttribute('data-etat'), ol:s.outlineStyle+' '+s.outlineWidth, x0:r.left, y0:r.top, x1:r.right, y1:r.bottom, fond:s.backgroundColor}; }); }""")
        for c in info:
            if c['etat'] != 'garde':
                if c['ol'].startswith('dashed'): juge('[%s] B · une carte « %s » sans pointillé' % (T, c['etat']), False, c['ol'])
                continue
            pg.evaluate("()=>{ const c=document.querySelector('#indexList .s4-carte[data-etat=garde]'); c.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(500)
            g = pg.evaluate("()=>{ const c=document.querySelector('#indexList .s4-carte[data-etat=garde]'), r=c.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, getComputedStyle(c).outlineWidth, getComputedStyle(c).outlineStyle]; }")
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = im.size[0] / pg.viewport_size['width']
            # le bord gauche de la carte, 1,5 pt à l'intérieur, de 30 % à 70 % de sa hauteur : des traits de la couleur attendue, en alternance
            x = int((g[0] + 1.5) * k); ys = range(int((g[1] + (g[3] - g[1]) * 0.3) * k), int((g[1] + (g[3] - g[1]) * 0.7) * k))
            col = [im.getpixel((x, y)) for y in ys if 0 <= y < im.size[1] and 0 <= x < im.size[0]] or [(0, 0, 0)]; n = sum(1 for q in col if proche(q, rgb(ATT), 60))
            alterne = sum(1 for i in range(1, len(col)) if proche(col[i], rgb(ATT), 60) != proche(col[i - 1], rgb(ATT), 60))
            juge('[%s] A · le pointillé de 3 pt en %s, lu sur l\'image (traits et jours alternés)' % (T, ATT), g[5] == 'dashed' and abs(float(g[4][:-2]) - 3) < 0.1 and 0.2 <= n / len(col) <= 0.8 and alterne >= 4,
                 '%s %s · %d %% de traits, %d alternances' % (g[5], g[4], round(100 * n / len(col)), alterne))
            fond = im.getpixel((int((g[0] + g[2]) / 2 * k), int((g[1] + 30) * k)))
            juge('[%s] A · le champ reste plein (aucun aplat retiré, aucune transparence)' % T, not proche(fond, rgb('#F7F0DE'), 30) and not proche(fond, rgb('#050302'), 30), fond)
            break
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
