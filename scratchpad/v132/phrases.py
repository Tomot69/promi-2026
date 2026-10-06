import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){}}")
    src=pg.evaluate("()=>window._murPhrases")
    # ce qui est réellement AFFICHÉ : on fait monter chaque phrase sur le mur du Peaufiner d'une fiche
    out=[]
    for i in range(len(src)):
        pg.evaluate("(i)=>{ try{closeAll()}catch(e){} localStorage.setItem('promi_murs', JSON.stringify({n:i,t:Date.now(),der:i-1,decouvert:1})); const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0]; openDetail(p.id); }", i); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(500)
        c=pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        pg.touchscreen.tap(*c); pg.wait_for_timeout(700)
        out.append(pg.evaluate("()=>{const p=document.getElementById('murPhrase'); return p?{t:p.textContent, mp:[...p.querySelectorAll('.mp')].map(e=>e.textContent)}:null}"))
    json.dump({'src':src,'vu':out}, open('scratchpad/v132/phrases.json','w'), ensure_ascii=False, indent=1)
    for i,(s,v) in enumerate(zip(src,out)): print(i+1, repr(s), '|', repr(v and v['t']), v and v['mp'])
    b.close()
