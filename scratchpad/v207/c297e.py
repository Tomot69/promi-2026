import sys, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src=open('scratchpad/v207/c297b.py').read(); exec(src.split('with sync_playwright()')[0])
PIEGE="""()=>{ window.__PD=[]; const o=Event.prototype.preventDefault; Event.prototype.preventDefault=function(){ if(/^touch|^pointer|wheel|scroll/.test(this.type)) window.__PD.push(this.type+' | '+(new Error().stack||'').split('\\n').slice(1,4).join(' / ')); return o.apply(this,arguments); };
  const d=document.getElementById('detailPoster'); window.__S=[]; d.addEventListener('scroll',()=>window.__S.push(Math.round(d.scrollTop)),{passive:true});
  const ds=Object.getOwnPropertyDescriptor(Element.prototype,'scrollTop'); Object.defineProperty(d,'scrollTop',{get(){return ds.get.call(this);}, set(v){ if(v!==ds.get.call(this)) window.__PD.push('scrollTop='+v+' | '+(new Error().stack||'').split('\\n').slice(1,4).join(' / ')); ds.set.call(this,v);}, configurable:true}); }"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--touch-events=enabled'])
    ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F); cdp=ctx.new_cdp_session(pg)
    pg.evaluate("()=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); }"%MOTS)
    pg.wait_for_timeout(3000); d=B.dev(pg)
    z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
    B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380); pg.evaluate(PIEGE); pg.wait_for_timeout(500)
    geste(pg,cdp,d,560,260); pg.wait_for_timeout(300)
    print('scroll', pg.evaluate("()=>window.__S")[:40]); 
    for x in pg.evaluate("()=>window.__PD")[:12]: print('  ',x[:300])
    b.close()
