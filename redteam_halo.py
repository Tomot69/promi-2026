# -*- coding: utf-8 -*-
"""redteam_halo.py — AUTOUR DE LA PELOTE, IL N'Y A QUE LA PAGE.

⚑ v136 (Tom, 7 oct. 2026, C-071) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_halo-avant-v136.py, 23 contrôles du mini halo
et de l'ombre de v119–v126). La décision qui remplace la règle d'avant, mot pour mot :
    « Le halo c'est une mauvaise idée en fait. […] Enlève tout ce qu'il y a comme effet autour de la Pelote pour le moment,
      ne masque pas, supprime. »
Ce que le juge protège (deux thèmes, « Réduire les animations », capture @3x) :
  A · ni `#auPeloteHalo`, ni `#auPeloteOmbre`, ni `#auPeloteFlaque`, ni aucun nœud `.au-halo` / `.au-ombre` : SUPPRIMÉS, pas masqués
  B · dans l'anneau de 125 à 150 pt autour du centre de la boule (la silhouette finit à 121), chaque pixel est le fond de la page
      (écart ≤ 3 niveaux par canal ; au plus 0,1 % de pixels au-delà)
  C · là où se tenait l'ombre (y 391 → 408, x 195 ± 56), chaque pixel est le fond de la page, même tolérance
  D · la colonne n'a pas bougé : « PARTAGER MA PELOTE » commence à 435,47 (composition B, v126), ± 0,5
Valeurs EN DUR (§7). Preuve : rouge sur l'état d'avant (APP=…/zz-av136.html : A, B et C).
"""
import io, sys, os
from playwright.sync_api import sync_playwright
from PIL import Image

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
S = 3; CX, CY = 195.0, 105.532 + 148.0; R0, R1 = 125.0, 150.0; BOUTON = 435.47; TOL = 3
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-78s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-78s KO  %s' % (nom, detail))


with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S, reduced_motion='reduce')
        pg = ctx.new_page()
        pg.add_init_script("try{localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("t=>{var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){ try{ setLight(t==='light'); }catch(e){ d.classList.toggle('light',t==='light'); } }}", th)
        pg.wait_for_timeout(400)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(4200)
        st = pg.evaluate("""()=>{const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
          const bt=document.getElementById('auPartage');
          return {clair:document.getElementById('device').classList.contains('light'),
            noeuds:['auPeloteHalo','auPeloteOmbre','auPeloteFlaque'].filter(i=>document.getElementById(i)).concat([].slice.call(document.querySelectorAll('.au-halo,.au-ombre')).map(e=>'.'+e.className)),
            bouton: bt? (bt.getBoundingClientRect().top-dv.top)/k : null, dv:[dv.left,dv.top,k]};}""")
        t('[%s] le thème est le bon' % T, st['clair'] == (th == 'light'))
        t('[%s] A · aucun nœud de halo, d\'ombre ni de flaque' % T, not st['noeuds'], str(st['noeuds']))
        f = 'scratchpad/v136/halo-%s.png' % th
        pg.screenshot(path=f, clip={'x': st['dv'][0], 'y': st['dv'][1], 'width': 390 * st['dv'][2], 'height': 844 * st['dv'][2]})
        im = Image.open(f).convert('RGB'); px = im.load(); e = im.width / 390.0
        fond = px[int(10 * e), int(CY * e)]
        def ecart(c): return max(abs(c[0] - fond[0]), abs(c[1] - fond[1]), abs(c[2] - fond[2]))
        n = 0; mauvais = 0; pire = 0
        for y in range(int((CY - R1) * e), int((CY + R1) * e)):
            for x in range(int((CX - R1) * e), int((CX + R1) * e)):
                d2 = ((x / e - CX) ** 2 + (y / e - CY) ** 2)
                if R0 * R0 <= d2 <= R1 * R1:
                    n += 1; d = ecart(px[x, y])
                    if d > TOL: mauvais += 1
                    if d > pire: pire = d
        t('[%s] B · l\'anneau 125–150 pt est le fond de la page' % T, n > 1000 and mauvais <= n * 0.001, '%d px · %d au-delà de %d niveaux · pire %d · fond %s' % (n, mauvais, TOL, pire, fond))
        n = 0; mauvais = 0; pire = 0
        for y in range(int(391 * e), int(408 * e)):
            for x in range(int(139 * e), int(251 * e)):
                n += 1; d = ecart(px[x, y])
                if d > TOL: mauvais += 1
                if d > pire: pire = d
        t('[%s] C · la place de l\'ombre est le fond de la page' % T, mauvais <= n * 0.001, '%d px · %d au-delà · pire %d' % (n, mauvais, pire))
        t('[%s] D · « PARTAGER MA PELOTE » à 435,47' % T, st['bouton'] is not None and abs(st['bouton'] - BOUTON) <= 0.5, str(st['bouton']))
        ctx.close()
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO : ' + ' · '.join(ko)); sys.exit(1)
