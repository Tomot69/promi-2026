from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import io
ECR=[('Promi à tenir','faire les crêpes'),('Promi en cours','nager le mardi'),('Promi tenue','planter un arbre'),("page + d'un Promi",None),('un mur de Ma Parole !','mur')]
IM={}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); try{setPremium(false)}catch(e){}}"); pg.wait_for_timeout(800)
    for nom,ti in ECR:
        if ti=='mur':
            pg.evaluate("()=>{ try{closeAll()}catch(e){} const PH=window._murPhrases||[]; const i=PH.findIndex(s=>s.indexOf('Ma Parole')>=0); localStorage.setItem('promi_murs', JSON.stringify({n:Math.max(0,i),t:Date.now(),der:Math.max(0,i)-1,decouvert:1})); const p=promises.filter(q=>q.title==='nager le mardi')[0]; openDetail(p.id); }"); pg.wait_for_timeout(1800)
            pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(700)
            c=pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
            pg.touchscreen.tap(*c); pg.wait_for_timeout(900)
            print('mur :', pg.evaluate("()=>{const p=document.getElementById('murPhrase'), m=p&&p.querySelector('.mp'); return [p&&p.className, p&&getComputedStyle(p).color, m&&getComputedStyle(m).color, p&&p.textContent.slice(0,50)]}"))
        elif ti: pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}",ti); pg.wait_for_timeout(3200)
        else:
            pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(4200)
        IM[nom]=Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
    b.close()
def police(t,g=True):
    try: return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if g else '/System/Library/Fonts/Supplemental/Arial.ttf',t)
    except Exception: return ImageFont.load_default()
W,H=IM[ECR[0][0]].size; M=60; T=110
def planche(cols, nom):
    nl=(len(ECR)+cols-1)//cols; P=Image.new('RGB',(M+cols*(W+M), 330+nl*(H+T+M)),(30,26,22)); d=ImageDraw.Draw(P); c=(247,240,222); g=(190,180,160)
    d.text((M,46),"v131 · §1 — le corps sombre d'un Promi : cobalt électrique #273CEB (rendu par l'app, @3x)",fill=c,font=police(54 if cols>2 else 38))
    L=["crème #F7F0DE sur le corps : 6,30:1 · « Ma Parole ! » #FF8664 : 3,02:1 (OKLCH h 36°, la teinte de #FB4C0D)",
       "états contre le corps (ΔE CIELAB, seuil 15) : à tenir 141,9 · en cours #291547 72,9 · tenu 128,8 · trait Promi #022140 87,2",
       "bande #82AEF8 contre corps : ΔE 76,3 · Δlum 95,6 (pour information)"]
    for i,l in enumerate(L): d.text((M,128+i*56),l if cols>2 else l[:86],fill=g,font=police(38 if cols>2 else 26,False))
    for i,(n,_) in enumerate(ECR):
        x=M+(i%cols)*(W+M); y=330+(i//cols)*(H+T+M); d.text((x,y+26),n,fill=c,font=police(48)); P.paste(IM[n],(x,y+T))
    P.save('planche-v131/'+nom); print(nom,P.size); return P
planche(5,'cobalt.png'); P=planche(2,'cobalt-telephone.png'); P.resize((1290,P.size[1]*1290//P.size[0]),Image.LANCZOS).save('planche-v131/cobalt-tel.png')
