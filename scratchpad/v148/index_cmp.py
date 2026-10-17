from playwright.sync_api import sync_playwright
from PIL import Image
import io
J = """()=>[...document.querySelectorAll('#indexList .s4-carte')].slice(0,6).map(c=>{ const t=c.querySelector('.s4-ti'), e=c.querySelector('.s4-et'); const a=t.getBoundingClientRect(), b=e?e.getBoundingClientRect():null;
  return [t.textContent.slice(0,18), Math.round(a.bottom), b?Math.round(b.top):null, getComputedStyle(t).fontSize, t.scrollHeight, t.clientHeight]; })"""
with sync_playwright() as p:
    b = p.chromium.launch(); ims = []
    for F in ('zz-av147.html', 'app.html'):
        pg = b.new_page(viewport={'width': 430, 'height': 932}); pg.add_init_script("localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','light')")
        pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6000)
        pg.evaluate("()=>{ closeAll(); setView('toile'); ouvrirIndex(); }"); pg.wait_for_timeout(5000)
        print(F); [print('  ', x) for x in pg.evaluate(J)]
        ims.append(Image.open(io.BytesIO(pg.screenshot()))); pg.close()
    w, h = ims[0].size; o = Image.new('RGB', (w * 2 + 20, h), 'white'); o.paste(ims[0], (0, 0)); o.paste(ims[1], (w + 20, 0)); o.resize((o.width // 2, o.height // 2)).save('scratchpad/v148/index_cmp.png')
    b.close()
