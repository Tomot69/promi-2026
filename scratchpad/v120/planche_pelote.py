# planche @3x — §3 : les 3 × 3 combinaisons ?densite= × ?halo=, en sombre, avec un recadrage à 100 % sur la pelure
import sys, io
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S=3; caps={}; TH=int(sys.argv[1]) if len(sys.argv)>1 else 1
with sync_playwright() as p:
    b=p.webkit.launch()
    for dn in (1,2,3):
        for hl in (1,2,3):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S,reduced_motion='reduce')
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?densite=%d&halo=%d'%(dn,hl)); pg.wait_for_timeout(7000)
            pg.evaluate("()=>{ window.__R=Math.random; Math.random=function(){return 0.125;}; }")
            ouvre(pg,TH); pg.evaluate("()=>{Math.random=window.__R}")
            for _ in range(40):
                if pg.evaluate("()=>{const c=document.getElementById('auBoule'); try{ return !!(c && c.width>400 && _aura.etat().pret); }catch(e){ return false; }}"): break
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(2500); pg.evaluate("()=>{_aura.fige(true); _aura.palier(0); _aura.vue(2.9,0.35);}"); pg.wait_for_timeout(2500)
            caps[(dn,hl)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44+104,'width':390,'height':396}))).convert('RGB')
            print(dn,hl,pg.evaluate("()=>{const e=_aura.etat(); return [e.palier, JSON.stringify(window._peloteReglage)]}")); ctx.close()
    b.close()
try: f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',40)
except Exception: f=ImageFont.load_default()
w,h=caps[(1,1)].size; G=40; T=60; cw=int(150*S)
W=3*(w+G+cw+G)+G; H=3*(h+T+G)+G
pl=Image.new('RGB',(W,H),(60,58,54)); dr=ImageDraw.Draw(pl)
for dn in (1,2,3):
    for hl in (1,2,3):
        x=G+(hl-1)*(w+G+cw+G); y=G+(dn-1)*(h+T+G); im=caps[(dn,hl)]
        dr.text((x,y),'?densite=%d (×%s, poil ×%s)  ·  ?halo=%d (ΔE00 %d au ras, %s D)  ·  recadrage 100 %%'%(dn,['1','1,5','2'][dn-1],['1','0,8','0,7'][dn-1],hl,[6,10,14][hl-1],['0,08','0,10','0,12'][hl-1]),fill=(240,236,224),font=f)
        pl.paste(im,(x,y+T))
        cx,cy=int((195-70)*S),int((122.532+148-104-70)*S)      # un recadrage 150 × 150 pt sur la pelure et le bord éclairé, 1 px d'image = 1 px d'écran @3x
        pl.paste(im.crop((cx-cw//2,cy-cw//2,cx+cw//2,cy+cw//2)),(x+w+G,y+T))
nom='planche-v120/planche-pelote-3x3-%s.png'%('sombre' if TH else 'clair'); pl.save(nom); print(nom,pl.size)
k=1800/pl.width; pl.resize((1800,int(pl.height*k))).save('scratchpad/v120/pelote-3x3-vue-%d.png'%TH)
