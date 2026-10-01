#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accueil_audit.py — relevé de l'accueil (la Toile), à l'exécution, deux thèmes.
A. inventaire des nœuds visibles + écouteurs (CDP)   B. chaque commande touchée : ce qui s'ouvre
C. zone libre (où un doigt atteint la Toile)          D. atteignabilité de chaque dalle par zoom
E. pincement réel au doigt CDP : le dézoom tient-il ? (relâché, fiche ouverte/fermée, plantation)"""
import json, sys
from playwright.sync_api import sync_playwright
APP = "http://127.0.0.1:8752/app.html"
OUT = {}

INV_JS = r"""()=>{
 const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
 const out=[];
 document.querySelectorAll('#device *').forEach(el=>{
   if(el.closest('.screen,.sheet,.poster,#promiOnb,#feedView,#scrim,svg>*'))return;
   const r=el.getBoundingClientRect(); if(r.width<2||r.height<2)return;
   const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05)return;
   if(r.right<D.left||r.left>D.right||r.bottom<D.top||r.top>D.bottom)return;
   const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
   const cx=r.left+r.width/2, cy=r.top+r.height/2;
   const top=document.elementFromPoint(cx,cy);
   out.push({tag:el.tagName.toLowerCase(),id:el.id||'',cls:(el.getAttribute('class')||'').slice(0,60),
     txt:own.slice(0,40), x:+((r.left-D.left)/k).toFixed(1), y:+((r.top-D.top)/k).toFixed(1),
     w:+(r.width/k).toFixed(1), h:+(r.height/k).toFixed(1), pe:cs.pointerEvents, cur:cs.cursor,
     z:cs.zIndex, op:cs.opacity, col:cs.color, bg:cs.backgroundColor, bd:cs.borderTopWidth+' '+cs.borderTopColor,
     rad:cs.borderTopLeftRadius, ff:cs.fontFamily.split(',')[0], fs:cs.fontSize, fw:cs.fontWeight,
     reach: !!top && (top===el||el.contains(top))});
 });
 return out;}"""

MASK_JS = r"""()=>{
 const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
 const cv=document.getElementById('toileCv'); const st=document.getElementById('stage').getBoundingClientRect();
 const cvr=cv.getBoundingClientRect();
 const rows=[]; const blockers={};
 for(let y=0;y<844;y+=4){ let row='';
   for(let x=0;x<390;x+=4){ const e=document.elementFromPoint(D.left+(x+2)*k, D.top+(y+2)*k);
     const free = e===cv; row+= free?'1':'0';
     if(!free&&e){const n=e.id?('#'+e.id):(e.closest('[id]')?('#'+e.closest('[id]').id+' '+e.tagName.toLowerCase()):e.tagName); blockers[n]=(blockers[n]||0)+1;}
   } rows.push(row);}
 return {rows, blockers, cv:{x:(cvr.left-D.left)/k,y:(cvr.top-D.top)/k,w:cvr.width/k,h:cvr.height/k, cw:cv.clientWidth, ch:cv.clientHeight},
   stage:{x:(st.left-D.left)/k,y:(st.top-D.top)/k,w:st.width/k,h:st.height/k}};}"""

# D — pour chaque dalle, à chaque zoom s, existe-t-il un cadrage admissible (la même borne cp()
# que le moteur) où un point de la dalle tombe sur la zone libre ET où Toile.hit rend CETTE dalle ?
# hit() est pur : pour émuler une vue (s,ox,oy), on interroge hit(ox0+s0*lx, oy0+s0*ly) sous la vue réelle.
REACH_JS = r"""(args)=>{
 const [rows, zooms] = args;
 const cv=document.getElementById('toileCv'); const W=cv.clientWidth, H=cv.clientHeight;
 const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
 const cvr=cv.getBoundingClientRect(); const offx=(cvr.left-D.left)/k, offy=(cvr.top-D.top)/k;
 const free=(sx,sy)=>{ const X=Math.floor((sx+offx)/4), Y=Math.floor((sy+offy)/4);
   return Y>=0&&Y<rows.length&&X>=0&&X<rows[0].length&&rows[Y][X]==='1'; };
 const v0=Toile.vue();
 const ids=promises.filter(p=>!p.draft&&!p.req).map(p=>p.id);
 const res={W,H,v0,zooms:{}};
 const polys={}; ids.forEach(id=>{const a=Toile.dalleAbs(id); if(a)polys[id]=a;});
 res.sansPoly=ids.filter(id=>!polys[id]);
 for(const s of zooms){
   const lx0=Math.min(0,W-W*s), hx0=Math.max(0,W-W*s), ly0=Math.min(0,H-H*s), hy0=Math.max(0,H-H*s);
   const NP=12; const unreach=[]; const atS1pan=[];
   for(const id of Object.keys(polys)){
     const a=polys[id]; let ok=false, okFixe=false;
     // points échantillons dans la boîte de la cellule
     const pts=[]; for(let i=1;i<8;i++)for(let j=1;j<8;j++)pts.push([a.minx+a.w*i/8, a.miny+a.h*j/8]);
     const good=pts.filter(([lx,ly])=>{const h=Toile.hit(v0.ox+v0.s*lx, v0.oy+v0.s*ly); return h&&h.pid==+id;});
     for(let pi=0;pi<=NP&&!ok;pi++)for(let pj=0;pj<=NP&&!ok;pj++){
       const ox=lx0+(hx0-lx0)*pi/NP, oy=ly0+(hy0-ly0)*pj/NP;
       for(const [lx,ly] of good){ if(free(ox+s*lx, oy+s*ly)){ok=true;break;} }
     }
     // sans déplacer la vue : au cadrage où l'on arrive (centré, ou borné)
     const oxc=Math.max(lx0,Math.min(hx0,(W-W*s)/2)), oyc=Math.max(ly0,Math.min(hy0,(H-H*s)/2));
     for(const [lx,ly] of good){ if(free(oxc+s*lx, oyc+s*ly)){okFixe=true;break;} }
     if(!ok)unreach.push(+id); if(!okFixe)atS1pan.push(+id);
   }
   res.zooms[s]={n:Object.keys(polys).length, inatteignables:unreach, sansDeplacer:atS1pan};
 }
 res.titres={}; ids.forEach(id=>{const p=promises.find(q=>q.id===id); res.titres[id]=(p.title||p.t||'').slice(0,24)+(p.nuee?' ['+p.nuee+']':'');});
 return res;}"""

CMDS = [('#brandBtn','mot-marque'),('#cercleTopBtn','rond haut gauche (Cercle)'),('#settingsBtn','rond haut droit (Réglages)'),
        ('#viewSwitch button[data-view=index]','Index'),('#viewSwitch button[data-view=toile]','Toile'),
        ('#studioBtn','Studio'),('#souffleBtn','Aura'),('#createBtn','+'),('#filBtn','Fil'),('#shareBtn','Partager')]

FT = "()=>{try{if(window.quitteVues)quitteVues();}catch(e){}document.querySelectorAll('.screen.show,.sheet.show,.poster.show').forEach(x=>x.classList.remove('show'));var s=document.getElementById('scrim');s&&s.classList.remove('show');document.querySelector('.device').classList.remove('sigmode');}"
OPEN_JS = r"""()=>{const o=[];document.querySelectorAll('.show,.in,.sigmode,.v-fil').forEach(e=>{if(e.closest('#promiOnb'))return;o.push((e.id?'#'+e.id:e.className.toString().split(' ')[0])+'.'+[...e.classList].filter(c=>['show','in','sigmode','v-fil'].includes(c)).join('.'));});
 const fv=document.getElementById('feedView'); if(fv&&fv.style.display!=='none')o.push('feedView visible'); return o;}"""


def passe_onb(pg):
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")


def pinch(cdp, cx, cy, d0, d1, steps=14, dt=16):
    t = 0
    def ev(typ, d):
        pts = [] if typ == 'touchEnd' else [{'x': cx - d/2, 'y': cy, 'id': 1}, {'x': cx + d/2, 'y': cy, 'id': 2}]
        cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': pts})
    ev('touchStart', d0)
    for i in range(1, steps + 1):
        ev('touchMove', d0 + (d1 - d0) * i / steps)
    ev('touchEnd', d1)


def drag(cdp, x0, y0, x1, y1, steps=12):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0, 'id': 1}]})
    for i in range(1, steps + 1):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1-x0)*i/steps, 'y': y0 + (y1-y0)*i/steps, 'id': 1}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})


with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        R = OUT[th] = {}
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page()
        pg.goto(APP); pg.wait_for_timeout(6800); passe_onb(pg)
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{var d=document.querySelector('.device');d.classList.remove('sigmode');var b=document.getElementById('brandBtn');b&&b.classList.remove('sig-on');}")
        R['inventaire'] = pg.evaluate(INV_JS)
        R['masque'] = pg.evaluate(MASK_JS)
        # écouteurs
        cdp = ctx.new_cdp_session(pg)
        lst = {}
        for sel in ['#brandBtn','#promiI','#subtitle','#cercleTopBtn','#settingsBtn','#viewSwitch','#stage','#toileCv','#toileEmpty','#sidelabel',
                    '#cap','.footer','.dock','#studioBtn','#souffleBtn','#createBtn','#filBtn','#filDot','#shareBtn','.topbar','.statusbar']:
            oid = cdp.send('Runtime.evaluate', {'expression': "document.querySelector('%s')" % sel})['result'].get('objectId')
            if not oid: lst[sel] = None; continue
            L = cdp.send('DOMDebugger.getEventListeners', {'objectId': oid})['listeners']
            lst[sel] = sorted(set('%s%s' % (l['type'], '(cap)' if l['useCapture'] else '') for l in L))
        R['ecouteurs'] = lst
        R['onclick'] = pg.evaluate("""()=>['brandBtn','cercleTopBtn','settingsBtn','studioBtn','souffleBtn','createBtn','filBtn','shareBtn']
            .reduce((o,i)=>{const e=document.getElementById(i);o[i]=!!(e&&e.onclick);return o;},{})""")
        # zones de hit:
        zooms = [0.4, 0.48, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 2, 3, 5]
        R['atteinte'] = pg.evaluate(REACH_JS, [R['masque']['rows'], zooms])
        # B — commandes
        cmd = {}
        for sel, nom in CMDS:
            pg.evaluate(FT); pg.wait_for_timeout(700)
            avant = pg.evaluate(OPEN_JS)
            try:
                pg.locator(sel).first.tap(timeout=3000)
            except Exception as e:
                cmd[nom] = {'erreur': str(e)[:120]}; continue
            pg.wait_for_timeout(1100)
            ap = pg.evaluate(OPEN_JS)
            cmd[nom] = {'ouvre': [x for x in ap if x not in avant], 'avant': avant}
            if nom == 'mot-marque':
                pg.locator(sel).first.tap(); pg.wait_for_timeout(400)
        pg.evaluate(FT); pg.wait_for_timeout(800)
        R['commandes'] = cmd
        # appui long sur la Toile (zone libre au centre)
        D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
        def dev(x, y): return D[0] + x*D[2], D[1] + y*D[2]
        x, y = dev(195, 600)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
        pg.wait_for_timeout(700)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        pg.wait_for_timeout(900)
        R['appuiLong'] = pg.evaluate(OPEN_JS)
        pg.evaluate(FT); pg.wait_for_timeout(900)
        # E — pincement réel
        E = R['zoom'] = {}
        E['depart'] = pg.evaluate("()=>Toile.vue()")
        cx, cy = dev(195, 470)
        pinch(cdp, cx, cy, 300*D[2], 60*D[2]); pg.wait_for_timeout(120)
        E['pendant'] = pg.evaluate("()=>Toile.vue()")
        pg.wait_for_timeout(1500)
        E['relache_1500ms'] = pg.evaluate("()=>Toile.vue()")
        drag(cdp, *dev(195, 470), *dev(120, 300)); pg.wait_for_timeout(600)
        E['apres_glisse'] = pg.evaluate("()=>Toile.vue()")
        pg.wait_for_timeout(4000)
        E['apres_4s'] = pg.evaluate("()=>Toile.vue()")
        # toucher une dalle au dézoom
        hitpt = pg.evaluate("""()=>{const v=Toile.vue();const ids=promises.filter(p=>!p.draft&&!p.req).map(p=>p.id);
            for(const id of ids){const a=Toile.dalleAbs(id); if(!a)continue; const lx=a.minx+a.w/2, ly=a.miny+a.h/2;
              const sx=v.ox+v.s*lx, sy=v.oy+v.s*ly; const h=Toile.hit(sx,sy); if(!h||h.pid!==id)continue;
              const cv=document.getElementById('toileCv').getBoundingClientRect(); const k=cv.width/cv.clientWidth||1;
              const X=cv.left+sx*k, Y=cv.top+sy*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv')return {id,X,Y};}
            return null;}""")
        E['cible'] = hitpt
        if hitpt:
            pg.touchscreen.tap(hitpt['X'], hitpt['Y']); pg.wait_for_timeout(1400)
            E['toucher_ouvre'] = pg.evaluate(OPEN_JS) + [pg.evaluate("()=>String(window.__dpId||'')")]
            pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(1500)
            E['apres_fiche_fermee'] = pg.evaluate("()=>Toile.vue()")
        # passer par un autre écran et revenir
        pg.evaluate(FT); pg.wait_for_timeout(500); pg.locator('#filBtn').tap(timeout=4000); pg.wait_for_timeout(900)
        pg.evaluate("()=>setView('toile')"); pg.wait_for_timeout(1500)
        E['apres_fil'] = pg.evaluate("()=>Toile.vue()")
        E['sync_appele'] = pg.evaluate("()=>{Toile.sync(promises.filter(p=>!p.draft&&!p.req).map(p=>p.id));return 1;}")
        pg.wait_for_timeout(2500)
        E['apres_sync'] = pg.evaluate("()=>Toile.vue()")
        # zoom avant maximum
        pinch(cdp, cx, cy, 40*D[2], 380*D[2], steps=20); pg.wait_for_timeout(1500)
        E['zoom_avant'] = pg.evaluate("()=>Toile.vue()")
        R['nb_promi'] = pg.evaluate("()=>promises.filter(p=>!p.draft&&!p.req).length")
        R['nb_brouillons'] = pg.evaluate("()=>promises.filter(p=>p.draft).length")
        R['nb_demandes'] = pg.evaluate("()=>promises.filter(p=>p.req).length")
        pg.screenshot(path='scratchpad/accueil_%s.png' % th, clip={'x': D[0], 'y': D[1], 'width': 390*D[2], 'height': 844*D[2]})
        ctx.close()
    b.close()
json.dump(OUT, open('scratchpad/accueil_audit.json', 'w'), ensure_ascii=False, indent=1)
print('ok')
