import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
LIT = open('scratchpad/v160/tom_versions.py').read().split('LIT = """')[1].split('"""')[0]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx, d = B.contexte_tom(b, 'etats/tom-20261023-125022.json')
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html', timeout=120000); av = None
    for k in range(4):
        if k: pg.reload(timeout=120000)
        pg.wait_for_timeout(11000); r = pg.evaluate(LIT)
        ls = pg.evaluate("()=>{var o={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);o[k]=localStorage.getItem(k);}return o;}")
        print('ouverture', k+1, 'vue', r['s'], r['oy'], 'réparées', pg.evaluate("()=>JSON.stringify(window._placesReparees||null)")[:200])
        if av:
            for kk in sorted(set(ls) | set(av)):
                if ls.get(kk) != av.get(kk):
                    a, c = av.get(kk) or '', ls.get(kk) or ''
                    i = next((j for j in range(min(len(a), len(c))) if a[j] != c[j]), min(len(a), len(c)))
                    print('   change', kk, '…', a[max(0,i-60):i+80], '  →  ', c[max(0,i-60):i+80])
        av = ls
    b.close()
