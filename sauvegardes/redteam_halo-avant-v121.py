#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_halo.py — LE MINI HALO ET L'OMBRE DE LA PELOTE (v119, Tom, 2 oct. 2026). WebKit, @3x, lu sur l'IMAGE RENDUE.

« Ce n'est pas un flou posé autour, c'est la lumière du velours qui déborde à peine de la silhouette. »
Les valeurs décidées, EN DUR (§7) — D = 232,064 pt (le diamètre de la boule), silhouette = boule + poil = 121 pt de rayon :
  A · le profil, du côté éclairé (la lumière vient d'en haut à gauche), ΔE00 face au fond de la page :
        au ras de la silhouette 5 à 9 · à 0,04 D 2 à 4 · à 0,08 D moins de 1 · RIEN au-delà (le fond exact)
  B · la direction : à l'opposé de la lumière, 20 % de l'intensité (on admet 8 à 35 % du ΔE du côté éclairé) ;
      sur le quart inférieur, presque nul (ΔE00 < 1)
  C · la trame : le long d'un profil radial, aucune bande de plus de 2 pt à valeur constante tant que le halo se voit
  D · il respire avec la lumière du velours : ± 20 % — le sommet (4,6 s) vaut 1,5 fois le creux (10,6 s), à ± 0,3 près
  E · l'ombre : ΔE00 ≥ 2 entre l'ombre et son pourtour immédiat, dans les DEUX thèmes ; en sombre, aucune ombre crème
  F · la mise en page : le halo ne touche pas le plateau ; « Partager ma Pelote » est à 525,47 (v118)
Preuve (§7) : `--sonde` fabrique le halo SANS trame (`window._haloSansTrame`) → C doit ROUGIR.
A, B, C, E, F se lisent avec « Réduire les animations » (le halo y est immobile, à sa valeur moyenne).
"""
import io, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad'))
from playwright.sync_api import sync_playwright
from PIL import Image

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
SONDE = '--sonde' in sys.argv
S = 3; D = 232.064; RS = 121.0; CXY = (195.0, 122.532 + 148.0)
LUM = math.atan2(-0.72, -0.58)                      # d'où vient la lumière (repère de l'écran, y vers le bas)
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-76s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-76s KO  %s' % (nom, detail))


def lab(c):
    def lin(v):
        v /= 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = lin(c[0]), lin(c[1]), lin(c[2])
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047; y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b; z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def dE00(c1, c2):
    L1, a1, b1 = lab(c1); L2, a2, b2 = lab(c2); R = math.pi / 180
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cb = (C1 + C2) / 2; G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    ap1, ap2 = (1 + G) * a1, (1 + G) * a2; Cp1, Cp2 = math.hypot(ap1, b1), math.hypot(ap2, b2)
    h1 = math.degrees(math.atan2(b1, ap1)) % 360; h2 = math.degrees(math.atan2(b2, ap2)) % 360
    dL, dC, dh = L2 - L1, Cp2 - Cp1, h2 - h1
    if Cp1 * Cp2 == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dH = 2 * math.sqrt(Cp1 * Cp2) * math.sin(dh / 2 * R); Lb, Cpb, hb = (L1 + L2) / 2, (Cp1 + Cp2) / 2, h1 + h2
    if Cp1 * Cp2 != 0:
        if abs(h1 - h2) > 180: hb += 360 if hb < 360 else -360
        hb /= 2
    T = 1 - 0.17 * math.cos((hb - 30) * R) + 0.24 * math.cos(2 * hb * R) + 0.32 * math.cos((3 * hb + 6) * R) - 0.20 * math.cos((4 * hb - 63) * R)
    Sl = 1 + 0.015 * (Lb - 50) ** 2 / math.sqrt(20 + (Lb - 50) ** 2); Sc = 1 + 0.045 * Cpb; Sh = 1 + 0.015 * Cpb * T
    Rt = -2 * math.sqrt(Cpb ** 7 / (Cpb ** 7 + 25 ** 7)) * math.sin(60 * math.exp(-((hb - 275) / 25) ** 2) * R)
    return math.sqrt((dL / Sl) ** 2 + (dC / Sc) ** 2 + (dH / Sh) ** 2 + Rt * (dC / Sc) * (dH / Sh))


def cap(pg): return Image.open(io.BytesIO(pg.screenshot(clip={'x': 20, 'y': 44, 'width': 390, 'height': 844}))).convert('RGB')


def moy(im, r, ang, demi=7, pas=1.0, ep=0.9):
    """la couleur moyenne sur un petit arc (± demi degrés) au rayon r (pt), autour de l'angle ang"""
    px = im.load(); n = 0; s = [0, 0, 0]
    for k in range(-demi * 2, demi * 2 + 1):
        a = ang + math.radians(k / 2.0)
        for e in (-ep, 0, ep):
            x = int(round((CXY[0] + (r + e) * math.cos(a)) * S)); y = int(round((CXY[1] + (r + e) * math.sin(a)) * S)); c = px[x, y]
            n += 1; s[0] += c[0]; s[1] += c[1]; s[2] += c[2]
    return [v / n for v in s]


def exces(c, fond):
    """ce que le halo AJOUTE au fond, en valeurs d'écran (la composition se fait là) : c − fond = opacité × (ton − fond), donc
    PROPORTIONNEL à son opacité — ce que ΔE00 et la lumière linéaire ne sont pas"""
    return sum(abs(c[i] - fond[i]) for i in range(3))


def ouvre(pg, sombre):
    pg.evaluate("()=>{closeAll(); const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click();}"); pg.wait_for_timeout(700)
    pg.evaluate("(d)=>{ try{_zzz.regle(false)}catch(e){} setTheme(d?'dark':'light'); try{ _peloteLumiere.recalibre(); }catch(e){} }", sombre); pg.wait_for_timeout(600)
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4500); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(700)


