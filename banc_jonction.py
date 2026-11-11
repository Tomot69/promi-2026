# -*- coding: utf-8 -*-
"""⚑ v190 (Tom, C-259, §5) — LE BANC DE LA ZONE DE JONCTION. La fiche (Cercle, Promi, Chiche) défilée pas à pas, aller et retour ; à chaque pas, l'image de la zone de la
jonction (112 → 212 pt, toute la largeur : le bas de la bande d'en-tête, 112, et ce qui passe dessous), lue après l'image. Horloge et hasard figés. La MATIÈRE des dalles
est exceptée (CLAUDE.md §8 bis : elle respire, deux passes ne la peignent pas au pixel) — les boîtes que l'app déclare (`_zonesMatiere`) sont masquées, sur les deux images.
Utilisé par redteam_jonction (Promi et Chiche contre v188) et redteam_haut_fiche (les trois natures contre la référence de v190 : banc-jonction/ref/)."""
import io, sys; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image, ImageChops
AMORCE = """(()=>{ let s=190; Math.random=()=>{ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; window._vivantOff=true;
  const t0=performance.now(); let t=t0; performance.now=()=>t; Date.now=(n=>()=>n)(Date.parse('2026-11-09T10:00:00Z'));
  window.__horloge=d=>{ t+=d; }; })();"""
MOTS = [['Marion', 'On commence quand ?'], ['Rachel', 'Je m’occupe de la farine.'], ['Nico', 'Samedi matin, ça te va ?']]
PAS = list(range(0, 121, 3)) + list(range(120, -1, -3))
def ouvre(b, F, nature, vw=390, vh=844):
    ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); ctx.add_init_script(AMORCE); pg = B.ouvre(ctx, F, 6000)
    if nature == 'cercle': pg.evaluate("m=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; m.forEach((x,i)=>o.comments.push({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); openEssaim('potager'); }", MOTS)
    else: pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); if(a[1]){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.comments=a[2].map((x,i)=>({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); openDetail(p.id); }",
                      [{'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}[nature], nature == 'chiche', MOTS])
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)   # la pose et les glissements finis, sur l'horloge figée
    pg.wait_for_timeout(600); return ctx, pg
def images(pg, pas=PAS, matiere=True):
    """matiere=False : rien n'est masqué (le Cercle : ses dalles sont posées une fois, à leur taille — C-231 — et la jonction est DANS sa boîte de matière)"""
    d = B.dev(pg); k = d[4]; out = []; EN = None
    if not matiere:   # le Cercle : l'enveloppe haute de sa vraie vague (déclarée par lot-V189-JONCTION) — au-dessus, ses dalles (la matière) ; dessous, rien n'est masqué
        pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=60; }"); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        EN = (pg.evaluate("()=>{ const j=window._v189Jonction&&_v189Jonction(); return j&&j.F&&j.F.EN; }") or None)
    for s in pas:
        pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s)
        pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1] + Y0 * k, 'width': 390 * k, 'height': H * k}))).convert('RGB')
        z = pg.evaluate("()=>window._zonesMatiere ? _zonesMatiere().zones : []") if matiere else []
        q = im.size[0] / 390.0; m = Image.new('L', im.size, 0); from PIL import ImageDraw; dr = ImageDraw.Draw(m)
        if EN:
            for i, e in enumerate(EN):
                yb = e - s - 2.5
                if yb > Y0: dr.rectangle([int(i * 2 * q) - 2, 0, int((i * 2 + 2) * q) + 2, int((yb - Y0) * q)], fill=255)
        for x, y, w, h in z: dr.rectangle([int(x * q) - 1, int((y - Y0) * q) - 1, int((x + w) * q) + 1, int((y + h - Y0) * q) + 1], fill=255)
        out.append((s, im, m))
    return out
Y0, H = 112, 100
def ecart(a, b, seuil=24):
    """a, b : (s, image, masque de matière) ; les pixels sous l'un OU l'autre masque ne comptent pas"""
    if a[1].size != b[1].size: return -1
    from PIL import ImageChops as C
    d = C.difference(a[1], b[1]).convert('L').point(lambda v: 255 if v > seuil else 0)
    d = C.subtract(d, C.lighter(a[2], b[2])); return sum(d.histogram()[1:])
def ecart_bords(a, ref, seuil=24, rayon=2):
    """⚑ v193 (Tom, Q616 tranchée) — « la référence au pixel ne s'impose plus au bord du trait : la même forme, la même position (0,5 pt près), les mêmes couleurs ;
    le lissage des bords peut différer ». Comme `ecart`, sauf les pixels à `rayon` pixels (2 px ≈ 0,67 pt au banc @3x) d'un BORD de la référence : un trait décalé de
    plus d'un demi-point, d'une autre forme ou d'une autre couleur laisse des pixels hors de cette bande, et il est pris."""
    if a[1].size != ref[1].size: return -1
    from PIL import ImageChops as C, ImageFilter as IF
    d = C.difference(a[1], ref[1]).convert('L').point(lambda v: 255 if v > seuil else 0)
    bord = ref[1].convert('L').filter(IF.FIND_EDGES).point(lambda v: 255 if v > 30 else 0).filter(IF.MaxFilter(2 * rayon + 1))
    from PIL import ImageDraw; W, H = bord.size; dr = ImageDraw.Draw(bord)   # la rangée du bord de la zone (112 pt : le haut du trait accroché) — le filtre n'y voit pas le bord ; le bas du trait, lui, reste jugé
    dr.rectangle([0, 0, W, rayon - 1], fill=255); dr.rectangle([0, H - rayon, W, H], fill=255)
    dr.rectangle([0, 0, 0, H], fill=255); dr.rectangle([W - 1, 0, W, H], fill=255)   # la colonne du bord de l'écran : à une échelle non entière, son pixel est à cheval sur le bord (le lissage du bord de l'écran)
    d = C.subtract(C.subtract(d, C.lighter(a[2], ref[2])), bord)
    import os
    if os.environ.get('BJ_DIFF'): d.save(os.environ['BJ_DIFF']); a[1].save(os.environ['BJ_DIFF']+'.a.png'); ref[1].save(os.environ['BJ_DIFF']+'.r.png')
    return sum(d.histogram()[1:])
