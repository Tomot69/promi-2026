#!/usr/bin/env python3
"""
redteam_sans_main.py — v147 (Tom, 15 oct. 2026, C-139, remplace C-110) : « Supprime la main PARTOUT, sans exception, avec son code, ses
réglages et ses juges. »

Comme Tom (banc_tom : WebKit, 390 × 844 ×3, doigt, webdriver masqué, Toile vide, paroles plantées par l'app) :
  1 · le code : `window.GesteFantome` n'existe pas ; aucune couche `#gesteFantome` ; aucune règle CSS ni aucun appel ne la nomme hors commentaire ;
  2 · les réglages : un téléphone qui porte encore les drapeaux d'avant (`geste_v`, `geste_vu_*`) les perd au chargement ; la rangée
      « Revoir les gestes » n'existe plus, « Revoir la présentation » est la seule rangée de rejeu ;
  3 · l'écran : sur une fiche à tenir (Promi, puis Chiche) laissée 7 s sans toucher, sur le trait de l'onboarding laissé 7 s, sur la page +,
      au Studio et à l'Aura : aucune main, aucun nœud `[data-main]`, aucun tracé qui grandit seul.
Rougit sur la version d'avant (`--page=zz-av146.html`).
"""
import sys, re, io
sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
PAGE = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('%s  %s  %s' % ('OK' if c else 'KO', nom, str(d)[:240]), flush=True)
# 1 · le code, sans navigateur : on retire les commentaires /* … */ des scripts et des styles, puis on cherche le nom
S = io.open(PAGE, encoding='utf-8').read()
code = re.sub(r'/\*.*?\*/', '', S, flags=re.S)
code = re.sub(r'<!--.*?-->', '', code, flags=re.S)
vus = sorted(set(m.group(0) for m in re.finditer(r'GesteFantome|gesteFantome|geste_vu_|data-main\b|Revoir les gestes', code)))
reste_nettoyage = [v for v in vus if v not in ('geste_vu_',)]   # le nettoyage des drapeaux d'avant nomme geste_vu_ : c'est lui qui les retire
juge('le code : aucun appel, aucune règle ne nomme la main (hors commentaires et hors le nettoyage des drapeaux)', not reste_nettoyage, vus)
VOIT = """()=>({gf:typeof window.GesteFantome, couche:!!document.getElementById('gesteFantome'), main:document.querySelectorAll('[data-main],[data-main-g],#gesteFantome svg').length,
  cles:Object.keys(localStorage).filter(k=>k.indexOf('geste_vu_')===0||k==='geste_v')})"""
with sync_playwright() as p:
    b = p.webkit.launch()
    # 2 · un téléphone qui porte les drapeaux d'avant
    ctx = B.contexte(b, stockage={'geste_v': '143', 'geste_vu_tenir': '1', 'geste_vu_pelote': '1'})
    pg = B.ouvre(ctx, PAGE)
    v = pg.evaluate(VOIT)
    juge('le composant n\'existe pas (window.GesteFantome)', v['gf'] == 'undefined', v['gf'])
    juge('les drapeaux d\'avant (geste_v, geste_vu_*) sont retirés au chargement', not v['cles'], v['cles'])
    pg.evaluate("()=>{ document.getElementById('settingsScreen').classList.add('show'); }"); pg.wait_for_timeout(800)
    r = pg.evaluate("()=>({gestes:[...document.querySelectorAll('#settingsScreen .scard')].filter(e=>/Revoir les gestes/.test(e.textContent)).length, pres:[...document.querySelectorAll('#settingsScreen .scard')].filter(e=>/Revoir la présentation/.test(e.textContent)).length})")
    juge('aux Réglages : plus de « Revoir les gestes », une seule « Revoir la présentation »', r['gestes'] == 0 and r['pres'] == 1, r)
    pg.evaluate("()=>{ document.getElementById('settingsScreen').classList.remove('show'); try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
    ctx.close()
    # 3 · l'écran, sur un stockage neuf (aucun drapeau : c'est là que la main paraissait)
    ctx = B.contexte(b); pg = B.ouvre(ctx, PAGE)
    for nat, titre in ((0, 'arroser le figuier'), (1, 'sauter du plongeoir')):
        B.plante_doigt(pg, titre, nature=nat); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ try{ window._peaufSortie && window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(800)
        pid = pg.evaluate("(t)=>(promises.find(q=>q.title===t)||{}).id", titre)
        pg.evaluate("(id)=>openDetail(id)", pid)
        mx = 0
        for i in range(28):
            pg.wait_for_timeout(250); v = pg.evaluate(VOIT); mx = max(mx, v['main'] + (1 if v['couche'] else 0))
        juge('fiche à tenir (%s) laissée 7 s sans toucher : aucune main' % ('Chiche' if nat else 'Promi'), mx == 0, '%d nœud(s) de main vus' % mx)
    pg.evaluate("()=>{ try{ window._peaufSortie && window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(700)
    for nom, js in (('page +', "()=>{ document.getElementById('createBtn').click(); }"), ('Studio', "()=>{ if(window.openStudio) openStudio(); else document.getElementById('studioBtn').click(); }"),
                    ('Aura', "()=>{ document.getElementById('auraBtn')&&document.getElementById('auraBtn').click(); }")):
        try: pg.evaluate(js)
        except Exception: pass
        mx = 0
        for i in range(16):
            pg.wait_for_timeout(250); v = pg.evaluate(VOIT); mx = max(mx, v['main'] + (1 if v['couche'] else 0))
        juge('%s laissé 4 s : aucune main' % nom, mx == 0, '%d nœud(s)' % mx)
        pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(600)
    ctx.close()
    # le trait de l'onboarding (premier lancement), laissé 7 s
    ctx = B.contexte(b, onb=False); pg = B.ouvre(ctx, PAGE, attente=4000)
    mx = 0
    for i in range(28):
        pg.wait_for_timeout(250); v = pg.evaluate(VOIT); mx = max(mx, v['main'] + (1 if v['couche'] else 0))
    juge('onboarding laissé 7 s : aucune main', mx == 0, '%d nœud(s)' % mx)
    ctx.close(); b.close()
n = sum(res); print('\n%d / %d' % (n, len(res))); sys.exit(0 if n == len(res) else 1)
