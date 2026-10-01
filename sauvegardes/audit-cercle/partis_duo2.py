# LE TRAIT, DEUX ÉTATS, MÊME CANEVAS, MÊME CADRAGE :
#   · gratuit  — un Chiche NON tenu : ma moitié pleine, l'autre en points (mode 'points')
#   · Cercle   — un Chiche TENU À DEUX : les DEUX moitiés tracées (mode 'duo', l.14772-15051)
# Le trait vit dans la matière de la fiche (#dpTrameCv), pas dans #tenirZone (0x0 sur une parole tenue).
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
# choisit un chiche par état ; ne modifie RIEN (les deux existent dans le jeu ?) — on le dit dans le rapport
CH = r"""(tenu)=>{ const l = promises.filter(q=>!q.draft && q.chiche);
  const p = tenu ? l.find(q=>q.status==='tenu' && q.avec) : l.find(q=>q.status!=='tenu');
  if(!p) return {aucun:true, liste:l.map(q=>({id:q.id,t:q.title,s:q.status,a:q.avec||null}))};
  closeAll(); openDetail(p.id); return {id:p.id, titre:p.title, status:p.status, avec:p.avec||null}; }"""
BOITES = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, o={};
  ['dpTrameCv','detailPoster','tenirZone','tenirCv'].forEach(k=>{ const e=document.getElementById(k); if(!e) return; const r=e.getBoundingClientRect();
    o[k]={x:+((r.left-dv.left)/s).toFixed(1), y:+((r.top-dv.top)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1), px:{x:r.left,y:r.top,w:r.width,h:r.height}}; });
  o._dev={x:dv.left,y:dv.top,s:s}; return o; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        for cle, tenu in (('gratuit', False), ('cercle', True)):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
            pg.evaluate(BASE); c = pg.evaluate(CH, tenu); pg.wait_for_timeout(2200)
            b = pg.evaluate(BOITES); R['%s_%s' % (th, cle)] = {'promi': c, 'boites': b}
            print(th, cle, c if c.get('aucun') else (c['id'], c['titre'], c['status'], c['avec']), '| dpTrameCv', b.get('dpTrameCv') and [b['dpTrameCv']['x'], b['dpTrameCv']['y'], b['dpTrameCv']['w'], b['dpTrameCv']['h']])
            if b.get('dpTrameCv'):
                r = b['dpTrameCv']['px']
                pg.screenshot(path=os.path.join(OUT, '%s_trame_%s.png' % (th, cle)), clip={'x': r['x'], 'y': r['y'], 'width': r['w'], 'height': r['h']})
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_fiche_%s.png' % (th, cle)))
            pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'duo2.json'), 'w'), ensure_ascii=False, indent=1)
