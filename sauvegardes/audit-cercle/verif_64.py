# CHANTIER 64 — vérifié à l'écran, deux thèmes : page + et gardé de côté, Peaufiner ouvert puis refermé par son « ✕ FERMER ».
import os, sys, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'bandeau' if len(sys.argv) <= 1 else 'bandeau_preuve'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
J = r"""()=>{ const cs=document.getElementById('createSheet'), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const vis=(e)=>!!(e&&e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&e.getBoundingClientRect().width>1);
  /* la barre du bas (#csBotBar) est opaque et fixe : la liste défile DESSOUS, voulu — ce n'est pas un recouvrement */
  const T=[...cs.querySelectorAll('*')].filter(e=>vis(e)&&!e.closest('#csBotBar')&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>{ const r=e.getBoundingClientRect(); return {t:e.textContent.trim().slice(0,20), x:(r.left-dv.left)/s, y:(r.top-dv.top)/s, w:r.width/s, h:r.height/s}; })
    .filter(a=>a.y<844 && a.y+a.h>0);
  const inter=[]; for(let i=0;i<T.length;i++) for(let j=i+1;j<T.length;j++){ const a=T[i], b=T[j]; const ox=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x), oy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y); if(ox>2&&oy>2) inter.push(a.t+' ∩ '+b.t); }
  return {peauf:cs.classList.contains('pp-peauf'), show:cs.classList.contains('show'), enh:vis(cs.querySelector(':scope > .enh')), photo:[...cs.querySelectorAll('.ph-photo-btn')].some(vis),
          tete:vis(cs.querySelector('.s2-tete')), fermer:vis(cs.querySelector('.s2-fermer')), marque:vis(cs.querySelector('.cs-mark')), inter}; }"""
KO = []
def ok(nom, c, d):
    print('   %s %s  %s' % ('✓' if c else '✗', nom, d));
    if not c: KO.append(nom)
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        print('════', th)
        for chemin in ('page +', 'gardé de côté'):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
            pg.evaluate(BASE); pg.wait_for_timeout(200)
            # ⚠ ON ATTEND UN ÉTAT, PAS UNE DURÉE : un toucher sur la tuile pendant l'animation d'ouverture est perdu (vu le 11 sept.,
            #   nuit : la page + restait sur le choix des natures, et le contrôle mesurait un autre écran)
            if chemin == 'page +':
                pg.evaluate("()=>document.getElementById('createBtn').click()")
                for i in range(15):
                    pg.wait_for_timeout(200)
                    if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-choix')"): break
                for essai in range(5):
                    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(700)
                    if pg.evaluate("()=>{ const cs=document.getElementById('createSheet'), b=document.getElementById('csBotBar'); return !cs.classList.contains('pp-choix') && !!b && b.checkVisibility(); }"): break
            else:
                pg.evaluate("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}")
                for i in range(15):
                    pg.wait_for_timeout(200)
                    if pg.evaluate("()=>{ const b=document.getElementById('csBotBar'); return document.getElementById('createSheet').classList.contains('show') && !!b && b.checkVisibility(); }"): break
                pg.wait_for_timeout(400)
            r0 = pg.evaluate(J)
            ok('%s %s · au repos : le plateau et le rond photo sont là, comme avant' % (th, chemin), r0['enh'] and r0['marque'] and not r0['peauf'], r0)
            for essai in range(3):
                pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1800)
                if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-peauf')"): break
            r1 = pg.evaluate(J)
            ok('%s %s · Peaufiner : ni le plateau de la page +, ni le rond photo ; son en-tête, lui, est là' % (th, chemin), r1['peauf'] and not r1['enh'] and not r1['photo'] and r1['tete'] and r1['fermer'], {k: r1[k] for k in ('peauf', 'enh', 'photo', 'tete', 'fermer')})
            ok('%s %s · Peaufiner : aucun texte n’en recouvre un autre' % (th, chemin), not r1['inter'], r1['inter'])
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s_peauf.png' % (th, chemin.replace(' ', '_').replace('+', 'plus'))))
            b = pg.evaluate("()=>{ const f=document.querySelector('#createSheet .s2-fermer'); if(!f) return null; const r=f.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
            if not b:
                ok('%s %s · le Peaufiner s’ouvre (sinon rien n’est mesuré)' % (th, chemin), False, 'pas de « ✕ FERMER » : le Peaufiner ne s’est pas ouvert'); pg.context.close(); continue
            pg.mouse.click(b[0], b[1]); pg.wait_for_timeout(1200)
            r2 = pg.evaluate(J)
            # ⚑ il referme la FEUILLE — comme avant le lot (mesuré sur app-avant-64.html) : ma première écriture supposait un retour au
            #   repos de la page +, que le produit n'a jamais fait. Le contrat vise ce que le bouton fait, pas ce que j'imaginais.
            ok('%s %s · son « ✕ FERMER » fonctionne : il referme la feuille, comme avant le lot' % (th, chemin), not r2['show'] and not r2['peauf'], {k: r2[k] for k in ('show', 'peauf')})
            pg.context.close()
    br.close()
print('══ %d raté(s)' % len(KO)); [print('   ✗ ' + k) for k in KO]
