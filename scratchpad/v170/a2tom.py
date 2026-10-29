"""A2 — l'état exporté de Tom (contexte_tom, sa fenêtre 390 × 651), le guide rejoué : la phrase du Studio (PromiLate « Studio », « monde ») tracée
en temps réel, puis un texte PromiLate posé à la main ; chaque tracé se termine, la dernière image est le texte (comparé au texte sans tracé)."""
import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.webkit.launch(); ctx,d=B.contexte_tom(b,'etats/tom-20261023-125022.json'); print('état', d['_fichier'], d.get('ecran'))
    pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html', timeout=300000); pg.wait_for_timeout(9000)
    n=pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('promi_state')||'{}').promises.length}catch(e){return -1}}"); print('paroles relues', n)
    for txt in ('PRIMO DEUXIO TERTIO','LA SUITE T’APPARTIENT.'):
        r=pg.evaluate("""async t=>{ const el=document.createElement('div'); el.style.cssText='position:fixed;left:20px;top:180px;width:330px;font:400 32px/1.3 PromiLate;color:#0E78F2;z-index:70'; el.textContent=t; document.body.appendChild(el);
          await document.fonts.load('400 32px PromiLate'); const t0=performance.now(); const C=TraceLettres.trace(el,null,{respecteReduire:false}); await C.pret;
          const fin=await Promise.race([C.fin.then(()=>'fin'), new Promise(r=>setTimeout(()=>r('timeout'),15000))]);
          await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
          const cp=getComputedStyle(el).clipPath; const res=[fin, Math.round(performance.now()-t0), cp, el.querySelectorAll('canvas').length]; el.remove(); return res; }""", txt)
        print(txt, '→', r)
    pg.evaluate("()=>{ try{ _guide.finir&&_guide.finir(); }catch(e){} _guide.montre('studio', true); }"); pg.wait_for_timeout(300)
    for _ in range(80):
        if pg.evaluate("()=>!!document.querySelector('#guidePhrase .gd-studio')"): break
        pg.wait_for_timeout(150)
    pg.wait_for_timeout(4000)
    g=pg.evaluate("()=>{const p=document.getElementById('guidePhrase'); return p?[p.textContent.trim(), getComputedStyle(p).clipPath, [...p.querySelectorAll('*')].filter(e=>getComputedStyle(e).clipPath!=='none').length]:null}")
    print('phrase du Studio', g); pg.screenshot(path='scratchpad/v170/a2tom.png')
    print('erreurs', [x for x in er if 'version.json' not in x][:5]); b.close()
