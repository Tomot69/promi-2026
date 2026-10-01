from playwright.sync_api import sync_playwright
CLIQUE=r"""(t)=>{ const L=[...document.querySelectorAll('#device *')].filter(e=>{const r=e.getBoundingClientRect(); const c=getComputedStyle(e); return r.width>0&&r.height>0&&c.visibility!=='hidden'&&c.display!=='none';});
  const e=L.find(e=>(e.getAttribute('aria-label')||'').toLowerCase()===t.toLowerCase()) || L.filter(e=>(e.textContent||'').trim().toLowerCase()===t.toLowerCase()).pop();
  if(!e) return 'introuvable'; e.click(); return (e.id||e.className||e.tagName)+''; }"""
OUV="()=>[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show,[id].show')].map(e=>e.id).filter(Boolean)"
ESSAIS=[('accueil',['STUDIO']),('accueil',['Partager']),('accueil',['AURA']),('accueil',['Réglages']),
        ('reglages',['Langue']),('reglages',['Vie privée']),('reglages',['Le Cercle']),('reglages',['Arranger la Toile']),
        ('aura',['?']),('accueil',['INDEX'])]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('ouverts au repos :', pg.evaluate(OUV))
    for dep,chemin in ESSAIS:
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400)
        if dep=='reglages': print('   réglages :', pg.evaluate(CLIQUE,'Réglages')); pg.wait_for_timeout(700)
        if dep=='aura': pg.evaluate(CLIQUE,'AURA'); pg.wait_for_timeout(900)
        for t in chemin: r=pg.evaluate(CLIQUE,t); pg.wait_for_timeout(900)
        print(dep, chemin, '→ cliqué', r, '· ouverts', pg.evaluate(OUV))
    b.close()
