from playwright.sync_api import sync_playwright
import json
JS="""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round((r.left-D.left)/k),Math.round((r.top-D.top)/k),Math.round(r.width/k),Math.round(r.height/k)]; };
 const o={}; document.querySelectorAll('[data-trait]').forEach(c=>{ const r=c.getBoundingClientRect(); if(r.width>50) o['trait:'+(c.id||c.className)]=[c.getAttribute('data-trait'), R(c)]; });
 o.tenirZone=R(document.getElementById('tenirZone')); o.tenirCv=R(document.getElementById('tenirCv'));
 try{ const f=window._onde.onde; o.ondeType=typeof f; o.ondeSrc=String(f).slice(0,160); }catch(e){ o.err=String(e); }
 return o; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); c=b.new_context(viewport={'width':430,'height':932}); c.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=c.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in (('fiche à tenir',"openDetail(promises.find(q=>q.title==='faire les crêpes').id)"),('fiche chiche',"openDetail(promises.find(q=>q.title==='courir dimanche').id)"),('page +',"document.getElementById('createBtn').click(); setTimeout(()=>{const t=document.querySelectorAll('.tile')[0]; if(t) t.click();},600)")):
        pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(600); pg.evaluate("()=>{%s}"%js); pg.wait_for_timeout(2600)
        print(nom, json.dumps(pg.evaluate(JS),ensure_ascii=False)[:900])
        if nom=='page +': print(pg.evaluate("()=>{const s=document.getElementById('createSheet'); return [s.className, [...s.querySelectorAll('canvas')].map(c=>(c.id||c.className)+':'+c.getAttribute('data-trait'))]}"))
    b.close()
