# la page + d'un Chiche, en sombre, ouverte après celle d'un Promi : quand paraît-elle ? (même ouverture que redteam_contraste_trait)
import sys
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark');}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(7000)
    def ferme(): pg.evaluate("()=>{ try{ window._peaufSortie && window._peaufSortie(); closeAll(); }catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); try{ setView('toile'); }catch(e){} }"); pg.wait_for_timeout(700)
    for nat in ('promi', 'chiche', 'nuee'):
        ferme(); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
        pg.evaluate("(k)=>{ const b=document.querySelector('.acc-pil[data-k='+k+']'); if(b) b.click(); }", nat)
        L = []
        for i in range(30):
            pg.wait_for_timeout(100)
            L.append(pg.evaluate("()=>{ const s=document.getElementById('createSheet'), c=getComputedStyle(s); const h=document.elementFromPoint(195, 300); return [s.className.split(' ').filter(x=>/show|pp-|cs-|acc/.test(x)).join(' '), c.visibility, c.opacity, c.transform.slice(0,30), h?(h.id||h.className).toString().slice(0,18):null]; }"))
        print(nat); prev = None
        for i, l in enumerate(L):
            if l != prev: print('  %4d' % ((i + 1) * 100), l); prev = l
    b.close()
