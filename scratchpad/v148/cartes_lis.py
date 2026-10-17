from playwright.sync_api import sync_playwright
import sys
page = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ('light','dark'):
        pg=b.new_page(viewport={'width':430,'height':932}); pg.add_init_script("localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s')"%th)
        pg.goto('http://127.0.0.1:8752/'+page); pg.wait_for_timeout(6000)
        pg.evaluate("()=>{ closeAll(); setView('toile'); ouvrirIndex(); }"); pg.wait_for_timeout(5000)
        print(th, 'INDEX', pg.evaluate("()=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>[c.querySelector('.s4-ti').textContent.slice(0,14), getComputedStyle(c).backgroundColor, getComputedStyle(c.querySelector('.s4-et')).color, getComputedStyle(c.querySelector('.s4-eb')).color])"))
        pg.evaluate("()=>{ closeAll(); document.getElementById('filBtn').click(); }"); pg.wait_for_timeout(5000)
        print(th, 'FIL', pg.evaluate("()=>[...document.querySelectorAll('#feedList .s4-carte, .s4-carte')].filter(c=>c.closest('#feedView,#filSheet,#feedSheet,[id*=eed]')).map(c=>[(c.querySelector('.s4-ti')||{}).textContent.slice(0,14), getComputedStyle(c).backgroundColor, getComputedStyle(c.querySelector('.s4-et')).color])"))
        pg.close()
    b.close()
