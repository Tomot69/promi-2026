# -*- coding: utf-8 -*-
"""PASSE 6 — la page + Chiche et Nuée, l'Index, le Fil, les Réglages. Je TOUCHE."""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

TEXTES = r"""(sel)=>{const h=document.querySelector(sel); if(!h) return ['HÔTE ABSENT'];
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const out=[];
  [...h.querySelectorAll('*')].forEach(e=>{const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim().replace(/\s+/g,' '); if(!t) return;
    const r=e.getBoundingClientRect(); const y=Math.round((r.top-dev.top)/sc);
    if(y<-20||y>860) return;
    out.push(y+'  «'+t.slice(0,64)+'»');});
  return [...new Set(out)];}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)

    for i,nat in ((1,'CHICHE'),(2,'NUÉE')):
        print('\n═══ PAGE + · %s ═══'%nat)
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
        pg.click('#createBtn'); pg.wait_for_timeout(900)
        pg.evaluate("(i)=>{const t=[...document.querySelectorAll('#createSheet .tile')][i];if(t)t.click();}",i)
        pg.wait_for_timeout(1200)
        for l in pg.evaluate(TEXTES,'#createSheet'): print('  ',l)
        r=pg.evaluate(CHEVAUCHE,'#createSheet')
        for s in r['sup'][:8]: print('   SUPERPOSE  ',s)
        for d in r['deb'][:5]: print('   DEBORDE    ',d)
        for q in pg.evaluate(POINTILLE,'#createSheet')[:6]: print('   POINTILLE  ',q)
        print('   pastilles atteignables :', pg.evaluate("""()=>[...document.querySelectorAll('#createSheet .chip,#createSheet .is')]
          .filter(e=>e.getBoundingClientRect().width>4).map(e=>e.textContent.trim()).slice(0,14)"""))

    print('\n═══ L\'INDEX · je cherche et je trie ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"); pg.wait_for_timeout(1600)
    n0=pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte').length")
    pg.evaluate("""()=>{const e=document.getElementById('ixSearch');e.focus();e.value='crêpes';
      e.dispatchEvent(new Event('input',{bubbles:true}));}"""); pg.wait_for_timeout(1200)
    n1=pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte').length")
    print('   cartes avant recherche : %d · après « crêpes » : %d'%(n0,n1))
    pg.evaluate("""()=>{const e=document.getElementById('ixSearch');e.value='';
      e.dispatchEvent(new Event('input',{bubbles:true}));}"""); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=document.getElementById('ixTriBtn');if(t)t.click();}"); pg.wait_for_timeout(1000)
    print('   après le bouton de tri :', pg.evaluate("""()=>{const m=document.getElementById('ixMenu')||document.getElementById('ixSort');
      if(!m) return 'AUCUN MENU';const c=getComputedStyle(m);const r=m.getBoundingClientRect();
      const dev=document.getElementById('device').getBoundingClientRect();const sc=dev.width/390;
      return c.display+' @'+Math.round((r.left-dev.left)/sc)+','+Math.round((r.top-dev.top)/sc)
        +' '+Math.round(r.width/sc)+'x'+Math.round(r.height/sc);}"""))
    r=pg.evaluate(CHEVAUCHE,'#indexSheet')
    for s in r['sup'][:6]: print('   SUPERPOSE  ',s)
    for d in r['deb'][:5]: print('   DEBORDE    ',d)
    print('   je touche une carte :', pg.evaluate("""()=>{const c=document.querySelector('#indexList .s4-carte');
      if(!c) return 'AUCUNE CARTE'; c.click(); return 'cliqué';}"""))
    pg.wait_for_timeout(1400)
    print('   la fiche s\'ouvre ?', pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))

    print('\n═══ LE FIL ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1600)
    print('   je touche un bandeau :', pg.evaluate("""()=>{const c=document.querySelector('#feedList .s4-carte');
      if(!c) return 'AUCUN BANDEAU'; c.click(); return 'cliqué';}"""))
    pg.wait_for_timeout(1500)
    print('   la fiche s\'ouvre ?', pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
    print('   TENIR / REPORTER encore là ?', pg.evaluate("""()=>[...document.querySelectorAll('#feedList .fd-acc,#feedList .fd-dec')]
      .filter(e=>e.getBoundingClientRect().width>3).length"""))

    print('\n═══ LES RÉGLAGES GÉNÉRAUX ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{const s=document.getElementById('settingsBtn');if(s)s.click();}"); pg.wait_for_timeout(1500)
    for l in pg.evaluate(TEXTES,'#settingsScreen')[:40]: print('  ',l)
    r=pg.evaluate(CHEVAUCHE,'#settingsScreen')
    for s in r['sup'][:8]: print('   SUPERPOSE  ',s)
    for d in r['deb'][:5]: print('   DEBORDE    ',d)
    print('\nERREURS JS :', er[:5])
    b.close()
