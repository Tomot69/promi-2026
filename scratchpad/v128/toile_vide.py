# la vraie Toile, Pochade, une seule parole, clair et sombre — pour montrer ses cellules vides à côté de la diapositive
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}"%th)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} const P=window.eval('promises'); const g=P.filter(q=>!q.draft&&!q.nuee&&!q.chiche)[0]; Toile.setTheme('encre'); Toile.sync([g.id]); }"); pg.wait_for_timeout(5000)
        pg.screenshot(path='scratchpad/v128/toile-%s.png'%th, clip={'x':20,'y':44,'width':390,'height':844}); ctx.close()
    b.close()
from PIL import Image, ImageDraw, ImageFont
fs=[('diapositive · clair','scratchpad/v128/fin-v128-light.png'),('vraie Toile, une parole · clair','scratchpad/v128/toile-light.png'),('diapositive · sombre','scratchpad/v128/fin-v128-dark.png'),('vraie Toile, une parole · sombre','scratchpad/v128/toile-dark.png')]
ims=[Image.open(f).convert('RGB') for _,f in fs]; w,h=ims[0].size; M=60; T=120
try: ft=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',54)
except: ft=None
def pl(idx,out):
    P=Image.new('RGB',(w*len(idx)+M*(len(idx)+1),h+T+M),(240,236,226)); d=ImageDraw.Draw(P)
    for k,i in enumerate(idx): x=M+k*(w+M); P.paste(ims[i],(x,T)); d.text((x,36),fs[i][0],fill=(32,25,8),font=ft)
    P.save(out)
pl([0,1,2,3],'planche-v128/onboarding-fin.png'); pl([0,1],'planche-v128/onboarding-fin-tel-clair.png'); pl([2,3],'planche-v128/onboarding-fin-tel-sombre.png')
Image.open('planche-v128/onboarding-fin.png').resize(((w*4+M*5)//4,(h+T+M)//4)).save('scratchpad/v128/ap-onb.png')
