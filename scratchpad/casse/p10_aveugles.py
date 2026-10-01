# -*- coding: utf-8 -*-
"""PASSE 10 — les trois zones aveugles + les pastilles de Peaufiner."""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)

    print('═══ LES PASTILLES DE PEAUFINER — atteignables ? ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}")
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1400)
    print(pg.evaluate("""()=>{const out=[];
      document.querySelectorAll('#detailPoster .s2-reg .chip,#detailPoster .s2-reg .is,#detailPoster .s2-reg button')
        .forEach(e=>{const c=getComputedStyle(e);const r=e.getBoundingClientRect();
          out.push((e.textContent||'').trim().slice(0,12)+' '+Math.round(r.width)+'×'+Math.round(r.height)
            +' '+c.display+'/'+c.visibility+'/pe:'+c.pointerEvents);});
      return out.slice(0,10);}"""))

    print('\n═══ ZONE 1 · LE CERCLE PAYANT (isPremium forcé) ═══')
    pg.evaluate("()=>{try{if(typeof setPremium==='function')setPremium(true);else window.isPremium=true;}catch(e){}}")
    pg.wait_for_timeout(600)
    pg.evaluate("()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}")
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1400)
    print('  isPremium :', pg.evaluate("()=>(typeof isPremium!=='undefined')?isPremium:'?'"))
    print(pg.evaluate("""()=>{const out=[];
      document.querySelectorAll('#detailPoster .s2-cercle .s2-reg,#detailPoster .s2-encart').forEach(e=>{
        const c=getComputedStyle(e);
        out.push((e.className||'').slice(0,14)+' «'+(e.textContent||'').trim().slice(0,26)+'» flou='+c.filter
          +' pe:'+c.pointerEvents);});
      return out;}"""))
    r=pg.evaluate(CHEVAUCHE,'#detailPoster')
    for s in r['sup'][:5]: print('  SUPERPOSE ',s)

    print('\n═══ ZONE 2 · UN BROUILLON (gardé de côté) ═══')
    did=pg.evaluate("""()=>{const p=promises.filter(x=>!x.req)[0];
      const n=JSON.parse(JSON.stringify(p)); n.id=990002; n.draft=true; n.title='l’atelier du samedi';
      n.status='encours'; promises.push(n);
      try{if(typeof relayout==='function')relayout();}catch(e){} return n.id;}""")
    pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}",did); pg.wait_for_timeout(1600)
    print('  fiche :', pg.evaluate("""()=>{const d=document.getElementById('detailPoster');
      return {cls:d.className.slice(0,60),
        marque:(document.getElementById('dptNat')||{}).textContent,
        etat:(document.getElementById('dptQuand')||{}).textContent,
        trace:(document.getElementById('dptTrace')||{}).textContent};}"""))
    r=pg.evaluate(CHEVAUCHE,'#detailPoster')
    for s in r['sup'][:5]: print('  SUPERPOSE ',s)
    for d in r['deb'][:3]: print('  DEBORDE   ',d)
    for q in pg.evaluate(POINTILLE,'#detailPoster')[:4]: print('  POINTILLE ',q)
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"); pg.wait_for_timeout(1700)
    print('  dans l\'Index :', pg.evaluate("""()=>{const c=[...document.querySelectorAll('#indexList .s4-carte')]
      .filter(x=>/atelier/.test(x.textContent||''))[0];
      return c?{etat:c.getAttribute('data-etat'),mot:(c.querySelector('.s4-et')||{}).textContent,
        contour:getComputedStyle(c).outlineStyle}:'ABSENTE DE L\\'INDEX';}"""))

    print('\n═══ ZONE 3 · LA NUÉE EN PROFONDEUR ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();const k=Object.keys(NUE)[0];if(k)openEssaim(k);}")
    pg.wait_for_timeout(1800)
    print('  écran :', pg.evaluate("""()=>{const e=document.getElementById('essaimSheet')||document.getElementById('detailPoster');
      return e?e.id+' '+(e.className||'').slice(0,50):'?';}"""))
    for sel in ('#essaimSheet','#detailPoster'):
        r=pg.evaluate(CHEVAUCHE,sel)
        if r['n']:
            print('  %s : %d feuilles · %d superpositions · %d débordements'%(sel,r['n'],len(r['sup']),len(r['deb'])))
            for s in r['sup'][:5]: print('     SUPERPOSE ',s)
            for d in r['deb'][:3]: print('     DEBORDE   ',d)
    print('\nERREURS JS :', er[:4])
    b.close()
