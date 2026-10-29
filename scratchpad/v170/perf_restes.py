import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    import os
    for m in [x for x in os.environ.get('ADD','').split(',') if x]: pg.add_script_tag(url='http://127.0.0.1:8752/'+m); pg.wait_for_timeout(300)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }")
    for txt,fz in (('LE RESTE S’EXPLORE À TON RYTHME',29),('PROMI',52),('TRACE POUR PLANTER',19)):
        r=pg.evaluate("""async a=>{ const [t,fz]=a; const el=document.createElement('div'); el.style.cssText='position:fixed;left:20px;top:200px;width:330px;font:400 '+fz+'px/1.25 PromiLate;color:#291547;z-index:70'; el.textContent=t; document.body.appendChild(el);
          await document.fonts.load('400 '+fz+'px PromiLate'); const lt=[]; const po=new PerformanceObserver(l=>l.getEntries().forEach(e=>lt.push(Math.round(e.duration)))); try{po.observe({entryTypes:['longtask']});}catch(e){}
          let mx=0, last=performance.now(), on=true; (function f(){ const n=performance.now(); mx=Math.max(mx,n-last); last=n; if(on) requestAnimationFrame(f); })();
          const t0=performance.now(); const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); const t1=performance.now(); await C.pret; const t2=performance.now(); await new Promise(r=>setTimeout(r,300)); on=false; el.remove(); const pr=TraceLettres._prof; TraceLettres._prof={}; return [Math.round(t1-t0), Math.round(t2-t0), Math.round(mx), JSON.stringify(pr, (k,v)=>typeof v==='number'?Math.round(v):v)]; }""",[txt,fz])
        print(txt,fz,'sync ms',r[0],'pret ms',r[1],'maxframe',r[2], r[3] if len(r)>3 else '')
    b.close()
