#!/usr/bin/env python3
"""
redteam_kaki.py — JAMAIS DE KAKI (Tom, v114, 30 sept. 2026 — règle absolue, CLAUDE.md §3).

EST KAKI toute couleur de teinte OKLCH 78°–140°, de chroma 0,015–0,10 ET de luminance 0,20–0,80 (v115, Tom : « le crème et
les jaunes vifs ne sont pas du kaki » — la règle de v114, sans bornes de chroma ni de luminance, les prenait). Interdit sur toute
dalle et toute matière vide produite par l'app : palette par défaut, palettes proposées, teintes dérivées. Seule exception :
la couleur mère que l'utilisateur choisit lui-même dans la jauge (et même alors, aucune teinte dérivée n'y entre d'elle-même).
Les SEUILS SONT EN DUR ci-dessous — le juge porte la décision (§7).

TROIS FAMILLES, et le verdict nomme chaque coupable :
  A · la SOURCE (sans navigateur) : les 24 palettes du Studio, les rampes des cellules vides (GPIX·GBRA·GLI·GMOS·GENC·GLIGHT)
      et le fond de la Toile (`_fondVifDesc`), lus dans promi-moteur.js ;
  B · le RENDU : les 20 mondes, Toile entière sans titres, clair ET sombre, par `banc_rendu.passe` (graine fixe, horloge pilotée) ;
      une image échoue si plus de SEUIL_PART de ses pixels opaques sont kaki (l'anticrénelage seul n'y arrive pas) ;
  C · les PLANCHES : chaque PNG passé en `--planche=chemin` (plusieurs permis), zone de la Toile (y 110 → 700 à l'échelle 390).
Usage : python3 redteam_kaki.py [--source] [--rendu] [--planche=…]      (sans option : A et B)
Rougi, preuve : python3 redteam_kaki.py --planche=planche-sombre/serie2/v1-touffe.png  (la série 2 du 30 sept.)
"""
import sys, os, re, json, io, base64, glob
from oklch import oklch
H_MIN, H_MAX, C_MIN, C_MAX, L_MIN, L_MAX = 78.0, 140.0, 0.015, 0.10, 0.20, 0.80   # décision Tom, v115
SEUIL_PART = 0.005                                  # 0,5 % des pixels opaques d'une image
ICI = os.path.dirname(os.path.abspath(__file__))
_c = {}
def kaki(r, g, b):
    k = (r, g, b)
    if k not in _c: L, C, h = oklch(r, g, b); _c[k] = (H_MIN <= h <= H_MAX and C_MIN <= C <= C_MAX and L_MIN <= L <= L_MAX)
    return _c[k]
def nom(c): L, C, h = oklch(*c); return '#%02X%02X%02X (h %.0f°, C %.3f, L %.2f)' % (c[0], c[1], c[2], h, C, L)

def source():
    M = io.open(os.path.join(ICI, 'promi-moteur.js'), encoding='utf-8').read(); bad = []
    for m in re.finditer(r"(\w+):\{name:'([^']+)',cols:(\[\[[\d,\[\] ]+\]\])", M):
        for c in json.loads(m.group(3)):
            if kaki(*c): bad.append('palette %-13s %s' % (m.group(2), nom(c)))
    for nm, arr in re.findall(r"\b(G(?:PIX|BRA|LI|MOS|ENC|LIGHT))\s*=\s*(\[\[[\d,\[\] ]+\]\])", M):
        for c in json.loads(arr):
            if kaki(*c): bad.append('rampe des vides %-6s %s' % (nm, nom(c)))
    f = re.search(r"function _fondVifDesc[^}]*\}", M)
    if f:
        for hx in re.findall(r"'#([0-9A-Fa-f]{6})'", f.group(0)):
            c = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
            if kaki(*c): bad.append('fond de la Toile      %s' % nom(c))
    return bad

