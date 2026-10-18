# C-151 : un titre de deux lignes sur une carte d'Index — hauteur du texte, place visible, ce qui le rogne.
import sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
J = """()=>[...document.querySelectorAll('#indexList .s4-carte')].slice(0,12).map(c=>{ const t=c.querySelector('.s4-ti'), e=c.querySelector('.s4-et'); const a=t.getBoundingClientRect(), b=e?e.getBoundingClientRect():null, cr=c.getBoundingClientRect();
  const R=document.createRange(); R.selectNodeContents(t); const tr=R.getBoundingClientRect(); const cs=getComputedStyle(t);
  return {t:t.textContent.slice(0,22), carte:[Math.round(cr.top),Math.round(cr.height),Math.round(cr.width)], boite:[Math.round(a.top),Math.round(a.bottom)], texte:[Math.round(tr.top),Math.round(tr.bottom)], etat:b?Math.round(b.top):null, fs:cs.fontSize, lh:cs.lineHeight, ov:cs.overflow, mh:cs.maxHeight, h:cs.height, sh:t.scrollHeight, ch:t.clientHeight, clamp:cs.webkitLineClamp}; })"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2); pg.add_init_script("localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s')" % th)
        pg.goto('http://127.0.0.1:8752/' + PAGE); pg.wait_for_timeout(6000)
        pg.evaluate("()=>{ closeAll(); setView('toile'); ouvrirIndex(); }"); pg.wait_for_timeout(4500)
        print(th)
        for x in pg.evaluate(J):
            if x['sh'] > x['ch'] + 1 or (x['etat'] and x['texte'][1] > x['etat']): print('  COUPÉ ', x)
            else: print('  ok    ', x['t'], x['texte'], x['etat'], x['fs'])
        if th == 'light': pg.screenshot(path='scratchpad/v149/index_titres.png')
        pg.close()
    b.close()
