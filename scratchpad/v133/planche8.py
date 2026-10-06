from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import re
src=open('scratchpad/v133/cv.py',encoding='utf-8').read()
PEUPLE=re.search(r'PEUPLE="""(.*?)"""',src,re.S).group(1); MES=re.search(r'MES="""(.*?)"""',src,re.S).group(1)
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
res={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for tag,page in (('avant','app.html'),('apres','zz-v133.html')):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+page); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light'); Toile.setTheme('encre');}"); pg.wait_for_timeout(2000)
        for n in (10,20,40):
            pg.evaluate(PEUPLE,[n,1]); pg.wait_for_timeout(4500); r=pg.evaluate(MES); res[(tag,n)]=r
            pg.screenshot(path=SC+'t8-%s-%d.png'%(tag,n), clip={'x':20,'y':44,'width':390,'height':844}); print(tag,n,'%.2f'%r['cv'],'%.1f'%(r['max']/max(1,r['min'])))
        ctx.close()
    b.close()
W,H=1170,2532; M=60; T=150
P=Image.new('RGB',(3*W+4*M, 2*(H+T)+M+170),(255,255,255)); d=ImageDraw.Draw(P)
try: f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',52); fb=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',64)
except Exception: f=fb=ImageFont.load_default()
d.text((M,40),'v133 · C-062 — la diversité des tailles, sous Pochade : avant (l’app) et après (prototype, non intégré)',fill=(32,25,8),font=fb)
for j,tag in enumerate(('avant','apres')):
    for i,n in enumerate((10,20,40)):
        x=M+i*(W+M); y=170+j*(H+T); r=res[(tag,n)]
        d.text((x,y+30),'%s · %d dalles · CV %.2f · la plus grande = %.1f × la plus petite'%('AVANT' if tag=='avant' else 'APRÈS',n,r['cv'],r['max']/max(1,r['min'])),fill=(32,25,8),font=f)
        P.paste(Image.open(SC+'t8-%s-%d.png'%(tag,n)),(x,y+T))
P.save('planche-v133/tailles.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v133/tailles-tel.png')
