# CHANTIER 70 — vérifié à l'écran : la liste du Peaufiner de la page + n'est plus rebâtie pour rien, le toucher sur l'encart ne se
# perd plus, et une VRAIE modification la met toujours à jour. Deux thèmes.
import os, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__))
OUTILS = open(os.path.join(D, 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
KO = []
def ok(nom, c, d):
    print('   %s %s  %s' % ('✓' if c else '✗', nom, d))
    if not c: KO.append(nom)
def ouvre(pg):
    pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()")
    for i in range(15):
        pg.wait_for_timeout(200)
        if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-choix')"): break
    for e in range(5):
        pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(700)
        if pg.evaluate("()=>{ const cs=document.getElementById('createSheet'), b=document.getElementById('csBotBar'); return !cs.classList.contains('pp-choix') && !!b && b.checkVisibility(); }"): break
    for e in range(3):
        pt = pg.evaluate("(s)=>window.__V.point(s)", '#csBotBar'); pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(1800)
        if pg.evaluate("()=>!!document.querySelector('#createSheet.pp-peauf .s2-encart')"): return True
    return False
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('light', 'dark'):
        print('════', th)
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
        if not ouvre(pg): ok('%s · le Peaufiner de la page + s’ouvre' % th, False, 'non'); pg.context.close(); continue
        # 1 · combien de fois la liste est-elle VIDÉE (ses enfants remplacés) en 3 s de repos, puis 3 s de défilement ?
        pg.evaluate("""()=>{ window.__R=0; const l=document.querySelector('#createSheet .s2-liste');
            window.__Rmo=new MutationObserver(ms=>{ if(ms.some(m=>m.removedNodes.length && [...m.removedNodes].some(x=>x.nodeType===1 && x.classList && (x.classList.contains('s2-reg')||x.classList.contains('s2-tete'))))) window.__R++; });
            window.__Rmo.observe(l,{childList:true}); }""")
        pg.wait_for_timeout(3000); repos = pg.evaluate("()=>window.__R")
        for k in range(6):
            pg.evaluate("(k)=>{const c=document.querySelector('#createSheet .dpd-corps')||document.getElementById('createSheet'); c.scrollTop=k*120;}", k); pg.wait_for_timeout(500)
        defil = pg.evaluate("()=>window.__R") - repos
        ok('%s · la liste n’est plus rebâtie pour rien (3 s de repos, 3 s de défilement)' % th, repos == 0 and defil == 0, ('repos', repos, 'défilement', defil))
        # 2 · le mur est toujours là, et l'encart répond 20 fois de suite (le toucher ne se perd plus)
        res = []
        for k in range(20):
            pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart'); pg.wait_for_timeout(200); pt = pg.evaluate("(s)=>window.__V.point(s)", '#createSheet .s2-encart')
            if not pt: res.append('·'); continue
            pg.evaluate("()=>{ window.__enc=document.querySelector('#createSheet .s2-encart'); }")
            pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(600)
            e = pg.evaluate("()=>window.__V.etat()"); res.append('✓' if (e['ps_show'] and e['dessus']) else '✗')
            pg.evaluate("()=>{ const s=document.getElementById('plusScreen'); s.classList.remove('show'); s.classList.remove('cercle-dessus'); }"); pg.wait_for_timeout(300)
        ok('%s · l’encart du mur ouvre le Cercle à chaque toucher (20)' % th, res.count('✓') == 20, ''.join(res))
        # 3 · une VRAIE modification met la liste à jour (le titre de la phrase change → l'en-tête suit)
        avant = pg.evaluate("()=>(document.querySelector('#createSheet .s2-titre')||{}).textContent")
        pg.evaluate("()=>{ window._phrase = Object.assign({}, window._phrase||{}, {titre:'aller voir la mer'}); if(window._ppTout) window._ppTout(); }"); pg.wait_for_timeout(500)
        apres = pg.evaluate("()=>(document.querySelector('#createSheet .s2-titre')||{}).textContent")
        ok('%s · une vraie modification rebâtit la liste (le titre suit)' % th, apres == 'aller voir la mer', (avant, '→', apres))
        n = pg.evaluate("()=>document.querySelectorAll('#createSheet .s2-cercle').length")
        ok('%s · le mur du Cercle est posé une fois, pas deux' % th, n == 1, n)
        pg.context.close()
    br.close()
print('══ %d raté(s)' % len(KO)); [print('   ✗ ' + k) for k in KO]
