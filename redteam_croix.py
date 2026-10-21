#!/usr/bin/env python3
"""redteam_croix.py — ⚑ v157 (Tom, C-173) : « × FERMER » DEVIENT UN SEUL « X ».

« Partout, “× FERMER” devient un seul “X”, sans mot. Il est toujours en PromiLate, en gras. Sa hauteur = la hauteur de capitale du titre à sa gauche sur la
même barre (PromiLate, Gilbert ou Atkinson selon la page), ± 1 pt. Sa couleur = celle de ce titre. Sa zone tactile : au moins 44 × 44 pt, centrée sur lui.
Juge : aucun “FERMER” nulle part ; hauteur du X = hauteur de capitale du titre ± 1 pt ; zone tactile ≥ 44 pt. »

Les 34 écrans de redteam_air, clair et sombre (appareil 390 × 844, ×3) ; sur chaque écran, la fermeture du dessus (celle que le doigt prend) :
  A · aucun texte « FERMER » / « Fermer » visible, nulle part sur l'écran ;
  B · la croix dit « X », en PromiLate ; la hauteur de son ENCRE (lue sur l'image : la croix peinte, puis effacée, le Studio et la Toile figés) = la hauteur
      de capitale du titre de sa rangée (le plus grand texte à sa gauche ; sa police lue sur la page, la hauteur de « H » mesurée par le juge) ± 1 pt ;
  C · sa couleur = celle du titre ;
  D · sa zone tactile fait au moins 44 × 44 pt, centrée sur l'encre (± 1,5 pt), et le doigt la prend à ses quatre coins (± 20 pt du centre).
Preuve : `--fichier=zz-av156.html` rougit (A, B).

⚑ v158 (Tom, C-173 RÉCIDIVE) — « Les X sont beaucoup plus gros que la capitale du titre. Le MÊME X partout : PromiLate, même taille, même couleur de rôle ;
sa taille est EXACTEMENT celle du “X” du mot “INDEX” du titre de la page Index ; seule sa position change. Juge : sur les 34 écrans × 2 thèmes, la boîte du X
est identique au pixel près (± 0,5 pt) à celle du X de “INDEX”. » CE QUE CE JUGE MESURAIT EN v157 : l'encre du X contre la capitale du titre, À L'ÉCHELLE 1
SEULEMENT (viewport 430 × 932 : l'appareil fait 390 pt sans réduction) — or le code divisait la taille par l'échelle de l'appareil : dans Safari (≈ 0,8)
le X sortait 22 à 27 % trop gros, et à l'échelle 1 l'erreur vaut zéro. Contrat remis au niveau (original : sauvegardes/redteam_croix-avant-v158.py) :
  B · l'ENCRE du X (largeur, hauteur) = celle du X de « INDEX » (le « x » du titre, lu sur l'image de la même façon), ± 0,5 pt — À DEUX ÉCHELLES : l'appareil
      à 1 (430 × 932) et réduit à 0,79 (330 × 714, comme dans Safari) ;
  C · sa couleur = celle du titre de sa barre (la couleur de rôle), à pleine opacité.
Preuve : `--fichier=zz-av157.html` rougit (B, à l'échelle 0,79).
"""
import sys, re, io, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
SEUL = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--seul=')), None)
air = io.open('redteam_air.py', encoding='utf-8').read()
ECRANS = [(m.group(1), m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$", air, re.M)]
ECRANS_TOUS = list(ECRANS)
if SEUL: ECRANS = [e for e in ECRANS if e[0] in SEUL.split(',')]
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
LIT = r"""()=>{ const dev=document.getElementById('device'), D=dev.getBoundingClientRect(), k=D.width/390;
  const vu=e=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return null; if(r.right<D.left||r.left>D.right||r.bottom<D.top||r.top>D.bottom) return null;
    for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return null; } return r; };
  const own=e=>[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('').trim();
  const mots=[]; document.querySelectorAll('body *').forEach(e=>{ const t=own(e); if(/fermer/i.test(t) && vu(e)) mots.push(t.slice(0,20)); });
  /* la fermeture du dessus : un élément de fermeture visible que le doigt prend en son centre */
  const C=[...document.querySelectorAll('.closeb, .s2-fermer, #npFermer, .ev-x, #shScopeClose, [data-close]')].filter(x=>{ const r=vu(x); if(!r) return false;
    const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!(h && (h===x || x.contains(h))); });
  const g=document.createElement('canvas').getContext('2d');
  return {mots:mots, croix:C.map(x=>{ const r=x.getBoundingClientRect(), cs=getComputedStyle(x);
    /* le titre de la rangée : le plus grand texte à gauche, dont le milieu tombe à ± 26 pt du milieu de la croix */
    const cy=r.top+r.height/2; let best=null, bf=0;
    const scr=x.closest('.screen, .sheet, .poster, #feedView, .feedview, #entierVue')||document.body;
    scr.querySelectorAll('*').forEach(e=>{ if(e===x||x.contains(e)||e.contains(x)) return; const t=own(e); if(!t||t==='X') return; const q=e.getBoundingClientRect(); if(q.width<2||q.right>r.left+2) return;
      if(Math.abs(q.top+q.height/2-cy)>26*k) return; if(!vu(e)) return; const f=parseFloat(getComputedStyle(e).fontSize)||0; if(f>bf){ bf=f; best=e; } });
    let T=null; if(best){ const c=getComputedStyle(best); g.font=c.fontStyle+' '+c.fontWeight+' 200px '+c.fontFamily; const m=g.measureText('H');
      const col=(c.webkitTextFillColor&&c.webkitTextFillColor!=='rgba(0, 0, 0, 0)')?c.webkitTextFillColor:c.color;
      T={txt:own(best).slice(0,20), fam:c.fontFamily.split(',')[0], cap:m.actualBoundingBoxAscent/200*parseFloat(c.fontSize)/1, col:col}; }
    const pts=[[-20,-20],[20,-20],[-20,20],[20,20]].map(([dx,dy])=>{ const h=document.elementFromPoint(r.left+r.width/2+dx*k, r.top+r.height/2+dy*k); return !!(h&&(h===x||x.contains(h))); });
    const gl=x.querySelector('.x157-g')||x; const gs=getComputedStyle(gl);   /* la police du GLYPHE (le conteneur peut porter celle d'un autre propriétaire) */
    return {sel:(x.id?'#'+x.id:'')+'.'+String(x.className).split(' ').slice(0,2).join('.'), txt:(x.textContent||'').trim(), fam:gs.fontFamily.split(',')[0], col:(cs.webkitTextFillColor&&cs.webkitTextFillColor!=='rgba(0, 0, 0, 0)')?cs.webkitTextFillColor:cs.color,
      op:+cs.opacity, clip:{x:r.left, y:r.top, width:r.width, height:r.height}, w:r.width/k, h:r.height/k, k:k, T:T, pts:pts}; })}; }"""
def encre(pg, clip, k, cache='.x157-g, .closeb > *, .s2-fermer > *'):
    import math; x0, y0 = math.floor(clip['x']), math.floor(clip['y']); clip = {'x': x0, 'y': y0, 'width': math.ceil(clip['x'] + clip['width']) - x0, 'height': math.ceil(clip['y'] + clip['height']) - y0}   # un cadre sur des pixels entiers : WebKit rééchantillonne une capture à cadre fractionnaire
    pg.evaluate("()=>{ window.__raf=window.requestAnimationFrame; window.requestAnimationFrame=function(){ return 0; }; }"); pg.wait_for_timeout(220)
    a = pg.screenshot(clip=clip)
    pg.evaluate("(c)=>{ const s=document.createElement('style'); s.id='__xEf'; s.textContent=c+'{visibility:hidden!important}'; document.head.appendChild(s); document.querySelectorAll(c).forEach(e=>{ e.style.setProperty('visibility','hidden','important'); e.__xEf=1; }); }", cache)
    pg.wait_for_timeout(250); b = pg.screenshot(clip=clip)
    if a == b: pg.wait_for_timeout(500); b = pg.screenshot(clip=clip)   # la peinture de l'effaçage peut tarder sous charge
    pg.evaluate("()=>{ const s=document.getElementById('__xEf'); if(s) s.remove(); document.querySelectorAll('*').forEach(e=>{ if(e.__xEf){ e.style.removeProperty('visibility'); e.__xEf=0; } }); window.requestAnimationFrame=window.__raf; }")
    A = Image.open(io.BytesIO(a)).convert('RGB'); B = Image.open(io.BytesIO(b)).convert('RGB'); d = ImageChops.difference(A, B).convert('L').point(lambda v: 255 if v > 40 else 0)
    bb = d.getbbox()
    if not bb: return None
    s = A.size[0] / clip['width'] * k   # pixels d'image par pt (v158 : × l'échelle — divisé, c'était faux dès que l'appareil est réduit)
    return {'h': (bb[3] - bb[1]) / s, 'w': (bb[2] - bb[0]) / s, 'cx': ((bb[0] + bb[2]) / 2) / s, 'cy': ((bb[1] + bb[3]) / 2) / s, 'W': clip['width'] / k, 'H': clip['height'] / k}
with sync_playwright() as p:
    b = p.webkit.launch(); erreurs = []
    for (vw, vh, th) in [(430, 932, 'light'), (430, 932, 'dark'), (330, 714, 'light'), (330, 714, 'dark')]:
        ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_guide','1')}catch(e){}")
        pg = ctx.new_page(); pg.on('pageerror', lambda e: erreurs.append(str(e)[:140])); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(500)
        # la référence : le X de « INDEX » (le « x » du titre de l'Index), son encre lue sur l'image
        pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(250)
        pg.evaluate(dict(ECRANS_TOUS)['Index 2']); pg.wait_for_timeout(3000)
        rc = pg.evaluate("()=>{ const t=document.querySelector('#indexSheet .scr-ti .ti-x'), r=t.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(); const x0=Math.floor(r.left-6), y0=Math.floor(r.top-6); return {clip:{x:x0, y:y0, width:Math.ceil(r.right+6)-x0, height:Math.ceil(r.bottom+6)-y0}, k:D.width/390}; }")
        ra = pg.screenshot(clip=rc['clip']); pg.evaluate("()=>document.querySelector('#indexSheet .scr-ti .ti-x').style.setProperty('visibility','hidden','important')"); pg.wait_for_timeout(300)
        rb = pg.screenshot(clip=rc['clip']); pg.evaluate("()=>document.querySelector('#indexSheet .scr-ti .ti-x').style.removeProperty('visibility')")
        _A = Image.open(io.BytesIO(ra)).convert('RGB'); _B = Image.open(io.BytesIO(rb)).convert('RGB'); _bb = ImageChops.difference(_A, _B).convert('L').point(lambda v: 255 if v > 40 else 0).getbbox()
        _s = _A.size[0] / rc['clip']['width'] * rc['k']; REF = {'w': (_bb[2] - _bb[0]) / _s, 'h': (_bb[3] - _bb[1]) / _s}   # le « x » du titre effacé sur l'élément, sans geler les images
        T = '%s %.2f' % (th[0], rc['k'])
        print('  référence [%s] : le X de « INDEX » — encre %.2f × %.2f pt' % (T, REF['w'], REF['h']), flush=True)
        for nom, js in ECRANS:
            pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(250)
            try: pg.evaluate(js)
            except Exception as ex: juge('[%s] %s · l\'écran s\'ouvre' % (T, nom), False, str(ex)[:80]); continue
            pg.wait_for_timeout(2600)   # les écrans de redteam_air ouvrent le Peaufiner 900 ms après la fiche
            # l'écran posé : la croix du dessus (élément, place, titre) identique sur deux relevés à 500 ms (8 s au plus) — sous charge un écran arrive lentement
            av = None
            for _ in range(16):
                L = pg.evaluate(LIT); cle = json.dumps([[c['sel'], round(c['clip']['x']), round(c['clip']['y']), c['T'] and c['T']['txt'], c['txt'], c['w']] for c in L['croix']])
                if L['croix'] and cle == av: break
                av = cle; pg.wait_for_timeout(500)
            juge('[%s] %-18s A · aucun « FERMER » à l\'écran' % (T, nom), not L['mots'], L['mots'][:3])
            if nom == 'accueil': juge('[%s] %-18s l\'accueil n\'a pas de fermeture' % (T, nom), not L['croix'], [c['sel'] for c in L['croix']]); continue
            if not L['croix']: juge('[%s] %-18s une fermeture que le doigt prend' % (T, nom), False, 'aucune'); continue
            for c in L['croix'][:2]:
                e = encre(pg, c['clip'], c['k'])
                Tt = c['T']
                okB = c['txt'] == 'X' and c['fam'] == 'PromiLate' and e and REF and abs(e['h'] - REF['h']) <= 0.5 and abs(e['w'] - REF['w']) <= 0.5
                juge('[%s] %-18s B · le X de « INDEX » : encre %s × %s pt pour %.2f × %.2f ± 0,5' % (T, nom, e and round(e['w'], 2), e and round(e['h'], 2), REF['w'], REF['h']), okB,
                     '%s · texte « %s » · police %s' % (c['sel'], c['txt'], c['fam']))
                juge('[%s] %-18s C · sa couleur = celle du titre, à pleine opacité' % (T, nom), bool(Tt) and c['col'] == Tt['col'] and c['op'] >= 0.999, '%s / titre %s · opacité %s' % (c['col'], Tt and Tt['col'], c['op']))
                okD = c['w'] >= 43.9 and c['h'] >= 43.9 and e and abs(e['cx'] - e['W'] / 2) <= 1.5 and abs(e['cy'] - e['H'] / 2) <= 1.5 and all(c['pts'])
                juge('[%s] %-18s D · zone tactile %s × %s pt, centrée sur l\'encre, prise à ses quatre coins' % (T, nom, round(c['w'], 1), round(c['h'], 1)), okD,
                     'écart du centre %s, %s pt · coins %s' % (e and round(e['cx'] - e['W'] / 2, 2), e and round(e['cy'] - e['H'] / 2, 2), c['pts']))
        ctx.close()
    b.close()
juge('aucune erreur de page', not [x for x in erreurs if 'version.json' not in x], erreurs[:2])
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
