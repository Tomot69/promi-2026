# -*- coding: utf-8 -*-
"""redteam_bord.py — LA PELOTE N'A PAS DE LISERÉ : LE BORD A LES COULEURS DE L'INTÉRIEUR (v137, C-002).

Décision (Tom, 8 oct. 2026), mot pour mot : « Le liseré du bord part aussi. Sur les derniers 8 % du rayon, la fourrure prend une autre
couleur que l'intérieur (ΔE 15 à 31), et ça fait la deuxième couche que Tom voit. La fourrure du bord prend les couleurs de l'intérieur :
ΔE ≤ 5 entre la bande du bord et l'intérieur voisin, en clair et en sombre, sur quatre palettes. La silhouette ne change pas. »

Ce qui est mesuré, sur la capture @3x, la Pelote figée, trois ouvertures par palette et par thème (le sol et le corps sont tirés au sort) :
  la couleur moyenne de la BANDE DU BORD (0,92 → 0,955 du rayon de la silhouette, 121 pt, soit 111,3 → 115,6 pt : jusqu'au rayon de la boule,
  116 pt ; au-delà le corps s'efface en 1,4 pt et seul le poil dépasse, jusqu'à 124 : c'est la silhouette, qui ne change pas) et celle de L'INTÉRIEUR VOISIN (0,84 → 0,90),
  secteur par secteur (24 secteurs de 15°) ; un secteur qui porte une île (écart-type de l'intérieur > 14 niveaux) n'est pas jugé.
  Verdict : la MÉDIANE des ΔE (CIELAB) des secteurs ≤ 5, à chaque ouverture. Valeur EN DUR (§7).
Preuve : rouge sur l'état d'avant (python3 redteam_bord.py zz-av137.html). La silhouette : redteam_contour, redteam_plein.
"""
import io, sys, math
from playwright.sync_api import sync_playwright
from PIL import Image
F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'
SEUIL = 5.0; PALETTES = ['signal', 'candide', 'irascible', 'taciturne']; N = 3; R = 121.0
ok = [0]; ko = []
def t(nom, c, d=''):
    if c: ok[0] += 1
    else: ko.append(nom)
    print('%s  %-58s %s' % ('OK' if c else 'KO', nom, d))
def lab(c):
    def lin(v): v /= 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [lin(v) for v in c]; X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047; Y = 0.2126 * r + 0.7152 * g + 0.0722 * b; Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))
def zone(px, cx, cy, e, a0, a1, r0, r1):
    s = [0, 0, 0]; s2 = 0; n = 0
    for ia in range(8):
        ang = math.radians(a0 + (a1 - a0) * (ia + 0.5) / 8)
        for ir in range(8):
            rr = (r0 + (r1 - r0) * (ir + 0.5) / 8) * R * e
            c = px[int(cx + rr * math.cos(ang)), int(cy + rr * math.sin(ang))]
            for i in range(3): s[i] += c[i]
            s2 += (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) ** 2; n += 1
    m = [v / n for v in s]; l = 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]
    return m, math.sqrt(max(0, s2 / n - l * l))
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        for pal in PALETTES:
            meds = []
            for k in range(N):
                ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3, reduced_motion='reduce')
                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
                pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500)
                pg.evaluate("([t,p])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){ try{ setLight(t==='light'); }catch(e){ d.classList.toggle('light',t==='light'); } } try{Toile.setPalette(p)}catch(e){} document.getElementById('souffleBtn').click(); }", [th, pal])
                pg.wait_for_timeout(3800)
                pg.evaluate("()=>{ try{ _aura.fige(true); }catch(e){} }"); pg.wait_for_timeout(350)
                g = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, document.getElementById('device').classList.contains('light')]}")
                im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px = im.load(); e = im.width / 430.0
                des = []
                for sct in range(24):
                    mi, si = zone(px, g[0] * e, g[1] * e, e, sct * 15, sct * 15 + 15, 0.84, 0.90)
                    mb, sb = zone(px, g[0] * e, g[1] * e, e, sct * 15, sct * 15 + 15, 0.92, 0.955)
                    if si > 14: continue
                    des.append(math.dist(lab(mi), lab(mb)))
                des.sort(); meds.append(des[len(des) // 2] if len(des) >= 8 else 99.0)
                ctx.close()
            t('[%s · %s] bord ↔ intérieur voisin : ΔE médian ≤ %.0f' % ('clair' if th == 'light' else 'sombre', pal, SEUIL), max(meds) <= SEUIL, ' · '.join('%.1f' % m for m in meds))
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: sys.exit(1)
