# LES DALLES DE L'ÉCRAN QUI VEND SE LISENT-ELLES ? ΔE (CIELAB, 1976) entre la matière de chaque dalle (couleur moyenne de ses
# pixels opaques) et le fond de l'écran — deux thèmes, quatre chargements chacun (la couleur d'une dalle est tirée au hasard
# à chaque chargement : chantier 59). Repère : le plancher de lisibilité d'une dalle, ΔE 15 (Q192, CLAUDE §7).
from playwright.sync_api import sync_playwright
J = r"""()=>{ const lab=(r,g,b)=>{ const f=v=>{v/=255; return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);}; let R=f(r),G=f(g),B=f(b);
    let X=(R*.4124+G*.3576+B*.1805)/.95047, Y=(R*.2126+G*.7152+B*.0722), Z=(R*.0193+G*.1192+B*.9505)/1.08883;
    const h=t=>t>.008856?Math.cbrt(t):(7.787*t+16/116); X=h(X);Y=h(Y);Z=h(Z); return [116*Y-16, 500*(X-Y), 200*(Y-Z)]; };
  const ps=document.getElementById('plusScreen'); const fb=getComputedStyle(ps).backgroundColor.match(/[\d.]+/g).map(Number); const F=lab(fb[0],fb[1],fb[2]);
  return [...ps.querySelectorAll('#plCadre .plv-dal')].map((c,i)=>{ const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0,r=0,g=0,b=0;
    for(let k=0;k<d.length;k+=4){ if(d[k+3]>200){ n++; r+=d[k]; g+=d[k+1]; b+=d[k+2]; } }
    if(!n) return [c.dataset.monde, null]; const M=lab(r/n,g/n,b/n); return [c.dataset.monde, +Math.hypot(M[0]-F[0],M[1]-F[1],M[2]-F[2]).toFixed(1), [Math.round(r/n),Math.round(g/n),Math.round(b/n)], (window._vendDalles||[])[i] && window._vendDalles[i].id]; }); }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        for k in range(4):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
            pg.evaluate("()=>{ closeAll(); document.getElementById('cercleTopBtn').click(); }"); pg.wait_for_timeout(1500)
            print(th, k + 1, pg.evaluate(J))
            pg.context.close()
    br.close()
