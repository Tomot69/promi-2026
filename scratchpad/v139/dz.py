from playwright.sync_api import sync_playwright
PHOTO = r"""()=>{ const c=document.createElement('canvas'); c.width=600; c.height=400; const g=c.getContext('2d'); [['#E00000',0,0],['#00B000',300,0],['#0000E0',0,200],['#E0E000',300,200]].forEach(q=>{ g.fillStyle=q[0]; g.fillRect(q[1],q[2],300,200); }); return c.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','bande','dessin'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1'));}catch(e){}")
    pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:150])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} openDetail(promises.find(q=>q.title==='nager le mardi').id)}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{window._dessin.ouvre()}"); pg.wait_for_timeout(800); src=pg.evaluate(PHOTO)
    pg.evaluate("(s)=>{window._dessin.ajoutePhoto(s)}",src); pg.wait_for_timeout(800)
    r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}")
    # trois traits aux trois tailles
    for i,y in enumerate((140,200,260)):
        pg.evaluate("()=>{for(var n=0;n<3 && !document.querySelector('#dessinMode [data-taille]');n++) document.querySelector('#dessinMode [data-outil=plume]').click();}"); pg.wait_for_timeout(200)
        pg.evaluate("(i)=>{document.querySelector('#dessinMode [data-taille=\"'+i+'\"]').click()}",i); pg.wait_for_timeout(200)
        pg.mouse.move(r[0]+60,r[1]+y); pg.mouse.down(); 
        for k in range(1,14): pg.mouse.move(r[0]+60+k*20,r[1]+y+(8 if k%2 else -8)); pg.wait_for_timeout(15)
        pg.mouse.up(); pg.wait_for_timeout(200)
    pg.evaluate("()=>{for(var n=0;n<3 && !document.querySelector('#dessinMode [data-taille]');n++) document.querySelector('#dessinMode [data-outil=plume]').click();}"); pg.wait_for_timeout(300)
    pg.screenshot(path='planche-v139/dessin-mode.png',clip={'x':r[0],'y':r[1],'width':390,'height':844}); print(er, pg.evaluate("()=>JSON.stringify(window._dessin.etat())"), pg.evaluate("()=>JSON.stringify(window._dessin.photos())")); b.close()
