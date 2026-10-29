import sys,os; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:200])); pg.on('console', lambda m: er.append('C:'+m.text[:200]) if m.type=='error' else None)
    pg.goto('http://127.0.0.1:8752/app.html'+os.environ.get('Q','')); pg.wait_for_timeout(6500)
    for txt,fam in (('Camille, donc. Quid d’un Promi','Atkinson'),('PRIMO DEUXIO','PromiLate')):
        r=pg.evaluate("""async a=>{ const [t,f]=a; const el=document.createElement('div'); el.style.cssText='position:fixed;left:20px;top:200px;width:330px;font:500 25px/1.25 '+f+';color:#291547;z-index:70'; el.textContent=t; document.body.appendChild(el);
          await document.fonts.load('500 25px '+f); const t0=performance.now(); const C=TraceLettres.trace(el,null,{respecteReduire:false}); await C.pret; const s=[]; for(let i=0;i<8;i++){ await new Promise(r=>setTimeout(r,150)); s.push(JSON.stringify(C.etat())); } const fin=await Promise.race([C.fin.then(()=>'fin'), new Promise(r=>setTimeout(()=>r('timeout'),4000))]); el.remove(); return [s, fin, Math.round(performance.now()-t0), C.duree]; }""",[txt,fam])
        print(fam, r[1], r[2], 'duree', r[3]); print('  ', r[0][0], r[0][-1])
    print(er[:5]); b.close()
