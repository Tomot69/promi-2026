import sys,os; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    r=pg.evaluate("""async ()=>{ const el=document.createElement('div'); el.style.cssText='position:fixed;left:20px;top:200px;width:330px;font:400 25px/1.25 PromiLate;color:#291547;z-index:70'; el.textContent='PRIMO'; document.body.appendChild(el);
      await document.fonts.load('400 25px PromiLate'); window.__D=[]; const pm=Worker.prototype.postMessage; Worker.prototype.postMessage=function(d,t){ if(d&&d.kind==='restes') window.__D.push(structuredClone(d)); return pm.call(this,d,t); }; const C=TraceLettres.trace(el,null,{respecteReduire:false}); await C.pret; await new Promise(r=>setTimeout(r,800));
      const w=TraceLettres._ouvrier; const out={ouvrier: w? 'oui':String(w), attente:Object.keys(TraceLettres._attente), gl:C.glyphes.length};
      // test direct dans un ouvrier neuf
      const src=[...document.scripts].map(s=>s.src).filter(s=>s.includes('trace-lettres'));
      out.src=src;
      const code='importScripts('+JSON.stringify(src[0])+');onmessage=function(e){try{var F=self.TraceLettres._restesCalc(e.data);postMessage({ok:1,n:F.length});}catch(x){postMessage({err:String(x)+" "+(x.stack||"")});}};';
      const w2=new Worker(URL.createObjectURL(new Blob([code],{type:'application/javascript'})));
      out.test=await new Promise(res=>{ w2.onmessage=e=>res(e.data); w2.onerror=e=>res('onerror '+e.message); setTimeout(()=>res('rien'),8000); const t0=performance.now(); out.nD=window.__D.length; if(window.__D.length) w2.postMessage(window.__D[0]); else res('pas de D'); }); out.ms=0;
      return out; }""")
    print(r); b.close()
