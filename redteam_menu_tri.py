#!/usr/bin/env python3
"""redteam_menu_tri.py — ⚑ v163 (Tom, Q578) : UN TOUCHER HORS DU MENU DE TRI LE REFERME, DANS L'INDEX COMME DANS LE FIL.

Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles. Pour l'Index et le Fil :
  A · ⇅ ouvre le menu ; un toucher SOUS le panneau le referme, et rien ne s'ouvre dessous ;
  B · un toucher au-dessus du panneau (sur le plateau) le referme aussi, rien ne s'ouvre ;
  C · un toucher DANS le panneau, hors d'une option, ne le referme pas ;
  D · une option touchée agit toujours (et referme le menu).
Preuve : `--fichier=zz-v162.html` rougit (l'Index ne se referme pas).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
OUVERT = "s=>{ const m=document.querySelector(s); return !!(m && m.classList.contains('on')); }"
AUTRE = "()=>['detailPoster','createSheet','studioScreen','auraScreen','settingsScreen'].filter(i=>{ const e=document.getElementById(i); return e && e.classList.contains('show'); })"
with sync_playwright() as p:
    b = p.webkit.launch()
    for nom, porte, btn, menu in (('Index', '#indexBtn', '#ixTriBtn', '#ixMenu'), ('Fil', '#filBtn', '#fdTriBtn', '#fdMenu')):
        ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
        B.tap_sel(pg, porte); pg.wait_for_timeout(2500)
        pn = None
        for etape, y in (('A', None), ('B', 60), ('C', 'dedans')):
            B.tap_sel(pg, btn); pg.wait_for_timeout(700); o1 = pg.evaluate(OUVERT, menu)
            pn = pg.evaluate("s=>{ const p=document.querySelector(s+' .ix-menu-p'); const r=p.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.top-D.top)/k, (r.bottom-D.top)/k, (r.left-D.left)/k]; }", menu)
            if etape == 'A': B.tap(pg, 195, min(800, pn[1] + 50))
            elif etape == 'B': B.tap(pg, 200, 60)
            else:
                pt = pg.evaluate("s=>{ const p=document.querySelector(s+' .ix-menu-p'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=p.getBoundingClientRect(); for(let y=r.top+4; y<r.bottom; y+=3){ const e=document.elementFromPoint(r.left+8*k, y); if(e && !e.closest('.ix-mi') && e.closest('.ix-menu-p')) return [(r.left-D.left)/k+8, (y-D.top)/k]; } return null; }", menu)
                if pt: B.tap(pg, pt[0], pt[1])
            pg.wait_for_timeout(700); o2 = pg.evaluate(OUVERT, menu); au = pg.evaluate(AUTRE)
            if etape == 'C':
                juge('[%s] C · un toucher dans le panneau, hors d\'une option, ne le referme pas' % nom, o1 and o2, 'ouvert %s → %s · point %s' % (o1, o2, pt))
                pg.evaluate("s=>{ document.querySelector(s).classList.remove('on'); }", menu)
            else:
                juge('[%s] %s · un toucher %s du panneau le referme, rien ne s\'ouvre dessous' % (nom, etape, 'sous le' if etape == 'A' else 'au-dessus'), o1 and not o2 and not au, 'ouvert %s → %s · écrans %s' % (o1, o2, au))
        B.tap_sel(pg, btn); pg.wait_for_timeout(700)
        it = pg.evaluate("s=>{ const L=[...document.querySelectorAll(s+' .ix-mi')].filter(e=>e.getBoundingClientRect().height>0 && !e.classList.contains('on')); const e=L[0]; if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k, e.textContent.trim()]; }", menu)
        if it: B.tap(pg, it[0], it[1]); pg.wait_for_timeout(800)
        on = pg.evaluate("s=>[...document.querySelectorAll(s+' .ix-mi.on')].map(e=>e.textContent.trim())", menu)
        juge('[%s] D · une option touchée agit et referme le menu' % nom, it and not pg.evaluate(OUVERT, menu) and any(it[2] in x for x in on), 'option %s · choisies %s' % (it and it[2], on))
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % nom, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
