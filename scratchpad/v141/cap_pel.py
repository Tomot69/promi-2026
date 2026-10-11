# la Pelote : avant v114 (peintre canevas), aujourd'hui (carte graphique), aujourd'hui (secours) — même thème, vue figée au même angle, @3x
import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
out=sys.argv[1]; th=sys.argv[2] if len(sys.argv)>2 else 'light'
CAS=[('zz-av114.html','avant v114',False),('app.html','aujourd’hui — carte graphique',False),('app.html','aujourd’hui — secours',True)]
if len(sys.argv)>3: CAS=[(sys.argv[3],'v140',False)]+CAS[1:]
ims=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for f,lab,sec in CAS:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){} %s"%(th,'window._peloteGL=false;' if sec else ''))
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(7000)
        info=pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(0.3,0.2);}catch(e){} var c=document.getElementById('auBoule'); var r=c.getBoundingClientRect(); var gl=document.getElementById('auBouleGL'); return {gl:!!(gl&&gl.style.visibility!=='hidden'&&gl.getBoundingClientRect().width>0),r:[r.left,r.top,r.width,r.height]}}")
        pg.wait_for_timeout(1500); r=info['r']
        pg.screenshot(path='/tmp/pel.png',clip={'x':r[0]-6,'y':r[1]-6,'width':r[2]+12,'height':r[3]+12}); im=Image.open('/tmp/pel.png').convert('RGB'); ims.append((lab+(' (GL)' if info['gl'] else ' (canevas)'),im)); print(f,lab,info)
        ctx.close()
    b.close()
W=max(i.width for _,i in ims); H=max(i.height for _,i in ims); C=330
P=Image.new('RGB',(len(ims)*(W+20),H+60+C*2+30),'white'); d=ImageDraw.Draw(P)
for k,(lab,im) in enumerate(ims):
    x=k*(W+20); d.text((x+8,8),lab,fill=(0,0,0)); P.paste(im,(x,30))
    cx,cy=im.width//2,im.height//2; R=int(116*3)
    a=im.crop((cx+int(R*0.707)-C//2, cy-int(R*0.707)-C//2, cx+int(R*0.707)+C//2, cy-int(R*0.707)+C//2)).resize((C*2,C*2),Image.NEAREST)   # le bord en haut à droite, ×2 du @3x
    P.paste(a.crop((0,0,min(C*2,W),C*2)),(x,H+50))
P.save(out); P.resize((P.width//2,P.height//2)).save(out.replace('.png','-p.png'))
