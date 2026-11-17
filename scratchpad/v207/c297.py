# C-297 : après « tenir », le trait ne suit plus le défilement vers le haut et la dalle bugue. On tient au doigt, puis molette bas/haut ; on compare à la même
# fiche tenue, rouverte (témoin), aux mêmes défilements.
import sys, io, os; sys.path.insert(0,'.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html')
NAT=os.environ.get('NAT','promi')
MOTS="Array.from({length:6},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true}))"
ZONE="(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
INFO="""()=>{ const d=document.getElementById('detailPoster'), c=document.getElementById('v192Colle'), J=window._v189Jonction&&_v189Jonction(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const r=c&&c.getBoundingClientRect(), pl=document.getElementById('v195Plat'), rp=pl&&pl.getBoundingClientRect(), fe=document.getElementById('v200Fenetre'), rf=fe&&fe.getBoundingClientRect();
  return {s:Math.round(d.scrollTop*10)/10, colle: r?Math.round((r.top-D.top)/k*10)/10:null, plat: rp?Math.round((rp.top-D.top)/k*10)/10:null, fen: rf?[Math.round((rf.top-D.top)/k),Math.round(rf.height/k)]:null, cls:d.className.split(' ').filter(x=>/v18|v19|v20|tenu|tracant|instant|pose/.test(x)).join(' '), F:J&&J.F?{min:J.F.min,max:J.F.max,base:J.F.base}:null, h:d.scrollHeight}; }"""
def zone(pg, d):
    k=d[4]; png=pg.screenshot(clip={'x':d[0],'y':d[1]+60*k,'width':390*k,'height':330*k}); return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def roule(pg, d, dy, pas=6, ms=16):
    pg.mouse.move(d[0]+195*d[4], d[1]+600*d[4]); n=max(1,int(abs(dy)/pas)); s=dy/n
    for _ in range(n): pg.mouse.wheel(0,s); pg.wait_for_timeout(ms)
def pose(pg):
    av=None
    for _ in range(12):
        pg.wait_for_timeout(300); s=pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
        if av is not None and abs(s-av)<0.1: return s
        av=s
    return av
def parcours(pg, d, nom, out):
    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(500)
    for etape,dy in (('haut',0),('bas 120',120),('bas 300',180),('haut -300',-400)):
        if dy: roule(pg,d,dy); pose(pg); pg.wait_for_timeout(400)
        i=pg.evaluate(INFO); im=zone(pg,d); out[(nom,etape)]=(i,im); print('  %-8s %-10s %s'%(nom,etape,i))
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F)
    pid=pg.evaluate("n=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche&&(!x.who||x.who==='moi'||x.who==='Moi')) || promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); if(n==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); return p.id; }"%MOTS, NAT)
    pg.wait_for_timeout(3000); d=B.dev(pg); out={}
    parcours(pg,d,'avant',out)
    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(800)
    z=pg.evaluate(ZONE,'tenirZone'); y=z[1]+z[3]*0.45
    B.glisse(pg,[[200+150*i/10,y] for i in range(11)],pas=30,tenue=380); pg.wait_for_timeout(5000)
    print('  statut', pg.evaluate("id=>promises.find(x=>x.id===id).status", pid))
    parcours(pg,d,'tenue',out)
    pg.evaluate("id=>{ try{_peaufSortie()}catch(e){} closeAll(); }", pid); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(3000)
    parcours(pg,d,'témoin',out)
    for e in ('haut','bas 120','bas 300','haut -300'):
        a=out[('tenue',e)][1]; t=out[('témoin',e)][1]; diff=np.abs(a-t).max(axis=2); nb=int((diff>24).sum())
        print('  tenue vs témoin %-10s pixels écartés %d'%(e,nb))
        Image.fromarray(np.concatenate([a,t],axis=1).astype(np.uint8)).save('scratchpad/v207/c297_%s_%s.png'%(NAT,e.replace(' ','')))
    print('  erreurs', pg.erreurs[:3])
    b.close()
