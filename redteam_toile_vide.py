#!/usr/bin/env python3
"""
redteam_toile_vide.py — v147 (C-136, Tom : « la Toile vide sort colorée au chargement, une fois sur six »). TRENTE CHARGEMENTS.

La règle : une Toile SANS parole est vide — aucune cellule colorée, à aucun instant du chargement, et pas seulement à la fin.
  A · comme Tom (WebKit, 390 × 844 × 3, webdriver masqué), premier lancement (onboarding) : `Toile.colored()` vaut 0 à CHAQUE relevé
      (toutes les 40 ms, de la première image à 9 s) — 10 chargements ;
  B · comme Tom, onboarding déjà fait et aucune sauvegarde : idem — 5 chargements ;
  C · le chemin des juges (Chromium, navigateur piloté : le jeu de démonstration s'y pose, puis l'onboarding le retire) : à 9 s, 0 cellule
      colorée et 0 parole ; à aucun instant la Toile entière colorée (l'ancien remplissage d'authentification) — 15 chargements.
La valeur se lit dans le moteur : `Toile.colored()` compte les graines qui ne sont pas grises (l'état réel du semis, pas une déclaration).
Rougit sur la version d'avant (`--page=zz-av146.html`). Option `--n=` (multiplie les chargements, défaut 1 → 30).
"""
import sys, time
sys.path.insert(0, '.')
import banc_tom
from playwright.sync_api import sync_playwright
PAGE = 'app.html'; K = 1
for a in sys.argv[1:]:
    if a.startswith('--page='): PAGE = a.split('=', 1)[1]
    if a.startswith('--n='): K = float(a.split('=', 1)[1])
URL = 'http://127.0.0.1:8752/' + PAGE
HOOK = r"""(function(){ window.__tl=[]; function arme(){ var T=window.Toile; if(!T||!T.colored) return setTimeout(arme,5);
  var der=-2; (function tic(){ var c=-1; try{c=T.colored();}catch(e){} if(c!==der){ window.__tl.push([performance.now()|0,c]); der=c; } setTimeout(tic,40); })(); } arme(); })();"""
ETAT = "()=>({n:((typeof promises!=='undefined'&&promises)||[]).filter(p=>!p.draft).length, c:window.Toile.colored(), tot:window.Toile.cells(), tl:window.__tl})"
OK = KO = 0; rouges = []
def juge(nom, bon, detail=''):
    global OK, KO
    if bon: OK += 1
    else: KO += 1; rouges.append('%s — %s' % (nom, detail))
with sync_playwright() as p:
    wk = p.webkit.launch()
    for mode, n in (('A', int(10 * K)), ('B', int(5 * K))):
        for i in range(n):
            ctx = banc_tom.contexte(wk, onb=(mode == 'B'), guide=True)
            ctx.add_init_script(HOOK)
            pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(9000)
            e = pg.evaluate(ETAT)
            vus = [c for t, c in e['tl'] if c > 0]
            juge('%s%d' % (mode, i + 1), e['n'] == 0 and e['c'] == 0 and not vus,
                 '%d parole(s), %d colorée(s) à 9 s, jusqu\'à %s colorée(s) pendant le chargement %s' % (e['n'], e['c'], max(vus) if vus else 0, e['tl'][:6]))
            print('%s%-2d paroles %d · colorées à 9 s %d · au plus %d' % (mode, i + 1, e['n'], e['c'], max(vus) if vus else 0), flush=True)
            ctx.close()
    wk.close()
    ch = p.chromium.launch()
    for i in range(int(15 * K)):
        ctx = ch.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script(HOOK)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(9000)
        e = pg.evaluate(ETAT)
        plein = [t for t, c in e['tl'] if c >= e['tot'] and c > 0]
        juge('C%d' % (i + 1), e['n'] == 0 and e['c'] == 0 and not plein,
             '%d parole(s), %d colorée(s) à 9 s sur %d, Toile entière colorée à %s ms' % (e['n'], e['c'], e['tot'], plein[:3]))
        print('C%-2d paroles %d · colorées à 9 s %d/%d · toile entière %s' % (i + 1, e['n'], e['c'], e['tot'], 'oui' if plein else 'non'), flush=True)
        ctx.close()
    ch.close()
for r in rouges: print('  ✗', r)
print('\n%d / %d' % (OK, OK + KO))
sys.exit(0 if KO == 0 else 1)
