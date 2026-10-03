# planche @3x — §3 : les cinq niveaux de halo, en clair et en sombre, densité 1, avec un recadrage à 100 % sur le bord éclairé
import sys, io, math
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S=3; caps={}; N={1:(6,'0,08'),2:(10,'0,10'),3:(14,'0,12'),4:(18,'0,14'),5:(24,'0,16')}
with sync_playwright() as p:
    b=p.webkit.launch()
    for hl in (1,2,3,4,5):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S,reduced_motion='reduce')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'+('' if hl==3 else '?halo=%d'%hl)); pg.wait_for_timeout(7000)
        for th in (0,1):
            pg.evaluate("()=>{ window.__R=Math.random; Math.random=function(){return 0.125;}; }"); ouvre(pg,th); pg.evaluate("()=>{Math.random=window.__R}")
            pg.wait_for_timeout(2500); pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.35);}"); pg.wait_for_timeout(1500)
            caps[(hl,th)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44+80,'width':390,'height':420}))).convert('RGB')
            pg.evaluate("()=>{_aura.fige(false)}")
        ctx.close()
    b.close()
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',40)
w,h=caps[(3,0)].size; G=40; T=110; cw=int(110*S)
LUM=math.atan2(-0.72,-0.58); bx,by=195+140*math.cos(LUM), 270.532-80+140*math.sin(LUM)
W=5*(w+G)+G; H=2*(h+cw+T+2*G)+G
pl=Image.new('RGB',(W,H),(150,146,138)); dr=ImageDraw.Draw(pl)
for j,th in enumerate((0,1)):
    for i,hl in enumerate((1,2,3,4,5)):
        x=G+i*(w+G); y=G+j*(h+cw+T+2*G); im=caps[(hl,th)]
        dr.text((x,y),'?halo=%d%s · %s'%(hl,' (défaut)' if hl==3 else '','sombre' if th else 'clair'),fill=(20,16,6),font=f)
        dr.text((x,y+48),'ΔE00 %d au ras · %s D'%(N[hl][0],N[hl][1]),fill=(20,16,6),font=f)
        pl.paste(im,(x,y+T))
        c=im.crop((int(bx*S)-cw//2,int(by*S)-cw//2,int(bx*S)+cw//2,int(by*S)+cw//2)); pl.paste(c,(x,y+T+h+G))
pl.save('planche-v121/planche-halo-5-niveaux.png'); print(pl.size)
k=1800/pl.width; pl.resize((1800,int(pl.height*k))).save('scratchpad/v121/halo-vue.png')
