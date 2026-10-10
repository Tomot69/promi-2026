import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'; monde=sys.argv[2] if len(sys.argv)>2 else 'ritournelle'
with sync_playwright() as p:
    b=p.webkit.launch()
    for n in (1,3,6,19):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
        pg.evaluate("([m,n])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} if(n<19){var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){}} Toile.setTheme(m); Toile.sync(promises.map(p=>p.id));}",[monde,n]); pg.wait_for_timeout(4000)
        dv=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}"); res=[]
        for (x,y) in ((195,300),(100,420),(290,520),(195,620),(60,250),(330,330)):
            h=pg.evaluate("([x,y])=>{const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(); const q=Toile.hit((x-r.left)*cv.clientWidth/r.width,(y-r.top)*cv.clientHeight/r.height); const e=document.elementFromPoint(x,y); return [q&&q.pid!=null?(promises.find(p=>p.id===q.pid)||{}).title:(q?('graine '+q.kind):null), e&&(e.id||e.className)]}",[dv[0]+x,dv[1]+y])
            pg.touchscreen.tap(dv[0]+x,dv[1]+y); pg.wait_for_timeout(1400)
            e=pg.evaluate("()=>{const dp=document.getElementById('detailPoster'), t=document.getElementById('dptTitre'); const r=[!!(dp&&dp.classList.contains('show')), t?t.textContent.trim():'']; try{closeAll()}catch(e){}; return r}"); pg.wait_for_timeout(600)
            res.append(((x,y),h,e))
        print(n); [print('   ',r) for r in res]; ctx.close()
    b.close()
