# instrument : chaque dalle rendue SEULE par le moteur, à horloge figée et hasard réamorcé, synchrone — seule, et en bande haute (rampe Q30)
import sys, json
from playwright.sync_api import sync_playwright
JS = r"""(th)=>{ const R={}; const out=[];
  for(const p of promises.filter(q=>!q.draft)){
    const nat=p.chiche?'chiche':(p.nuee?'nuee':'promi');
    for(const mode of ['seule','bande']){
      const mr=Math.random; let s=777; Math.random=function(){ s=(s*1664525+1013904223)%4294967296; return s/4294967296; };
      window.__tFige=86400000; const cv=document.createElement('canvas'); let ok=false;
      try{ ok=!!Toile.dalleTrame(cv, p.id, 2, undefined, mode==='bande'&&window._ppRampe?{rampe:window._ppRampe(nat)}:undefined); }catch(e){ ok='err '+e; }
      Math.random=mr; window.__tFige=null;
      if(!cv.width) { R[p.title+'|'+mode]={ok:ok}; continue; }
      const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, h={}; let n=0;
      for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const q=(d[i]<<16)|(d[i+1]<<8)|d[i+2]; h[q]=(h[q]||0)+1; }
      R[p.title+'|'+mode]={ok:ok, n:n, w:cv.width, h:cv.height, dom:Object.keys(h).map(q=>[+q,h[q]/n]).filter(a=>a[1]>=0.02).sort((a,b)=>b[1]-a[1]).slice(0,8).map(a=>[(a[0]>>16)&255,(a[0]>>8)&255,a[0]&255,+a[1].toFixed(3)])};
    } }
  return R; }"""
def releve(url):
    with sync_playwright() as p:
        b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');Math.random=(function(){var s=20261002;return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;};})();window.__tFige=null;var _pn=performance.now.bind(performance);performance.now=function(){return window.__tFige!=null?window.__tFige:_pn();};}catch(e){}")
        pg=ctx.new_page(); pg.goto(url); pg.wait_for_timeout(6800); R={}
        for th in ('light','dark'):
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(800)
            for k,v in pg.evaluate(JS,th).items(): R[k+'|'+th]=v
        b.close(); return R
if __name__=='__main__':
    A=releve(sys.argv[1]); B=releve(sys.argv[2])
    import math
    def lab(c):
        def lin(v): v/=255.0; return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
        r,g,b=lin(c[0]),lin(c[1]),lin(c[2]); x=(0.4124564*r+0.3575761*g+0.1804375*b)/0.95047; y=0.2126729*r+0.7151522*g+0.0721750*b; z=(0.0193339*r+0.1191920*g+0.9503041*b)/1.08883
        f=lambda v: v**(1/3) if v>0.008856 else 7.787*v+16/116; return (116*f(y)-16,500*(f(x)-f(y)),200*(f(y)-f(z)))
    def dE(a,b): A_,B_=lab(a),lab(b); return math.sqrt(sum((A_[i]-B_[i])**2 for i in range(3)))
    n=0; e=0
    for k in sorted(A):
        a,r=A[k],B.get(k)
        if not r or 'dom' not in a or 'dom' not in r: print('?',k,a.get('ok'),r and r.get('ok')); continue
        for col in a['dom']:
            n+=1; m=min(dE(col[:3],x[:3]) for x in r['dom'])
            if m>2.0: e+=1; print('✗ %-40s rgb%s %.0f%%  au plus près ΔE %.1f' % (k, tuple(col[:3]), 100*col[3], m))
    print('%d couleurs comparées, %d écarts'%(n,e))
