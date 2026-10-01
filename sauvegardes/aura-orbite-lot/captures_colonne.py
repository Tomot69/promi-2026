# Les captures de la colonne, à 2×, sur l'app INSÉRÉE — gardées sur disque, jamais envoyées (Tom, 10 sept.).
# Deux thèmes × deux phrases (deux lignes : 0 ; une ligne : 1) × deux positions (ouverture, défilé au bout).
import os, sys
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(700)
        for i, nom in ((0, 'deux_lignes'), (1, 'une_ligne')):
            pg.evaluate("(i)=>_aura.mot(i)", i); pg.wait_for_timeout(400)
            pg.evaluate("()=>{document.getElementById('auCadre').scrollTop=0;}"); pg.wait_for_timeout(300)
            pg.query_selector('#device').screenshot(path=os.path.join(OUT, 'colonne_%s_%s_ouverture.png' % (th, nom)))
            h = pg.evaluate("()=>{const c=document.getElementById('auCadre'); c.scrollTop=c.scrollHeight; return c.scrollTop;}")
            pg.wait_for_timeout(400)
            pg.query_selector('#device').screenshot(path=os.path.join(OUT, 'colonne_%s_%s_defile.png' % (th, nom)))
            print(th, nom, 'défile de %d px' % h)
            pg.evaluate("()=>{document.getElementById('auCadre').scrollTop=0;}")
        pg.evaluate("()=>_aura.mot(null)")
    print('ERREURS JS', er[:3]); b.close()
print(sorted(os.listdir(OUT)))
