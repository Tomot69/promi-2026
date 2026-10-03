# §1 — la planche : l'actuel (peintre d'origine) et le nouveau rendu (carte graphique), même ouverture, même angle, même souffle ; @3x
import sys
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',40); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000); R={}
    for th in (0,1):
        ouvre(pg,th); pg.wait_for_timeout(2800); pg.evaluate("()=>{document.getElementById('auraScreen').scrollTop=0; _aura.fige(true); _aura.vue(3.1,0.32)}")
        bo=pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        for nom,gl in (('actuel',False),('nouveau',True)):
            pg.evaluate("(g)=>{window._peloteGL=g; _aura.pelote()}", gl); pg.wait_for_timeout(900)
            fn='scratchpad/v125/pel-%s-%d.png'%(nom,th); pg.screenshot(path=fn, clip={'x':bo[0]-24,'y':bo[1]-24,'width':bo[2]+48,'height':bo[3]+48}); R[(nom,th)]=Image.open(fn).convert('RGB')
        pg.evaluate("()=>{window._peloteGL=true; _aura.fige(false)}")
    b.close()
W,H=R[('actuel',0)].size; C=450   # recadrage à 100 % : 450 px d'image = 150 pt d'écran
out=Image.new('RGB',(2*W+2*C+5*40, 2*(H+120)+40),(255,255,255)); d=ImageDraw.Draw(out)
for th in (0,1):
    y=40+th*(H+120); nomth='sombre' if th else 'clair'
    for j,nom in enumerate(('actuel','nouveau')):
        x=40+j*(W+40); out.paste(R[(nom,th)],(x,y+70)); d.text((x,y+14),('ACTUEL — peintre d\'origine' if nom=='actuel' else 'NOUVEAU — carte graphique')+' · '+nomth,font=F,fill=(20,20,20))
        cx=40+2*(W+40)+j*(C+40); cr=R[(nom,th)].crop((W//2-40, H//2-C//2-60, W//2-40+C, H//2+C//2-60)); out.paste(cr,(cx,y+70))
        d.text((cx,y+14),'recadrage à 100 % · '+nom,font=f,fill=(20,20,20))
        cr2=R[(nom,th)].crop((W-C-10, 60, W-10, 60+C)); out.paste(cr2,(cx,y+70+C+30)); d.text((cx,y+70+C+2),'le bord',font=f,fill=(90,90,90))
out.save('planche-v125/pelote-actuel-nouveau.png'); print(out.size)
out.resize((out.size[0]//3,out.size[1]//3)).save('scratchpad/v125/pelote-vue.png')
