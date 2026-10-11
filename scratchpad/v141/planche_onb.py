import sys
from playwright.sync_api import sync_playwright
from PIL import Image
ims=[]
def toucher(cdp,pg,x,y):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
def centre(pg,sel): return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}",sel)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500); cdp=ctx.new_cdp_session(pg)
    def cap():
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='/tmp/o.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('/tmp/o.png').convert('RGB'))
    cap()
    c=centre(pg,'#onbPh'); toucher(cdp,pg,c[0],c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille',delay=30); pg.wait_for_timeout(400); cap()
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900); pg.keyboard.type('marcher une heure',delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(2600); cap()
    z=pg.evaluate("()=>{const c=document.getElementById('onbTrait'); const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    a=[float(v) for v in z['dep'].split(',')]; e=[float(v) for v in z['arr'].split(',')]
    x0,y0,x1,y1=z['l']+a[0]*z['k'],z['t']+a[1]*z['k'],z['l']+(e[0]+6)*z['k'],z['t']+e[1]*z['k']
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x0,'y':y0}]}); pg.wait_for_timeout(90)
    for i in range(1,25):
        u=i/24.0; cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x0+(x1-x0)*u,'y':y0+(y1-y0)*u-14*z['k']*(1-abs(2*u-1))}]}); pg.wait_for_timeout(22)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(6400); cap()
    d=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height*0.36];}"); toucher(cdp,pg,d[0],d[1]); pg.wait_for_timeout(1200); cap()
    b.close()
P=Image.new('RGB',(sum(i.width for i in ims)+20*len(ims),ims[0].height),'white'); x=0
for i in ims: P.paste(i,(x,0)); x+=i.width+20
P.save('planche-v141/PLANCHE-3-onboarding.png'); P.resize((P.width//4,P.height//4)).save('scratchpad/v141/p3.png')
