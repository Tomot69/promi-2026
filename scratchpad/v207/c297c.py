import sys, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html')
exec(open('scratchpad/v207/c297b.py').read().split('with sync_playwright()')[0].split("F=os.environ")[0])
src=open('scratchpad/v207/c297b.py').read(); pre=src.split('with sync_playwright()')[0]; exec(pre)
for att in (600, 1500, 2500, 3500):
  with sync_playwright() as p:
    b=p.chromium.launch(args=['--touch-events=enabled'])
    ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F); cdp=ctx.new_cdp_session(pg)
    pid=pg.evaluate("()=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); return p.id; }"%MOTS)
    pg.wait_for_timeout(3000); d=B.dev(pg)
    z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
    B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380); pg.wait_for_timeout(att)
    pg.evaluate(REC); geste(pg,cdp,d,560,260); geste(pg,cdp,d,400,-420); pg.wait_for_timeout(2500)
    Fr=pg.evaluate("()=>window.__F")
    ec=[(f[0], None if f[1] is None else round(f[1]+f[0],1), f[2], None if f[3] is None else round(f[3]+f[0],1), f[4]) for f in Fr]
    sv=[x[0] for x in ec]; 
    print('attente %d ms · s max %.0f fin %.0f · colle+s valeurs %s · trame+s %s · base %s · inst %s'%(att, max(sv), sv[-1], sorted(set(x[1] for x in ec))[:8], sorted(set(x[3] for x in ec))[:6], sorted(set(str(x[2]) for x in ec)), pg.evaluate("()=>window._instant")))
    b.close()
