# LE MUR DU CERCLE — OÙ EXISTE-T-IL VRAIMENT ? (Tom, 11 sept. : « les quatre réglages n'existent nulle part
# d'atteignable. Ni sur une fiche plantée, ni sur la page +, et Peaufiner ne s'ouvre jamais sur un gardé de côté. »)
# Vérifié à l'écran, pas supposé, deux thèmes, gratuit :
#   A · un Promi PLANTÉ À NEUF (par le bouton de la page +) → sa fiche → Peaufiner : le bloc y est-il ? visible ?
#   B · un Promi du jeu de démonstration (126) → Peaufiner : le bloc (le témoin de l'audit)
#   C · un gardé de côté → ce qui s'ouvre ; un Peaufiner s'ouvre-t-il ? le bloc ?
#   D · la page + → Peaufiner (#csBotBar) : le bloc ?
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'mur'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
BLOC = r"""(hote)=>{ const h=document.querySelector(hote); if(!h) return {hote:false};
  const b=h.querySelector('.s2-cercle'); const ouvert=(h.classList.contains('s2-ouv')||h.classList.contains('pp-peauf'));
  if(!b) return {hote:true, peaufiner_ouvert:ouvert, bloc:false};
  b.scrollIntoView({block:'center'});
  const r=b.getBoundingClientRect(), regs=[...b.querySelectorAll('.s2-reg')];
  const enc=b.querySelector('.s2-encart,.set-cercle');
  return {hote:true, peaufiner_ouvert:ouvert, bloc:true, visible:b.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}),
          taille:[Math.round(r.width),Math.round(r.height)], reglages:regs.length,
          flous:regs.filter(x=>/blur/.test(getComputedStyle(x).filter)).length,
          encart: enc? enc.textContent.replace(/\s+/g,' ').trim() : null}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        # A · planter à neuf
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
        avant = pg.evaluate("()=>promises.map(p=>p.id)")
        pg.evaluate("()=>{const t=document.getElementById('fTitle'); t.value='aller voir la mer'; document.getElementById('addPromi').click();}"); pg.wait_for_timeout(2600)
        neuf = pg.evaluate("(av)=>{const n=promises.filter(p=>av.indexOf(p.id)<0); return n.length?n[0].id:null;}", avant)
        pg.evaluate(BASE); pg.evaluate("(id)=>openDetail(id)", neuf); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"); pg.wait_for_timeout(1600)
        a = pg.evaluate(BLOC, '#detailPoster'); pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_A_plante.png' % th))
        # B · le témoin
        pg.evaluate(BASE); pg.evaluate("()=>openDetail(126)"); pg.wait_for_timeout(1400)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"); pg.wait_for_timeout(1600)
        b = pg.evaluate(BLOC, '#detailPoster')
        # C · un gardé de côté
        drafts = pg.evaluate("()=>promises.filter(p=>p.draft).map(p=>({id:p.id,t:p.title||p.t||p.titre}))")
        c = {'gardes': drafts}
        if drafts:
            pg.evaluate(BASE); pg.evaluate("(id)=>openDetail(id)", drafts[0]['id']); pg.wait_for_timeout(1600)
            c['ouvre'] = pg.evaluate("()=>[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')")
            c['barre'] = pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(!x) return 'aucune'; const r=x.getBoundingClientRect(); return {vis:x.checkVisibility(), w:Math.round(r.width), h:Math.round(r.height)};}")
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_C_garde_ouvert.png' % th))
            pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"); pg.wait_for_timeout(1600)
            c['apres_toucher_barre'] = pg.evaluate(BLOC, '#detailPoster')
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_C_garde_barre.png' % th))
        # D · la page +
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
        pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1500)
        d = pg.evaluate(BLOC, '#createSheet')
        R[th] = {'A_plante_%s' % neuf: a, 'B_temoin_126': b, 'C_garde': c, 'D_page_plus': d}
        print('\n== %s\n  A · Promi planté à neuf (%s) : %s\n  B · témoin 126 : %s\n  C · gardé de côté : %s\n  D · page + : %s' % (th, neuf, a, b, c, d))
        ctx.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'verif_mur.json'), 'w'), ensure_ascii=False, indent=1)
