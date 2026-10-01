# LE TRAIT EN MODE « DUO » — un Chiche TENU À DEUX : les deux moitiés tracées, séparées au centre (l. 14772 de l'app).
# C'est la forme du produit pour « les deux côtés ». Si le jeu n'a pas de Chiche tenu AVEC un compagnon, on le complète
# POUR LA PRISE (comme la planche 2 accrochait la brique du mur là où elle manquait) — et c'est dit dans la planche.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
CHOIX = r"""()=>{ let p = promises.find(q=>!q.draft && q.chiche && q.status==='tenu' && q.avec);
  let pose = false;
  if(!p){ p = promises.find(q=>!q.draft && q.chiche && q.status==='tenu'); if(p && !p.avec){ p.avec='Marion'; pose = true; } }
  if(!p){ p = promises.find(q=>!q.draft && q.chiche); if(p){ p.status='tenu'; if(!p.avec) p.avec='Marion'; pose = true; } }
  if(!p) return null; closeAll(); openDetail(p.id); return {id:p.id, titre:p.title, qui:p.who, avec:p.avec, complete:pose}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate(BASE); c = pg.evaluate(CHOIX); pg.wait_for_timeout(2000)
        z = pg.evaluate("""()=>{ const e=document.getElementById('tenirZone'); if(!e) return null; const r=e.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
            return {x:r.left, y:r.top, w:r.width, h:r.height, w390:+(r.width/s).toFixed(0), h390:+(r.height/s).toFixed(0)}; }""")
        R['%s' % th] = {'promi': c, 'zone': z}
        print(th, c, z and [z['w390'], z['h390']])
        if z and z['w'] > 4:
            pg.screenshot(path=os.path.join(OUT, '%s_trait_duo.png' % th), clip={'x': z['x'], 'y': z['y'], 'width': z['w'], 'height': z['h'] * 0.74})
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_fiche_duo.png' % th))
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'duo.json'), 'w'), ensure_ascii=False, indent=1)
