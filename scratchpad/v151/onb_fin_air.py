# v151 §6 §7 : à la fin de l'onboarding (3 touchers), l'air à l'encre entre « Tout le monde promet… » et « La suite t'appartient. », son centrage, et les couleurs de Primo…
import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
URL='http://127.0.0.1:8752/' + F
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ('dark', 'light'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True, color_scheme=th)
        if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(2500); trace(pg, cdp); pg.wait_for_timeout(5200)
        for _ in range(3): toucher(cdp, pg, 215, 280); pg.wait_for_timeout(3800)
        print(th, pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), K=D.width/390;
          const ink=e=>{ const r=document.createRange(); r.selectNodeContents(e); const b=r.getBoundingClientRect(); return [+((b.left-D.left)/K).toFixed(1), +((b.top-D.top)/K).toFixed(1), +((b.right-D.left)/K).toFixed(1), +((b.bottom-D.top)/K).toFixed(1)]; };
          const fin=document.querySelector('#onbV .onbv-l-fin'), der=document.querySelector('#onbV .onbv-l-der'), ton=document.querySelector('#onbV .onbv-ton');
          const a=ink(fin), d=ink(der); return {air:+(d[1]-a[3]).toFixed(1), der:d, centre:+(((d[0]+d[2])/2)-195).toFixed(1), ton:ton.textContent,
            k:[...document.querySelectorAll('#onbV .onbv-k')].map(e=>e.textContent.trim()+' '+getComputedStyle(e).webkitTextFillColor)}; }"""))
        ctx.close()
    b.close()
