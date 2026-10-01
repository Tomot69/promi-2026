# -*- coding: utf-8 -*-
"""PASSE 5 — les MOTS : ce que l'app écrit, et le bloc du Cercle."""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

TEXTES = r"""(sel)=>{
  const h=document.querySelector(sel); if(!h) return ['HÔTE ABSENT'];
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const out=[];
  [...h.querySelectorAll('*')].forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim().replace(/\s+/g,' '); if(!t) return;
    const r=e.getBoundingClientRect();
    out.push(Math.round((r.top-dev.top)/sc)+'  «'+t.slice(0,72)+'»');
  });
  return [...new Set(out)];}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)
    cid=pg.evaluate("()=>(promises.filter(p=>p.chiche)[0]||{}).id")

    print('═══ TOUS LES MOTS D\'UNE FICHE CHICHE (Peaufiner fermé) ═══')
    pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}",cid); pg.wait_for_timeout(1600)
    for l in pg.evaluate(TEXTES,'#detailPoster'): print('  ',l)

    print('\n═══ LE MÊME CHICHE, PEAUFINER OUVERT ═══')
    pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog');if(t)t.click();}")
    pg.wait_for_timeout(1400)
    for l in pg.evaluate(TEXTES,'#detailPoster'): print('  ',l)

    print('\n═══ LE BLOC DU CERCLE (§3.8) : quatre réglages floutés + encart ═══')
    print(pg.evaluate("""()=>{const d=document.getElementById('detailPoster');
      const f=[...d.querySelectorAll('*')].filter(e=>/blur/.test(getComputedStyle(e).filter));
      const enc=[...d.querySelectorAll('*')].filter(e=>/Cercle/.test(e.textContent||'')
        && (e.textContent||'').trim().length<60);
      return {flous:f.map(e=>(e.id?'#'+e.id:'.'+(e.className+'').split(' ')[0])+' '+getComputedStyle(e).filter),
              encart:enc.map(e=>(e.className+'').slice(0,30)+' «'+(e.textContent||'').trim().slice(0,40)+'»'),
              premium:(typeof isPremium!=='undefined')?isPremium:'?'};}"""))

    print('\n═══ PEAUFINER GÉNÉRAL (les réglages hors fiche) ═══')
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const s=document.getElementById('settingsBtn');if(s)s.click();}"); pg.wait_for_timeout(1400)
    for l in pg.evaluate(TEXTES,'#settingsScreen')[:45]: print('  ',l)
    print('  superpositions :')
    r=pg.evaluate(CHEVAUCHE,'#settingsScreen')
    for s in r['sup'][:10]: print('    ',s)
    for d in r['deb'][:6]: print('     DEBORDE ',d)
    print('\nERREURS JS :', er[:5])
    b.close()
