import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src=open('redteam_premiere_froid.py',encoding='utf-8').read(); LENT=src.split('LENT = r"""')[1].split('"""')[0]
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b,onb=False,guide=False); ctx.add_init_script(CLAV)
    if '--lent' in sys.argv: ctx.add_init_script(LENT)
    pg=B.ouvre(ctx,'app.html',attente=7000)
    B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter')
    for i in range(70):
        r=pg.evaluate("""()=>{ const e=document.querySelector('#onbPh .onbv-pm[data-onb=parole]'); if(!e) return null; const ph=document.getElementById('onbPh');
          const f=x=>x?((x.style.getPropertyValue('clip-path')||'').slice(0,30)+(x.__trace?' T':'')):'-';
          return [Math.round(performance.now()), ph.style.visibility, f(ph), f(e), f(e.querySelector('.v200-mt')), (e.textContent||'').slice(0,26), e.className, !!document.querySelector('#onbPh canvas[data-trace], #onbV canvas[data-trace]'), (window.TraceLettres.journal||[]).slice(-1).map(j=>j.quoi+':'+(j.texte||j.car||'')).join()]; }""")
        if i%3==0: print(r)
        pg.wait_for_timeout(100)
    b.close()
