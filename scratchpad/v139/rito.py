import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'; mondes=(sys.argv[2] if len(sys.argv)>2 else 'ritournelle,bobinette,esquille,encre').split(',')
HIT=r"""()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(); const kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height; const G={};
  for(let y=dv.top+4;y<dv.bottom-4;y+=6) for(let x=dv.left+4;x<dv.right-4;x+=6){ let h=null; try{h=Toile.hit((x-r.left)*kx,(y-r.top)*ky);}catch(e){} if(h&&h.pid!=null){ const g=G[h.pid]=G[h.pid]||{n:0,x0:1e9,y0:1e9,x1:-1e9,y1:-1e9}; g.n++; g.x0=Math.min(g.x0,x-dv.left); g.x1=Math.max(g.x1,x-dv.left); g.y0=Math.min(g.y0,y-dv.top); g.y1=Math.max(g.y1,y-dv.top);} }
  return {G:Object.keys(G).map(k=>{const p=promises.find(q=>q.id==k); return [(p?p.title:k), G[k].n, Math.round(G[k].x0), Math.round(G[k].y0), Math.round(G[k].x1), Math.round(G[k].y1)]}), zoom:(Toile.zoom?Toile.zoom():null), vue:(Toile.vue?Toile.vue():null), n:promises.length, gr:Toile.graines&&Toile.graines()}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    for m in mondes:
        N=int(sys.argv[3]) if len(sys.argv)>3 else 0
        if N: pg.evaluate("(n)=>{ promises.splice(n); try{ for(var k in NUE) delete NUE[k]; }catch(e){} syncAll(); }", N)
        pg.evaluate("(m)=>{ try{closeAll()}catch(e){} setView(\"toile\"); Toile.setTheme(m); }", m); pg.wait_for_timeout(3500)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='planche-v139/rito-%s.png'%m,clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]})
        o=pg.evaluate(HIT); print(m,'zoom',o['zoom'],'vue',o['vue'],'paroles',o['n'],'graines',o['gr']); 
        for g in o['G']: print('   ',g)
    b.close()