# LE TEXTE N'EST PAS DE LA MATIÈRE — une planche porte ses titres, peints à l'ENCRE de l'interface (#201908, et le crème
# #F7F0DE sur sombre). Pour les planches seulement, on écarte les pixels à moins de ΔE OK 0,03 de ces encres. (Le rendu B est
# pris SANS titres, il n'en a pas besoin.) L'Index n'est pas jugé : c'est de l'interface, pas de la Toile.
ENCRES = [oklch(0x20,0x19,0x08), oklch(0xF7,0xF0,0xDE)]
import math
def _ok(c):
    L,C,h=oklch(*c); return (L, C*math.cos(math.radians(h)), C*math.sin(math.radians(h)))
_E=[_ok(c) for c in ((0x20,0x19,0x08),(0xF7,0xF0,0xDE))]
_t={}
def texte(c):
    if c not in _t:
        a=_ok(c); _t[c]=any(math.dist(a,e)<0.03 for e in _E)
    return _t[c]
def image(png_bytes, crop=None, sans_texte=False):
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert('RGBA')
    if crop: sx = im.width / 390; im = im.crop((0, int(crop[0]*sx), im.width, int(crop[1]*sx)))
    px = [p for p in im.getdata() if p[3] > 200]
    if not px: return 0, 0, []
    from collections import Counter
    if sans_texte: px = [p for p in px if not texte((p[0], p[1], p[2]))]
    k = Counter((p[0], p[1], p[2]) for p in px if kaki(p[0], p[1], p[2]))
    return sum(k.values()), len(px), [nom(c) + ' ×%d' % n for c, n in k.most_common(3)]

def rendu():
    import banc_rendu
    res, errs = banc_rendu.passe(banc_rendu.URL)
    bad = []; lignes = []
    for m, r in res.items():
        for vue in ('toile-clair', 'toile-sombre'):
            v = (r['images'] or {}).get(vue) or {}
            if 'png' not in v: bad.append('%s %s : pas de rendu' % (m, vue)); continue
            n, t, top = image(base64.b64decode(v['png'].split(',', 1)[1]))
            part = n / t if t else 0
            lignes.append('  %-12s %-13s kaki %5.1f %%  %s' % (m, vue, 100*part, '✗ ' + '; '.join(top) if part > SEUIL_PART else 'OK'))
            if part > SEUIL_PART: bad.append('%s %s : %.1f %% kaki — %s' % (m, vue, 100*part, top[0] if top else ''))
    print('\n'.join(lignes)); return bad

def planches(chemins):
    bad = []
    for p in chemins:
        for f in sorted(glob.glob(p)):
            if 'index' in os.path.basename(f): continue
            n, t, top = image(open(f, 'rb').read(), crop=(110, 700), sans_texte=True)
            part = n / t if t else 0
            print('  %-50s kaki %5.1f %%  %s' % (os.path.relpath(f, ICI), 100*part, '✗ ' + '; '.join(top) if part > SEUIL_PART else 'OK'))
            if part > SEUIL_PART: bad.append('%s : %.1f %% kaki — %s' % (os.path.relpath(f, ICI), 100*part, top[0] if top else ''))
    return bad

if __name__ == '__main__':
    PL = [a.split('=', 1)[1] for a in sys.argv if a.startswith('--planche=')]
    faire_src = '--source' in sys.argv or not (PL or '--rendu' in sys.argv)
    faire_ren = '--rendu' in sys.argv or not (PL or '--source' in sys.argv)
    B = []
    if faire_src:
        print('A · LA SOURCE'); b = source(); B += b
        for x in b: print('  ✗', x)
        if not b: print('  OK')
    if faire_ren: print('B · LE RENDU (20 mondes × clair, sombre)'); B += rendu()
    if PL: print('C · LES PLANCHES'); B += planches(PL)
    try: json.dump(B, open(os.path.join(ICI,'kaki-coupables.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=0)
    except Exception: pass
    print('\n%s — %d coupable(s)' % ('✅ AUCUN KAKI' if not B else '❌ DU KAKI', len(B)))
    sys.exit(1 if B else 0)
