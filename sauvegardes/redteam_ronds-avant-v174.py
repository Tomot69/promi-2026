#!/usr/bin/env python3
"""redteam_ronds.py — ⚑ v148 (Tom, 16 oct. 2026, C-143) : « Sur les fiches, et dans la page + s'ils y paraissent, il y a deux ronds orange,
à gauche et à droite, qui indiquent de signer en traçant. C'est du bruit, c'est moche. Supprime-les PARTOUT. Le chevron orange du départ de la
flèche (C-133) reste. »

LA CAUSE (mesurée en v148) : le canevas du geste (`#tenirCv` sur la fiche, `#planterCv` sur la page +) peint encore les deux points de guidage
du geste d'origine (un rond plein à 38 pt du bord gauche, un anneau à 38 pt du bord droit, rayon 19). Sur la fiche une règle le pose à
`opacity:0 !important` — Chromium l'efface, MAIS l'animation `tenirPouls` (« le point de gauche pulse doucement ») l'emporte sur ce
`!important` dans WebKit : sur l'iPhone, les deux ronds pulsaient entre 50 et 100 %. Chromium ne le montre pas : le juge passe par WebKit.

Le juge, dans WebKit (banc_tom, 390 × 844 ×3), clair et sombre : fiche d'un Promi, fiche d'un Chiche, page + d'un Promi, d'un Chiche, d'un Cercle.
  A · le canevas du geste ne PEINT rien à la place des deux ronds (au repos)
  B · rien de ce canevas ne se voit : opacité calculée relevée 12 fois sur 3 s (l'animation comprise) ≤ 0,02, OU contenu vide aux ronds
  C · aucun rond à l'écran : sur la CAPTURE, autour des deux places, rien ne change quand on cache le canevas du geste (≤ 4 pixels) — et aucun
      pixel orange de plus (le chevron du départ de la flèche, peint ailleurs, reste)
  D · le chevron orange du départ de la flèche est toujours là (C-133)
  E · (C-139, chef de chantier : aucune invitation animée tant que Tom n'a pas choisi) la bande du trait ne bouge pas au repos, 7 s
Preuve : `--fichier=zz-av147.html` rougit (A, C).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append((nom, ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, d))

CONTENU = """(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(); if(r.width<10) return {absent:true};
  const g=c.getContext('2d'); const W=c.width, H=c.height, k=W/Math.max(1,r.width)*(r.width/c.clientWidth||1); const d=g.getImageData(0,0,W,H).data;
  const sx=W/c.clientWidth, sy=H/c.clientHeight; let n=0;
  /* les deux places : (38 ; H/2) et (W-38 ; H/2), rayon 19 — et celles de la page + (42/308, 266/308 de la largeur ; 52/118 de la hauteur) */
  const P=[[38,c.clientHeight/2],[c.clientWidth-38,c.clientHeight/2],[c.clientWidth*42/308,c.clientHeight*52/118],[c.clientWidth*266/308,c.clientHeight*52/118]];
  P.forEach(([x,y])=>{ for(let j=-20;j<=20;j+=2) for(let i=-20;i<=20;i+=2){ const X=Math.round((x+i)*sx), Y=Math.round((y+j)*sy); if(X<0||Y<0||X>=W||Y>=H) continue; if(d[(Y*W+X)*4+3]>20) n++; } });
  return {n:n}; }"""
OPA = """async (id)=>{ const c=document.getElementById(id); if(!c) return 0; let m=0; for(let i=0;i<12;i++){ let o=1; for(let q=c;q&&q.nodeType===1;q=q.parentElement){ const s=getComputedStyle(q); if(s.display==='none'||s.visibility==='hidden'){ o=0; break; } o*=+s.opacity; } m=Math.max(m,o); await new Promise(r=>setTimeout(r,250)); } return m; }"""
PLACES = """(id)=>{ const c=document.getElementById(id), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!c) return null; const r=c.getBoundingClientRect(); if(r.width<10) return null;
  const x0=(r.left-D.left)/k, y0=(r.top-D.top)/k, w=r.width/k, h=r.height/k; return [[x0+38,y0+h/2],[x0+w-38,y0+h/2],[x0+w*42/308,y0+h*52/118],[x0+w*266/308,y0+h*52/118]]; }"""
def capture(pg):
    d = B.dev(pg); return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]}))).convert('RGB')
def orange(px):
    r, g, b = px
    return (r > 190 and 50 < g < 120 and b < 70)
def ecart(im, im0, places):
    s = im.size[0] / 390.0; n = 0
    for x, y in places[:2]:
        for j in range(-20, 21, 2):
            for i in range(-20, 21, 2):
                X, Y = int((x + i) * s), int((y + j) * s)
                if 0 <= X < im.size[0] and 0 <= Y < im.size[1] and sum(abs(a - b) for a, b in zip(im.getpixel((X, Y)), im0.getpixel((X, Y)))) > 60: n += 1
    return n
def oranges(im, places):
    s = im.size[0] / 390.0; n = 0
    for x, y in places:
        for j in range(-20, 21, 2):
            for i in range(-20, 21, 2):
                X, Y = int((x + i) * s), int((y + j) * s)
                if 0 <= X < im.size[0] and 0 <= Y < im.size[1] and orange(im.getpixel((X, Y))): n += 1
    return n
def un(b, th, ecran, nature):
    T = '[%s, %s %s]' % ('clair' if th == 'light' else 'sombre', ecran, ['Promi', 'Chiche', 'Cercle'][nature])
    ctx = B.contexte(b, sombre=(th == 'dark')); pg = B.ouvre(ctx, F)
    if ecran == 'fiche':
        if nature == 1: B.plante_doigt(pg, 'courir dimanche', qui='Marion', nature=1)
        else: B.plante(pg, 'rendre le livre', qui='Marion')
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2800); cid = 'tenirCv'
    else:
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700)
        B.tap_sel(pg, '.acc-pil[data-k=%s]' % ['promi', 'chiche', 'nuee'][nature])
        for _ in range(40):
            pg.wait_for_timeout(120)
            if pg.evaluate("()=>{ var s=document.getElementById('createSheet'); return !!(s && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe') && s.classList.contains('show')); }"): break
        pg.wait_for_timeout(1500)
        cid = pg.evaluate("()=>['planterCv','planterCvN','planterCvD'].find(i=>{ const c=document.getElementById(i); return c && c.getBoundingClientRect().width>10; })||'planterCv'")
    c = pg.evaluate(CONTENU, cid); o = pg.evaluate(OPA, cid); pl = pg.evaluate(PLACES, cid)
    im = capture(pg)
    pg.evaluate("(id)=>{ const c=document.getElementById(id); if(c) c.style.setProperty('visibility','hidden','important'); }", cid); pg.wait_for_timeout(120)
    im0 = capture(pg)
    pg.evaluate("(id)=>{ const c=document.getElementById(id); if(c) c.style.removeProperty('visibility'); }", cid)
    n1 = oranges(im, pl or []); n0 = oranges(im0, pl or [])
    chev = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(); return 1; }")
    juge('%s A · le canevas du geste (%s) ne peint rien à la place des deux ronds' % (T, cid), c is not None and (c.get('absent') or c['n'] == 0), c)
    juge('%s B · rien de ce canevas ne se voit, ou il est vide aux ronds (opacité au plus haut sur 3 s : %.2f)' % (T, o), o <= 0.02 or (c and (c.get('absent') or c['n'] == 0)), '')
    ne = ecart(im, im0, pl or [])
    juge('%s C · aucun rond à l\'écran aux deux places : la capture est la même avec et sans le canevas du geste (pixels orange : %d / %d)' % (T, n1, n0), ne <= 4 and n1 - n0 <= 2, '%d pixels changent' % ne)
    # D · le chevron orange du départ de la flèche (C-133) : un orange #FB4C0D (ΔE) peint dans le canevas du trait
    ch = pg.evaluate("""()=>{ const ids=['dpTrameCv','csTrameCv']; let n=0; ids.forEach(i=>{ const c=document.getElementById(i); if(!c||c.getBoundingClientRect().width<10) return; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
        for(let q=0;q<d.length;q+=4*5){ if(d[q+3]>200 && d[q]>230 && d[q+1]>50 && d[q+1]<110 && d[q+2]<40) n++; } }); return n; }""")
    juge('%s D · le chevron orange du départ de la flèche est toujours là (C-133)' % T, ch > 20, '%d pixels' % ch)
    # E (v148, C-139, décision du chef de chantier) : « tant que Tom n'a pas choisi, AUCUNE invitation animée dans l'app » — la bande du trait
    #   ne bouge pas au repos : 14 captures, une toutes les 500 ms, ≤ 0,3 % de pixels qui changent d'une capture à la suivante
    if pl:
        y0 = max(0, pl[0][1] - 75); y1 = min(844, pl[0][1] + 45); pire = 0; prec = None
        for _ in range(14):
            pg.wait_for_timeout(500); im2 = capture(pg); s_ = im2.size[0] / 390.0
            bd = im2.crop((0, int(y0 * s_), im2.size[0], int(y1 * s_))).convert('L').resize((390, int(y1 - y0)))
            if prec is not None:
                a = bd.load(); c_ = prec.load(); n = sum(1 for j in range(bd.size[1]) for i in range(bd.size[0]) if abs(a[i, j] - c_[i, j]) > 12)
                pire = max(pire, n / float(bd.size[0] * bd.size[1]))
            prec = bd
        juge('%s E · aucune invitation animée : la bande du trait ne bouge pas au repos (7 s)' % T, pire <= 0.003, 'au pire %.2f %% des pixels changent' % (100 * pire))
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        for ecran, nat in ((('fiche', 0),) if '--vite' in sys.argv else (('fiche', 0), ('fiche', 1), ('page +', 0), ('page +', 1), ('page +', 2))):
            if ecran == 'fiche' or th == 'light' or nat == 0: un(b, th, ecran, nat)
    b.close()
ok = sum(1 for _, c in res if c); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
