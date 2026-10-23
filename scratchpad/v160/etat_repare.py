import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx, d = B.contexte_tom(b, 'etats/tom-20261023-125022.json')
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html', timeout=120000); pg.wait_for_timeout(12000)
    d['ls'] = pg.evaluate("()=>{var o={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);o[k]=localStorage.getItem(k);}return o;}")
    json.dump(d, open('scratchpad/v160/tom-repare.json', 'w'), ensure_ascii=False); b.close()
print('ok')
