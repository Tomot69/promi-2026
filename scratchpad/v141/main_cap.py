from playwright.sync_api import sync_playwright
from PIL import Image
ims=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for cas in ('fiche','plus-soi','plus-qqn','recadre'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');['bande','pelote'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')})}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        if cas=='fiche':
            pg.evaluate("()=>{ var p=promises.find(p=>p.title==='faire les crêpes'); openDetail(p.id); }"); pg.wait_for_timeout(3600)
        elif cas=='recadre':
            pg.evaluate("()=>{ window._vueMain=true; try{_majRecadre()}catch(e){} }"); pg.wait_for_timeout(900)
        else:
            pg.evaluate("()=>{ document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(2500)
            pg.evaluate("()=>{ const cs=document.getElementById('createSheet'); if(cs.classList.contains('pp-choix')){ const t=cs.querySelector('[data-kind=promi]'); if(t) t.click(); } }"); pg.wait_for_timeout(2500)
            pg.evaluate("(q)=>{ window._phrase.titre='arroser les plantes'; window._phrase.qui=q; var ft=document.getElementById('fTitle'); if(ft){ft.value='arroser les plantes';} try{ if(window._phraseRendu) _phraseRendu(); if(window._ppArme) _ppArme(); if(window._ppTrait) _ppTrait(); }catch(e){} }", 'Moi' if cas=='plus-soi' else 'Rachel'); pg.wait_for_timeout(2600)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='planche-v141/main-%s.png'%cas,clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('planche-v141/main-%s.png'%cas).convert('RGB'))
        print(cas, pg.evaluate("()=>{const t=document.querySelector('#createSheet .pp-trace'); const g=document.getElementById('gesteFantome'); const rc=document.getElementById('accRecadre'); const D=document.getElementById('device').getBoundingClientRect(); return [t&&getComputedStyle(t).display!=='none'?t.textContent:null, g&&g.getAttribute('data-geste'), rc&&rc.classList.contains('vu')&&Math.round(rc.getBoundingClientRect().bottom-D.top)]}"))
        ctx.close()
    b.close()
P=Image.new('RGB',(sum(i.width for i in ims)+60,ims[0].height),'white'); x=0
for i in ims: P.paste(i,(x,0)); x+=i.width+20
P.save('planche-v141/PLANCHE-5-main-et-mots.png'); P.resize((P.width//4,P.height//4)).save('scratchpad/v141/p5.png')
