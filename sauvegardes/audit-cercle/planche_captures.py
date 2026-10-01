# LE CERCLE — LA MATIÈRE DE LA PLANCHE, PRISE DANS L'APP (11 sept. 2026).
# Rien n'est écrit dans app.html. Deux sortes d'images :
#  1 · les VRAIES dalles des trois mondes du Cercle — Toile.dalleTrame(cv, id, 1, monde), échelle 1, le monde passé en
#      4ᵉ argument (le monde courant, seul `m` changé) : sillons, gravure, terrazzo ;
#  2 · deux écrans de l'app avec les LIBELLÉS DÉJÀ DÉCIDÉS posés dans la page, le temps de la capture :
#      · le Studio sur un monde payant — Q106 (rien au repos que l'encart du §3.8) et Q117 (« ✦ Le Cercle / sillons,
#        gravure, terrazzo », « Adopte Terrazzo — 1 € » au doigt), sans l'ombre de texte (§6) ;
#      · les Réglages — l'encart porte le sous-titre du §3.8 (« importance, récurrence, rappels, mémoire »), sans halo.
# Viewport 430 × 932 → #device 390 × 844, DPR 2.
import os, base64
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'planche')
os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"

DALLE = r"""(a)=>{ const [w, id, px] = a; const cv=document.createElement('canvas'); cv.width=px; cv.height=px;
  cv.style.cssText='position:fixed;left:0;top:0;width:'+(px/2)+'px;height:'+(px/2)+'px;opacity:.01;pointer-events:none';
  document.body.appendChild(cv);
  const m = Object.assign({}, Toile.mondeCourant(), {m:w});
  const ok = Toile.dalleTrame(cv, id, 1, m);
  const url = cv.toDataURL('image/png'); cv.remove(); return {ok, monde:m, url}; }"""

STUDIO_PATCH = r"""(doigt)=>{
  const st=document.getElementById('studioScreen'), dark=!st.classList.contains('stp-clair');
  const cta=document.getElementById('stLockCta'), t=cta.querySelector('.sc-t'), s=cta.querySelector('.sc-s'), g=cta.querySelector('.sc-go'), tx=cta.querySelector('.sc-tx');
  const P=(e,k,v)=>e&&e.style.setProperty(k,v,'important');
  t.textContent='✦ Le Cercle'; s.textContent='sillons, gravure, terrazzo';
  const fond = dark?'#F4EEE1':'#16171B', teinte = dark?'#AE86F2':'#CBAAFF';
  P(cta,'background',fond); P(cta,'border','0'); P(cta,'border-radius','26px'); P(cta,'justify-content','center');
  P(tx,'align-items','center'); P(tx,'text-align','center'); P(tx,'gap','5px'); P(tx,'width','100%');
  P(tx,'display','flex'); P(tx,'flex-direction','column');
  [t,s].forEach(e=>{P(e,'color',teinte); P(e,'-webkit-text-fill-color',teinte); P(e,'text-shadow','none'); P(e,'opacity','1');});
  P(t,'font-family','Bricolage'); P(t,'font-weight','700'); P(t,'font-size','22px'); P(t,'letter-spacing','-.02em');
  P(s,'font-family','Bricolage'); P(s,'font-weight','600'); P(s,'font-size','15px'); P(s,'letter-spacing','0');
  if(g) P(g,'display','none');
  const buy=document.getElementById('stLockBuy'), btx=document.getElementById('stBuyTx'), arr=buy&&buy.querySelector('.st-buy-arr');
  /* ⚠ LE ROTATEUR DE L'APP réécrit #stBuyTx au hasard à chaque changement de classe du Studio (CLAUDE §8) : le libellé
     posé était remplacé avant la prise. Le temps de la capture seulement, on rend son textContent sourd aux écritures. */
  if(doigt){ P(buy,'display','flex'); btx.textContent='Adopte Terrazzo — 1 €';
             Object.defineProperty(btx,'textContent',{configurable:true,get(){return 'Adopte Terrazzo — 1 €';},set(){}});
             [btx,arr].forEach(e=>{P(e,'text-shadow','none');}); }
  else P(buy,'display','none');
  return {cta:cta.textContent.trim(), buy: doigt ? btx.textContent : '(au repos : rien)'}; }"""

REGLAGES_PATCH = r"""()=>{
  const b=document.getElementById('openPlusTop'), t=b.querySelector('.sc-t'), s=b.querySelector('.sc-s');
  const P=(e,k,v)=>e&&e.style.setProperty(k,v,'important');
  t.textContent='✦ Le Cercle'; s.textContent='importance, récurrence, rappels, mémoire';
  [t,s].forEach(e=>P(e,'text-shadow','none'));
  b.scrollIntoView({block:'center'}); return b.textContent.trim(); }"""

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.fonts.ready")
    # 1 · les dalles (deux Promi réels, trois mondes)
    for w in ('sillons', 'gravure', 'terrazzo'):
        for pid in (125, 129, 134, 139):
            r = pg.evaluate(DALLE, [w, pid, 240])
            open(os.path.join(OUT, 'dalle_%s_%d.png' % (w, pid)), 'wb').write(base64.b64decode(r['url'].split(',')[1]))
            print('dalle', w, pid, 'peinte' if r['ok'] is not False else 'ÉCHEC', r['monde'])
    # 2 · le Studio et les Réglages, deux thèmes, gratuit
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        for doigt in (False, True):
            pg.evaluate(BASE); pg.wait_for_timeout(200)
            pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(1900)
            pg.evaluate("()=>{const d=document.querySelector('#studioScreen [data-w=\"terrazzo\"]'); if(d) d.click();}"); pg.wait_for_timeout(1600)
            r = pg.evaluate(STUDIO_PATCH, doigt); pg.wait_for_timeout(400)
            pg.locator('#device').screenshot(path=os.path.join(OUT, 'studio_%s_%s.png' % (th, 'doigt' if doigt else 'repos')))
            print('studio', th, r)
        pg.evaluate(BASE); pg.wait_for_timeout(200)
        pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(1700)
        r = pg.evaluate(REGLAGES_PATCH); pg.wait_for_timeout(500)
        pg.locator('#device').screenshot(path=os.path.join(OUT, 'reglages_%s.png' % th))
        print('réglages', th, r)
    br.close()
print('écrit dans', OUT)
