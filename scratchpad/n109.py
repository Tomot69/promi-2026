from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        ctx.add_init_script("window.__notifs=[];window.__demandes=0;window.Notification=function(t,o){window.__notifs.push([t,o&&o.body])};Notification.permission='default';Notification.requestPermission=function(){window.__demandes++;Notification.permission='granted';return Promise.resolve('granted')};")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        perm=pg.evaluate("()=>typeof Notification!=='undefined'?Notification.permission:'absent'")
        pg.evaluate("t=>{setTheme(t);setPremium(false)}",th)
        # planter un Promi daté
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{document.getElementById('fTitle').value='rendre le livre';document.getElementById('fWho').value='Nico';due=3;window._csEnLair=false}")
        pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2600)
        q=pg.evaluate("()=>{const q=document.getElementById('rapQuestion');return q?[q.className,q.textContent,getComputedStyle(q).display]:null}")
        pg.screenshot(path=f'scratchpad/n109_q_{th}.png')
        plan0=pg.evaluate("()=>_notifPlan().length")
        # oui
        pg.evaluate("()=>{document.querySelector('#rapQuestion [data-r=oui]').click()}"); pg.wait_for_timeout(300)
        et=pg.evaluate("()=>_notifEtat()"); pl=pg.evaluate("()=>_notifPlan().map(e=>[e.type,new Date(e.quand).toString().slice(0,21),e.mots.titre,e.mots.texte])")
        # Réglages → page
        pg.evaluate("()=>{closeAll();document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(1000)
        pg.evaluate("()=>document.getElementById('notifCard').click()"); pg.wait_for_timeout(1200)
        pg.screenshot(path=f'scratchpad/n109_page_{th}.png')
        txt=pg.evaluate("()=>document.getElementById('notifScreen').innerText")
        print(th,'perm',perm,'err',errs,'\n q',q,'\n plan avant oui',plan0,'\n etat',et,'\n plan',pl,'\n page',txt.replace('\n',' | '))
        ctx.close()
