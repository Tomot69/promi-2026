# Les captures finales de la fiche d'une personne, dans l'app intégrée — à REGARDER une par une (Tom).
# Deux thèmes · Rachel (plein, ouverte AU DOIGT depuis la rangée de l'Aura, à l'ouverture puis défilée jusqu'au bout) ·
# Nico (vide) · et la page + ouverte par « + Lancer un Chiche », la personne déjà choisie.
import os
from playwright.sync_api import sync_playwright
O = 'sauvegardes/audit-fiche-personne/apres/'; os.makedirs(O, exist_ok=True)
def aura_tap(pg, nom):
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(250)
    pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(600)
    pt = pg.evaluate("""(n)=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()===n); const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
        for(const x of document.querySelectorAll('#auraScreen .au-nb')){ const r=x.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""", nom)
    pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1800)
def shot(pg, nom):
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    pg.screenshot(path=O + nom + '.png', clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]}); print('   ', O + nom + '.png')
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        aura_tap(pg, 'Rachel'); shot(pg, 'final-%s-rachel-ouverture' % th)
        pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); if(c) c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(500); shot(pg, 'final-%s-rachel-defilee' % th)
        pg.evaluate("()=>openPerson('Nico')"); pg.wait_for_timeout(1400); shot(pg, 'final-%s-nico-vide' % th)
        if th == 'dark':
            aura_tap(pg, 'Rachel')
            pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); if(c) c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(400)
            bx = pg.evaluate("()=>{ const e=document.querySelector('#psCadre .ps-bt[data-geste=chiche]'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
            pg.mouse.click(bx[0], bx[1]); pg.wait_for_timeout(1600); shot(pg, 'final-dark-page-plus-chiche-rachel')
        pg.close()
    b.close()
