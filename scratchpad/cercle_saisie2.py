from playwright.sync_api import sync_playwright
OUVRE="()=>{closeAll();openEssaim('potager');setTimeout(()=>{const t=document.querySelector('#dpDetails .dpd-tog')||document.getElementById('dpdTog');t&&t.click()},1200)}"
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for th in ('dark','light'):
      pg.evaluate("t=>setTheme(t)",th)
      for k in range(3):
        pg.evaluate(OUVRE); pg.wait_for_timeout(3200)
        cartes=pg.evaluate("()=>!!document.getElementById('npDesc') && getComputedStyle(document.getElementById('npDesc')).display!=='none'")
        for id,cible in (('nqNote','#npDesc, .s2-zone'),('dCommentInput','#npComm, .s2-zone')):
            r=pg.evaluate("id=>{const f=document.getElementById(id); if(!f) return null; f.scrollIntoView({block:'center'}); const q=f.getBoundingClientRect(); const h=document.elementFromPoint(q.x+q.width/2,q.y+q.height/2); return [q.x+q.width/2,q.y+q.height/2,Math.round(q.width),Math.round(q.height),h===f]}",id)
            if not r or r[2]<5: print(th,k,'cartes' if cartes else 'liste',id,'INVISIBLE',r); continue
            pg.evaluate("()=>{if(document.activeElement)document.activeElement.blur();}")
            pg.touchscreen.tap(r[0],r[1]); pg.wait_for_timeout(500)
            act=pg.evaluate("()=>document.activeElement&&document.activeElement.id")
            pg.keyboard.type('ok'); pg.wait_for_timeout(200)
            v=pg.evaluate("id=>document.getElementById(id).value",id)
            print(th,k,'cartes' if cartes else 'liste',id,'boîte',r[2],'x',r[3],'dessus',r[4],'focus',act,'valeur',repr(v[-8:]))
            pg.evaluate("id=>{const f=document.getElementById(id); f.value=''; f.dispatchEvent(new Event('change'));}",id)
        if th=='dark' and k==0 and cartes: pg.screenshot(path='scratchpad/v111_peauf_cercle.png',clip={'x':20,'y':44,'width':390,'height':844})
    pg.evaluate("()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id)}"); pg.wait_for_timeout(1500)
    print('rendus :',pg.evaluate("()=>['nqNote','dCommentInput'].map(i=>{const f=document.getElementById(i);return i+'→'+(f.parentNode.id||f.parentNode.className)+' np:'+f.classList.contains('np-champ')})"))
