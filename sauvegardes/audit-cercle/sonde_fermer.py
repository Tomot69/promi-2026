# Deux observations, hors chantier : que fait le « ✕ FERMER » du Peaufiner d'une FICHE ? et le gardé de côté au repos, en clair.
from playwright.sync_api import sync_playwright
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('light')")
    pg.evaluate(BASE); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1400)
    pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
    b = pg.evaluate("()=>{ const f=document.querySelector('#detailPoster .s2-fermer'); const r=f.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    pg.mouse.click(b[0], b[1]); pg.wait_for_timeout(1200)
    print('fiche · après ✕ FERMER du Peaufiner :', pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return {fiche:d.classList.contains('show'), peaufiner:d.classList.contains('s2-ouv')}; }"))
    pg.evaluate(BASE); pg.evaluate("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}"); pg.wait_for_timeout(2200)
    print('gardé au repos, clair :', pg.evaluate("""()=>{ const cs=document.getElementById('createSheet'), dv=document.getElementById('device').getBoundingClientRect();
      return [...cs.querySelectorAll('*')].filter(e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}) && /Je me promets/.test([...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(''))).map(e=>{ const r=e.getBoundingClientRect(); return [(e.id||String(e.className).split(' ')[0]), e.textContent.trim().slice(0,30), Math.round(r.left-dv.left), Math.round(r.top-dv.top), Math.round(r.width), Math.round(r.height), getComputedStyle(e).opacity]; }); }"""))
    pg.locator('#device').screenshot(path='bandeau/garde_repos_clair.png')
    br.close()
