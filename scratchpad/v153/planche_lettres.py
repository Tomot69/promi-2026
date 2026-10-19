# planche : chaque lettre à 8 instants (rouge sombre = pas encore tracé, vert = tracé)
import sys, io, base64; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
pol, gr = sys.argv[1], sys.argv[2]; LET = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 'abcdefghijklmnopqrstuvwxyzéèàçùêô’,.?!'
JS = """async a=>{ const [pol,gr,L]=a; TraceLettres._cache={}; await document.fonts.load(gr+' 60px '+pol); const K=6, cw=150, ch=170, per=3, out=document.createElement('canvas'); out.width=cw*K*per; out.height=ch*Math.ceil(L.length/per); const o=out.getContext('2d'); o.fillStyle='#000'; o.fillRect(0,0,out.width,out.height);
  let el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:80px;font:'+gr+' 60px/80px '+pol+';color:#00ff00;z-index:60'; document.body.appendChild(el);
  for(let li=0; li<L.length; li++){ el.textContent=L[li]; const c=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await c.pret; const cv=c.canevas; if(!cv){ c.stop(); continue; }
    c.va(0.99999); const R=document.createElement('canvas'); R.width=cv.width; R.height=cv.height; R.getContext('2d').drawImage(cv,0,0);
    for(let k=0;k<K;k++){ c.va((k+1)/(K+1)); const x0=((li%per)*K+k)*cw, y0=Math.floor(li/per)*ch; o.save(); o.globalAlpha=0.3; o.drawImage(R,x0,y0); o.restore(); o.drawImage(cv,x0,y0); o.fillStyle='#333'; o.fillRect(x0+cw-2,y0,2,ch); o.fillStyle='#000'; }
    c.stop(); }
  el.remove(); return out.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, dsf=2); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.wait_for_timeout(300)
    if '--vieux' in sys.argv: pg.add_script_tag(url='http://127.0.0.1:8752/sauvegardes/trace-lettres-avant-v153.js'); pg.wait_for_timeout(300)
    d = pg.evaluate(JS, [pol, gr, LET]); io.open('scratchpad/v153/planche-%s%s.png' % (pol, '-vieux' if '--vieux' in sys.argv else ''), 'wb').write(base64.b64decode(d.split(',')[1])); b.close()
