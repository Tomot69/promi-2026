# v208 §1 : après « tenir », le trait s'accroche-t-il à la jonction ? Molette pas à pas (6 pt), à chaque pas : la bande 104 → 124 pt, colonne par colonne, porte-t-elle le trait ?
import sys, io, os; sys.path.insert(0,'.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html'); ETAT=os.environ.get('ETAT','apres'); NAT=os.environ.get('NAT','promi')   # encours · apres · recharge
MOTS=os.environ.get("MOTSJS") or "Array.from({length:6},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true}))"
ZONE="(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
def roule(pg,d,dy):
    pg.mouse.move(d[0]+195*d[4], d[1]+600*d[4]); pg.mouse.wheel(0,dy)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    if os.environ.get('PLEIN'): ctx.add_init_script("document.addEventListener('DOMContentLoaded',function(){ var st=document.createElement('style'); st.textContent='.frame{padding:0!important;--fit:1!important}#device{border-radius:0!important;box-shadow:none!important}'; document.head.appendChild(st); });")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F)
    pid=pg.evaluate("(n)=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); if(n==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.who='moi'; p.comments=%s; delete p.parts; saveState(true); closeAll(); openDetail(p.id); return p.id; }"%MOTS, NAT)
    pg.wait_for_timeout(3000); d=B.dev(pg)
    if ETAT in ('apres','recharge'):
        z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
        B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380); pg.wait_for_timeout(5000)
    if ETAT=='recharge':
        pg.evaluate("()=>saveState(true)"); pg.reload(); pg.wait_for_timeout(6500); pg.evaluate("id=>{ closeAll(); openDetail(id); }",pid); pg.wait_for_timeout(3000); d=B.dev(pg)
    print(ETAT, 'statut', pg.evaluate("id=>promises.find(x=>x.id===id).status",pid), 'instant', pg.evaluate("()=>window._instant"))
    k=d[4]; imgs=[]
    pg.evaluate("()=>{ window._ficheSure=function(t){return t;}; }")
    print('  défilement possible', pg.evaluate("()=>{const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight;}"))
    for sc in range(0,236,12):
        pg.evaluate("v=>{ const d=document.getElementById('detailPoster'); d.style.scrollBehavior='auto'; d.scrollTop=v; }", sc); pg.wait_for_timeout(90)
        png=pg.screenshot(clip={'x':d[0],'y':d[1]+80*k,'width':390*k,'height':120*k}); imgs.append(np.asarray(Image.open(io.BytesIO(png)).convert('RGB')))
    Image.fromarray(np.concatenate(imgs,axis=0)).resize((390,120*len(imgs))).save('scratchpad/v207/c297_pas_%s_%s.png'%(NAT,ETAT))
    b.close()
