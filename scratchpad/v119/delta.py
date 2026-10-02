# la structure de l'écart « velours max − repos » : par zone 6×6, à trois angles, deux thèmes
import sys, io, math
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
J = r"""async ([lac])=>{ _aura.fige(true); _aura.vue(lac, 0.35); const cv=document.getElementById('auBoule'); const W=cv.width;
  function lit(v){ return new Promise(r=>{ window._peloteMod=function(o){ o.velours=v; }; requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{ const d=cv.getContext('2d').getImageData(0,0,W,W).data; r(d); }))); }); }
  const A=await lit(0), B=await lit(0.55); window._peloteMod=null;
  const N=6, out=[]; for(let j=0;j<N;j++) for(let i=0;i<N;i++){ let n=0,a=[0,0,0],b=[0,0,0]; const x0=Math.floor(W*(0.12+0.76*i/N)), x1=Math.floor(W*(0.12+0.76*(i+1)/N)), y0=Math.floor(W*(0.12+0.76*j/N)), y1=Math.floor(W*(0.12+0.76*(j+1)/N));
    for(let y=y0;y<y1;y+=2) for(let x=x0;x<x1;x+=2){ const k=(y*W+x)*4; if(A[k+3]<250) continue; n++; for(let c=0;c<3;c++){ a[c]+=A[k+c]; b[c]+=B[k+c]; } }
    out.push(n>40?[a.map(v=>v/n), b.map(v=>v/n)]:null); }
  return {W:W, z:out}; }"""
def lum(c): return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for d in (0, 1):
        ouvre(pg, d); pg.wait_for_timeout(2500)
        for lac in (2.9, 4.4, 6.0):
            r = pg.evaluate(J, [lac]); g = [None if z is None else lum(z[1])/max(1, lum(z[0])) for z in r['z']]
            print('sombre' if d else 'clair', 'lac %.1f' % lac, 'W', r['W'])
            for j in range(6): print('   ' + ' '.join('  -- ' if g[j*6+i] is None else '%.3f' % g[j*6+i] for i in range(6)))
            # le rapport par canal, zone centrale
            z = r['z'][14]; print('   zone centre : repos', [round(v) for v in z[0]], 'max', [round(v) for v in z[1]])
        pg.evaluate("()=>{_aura.fige(false); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    b.close()
