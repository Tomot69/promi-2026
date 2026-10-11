# mesure Ritournelle : largeur peinte de la dalle (pixels), dalles entières, cellules vides entièrement visibles
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; M=sys.argv[2] if len(sys.argv)>2 else 'ritournelle'
NS=[1,2,3,4,9]
CEL="""()=>{ const L=Toile_lecture(), v=L.vue, G=L.graines; const st={};
  for(let y=1;y<L.H;y+=2) for(let x=1;x<L.W;x+=2){ let bd=1e18,bk=-1; for(let k=0;k<G.length;k++){ const d=Math.hypot(x-G[k].x,y-G[k].y)-G[k].w; if(d<bd){bd=d;bk=k;} }
    const sx=x*v.s+v.ox, sy=y*v.s+v.oy; const o=st[bk]=st[bk]||{n:0,de:0,x0:1e9,x1:-1e9,y0:1e9,y1:-1e9}; o.n++; if(sx<0||sx>L.W||sy<0||sy>L.H) o.de++; o.x0=Math.min(o.x0,sx);o.x1=Math.max(o.x1,sx);o.y0=Math.min(o.y0,sy);o.y1=Math.max(o.y1,sy); }
  const out=[]; for(const k in st){ const g=G[k], o=st[k]; out.push({kind:g.kind,pid:g.pid,ent:o.de===0 && o.x0>2&&o.x1<L.W-2&&o.y0>2&&o.y1<L.H-2, bx:[Math.round(o.x0),Math.round(o.x1),Math.round(o.y0),Math.round(o.y1)]}); }
  return {s:v.s,ox:v.ox,oy:v.oy,W:L.W,H:L.H,c:out}; }"""
def dalle(c): return (abs(c[0]-130)<26 and abs(c[1]-174)<26 and abs(c[2]-248)<26) or (abs(c[0]-255)<22 and abs(c[1]-184)<24 and abs(c[2]-210)<26)
with sync_playwright() as p:
    b=p.webkit.launch()
    for n in NS:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6000)
        pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} }",n)
        pg.evaluate("(m)=>{Toile.setTheme(m); Toile.sync([]); }",M); pg.wait_for_timeout(1200)
        for k in range(1,n+1):
            pg.evaluate("(k)=>{ Toile.sync(promises.slice(0,k).map(p=>p.id)); }",k); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ try{Toile_recadre()}catch(e){} }"); pg.wait_for_timeout(4500)
        o=pg.evaluate(CEL)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        im=Image.open(io.BytesIO(pg.screenshot(clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}))).convert('RGB').resize((390,844)); im.save('scratchpad/v141/rito-%s-%d.png'%(F.replace('.html',''),n)); px=im.load()
        xs=[];ys=[]
        for y in range(104,706,2):
            for x in range(0,390,2):
                if dalle(px[x,y]): xs.append(x); ys.append(y)
        bo=[min(xs),max(xs),min(ys),max(ys)] if xs else None
        vides=[c for c in o['c'] if c['kind']=='gray' and c['ent']]; par=[c for c in o['c'] if c['kind']!='gray']
        print('%d parole(s) : zoom %.2f · matière peinte %s (largeur %s) · cellules de parole entières %d/%d %s · vides entièrement visibles %d'%(n,o['s'],bo,(bo[1]-bo[0]) if bo else None,sum(1 for c in par if c['ent']),len(par),[c['bx'] for c in par],len(vides)))
        ctx.close()
    b.close()
