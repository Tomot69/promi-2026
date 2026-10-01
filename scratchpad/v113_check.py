from playwright.sync_api import sync_playwright
ECR=[('promi fiche',"()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id)}"),
 ('chiche fiche',"()=>{closeAll();openDetail(promises.find(p=>p.title==='courir dimanche').id)}"),
 ('cercle fiche',"()=>{closeAll();openEssaim('potager')}"),
 ('tenu fiche',"()=>{closeAll();openDetail(promises.find(p=>p.title==='planter un arbre').id)}"),
 ('promi page +',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()},400)}"),
 ('chiche page +',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][1];x&&x.click()},400)}"),
 ('cercle page +',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()},400)}")]
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}"); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for th in ('dark','light'):
        pg.evaluate("t=>setTheme(t)",th)
        for nom,js in ECR:
            pg.evaluate(js); pg.wait_for_timeout(2600)
            r=pg.evaluate("""()=>{const sc=document.querySelector('#detailPoster.show,#createSheet.show');return {fond:getComputedStyle(sc).backgroundColor,
              trait:[...sc.querySelectorAll('canvas[data-filet-trait]')].map(c=>c.getAttribute('data-filet-trait')).join(''),
              disques:[...sc.querySelectorAll('canvas.kr-c')].filter(c=>c.getBoundingClientRect().width>8).map(c=>window._fondSombreSous&&window._fondSombreSous(c)&&!(window._sansFilet&&window._sansFilet(c))?'F':'-').join('')}}""")
            print(th,'%-14s'%nom,r)
            if th=='dark': pg.screenshot(path='scratchpad/v113_%s.png'%nom.replace(' ','_').replace('+','plus'),clip={'x':20,'y':44,'width':390,'height':844})
