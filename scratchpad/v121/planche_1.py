# planche 1 @3x : fiches Promi, Chiche et Cercle, page + et Index — en sombre puis en clair — v118 (578ec80) | l'état corrigé, côte à côte
import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S=3; caps={}
E=[('fiche Promi',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),
   ('fiche Chiche',"()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; openDetail(p.id);}"),
   ('fiche Cercle',"()=>{closeAll(); openEssaim('potager');}"),
   ('page +',"()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"),
   ('Index',"()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}")]
V=[('v118 (578ec80)','zz-ref-v118.html'),('corrigé (v121)','app.html')]
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        for ver,url in V:
            for nom,js in E:
                ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
                pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(7000)
                pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(700)
                pg.evaluate(js); pg.wait_for_timeout(4200)
                caps[(th,ver,nom)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); ctx.close()
    b.close()
try: f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',44)
except Exception: f=ImageFont.load_default()
w,h=caps[('dark','corrigé (v121)','Index')].size; G=40; T=70; GP=110
pl=Image.new('RGB',(len(E)*(2*w+G)+(len(E)-1)*GP+2*G, 2*(h+T+G)+G),(150,146,138)); dr=ImageDraw.Draw(pl)
for j,th in enumerate(('dark','light')):
    x=G; y=G+j*(h+T+G)
    for nom,_ in E:
        for ver,_u in V:
            dr.text((x,y),'%s · %s · %s'%(nom,'sombre' if th=='dark' else 'clair',ver),fill=(20,16,6),font=f); pl.paste(caps[(th,ver,nom)],(x,y+T)); x+=w+G
        x+=GP-G
pl.save('planche-v121/planche-1-v118-contre-corrige.png'); print(pl.size)
k=2000/pl.width; pl.resize((2000,int(pl.height*k))).save('scratchpad/v121/planche1-vue.png')
