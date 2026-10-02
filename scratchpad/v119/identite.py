# §2 — preuve d'identité : la Pelote de v119 (lumière après le rendu) contre celle de v118 (lumière par poil), au repos et au maximum
import sys, os, math
sys.path.insert(0, '.'); sys.argv = sys.argv[:1]
import importlib.util
sp = importlib.util.spec_from_file_location('h', 'redteam_halo.py')
src = open('redteam_halo.py', encoding='utf-8').read().split("with sync_playwright() as p:")[0]
ns = {'__file__': os.path.abspath('redteam_halo.py')}; exec(compile(src, 'h', 'exec'), ns); dE00 = ns['dE00']
from playwright.sync_api import sync_playwright
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); }"""
ZONES = r"""async ([mode, val, lac])=>{ _aura.fige(true); _aura.vue(lac, 0.35); const cv=document.getElementById('auBoule');
  if(mode==='v118'){ window._peloteMod=function(o){ o.velours=val*0.55; }; } else { window._peloteU=val; }
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r)))));
  const W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data, R=0.392*W*0.93, c=W/2, Z=[];
  for(let j=0;j<3;j++) for(let i=0;i<3;i++){ let n=0,s=[0,0,0]; for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const dx=x-c, dy=y-c; if(dx*dx+dy*dy>R*R) continue;
      if(Math.floor((dx+R)/(2*R/3))!==i || Math.floor((dy+R)/(2*R/3))!==j) continue; const k=(y*W+x)*4; n++; s[0]+=d[k]; s[1]+=d[k+1]; s[2]+=d[k+2]; } Z.push(n>200?[s[0]/n,s[1]/n,s[2]/n,n]:null); }
  if(mode==='v118') window._peloteMod=null; else window._peloteU=undefined; return Z; }"""
def releve(b, url, mode, sombre):
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(7000)
    pg.evaluate("(d)=>{closeAll(); setTheme(d?'dark':'light'); Toile.setPalette('signal'); window.__R=Math.random; Math.random=function(){return 0.125;};}", sombre); pg.wait_for_timeout(700)
    pg.evaluate(OUVRE); pg.wait_for_timeout(400); pg.evaluate("()=>{Math.random=window.__R; _aura.fige(true); _aura.vue(2.9,0.35)}"); pg.wait_for_timeout(5000)
    out = {}
    for lac in (2.9, 4.4, 6.0):
        for val in (0, 1): out[(lac, val)] = pg.evaluate(ZONES, [mode, val, lac])
    ctx.close(); return out
def glob(Z): 
    n = sum(z[3] for z in Z if z); return [sum(z[c]*z[3] for z in Z if z)/n for c in range(3)]
with sync_playwright() as p:
    b = p.webkit.launch()
    print('ΔE00 entre v118 et v119 — couleur moyenne de la Pelote (dans la silhouette), et la pire des 9 zones')
    for sombre in (0, 1):
        A = releve(b, 'http://127.0.0.1:8752/zz-v118.html', 'v118', sombre); B = releve(b, 'http://127.0.0.1:8752/app.html', 'v119', sombre)
        for lac in (2.9, 4.4, 6.0):
            for val in (0, 1):
                za, zb = A[(lac, val)], B[(lac, val)]; g = dE00(glob(za), glob(zb)); pire = max(dE00(x[:3], y[:3]) for x, y in zip(za, zb) if x and y)
                eff = dE00(glob(A[(lac, 0)]), glob(A[(lac, 1)]))
                if val: print('      repos', [round(v,1) for v in glob(A[(lac,0)])], 'max v118', [round(v,1) for v in glob(za)], 'max v119', [round(v,1) for v in glob(zb)])
                print('  %-6s angle %.1f  %-8s  moyenne %.2f   pire zone %.2f   (la lumière elle-même vaut %.2f en v118)' % ('sombre' if sombre else 'clair', lac, 'MAXIMUM' if val else 'repos', g, pire, eff))
    b.close()
