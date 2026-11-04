#!/usr/bin/env python3
"""redteam_nature_plus.py — v177 (Tom, C-224, C-223). LA PAGE + LIT SA NATURE SUR `data-kind`.
A · C-224 : un Cercle ouvert puis fermé par son X, puis un Promi, puis un Chiche : le trait plante à chaque fois, la bonne nature, et un Cercle ensuite plante un Cercle. Au doigt (banc comme Tom, WebKit).
B · C-223 : sur la page + d'un Cercle, le premier toucher du trait (dans SA zone, `#planterZoneN`) arrête le clignotement du départ, comme pour un Promi et un Chiche.
Rouge sur v176 (`--fichier=zz-v176.html`) : A (rien n'est planté), B Cercle."""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html'); res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-84s %s' % ('✅' if ok else '❌', n, str(d)[:190]), flush=True)
SL = {'promi': '#csPhrase .ph-m[data-ph="titre"]', 'chiche': '#csPhrase .ph-m[data-ph="titre"]', 'nuee': '#nueePhrase .ph-m[data-np="nom"]'}
def ouvre(pg, nat):
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2800)
def saisit(pg, nat, t):
    for _ in range(6):
        B.tap_sel(pg, SL[nat]); pg.wait_for_timeout(1000)
        if pg.evaluate("()=>{const a=document.activeElement;return !!a&&(a.id==='phIn'||a.id==='nueeNomIn');}"): break
    pg.keyboard.type(t, delay=50); pg.wait_for_timeout(1500)
def trace(pg):
    y = pg.evaluate("()=>{const e=_ppEcran(),O=_onde,f=O.onde(e.base,e.amp);return [...Array(15)].map((_,i)=>[30+i*12,f(30+i*12)])}"); B.glisse(pg, y, tenue=380); pg.wait_for_timeout(4500)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_nature_plus — %s, charge %.1f' % (F, B.charge()))
    ctx = B.contexte(b, False, vw=390, vh=844); pg = B.ouvre(ctx, F)
    ouvre(pg, 'nuee'); saisit(pg, 'nuee', 'x'); pg.keyboard.press('Enter'); pg.wait_for_timeout(1000); B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1500)
    for nat, t in (('promi', 'nager'), ('chiche', 'sauter')):
        ouvre(pg, nat); saisit(pg, nat, t); trace(pg); r = pg.evaluate("t=>{const p=promises.find(q=>q.title===t);return {la:!!p,chiche:!!(p&&p.chiche),ouverte:document.getElementById('createSheet').classList.contains('show'),titres:promises.map(q=>q.title),trait:window._traitDernier};}", t)
        juge('A · après un Cercle fermé, le trait d\'un %s plante' % nat, r['la'] and r['chiche'] == (nat == 'chiche') and not r['ouverte'], r)
    ouvre(pg, 'nuee'); saisit(pg, 'nuee', 'Les voisins'); trace(pg); r = pg.evaluate("()=>Object.values(NUE)")
    juge('A · puis le trait d\'un Cercle plante un Cercle', 'Les voisins' in r, r)
    ctx.close()
    for nat, z in (('promi', 'planterZone'), ('chiche', 'planterZone'), ('nuee', 'planterZoneN')):
        ctx = B.contexte(b, False, vw=390, vh=844); pg = B.ouvre(ctx, F); ouvre(pg, nat); saisit(pg, nat, 'nager'); pg.keyboard.press('Enter'); pg.wait_for_timeout(2800)   # v178b (C-229) : le trait ne naît qu'à la validation
        c0 = pg.evaluate("()=>{const d=document.getElementById('ppDepart');return !!d&&d.classList.contains('clignote');}")
        pg.evaluate("z=>{const c=document.getElementById(z).querySelector('canvas'),r=c.getBoundingClientRect();const o={bubbles:true,clientX:r.left+r.width*0.8,clientY:r.top+r.height/2,pointerType:'touch',isPrimary:true};c.dispatchEvent(new PointerEvent('pointerdown',o));c.dispatchEvent(new PointerEvent('pointerup',o));}", z); pg.wait_for_timeout(500)
        c1 = pg.evaluate("()=>{const d=document.getElementById('ppDepart');return !!d&&d.classList.contains('clignote');}")
        juge('B · %s : le premier toucher du trait arrête le clignotement' % nat, c0 and not c1, '%s → %s' % (c0, c1)); ctx.close()
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
