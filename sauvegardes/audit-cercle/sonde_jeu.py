# SONDE : le jeu de démonstration de ce soir, et le Peaufiner de la fiche que les vérifications choisissent.
from playwright.sync_api import sync_playwright
CHOIX = "()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee) || promises.find(q=>!q.draft && !q.nuee); if(!p) return null; closeAll(); openDetail(p.id); return {id:p.id, titre:p.title, qui:p.who, statut:p.status}; }"
ETAT = """()=>{ const dp=document.getElementById('detailPoster'); const L=dp.querySelector('.s2-liste');
  return {show:dp.classList.contains('show'), ouv:dp.classList.contains('s2-ouv'), nuee:dp.classList.contains('dp-nuee'),
          rangs:L?[...L.children].map(e=>(e.querySelector('.s2-lab')||e).textContent.trim().slice(0,18)||e.className.slice(0,18)):null,
          cercle:!!dp.querySelector('.s2-cercle'), tog:!!document.querySelector('#dpDetails .dpd-tog')}; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('actuelle', 'http://127.0.0.1:8752/app.html'), ('avant le lot', 'http://127.0.0.1:8752/sauvegardes/app-avant-seuil-pilule.html')):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
        err = []; pg.on('pageerror', lambda e: err.append(str(e)[:200]))
        pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        print('\n==', nom)
        print('   jeu :', pg.evaluate("()=>promises.map(q=>[q.id, q.title.slice(0,22), q.status, q.who, q.draft?'gardé':'', q.chiche?'chiche':'', q.nuee||''])"))
        print('   choisi :', pg.evaluate(CHOIX)); pg.wait_for_timeout(1400)
        print('   après openDetail :', pg.evaluate(ETAT))
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"); pg.wait_for_timeout(1800)
        print('   après la barre :', pg.evaluate(ETAT))
        if err: print('   erreurs JS :', err[:3])
        ctx.close()
    br.close()
