# L'ÉCRAN QUI VEND, bas de la planche — première sonde : ce que l'app a composé, les cotes, les dalles peintes, deux thèmes.
import json, os
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vend'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
J = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390; const ps=document.getElementById('plusScreen');
  const R=(e)=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [+((r.left-dv.left)/s).toFixed(1), +((r.top-dv.top)/s).toFixed(1), +(r.width/s).toFixed(1), +(r.height/s).toFixed(1)]; };
  const alpha=(c)=>{ const g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data; let n=0, t=0; for(let i=3;i<d.length;i+=4){ t++; if(d[i]>10) n++; } return +(100*n/t).toFixed(1); };
  return {dalles: window._vendDalles, canevas:[...document.querySelectorAll('#plCadre .plv-dal')].map(c=>({monde:c.dataset.monde, r:R(c), peint:alpha(c)})),
    noms:[...document.querySelectorAll('#plCadre .plv-nom')].map(e=>[e.textContent, R(e)]), prix:[document.querySelector('#plCadre .plv-prix').textContent, R(document.querySelector('#plCadre .plv-prix'))],
    sous:[document.querySelector('#plCadre .plv-sous').textContent, R(document.querySelector('#plCadre .plv-sous'))],
    annee:[document.getElementById('buyYear').textContent.trim(), R(document.getElementById('buyYear'))], essai:[document.getElementById('buyMonth').textContent.trim(), R(document.getElementById('buyMonth'))],
    notes:[...document.querySelectorAll('#plCadre .pl-note')].map(e=>[e.textContent.trim().slice(0,30), R(e), getComputedStyle(e).opacity]),
    anciens:['#plHeroCv','.pl-h','.pl-sub','.pl-feat'].map(q=>[q, [...ps.querySelectorAll(q)].some(e=>e.checkVisibility())]),
    defile: ps.scrollHeight - ps.clientHeight, plateau:R(ps.querySelector('.enh')), dessus:ps.classList.contains('cercle-dessus')}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        err = []; pg.on('pageerror', lambda e: err.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('cercleTopBtn').click()"); pg.wait_for_timeout(1500)
        R[th + ' · accueil'] = pg.evaluate(J)
        clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
        pg.screenshot(path=os.path.join(OUT, 'planche_%s_accueil.png' % th), clip=clip)
        # par-dessus, depuis le mur d'une fiche
        pg.evaluate(BASE); pg.wait_for_timeout(200)
        pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1400)
        pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
        pg.evaluate("()=>{ const e=document.querySelector('#detailPoster .s2-encart'); e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(300)
        r = pg.evaluate("()=>{ const e=document.querySelector('#detailPoster .s2-encart').getBoundingClientRect(); return [e.left+e.width*.8, e.top+e.height/2]; }")
        pg.mouse.click(r[0], r[1]); pg.wait_for_timeout(1500)
        R[th + ' · par-dessus'] = pg.evaluate(J)
        pg.screenshot(path=os.path.join(OUT, 'planche_%s_dessus.png' % th), clip=clip)
        if err: R[th + ' · erreurs'] = err[:3]
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'planche_sonde.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in R.items(): print('==', k); print('  ', json.dumps(v, ensure_ascii=False)[:1500])
