import sys, os, io, json, math
sys.path.insert(0,'scratchpad'); sys.path.insert(0,'scratchpad/v114'); from aura_ouvre import ouvre; from de00 import de00
from playwright.sync_api import sync_playwright
from PIL import Image
REG=json.loads(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].startswith('{') else None
PALS=['signal','primesautier','allegre','taciturne']
S=3; CX,CY,RSIL,RING=195,276.532,121.0,0.04*232.064
def mesure(im,bg):
    px=im.load(); acc=[0,0,0]; n=0
    for k in range(0,720):
        a=k*math.pi/360
        for rr in (RSIL+0.5+i*(RING-1)/6 for i in range(7)):
            x=(20+CX+math.cos(a)*rr)*S; y=(44+CY+math.sin(a)*rr)*S
            c=px[int(x),int(y)]; acc=[acc[j]+c[j] for j in range(3)]; n+=1
    m=tuple(round(v/n) for v in acc); return de00(m,bg), m
res={}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
    ctx.add_init_script(("window._couronneReglage=%s;"%json.dumps(REG) if REG else "")+"try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for pal in PALS:
        for d in (0,1):
            pg.evaluate("(k)=>{try{_aura.fige(false)}catch(e){} Toile.setPalette(k); window.__R=Math.random; Math.random=function(){return 0.125;};}", pal)
            ouvre(pg,d); pg.evaluate("()=>{Math.random=window.__R}"); pg.wait_for_timeout(5500)
            pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); pg.wait_for_timeout(300)
            im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
            bg=im.getpixel((int((20+10)*S),int((44+300)*S)))
            e,m=mesure(im,bg)
            pg.evaluate("()=>{document.getElementById('auPeloteCouronne').style.visibility='hidden'}"); pg.wait_for_timeout(100)
            e0,_=mesure(Image.open(io.BytesIO(pg.screenshot())).convert('RGB'),bg)
            pg.evaluate("()=>{document.getElementById('auPeloteCouronne').style.visibility=''}")
            k='%s-%s'%(pal,'sombre' if d else 'clair'); res[k]=(round(e,2),round(e0,2))
            E=pg.evaluate('()=>_couronne.etat()'); rm=E['rampeMoy']; res[k]=res[k]+(round(de00(tuple(rm),bg),2),rm,bg,E['gain'])
            print('%-24s ΔE00(rampe,fond) %5.2f  anneau %5.2f  (sans couronne %5.2f)'%(k,res[k][2],e,e0))
    b.close()
json.dump(res,open('scratchpad/v114/couronne_banc.json','w'))
