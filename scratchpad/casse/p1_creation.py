# -*- coding: utf-8 -*-
"""PASSE 1 — je plante un Promi comme un utilisateur : je remplis CHAQUE champ,
   je touche CHAQUE pastille, et je vérifie que la valeur ARRIVE quelque part."""
import sys, json
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

def dump(pg, titre, sel='#createSheet'):
    print('\n──', titre)
    r=pg.evaluate(CHEVAUCHE, sel)
    for s in r['sup']: print('   SUPERPOSE  ', s)
    for d in r['deb']: print('   DEBORDE    ', d)
    for p in pg.evaluate(POINTILLE, sel): print('   POINTILLE  ', p)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)

    print('════════ LA PAGE + · PROMI ════════')
    pg.click('#createBtn'); pg.wait_for_timeout(1200)
    print('après le +  :', pg.evaluate("()=>{const cs=document.getElementById('createSheet');return cs.className;}"))
    # la page des trois natures : je touche la première carte
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0]; if(t)t.click();}")
    pg.wait_for_timeout(1000)
    print('après la carte Promi :', pg.evaluate("()=>document.getElementById('createSheet').className"))
    dump(pg,'PROMI · au repos')

    # ── LE TITRE ──
    print('\n── je remplis LE TITRE ──')
    r=pg.evaluate("""()=>{const e=document.getElementById('fTitle');
      if(!e) return 'ABSENT';
      const c=getComputedStyle(e); const b=e.getBoundingClientRect();
      return {vis:c.display+'/'+c.visibility+'/'+c.opacity, box:[Math.round(b.width),Math.round(b.height)],
              readonly:e.readOnly, disabled:e.disabled, pe:c.pointerEvents};}""")
    print('   #fTitle :', r)
    try:
        pg.fill('#fTitle','aller voir la mer'); pg.wait_for_timeout(600)
        print('   après fill :', pg.evaluate("()=>document.getElementById('fTitle').value"))
        print('   la phrase dit :', pg.evaluate("""()=>{const e=document.querySelector('.pp-phrase');
          return e?(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,80):'PAS DE PHRASE';}"""))
    except Exception as e: print('   fill IMPOSSIBLE :', str(e)[:120])

    # ── LE « À QUI » ──
    print('\n── je remplis « à qui » ──')
    print('   #fWho :', pg.evaluate("""()=>{const e=document.getElementById('fWho');if(!e)return 'ABSENT';
      const c=getComputedStyle(e),b=e.getBoundingClientRect();
      return {vis:c.display+'/'+c.visibility, w:Math.round(b.width), pe:c.pointerEvents, val:e.value};}"""))
    print('   pastilles whoChips :', pg.evaluate("""()=>[...document.querySelectorAll('#whoChips .chip')]
      .map(c=>c.textContent.trim()+(c.classList.contains('on')?'*':''))"""))

    # ── L'ÉCHÉANCE ──
    print('\n── les pastilles d\'échéance ──')
    print('   #dueChips :', pg.evaluate("""()=>[...document.querySelectorAll('#dueChips .chip,#dueChips .is,#dueChips button')]
      .map(c=>c.textContent.trim()+(c.classList.contains('on')?'*':''))"""))

    # ── LA NUÉE ──
    print('   #nueeChips :', pg.evaluate("""()=>[...document.querySelectorAll('#nueeChips .chip')]
      .map(c=>c.textContent.trim()+(c.classList.contains('on')?'*':''))"""))

    print('\n════════ PEAUFINER DE LA PAGE + ════════')
    pg.evaluate("()=>{const b=document.querySelector('#createSheet .cbb-lab,#createSheet #csBotBar');if(b)b.click();}")
    pg.wait_for_timeout(1200)
    print('classe :', pg.evaluate("()=>document.getElementById('createSheet').className"))
    print('les réglages, dans l\'ordre :')
    for l in pg.evaluate("""()=>[...document.querySelectorAll('#createSheet .s2-liste > *')].map(e=>{
      const c=getComputedStyle(e); const b=e.getBoundingClientRect();
      const lab=e.querySelector('.s2-lab,.s2-l'); const val=e.querySelector('.s2-val,.s2-v');
      return (lab?lab.textContent.trim():'?')+'  →  «'+(val?val.textContent.trim():'')+'»'
        +'   h='+Math.round(b.height)+' contour='+c.borderTopStyle+' '+Math.round(parseFloat(c.borderTopWidth))
        +(e.className.includes('cercle')||e.closest('.s2-cercle')?'  [CERCLE]':'  [gratuit]');})"""):
        print('   ', l)
    dump(pg,'PEAUFINER de la page + · superpositions','#createSheet')
    print('\nERREURS JS :', er[:4])
    b.close()
