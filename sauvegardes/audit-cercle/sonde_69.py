# CHANTIER 69 — au clic sur #addPromi, QUAND le nouveau Promi entre-t-il dans la liste ? et l'écouteur du lot tourne-t-il ?
from playwright.sync_api import sync_playwright
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(1000)
    print(pg.evaluate("""()=>new Promise(res=>{ const a=document.getElementById('addPromi'); const n0=promises.length, T=[], m0=Math.max(...promises.map(q=>q.id));
        const note=(k)=>T.push([k, promises.length, (promises.filter(q=>q.id>m0)[0]||{}).trait||null]);
        a.addEventListener('click', ()=>note('mon écouteur (bulle)'), false);
        window._ppPinceau = window._ppPinceau || null;
        const f=document.getElementById('fTitle'); if(f) f.value='essayer le pinceau';
        window._phrase=Object.assign({}, window._phrase||{}, {sens:'faire', qui:'Moi', titre:'essayer le pinceau', quand:'un jour'});
        a.click(); note('juste après click()'); Promise.resolve().then(()=>note('micro-tâche'));
        setTimeout(()=>note('0 ms'),0); setTimeout(()=>note('50 ms'),50); setTimeout(()=>note('200 ms'),200); setTimeout(()=>{ note('800 ms');
          res({n0, T, visible:a.checkVisibility(), meme:a===document.getElementById('addPromi'), pinceau:(window.promiPinceau?window.promiPinceau(null):'?')}); },800); })"""))
    br.close()
