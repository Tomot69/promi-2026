import sys, json; from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':1200,'height':400})
    pg.goto('http://127.0.0.1:8752/scratchpad/v147/carte_dbg.html'); pg.wait_for_function('window.pret')
    for c in sys.argv[2]: print(c, json.dumps(pg.evaluate("c=>dbg(c)", c)))
    pg.screenshot(path=sys.argv[1]); b.close()