with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}" + (" window._haloSansTrame=true;" if SONDE else ""))
    if SONDE: print('SONDE : le halo est fabriqué SANS trame')
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(APP); pg.wait_for_timeout(7000)
    for sombre in (0, 1):
        th = 'sombre' if sombre else 'clair'; ouvre(pg, sombre); im = cap(pg); px = im.load()
        fond = px[int(22 * S), int(300 * S)]
        e0 = dE00(moy(im, RS + 1.5, LUM), fond); e4 = dE00(moy(im, RS + 0.04 * D, LUM), fond); e8 = dE00(moy(im, RS + 0.08 * D, LUM), fond)
        au = max(dE00(moy(im, RS + 0.08 * D + 2.5, math.radians(a), demi=4), fond) for a in range(0, 360, 20))
        t('A · [%s] au ras de la silhouette : ΔE00 entre 5 et 9' % th, 5 <= e0 <= 9, '%.2f' % e0)
        t('A · [%s] à 0,04 D : ΔE00 entre 2 et 4' % th, 2 <= e4 <= 4, '%.2f' % e4)
        t('A · [%s] à 0,08 D : ΔE00 sous 1' % th, e8 < 1, '%.2f' % e8)
        t('A · [%s] rien au-delà de 0,08 D' % th, au < 0.5, 'pire ΔE00 %.2f sur 18 directions' % au)
        # ⚠ à l'opposé et en bas, le POIL dépasse de 5,5 pt : on lit le halo à 5 pt de la silhouette (au-delà du poil), et on le compare
        #   au côté éclairé AU MÊME RAYON — sinon on mesure la fourrure, pas le halo
        #   ⚠ et l'opposé exact de la lumière (en bas à droite) tombe DANS le quart inférieur, où le halo est presque nul : la loi
        #   (100 % → 20 %) se vérifie donc à 90° (60 % attendus) et à 135° (32 % attendus) de la lumière, en opacité
        ref = exces(moy(im, RS + 5, LUM), fond); q90 = exces(moy(im, RS + 5, LUM + math.pi / 2), fond) / ref; q135 = exces(moy(im, RS + 5, LUM + 0.75 * math.pi), fond) / ref
        bas = dE00(moy(im, RS + 5, math.pi / 2), fond); opp = dE00(moy(im, RS + 5, LUM + math.pi), fond)
        t('B · [%s] il décroît vers l\'opposé : 60 %% à 90° de la lumière, 32 %% à 135° (± 12)' % th, 0.48 <= q90 <= 0.72 and 0.20 <= q135 <= 0.44, '%.0f %% · %.0f %%' % (100 * q90, 100 * q135))
        t('B · [%s] sur le quart inférieur (l\'opposé y tombe) : presque nul' % th, bas < 1 and opp < 1, 'ΔE00 %.2f en bas · %.2f à l\'opposé' % (bas, opp))
        # C · la plus longue bande à valeur constante, le long de trois profils radiaux, là où le halo se voit encore
        #   une MARCHE de quantification, c'est un escalier : l'écart au fond ne fait que descendre, par paliers. Tramé, il remonte
        #   d'un pixel à l'autre une fois sur trois. On exige au moins 12 % de remontées, et aucun palier de plus de 2 pt.
        pire = 0; rem = 0; tot = 0
        for da in (-25, 0, 25):
            a = LUM + math.radians(da); prec = None; n = 0; av = None
            for k in range(int((RS + 6) * S), int((RS + 0.08 * D - 1.5) * S)):
                c = px[int(round(CXY[0] * S + k * math.cos(a))), int(round(CXY[1] * S + k * math.sin(a)))]
                if c == prec: n += 1
                else: prec = c; n = 1
                pire = max(pire, n); v = sum(abs(c[i] - fond[i]) for i in range(3))
                if av is not None: tot += 1; rem += 1 if v > av else 0
                av = v
        t('C · [%s] trame : aucune bande de plus de 2 pt à valeur constante' % th, pire / S <= 2.0, 'la plus longue : %.1f pt (%d px)' % (pire / S, pire))
        t('C · [%s] trame : aucune marche de quantification (le profil remonte ≥ 12 %% du temps)' % th, tot > 60 and rem / tot >= 0.12, '%.0f %% de remontées sur %d pas' % (100.0 * rem / max(1, tot), tot))
        # E · l'ombre (centre 195 ; 461,35 — demi-axes 52,2 × 8,1) contre son pourtour immédiat
        cen = [sum(px[int((195 + dx) * S), int((461.35 + dy) * S)][c] for dx in (-6, 0, 6) for dy in (-1, 0, 1)) / 9.0 for c in range(3)]
        tour = [sum(px[int((195 + sx * 64) * S), int((461.35 + dy) * S)][c] for sx in (-1, 1) for dy in (-1, 0, 1)) / 6.0 for c in range(3)]
        eo = dE00(cen, tour)
        t('E · [%s] l\'ombre se détache de son pourtour immédiat (ΔE00 ≥ 2)' % th, eo >= 2, '%.2f · centre %s · pourtour %s' % (eo, [round(v) for v in cen], [round(v) for v in tour]))
        if sombre:
            st = pg.evaluate("()=>[getComputedStyle(document.getElementById('auPeloteOmbre')).display, getComputedStyle(document.getElementById('auPeloteFlaque')).display]")
            t('E · [sombre] aucune ombre crème : l\'ombre est le creux de la flaque de lumière', st[0] == 'none' and st[1] != 'none' and all(abs(cen[i] - fond[i]) <= 2 for i in range(3)), '%s · creux %s · fond %s' % (st, [round(v) for v in cen], fond))
        g = pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, R=s=>{const r=document.querySelector(s).getBoundingClientRect(); return [(r.top-dv.top)/k,(r.bottom-dv.top)/k]}; return {pl:R('#auraScreen .enh'), bt:R('#auPartage')}}")
        t('F · [%s] le halo ne touche pas le plateau ; le bouton est à sa place de v118' % th, CXY[1] - RS - 0.08 * D > g['pl'][1] + 8 and abs(g['bt'][0] - 525.47) < 0.3, 'haut du halo %.1f · bas du plateau %.1f · bouton %.2f' % (CXY[1] - RS - 0.08 * D, g['pl'][1], g['bt'][0]))
        pg.evaluate("()=>{_aura.fige(false); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(800)
    ctx.close()
    # D · la respiration, animations permises : le halo au sommet (4,6 s) et au creux (10,6 s) du cycle
    if not SONDE:
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{ try{_zzz.regle(false)}catch(e){} setTheme('dark'); }"); pg.wait_for_timeout(500)
        pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
        vus = []
        for _ in range(60):
            pg.wait_for_timeout(450); u = pg.evaluate("()=>{try{return _peloteLumiere.etat().u}catch(e){return null}}")
            if u is None: continue
            im = cap(pg); f = im.load()[int(22 * S), int(300 * S)]; vus.append((u, exces(moy(im, RS + 5, LUM, demi=10), f)))
        hauts = [e for u, e in vus if u > 0.93]; bas_ = [e for u, e in vus if u < 0.07]
        if hauts and bas_:
            r = (sum(hauts) / len(hauts)) / (sum(bas_) / len(bas_))
            t('D · le halo respire avec la lumière : ± 20 % (sommet ÷ creux = 1,5 ± 0,3)', 1.2 <= r <= 1.8, '%.2f (%d relevés au sommet, %d au creux)' % (r, len(hauts), len(bas_)))
        else: t('D · le halo respire avec la lumière', False, 'sommet ou creux non saisi (%d relevés)' % len(vus))
        ctx.close()
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
