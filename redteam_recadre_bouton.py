#!/usr/bin/env python3
"""redteam_recadre_bouton.py — ⚑ v163 (Tom, C-188) : LE BOUTON « RECADRER » DE L'ACCUEIL.

« Aucun encart ni fond : un symbole seul, à l'encre du mode, ≈ 22 pt, une zone de toucher invisible de 44 pt ; en bas à droite, juste au-dessus de la barre.
Il paraît quand on a déplacé ou zoomé la vue, et disparaît de lui-même après 4 s sans toucher, en flaques rapides (≈ 300 ms), jamais d'un coup ; il revient au
déplacement suivant. Le double toucher pour recadrer reste. »
Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles, clair et sombre :
  A · au repos (vue d'origine) : rien ;
  B · un glissé au doigt sur la Toile : il NAÎT par `_passageFlaques` (mode « couvre », 300 ms), puis le symbole est là ;
  C · le symbole : son encre (lue sur l'image, différence avec la même vue sans lui) fait 20 à 24 pt, à l'encre du mode (#201908 / #F7F0DE), son bas à
      12 pt (± 1,5) de la barre, son bord droit à 24 pt (± 1,5) du bord ; RIEN d'autre ne change à l'image (aucun fond, aucun cerne) ;
  D · la zone de 44 pt : ses quatre coins (à 3 pt du bord) le donnent au doigt ;
  E · 4 s sans toucher : il PART en flaques (« ouvre », 300 ms) — à mi-passage il en reste une partie (jamais d'un coup) —, puis plus rien ;
  F · un nouveau glissé le fait revenir ;
  G · le toucher sur lui recadre (la vue n'est plus celle de la main), il part en flaques ;
  H · le double toucher sur la Toile recadre toujours.
Preuve : `--fichier=zz-v162.html` rougit (B, C : un rond plein, aucun passage en flaques ; E : il ne part jamais seul).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
PIEGE = """(()=>{ window.__pf=[]; let f; Object.defineProperty(window,'_passageFlaques',{configurable:true, get:()=>f ? function(h,o){ if(h && h.id==='accRecadre') window.__pf.push([o&&o.mode, o&&o.duree, Math.round(performance.now())]); return f.apply(this, arguments); } : f, set:v=>{ f=v; }}); })();"""
ETAT = "()=>({vu:document.getElementById('accRecadre').classList.contains('vu'), cache:document.getElementById('accRecadre').classList.contains('rc-cache'), main:!!window._vueMain, pf:window.__pf.slice()})"
def cap(pg):
    D = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390]; }")
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = im.size[0] / pg.viewport_size['width']
    return im, D, k
def fige(pg, oui):
    pg.evaluate("o=>{ if(o){ window.__raf0=window.__raf0||window.requestAnimationFrame; window._vivantOff=true; } }", oui)
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'; ENC = (247, 240, 222) if sombre else (32, 25, 8)
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>{ window._vivantOff=true; }")
        e = pg.evaluate(ETAT); juge('[%s] A · au repos, aucun bouton' % T, not e['vu'], e)
        B.glisse(pg, B.droite([200, 420], [150, 390], 12), pas=20); tg = pg.evaluate("()=>performance.now()"); pg.wait_for_timeout(1400)
        e = pg.evaluate(ETAT); nait = [x for x in e['pf'] if x[0] == 'couvre']
        juge('[%s] B · un glissé : il naît en flaques (300 ms), puis il est là' % T, e['vu'] and not e['cache'] and nait and abs(nait[0][1] - 300) <= 30, e)
        # C : la même vue, avec et sans le bouton
        im1, D, k = cap(pg)
        pg.evaluate("()=>{ document.getElementById('accRecadre').style.setProperty('visibility','hidden','important'); }"); pg.wait_for_timeout(120)
        im0, _, _ = cap(pg)
        pg.evaluate("()=>{ document.getElementById('accRecadre').style.removeProperty('visibility'); }")
        zb = pg.evaluate("()=>{ const q=document.getElementById('accRecadre').getBoundingClientRect(); return [q.left-30, q.top-30, q.right+30, q.bottom+30]; }")
        box = tuple(int(v * k) for v in zb); im1 = im1.crop(box); im0 = im0.crop(box); D = [D[0] - zb[0], D[1] - zb[1], D[2]]
        diff = ImageChops.difference(im1, im0).convert('L').point(lambda v: 255 if v > 24 else 0); bb = diff.getbbox()
        if bb:
            x0, y0, x1, y1 = [((bb[0] / k) - D[0]) / D[2], ((bb[1] / k) - D[1]) / D[2], ((bb[2] / k) - D[0]) / D[2], ((bb[3] / k) - D[1]) / D[2]]
            px = [im1.getpixel((x, y)) for x in range(bb[0], bb[2]) for y in range(bb[1], bb[3]) if diff.getpixel((x, y))]
            moy = tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))
            ok = 20 <= x1 - x0 <= 24.5 and 20 <= y1 - y0 <= 24.5 and abs((710 - y1) - 12) <= 1.5 and abs((390 - x1) - 24) <= 1.5 and sum(abs(a - b_) for a, b_ in zip(moy, ENC)) <= 60
            juge('[%s] C · le symbole seul : 22 pt, encre du mode, 12 pt au-dessus de la barre, 24 pt du bord droit, rien d\'autre à l\'image' % T, ok,
                 'encre %.1f×%.1f à (%.1f–%.1f, %.1f–%.1f) · couleur médiane %s' % (x1 - x0, y1 - y0, x0, x1, y0, y1, moy))
        else: juge('[%s] C · le symbole est peint' % T, False, 'aucune différence')
        z = pg.evaluate("()=>{ const r=document.getElementById('accRecadre'), q=r.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const pts=[[q.left+3*k,q.top+3*k],[q.right-3*k,q.top+3*k],[q.left+3*k,q.bottom-3*k],[q.right-3*k,q.bottom-3*k]]; return [q.width/k, q.height/k, pts.map(p=>{ const e=document.elementFromPoint(p[0],p[1]); return !!(e && e.closest && e.closest('#accRecadre')); })]; }")
        juge('[%s] D · une zone de toucher de 44 pt, ses quatre coins le donnent' % T, abs(z[0] - 44) < 0.6 and abs(z[1] - 44) < 0.6 and all(z[2]), z)
        # E : 4 s sans toucher
        t0 = pg.evaluate("()=>performance.now()"); vu_mi = None; parti = None
        for i in range(60):
            pg.wait_for_timeout(100); e = pg.evaluate(ETAT); part = [x for x in e['pf'] if x[0] == 'ouvre']
            if part and vu_mi is None:
                pg.wait_for_timeout(max(0, part[0][2] + 150 - pg.evaluate("()=>performance.now()")))
                vu_mi = pg.evaluate("()=>{ const c=document.querySelector('#accRecadre canvas.passage-flaques'); if(!c) return 0; const g=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<g.length;i+=4) if(g[i]>40) n++; return n; }")
            if part and not e['vu']: parti = part[0]; break
        juge('[%s] E · 4 s sans toucher : il part en flaques (300 ms), à mi-passage il en reste, puis plus rien' % T,
             parti is not None and abs(parti[1] - 300) <= 30 and 3800 <= parti[2] - tg <= 6500 and (vu_mi or 0) > 30, 'passage %s · %s ms après le glissé · pixels à mi-passage %s' % (parti, parti and round(parti[2] - tg), vu_mi))
        B.glisse(pg, B.droite([180, 400], [220, 430], 12), pas=20); pg.wait_for_timeout(1300)
        e = pg.evaluate(ETAT); juge('[%s] F · un nouveau glissé : il revient' % T, e['vu'] and not e['cache'], e)
        r = pg.evaluate("()=>{ const q=document.getElementById('accRecadre').getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(q.left+q.width/2-D.left)/k, (q.top+q.height/2-D.top)/k]; }")
        B.tap(pg, r[0], r[1]); pg.wait_for_timeout(1500)
        e = pg.evaluate(ETAT); juge('[%s] G · le toucher recadre, il part en flaques' % T, not e['main'] and not e['vu'] and [x for x in e['pf'] if x[0] == 'ouvre'][-1:] and e['pf'][-1][0] == 'ouvre', e)
        B.glisse(pg, B.droite([200, 420], [150, 390], 12), pas=20); pg.wait_for_timeout(900)
        B.tap(pg, 195, 420); pg.wait_for_timeout(120); B.tap(pg, 195, 420); pg.wait_for_timeout(1500)
        e = pg.evaluate(ETAT); juge('[%s] H · le double toucher sur la Toile recadre toujours' % T, not e['main'], e)
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
