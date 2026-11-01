#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_flash_etat.py — PAS DE FLASH ORANGE À L'OUVERTURE D'UNE FICHE « À TENIR » EN SOMBRE (v122, Tom, Q374, 3 oct. 2026).

« À l'ouverture d'une fiche « à tenir » en sombre, l'à-qui, l'échéance et « trace pour tenir » restent 1 à 2 s en orange avant de passer à
la crème. La couleur finale doit être posée dès la première image. Juge : vingt ouvertures, avec une capture à la première image, et aucun
orange sur ces trois éléments. »

Valeurs EN DUR (§7) : la crème #F7F0DE = rgb(247, 240, 222) (décision v16 / Q290 : les textes d'état sur fond sombre passent crème) ;
l'orange d'état #DD4D23 = rgb(221, 77, 35).
Pour chacune des vingt ouvertures (WebKit, sombre, « faire les crêpes ») :
  1 · dans la page, à CHAQUE image depuis `openDetail` jusqu'à 1,5 s, la couleur calculée des trois éléments : aucune n'est l'orange, et la
      première image où ils paraissent les montre déjà crème ;
  2 · une capture prise dès que la fiche paraît : dans le rectangle de chacun des trois éléments, aucun pixel proche de l'orange (ΔRVB ≤ 40).
Preuve (§7) : sur `sauvegardes/app-avant-v122.html` il ROUGIT (orange de ~400 ms à ~1 s, à chaque ouverture).

