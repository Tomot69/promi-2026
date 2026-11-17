import sys, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src=open('scratchpad/v207/c297b.py').read(); exec(src.split('with sync_playwright()')[0])
with sync_playwright() as p:
    b=p.chromium.launch(args=['--touch-events=enabled'])
    ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F)
    pg.evaluate("()=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); }"%MOTS)
    pg.wait_for_timeout(3000); d=B.dev(pg)
    z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
    B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380)
    for t in (300,900,1500,2100,2700,3300):
        pg.wait_for_timeout(300 if t>300 else 300)
        r=pg.evaluate("""(k)=>{ const D=document.getElementById('device').getBoundingClientRect(), s=D.width/390, dp=document.getElementById('detailPoster'), c=getComputedStyle(dp);
          const pts=[[300,560],[300,300],[100,700]].map(([x,y])=>{ const e=document.elementFromPoint(D.left+x*s, D.top+y*s); return e?(e.tagName+'#'+e.id+'.'+String(e.className).slice(0,40)+' pe:'+getComputedStyle(e).pointerEvents+' ta:'+getComputedStyle(e).touchAction):null; });
          return {ov:c.overflowY, ta:c.touchAction, h:dp.scrollHeight, ch:dp.clientHeight, anime:!!window._tenirAnime, inst:window._instant, cls:dp.className.split(' ').filter(x=>/tenir|maree|anim|instant|bloq|fige|v18|v19/.test(x)).join(' '), pts:pts, body:getComputedStyle(document.body).overflow}; }""")
        print(t, r)
    b.close()
