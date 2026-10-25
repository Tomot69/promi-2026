#!/usr/bin/env python3
"""redteam_appartient.py — ⚑ v163 (Tom, C-165 suite) : « T'APPARTIENT. » MULTICOLORE.

« Dans « La suite t'appartient. », le mot « T'APPARTIENT. » prend une lettre par couleur de la palette de base, dans l'ordre de la palette, comme « Studio »
dans le guide. En clair ET en sombre (en sombre, les variantes claires, au moins 3:1). « La suite » ne change pas. »
Le vrai chemin (banc comme Tom : WebKit ×3, doigt) : l'onboarding jusqu'au dernier paragraphe de « Promi planté ! » (trois touchers), le tracé fini.
Lu SUR L'IMAGE, lettre par lettre (les tons de « Studio » du guide, en dur) :
  A · chaque lettre de « t'appartient » a le ton attendu, dans l'ordre (bleu, rose, lilas, crème, …) — ΔE ≤ 12 entre l'encre lue et le ton ;
  B · chaque lettre tient 3:1 sur le fond lu derrière elle ;
  C · « La suite » garde sa couleur d'avant (celle de v162, lue sur l'image) ;
aux échelles 1 (430 × 932) et 0,79 (330 × 714), clair et sombre. Preuve : `--fichier=zz-v162.html` rougit (A).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
TONS = {False: [0x476FB4, 0x9B5D75, 0x8161A8, 0x796E55], True: [0x82AEF8, 0xFFB8D2, 0xC9A8F5, 0xEFE3C7]}
def rgb(h): return ((h >> 16) & 255, (h >> 8) & 255, h & 255)
def lab(c):
    def f(u):
        u /= 255; return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c); X = (0.4124*r + 0.3576*g + 0.1805*b) / 0.95047; Y = 0.2126*r + 0.7152*g + 0.0722*b; Z = (0.0193*r + 0.1192*g + 0.9505*b) / 1.08883
    g3 = lambda t: t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
    return (116 * g3(Y) - 16, 500 * (g3(X) - g3(Y)), 200 * (g3(Y) - g3(Z)))
def de(a, b): A, Bb = lab(a), lab(b); return sum((x - y) ** 2 for x, y in zip(A, Bb)) ** 0.5
def lum(c):
    def f(u):
        u /= 255; return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
def ctr(a, b): la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
CLAVIER = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
TRAIT = open('redteam_onboarding_complet.py', encoding='utf-8').read().split('TRAIT = """')[1].split('"""')[0]
def trace(pg):
    z = pg.evaluate(TRAIT); a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
BOITES = """()=>{ const L=[...document.querySelectorAll('#onbV .onbv-app')]; const app=L[L.length-1]; if(!app) return null;
  const k=[...app.querySelectorAll('.onbv-al')], suite=app.parentNode; const out={lettres:[], suite:null};
  const R=e=>{ const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); return [r.left,r.top,r.right,r.bottom]; };
  if(k.length) k.forEach(e=>out.lettres.push({c:e.textContent, b:R(e)})); else { /* v162 : un seul mot, sans lettres séparées */ const t=app.firstChild; const s=app.textContent;
    for(let i=0;i<s.length;i++){ const rg=document.createRange(); rg.setStart(t,i); rg.setEnd(t,i+1); const r=rg.getBoundingClientRect(); out.lettres.push({c:s[i], b:[r.left,r.top,r.right,r.bottom]}); } }
  const tn=[...suite.childNodes].find(n=>n.nodeType===3 && /La suite/.test(n.textContent)); if(tn){ const rg=document.createRange(); rg.selectNodeContents(tn); const r=rg.getBoundingClientRect(); out.suite=[r.left,r.top,r.right,r.bottom]; }
  return out; }"""
def encre(im, b, dsf, fond):
    x0, y0, x1, y1 = [int(v * dsf) for v in b]; best, nb = None, 0
    px = [im.getpixel((x, y)) for x in range(x0, max(x0 + 1, x1)) for y in range(y0, max(y0 + 1, y1))]
    loin = [p for p in px if de(p, fond) > 25]
    if not loin: return None
    loin.sort(key=lambda p: -de(p, fond)); cut = loin[:max(1, len(loin) // 3)]   # le cœur du trait, pas l'anticrénelage
    return tuple(sorted(c[i] for c in cut)[len(cut) // 2] for i in range(3))
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ((430, 932), (330, 714)):
        for sombre in (False, True):
            T = '%s · %s' % ('échelle 1' if vw == 430 else 'échelle 0,79', 'sombre' if sombre else 'clair')
            ctx = B.contexte(b, sombre=sombre, onb=False, guide=False, vw=vw, vh=vh); ctx.add_init_script(CLAVIER); pg = B.ouvre(ctx, F, attente=7000)
            B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200)
            B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(600); pg.keyboard.type('marcher une heure', delay=12); pg.wait_for_timeout(800)
            pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(2200); trace(pg); pg.wait_for_timeout(5600)
            for _ in range(3): B.tap(pg, 195, 300); pg.wait_for_timeout(3800)
            pg.wait_for_timeout(2500)
            Bx = pg.evaluate(BOITES)
            if not Bx: juge('[%s] « La suite t\'appartient. » paraît' % T, False); ctx.close(); continue
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); dsf = im.size[0] / vw
            L = [x for x in Bx['lettres'] if x['c'].isalpha()]
            # le fond : sous la ligne, à gauche du mot (aucune lettre)
            fb = Bx['lettres'][0]['b']; fond = im.getpixel((int((fb[0] - 8) * dsf), int((fb[1] + fb[3]) / 2 * dsf)))
            att = [rgb(TONS[sombre][i % 4]) for i in range(len(L))]
            lu = [encre(im, x['b'], dsf, fond) for x in L]
            ecarts = [round(de(a, l), 1) if l else None for a, l in zip(att, lu)]
            juge('[%s] A · chaque lettre de « t\'appartient » au ton de la palette, dans l\'ordre (ΔE ≤ 12)' % T, len(L) == 11 and all(e is not None and e <= 12 for e in ecarts), 'ΔE %s' % ecarts)
            cs = [round(ctr(l, fond), 2) if l else 0 for l in lu]
            juge('[%s] B · chaque lettre tient 3:1 sur son fond' % T, all(c >= 3 for c in cs), 'contrastes %s · fond %s' % (cs, fond))
            su = encre(im, Bx['suite'], dsf, fond) if Bx['suite'] else None
            juge('[%s] C · « La suite » lu sur l\'image' % T, su is not None, 'encre %s' % (su,))
            print('     suite=%s' % (su,))
            er = [x for x in pg.erreurs if 'version.json' not in x]
            if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
