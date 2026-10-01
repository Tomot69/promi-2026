import sys, json
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'app.html'
VP=[(430,932)]+([(375,667)] if '--se' in sys.argv else [])
MES="""()=>{const dv=document.getElementById('device').getBoundingClientRect(),s=dv.width/390,cad=document.querySelector('#auraScreen .au-cadre');
 const Y=v=>(v-dv.top)/s;
 function ink(e){ if(!e) return null; const rg=document.createRange(); rg.selectNodeContents(e); const R=[...rg.getClientRects()].filter(q=>q.width>1&&q.height>1); if(!R.length) return null;
   return {t:Y(Math.min(...R.map(q=>q.top))), b:Y(Math.max(...R.map(q=>q.bottom)))}; }
 function box(q){ const e=cad.querySelector(q); if(!e) return null; const r=e.getBoundingClientRect(); return {t:Y(r.top),b:Y(r.bottom)}; }
 const cv=document.getElementById('auBoule'); let sil=null;
 try{ const t=document.createElement('canvas'); t.width=cv.width; t.height=cv.height; const x=t.getContext('2d'); x.drawImage(cv,0,0); const d=x.getImageData(0,0,cv.width,cv.height).data;
   let top=null,bot=null; const cx=cv.width>>1; for(let y=0;y<cv.height;y++){ let a=0; for(let dx=-6;dx<=6;dx++) a=Math.max(a,d[(y*cv.width+cx+dx)*4+3]); if(a>128){ if(top===null) top=y; bot=y; } }
   const r=cv.getBoundingClientRect(), k=r.height/cv.height; sil={t:Y(r.top+top*k), b:Y(r.top+(bot+1)*k)}; }catch(e){ sil={err:String(e)}; }
 const toi=cad.querySelector('.au-moi .au-lb');
 return {plateau:(()=>{const r=document.querySelector('#auraScreen .enh').getBoundingClientRect();return Y(r.bottom)})(), silhouette:sil, ombre:box('.au-ombre'), mot:ink(cad.querySelector('.au-mot')),
   nx:box('.au-nx'), toi:ink(toi), toiTxt:toi&&toi.textContent, lg:ink(cad.querySelector('.au-lg')), cpt:ink(cad.querySelector('.au-cpt')), bt:box('.au-bt'), fin:box('.au-fin'), scrollH:cad.scrollHeight/ (cad.getBoundingClientRect().height/cad.clientHeight) }}"""
out={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for vw,vh in VP:
        ctx=b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+URL); pg.wait_for_timeout(7000)
        for d in (0,1):
            ouvre(pg,d); pg.wait_for_timeout(2500)
            k='%dx%d-%s'%(vw,vh,'sombre' if d else 'clair'); out[k]=pg.evaluate(MES)
            if '--cap' in sys.argv: pg.screenshot(path='scratchpad/v114/aura-%s.png'%k)
        ctx.close()
    b.close()
print(json.dumps(out,indent=0)[:3000])
json.dump(out,open('scratchpad/v114/aura_cotes.json','w'),indent=1)
