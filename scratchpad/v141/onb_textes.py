# les textes de chaque étape de l'onboarding, au doigt
import sys, json
sys.argv=[sys.argv[0]]+sys.argv[1:]
from playwright.sync_api import sync_playwright
F=sys.argv[1]
TX="""()=>{ const o=document.getElementById('promiOnb'); const out=[]; const w=document.createTreeWalker(o,NodeFilter.SHOW_TEXT); const D=document.getElementById('device').getBoundingClientRect();
  while(w.nextNode()){ const n=w.currentNode; const e=n.parentElement; let v=e, vis=true; while(v&&v!==o.parentElement){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05){vis=false;break;} v=v.parentElement; } if(!vis) continue;
    const rg=document.createRange(); rg.selectNodeContents(n); const r=rg.getBoundingClientRect(); if(r.width<1||r.top>D.bottom||r.bottom<D.top) continue; out.push(n.nodeValue); }
  return out.join('').replace(/\\u00a0/g,' ').replace(/\\s+/g,' ').trim(); }"""
def toucher(cdp,pg,x,y):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
def centre(pg,sel): return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}",sel)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500); cdp=ctx.new_cdp_session(pg)
    R={}
    R['prenom']=pg.evaluate(TX)
    c=centre(pg,'#onbPh'); toucher(cdp,pg,c[0],c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille',delay=30); pg.wait_for_timeout(300); R['prenom saisi']=pg.evaluate(TX)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900); R['parole']=pg.evaluate(TX)
    pg.keyboard.type('marcher une heure',delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(900); R['trait']=pg.evaluate(TX)
    z=pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    if z and z['dep']:
        a=[float(v) for v in z['dep'].split(',')]; e=[float(v) for v in z['arr'].split(',')]
        x0,y0,x1,y1=z['l']+a[0]*z['k'],z['t']+a[1]*z['k'],z['l']+(e[0]+6)*z['k'],z['t']+e[1]*z['k']
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x0,'y':y0}]}); pg.wait_for_timeout(90)
        for i in range(1,25):
            u=i/24.0; cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x0+(x1-x0)*u,'y':y0+(y1-y0)*u-14*z['k']*(1-abs(2*u-1))}]}); pg.wait_for_timeout(22)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        pg.wait_for_timeout(6400); R['fin']=pg.evaluate(TX)
        d=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height*0.36];}"); toucher(cdp,pg,d[0],d[1]); pg.wait_for_timeout(1000); R['compte']=pg.evaluate(TX)
    print(json.dumps(R,ensure_ascii=False,indent=1)); b.close()
