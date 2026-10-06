from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import re, json
src=open('scratchpad/v135/cv.py',encoding='utf-8').read()
PEUPLE=re.search(r'PEUPLE="""(.*?)"""',src,re.S).group(1)
MONDES=[('esquille','Esquille'),('halin','Halin'),('brouillamini','Brouillamini'),('ramage','Ramage'),('guingois','Guingois'),('chantourne','Chantourné'),('volubilis','Volubilis'),('chamade','Chamade'),('ritournelle','Ritournelle'),('mascaret','Mascaret')]
A=json.load(open('scratchpad/v135/cv-avant-esquille-halin-brouillamini-ramage-guingois-chantourne-volubilis-chamade-ritournelle-mascaret-bobinette.json'))
B=json.load(open('scratchpad/v135/cv-apres-esquille-halin-brouillamini-ramage-guingois-chantourne-volubilis-chamade-ritournelle-mascaret.json'))
SC='scratchpad/v135/'
with sync_playwright() as p:
    b=p.webkit.launch()
    for tag,page in (('av','zz-v135-avant.html'),('ap','app.html')):
        for mo,_ in MONDES:
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+page); pg.wait_for_timeout(6500)
            pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light'); setPremium(true); Toile.setTheme(m);}",mo); pg.wait_for_timeout(2500)
            for n in (20,40):
                pg.evaluate(PEUPLE,[n,1]); pg.wait_for_timeout(5000)
                pg.screenshot(path=SC+'t-%s-%s-%d.png'%(tag,mo,n), clip={'x':20,'y':44,'width':390,'height':844})
            ctx.close(); print(tag,mo,flush=True)
    b.close()
W,H,M,T=780,1688,40,110
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',38)
for k,grp in enumerate((MONDES[:5],MONDES[5:])):
    P=Image.new('RGB',(4*W+5*M, len(grp)*(H+T)+M),(255,255,255)); d=ImageDraw.Draw(P)
    for i,(mo,nom) in enumerate(grp):
        for j,(tag,n) in enumerate((('av',20),('ap',20),('av',40),('ap',40))):
            x=M+j*(W+M); y=M+i*(H+T); cv=(A if tag=='av' else B)[mo][str(n)]['cv']
            d.text((x,y+10),'%s · %d dalles · %s'%(nom,n,'AVANT' if tag=='av' else 'APRÈS'),fill=(32,25,8),font=f); d.text((x,y+56),'coefficient de variation %.2f'%cv,fill=(32,25,8),font=f)
            P.paste(Image.open(SC+'t-%s-%s-%d.png'%(tag,mo,n)),(x,y+T))
    P.save('planche-v135/tailles-%d.png'%(k+1)); P.resize((1290,int(P.height*1290/P.width))).save('planche-v135/tailles-%d-tel.png'%(k+1))
