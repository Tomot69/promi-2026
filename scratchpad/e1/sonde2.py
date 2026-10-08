from playwright.sync_api import sync_playwright
import json
C="""()=>{ const D=document.getElementById('device').getBoundingClientRect(); const e=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6); const ch=[]; for(let q=e;q&&q!==document.body;q=q.parentElement) ch.push((q.id?'#'+q.id:'')+(typeof q.className==='string'&&q.className?'.'+q.className.split(' ').slice(0,3).join('.'):q.tagName)); return ch.slice(0,7); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); c=b.new_context(viewport={'width':430,'height':932}); c.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=c.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in (('fil',"setView('fil')"),('aura',"document.getElementById('souffleBtn').click()"),('studio',"document.getElementById('studioBtn').click()"),('partage',"document.getElementById('shareBtn').click()"),('page +',"document.getElementById('createBtn').click(); setTimeout(()=>{const t=document.querySelectorAll('.tile')[0]; if(t) t.click();},600)"),('accueil','0')):
        pg.evaluate("()=>{try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(600); pg.evaluate("()=>{%s}"%js); pg.wait_for_timeout(2400)
        print(nom, pg.evaluate(C))
        if nom=='fil': print('  ', pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('[class*=s5-]')].filter(e=>e.getBoundingClientRect().width>300).slice(0,4).map(e=>e.className+':'+Math.round(e.getBoundingClientRect().top-D.top)+':'+Math.round(e.getBoundingClientRect().height))}"))
        if nom=='page +': print('  ', pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(); return ['planterCv','planterCvN','planterCvD','csGeste'].map(i=>{const e=document.getElementById(i); if(!e) return i+':absent'; const r=e.getBoundingClientRect(); return i+':'+[Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)].join(',')+':'+getComputedStyle(e).display+':'+[...e.attributes].map(a=>a.name).join(' ')}).concat([JSON.stringify(window._ppTraitGeo||null), String(typeof window._ppTrait)])}"))
        if nom=='partage': print('  ', pg.evaluate("()=>[window.shNoyau, typeof shareMode!=='undefined'?shareMode:null, window.shNyX, window.shNyY, !!window.shPelote]"))
    b.close()
