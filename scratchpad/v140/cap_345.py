from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
SRC="""()=>{ const c=document.createElement('canvas'); c.width=600; c.height=800; const g=c.getContext('2d'); g.fillStyle='#E07030'; g.fillRect(0,0,600,800); g.fillStyle='#2080C0'; g.fillRect(0,0,600,300); g.fillStyle='#FFE080'; g.beginPath(); g.arc(300,420,160,0,7); g.fill(); return c.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin','aura-apparait'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()"); cl={'x':d['x'],'y':d['y'],'width':390,'height':844}
    src=pg.evaluate(SRC)
    pg.evaluate("()=>{ const q=promises.find(p=>p.status!=='tenu'&&!p.chiche&&!p.nuee&&!p.draft); window.__q=q; q.photo=null; delete q.dessin; openDetail(q.id); }"); pg.wait_for_timeout(2800)
    pg.evaluate("()=>_dessin.ouvre()"); pg.wait_for_timeout(900)
    r=pg.evaluate("()=>{const s=document.querySelector('#dessinMode canvas'); const r=s.getBoundingClientRect(); return [r.left,r.top]}")
    for i in range(3):
        for _ in range(3):
            if pg.evaluate("()=>!!document.querySelector('#dessinMode [data-taille]')"): break
            pg.evaluate("()=>document.querySelector('#dessinMode [data-outil=plume]').click()"); pg.wait_for_timeout(250)
        if i==2: pg.screenshot(path='scratchpad/v140/c3-tailles.png',clip={'x':d['x'],'y':d['y']+560,'width':390,'height':284})
        pg.evaluate("(i)=>document.querySelector('#dessinMode [data-taille=\"'+i+'\"]').click()",i); pg.wait_for_timeout(250)
        pg.mouse.move(r[0]+60,r[1]+160+70*i); pg.mouse.down()
        for k in range(18): pg.mouse.move(r[0]+60+k*15, r[1]+160+70*i+(k%3)*10); pg.wait_for_timeout(12)
        pg.mouse.up(); pg.wait_for_timeout(250)
    pg.screenshot(path='scratchpad/v140/c3-traits.png',clip=cl)
    pg.evaluate("()=>_dessin.sort(true)"); pg.wait_for_timeout(1300)
    # la vue en entier du dessin
    pg.evaluate("()=>window._entier.ouvre()"); pg.wait_for_timeout(600); pg.screenshot(path='scratchpad/v140/c4-entier-dessin.png',clip=cl)
    print(pg.evaluate("()=>{const e=document.querySelector('#entierVue .ev-garde'); const r=e.getBoundingClientRect(); return [e.getAttribute('aria-label'), e.textContent.trim(), Math.round(r.width), Math.round(r.height), getComputedStyle(e).display]}"))
    pg.evaluate("()=>window._entier.ferme()")
    pg.evaluate("(s)=>{ const b=document.querySelector('#detailPoster .ph-photo-btn'); const q=b._p; q.photo=s; window._photoImportee(q); b._rejoue&&b._rejoue(); }",src); pg.wait_for_timeout(1500)
    pg.screenshot(path='scratchpad/v140/c3-photo.png',clip=cl)
    pg.evaluate("()=>window._entier.ouvre()"); pg.wait_for_timeout(600); pg.screenshot(path='scratchpad/v140/c4-entier-photo.png',clip=cl)
    pg.evaluate("()=>{ window._entier.ferme(); closeAll(); }"); pg.wait_for_timeout(1200); pg.screenshot(path='scratchpad/v140/c4-accueil.png',clip=cl)
    b.close()
def F(n):
    try: return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
    except: return None
# planche 3
a=Image.open('scratchpad/v140/c3-traits.png'); t=Image.open('scratchpad/v140/c3-tailles.png'); ph=Image.open('scratchpad/v140/c3-photo.png')
P=Image.new('RGB',(a.width*3,a.height+80),'white'); dr=ImageDraw.Draw(P)
P.paste(a,(0,80)); P.paste(t,(a.width,80)); P.paste(ph,(a.width*2,80))
for i,s in enumerate(('les trois tailles : 2 · 6 · 22 pt','le choix de taille : cibles de 44 pt, points + 3 pt','après un dessin, une photo importée : elle le remplace, sans reste')): dr.text((a.width*i+20,20),s,fill=(0,0,0),font=F(40))
P.save('planche-v140/PLANCHE-3-dessin-photo.png')
# planche 4
L=[Image.open('scratchpad/v140/c4-%s.png'%n) for n in ('entier-photo','entier-dessin','accueil')]
P=Image.new('RGB',(L[0].width*3,L[0].height+80),'white'); dr=ImageDraw.Draw(P)
for i,(im,s) in enumerate(zip(L,('photo en entier : l’icône, en bas','dessin en entier : la même','accueil : dans le plateau, à gauche de Partager'))): P.paste(im,(im.width*i,80)); dr.text((im.width*i+20,20),s,fill=(0,0,0),font=F(40))
P.save('planche-v140/PLANCHE-4-enregistrer.png'); P.resize((P.width//4,P.height//4)).save('scratchpad/v140/p4-vue.png')
# planche 5 : le +, coté
im=Image.open('scratchpad/v140/plus-light.png').convert('RGB'); S=3; dr=ImageDraw.Draw(im); f=F(30); R=(200,0,60)
def y(v): return (v-690)*S
for (v,lab) in ((730,'haut de la barre 730'),(744,'haut de l’anneau 744'),(816,'bas de l’anneau 816'),(830,'bas de la barre 830')):
    dr.line([(0,y(v)),(im.width,y(v))],fill=R,width=2); dr.text((14,y(v)-34 if v in (730,744) else y(v)+4),lab,fill=R,font=f)
dr.text((640,y(735)),'12 pt',fill=R,font=f); dr.text((640,y(818)),'12 pt',fill=R,font=f)
dr.line([(159*S,y(780)),(231*S,y(780))],fill=R,width=2); dr.text((236*S,y(772)),'anneau 72 pt · disque 45 · épaisseur 13,5',fill=R,font=f)
im.save('planche-v140/PLANCHE-5-plus.png')
