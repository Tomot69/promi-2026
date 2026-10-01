# PORTE 8 — combien de temps met la fiche de Rachel à s'ouvrir après le toucher sur son disque, et le disque est-il rebâti sous le doigt ?
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(); res = []
    for k in range(10):
        pg = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('dark')"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ closeAll(); const p=promises.find(q=>q.title==='faire les crêpes' && q.who==='Rachel'); openDetail(p.id); }"); pg.wait_for_timeout(1200)
        kr = pg.evaluate("""()=>{ const k=[...document.querySelectorAll('.kring[data-p]')].find(e=>e.getAttribute('data-p')==='Rachel'&&e.getBoundingClientRect().width>0); if(!k) return null;
            window.__k=k; const r=k.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2}; }""")
        if not kr: res.append(('pas de disque',)); pg.context.close(); continue
        pg.evaluate("()=>{ window.__t0=performance.now(); window.__to=null; const f=()=>{ if(document.getElementById('personSheet').classList.contains('show')){ window.__to=performance.now()-window.__t0; return; } if(performance.now()-window.__t0<4000) setTimeout(f,100); }; setTimeout(f,0); }")
        pg.mouse.click(kr['x'], kr['y']); pg.wait_for_timeout(4200)
        res.append(pg.evaluate("()=>({ouverte_en_ms: window.__to==null?null:Math.round(window.__to), disque_detache: !window.__k.isConnected, fiche:(document.getElementById('psCadre')||{getAttribute:()=>null}).getAttribute('data-fiche')})"))
        pg.context.close()
    br.close()
for r in res: print('   ', r)
