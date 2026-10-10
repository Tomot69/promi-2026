# le chemin de Tom : stockage vierge, onboarding, une parole ; puis Ritournelle ; rechargement
import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from redteam_onboarding import POIGNEE, toucher, tracer, PRENOM, PAROLE
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'; monde=sys.argv[2] if len(sys.argv)>2 else 'ritournelle'; pre=sys.argv[3] if len(sys.argv)>3 else 'rito2'
VU="()=>{ const o=document.getElementById('promiOnb'); if(!o) return false; const c=getComputedStyle(o); return !o.classList.contains('gone') && c.display!=='none'; }"
HIT=r"""()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(); const kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height; const G={};
  for(let y=dv.top+4;y<dv.bottom-4;y+=6) for(let x=dv.left+4;x<dv.right-4;x+=6){ let h=null; try{h=Toile.hit((x-r.left)*kx,(y-r.top)*ky);}catch(e){} if(h&&h.pid!=null){ const g=G[h.pid]=G[h.pid]||{n:0,x0:1e9,y0:1e9,x1:-1e9,y1:-1e9}; g.n++; g.x0=Math.min(g.x0,x-dv.left); g.x1=Math.max(g.x1,x-dv.left); g.y0=Math.min(g.y0,y-dv.top); g.y1=Math.max(g.y1,y-dv.top);} }
  return {G:Object.keys(G).map(k=>{const p=promises.find(q=>q.id==k); return [(p?p.title:k), G[k].n, Math.round(G[k].x0), Math.round(G[k].y0), Math.round(G[k].x1), Math.round(G[k].y1)]}), vue:(Toile.vue?Toile.vue():null), n:promises.length, gr:Toile.graines&&Toile.graines(), th:Toile.getTheme()}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6800)
    pr=pg.evaluate(POIGNEE,'[data-onb="prenom"]'); toucher(cdp,pr['x'],pr['y']); pg.wait_for_timeout(300); pg.keyboard.type(PRENOM,delay=30); pg.wait_for_timeout(200)
    s=pg.evaluate(POIGNEE,'[data-onb="suite"]')
    if s: toucher(cdp,s['x'],s['y'])
    else: pg.keyboard.press('Enter')
    pg.wait_for_timeout(1400)
    q=pg.evaluate(POIGNEE,'[data-onb="parole"]'); toucher(cdp,q['x'],q['y']); pg.wait_for_timeout(300); pg.keyboard.type(PAROLE,delay=25); pg.wait_for_timeout(600)
    z=pg.evaluate(POIGNEE,'[data-onb="trait"]'); tracer(cdp,z); pg.wait_for_timeout(6600)
    dd=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height*0.45}}")
    for _ in range(14):
        pt=pg.evaluate(POIGNEE,'[data-onb="plus-tard"]')
        if pt: toucher(cdp,pt['x'],pt['y']); pg.wait_for_timeout(1200); break
        if not pg.evaluate(VU): break
        if pg.evaluate("()=>{const f=document.getElementById('onbFin'); return !!f && getComputedStyle(f).display!=='none' && +getComputedStyle(f).opacity>0.5;}"): toucher(cdp,dd['x'],dd['y'])
        pg.wait_for_timeout(900)
    pg.wait_for_timeout(2500)
    def cap(nom):
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='planche-v139/%s-%s.png'%(pre,nom),clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); o=pg.evaluate(HIT); print(nom,{k:o[k] for k in ('vue','n','gr','th')}); [print('   ',g) for g in o['G']]; return r,o
    cap('0-apres-onboarding')
    pg.evaluate("(m)=>{ try{setPremium(true)}catch(e){} try{localStorage.setItem('geste_vu_tenir','1')}catch(e){} Toile.setTheme(m); }",monde); pg.wait_for_timeout(3500)
    cap('1-monde')
    pg.reload(); pg.wait_for_timeout(7000)
    r,o=cap('2-recharge')
    # au doigt, au centre de la boîte que le toucher reconnaît
    for g in o['G'][:1]:
        x=r[0]+(g[2]+g[4])/2; y=r[1]+(g[3]+g[5])/2
        print('dessus:',pg.evaluate("([x,y])=>{const h=document.elementFromPoint(x,y); return h?(h.id||h.className||h.tagName):null}",[x,y]))
        toucher(cdp,x,y); pg.wait_for_timeout(1800)
        print('fiche ouverte :',pg.evaluate("()=>{const dp=document.getElementById('detailPoster'), t=document.getElementById('dptTitre'); return [!!(dp&&dp.classList.contains('show')), t?t.textContent.trim():'']}"))
    b.close()
