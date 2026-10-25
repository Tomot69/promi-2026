#!/usr/bin/env python3
"""redteam_pinceau_rail.py — ⚑ v163b (Tom, C-196 ; AUDIT-BOUTONS 2, 10, 31, point 8) : LES DOUZE TRAITS S'ATTEIGNENT, LES PAYANTS SONT DERRIÈRE LE MUR.

« Le rail du pinceau défile : les douze traits s'atteignent, sur la page + et dans Peaufiner. Les traits payants passent derrière le mur de Ma Parole ! :
plus de « — 0,50 € » en pointillé, plus d'application sans payer. »
Banc comme Tom (WebKit ×3, doigt), sans Ma Parole ! puis membre :
  A · page + et Peaufiner d'une fiche : le rail défile (la molette horizontale, que WebKit fait défiler comme un doigt — les glissés du banc, créés en
      JavaScript, ne font défiler aucun conteneur) jusqu'à amener le DERNIER trait à l'écran, dans le cadre du rail, entier ;
  B · sans Ma Parole ! : les huit traits payants sont flous (4,8 px), au trait plein (aucun pointillé) ; « 0,50 € » n'est écrit nulle part ;
  C · sans Ma Parole ! : un trait payant touché ne s'applique pas (le pinceau reste), la phrase d'un mur paraît ;
  D · membre : aucun mur ; un trait payant touché s'applique.
Preuve : `--fichier=zz-v162.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
def boite(pg, sel):
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left-D.left)/k, (r.top-D.top)/k, (r.right-D.left)/k, (r.bottom-D.top)/k]; }", sel)
def glisse_rail(pg, rail, dernier):
    r = boite(pg, rail)
    if not r: return None
    y = (r[1] + r[3]) / 2
    # ⚠ les glissés du banc sont des TouchEvent créés en JavaScript : ils ne font défiler AUCUN conteneur (sur aucune version). Le défilement natif se prouve
    #   par la molette horizontale (WebKit la fait défiler comme un doigt, si rien ne la bloque) ; le geste réel se regarde sur l'iPhone.
    ok = pg.evaluate("""s=>{ const e=document.querySelector(s); if(!e) return null; const st=getComputedStyle(e); let ta=[]; for(let q=e; q && q.id!=='device'; q=q.parentElement){ const t=getComputedStyle(q).touchAction; if(t && t!=='auto') ta.push((q.id||q.className)+':'+t); }
        const libre=ta.every(t=>/pan-x|manipulation/.test(t)); const avant=e.scrollLeft; e.scrollLeft=e.scrollWidth; return {ox:st.overflowX, deborde:e.scrollWidth>e.clientWidth+2, touch:ta, libre:libre, defile:e.scrollLeft-avant}; }""", rail)
    pg.wait_for_timeout(300)
    if not ok or ok['ox'] not in ('auto', 'scroll') or not ok['deborde'] or not ok['libre']: return r, None, ok
    d = boite(pg, dernier); return r, d, ok
MURS = "s=>[...document.querySelectorAll(s+' .pc-t')].map(b=>{ const st=getComputedStyle(b); return [b.getAttribute('data-t'), st.filter, st.borderTopStyle, b.classList.contains('pc-mur')]; })"
with sync_playwright() as p:
    b = p.webkit.launch()
    for membre in (False, True):
        T = 'membre' if membre else 'sans Ma Parole !'
        ctx = B.contexte(b); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F)
        if membre: pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }"); pg.wait_for_timeout(400)
        payants = pg.evaluate("()=>(window._PINCEAU_META||[]).filter(m=>!m[1]).map(m=>m[0])")
        # la page +
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
        if not membre:
            M = pg.evaluate(MURS, '#csPinceau')
            okB = M and all((x[0] in payants) == x[3] for x in M) and all(('blur(4.8px)' in x[1]) == x[3] for x in M) and all(x[2] == 'solid' for x in M)
            juge('[%s] B · page + : les huit payants flous (4,8 px), au trait plein ; les quatre libres nets' % T, okB, M)
        g = glisse_rail(pg, '#csPinceau', '#csPinceau .pc-t:last-child')
        okA = g and g[1] and g[1][2] <= min(g[0][2], 390 - 24) + 0.5 and g[1][0] >= max(g[0][0], 0) - 0.5   # la marge de 24 pt au bout
        juge('[%s] A · page + : le rail défile jusqu\'au dernier trait, à l\'écran, entier' % T, okA, g)
        avant = pg.evaluate("()=>window.promiPinceau(null)")
        c = pg.evaluate("p=>{ const b=[...document.querySelectorAll('#csPinceau .pc-t')].find(x=>p.indexOf(x.getAttribute('data-t'))>=0 && x.getBoundingClientRect().left>0 && x.getBoundingClientRect().right<document.getElementById('device').getBoundingClientRect().right); if(!b) return null; const r=b.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k, b.getAttribute('data-t')]; }", payants)
        if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(900)
        apres = pg.evaluate("()=>window.promiPinceau(null)"); phrase = pg.evaluate("()=>{ const m=document.getElementById('murPhrase'); return !!(m && getComputedStyle(m).display!=='none' && m.textContent.trim()); }")
        if membre: juge('[%s] D · page + : un trait payant touché s\'applique' % T, c and apres == c[2], '%s → %s (touché %s)' % (avant, apres, c and c[2]))
        else: juge('[%s] C · page + : un trait payant touché ne s\'applique pas, la phrase du mur paraît' % T, c and apres == avant and phrase, '%s → %s · phrase %s (touché %s)' % (avant, apres, phrase, c and c[2]))
        pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(2500)
        # Peaufiner d'une fiche
        pid = pg.evaluate("()=>promises.find(q=>!q.draft && !q.nuee && q.status!=='tenu').id")
        pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2400); B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
        r = boite(pg, '#dpTraitReg')
        if r: B.tap(pg, r[0] + 40, r[1] + 22); pg.wait_for_timeout(700)
        txt = pg.evaluate("()=>document.getElementById('detailPoster').innerText")
        if not membre: juge('[%s] B · « 0,50 € » n\'est écrit nulle part (Peaufiner)' % T, '0,50' not in txt, [l for l in txt.split('\n') if '0,50' in l][:2])
        g = glisse_rail(pg, '#dpTraitReg .pc-glisse', '#dpTraitReg .pc-t:last-child')
        okA = g and g[1] and g[1][2] <= g[0][2] + 0.5 and g[1][0] >= g[0][0] - 0.5
        juge('[%s] A · Peaufiner : le rail défile jusqu\'au dernier trait, dans le cadre du rail, entier' % T, okA, g)
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
