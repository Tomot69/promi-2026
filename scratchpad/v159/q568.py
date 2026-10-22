import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_suite_libelle.py').read().split('ONB = {')[0].split('res = []')[1].split('def juge')[0])
src=open('redteam_suite_libelle.py').read(); CL=src.split('CLAVIER = """')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, onb=False, guide=False); ctx.add_init_script(CL); pg=B.ouvre(ctx,'app.html',attente=7000)
    B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
    B.tap_sel(pg,'[data-onb="parole"]'); pg.wait_for_timeout(600); pg.keyboard.type('appeler ma grand-mère chaque dimanche',delay=15); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>{const ph=document.getElementById('onbPh');const rg=document.createRange();rg.selectNodeContents(ph);return {h:ph.offsetHeight,fs:getComputedStyle(ph).fontSize,lh:getComputedStyle(ph).lineHeight,html:ph.innerHTML.slice(0,300),r:[...rg.getClientRects()].map(q=>[Math.round(q.top),Math.round(q.height),Math.round(q.width)])}}"""))
    b.close()
