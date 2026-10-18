# v150 : la page du trait (sombre) et la fin de l'onboarding après le 3e pas (clair) — captures pour moi
import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL='http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ('dark', 'light'):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, color_scheme=th)
        if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(2500)
        pg.screenshot(path='scratchpad/v150/onb_trait_%s.png' % th)
        trace(pg, cdp); pg.wait_for_timeout(5200)
        for _ in range(3): toucher(cdp, pg, 195, 260); pg.wait_for_timeout(3600)
        pg.screenshot(path='scratchpad/v150/onb_fin_%s.png' % th); ctx.close()
    b.close()
from PIL import Image
L=[Image.open('scratchpad/v150/onb_%s.png' % n) for n in ('trait_dark','fin_dark','fin_light')]
W=sum(i.width for i in L)+40; c=Image.new('RGB',(W,L[0].height),(0,0,0)); x=0
for i in L: c.paste(i,(x,0)); x+=i.width+20
c.resize((W//2,L[0].height//2)).save('scratchpad/v150/onb_trois.png')
