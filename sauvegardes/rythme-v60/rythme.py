# Le rythme des animations de monde, dans trois conditions :
#   page  : celebration-mondes.html (la page où Tom a validé) — la vraie app dans un cadre, appel direct au moteur
#   app   : app.html, même appel direct
#   reel  : app.html, arrivée par le VRAI chemin — la page + et le tracé au doigt (impression, closeAll, passes)
# Par monde, arrivée et départ : durée du mouvement (dernière image où la Toile change encore), nombre d'images, pire image.
# python3 rythme.py [--webkit] [--mondes=a,b] [--app=fichier] [--sans-reel] → rythme-<moteur>.json
import sys, json, statistics as st
from playwright.sync_api import sync_playwright
WK='--webkit' in sys.argv
MONDES=(next((a.split('=')[1] for a in sys.argv if a.startswith('--mondes=')),None) or 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons').split(',')
PAGE=next((a.split('=')[1] for a in sys.argv if a.startswith('--page=')),'celebration-mondes.html')
APP=next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')),'app.html')
ENREG=r"""(a)=>{ const W=window; W.__R=[]; W.__T0=null; W.__fin=false; const gen=W.__gen=(W.__gen||0)+1;
  if(!W.__envAdd){ W.__envAdd=1; const f=W.Toile.addPromi; W.Toile.addPromi=function(){ if(W.__T0==null) W.__T0=performance.now(); let s=12345; W.Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; return f.apply(this,arguments); };   /* même tirage de place dans les trois conditions */
    const g=W.Toile.sync; W.Toile.sync=function(){ if(W.__arme==='sync'&&W.__T0==null) W.__T0=performance.now(); return g.apply(this,arguments); }; }
  const cv=W.document.getElementById('toileCv'), w=Math.round(cv.width/4), h=Math.round(cv.height/4);
  const c=W.document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
  function img(){ x.drawImage(cv,0,0,w,h); return x.getImageData(0,0,w,h).data; }
  W.__tp=0; let prev=img(); const B=8, bw=Math.ceil(w/B), bh=Math.ceil(h/B);
  (function f(){ if(W.__fin||W.__gen!==gen) return; const cur=img(); const acc=new Float32Array(bw*bh);
    for(let y=0;y<h;y++) for(let xx=0;xx<w;xx++){ const i=(y*w+xx)*4; acc[((y/B)|0)*bw+((xx/B)|0)]+=Math.abs(cur[i]-prev[i])+Math.abs(cur[i+1]-prev[i+1])+Math.abs(cur[i+2]-prev[i+2]); }
    let m=0; for(const a of acc) if(a>m) m=a; const tn=performance.now(), dt=W.__tp?tn-W.__tp:16.667; W.__tp=tn; W.__R.push([tn, m/(B*B*3)*16.667/Math.max(8,dt)]); prev=cur; W.requestAnimationFrame(f); })(); }"""
LIT=r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; if(T0==null) return null;
  const R=W.__R.filter(r=>r[0]>=T0).map(r=>[r[0]-T0,r[1]]); let fin=0; for(const r of R) if(r[1]>0.5) fin=r[0];
  const F=R.filter(r=>r[0]<=fin+1); const d=[]; for(let i=1;i<F.length;i++) d.push(F[i][0]-F[i-1][0]);
  d.sort((a,b)=>a-b); return {duree:Math.round(fin), images:F.length, mediane:d.length?+d[d.length>>1].toFixed(1):0, pire:d.length?Math.round(d[d.length-1]):0}; }"""
def mesure(ctx_eval, W_eval, pg, monde, cond):
    out={}
    W_eval("m=>{ let s=777; window.Math.random=function(){ s=(s*1103515245+12345)&0x7fffffff; return s/0x7fffffff; }; window.Toile.setTheme(m); }", monde); pg.wait_for_timeout(3000)
    # arrivée
    W_eval(ENREG, None); W_eval("()=>{ window.__arme='add'; }", None)
    if cond=='reel':
        pg.mouse.click(*pg.evaluate("()=>{const r=document.getElementById('createBtn').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(600)
        pg.mouse.click(*pg.evaluate("()=>{const r=document.querySelector('#accChoix .acc-pil[data-k=promi]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const t=document.getElementById('fTitle'); t.value='mesure du rythme'; t.dispatchEvent(new Event('input',{bubbles:true})); }")
        W_eval(ENREG, None)
        z=pg.evaluate("()=>{ const r=document.getElementById('planterZone').getBoundingClientRect(); return [r.left, r.top+r.height/2, r.width]; }")
        pg.mouse.move(z[0]+12,z[1]); pg.mouse.down()
        for i in range(1,26): pg.mouse.move(z[0]+12+(z[2]-24)*i/25, z[1]); pg.wait_for_timeout(12)
        pg.mouse.up(); pg.wait_for_timeout(4200)
    else:
        W_eval("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); window.Toile.addPromi(97001); }", None)
        pg.wait_for_timeout(3500)
    out['arrivee']=W_eval(LIT, None); pg.wait_for_timeout(1500)
    # départ : la même parole retirée (sync, comme une suppression)
    W_eval(ENREG, None); W_eval("()=>{ window.__arme='sync'; }", None)
    if cond=='reel':   # le vrai chemin : la fiche, puis « Supprimer » deux fois (confirmation)
        pg.evaluate("()=>{ const p=promises.find(p=>p.title==='mesure du rythme'); openDetail(p.id); }"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ window._v16SupprimerPromi(cur); }"); pg.wait_for_timeout(700)
        W_eval(ENREG, None); W_eval("()=>{ window.__arme='sync'; }", None)
        xy=pg.evaluate("()=>{ const b=document.querySelector('#v16Conf .v16-oui'); const r=b.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        pg.mouse.click(*xy)
    else:
        W_eval("()=>{ const P=window.eval('promises'); const i=P.findIndex(p=>p.title==='mesure du rythme'); if(i>=0) P.splice(i,1); window.Toile.sync(P.filter(p=>!p.draft).map(p=>p.id)); }", None)
    pg.wait_for_timeout(3500)
    out['depart']=W_eval(LIT, None); W_eval("()=>{ window.__arme=null; }", None); pg.wait_for_timeout(1500)
    return out
res={}
with sync_playwright() as p:
    b=p.webkit.launch() if WK else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])   # v61 : le vrai GPU (sans lui, Madrure prend son chemin de secours)
    for cond in (['page','app'] + ([] if '--sans-reel' in sys.argv else ['reel'])):
        pg=b.new_page(viewport={'width':1100,'height':950} if cond=='page' else {'width':430,'height':932}, device_scale_factor=2)
        if cond=='page':
            pg.goto('http://127.0.0.1:8752/'+PAGE); pg.wait_for_timeout(9000)
            pg.evaluate("()=>{ window.tour=function(){}; }"); pg.wait_for_timeout(5000)   # on arrête la boucle de la page
            fr=pg.frames[1]; W_eval=lambda js,a: fr.evaluate(js,a)
        else:
            pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(9000)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}")
            pg.wait_for_timeout(1500); W_eval=lambda js,a: pg.evaluate(js,a)
        for m in MONDES:
            r=mesure(None, W_eval, pg, m, cond); res.setdefault(m,{})[cond]=r
            print(cond, m, json.dumps(r), flush=True)
            if cond=='reel': pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(600)
        pg.close()
    b.close()
json.dump(res, open(next((a.split('=')[1] for a in sys.argv if a.startswith('--sortie=')),'rythme-%s.json'%('webkit' if WK else 'chromium')),'w'), indent=1)
