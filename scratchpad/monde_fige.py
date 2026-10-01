#!/usr/bin/env python3
"""LA DALLE EST-ELLE FIGÉE À LA PLANTATION ?

On peint la MÊME dalle (même id) dans deux mondes différents et on compare
sa SIGNATURE de composition — pas ses pixels bruts (la matière respire avec
performance.now(), CLAUDE.md §7). On compare : le rectangle peint et un
histogramme grossier des couleurs, qui distingue un monde d'un autre.
"""
from playwright.sync_api import sync_playwright

SIG = r"""(id)=>{
  const c=document.createElement('canvas'); c.width=240; c.height=240;
  c.style.cssText='width:120px;height:120px';
  document.body.appendChild(c);
  const ok = window.Toile.dalleTrame(c,id,1);
  const g=c.getContext('2d'), d=g.getImageData(0,0,240,240).data;
  let n=0, minx=1e9,miny=1e9,maxx=-1,maxy=-1;
  const hist={};
  for(let y=0;y<240;y+=2)for(let x=0;x<240;x+=2){
    const i=(y*240+x)*4;
    if(d[i+3]<10) continue;
    n++;
    if(x<minx)minx=x; if(x>maxx)maxx=x; if(y<miny)miny=y; if(y>maxy)maxy=y;
    const k=(d[i]>>5)+'-'+(d[i+1]>>5)+'-'+(d[i+2]>>5);
    hist[k]=(hist[k]||0)+1;
  }
  c.remove();
  const tons = Object.keys(hist).sort((a,b)=>hist[b]-hist[a]).slice(0,4);
  return {ok:ok, remplissage:n, boite:[maxx-minx,maxy-miny], tons:tons};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ids = pg.evaluate("()=>promises.filter(p=>!p.draft&&!p.req).slice(0,3).map(p=>p.id)")
    print('Promi mesurés :', ids)
    print('\nUn Promi porte-t-il un monde ?  →',
          pg.evaluate("()=>{const p=promises[0]; return Object.keys(p).filter(k=>/monde|world|struct|theme/i.test(k));}")
          or 'AUCUN CHAMP de monde sur un Promi')
    for monde in ('encre','mosaique','terrazzo'):
        pg.evaluate("(m)=>{window.Toile.setTheme(m); if(typeof state!=='undefined')state.structure=m;}", monde)
        pg.wait_for_timeout(900)
        print('\n── monde courant :', monde)
        for i in ids:
            print('   dalle', i, pg.evaluate(SIG, i))
    b.close()