⚑ v123 (Tom, Q375) — « À l'ouverture d'une fiche, la première image porte encore l'état de la fiche précédente pendant environ 200 ms.
L'état juste dès la première image. » Contrôle 3 : trois enchaînements (une fiche, on la ferme, on ouvre la suivante), cinq fois chacun,
dans le thème où l'écart se voit — Chiche tenu → Chiche lancé (clair) · Promi tenue → Promi à tenir (clair) · Promi à tenir → Promi
tenue (sombre). À la PREMIÈRE image où la fiche paraît (premier `requestAnimationFrame` après l'ouverture, donc ce qui va être peint),
le MOT et la COULEUR de l'à-qui, de l'échéance et de la phrase du trait sont déjà ceux de l'état posé (relevés à 1,5 s).
Preuve : sur `sauvegardes/app-avant-v123.html` il ROUGIT.
"""
import os, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image

FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = 20
CREME, ORANGE = 'rgb(247, 240, 222)', 'rgb(221, 77, 35)'
# ⚑ v130 (Tom, 5 oct. 2026) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_flash_etat-avant-v130.py).
#   La règle d'avant : « les textes d'état sur fond sombre passent crème » (v16, Q290) — le corps sombre d'un Promi ÉTAIT sombre.
#   La décision qui la remplace sur la fiche Promi : le corps sombre devient Tropical Breeze #8ACBE8 et « le texte posé sur ce corps
#   passe à l'encre #201908 (titre, à-qui, échéance, mentions) ». Le contrôle protège la même chose — la couleur FINALE dès la
#   première image, jamais l'orange — avec la valeur d'aujourd'hui.
ENCRE = 'rgb(32, 25, 8)'
# ⚑ v131 (Tom, 5 oct. 2026) — Tropical Breeze est écarté, le corps sombre d'un Promi est le cobalt #273CEB : « le texte posé sur ce corps
#   redevient crème #F7F0DE, comme avant ». Le contrat revient à la crème (v16, Q290), avec cette source.
IDS = ['dptQui', 'dptQuand', 'dptTrace']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-74s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


SUIT = r"""(ids)=>new Promise(res=>{ const t0=performance.now(), vu=[]; let premiere=null;
  const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);
  function f(){ const dp=document.getElementById('detailPoster'); const r={t:(performance.now()-t0)|0, c:{}};
    let paru=dp && dp.classList.contains('show') && +getComputedStyle(dp).opacity>0.05;
    ids.forEach(i=>{ const e=document.getElementById(i); if(!e) return; const b=e.getBoundingClientRect(); const cs=getComputedStyle(e);
      if(b.width>2&&b.height>2&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05&&(e.textContent||'').trim()) r.c[i]=cs.webkitTextFillColor||cs.color; });
    if(paru && Object.keys(r.c).length){ vu.push(r); if(!premiere) premiere=r; }
    if(performance.now()-t0<1500) requestAnimationFrame(f); else res({premiere:premiere, vu:vu}); }
  requestAnimationFrame(f); })"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    # ⚠ la fiche GLISSE à l'ouverture : une capture prise quelques ms après la lecture des rectangles tombe sur le trait orange de la vague
    #   qui défile (vu : 6 ouvertures sur 20, rectangles du texte entre y 606 et 655). La couleur ne dépend pas du glissement : pendant ce
    #   juge, la fiche ne glisse pas, et la capture et les rectangles coïncident. Le contrôle 1 (chaque image), lui, garde le vrai chemin.
    ctx.add_init_script("document.addEventListener('DOMContentLoaded',function(){ var s=document.createElement('style'); s.textContent='#detailPoster,#detailPoster *{transition:none!important}'; document.head.appendChild(s); });")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(800)
    oranges = 0; premieres_ko = 0; pix_ko = 0; details = []
    for i in range(N):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        # la capture : on attend, côté Python, la première image où la fiche paraît (au plus vite), puis on capture
        pg.evaluate("()=>{ window.__suit=null; }")
        pg.evaluate("(ids)=>{ window.__suit=(" + SUIT + ")(ids); }", IDS)
        rects = None
        for _ in range(200):
            rects = pg.evaluate("(ids)=>{ const dp=document.getElementById('detailPoster'); if(!(dp&&dp.classList.contains('show')&&+getComputedStyle(dp).opacity>0.05)) return null; const dv=document.getElementById('device').getBoundingClientRect(); const o={}; ids.forEach(i=>{ const e=document.getElementById(i); if(!e||!(e.textContent||'').trim()) return; const rg=document.createRange(); rg.selectNodeContents(e); const b=rg.getBoundingClientRect(); if(b.width>2&&b.height>2) o[i]=[b.left,b.top,b.right,b.bottom]; });   /* le rectangle du TEXTE, pas de la boîte (342 de large, elle attrapait le trait orange de la vague) */ return Object.keys(o).length?o:null; }", IDS)
            if rects: break
            pg.wait_for_timeout(5)
        im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB') if rects else None
        r = pg.evaluate("()=>window.__suit")
        # 1 · chaque image
        o_img = [(v['t'], k) for v in (r or {}).get('vu', []) for k, c in v['c'].items() if c == ORANGE]
        if o_img: oranges += 1; details.append('ouverture %d : orange de %d à %d ms (%s)' % (i + 1, o_img[0][0], o_img[-1][0], ', '.join(sorted(set(k for _, k in o_img)))))
        pr = (r or {}).get('premiere') or {}
        if not pr or any(c != CREME for c in pr.get('c', {}).values()): premieres_ko += 1
        # 2 · la capture
        if im:
            px = im.load(); n_or = 0
            for k, (x0, y0, x1, y1) in rects.items():
                W, H = im.size
                for y in range(max(0, int(y0 * 2)), min(H, int(y1 * 2)), 2):
                    for x in range(max(0, int(x0 * 2)), min(W, int(x1 * 2)), 2):
                        c = px[x, y]
                        if abs(c[0] - 221) + abs(c[1] - 77) + abs(c[2] - 35) <= 40: n_or += 1
            if n_or > 6:
                pix_ko += 1; details.append('ouverture %d : %d pixels orange sur la capture %s' % (i + 1, n_or, str({k: [round(v) for v in r_] for k, r_ in rects.items()})))
                if '--garder' in sys.argv: im.save('scratchpad/v122/flash-%d.png' % (i + 1))
    t('1 · [sombre] aucune image (0 → 1,5 s) ne montre l\'orange sur les trois éléments (%d ouvertures)' % N, oranges == 0, '%d ouverture(s) avec orange' % oranges)
    t('1 · [sombre] la première image où ils paraissent les montre déjà crème (v131, corps cobalt)', premieres_ko == 0, '%d sur %d' % (premieres_ko, N))
    t('2 · [sombre] la capture à la première image : aucun pixel orange sur eux', pix_ko == 0, '%d sur %d' % (pix_ko, N))
    for d in details[:6]: print('     ', d)
    # 3 · Q375 : la première image porte l'état de CETTE fiche, pas celui de la précédente
    # ⚠ L'INSTRUMENT : un relevé pris DANS un `requestAnimationFrame` passe avant les autres rappels de la même image (dont celui qui
    #   pose la fiche) — il lit un état qui ne sera jamais peint. On lit donc APRÈS l'image : une tâche postée depuis le rappel
    #   (MessageChannel), qui s'exécute une fois l'image rendue. Deux enchaînements : la fiche d'avant FERMÉE puis la suivante
    #   (`ferme`), et la suivante ouverte PAR-DESSUS la fiche d'avant, sans la fermer (`direct` — un disque, une carte du fil).
    PREM = r"""([avant, apres, ids, direct])=>new Promise(async res=>{ const F=t=>promises.filter(q=>q.title===t)[0].id;
      try{closeAll()}catch(e){} openDetail(F(avant)); await new Promise(r=>setTimeout(r,2200)); if(!direct){ try{closeAll()}catch(e){} await new Promise(r=>setTimeout(r,700)); }
      const lit=()=>{ const o={}; ids.forEach(i=>{ const e=document.getElementById(i); if(!e) return; const cs=getComputedStyle(e), b=e.getBoundingClientRect();
        if(b.width>2&&b.height>2&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05&&(e.textContent||'').trim()) o[i]=(e.textContent||'').trim()+' | '+(cs.webkitTextFillColor||cs.color); }); return o; };
      let premiere=null; const t0=performance.now(); const mc=new MessageChannel();
      mc.port1.onmessage=()=>{ const dp=document.getElementById('detailPoster'); const paru=dp&&dp.classList.contains('show')&&+getComputedStyle(dp).opacity>0.05;
        if(paru&&!premiere){ const o=lit(); if(Object.keys(o).length) premiere={t:(performance.now()-t0)|0, o:o}; }
        if(performance.now()-t0<1500) requestAnimationFrame(f); else res({premiere:premiere, fin:lit()}); };
      function f(){ mc.port2.postMessage(1); }
      openDetail(F(apres)); requestAnimationFrame(f); })"""
    for avant, apres, th, direct in [(a, b_, c, d) for d in (False, True) for (a, b_, c) in (('le grand plongeoir', 'courir dimanche', 'light'), ('planter un arbre', 'faire les crêpes', 'light'), ('faire les crêpes', 'planter un arbre', 'dark'))]:
        pg.evaluate("(t)=>{ try{closeAll()}catch(e){} setTheme(t); }", th); pg.wait_for_timeout(600)
        faux = 0; ex = ''
        for _ in range(5):
            r = pg.evaluate(PREM, [avant, apres, IDS, direct])
            pr = (r or {}).get('premiere') or {}; fin = (r or {}).get('fin') or {}
            dif = [k for k in fin if (pr.get('o') or {}).get(k) != fin[k]]
            if not pr or not fin or dif:
                faux += 1
                if not ex and dif: ex = '%s : « %s » à la 1re image (%d ms), « %s » posé' % (dif[0], (pr.get('o') or {}).get(dif[0]), pr.get('t', -1), fin[dif[0]])
        t('3 · [%s · %s] « %s » après « %s » : la première image porte déjà le mot et la couleur posés (5 ouvertures)' % ('clair' if th == 'light' else 'sombre', 'par-dessus' if direct else 'fermée', apres, avant), faux == 0, '%d sur 5 %s' % (faux, ex))
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
