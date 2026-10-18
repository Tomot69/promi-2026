# La vague de création, doigt encore posé (60 pt passés) : sa couleur, celle du trait de la page +, en clair (WebKit @2).
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
TIENT = r"""async ([pts])=>{ const el0=document.elementFromPoint(pts[0][0],pts[0][1]); const T=(x,y)=>{ const o={identifier:7,target:el0,clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,radiusX:11,radiusY:11,force:.5}; try{return new Touch(o);}catch(e){return o;} };
  const ev=(typ,x,y)=>{ const t=T(x,y), L=[t]; let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,composed:true,touches:L,targetTouches:L,changedTouches:[t]}); if(!e.changedTouches||!e.changedTouches.length) throw 0; }catch(_){ e=new Event(typ,{bubbles:true,cancelable:true,composed:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t]}); } el0.dispatchEvent(e); };
  const pe=(typ,x,y)=>el0.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,composed:true,pointerId:7,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,width:22,height:22,pressure:.5}));
  const att=ms=>new Promise(r=>setTimeout(r,ms)); pe('pointerdown',pts[0][0],pts[0][1]); ev('touchstart',pts[0][0],pts[0][1]);
  for(let i=1;i<pts.length;i++){ await att(30); pe('pointermove',pts[i][0],pts[i][1]); ev('touchmove',pts[i][0],pts[i][1]); } window.__fin=()=>{ const L=pts[pts.length-1]; pe('pointerup',L[0],L[1]); const t=T(L[0],L[1]); let e; try{ e=new TouchEvent('touchend',{bubbles:true,cancelable:true,composed:true,touches:[],targetTouches:[],changedTouches:[t]}); }catch(_){ e=new Event('touchend',{bubbles:true}); Object.defineProperty(e,'changedTouches',{value:[t]}); Object.defineProperty(e,'touches',{value:[]}); } el0.dispatchEvent(e); }; }"""
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat, k in (('promi', 0), ('chiche', 1)):
        ctx = contexte(b, dsf=2); pg = ouvre(ctx)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("n=>{const x=[...document.querySelectorAll('#createSheet .tile')][n];x&&x.click()}", k); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", 'arroser les tomates'); pg.wait_for_timeout(600)
        z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
        P = [list(pt(pg, 40 + 160 * i / 10, y)) for i in range(11)]
        pg.evaluate(TIENT, [P]); pg.wait_for_timeout(450)
        capture(pg, 'scratchpad/v149/vague_%s.png' % nat)
        pg.evaluate("()=>window.__fin()"); pg.wait_for_timeout(300); ctx.close()
    b.close()
