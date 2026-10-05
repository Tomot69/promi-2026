from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import io
ECR=[('Promi à tenir','faire les crêpes'),('Promi en cours','nager le mardi'),('Promi tenue','planter un arbre'),('page + d\'un Promi',None)]
IM={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for ver,url in (('avant','zz-v129.html'),('après','app.html')):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(800)
        for nom,ti in ECR:
            if ti: pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}",ti); pg.wait_for_timeout(3200)
            else:
                pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(4200)
            IM[(ver,nom)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
        ctx.close()
    b.close()
def police(t):
    for f in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf','/System/Library/Fonts/Helvetica.ttc'):
        try: return ImageFont.truetype(f,t)
        except Exception: pass
    return ImageFont.load_default()
W,H=IM[('avant',ECR[0][0])].size; M=60; T=150
def planche(cols, nom):
    rows=[]; 
    items=[(v,n) for n,_ in ECR for v in ('avant','après')] if cols==2 else [(v,n) for v in ('avant','après') for n,_ in ECR]
    nl=(len(items)+cols-1)//cols
    P=Image.new('RGB',(M+cols*(W+M), 220+nl*(H+T+M)),(245,243,238)); d=ImageDraw.Draw(P)
    d.text((M,50),'v130 · §4 — le corps sombre d\'un Promi devient Tropical Breeze #8ACBE8 (rendu par l\'app, @3x)',fill=(32,25,8),font=police(54 if cols>2 else 40))
    d.text((M,130),'bande #82AEF8 contre corps #8ACBE8 : ΔE (CIELAB) 28,5 · ΔE00 13,1 · Δlum 17,6 — encre #201908 sur le corps : 9,79:1',fill=(90,80,60),font=police(40 if cols>2 else 26))
    for i,(v,n) in enumerate(items):
        x=M+(i%cols)*(W+M); y=220+(i//cols)*(H+T+M)
        d.text((x,y+30),('AVANT (#335382) · ' if v=='avant' else 'APRÈS (#8ACBE8) · ')+n,fill=(32,25,8),font=police(48)); P.paste(IM[(v,n)],(x,y+T))
    P.save('planche-v130/'+nom); print(nom,P.size)
planche(4,'tropical-avant-apres.png'); planche(2,'tropical-avant-apres-telephone.png')
for k,im in IM.items(): im.save('scratchpad/v130/trop-%s-%s.png'%(k[0],k[1].replace(' ','_').replace("'",'')))
