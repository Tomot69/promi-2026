# LE MUR DES QUATRE RÉGLAGES — reprise. La passe précédente découpait aux coordonnées BRUTES d'un bloc situé à y=806,
# donc HORS FENÊTRE (932 de haut) : Playwright rogne sur ce qui est à l'écran et rend la barre Peaufiner + du noir.
# Ici : on amène le bloc dans la fenêtre, on RE-MESURE après, et on REFUSE de capturer si le rectangle n'y tient pas.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
VW, VH = 430, 932
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
MES = r"""()=>{ const b=document.querySelector('#detailPoster .s2-cercle'); if(!b) return null; const r=b.getBoundingClientRect();
  return {x:r.left, y:r.top, w:r.width, h:r.height, vis:b.checkVisibility(),
          enfants:[...b.children].map(e=>e.className||e.tagName)}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        pg.evaluate(BASE)
        pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }")
        pg.wait_for_timeout(1800)
        pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t) t.click();}")
        pg.wait_for_timeout(2000)
        pg.evaluate("""()=>{ const b=document.querySelector('#detailPoster .s2-cercle'); if(!b) return; const e=b.querySelector('.s2-encart');
            if(e) e.style.setProperty('visibility','hidden','important'); b.scrollIntoView({block:'center'}); }""")
        pg.wait_for_timeout(700)
        m = pg.evaluate(MES)
        dedans = m and m['x'] >= 0 and m['y'] >= 0 and m['x'] + m['w'] <= VW and m['y'] + m['h'] <= VH
        print('%-6s boîte après mise en fenêtre : x=%.0f y=%.0f %.0fx%.0f  dans la fenêtre : %s' % (th, m['x'], m['y'], m['w'], m['h'], dedans))
        print('        enfants :', m['enfants'])
        R[th] = {'boite': m, 'dans_fenetre': dedans}
        if dedans:
            pg.screenshot(path=os.path.join(OUT, '%s_mur_rangees.png' % th), clip={'x': m['x'], 'y': m['y'], 'width': m['w'], 'height': m['h']})
            print('        capturé')
        else:
            print('        ⚠ REFUS de capturer : le rectangle ne tient pas dans la fenêtre')
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'mur2.json'), 'w'), ensure_ascii=False, indent=1)
