# -*- coding: utf-8 -*-
"""BALAYAGE COMPLET DES ÉLÉMENTS D'ÉTAT — quinze écrans, deux thèmes.
   Les trois seules valeurs admises (Tom, 22 sept.) : #DD4D23 · #291547 · #00341A.
   On lit le RENDU, jamais la feuille (§8 : on trie les surfaces, pas les règles)."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
NEUF = {'#DD4D23','#291547','#00341A'}
ANCIENS = {'#2BE88C':'menthe','#8FA0FF':'périwinkle','#F07A2E':"orange d'origine",'#FFD447':'jaune',
           '#33BA6C':'vert clair (retiré)','#A77CF7':'violet clair (retiré)','#8FE08F':'amande (célébration seule)'}
ECRANS = [
 ('accueil',      "()=>{closeAll();}"),
 ('aura',         "()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
 ("aide de l'Aura","()=>{closeAll(); document.getElementById('souffleBtn').click(); setTimeout(()=>{const b=document.getElementById('auraInfoBtn'); b&&b.click();},900);}"),
 ('index',        "()=>{closeAll(); document.getElementById('indexBtn').click();}"),
 ('fil',          "()=>{closeAll(); document.getElementById('filBtn').click();}"),
 ('fiche',        "()=>{closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee&&p.status!=='tenu')[0].id);}"),
 ('fiche tenue',  "()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"),
 ('Peaufiner',    "()=>{closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee)[0].id); setTimeout(()=>{const b=document.getElementById('dpBarre')||document.querySelector('#detailPoster .dp-barre'); b&&b.click();},700);}"),
 ('fiche de Nuée',"()=>{closeAll(); const k=Object.keys(NUE||{})[0]; if(k) window.openNueeDetail(k);}"),
 ('page +',       "()=>{closeAll(); document.getElementById('createBtn').click();}"),
 ('partage',      "()=>{closeAll(); const b=document.getElementById('shareBtn')||document.querySelector('[data-open=share]'); if(b) b.click(); else if(window.openShare) openShare();}"),
 ('Studio',       "()=>{closeAll(); document.getElementById('studioBtn').click();}"),
 ('Réglages',     "()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}"),
 ('fiche personne',"()=>{closeAll(); try{openPerson('Adrien');}catch(e){}}"),
]
SCAN = r"""()=>{
  const out=[], vu=new Set();
  const hex=(c)=>{const m=/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/.exec(c||''); if(!m) return null;
    if(m[4]!==undefined && +m[4]===0) return null;
    return '#'+[1,2,3].map(i=>(+m[i]).toString(16).padStart(2,'0')).join('').toUpperCase();};
  const nom=(e)=>{let p=e,s=[];for(let i=0;i<3&&p;i++,p=p.parentElement){const cn=(p.className&&typeof p.className==='string')?p.className:(p.className&&p.className.baseVal)||'';
      s.unshift((p.tagName||'').toLowerCase()+(p.id?'#'+p.id:'')+(cn?'.'+cn.trim().split(/\s+/).slice(0,2).join('.'):''));}
    return s.join(' ');};
  const dv=document.getElementById('device'); if(!dv) return out;
  const dr=dv.getBoundingClientRect();
  dv.querySelectorAll('*').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
    if(r.bottom<dr.top-4||r.top>dr.bottom+4) return;     /* hors de l'appareil : pas à l'écran */
    const cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0) return;
    [['fond',cs.backgroundColor],['texte',cs.color],['contour',cs.borderTopColor],
     ['trait',e.getAttribute&&e.getAttribute('stroke')],['fill',e.getAttribute&&e.getAttribute('fill')]].forEach(([q,v])=>{
      let h = (v && v[0]==='#') ? v.toUpperCase() : hex(v);
      if(!h) return;
      const k=nom(e)+'|'+q+'|'+h; if(vu.has(k)) return; vu.add(k);
      out.push({n:nom(e), q:q, c:h, t:(e.textContent||'').trim().slice(0,22)});});
  });
  return out; }"""
reste=[]; justes=0
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        for nom, js in ECRANS:
            try: pg.evaluate(js)
            except Exception as e: print('   (%s : %s)' % (nom, str(e)[:60])); continue
            pg.wait_for_timeout(1800)
            for o in pg.evaluate(SCAN):
                if o['c'] in NEUF: justes+=1
                elif o['c'] in ANCIENS: reste.append((th,nom,o['n'],o['q'],o['c'],o['t']))
    b.close()
print('\n%d surfaces portent une des TROIS valeurs décidées.' % justes)
print('%d portent encore une ancienne valeur d\'état :' % len(reste))
for th,ec,n,q,c,t in reste:
    print('   [%s] %-16s %-40s %-7s %s  « %s »' % (th, ec, n[-40:], q, ANCIENS[c]+' '+c, t))
