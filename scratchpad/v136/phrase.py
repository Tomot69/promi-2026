from playwright.sync_api import sync_playwright
from PIL import Image
CAS=[('à soi',"p=promises.find(q=>q.id===128)"),
     ('à une personne',"p=promises.find(q=>q.id===126)"),
     ('à plusieurs (3)',"p=promises.find(q=>q.id===126); p.who='Rachel, Marion, Nico'"),
     ('à plusieurs (6)',"p=promises.find(q=>q.id===126); p.who='Rachel, Marion, Nico, Adrien, Léa, Jo'"),
     ('Promi reçu',"p=promises.find(q=>q.id===140); p.from='Rachel'; p.who='moi'"),
     ('Chiche lancé',"p=promises.find(q=>q.id===127)"),
     ('Chiche reçu',"p=promises.find(q=>q.id===127); p.from='Marion'; p.who='moi'; p.avec=''"),
     ('Promi tenu, voyelle',"p=promises.find(q=>q.id===125); p.title='aller voir la mer'")]
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    for i,(nom,js) in enumerate(CAS):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6200)
        pg.evaluate("(js)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light'); let p; eval(js); closeAll(); openDetail(p.id);}",js); pg.wait_for_timeout(3000)
        r=pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(), q=document.getElementById('dptQui'), t=document.getElementById('dptTitre'), e=document.getElementById('dptQuand'); const g=x=>{const r=x.getBoundingClientRect(); return [Math.round(r.top-D.top), Math.round(r.bottom-D.top)]}; return {phrase:q.textContent, titre:t.textContent, q:g(q), t:g(t), e:g(e), fq:getComputedStyle(q).fontSize, ft:getComputedStyle(t).fontSize, cq:getComputedStyle(q).color}}")
        print(nom, r)
        f='scratchpad/v136/ph-%d.png'%i; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        if '6' in nom:
            c=pg.evaluate("()=>{const e=document.querySelector('#dptQui .dpt-plus'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
            if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1500)
            print('  déplié', pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(), q=document.getElementById('dptQui'), t=document.getElementById('dptTitre'); return [q.textContent, Math.round(q.getBoundingClientRect().bottom-D.top), Math.round(t.getBoundingClientRect().top-D.top)]}"))
            f='scratchpad/v136/ph-%db.png'%i; pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
        ctx.close()
    b.close()
W,H=1170,2532; n=len(ims); P=Image.new('RGB',(n*(W+40)+40,H+80),(255,255,255))
for i,f in enumerate(ims): P.paste(Image.open(f),(40+i*(W+40),40))
P.save('planche-v136/phrases.png'); P.resize((2400,int(P.height*2400/P.width))).save('scratchpad/v136/phrases-vue.png')
