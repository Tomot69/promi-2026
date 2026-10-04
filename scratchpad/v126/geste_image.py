# le geste de couleur du Studio, jugé À L'IMAGE : ce qu'on voit sous le doigt change-t-il pendant qu'on glisse ?
import sys, io, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
def doigt(cdp,t,x,y,ms): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':([] if t=='touchEnd' else [{'x':x,'y':y}]),'timestamp':ms/1000.0})
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True,is_mobile=True,device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(3500)
    d=pg.evaluate("()=>{var d=document.getElementById('device').getBoundingClientRect();return [d.left,d.top,d.width,d.height];}")
    pt=[d[0]+d[2]/2, d[1]+d[3]*0.42]
    print('sous le doigt :', pg.evaluate("([x,y])=>document.elementsFromPoint(x,y).slice(0,6).map(e=>(e.id||e.className||e.tagName)+'').join(' > ')", pt))
    clip={'x':d[0]+30,'y':d[1]+150,'width':d[2]-60,'height':330}
    cap=lambda: Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
    def ecart(a,b_): return sum(ImageStat.Stat(ImageChops.difference(a,b_)).mean)/3
    a0=cap(); pg.wait_for_timeout(700); a1=cap(); print('bruit au repos (deux captures) : %.2f niveaux' % ecart(a0,a1))
    et=lambda: pg.evaluate("()=>({hue:Toile.getHue(), pal:Toile.getPalette(), arme:window._studioGesteCouleur&&_studioGesteCouleur.arme()})")
    print('avant', et())
    ms=1000; doigt(cdp,'touchStart',pt[0],pt[1],ms); pg.wait_for_timeout(720); print('après appui long', et())
    for i in range(1,7): ms+=40; doigt(cdp,'touchMove',pt[0]+i*20,pt[1],ms)
    pg.wait_for_timeout(700); h=cap(); print('glissé de 120 px à l\'horizontale', et(), '· image : %.2f niveaux d\'écart' % ecart(a1,h)); h.save('scratchpad/v126/geste-h-%s.png' % F.replace('.html',''))
    for i in range(1,7): ms+=40; doigt(cdp,'touchMove',pt[0]+120,pt[1]+i*20,ms)
    pg.wait_for_timeout(900); v=cap(); print('puis 120 px à la verticale', et(), '· image : %.2f niveaux d\'écart avec le départ, %.2f avec l\'étape d\'avant' % (ecart(a1,v), ecart(h,v)))
    doigt(cdp,'touchEnd',0,0,ms+60); pg.wait_for_timeout(900); f=cap(); print('relâché', et(), '· image : %.2f avec le départ' % ecart(a1,f))
    a1.save('scratchpad/v126/geste-0.png'); f.save('scratchpad/v126/geste-fin-%s.png' % F.replace('.html',''))
    b.close()
