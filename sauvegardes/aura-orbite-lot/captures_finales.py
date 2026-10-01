# Captures finales à 2× — l'app INSÉRÉE (aucune injection), 430 × 932 pour que #device
# sorte exactement à 390 × 844 (§8 : un comparateur qui redimensionne ment).
# Deux thèmes × quatre états : l'écran, après une caresse, la personne ouverte, l'état vide.
import os, json
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, 'finales'); os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def ouvre():
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(700)
    def cap(nom):
        pg.query_selector('#device').screenshot(path=os.path.join(OUT, nom + '.png'))
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        ouvre(); cap('aura_%s' % th)
        # une caresse, lente, en travers de la boule
        r = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,R:r.width*0.392};}")
        pg.mouse.move(r['cx'] - 0.5 * r['R'], r['cy'] + 0.1 * r['R']); pg.mouse.down()
        for k in range(1, 21):
            pg.mouse.move(r['cx'] - 0.5 * r['R'] + k * 0.05 * r['R'], r['cy'] + 0.1 * r['R']); pg.wait_for_timeout(35)
        pg.mouse.up()
        for _ in range(150):
            if pg.evaluate("()=>_aura.etat().traces>0"): break
            pg.wait_for_timeout(100)
        pg.wait_for_timeout(1200); cap('aura_%s_caresse' % th)
        pg.evaluate("()=>_aura.relisse()")
        # la personne, ouverte d'un toucher
        n = pg.evaluate("()=>{const n=document.querySelector('#auraScreen .au-gp .au-n .au-nb');if(!n)return null;const r=n.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];}")
        if n:
            pg.mouse.click(n[0], n[1]); pg.wait_for_timeout(1200); cap('aura_%s_personne' % th)
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400)
        # l'état vide
        pg.evaluate("()=>{window.__d=promises.map(p=>[p,p.draft]);promises.forEach(p=>{p.draft=true;});}")
        ouvre(); cap('aura_%s_vide' % th)
        pg.evaluate("()=>{(window.__d||[]).forEach(x=>{x[0].draft=x[1];});}")
    print('état', json.dumps(pg.evaluate("()=>_aura.etat()"))[:300])
    print('ERREURS JS', er[:3])
    # ⚑ UNE VITESSE NE SE JUGE PAS SUR UNE IMAGE FIXE : 20 s de rotation lente, en temps réel,
    #   filmées (thème sombre, rien ne touche la boule). Un tour = 2 min : sur 20 s, 1/6 de tour.
    cx = b.new_context(viewport={'width': 430, 'height': 932}, record_video_dir=OUT,
                       record_video_size={'width': 430, 'height': 932})
    pv = cx.new_page()
    pv.goto('http://127.0.0.1:8752/app.html'); pv.wait_for_timeout(6800)
    pv.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pv.evaluate("()=>setTheme('dark')"); pv.wait_for_timeout(400)
    pv.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pv.wait_for_timeout(250); pv.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pv.wait_for_timeout(250)
        if pv.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    l0 = pv.evaluate("()=>_aura.etat().lac"); pv.wait_for_timeout(20000); l1 = pv.evaluate("()=>_aura.etat().lac")
    print('film : %.4f rad en 20 s -> %.4f rad/s (decide 0.0524)' % (l1 - l0, (l1 - l0) / 20))
    vid = pv.video.path(); cx.close()
    os.replace(vid, os.path.join(OUT, 'aura_rotation_20s.webm'))
    print('captures :', sorted(os.listdir(OUT)))
    b.close()
