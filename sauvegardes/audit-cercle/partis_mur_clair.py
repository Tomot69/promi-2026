# LE MUR DES QUATRE RÉGLAGES, DANS LES DEUX THÈMES. La prise en clair avait échoué sans que la raison soit gardée :
# on mesure l'état à chaque étape (Peaufiner ouvert ? le bloc existe ? sa boîte ?) avant de capturer.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ETAT = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const b=document.querySelector('#detailPoster .s2-cercle'); const t=document.querySelector('#dpDetails .dpd-tog');
  const box=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return {x:+((r.left-dv.left)/s).toFixed(1), y:+((r.top-dv.top)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1), vis:e.checkVisibility()}; };
  return {poster: document.getElementById('detailPoster').classList.contains('show'), peauf: document.getElementById('detailPoster').className,
          tog: !!t, cercle: !!b, boite: box(b), rangees: b ? [...b.querySelectorAll('.s2-rang,.row,.field')].length : 0,
          px: b ? (r=>({x:r.left,y:r.top,w:r.width,h:r.height}))(b.getBoundingClientRect()) : null}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('light', 'dark'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        pg.evaluate(BASE)
        pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }")
        pg.wait_for_timeout(1800); e1 = pg.evaluate(ETAT)
        pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t) t.click();}")
        pg.wait_for_timeout(2000); e2 = pg.evaluate(ETAT)
        pg.evaluate("""()=>{ const b=document.querySelector('#detailPoster .s2-cercle'); if(!b) return; const e=b.querySelector('.s2-encart');
            if(e) e.style.setProperty('visibility','hidden','important'); }""")
        pg.wait_for_timeout(500); e3 = pg.evaluate(ETAT)
        R[th] = {'avant Peaufiner': e1['boite'], 'après Peaufiner': e2['boite'], 'sans encart': e3['boite'], 'rangées': e3['rangees'], 'tog': e2['tog']}
        print('%-6s  tog=%s  avant=%s  après=%s  rangées=%s' % (th, e2['tog'], e1['boite'], e2['boite'], e3['rangees']))
        if e3['px'] and e3['px']['w'] > 4 and e3['px']['h'] > 4:
            r = e3['px']; pg.screenshot(path=os.path.join(OUT, '%s_mur_rangees.png' % th), clip={'x': r['x'], 'y': r['y'], 'width': r['w'], 'height': r['h']})
            print('        capturé %s_mur_rangees.png' % th)
        else:
            print('        ⚠ pas de boîte à capturer en %s' % th)
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'mur.json'), 'w'), ensure_ascii=False, indent=1)
