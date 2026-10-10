#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_remplace.py — DESSIN ↔ PHOTO : L'UN REMPLACE L'AUTRE, SANS RESTE (v140, Tom, 10 oct. 2026, C-086, C-085).

« Remplacer : on doit pouvoir passer d'un dessin à une photo et inversement, par le menu du bouton. Aujourd'hui, après un dessin, on ne
peut plus mettre de photo. — Bug : quand on importe une photo, une bande parasite apparaît au-dessus du trait […]. La photo remplace
entièrement ce qui était dans la bande, sans aucun reste. Juge : dessin → photo → dessin → photo sur la même fiche, sans résidu à l'écran. »

WebKit, une fiche Promi à tenir, clair et sombre. La photo passe par le VRAI champ de fichier du bouton (événement `change`), le dessin par
l'outil (traits tracés, POSER). La bande se lit sur l'IMAGE (de 104 pt au trait − 12 pt) :
  0 · la référence : la photo seule, sur la fiche qui n'a jamais eu de dessin ;
  1 · dessin posé : la bande montre le dessin (aucun pixel aux couleurs de la photo), le menu offre « Importer une photo » ;
  2 · photo importée : la bande est celle de la référence, au pixel (≤ 0,2 % d'écart) ; plus de dessin (ni donnée, ni couche, ni œil) ;
      le menu offre « Dessiner » ;
  3 · dessin posé de nouveau : plus de photo (ni donnée ni pixel) ;
  4 · photo de nouveau : la référence, au pixel.
Preuve : rouge sur l'état d'avant (python3 redteam_remplace.py zz-av140.html).
"""
import sys, io, os, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
# une photo aux couleurs qu'aucun dessin ni aucune dalle ne porte : magenta vif et vert vif en damier
tmp = os.path.join(tempfile.gettempdir(), '_remplace.png')
im = Image.new('RGB', (600, 800)); px = im.load()
for y in range(800):
    for x in range(600): px[x, y] = (255, 0, 200) if ((x // 60 + y // 60) % 2 == 0) else (0, 230, 40)
im.save(tmp)
def photo_px(c): return (c[0] > 200 and c[1] < 70 and c[2] > 150) or (c[0] < 70 and c[1] > 190 and c[2] < 100)
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}" % th)
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        inf = pg.evaluate("()=>{ const q=promises.find(p=>p.status!=='tenu'&&!p.done&&!p.chiche&&!p.nuee&&!p.draft)||promises[0]; window.__q=q; q.photo=null; delete q.dessin; openDetail(q.id); return q.title; }"); pg.wait_for_timeout(3200)
        geo = pg.evaluate("()=>{ const d=document.getElementById('device').getBoundingClientRect(); const e=window._ficheEcran(document.getElementById('detailPoster'), window.__q); return [d.left,d.top,d.width/390,e.base,e.amp]; }")
        haut, bas = 104, geo[3] - geo[4] - 12
        def bande():
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': geo[0], 'y': geo[1] + haut * geo[2], 'width': 390 * geo[2], 'height': (bas - haut) * geo[2]}))).convert('RGB'); return im
        def etat(): return pg.evaluate("()=>{ const q=window.__q, h=document.getElementById('detailPoster'); return {photo:!!q.photo, dessin:!!(q.dessin&&q.dessin.poses&&q.dessin.poses.length), couche:!!h.querySelector(':scope > canvas.dz-bande'), oeil:!!h.querySelector(':scope > button.dz-oeil')}; }")
        def importe():
            pg.set_input_files('#detailPoster .ph-photo-in', tmp); pg.wait_for_timeout(2200)
        def dessine(n):
            pg.evaluate("()=>_dessin.ouvre()"); pg.wait_for_timeout(900)
            r = pg.evaluate("()=>{const s=document.querySelector('#dessinMode canvas'); const r=s.getBoundingClientRect(); return [r.left,r.top]}")
            pg.mouse.move(r[0] + 50, r[1] + 150 + 30 * n); pg.mouse.down()
            for i in range(22): pg.mouse.move(r[0] + 50 + i * 13, r[1] + 150 + 30 * n + (i % 4) * 16); pg.wait_for_timeout(12)
            pg.mouse.up(); pg.wait_for_timeout(250); pg.evaluate("()=>_dessin.sort(true)"); pg.wait_for_timeout(1500)
        def menu():
            pg.evaluate("()=>{ try{window._photoMenuFerme()}catch(e){} document.querySelector('#detailPoster .ph-photo-btn').click(); }"); pg.wait_for_timeout(350)
            L = pg.evaluate("()=>[].map.call(document.querySelectorAll('#detailPoster .ph-photo-menu button'), b=>b.textContent)"); pg.evaluate("()=>{ try{window._photoMenuFerme()}catch(e){} }"); return L
        def part_photo(im):
            d = im.getdata(); n = sum(1 for c in d if photo_px(c)); return 100.0 * n / len(d)
        def ecart(a, b_):
            da, db = a.getdata(), b_.getdata(); n = sum(1 for i in range(0, len(da), 3) if abs(da[i][0] - db[i][0]) + abs(da[i][1] - db[i][1]) + abs(da[i][2] - db[i][2]) > 36); return 100.0 * n / (len(da) / 3.0)
        # 0 · la référence
        importe(); REF = bande(); e0 = etat(); pr = part_photo(REF)
        juge('[%s] 0 · la référence : la photo seule est dans la bande' % T, e0['photo'] and not e0['dessin'] and pr > 15, '%s · %.1f %% de la bande aux couleurs de la photo' % (e0, pr))
        pg.evaluate("()=>{ window.__q.photo=null; delete window.__q.photoCadre; _ficheTrait(); }"); pg.wait_for_timeout(1200)
        # 1 · dessin
        dessine(0); e1 = etat(); B1 = bande(); m1 = menu()
        juge('[%s] 1 · dessin posé : la bande montre le dessin, sans un pixel de photo' % T, e1['dessin'] and e1['couche'] and not e1['photo'] and part_photo(B1) < 0.05, '%s · photo %.2f %%' % (e1, part_photo(B1)))
        juge('[%s] 1 · le menu offre « Importer une photo »' % T, 'Importer une photo' in m1, str(m1))
        # 2 · photo
        importe(); e2 = etat(); B2 = bande(); m2 = menu(); ec2 = ecart(B2, REF)
        juge('[%s] 2 · dessin → photo : la bande est celle de la photo seule, sans reste (≤ 0,2 %%)' % T, ec2 <= 0.2 and part_photo(B2) > 15, 'écart à la référence %.2f %% · photo %.1f %%' % (ec2, part_photo(B2)))
        juge('[%s] 2 · plus de dessin : ni donnée, ni couche, ni œil' % T, e2['photo'] and not e2['dessin'] and not e2['couche'] and not e2['oeil'], str(e2))
        juge('[%s] 2 · le menu offre « Dessiner »' % T, 'Dessiner' in m2 and 'Retirer le dessin' not in m2, str(m2))
        # 3 · dessin de nouveau
        dessine(1); e3 = etat(); B3 = bande()
        juge('[%s] 3 · photo → dessin : plus de photo, ni donnée ni pixel' % T, e3['dessin'] and e3['couche'] and not e3['photo'] and part_photo(B3) < 0.05, '%s · photo %.2f %%' % (e3, part_photo(B3)))
        # 4 · photo de nouveau
        importe(); e4 = etat(); B4 = bande(); ec4 = ecart(B4, REF)
        juge('[%s] 4 · dessin → photo, encore : la référence, sans reste (≤ 0,2 %%)' % T, ec4 <= 0.2 and e4['photo'] and not e4['dessin'] and not e4['couche'], 'écart %.2f %% · %s' % (ec4, e4))
        if th == 'light':
            pg.screenshot(path='scratchpad/v140/remplace-%s.png' % FICHIER.replace('.html', ''), clip={'x': geo[0], 'y': geo[1], 'width': 390 * geo[2], 'height': 520 * geo[2]})
        juge('[%s] aucune erreur de page' % T, not er, str(er[:2])); ctx.close()
    b.close()
print('\n%d/%d' % (ok, ok + len(ko)))
if ko: sys.exit(1)
