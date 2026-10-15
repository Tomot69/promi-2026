import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
    E = "()=>{ const e=_aura.etat(), s=document.getElementById('auraScreen'), r=s.getBoundingClientRect(), cs=getComputedStyle(s); return {peints:e.peints, tick:e.frames, show:s.classList.contains('show'), top:Math.round(r.top), vis:cs.visibility, disp:cs.display, op:cs.opacity, tr:cs.transform.slice(0,40)}; }"
    print('avant toute ouverture', pg.evaluate(E))
    B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(3500); a = pg.evaluate(E); print('Aura ouverte      ', a)
    pg.wait_for_timeout(1000); a2 = pg.evaluate(E); print('  +1 s            ', a2['peints'] - a['peints'], 'images peintes')
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(1500); c = pg.evaluate(E); print('après closeAll    ', c)
    pg.wait_for_timeout(2000); c2 = pg.evaluate(E); print('  +2 s sur l\'accueil :', c2['peints'] - c['peints'], 'images de Pelote peintes alors qu\'on ne la voit pas')
    b.close()
