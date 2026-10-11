import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import io as _io
R={}
def im(pg): return Image.open(_io.BytesIO(B.capture(pg))).convert('RGB').resize((390,844))
with sync_playwright() as p:
    b=p.webkit.launch()
    for F in sys.argv[1:]:
        for sombre in (False,True):
            ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True,is_mobile=True,user_agent=B.UA,color_scheme='dark' if sombre else 'light')
            ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000); L=[im(pg)]
            B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Tom',delay=40); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200); L.append(im(pg))
            pg.keyboard.type('marcher une heure',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500); L.append(im(pg))
            z=pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return {l:(r.left-d.left)/k,t:(r.top-d.top)/k,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
            print(F,sombre,'trait',z, pg.evaluate("()=>[localStorage.getItem('promi_theme'), document.getElementById('device').className.slice(0,60)]"))
            if z and z['dep']:
                a=[float(v) for v in z['dep'].split(',')]; e=[float(v) for v in z['arr'].split(',')]
                pts=[[z['l']+a[0]+(e[0]+6-a[0])*i/24, z['t']+a[1]+(e[1]-a[1])*i/24-14*(1-abs(2*i/24-1))] for i in range(25)]
                B.glisse(pg,pts,pas=22); pg.wait_for_timeout(1200); L.append(im(pg)); pg.wait_for_timeout(5500); L.append(im(pg))
                B.tap(pg,195,300); pg.wait_for_timeout(1200); L.append(im(pg))
                B.tap_sel(pg,'.onbv-compte .tard'); pg.wait_for_timeout(600); L.append(im(pg)); pg.wait_for_timeout(1500); L.append(im(pg)); pg.wait_for_timeout(2500); L.append(im(pg))
            R[(F,sombre)]=L; ctx.close()
    b.close()
n=max(len(v) for v in R.values()); W=Image.new('RGB',(200*n,430*len(R)),'white')
for r,(k,L) in enumerate(R.items()):
    for i,a in enumerate(L): W.paste(a.resize((195,422)),(i*200,r*430))
W.save('scratchpad/v143/onb2-vue.png')
