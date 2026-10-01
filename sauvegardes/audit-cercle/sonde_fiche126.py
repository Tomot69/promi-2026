# SONDE : pourquoi openDetail(126) n'ouvre-t-il plus rien dans les conditions de verif_integration ?
from playwright.sync_api import sync_playwright
J = """(id)=>{ const out={}; const p=(window.promises||(typeof promises!=='undefined'?promises:[])); 
  try{ out.existe = !!p.find(x=>x.id===id); out.ids = p.slice(0,12).map(x=>x.id); out.n=p.length; }catch(e){ out.existe='?'+e; }
  try{ closeAll(); }catch(e){}
  try{ openDetail(id); out.erreur=null; }catch(e){ out.erreur=String(e).slice(0,200); }
  return out; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for tactile in (False, True):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=tactile); pg = ctx.new_page()
        err = []; pg.on('pageerror', lambda e: err.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        r = pg.evaluate(J, 126); pg.wait_for_timeout(1400)
        r['show'] = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        r['couches'] = pg.evaluate("()=>[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')")
        print('tactile' if tactile else 'souris ', r, '| erreurs JS :', err[:3])
        ctx.close()
    br.close()
