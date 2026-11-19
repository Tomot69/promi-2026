# C-297, au vrai doigt (Chromium, Input.synthesizeScrollGesture tactile) : défiler en posant le doigt SUR le trait, puis ailleurs ; avant « tenir », juste après, et rouverte.
import sys, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html'); NAT=os.environ.get('NAT','promi')
MOTS="Array.from({length:6},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true}))"
ZONE="(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
def st(pg): return pg.evaluate("()=>Math.round(document.getElementById('detailPoster').scrollTop)")
def geste(pg, cdp, d, y, dy):
    k=d[4]; cdp.send('Input.synthesizeScrollGesture',{'x':d[0]+300*k,'y':d[1]+y*k,'yDistance':-dy*k,'gestureSourceType':'touch','speed':600,'preventFling':True}); pg.wait_for_timeout(900)
REC="""()=>{ window.__F=[]; const d=document.getElementById('detailPoster'), D=document.getElementById('device'); (function f(){ const c=document.getElementById('v192Colle'), R=D.getBoundingClientRect(), k=R.width/390, J=window._v189Jonction&&_v189Jonction();
  const cv=document.getElementById('dpTrameCv'), rc=cv&&cv.getBoundingClientRect(); window.__F.push([Math.round(d.scrollTop*10)/10, c?Math.round((c.getBoundingClientRect().top-R.top)/k*10)/10:null, J&&J.F?J.F.base:null, rc?Math.round((rc.top-R.top)/k*10)/10:null, d.className.indexOf('f-tenue')>=0?1:0]); if(window.__F.length<400) requestAnimationFrame(f); })(); }"""
def suivi(pg, cdp, d, nom):
    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(600)
    pg.evaluate(REC); geste(pg,cdp,d,560,260); geste(pg,cdp,d,400,-420); pg.wait_for_timeout(500)
    Fr=pg.evaluate("()=>window.__F"); ec=[(f[0], round(f[1]+f[0],1), f[2], round(f[3]+f[0],1)) for f in Fr if f[1] is not None and f[3] is not None]
    c0=ec[0][1]; t0=ec[0][3]; mauv=[x for x in ec if abs(x[1]-c0)>0.6 or abs(x[3]-t0)>0.6]
    print('  %-10s images %d · fin s %s · colle+s (doit rester %.1f) écarts %d · trame+s (doit rester %.1f) écarts %d %s'%(nom,len(ec),Fr[-1][0],c0,sum(1 for x in ec if abs(x[1]-c0)>0.6),t0,sum(1 for x in ec if abs(x[3]-t0)>0.6), mauv[:6]))
def essai(pg, cdp, d, nom):
    suivi(pg, cdp, d, nom)
    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(600)
    J=pg.evaluate("()=>{ const f=_v189Jonction().F; return f?f.base:null; }")
    out=[]
    for y,lab in ((J or 290,'sur le trait'),(620,'plus bas')):
        pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(500)
        s0=st(pg); geste(pg,cdp,d,y,200); s1=st(pg); geste(pg,cdp,d,y-100 if y>300 else 400,-200); s2=st(pg)
        out.append('%s (y %d) : bas %d→%d, haut →%d'%(lab,y,s0,s1,s2))
    z=pg.evaluate("()=>{ const z=document.getElementById('tenirZone'); if(!z) return null; const c=getComputedStyle(z); return [c.pointerEvents,c.touchAction,c.display,c.visibility]; }")
    print('  %-10s base %s · zone %s · %s'%(nom,J,z,' · '.join(out)))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--touch-events=enabled'])
    ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F); cdp=ctx.new_cdp_session(pg)
    pid=pg.evaluate("n=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); if(n==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); return p.id; }"%MOTS, NAT)
    pg.wait_for_timeout(3000); d=B.dev(pg)
    essai(pg,cdp,d,'avant')
    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(800)
    z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
    B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380); pg.wait_for_timeout(5000)
    print('  statut', pg.evaluate("id=>promises.find(x=>x.id===id).status", pid))
    essai(pg,cdp,d,'tenue')
    pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} closeAll(); }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(3000)
    essai(pg,cdp,d,'témoin')
    print('  erreurs', pg.erreurs[:3]); b.close()
