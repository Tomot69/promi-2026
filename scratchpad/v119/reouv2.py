from playwright.sync_api import sync_playwright
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""
M = """()=>{ const cv=document.getElementById('auBoule'), W=cv.width; const d=cv.getContext('2d').getImageData(W/2-80,W/2-80,160,160).data; let s=0; for(let i=0;i<d.length;i+=4) s+=d[i]+d[i+1]+d[i+2]; const e=_peloteLumiere.etat(); return [+e.u.toFixed(2), e.calibrages, +(s/(d.length/4)/3).toFixed(2), e.cle]; }"""
def duo(pg,nom):
    r=[]
    for u in (0,1,0,1):
        pg.evaluate("(u)=>{window._peloteU=u}",u); pg.wait_for_timeout(700); r.append(pg.evaluate(M))
    pg.evaluate("()=>{delete window._peloteU}")
    print(nom); [print('   ',x) for x in r]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800); pg.evaluate(OUVRE); pg.wait_for_timeout(4000); duo(pg,'ouverture 1')
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1500); pg.evaluate(OUVRE); pg.wait_for_timeout(3000); duo(pg,'ouverture 2')
    pg.evaluate("()=>{try{_aura.fige(false)}catch(e){}}"); pg.wait_for_timeout(1500); duo(pg,'ouverture 2, en rotation')
    b.close()
