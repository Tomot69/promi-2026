# après « tenir » : tous les textes visibles sur la fiche, à plusieurs instants ; et tracer la SECONDE moitié seule (195→360) tient-il ?
import sys
from playwright.sync_api import sync_playwright
ONDE_FI = "(a)=>{ const cv=document.getElementById('dpTrameCv'), t=cv&&(cv.getAttribute('data-trait')||'').split(','); if(!t||t.length<4) return null; const r=cv.getBoundingClientRect(), k=r.width/390, f=window._onde.onde(+t[0],+t[1]), P=[]; for(let x=a[0];x<=a[1];x+=11) P.push([r.left+x*k, r.top+f(x)*k]); return P; }"
TXT = """()=>{ const D=document.getElementById('device').getBoundingClientRect(); const out=[]; const w=document.createTreeWalker(document.getElementById('device'),NodeFilter.SHOW_TEXT);
  while(w.nextNode()){ const n=w.currentNode, t=(n.nodeValue||'').trim(); if(!t) continue; const e=n.parentElement, c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) continue; const rg=document.createRange(); rg.selectNodeContents(n); const r=rg.getBoundingClientRect(); if(r.width<2||r.bottom<D.top||r.top>D.bottom||r.left>D.right||r.right<D.left) continue;
    const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); if(!h||!(h===e||e.contains(h)||h.contains(e))) continue; out.push(t+' @'+Math.round((r.top-D.top)/(D.width/390))); } return out; }"""
def tracer(cdp, pg, P):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': P[0][0], 'y': P[0][1]}]}); pg.wait_for_timeout(120)
    for (x, y) in P[1:]:
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(22)
    pg.wait_for_timeout(120); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.chromium.launch()
    for (lab,sel,x0,x1) in [('Promi à soi','!p.chiche&&(p.who==="moi"||p.who==="Moi")',30,360),('Promi à quelqu\'un','!p.chiche&&p.who&&p.who.toLowerCase()!=="moi"',30,360),('Chiche','!!p.chiche',30,360),('Promi, seconde moitié seule','!p.chiche',195,360)]:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','bande'].forEach(k=>localStorage.setItem('geste_vu_'+k,'1'))}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6000); cdp=ctx.new_cdp_session(pg)
        i=pg.evaluate("()=>{ var p=promises.find(p=>!p.draft&&!p.nuee&&!p.req&&p.status!=='tenu'&&(%s)); if(!p) return null; openDetail(p.id); return [p.id,p.title,p.who,p.status]; }"%sel)
        pg.wait_for_timeout(2200)
        if not i: print(lab,': aucune parole'); ctx.close(); continue
        av=[t for t in pg.evaluate(TXT)]
        P=pg.evaluate(ONDE_FI,[x0,x1]); tracer(cdp,pg,P)
        vus=[]
        for ms in (250,700,700,1200,2500):
            pg.wait_for_timeout(ms); vus.append(pg.evaluate(TXT))
        st=pg.evaluate("(i)=>promises.find(p=>p.id===i).status",i[0])
        print('══',lab,i,'→',st); print('  avant :',av)
        vu=set(av)
        for k,v in enumerate(vus):
            neuf=[t for t in v if t not in vu]; vu|=set(v)
            if neuf: print('  +',['0,25 s','0,95 s','1,65 s','2,85 s','5,35 s'][k],':',neuf)
        print('  à la fin :',vus[-1])
        ctx.close()
    b.close()
