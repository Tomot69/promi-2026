# v151 §7 : à la fin (3 touchers), l'air entre le bas de l'ENCRE de « La suite t'appartient. » et le haut des dalles (lu sur l'image, sombre)
import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
URL='http://127.0.0.1:8752/' + F
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True, color_scheme='dark')
    ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(2500); trace(pg, cdp); pg.wait_for_timeout(5200)
    for _ in range(3): toucher(cdp, pg, 215, 280); pg.wait_for_timeout(3800)
    pg.wait_for_timeout(1500)
    D = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); const e=document.querySelector('#onbV .onbv-l-der .onbv-k'); const q=e.getBoundingClientRect(); return [r.left,r.top,r.width/390,q.left,q.right,q.top,q.bottom]; }")
    png='scratchpad/v151/onb_fin_dalles_%s.png' % F.split('.')[0]; pg.screenshot(path=png)
    im=Image.open(png).convert('RGB'); s=2
    x0,x1,y0,y1=int(D[3]*s),int(D[4]*s),int(D[5]*s),int(D[6]*s)
    def fonce(c): return max(c)<40
    # bas de l'encre du mot : la dernière ligne qui porte de la crème dans sa boîte
    bas=None
    for y in range(y0, y1+40):
        if any(min(im.getpixel((x,y)))>180 for x in range(x0,x1,2)): bas=y
    # haut des dalles : la première ligne, sous l'encre, où plus d'un tiers de la largeur de l'appareil n'est pas le fond
    X0,X1=int(D[0]*s),int((D[0]+390*D[2])*s); haut=None
    for y in range(bas+2, im.height):
        n=sum(1 for x in range(X0,X1,4) if not fonce(im.getpixel((x,y)))); 
        if n > (X1-X0)/4*0.05: haut=y; break
    print(F, 'bas de l\'encre %.1f pt · haut des dalles %.1f pt · air %.1f pt' % ((bas/s-D[1])/D[2], (haut/s-D[1])/D[2], (haut-bas)/s/D[2]))
    b.close()
