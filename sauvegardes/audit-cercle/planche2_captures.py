# LE CERCLE, PLANCHE 2 — LA MATIÈRE, PRISE DANS L'APP (11 sept. 2026). Rien n'est écrit dans app.html.
# Décisions de Tom appliquées le temps de la prise :
#   · l'encart du mur porte « ✦ Le Cercle », SEUL — il nomme l'offre, pas son contenu (Q201) ;
#   · la page + reçoit le mur : la brique même de l'app, `window._s2Briques.cercle()`, accrochée en fin de sa liste
#     (après PIÈCES JOINTES — la page + n'a ni commentaires, ni relance, ni suppression) ;
#   · l'état abonné est celui que l'app pose déjà (`setPremium(true)` + `_cerclePaye()`), le mur de la page + compris.
# Sorties : planche2/<cadre>_<thème>.png + planche2/cotes.json (la place de l'encart, pour l'annotation du doigt).
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'planche2'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
PAGEPLUS = [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 500),
  ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
  ("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu();}", 700),
  ("()=>document.getElementById('csBotBar').click()", 1500)]
ENCART_SEUL = r"""(hote)=>{ const H=document.querySelector(hote);
  H.querySelectorAll('.s2-encart .s2-enc-s').forEach(s=>s.style.setProperty('display','none','important'));
  return [...H.querySelectorAll('.s2-encart .s2-enc-t')].map(t=>t.textContent); }"""
# ⚠ PREMIÈRE ÉCRITURE : le bloc était accroché une fois — et la page + REBÂTIT sa liste derrière (peaufBati relancé par
# les écouteurs du pinceau, [80, 260, 600] ms après chaque clic) : la mesure suivante ne le trouvait plus (cotes None).
# C'est « repeindre derrière le moteur » (CLAUDE §8). On pose donc un OBSERVATEUR sur la feuille, qui remet le bloc
# chaque fois que la liste est refaite SANS lui — en comparant avant d'agir (sinon il se réveille lui-même). C'est aussi la
# forme que prendra l'intégration.
MUR_PAGEPLUS = r"""()=>{ const cs=document.getElementById('createSheet');
  const pose=()=>{ const l=cs.querySelector(':scope > .dpd-corps .s2-liste')||cs.querySelector('.s2-liste');
    if(!l || !cs.classList.contains('pp-peauf')) return false;
    if(l.querySelector('.s2-cercle')) return false;                   /* comparer avant d'agir */
    l.appendChild(window._s2Briques.cercle());
    l.querySelectorAll('.s2-encart .s2-enc-s').forEach(s=>s.style.setProperty('display','none','important'));
    try{ if(window._cerclePaye) window._cerclePaye(); }catch(e){}
    return true; };
  if(!window.__murPP){ window.__murPP=new MutationObserver(()=>pose()); window.__murPP.observe(cs,{childList:true,subtree:true}); }
  pose();
  const l=cs.querySelector('.s2-liste'); return l ? l.querySelectorAll('.s2-cercle .s2-reg').length + ' réglages' : 'pas de liste'; }"""
COTES = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const b=document.querySelector(hote+' .s2-cercle'); if(!b) return null; b.scrollIntoView({block:'center'});
  const q=(e)=>{ if(!e) return null; const r=e.getBoundingClientRect(); return {x:(r.left-dv.left)/s, y:(r.top-dv.top)/s, w:r.width/s, h:r.height/s,
     vis:e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})}; };
  return {bloc:q(b), encart:q(b.querySelector('.s2-encart')),
          flous:[...b.querySelectorAll('.s2-reg')].map(r=>getComputedStyle(r).filter), touchable:[...b.querySelectorAll('.s2-reg')].map(r=>getComputedStyle(r).pointerEvents)}; }"""
C = {}
def prise(pg, nom, th):
    pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s.png' % (nom, th)))
def joue(pg, steps):
    for js, w in steps:
        pg.evaluate(js); pg.wait_for_timeout(w)
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>document.fonts.ready"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        for mode in ('gratuit', 'abonne'):
            pg.evaluate("(v)=>setPremium(v)", mode == 'abonne'); pg.wait_for_timeout(400)
            for nom, pid in (('fiche_promi', 126), ('fiche_chiche', 127)):
                joue(pg, [(BASE, 200), ("(id)=>openDetail(%d)" % pid, 1400)])
                if mode == 'gratuit' and nom == 'fiche_promi': prise(pg, 'fiche_promi_repos', th)
                joue(pg, [(PEAUF, 1600)])
                pg.evaluate(ENCART_SEUL, '#detailPoster')
                c = pg.evaluate(COTES, '#detailPoster'); pg.wait_for_timeout(500)
                prise(pg, '%s_%s' % (mode, nom), th); C['%s_%s_%s' % (mode, nom, th)] = c
                print(th, mode, nom, c and {k: c[k] for k in ('encart', 'flous', 'touchable')})
            joue(pg, PAGEPLUS)
            r = pg.evaluate(MUR_PAGEPLUS); pg.wait_for_timeout(900)   # laisser passer les rebâtisseurs de la liste
            c = pg.evaluate(COTES, '#createSheet'); pg.wait_for_timeout(500)
            prise(pg, '%s_pageplus' % mode, th); C['%s_pageplus_%s' % (mode, th)] = c
            print(th, mode, 'page +', r, c and {k: c[k] for k in ('encart', 'flous', 'touchable')})
            # un gardé de côté rouvre la page + (openDetail → reprendreBrouillon) : il reçoit le même mur
            joue(pg, [(BASE, 200), ("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}", 1800),
                      ("()=>document.getElementById('csBotBar').click()", 1500)])
            r = pg.evaluate(MUR_PAGEPLUS); pg.wait_for_timeout(700)
            c = pg.evaluate(COTES, '#createSheet'); pg.wait_for_timeout(500)
            prise(pg, '%s_garde' % mode, th); C['%s_garde_%s' % (mode, th)] = c
            print(th, mode, 'gardé de côté', r, c and {k: c[k] for k in ('encart', 'flous', 'touchable')})
        ctx.close()
    br.close()
json.dump(C, open(os.path.join(OUT, 'cotes.json'), 'w'), ensure_ascii=False, indent=1)
print('écrit', OUT)
