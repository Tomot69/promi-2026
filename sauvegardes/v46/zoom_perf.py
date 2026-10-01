# Intervalle entre images PENDANT un pincement (dézoom puis zoom, 1,6 s), par monde. Pincement joué DANS la page avec de
# vrais PointerEvent (WebKit n'a pas de CDP). python3 zoom_perf.py [--webkit] monde...
import sys
from playwright.sync_api import sync_playwright
WK='--webkit' in sys.argv; MS=[a for a in sys.argv[1:] if not a.startswith('--')]
JS=r"""async (m)=>{ Toile.setTheme(m); await new Promise(r=>setTimeout(r,2500)); Toile_recadre(); await new Promise(r=>setTimeout(r,1500));
 const host=document.getElementById('toileCv'), R=host.getBoundingClientRect(), cx=R.left+R.width/2, cy=R.top+R.height*0.52;
 function ev(type,id,x,y){ host.dispatchEvent(new PointerEvent(type,{pointerId:id,clientX:x,clientY:y,bubbles:true,cancelable:true,pointerType:'touch',isPrimary:id===1})); }
 const d=[]; let t0=performance.now(), tp=t0, i=0; const N=96;
 ev('pointerdown',1,cx-60,cy); ev('pointerdown',2,cx+60,cy);
 await new Promise(res=>{ function f(t){ d.push(t-tp); tp=t; i++; const u=i/N, dd= u<0.5 ? 120-90*(u/0.5) : 30+270*((u-0.5)/0.5);
   ev('pointermove',1,cx-dd,cy); ev('pointermove',2,cx+dd,cy); if(i<N) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 ev('pointerup',1,cx-150,cy); ev('pointerup',2,cx+150,cy);
 d.shift(); d.sort((a,b)=>a-b); return {n:d.length, med:+d[d.length>>1].toFixed(1), p90:+d[Math.floor(d.length*.9)].toFixed(1), max:+d[d.length-1].toFixed(1), s:+Toile.vue().s.toFixed(2)}; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:100]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in MS: print(('webkit' if WK else 'chromium'), m, pg.evaluate(JS,m))
    print('erreurs', er[:3]); b.close()
