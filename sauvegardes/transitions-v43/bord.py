# Les cinq mondes neufs : une dalle qui arrive AU BORD. On plante plusieurs fois ; pour chaque arrivée, on relève par image
# l'écart MAXIMAL sur des carrés de 12 px (pas la moyenne, qui noie un défaut local), et on repère les pics (saut local).
import sys, json
from playwright.sync_api import sync_playwright
MONDES=sys.argv[1:] or ['halin','esquille','bobinette','ritournelle','madrure']
JS=r"""async (a)=>{ const cv=document.getElementById('toileCv'); const S=4, w=Math.round(cv.width/S), h=Math.round(cv.height/S);
 const c=document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
 function img(){ x.drawImage(cv,0,0,w,h); return x.getImageData(0,0,w,h).data; }
 const B=6, bw=Math.ceil(w/B), bh=Math.ceil(h/B);
 const res=[];
 for(let n=0;n<a.n;n++){
  const id=9000+n+Math.floor(Math.random()*500); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null}));
  let prev=img(); Toile.addPromi(id); const t0=performance.now(); const L=[];
  await new Promise(r=>{ function f(){ const e=performance.now()-t0; const cur=img(); const blk=new Float32Array(bw*bh);
     for(let yy=0;yy<h;yy++) for(let xx=0;xx<w;xx++){ const i=(yy*w+xx)*4; blk[((yy/B)|0)*bw+((xx/B)|0)]+=Math.abs(cur[i]-prev[i])+Math.abs(cur[i+1]-prev[i+1])+Math.abs(cur[i+2]-prev[i+2]); }
     let m=0,mi=0; for(let k=0;k<blk.length;k++){ if(blk[k]>m){m=blk[k];mi=k;} }
     L.push([Math.round(e), +(m/(B*B*3)).toFixed(1), (mi%bw)*B*S, ((mi/bw)|0)*B*S]); prev=cur; if(e<a.dur) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  const D=Toile.dalleAbs(id), V=Toile.vue(), Wt=cv.width/V.dpr, Ht=cv.height/V.dpr;
  let bord=null; if(D){ const x0=D.minx*V.s+V.ox, y0=D.miny*V.s+V.oy, x1=x0+D.w*V.s, y1=y0+D.h*V.s; bord=[Math.round(x0),Math.round(y0),Math.round(x1),Math.round(y1), (x0<4||y0<4||x1>Wt-4||y1>Ht-4)]; }
  res.push({bord:bord, L:L});
  promises.pop(); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id)); await new Promise(r=>setTimeout(r,2200));
 }
 return res; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    out={}
    for m in MONDES:
        pg.evaluate("m=>Toile.setTheme(m)",m); pg.wait_for_timeout(3000)
        R=pg.evaluate(JS,{'n':4,'dur':2400}); out[m]=R
        for r in R:
            v=[q[1] for q in r['L']]
            pics=[]
            for i in range(1,len(v)-1):
                voisins=sorted(v[max(0,i-4):i]+v[i+1:i+5]); med=voisins[len(voisins)//2]
                if v[i]>25 and v[i]>3*max(med,3): pics.append(tuple(r['L'][i]))
            print(m,'bord' if (r['bord'] and r['bord'][4]) else 'dedans', r['bord'][:4] if r['bord'] else None,'| pics',pics[:6])
    json.dump(out,open('bord.json','w'))
    b.close()
