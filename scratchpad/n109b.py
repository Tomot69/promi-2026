from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
    n0=pg.evaluate("()=>promises.length")
    print(pg.evaluate("()=>{try{return typeof due}catch(e){return 'err '+e}}"))
    pg.evaluate("()=>{document.getElementById('fTitle').value='rendre le livre';document.getElementById('fWho').value='Nico';try{due=3}catch(e){};window._csEnLair=false}")
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2600)
    print(n0, pg.evaluate("()=>{const p=promises[promises.length-1];return [promises.length,p.title,p.who,p.due,p.enLair,p.status,p.from,p.dueISO,p.draft,p.req]}"), errs)
    print(pg.evaluate("()=>[localStorage.getItem('promi_onb'),document.getElementById('device').className,typeof Notification!=='undefined'&&Notification.permission, JSON.stringify(_notifEtat())]"))
