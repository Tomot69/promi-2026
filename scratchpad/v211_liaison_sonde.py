import sys, re, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src = open('redteam_onb_exemple.py', encoding='utf-8').read()
m = re.search(r'^CLAV\s*=\s*(""".*?"""|"[^\n]*")', src, re.S | re.M); CLAV = eval(m.group(1)) if m else ''
REC = r"""(sel)=>{ window.__fr=[]; let on=true; window.__frStop=()=>{on=false;}; const f=()=>{ if(!on) return;
  const L=[...document.querySelectorAll(sel)].filter(e=>e.isConnected).map(e=>{ const w=getComputedStyle(e), r=e.getBoundingClientRect(); if(!e.__nid) e.__nid=(window.__nidc=(window.__nidc||0)+1); return [e.__nid, e.textContent, w.clipPath.slice(0,34), +w.opacity, w.visibility, Math.round(r.left), Math.round(r.width), e.__v203tx?1:0]; });
  const li=document.querySelector(sel), lr=li&&li.getBoundingClientRect();
  const cop=[...document.querySelectorAll('canvas[data-trace]')].filter(c=>{ const r=c.getBoundingClientRect(); return lr && r.right>lr.left && r.left<lr.right && r.bottom>lr.top && r.top<lr.bottom && r.width>0; }).map(c=>{ let n=0; try{ const g=c.getContext('2d'), r=c.getBoundingClientRect(), sx=c.width/r.width, sy=c.height/r.height, x0=Math.max(0,Math.floor((lr.left-r.left)*sx)), y0=Math.max(0,Math.floor((lr.top-r.top)*sy)), w=Math.max(1,Math.min(c.width-x0,Math.ceil(lr.width*sx))), h=Math.max(1,Math.min(c.height-y0,Math.ceil(lr.height*sy))); const d=g.getImageData(x0,y0,w,h).data; for(let i=3;i<d.length;i+=4) if(d[i]>60) n++; }catch(e){ n=-1; } return n; });
  window.__fr.push([Math.round(performance.now()), L, cop]); requestAnimationFrame(f); }; requestAnimationFrame(f); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); ctx.add_init_script(CLAV) if CLAV else None
    if '--lent' in sys.argv:
        L=open('redteam_premiere_froid.py',encoding='utf-8').read(); m2=re.search(r'^LENT = (r""".*?""")', L, re.S|re.M); ctx.add_init_script(eval(m2.group(1)))
    ctx2=None
    if '--onb' in sys.argv:
        ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV)
        pg = B.ouvre(ctx, 'app.html', attente=7000); B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(700)
        pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(400); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200); B.attend_parole(pg)
        B.tap_sel(pg, '#onbPh [data-onb="parole"]'); pg.wait_for_timeout(1500); SEL='#onbPh .onbv-de'
    else:
        pg = B.ouvre(ctx, 'app.html')
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
        B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500); SEL='#csPhrase .ph-li'
    pg.evaluate(REC, SEL)
    for c in 'aller': pg.keyboard.type(c); pg.wait_for_timeout(300)
    pg.wait_for_timeout(1500)
    for _ in range(5): pg.keyboard.press('Backspace'); pg.wait_for_timeout(300)
    pg.wait_for_timeout(2000); pg.evaluate("()=>__frStop()"); fr = pg.evaluate("()=>__fr")
    prev = None
    for t, L, c in fr:
        k = json.dumps([L, c])
        if k != prev: print(t, L, c); prev = k
    b.close()
