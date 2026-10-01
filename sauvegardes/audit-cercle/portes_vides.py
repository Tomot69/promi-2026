# DEPUIS UN ÉTAT VIDE (aucun Promi planté — le démarrage neuf de l'app, `promi_fresh`), quelles portes mènent au Cercle ?
# Tom : « personne n'arrive sur le Cercle sans avoir rien planté […] Si tu trouves un chemin qui mène au Cercle depuis un état
# vide, note-le — c'est probablement lui qu'il faut corriger. » Et l'écran qui vend, sans dalles : la rangée cachée, le prix remonté.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'vend')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
POINT = r"""(sel)=>{ const e=document.querySelector(sel); if(!e) return {existe:false}; const dv=document.getElementById('device').getBoundingClientRect();
  let r=e.getBoundingClientRect(); if(r.top<dv.top||r.bottom>dv.bottom){ e.scrollIntoView({block:'center'}); r=e.getBoundingClientRect(); }
  const vis=e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}) && r.width>2 && r.height>2; const x=r.left+r.width*.8, y=r.top+r.height/2;
  const h=document.elementFromPoint(x,y); return {existe:true, vis, doigt:!!(h&&(h===e||e.contains(h))), x, y, texte:(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,40)}; }"""
DELEGUES = r"""()=>[...document.querySelectorAll('.adv-lock,[data-cercle],.set-cercle,#pplusBanner,#openPlus,.nqh-cercle,#karmaCercle')].filter(e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&e.getBoundingClientRect().width>2).map(e=>(e.id||e.className).toString().slice(0,40)+' « '+(e.textContent||'').trim().slice(0,30)+' »')"""
VIDE = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390; const c=document.getElementById('plCadre'); const y=(q)=>{ const e=document.querySelector('#plusScreen '+q); return e&&e.checkVisibility()? +((e.getBoundingClientRect().top-dv.top)/s).toFixed(1) : null; };
  return {n:(typeof promises!=='undefined'?promises.length:null), sans: c?c.classList.contains('plv-sans'):null, dalles:[...document.querySelectorAll('#plCadre .plv-dal')].map(e=>e.checkVisibility()), noms:[...document.querySelectorAll('#plCadre .plv-nom')].map(e=>e.checkVisibility()),
    prix:y('.plv-prix'), sous:y('.plv-sous'), annee:y('#buyYear'), essai:y('#buyMonth'), notes:[...document.querySelectorAll('#plCadre .pl-note')].map(e=>+((e.getBoundingClientRect().top-dv.top)/s).toFixed(1)), declare:window._vendSans}; }"""
PORTES = [
  ('accueil · le bouton du Cercle', [], '#cercleTopBtn'),
  ('Réglages · l’encart', [("()=>document.getElementById('settingsBtn').click()", 1700)], '#openPlusTop'),
  ('Studio · un monde payant (Terrazzo)', [("()=>document.getElementById('studioBtn').click()", 1900), ("()=>{const d=document.querySelector('#studioScreen [data-w=\"terrazzo\"]'); if(d) d.click();}", 1500)], '#stLockCta'),
  ('Aura · l’aide « i »', [("()=>document.getElementById('souffleBtn').click()", 2600), ("()=>document.getElementById('auraInfoBtn').click()", 1200)], '#ahCercleCta'),
  ('page + · le mur de son Peaufiner', [("()=>document.getElementById('createBtn').click()", 600),
      ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
      ("()=>document.getElementById('csBotBar').click()", 1800)], '#createSheet .s2-encart'),
]
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        for nom, steps, cible in PORTES:
            ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            ctx.add_init_script("try{ localStorage.setItem('promi_fresh','1'); }catch(e){}")
            pg = ctx.new_page()
            try: pg.goto('http://127.0.0.1:8752/app.html', timeout=90000)
            except Exception: pg.goto('http://127.0.0.1:8752/app.html', timeout=90000)
            pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
            n0 = pg.evaluate("()=>typeof promises!=='undefined'?promises.filter(q=>!q.draft).length:null")
            pg.evaluate(BASE); pg.wait_for_timeout(300)
            for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
            deleg = pg.evaluate(DELEGUES)
            pt = pg.evaluate(POINT, cible); pg.wait_for_timeout(250); pt = pg.evaluate(POINT, cible)
            ouvre = None
            if pt.get('existe') and pt.get('vis'):
                pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(1300)
                ouvre = pg.evaluate("()=>document.getElementById('plusScreen').classList.contains('show')")
            v = pg.evaluate(VIDE) if ouvre else None
            R['%s · %s' % (th, nom)] = {'promi_plantes': n0, 'porte': pt, 'ouvre_le_cercle': ouvre, 'ecran_vide': v, 'autres_portes_visibles': deleg}
            print('%-5s %-38s plantés %s · porte %s · doigt %s · ouvre %s · %s' % (th, nom, n0, 'visible' if pt.get('vis') else ('absente' if not pt.get('existe') else 'cachée'), pt.get('doigt'), ouvre, json.dumps(v, ensure_ascii=False) if v else ''))
            if deleg: print('      autres portes visibles :', deleg)
            if ouvre and nom.startswith('accueil'):
                clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
                pg.screenshot(path=os.path.join(OUT, 'vide_%s.png' % th), clip=clip)
            ctx.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'portes_vides.json'), 'w'), ensure_ascii=False, indent=1)
