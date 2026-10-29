import sys, json; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx, d = B.contexte_tom(b, 'etats/tom-20261023-125022.json')
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(1500)
    for q in ('studio', 'plus', 'partage', 'reste'):
        r = pg.evaluate("""async q=>{ const T=TraceLettres; const i0=T.mesures.image.length, a0=T.mesures.appl.length, r0=T.mesures.restes.length;
          const F=[]; let t=performance.now(), run=true; (function f(n){ F.push(n-t); t=n; if(run) requestAnimationFrame(f); })(t);
          try{ _guide.finir&&_guide.finir(); }catch(e){} _guide.montre(q);
          await new Promise(r=>setTimeout(r,4500)); run=false;
          const im=T.mesures.image.slice(i0), ap=T.mesures.appl.slice(a0), rs=T.mesures.restes.slice(r0);
          const s=a=>a.slice().sort((x,y)=>x-y); const p=(a,k)=>{a=s(a); return a.length?+a[Math.min(a.length-1,Math.floor(k*a.length))].toFixed(1):null;};
          return {images:F.length, sup20:F.filter(x=>x>20).length, pire:+Math.max(...F).toFixed(0), jsP95:p(im,.95), jsMax:p(im,1), applBuildMax:p(ap.map(x=>x[0]),1), applPoseMax:p(ap.map(x=>x[1]),1), pathMax:Math.max(0,...ap.map(x=>x[2])), restesFil:rs.length, restesMax:p(rs.map(x=>x[2]),1), ouvrier:T.ouvrierEtat, journal:T.journal.slice(-6).map(e=>[e.quoi,e.texte||e.car||'',e.prevu||e.ms||'',e.reel||''])}; }""", q)
        print(q, json.dumps(r, ensure_ascii=False), flush=True)
    b.close()
print('charge', B.charge())
