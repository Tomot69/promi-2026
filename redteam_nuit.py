#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_nuit.py — LE Zzz : LA NUIT, L'APP SE REPOSE (v118, Tom, 2 oct. 2026). WebKit, fuseau et horloge simulés.

Les règles, EN DUR ici (§7 — le juge porte la décision, l'app la respecte) :
  1 · premier lancement : thème CLAIR (même si le téléphone est en sombre), Zzz ACTIVÉ ;
  2 · clair + Zzz : du coucher du soleil + 1 h au lever, sombre DE NUIT ; au lever, retour au clair ;
  3 · clair, Zzz éteint : toujours clair ;
  4 · sombre + Zzz : le cran de nuit sur les mêmes heures ; le jour, sombre ordinaire ;
  5 · sombre, Zzz éteint : sombre ordinaire, même la nuit ;
  6 · les deux choix sont mémorisés d'une ouverture à l'autre.
Le soleil : NOAA, aux coordonnées de référence du fuseau — vérifié contre des heures d'ALMANACH écrites ici (Paris, la référence
d'un appareil à Marseille : 21 juin 2026, lever 05:47 · coucher 21:58 ; 21 déc. 2026, 08:41 · 16:56 ; ± 3 min) et contre un
second calcul, indépendant, fait par le juge. Fuseau inconnu : 22 h – 7 h.
AUCUNE BASCULE SOUS LES YEUX : l'heure franchit le seuil pendant qu'un écran est affiché → rien ne bouge ; au changement d'écran
(ou au retour au premier plan) → le thème change, d'un coup (aucune transition).
Le cran de nuit : les jetons crème et blanc clairs baissent de 0,06 de luminance OKLCH (± 0,006), teinte gardée ; TOUS les autres
jetons sont identiques AU HEX PRÈS ; les couleurs de nature et d'état PEINTES (champ d'une fiche, légende de l'Aura) sont exactes ;
contraste du texte ≥ 7 : 1 ; aucun filtre, aucun voile.
Preuve (§7) : `--sonde` fait basculer l'app EN DIRECT (une réévaluation toutes les 150 ms) → le juge doit ROUGIR.
⚠ v118 : le bouton « Zzz » du Studio n'est pas posé (la ligne ne reçoit pas trois boutons sans déplacer ses voisins — rapport
v118) ; tant qu'il manque, le Zzz ne s'active pas seul au premier lancement : la ligne 1 est ROUGE, nommément, jusqu'à sa pose.
"""
import os, sys, math, datetime
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
SONDE = '--sonde' in sys.argv
NATURES = {'promi': (130, 174, 248), 'chiche': (255, 184, 210)}
ETATS = {(221, 77, 35), (41, 21, 71), (0, 52, 26), (167, 124, 247), (51, 186, 108)}     # à tenir · en cours · tenu, et leurs claires — §3
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-78s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-78s KO  %s' % (nom, detail))


# ── le soleil, recalculé ICI (Meeus, autre écriture que celle de l'app) ───────────────────────────────────────────
def soleil(y, m, d, lat, lon):
    n = datetime.date(y, m, d).toordinal() - datetime.date(2000, 1, 1).toordinal() - lon / 360.0            # jours depuis J2000 (1er janv. 2000, 12 h TU), au midi local
    g = math.radians((357.5291 + 0.98560028 * n) % 360)
    c = 1.9148 * math.sin(g) + 0.0200 * math.sin(2 * g) + 0.0003 * math.sin(3 * g)
    lam = math.radians((math.degrees(g) + c + 180 + 102.9372) % 360)
    jt = 2451545.0 + n + 0.0053 * math.sin(g) - 0.0069 * math.sin(2 * lam)
    dec = math.asin(math.sin(lam) * math.sin(math.radians(23.4397)))
    ch = (math.sin(math.radians(-0.833)) - math.sin(math.radians(lat)) * math.sin(dec)) / (math.cos(math.radians(lat)) * math.cos(dec))
    w = math.degrees(math.acos(ch)) / 360.0
    def ms(j): return (j - 2440587.5) * 86400000.0
    return ms(jt - w), ms(jt + w)


def oklch(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = f(c[0] / 255), f(c[1] / 255), f(c[2] / 255)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3); m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s; a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s; bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def contraste(a, b):
    def lu(c):
        f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(c[0] / 255) + 0.7152 * f(c[1] / 255) + 0.0722 * f(c[2] / 255)
    x, y = lu(a), lu(b); return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def hexrgb(h): h = h.strip().lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


ETAT = "()=>{const d=document.getElementById('device'); return {clair:d.classList.contains('light'), nuit:d.classList.contains('zzz-nuit'), creme:getComputedStyle(document.documentElement).getPropertyValue('--c-creme95').trim().toUpperCase(), e:window._zzz?_zzz.etat():null}}"
HEURE = "(iso)=>{ window.__t=Date.parse(iso); window._zzzMaintenant=()=>window.__t; }"
ECRAN = "()=>{ closeAll(); }"                      # un changement d'écran


def page(ctx, vierge=False):
    pg = ctx.new_page()
    pg.goto(APP); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    return pg


def attend(pg, clair, nuit, nom, ms=900):
    pg.wait_for_timeout(ms); e = pg.evaluate(ETAT)
    t(nom, e['clair'] == clair and e['nuit'] == nuit, 'clair=%s cran=%s crème=%s' % (e['clair'], e['nuit'], e['creme'])); return e


with sync_playwright() as p:
    b = p.webkit.launch()
    # ── 1 · premier lancement, téléphone en SOMBRE ────────────────────────────────────────────────────────────────
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, timezone_id='Europe/Paris', color_scheme='dark')
    pg = page(ctx); e = pg.evaluate(ETAT)
    t('1 · premier lancement : thème CLAIR, même si le téléphone est en sombre', bool(e['e']) and e['e']['choix'] == 'light' and e['clair'], str(e['e'] and e['e']['choix']))
    t('1 · premier lancement : Zzz ACTIVÉ', bool(e['e']) and e['e']['zzz'] is True, 'zzz=%s · bouton posé=%s' % (e['e'] and e['e']['zzz'], e['e'] and e['e']['bouton']))
    ctx.close()

    # ── le soleil : l'almanach, puis le second calcul ─────────────────────────────────────────────────────────────
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, timezone_id='Europe/Paris', device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = page(ctx)
    if SONDE:
        pg.evaluate("()=>{ setInterval(function(){ try{ _zzz.evalue(); }catch(e){} }, 150); }"); print('SONDE : l\'app réévalue le thème EN DIRECT, toutes les 150 ms')
    ALMANACH = {'2026-06-21': ('05:47', '21:58', '+02:00'), '2026-12-21': ('08:41', '16:56', '+01:00')}
    for jour, (lv, cc, dec) in ALMANACH.items():
        f = pg.evaluate("(iso)=>{const f=_zzz.fenetre(Date.parse(iso)); return [f.lever, f.coucher, f.source]}", jour + 'T12:00:00' + dec)
        def hm(ms): return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone(datetime.timedelta(hours=int(dec[1:3])))).strftime('%H:%M:%S')
        def ecart(ms, ref): h, m = ref.split(':'); x = datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone(datetime.timedelta(hours=int(dec[1:3])))); return abs(x.hour * 60 + x.minute + x.second / 60 - (int(h) * 60 + int(m)))
        t('soleil · %s (Paris) : l\'almanach, ± 3 min' % jour, f[2] == 'soleil' and ecart(f[0], lv) <= 3 and ecart(f[1], cc) <= 3, 'lever %s · coucher %s' % (hm(f[0]), hm(f[1])))
        y, m, d = map(int, jour.split('-')); a, z = soleil(y, m, d, 48.87, 2.33)
        t('soleil · %s : le second calcul, ± 3 min' % jour, abs(f[0] - a) <= 180000 and abs(f[1] - z) <= 180000, 'écarts %.1f / %.1f min' % ((f[0] - a) / 60000, (f[1] - z) / 60000))

    # ── les bornes de la nuit : Marseille (fuseau de Paris) en juin et en décembre, puis un fuseau inconnu ────────
    BORNES = [('juin', None, [('2026-06-21T22:50:00+02:00', False), ('2026-06-21T23:05:00+02:00', True), ('2026-06-22T00:10:00+02:00', True), ('2026-06-22T05:40:00+02:00', True), ('2026-06-22T05:55:00+02:00', False), ('2026-06-21T15:00:00+02:00', False)]),
              ('décembre', None, [('2026-12-21T17:50:00+01:00', False), ('2026-12-21T18:02:00+01:00', True), ('2026-12-22T08:35:00+01:00', True), ('2026-12-22T08:48:00+01:00', False)]),
              ('fuseau inconnu', 'Mars/Olympus', [('2026-06-21T21:59:00+02:00', False), ('2026-06-21T22:01:00+02:00', True), ('2026-06-22T06:59:00+02:00', True), ('2026-06-22T07:01:00+02:00', False)])]
    for nom, tz, cas in BORNES:
        pg.evaluate("(z)=>{ if(z) window._zzzFuseau=z; else delete window._zzzFuseau; }", tz)
        r = [pg.evaluate("(iso)=>_zzz.nuit(Date.parse(iso))", iso) for iso, _ in cas]
        t('la nuit · %s : coucher + 1 h → lever' % nom, r == [v for _, v in cas], ' '.join('%s%s' % (iso[11:16], '☾' if x else '☀') for (iso, _), x in zip(cas, r)))
        if tz: t('la nuit · %s : la source est « 22 h – 7 h »' % nom, pg.evaluate("()=>_zzz.etat().source") == '22h-7h')
    pg.evaluate("()=>{ delete window._zzzFuseau; }")

    # ── 2 · clair + Zzz ───────────────────────────────────────────────────────────────────────────────────────────
    pg.evaluate(HEURE, '2026-12-21T15:00:00+01:00'); pg.evaluate("()=>{ setTheme('light'); _zzz.regle(true); closeAll(); }")
    attend(pg, True, False, '2 · clair + Zzz, le jour : clair')
    # l'heure passe le seuil PENDANT que l'accueil est affiché
    pg.evaluate(HEURE, '2026-12-21T18:05:00+01:00')
    attend(pg, True, False, '2 · le seuil franchi SOUS LES YEUX : rien ne bouge', 2500)
    pg.evaluate(ECRAN)
    tr = pg.evaluate("()=>getComputedStyle(document.getElementById('device')).transitionDuration+'|'+document.getElementById('device').classList.contains('zzz-coupe')")
    e = attend(pg, False, True, '2 · au changement d\'écran : sombre DE NUIT', 700)
    t('2 · la bascule se fait sans fondu', tr.endswith('true') or tr.startswith('0s'), tr)
    pg.evaluate(HEURE, '2026-12-22T08:50:00+01:00')
    attend(pg, False, True, '2 · le lever passé SOUS LES YEUX : rien ne bouge', 2500)
    pg.evaluate("()=>{ document.dispatchEvent(new Event('visibilitychange')); }")
    attend(pg, True, False, '2 · au retour au premier plan : le clair revient')
    # un écran qui S'OUVRE compte aussi pour un changement d'écran
    pg.evaluate(HEURE, '2026-12-22T18:30:00+01:00'); pg.evaluate("()=>{ document.getElementById('settingsBtn').click(); }")
    attend(pg, False, True, '2 · à l\'ouverture d\'un écran (les Réglages) : sombre de nuit', 1300)

    # ── le cran de nuit, pendant qu'il est posé ───────────────────────────────────────────────────────────────────
    J = pg.evaluate(r"""()=>{ const t=document.getElementById('lot-TOKENS-css').textContent, re=/(--c-[\w-]+?)\s*:\s*(#[0-9a-fA-F]{6})\b/g, cs=getComputedStyle(document.documentElement), out=[], vu={}; let m;
        while((m=re.exec(t))){ if(vu[m[1]]) continue; vu[m[1]]=1; out.push([m[1], m[2].toUpperCase(), cs.getPropertyValue(m[1]).trim().toUpperCase()]); } return out; }""")
    neutres = [x for x in J if x[0].startswith(('--c-creme', '--c-blanc')) and oklch(hexrgb(x[1]))[0] >= 0.80]
    autres = [x for x in J if x not in neutres]
    bouges = [x for x in autres if x[1] != x[2]]
    t('cran · tous les jetons qui ne sont pas des neutres clairs sont identiques AU HEX PRÈS', not bouges and len(autres) > 150, '%d jetons, %d ont bougé %s' % (len(autres), len(bouges), bouges[:3]))
    pire_l = 0; pire_h = 0
    for n_, de, a in neutres:
        o, q = oklch(hexrgb(de)), oklch(hexrgb(a)); pire_l = max(pire_l, abs((q[0] - o[0]) + 0.06))
        if o[1] > 0.012:      # la teinte d'un ton presque gris n'est tenue qu'à l'arrondi des 8 bits près : on juge l'écart EN TROP
            dh = min(abs(q[2] - o[2]), 360 - abs(q[2] - o[2])); pire_h = max(pire_h, dh - math.degrees(math.atan(0.003 / o[1])))
    t('cran · les neutres clairs baissent de 0,06 de luminance OKLCH (± 0,006)', len(neutres) >= 20 and pire_l <= 0.006, '%d jetons, pire écart %.4f' % (len(neutres), pire_l))
    t('cran · leur teinte est gardée (± 2°, hors arrondi des 8 bits)', pire_h <= 2.0, 'pire écart hors arrondi %.2f°' % pire_h)
    fond = pg.evaluate("()=>{const m=/(\\d+)[, ]+(\\d+)[, ]+(\\d+)/.exec(getComputedStyle(document.getElementById('device')).backgroundColor); return m?[+m[1],+m[2],+m[3]]:null}")
    creme = hexrgb(e['creme']) if e['creme'].startswith('#') else (0, 0, 0)
    t('cran · le contraste du texte reste ≥ 7 : 1', bool(fond) and contraste(creme, fond) >= 7, '%.1f : 1 (%s sur %s)' % (contraste(creme, fond or (0, 0, 0)), e['creme'], fond))
    filt = pg.evaluate("()=>[...document.querySelectorAll('html,body,.frame,#device')].map(e=>{const c=getComputedStyle(e); return c.filter+'|'+c.mixBlendMode+'|'+c.opacity}).filter(s=>s!=='none|normal|1')")
    t('cran · aucun filtre, aucun voile', not filt, str(filt))
    # les couleurs PEINTES : le champ d'une fiche (nature), la légende de l'Aura (états)
    for nat, c in NATURES.items():
        px = pg.evaluate("(n)=>{ closeAll(); const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.photo&&(n==='chiche'?q.chiche:!q.chiche)&&q.status!=='tenu'); if(!p) return null; openDetail(p.id); return new Promise(r=>setTimeout(()=>{const cv=document.getElementById('dpTrameCv'), k=cv.width/390, d=cv.getContext('2d').getImageData(Math.round(4*k),Math.round(4*k),1,1).data; r([d[0],d[1],d[2]]);},1500)); }", nat)
        t('cran · le champ d\'une fiche %s garde sa couleur, au hex près' % nat, px is not None and tuple(px) == c, str(px))
    LEGENDE = "()=>{ closeAll(); document.getElementById('souffleBtn').click(); return new Promise(r=>setTimeout(()=>r([...document.querySelectorAll('#auraScreen .au-lg i')].map(i=>{const m=/(\\d+)[, ]+(\\d+)[, ]+(\\d+)/.exec(getComputedStyle(i).backgroundColor); return m?[+m[1],+m[2],+m[3]]:null})),2500)); }"
    lgN = pg.evaluate(LEGENDE)
    t('cran · la légende de l\'Aura porte trois couleurs d\'état exactes', bool(lgN) and len(lgN) == 3 and all(x and tuple(x) in ETATS for x in lgN), str(lgN))
    pal = pg.evaluate("()=>JSON.stringify(Toile.cols())")
    t('cran · la palette des dalles n\'a pas bougé', pal == pg.evaluate("()=>{const p=Toile.palettes()[Toile.getPalette()]; return JSON.stringify(p.cols)}"), pal[:60])
    pg.evaluate("()=>{ const x=document.querySelector('#auraScreen .closeb'); if(x) x.click(); closeAll(); }"); pg.wait_for_timeout(600)

    # ── 3 · clair, Zzz éteint ─────────────────────────────────────────────────────────────────────────────────────
    pg.evaluate(HEURE, '2026-12-21T23:30:00+01:00'); pg.evaluate("()=>{ setTheme('light'); _zzz.regle(false); closeAll(); }")
    attend(pg, True, False, '3 · clair, Zzz éteint, la nuit : toujours clair')
    # ── 4 · sombre + Zzz ──────────────────────────────────────────────────────────────────────────────────────────
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(true); closeAll(); }")
    attend(pg, False, True, '4 · sombre + Zzz, la nuit : le cran de nuit')
    pg.evaluate(HEURE, '2026-12-22T12:00:00+01:00'); pg.evaluate(ECRAN)
    attend(pg, False, False, '4 · sombre + Zzz, le jour : sombre ordinaire')
    lgJ = pg.evaluate(LEGENDE); pg.evaluate("()=>{ const x=document.querySelector('#auraScreen .closeb'); if(x) x.click(); closeAll(); }"); pg.wait_for_timeout(500)
    t('cran · la légende de l\'Aura est la MÊME, au hex près, en sombre ordinaire et en sombre de nuit', lgJ == lgN, '%s / %s' % (lgJ, lgN))
    # ── 5 · sombre, Zzz éteint ────────────────────────────────────────────────────────────────────────────────────
    pg.evaluate(HEURE, '2026-12-21T23:30:00+01:00'); pg.evaluate("()=>{ _zzz.regle(false); closeAll(); }")
    e5 = attend(pg, False, False, '5 · sombre, Zzz éteint, la nuit : sombre ordinaire')
    t('5 · la crème est revenue à sa valeur', e5['creme'] == '#F7F0DE', e5['creme'])
    # ── 6 · la mémoire ────────────────────────────────────────────────────────────────────────────────────────────
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(true); }"); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(6500); e6 = pg.evaluate(ETAT)
    t('6 · après rechargement : le choix « sombre » et le Zzz activé sont retrouvés', bool(e6['e']) and e6['e']['choix'] == 'dark' and e6['e']['zzz'] is True, str(e6['e'] and (e6['e']['choix'], e6['e']['zzz'])))
    pg.evaluate("()=>{ setTheme('light'); _zzz.regle(false); }"); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(6500); e6 = pg.evaluate(ETAT)
    t('6 · après rechargement : le choix « clair » et le Zzz éteint sont retrouvés', bool(e6['e']) and e6['e']['choix'] == 'light' and e6['e']['zzz'] is False and e6['clair'], str(e6['e'] and (e6['e']['choix'], e6['e']['zzz'])))
    b.close()

print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
