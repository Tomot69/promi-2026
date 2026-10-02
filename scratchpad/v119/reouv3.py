from playwright.sync_api import sync_playwright
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""
M = """()=>{ const cv=document.getElementById('auBoule'), W=cv.width; const d=cv.getContext('2d').getImageData(W/2-80,W/2-80,160,160).data; let s=0; for(let i=0;i<d.length;i+=4) s+=d[i]+d[i+1]+d[i+2]; const e=_peloteLumiere.etat(); return [+e.u.toFixed(2), e.calibrages, +(s/(d.length/4)/3).toFixed(2), e.cle]; }"""
C = """()=>{const c=_peloteLumiere.carte(); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; const W0=c.width, dc=c.getContext('2d').getImageData(W0/2-80,W0/2-80,160,160).data; let ca=0,cr=0,cg=0,cb=0; for(let i=0;i<dc.length;i+=4){ca+=dc[i+3]; cr+=dc[i]*dc[i+3]/255; cg+=dc[i+1]*dc[i+3]/255; cb+=dc[i+2]*dc[i+3]/255;} const N=dc.length/4; window.__ctr=[+(ca/N).toFixed(1),+(cr/N).toFixed(1),+(cg/N).toFixed(1),+(cb/N).toFixed(1)]; let n=0,sa=0,mx=0,sr=0; for(let i=3;i<d.length;i+=4){ if(d[i]){ n++; sa+=d[i]; sr+=d[i-3]; if(d[i]>mx)mx=d[i]; } } return {W:c.width, pleins:n, alphaMoy:+(sa/Math.max(1,n)).toFixed(1), rMoy:+(sr/Math.max(1,n)).toFixed(0), alphaMax:mx, centre:window.__ctr}}"""
M = """()=>{ const cv=document.getElementById('auBoule'), W=cv.width; const d=cv.getContext('2d').getImageData(W/2-80,W/2-80,160,160).data; let r=0,g=0,b=0,op=0,am=255; for(let i=0;i<d.length;i+=4){ if(d[i+3]<255) op++; if(d[i+3]<am) am=d[i+3]; r+=d[i]; g+=d[i+1]; b+=d[i+2]; } const N=d.length/4; const e=_peloteLumiere.etat(); return [+e.u.toFixed(2), e.calibrages, [+(r/N).toFixed(1),+(g/N).toFixed(1),+(b/N).toFixed(1)], 'non opaques '+(100*op/N).toFixed(1)+'% min '+am, e.cle]; }"""
def duo(pg,nom):
    print('  carte',pg.evaluate(C))
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
    pg.evaluate('()=>_peloteLumiere.recalibre()'); pg.wait_for_timeout(1500); duo(pg,'recalibrée')
    for v in (0,.55,0,.55):
        pg.evaluate("(v)=>{window._peloteMod=function(o){o.velours=v}}",v); pg.wait_for_timeout(800); print('   peintre direct velours',v,pg.evaluate(M)[2])
    pg.evaluate("()=>{delete window._peloteMod}")
    b.close()
