# LE TRAIT ENTIER — la création d'une Nuée se lance en traçant le trait ENTIER (0 → 390, mode complet du §2.6).
# On cherche sa zone de tracé sur la page +, on la capture ; et on reprend le geste d'un Promi rogné AU-DESSUS des mots.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ZONES = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  return [...document.querySelectorAll('#createSheet canvas, #createSheet [id*=race], #createSheet [class*=trace], #createSheet [id*=tenir]')]
    .map(e=>{ const r=e.getBoundingClientRect(); return {el:(e.id?'#'+e.id:'')+'.'+String(e.className).split(' ').slice(0,2).join('.'), vis:e.checkVisibility(),
      r:[+((r.left-dv.left)/s).toFixed(0), +((r.top-dv.top)/s).toFixed(0), +(r.width/s).toFixed(0), +(r.height/s).toFixed(0)]}; }).filter(x=>x.r[2]>20 && x.r[3]>10); }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        # la page + d'une NUÉE : sa zone de tracé porte le trait entier
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()")
        for i in range(15):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-choix')"): break
        for e in range(5):
            pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')].find(x=>x.dataset.kind==='nuee'); var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(800)
            if pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('pp-choix')"): break
        Z = pg.evaluate(ZONES); R['%s · page + Nuée' % th] = Z
        print(th, 'page + Nuée :'); [print('   ', z) for z in Z]
        pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_pageplus_nuee.png' % th))
        # le geste d'un Promi, rogné au-dessus des mots peints dans le canevas (les mots occupent le bas)
        pg.evaluate(BASE); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && q.who!=='moi' && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1900)
        t = pg.evaluate("()=>{ const z=document.getElementById('tenirZone'); const r=z.getBoundingClientRect(); return {x:r.left, y:r.top, w:r.width, h:r.height}; }")
        pg.screenshot(path=os.path.join(OUT, '%s_geste_rogne.png' % th), clip={'x': t['x'], 'y': t['y'], 'width': t['w'], 'height': t['h'] * 0.73})
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'zones_nuee.json'), 'w'), ensure_ascii=False, indent=1)
