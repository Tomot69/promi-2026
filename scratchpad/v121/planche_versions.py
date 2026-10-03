# planche 2 (de secours) @3x : la fiche « faire les crêpes », sombre et clair, rendue depuis chaque version de v113 à v119, avec SON moteur
import io, os, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S=3
def git(c, f): return subprocess.run(['git','show','%s:%s'%(c,f)],capture_output=True,check=True).stdout.decode('utf-8')
def lit(p): return io.open(p,encoding='utf-8').read()
V=[('v113','sauvegardes/app-avant-v114.html','sauvegardes/promi-moteur-avant-v115.js','sauvegarde app-avant-v114 (moteur avant-v115)'),
   ('v114','sauvegardes/app-avant-v115.html','sauvegardes/promi-moteur-avant-v115.js','sauvegarde app-avant-v115'),
   ('v115','sauvegardes/app-avant-v116.html','sauvegardes/promi-moteur-avant-v116.js','sauvegarde app-avant-v116'),
   ('v116','sauvegardes/app-avant-v117.html','sauvegardes/promi-moteur-avant-v117.js','sauvegarde app-avant-v117'),
   ('v117','sauvegardes/app-avant-v118.html','sauvegardes/promi-moteur-avant-v118.js','sauvegarde app-avant-v118'),
   ('v118','git:578ec80','git:578ec80','commit 578ec80'),
   ('v119','git:bd156ae','git:bd156ae','commit bd156ae')]
urls=[]
for nom,a,m,src in V:
    A=git(a[4:],'app.html') if a.startswith('git:') else lit(a); M=git(m[4:],'promi-moteur.js') if m.startswith('git:') else lit(m)
    assert A.count('<script src="promi-moteur.js"></script>')==1, nom
    io.open('zz-pv-%s.html'%nom,'w',encoding='utf-8').write(A.replace('<script src="promi-moteur.js"></script>','<script src="zz-pv-%s.js"></script>'%nom))
    io.open('zz-pv-%s.js'%nom,'w',encoding='utf-8').write(M); urls.append((nom,src))
caps={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for nom,src in urls:
        for th in ('dark','light'):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_zzz','0')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/zz-pv-%s.html'%nom); pg.wait_for_timeout(7000)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(700)
            pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(4200)
            caps[(nom,th)]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); ctx.close()
    b.close()
for f in os.listdir('.'):
    if f.startswith('zz-pv-'): os.remove(f)
try: f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',46); f2=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',34)
except Exception: f=f2=ImageFont.load_default()
w,h=caps[('v118','dark')].size; G=50; T=120
pl=Image.new('RGB',(len(urls)*(w+G)+G, 2*(h+T)+2*G),(150,146,138)); dr=ImageDraw.Draw(pl)
for j,th in enumerate(('dark','light')):
    for i,(nom,src) in enumerate(urls):
        x=G+i*(w+G); y=G+j*(h+T)
        dr.text((x,y),'%s — %s'%(nom,'sombre' if th=='dark' else 'clair'),fill=(20,16,6),font=f); dr.text((x,y+56),src,fill=(40,34,20),font=f2)
        pl.paste(caps[(nom,th)],(x,y+T))
pl.save('planche-v121/planche-2-fiche-crepes-v113-v119.png'); print(pl.size)
k=2000/pl.width; pl.resize((2000,int(pl.height*k))).save('scratchpad/v121/versions-vue.png')
