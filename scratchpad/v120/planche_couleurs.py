# planche @3x — §2 : la fiche « faire les crêpes », la page + et l'Index, AVANT (v118, seiche) | APRÈS (v120, avant v116), en sombre
import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S=3; caps={}
E=[('fiche « faire les crêpes »',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),
   ('page +',"()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"),
   ('Index',"()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}")]
with sync_playwright() as p:
    b=p.webkit.launch()
    for ver,url in (('AVANT (v118)','zz-avant-v120.html'),('APRÈS (v120)','app.html')):
        for nom,js in E:
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(7000)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(700)
            pg.evaluate(js); pg.wait_for_timeout(4200)
            caps[(ver,nom)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); ctx.close()
    b.close()
try: f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',44)
except Exception: f=ImageFont.load_default()
w,h=caps[('APRÈS (v120)','Index')].size; G=50; T=70
pl=Image.new('RGB',(6*w+7*G+G, h+T+2*G),(150,146,138)); dr=ImageDraw.Draw(pl); x=G
for nom,_ in E:
    for ver in ('AVANT (v118)','APRÈS (v120)'):
        dr.text((x,G),'%s — %s'%(nom,ver),fill=(20,16,6),font=f); pl.paste(caps[(ver,nom)],(x,G+T)); x+=w+G
    x+=G//2
pl.save('planche-v120/planche-couleurs-avant-apres-sombre.png'); print(pl.size)
k=1800/pl.width; pl.resize((1800,int(pl.height*k))).save('scratchpad/v120/couleurs-vue.png')
