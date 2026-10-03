#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_garder_toile.py — « GARDER TA TOILE » : EN GRAS, UNE COULEUR DE LA PALETTE RETIRÉE À CHAQUE RETOUR (v124, Tom, 3 oct. 2026). WebKit.

« Le texte passe en gras. Sa couleur est tirée au hasard dans la palette choisie, et retirée chaque fois qu'on revient sur la page, par
n'importe quel chemin. Même règle de contraste (≥ 4,5:1 s'il s'agit de texte courant, ≥ 3:1 s'il est en grand), même repli sur l'encre,
jamais de kaki. Juge : vingt allers-retours, au moins deux teintes différentes vues, contraste toujours tenu. »

La rangée « Garder ta Toile » des Réglages (`#compteCard .k`) : du texte courant (13 px) → 4,5:1, EN DUR (§7), face au fond réellement
peint sous elle. Le gras : Atkinson 700 (la face embarquée). L'encre du mode : #201908 (clair) / #F7F0DE (sombre).
Vingt allers-retours par cas, deux chemins alternés — le bouton des Réglages depuis l'accueil, et un sous-écran qu'on referme (les notifications) —
sur deux palettes (Ingénu, Irascible) et les deux thèmes. LE VERDICT VIENT DU RENDU (couleur et fond calculés) ; ce qui était tirable est
recalculé ici depuis la palette lue.
  1 · en gras (Atkinson 700) ;
  2 · contraste ≥ 4,5:1 à chaque retour ; jamais kaki (hors l'encre du mode, le repli décidé) ;
  3 · la couleur est un ton de la palette, ou l'encre du mode quand aucun ton n'est tirable ;
  4 · au moins deux teintes différentes vues sur vingt retours (quand au moins deux tons sont tirables) ;
  5 · elle est RETIRÉE au retour : par les deux chemins, la teinte change d'un retour à l'autre au moins une fois.
Preuve (§7) : sur `sauvegardes/app-avant-v124.html` il ROUGIT (Atkinson 500, une seule couleur).
"""
import os, sys, io, re, math
ICI = os.path.dirname(os.path.abspath(__file__))
_src = io.open(os.path.join(ICI, 'redteam_corps.py'), encoding='utf-8').read()
exec(_src[_src.index('def lin(v):'):_src.index('# ce qui est PEINT')])
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
N = 20
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-96s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


def lumrel(c): return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])
def contraste(a, b):
    x, y = lumrel(a), lumrel(b); return (max(x, y) + 0.05) / (min(x, y) + 0.05)
def rgb(v): return [int(x) for x in re.findall(r'\d+', v or '')[:3]] or None


LIT = r"""()=>{ const k=document.querySelector('#settingsScreen #compteCard .k'); if(!k) return null; const cs=getComputedStyle(k), r=k.getBoundingClientRect();
  const dv=document.getElementById('device').getBoundingClientRect(); const e=document.elementFromPoint(dv.left+dv.width/2, dv.top+dv.height*0.5); if(!(e&&e.closest('#settingsScreen'))) return null;   /* la page des Réglages est à l'écran (la rangée, elle, est sous le pli) */
  let fond=null, a=k; while(a&&a!==document.documentElement){ const m=/rgba?\((\d+)[, ]+(\d+)[, ]+(\d+)(?:[, \/]+([\d.]+))?\)/.exec(getComputedStyle(a).backgroundColor); if(m&&(m[4]===undefined||+m[4]>0.98)){ fond=[+m[1],+m[2],+m[3]]; break; } a=a.parentElement; }
  return {mot:k.textContent.trim(), col:cs.color, fill:cs.webkitTextFillColor, ff:cs.fontFamily, fw:cs.fontWeight, fs:cs.fontSize, fond:fond, pal:Toile.cols().map(c=>[c[0]|0,c[1]|0,c[2]|0])}; }"""
OUVRE = "()=>{ document.getElementById('settingsBtn').click(); }"
# le second chemin : un sous-écran des Réglages (les notifications) qu'on referme — on REVIENT sur la page sans passer par son bouton
SOUS = "()=>{ const c=[...document.querySelectorAll('#settingsScreen .scard')].find(e=>/Notifications/i.test(e.textContent)&&getComputedStyle(e).display!=='none'); if(c) c.click(); return !!c; }"
FERME_SOUS = "()=>{ const s=[...document.querySelectorAll('.screen.show, .sheet.show')].filter(e=>e.id!=='settingsScreen'&&e.id!=='auraScreen'&&e.id!=='studioScreen'); const x=s.length&&s[s.length-1].querySelector('.closeb'); if(x){ x.click(); return true; } return false; }"

with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(APP); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for pal in ('signal', 'irascible'):
        for th in ('light', 'dark'):
            pg.evaluate("([t,p])=>{ try{closeAll()}catch(e){} setTheme(t); try{Toile.setPalette(p)}catch(e){} }", [th, pal]); pg.wait_for_timeout(500)
            encre = [32, 25, 8] if th == 'light' else [247, 240, 222]
            vus = []; bas = 99.0; n_kaki = 0; hors = 0; gras = 0; lus = 0; tir = 0; sous_ok = 0; ex = ''
            for i in range(N):
                if i % 2 == 0:
                    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(450); pg.evaluate(OUVRE)
                else:
                    if pg.evaluate(SOUS):
                        pg.wait_for_timeout(700)
                        if pg.evaluate(FERME_SOUS): sous_ok += 1
                        else: pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(450); pg.evaluate(OUVRE)
                    else:
                        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(450); pg.evaluate(OUVRE)
                pg.wait_for_timeout(900); m = pg.evaluate(LIT)
                if not m: continue
                lus += 1; c = rgb(m['fill'] or m['col']); f = m['fond'] or ([247, 240, 222] if th == 'light' else [5, 3, 2])
                if str(m['ff']).lstrip('"\'').startswith('Atkinson') and str(m['fw']) == '700': gras += 1
                r_ = contraste(c, f)
                if r_ < bas: bas = r_; ex = 'retour %d : %s sur %s' % (i + 1, c, f)
                if c != encre and kaki(c): n_kaki += 1
                # ⚑ v125 (Tom) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_garder_toile-avant-v125.py). « La teinte tirée garde sa teinte OKLCH
                #   et s'assombrit, ou s'éclaircit en sombre, juste assez pour atteindre le contraste. Plus de repli sur l'encre. » Jamais l'encre ;
                #   la teinte OKLCH du texte est celle d'un ton de la palette (à 8° près ; un ton presque gris n'a pas de teinte à comparer).
                T = m['pal']; tir = max(tir, len(set(tuple(q) for q in T)))
                hc = oklch(c)
                if c == encre or not any((abs((hc[2] - oklch(q)[2] + 180) % 360 - 180) <= 8) or oklch(q)[1] < 0.03 or hc[1] < 0.02 for q in T): hors += 1
                vus.append(tuple(c))
            tag = '[%s · %s]' % (pal, 'clair' if th == 'light' else 'sombre')
            t('%s les %d retours sont lus (dont %d par un sous-écran refermé)' % (tag, N, sous_ok), lus == N, '%d lus' % lus)
            t('1 · %s « Garder ta Toile » est en gras (Atkinson 700)' % tag, lus > 0 and gras == lus, '%d sur %d' % (gras, lus))
            t('2 · %s contraste ≥ 4,5:1 à chaque retour' % tag, lus > 0 and bas >= 4.5, 'le plus bas : %.2f · %s' % (bas, ex))
            t('2 · %s jamais kaki' % tag, lus > 0 and n_kaki == 0, '%d retour(s)' % n_kaki)
            t('3 · %s jamais à l\'encre : la teinte d\'un ton de la palette, clarté ajustée' % tag, lus > 0 and hors == 0, '%d retour(s) hors règle · %d ton(s)' % (hors, tir))
            t('4 · %s au moins deux teintes différentes vues (si deux tons sont tirables)' % tag, lus > 0 and (len(set(vus)) >= 2 or tir < 2), '%d teinte(s) vue(s), %d tirable(s)' % (len(set(vus)), tir))
            chg = sum(1 for a_, b_ in zip(vus, vus[1:]) if a_ != b_)
            t('5 · %s la teinte est retirée au retour (elle change d\'un retour à l\'autre, si deux tons sont tirables)' % tag, lus > 0 and (chg >= 1 or tir < 2), '%d changement(s) sur %d retours' % (chg, max(0, len(vus) - 1)))
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:8]))
sys.exit(1 if ko else 0)
