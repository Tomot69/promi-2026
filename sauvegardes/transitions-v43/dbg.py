from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    print(pg.evaluate("""async()=>{Toile.setTheme('ritournelle'); await new Promise(r=>setTimeout(r,2000));
      var o=[]; Toile.addPromi(null); for(var i=0;i<8;i++){ await new Promise(r=>setTimeout(r,150)); o.push(JSON.stringify(window._ritTrans)); } return o}"""))
    b.close()
