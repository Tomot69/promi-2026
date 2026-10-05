import sys, math
from playwright.sync_api import sync_playwright
from PIL import Image
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
th=sys.argv[1] if len(sys.argv)>1 else 'dark'; quoi=sys.argv[2] if len(sys.argv)>2 else 'promi'
clip={'x':20,'y':44,'width':390,'height':844}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(600)
    if quoi=='promi': pg.evaluate("()=>{closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}")
    elif quoi=='cercle': pg.evaluate("()=>{closeAll(); openEssaim('potager');}")
    else: pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}")
    pg.wait_for_timeout(3600)
    def centre(sel):
        return pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].filter(x=>x.getBoundingClientRect().width>0)[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", sel)
    ims=[]
    def prise(): pg.wait_for_timeout(350); pg.screenshot(path=SC+'dz-%d.png'%len(ims), clip=clip); ims.append(SC+'dz-%d.png'%len(ims))
    c=centre('.ph-photo-btn'); print('bouton photo', c); pg.touchscreen.tap(*c); prise()
    c=centre('.ph-photo-menu [data-dessiner]'); print('Dessiner', c, pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(b=>b.textContent+' '+Math.round(b.getBoundingClientRect().height))")); pg.touchscreen.tap(*c); pg.wait_for_timeout(400)
    print('mode ouvert', pg.evaluate("()=>window._dessin.ouvert()"), pg.evaluate("()=>window._dessin.etat()"))
    def trait(F, n=40, pas=12):
        P=[F(i/n) for i in range(n+1)]; pg.mouse.move(20+P[0][0],44+P[0][1]); pg.mouse.down()
        for x,y in P[1:]: pg.mouse.move(20+x,44+y); pg.wait_for_timeout(pas)
        pg.mouse.up()
    trait(lambda u:(60+u*250, 220+70*math.sin(u*9)))
    trait(lambda u:(195+90*math.cos(u*6.28), 480+90*math.sin(u*6.28)), 50, 8)
    trait(lambda u:(80+u*220, 680), 12, 4)
    prise()
    pg.touchscreen.tap(*centre('#dessinMode [data-outil=plume]')); prise()
    pg.touchscreen.tap(*centre('#dessinMode [data-taille="2"]')); pg.touchscreen.tap(*centre('#dessinMode [data-outil=couleur]')); prise()
    tons=pg.evaluate("()=>[...document.querySelectorAll('#dessinMode .dz-ton')].map(e=>e.getAttribute('data-ton')+(e.disabled?' (grisé)':''))"); print('tons', tons)
    pg.touchscreen.tap(*centre('#dessinMode .dz-ton:not([disabled])')); trait(lambda u:(100+u*200, 330+u*40), 20, 10); prise()
    print('état', pg.evaluate("()=>window._dessin.etat()"))
    pg.touchscreen.tap(*centre('#dessinMode [data-outil=poser]')); pg.wait_for_timeout(600); prise()
    print('après POSER : mode', pg.evaluate("()=>window._dessin.ouvert()"), 'bande', pg.evaluate("()=>{const c=document.querySelector('.dz-bande'); return c?[c.width,c.height,c.getBoundingClientRect().top]:null}"), 'œil', centre('.dz-oeil'))
    pg.touchscreen.tap(20+195, 44+(150 if quoi=='cercle' else 220)); pg.wait_for_timeout(500); print('vue entière', pg.evaluate("()=>window._entier.ouverte()")); prise()
    pg.evaluate("()=>window._entier.ferme()")
    c=centre('.dz-oeil')
    if c: pg.touchscreen.tap(*c); prise()
    L=[Image.open(f) for f in ims]; P=Image.new('RGB',(sum(i.size[0] for i in L)//2+10*len(L), 844),(255,255,255)); x=0
    for i in L: P.paste(i.resize((390,844)),(x,0)); x+=400
    P.save(SC+'dz-%s-%s.png'%(quoi,th)); b.close()
