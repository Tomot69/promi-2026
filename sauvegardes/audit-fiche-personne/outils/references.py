import json, sys
from playwright.sync_api import sync_playwright
O='sauvegardes/audit-fiche-personne/references/'
RANGEE = r"""()=>{ const n=document.querySelector('#auraScreen .au-n'); if(!n) return null;
  const q=(s)=>{const e=n.querySelector(s); if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return {w:Math.round(r.width), h:Math.round(r.height), bg:c.backgroundImage.slice(0,50), rad:c.borderRadius}; };
  return JSON.stringify({html:n.innerHTML.slice(0,500), nb:q('.au-nb'), lb:q('.au-lb')}); }"""
MOISSON = r"""()=>{ const h=document.querySelector('#auraScreen .au-mo h3'); const c=document.querySelector('#auraScreen .au-c');
  if(!h||!c) return null; const s=getComputedStyle(h), r=c.getBoundingClientRect(), sp=c.querySelector('span'), ss=sp?getComputedStyle(sp):null;
  return JSON.stringify({h3:h.textContent, h3f:s.fontFamily.split(',')[0]+' '+s.fontWeight+' '+s.fontSize+' ls '+s.letterSpacing+' op '+s.opacity, cell:[Math.round(r.width),Math.round(r.height)], lab:ss?ss.fontFamily.split(',')[0]+' '+ss.fontWeight+' '+ss.fontSize:null}); }"""
CARTE = r"""()=>{ const c=document.querySelector('#indexSheet .s4-carte'); if(!c) return null; const r=c.getBoundingClientRect();
  return JSON.stringify({n:document.querySelectorAll('#indexSheet .s4-carte').length, box:[Math.round(r.width),Math.round(r.height)], etat:c.getAttribute('data-etat'), nat:c.getAttribute('data-nat'), html:c.innerHTML.slice(0,600)}); }"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    d=pg.evaluate("""()=>{ const L=promises.filter(p=>!p.draft); const par={};
      ['Rachel','Marion','Adrien'].forEach(n=>{ const it=L.filter(p=>p.who===n||p.from===n||p.avec===n); par[n]={total:it.length, tenus:it.filter(p=>p.status==='tenu').map(p=>p.title+(p.chiche?' [Chiche]':''))}; }); return par; }""")
    print('par personne :', json.dumps(d, ensure_ascii=False))
    dev=lambda: pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(1200); v=dev()
        pg.screenshot(path=O+'aura-%s.png'%th, clip={'x':v[0],'y':v[1],'width':v[2],'height':v[3]})
        if th=='dark': print('rangée :', pg.evaluate(RANGEE)); print('moisson :', pg.evaluate(MOISSON))
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();else document.getElementById('indexSheet').classList.add('show');}"); pg.wait_for_timeout(1800); v=dev()
        pg.screenshot(path=O+'index-%s.png'%th, clip={'x':v[0],'y':v[1],'width':v[2],'height':v[3]})
        if th=='dark': print('carte :', pg.evaluate(CARTE))
    pg.close()
    pg=b.new_page(viewport={'width':1340,'height':1000})
    pg.goto('http://127.0.0.1:8752/PLANCHE-FICHE-PERSONNE-2.html'); pg.wait_for_timeout(2500)
    print('planche, titre du plateau :', pg.evaluate("""()=>{ const t=document.querySelector('.plat .t'); const c=getComputedStyle(t);
       return JSON.stringify({ff:c.fontFamily, fw:c.fontWeight, ok:document.fonts.check('700 27px Bricolage'), faces:[...document.fonts].filter(f=>/Bricolage|Fraunces/.test(f.family)).map(f=>f.family+' '+f.weight+' '+f.status)}); }"""))
    b.close()
