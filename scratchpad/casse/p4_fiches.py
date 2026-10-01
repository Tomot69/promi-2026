# -*- coding: utf-8 -*-
"""PASSE 4 — les fiches, une par une, ETAT PROPRE entre chaque. Et Peaufiner."""
import sys, os
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright
OUT=R+'/scratchpad/casse/shots2'; os.makedirs(OUT,exist_ok=True)

FICHE = r"""()=>{
  const dp=document.getElementById('detailPoster');
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const b=e=>{if(!e)return '—';const r=e.getBoundingClientRect();
    return Math.round((r.left-dev.left)/sc)+','+Math.round((r.top-dev.top)/sc)+' '
          +Math.round(r.width/sc)+'x'+Math.round(r.height/sc);};
  const vu=e=>{if(!e)return false;const c=getComputedStyle(e);
    return c.display!=='none'&&c.visibility!=='hidden'&&parseFloat(c.opacity)>0.05;};
  const cv=document.getElementById('dpTrameCv');
  let peint=0;
  try{const g=cv.getContext('2d');const d=g.getImageData(0,0,cv.width,Math.min(cv.height,400)).data;
    for(let i=3;i<d.length;i+=400) if(d[i]>10) peint++;}catch(e){}
  return {cls:dp.className, peauf:dp.classList.contains('dpd-ouv')||!!dp.querySelector('.dpd-corps.ouv'),
    trame:b(cv)+' pixels='+peint,
    marque:(document.getElementById('dptNat')||{textContent:'—'}).textContent.trim(),
    marqueVu:vu(document.getElementById('dptNat')),
    qui:(document.getElementById('dptQui')||{textContent:'—'}).textContent.trim(),
    titre:(document.getElementById('dptTitre')||{textContent:'—'}).textContent.trim(),
    quand:(document.getElementById('dptQuand')||{textContent:'—'}).textContent.trim(),
    trace:(document.getElementById('dptTrace')||{textContent:'—'}).textContent.trim(),
    traceVu:vu(document.getElementById('dptTrace')),
    geste:vu(dp.querySelector('.geste-env'))+' '+b(dp.querySelector('.geste-env')),
    barre:b(document.getElementById('dpDetails')),
  };}"""
REGLAGES = r"""()=>[...document.querySelectorAll('#detailPoster .s2-liste > *, #detailPoster .dpd-corps > *')]
  .filter(e=>{const c=getComputedStyle(e);return c.display!=='none'&&e.getBoundingClientRect().height>6;})
  .map(e=>{const c=getComputedStyle(e);const r=e.getBoundingClientRect();
    const dev=document.getElementById('device').getBoundingClientRect();const sc=dev.width/390;
    const lab=e.querySelector('.s2-lab,.s2-l,label');const val=e.querySelector('.s2-val,.s2-v');
    const flou=/blur/.test(c.filter)|| !!e.closest('[style*=blur]') || /blur/.test(getComputedStyle(e.parentElement||e).filter);
    return (lab?lab.textContent.trim():(e.className+'').slice(0,22))
      +' → «'+(val?val.textContent.trim():'')+'»'
      +'  @'+Math.round((r.top-dev.top)/sc)+' h='+Math.round(r.height/sc)
      +' contour='+c.borderTopStyle+(flou?'  [FLOUTÉ/CERCLE]':'');})"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)
    ids=pg.evaluate("""()=>({promi:(promises.filter(p=>!p.draft&&!p.req&&!p.chiche&&p.status==='encours')[0]||{}).id,
      atenir:(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0]||{}).id,
      tenu:(promises.filter(p=>!p.draft&&p.status==='tenu')[0]||{}).id,
      chiche:(promises.filter(p=>p.chiche)[0]||{}).id})""")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(400)
        for k,v in ids.items():
            if v is None: continue
            # ÉTAT PROPRE : on ferme tout, on referme Peaufiner
            pg.evaluate("""()=>{if(window.closeAll)closeAll();
              const dp=document.getElementById('detailPoster');
              if(dp){dp.classList.remove('dpd-ouv');const c=dp.querySelector('.dpd-corps');if(c)c.classList.remove('ouv');}}""")
            pg.wait_for_timeout(500)
            pg.evaluate("(i)=>openDetail(i)",v); pg.wait_for_timeout(1500)
            print('\n═══ FICHE %s [%s] ═══'%(k,th))
            f=pg.evaluate(FICHE)
            for kk in ('cls','peauf','trame','marque','marqueVu','qui','titre','quand','trace','traceVu','geste','barre'):
                print('   %-9s %s'%(kk, f[kk]))
            r=pg.evaluate(CHEVAUCHE,'#detailPoster')
            for s in r['sup'][:8]: print('   SUPERPOSE  ',s)
            for d in r['deb'][:5]: print('   DEBORDE    ',d)
            for q in pg.evaluate(POINTILLE,'#detailPoster')[:6]: print('   POINTILLE  ',q)
            pg.query_selector('#device').screenshot(path=OUT+'/fiche_%s_%s.png'%(k,th))
            if th=='dark':
                pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog');if(t)t.click();}")
                pg.wait_for_timeout(1300)
                print('   ── Peaufiner ouvert ──')
                for l in pg.evaluate(REGLAGES): print('      ',l)
                r2=pg.evaluate(CHEVAUCHE,'#detailPoster')
                for s in r2['sup'][:8]: print('      SUPERPOSE  ',s)
                for d in r2['deb'][:5]: print('      DEBORDE    ',d)
                pg.query_selector('#device').screenshot(path=OUT+'/peauf_%s_%s.png'%(k,th))
    print('\nERREURS JS :', er[:5])
    b.close()
