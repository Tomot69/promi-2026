# -*- coding: utf-8 -*-
"""Batterie 6 — le geste du Noyau (chantiers 13 et 14)."""
from playwright.sync_api import sync_playwright
import os as _os, sys
_ICI=_os.path.dirname(_os.path.abspath(__file__))
def _url():
    import re as _re
    for p in [_os.path.join(_ICI,'app.html'),'/home/claude/app.html']:
        if _os.path.exists(p): return 'file://'+p
    for f in sorted(_os.listdir(_ICI),reverse=True):
        if _re.match(r'promi-v\d+\.html$',f): return 'file://'+_os.path.join(_ICI,f)
    return 'file:///home/claude/app.html'
R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))
PIEGE_TXT = """(()=>{ window.__txt=[]; const P=CanvasRenderingContext2D.prototype, f=P.fillText;
  P.fillText=function(t){ try{ if(this.canvas) window.__txt.push({t:String(t), s:String(this.fillStyle).toLowerCase()}); }catch(e){} return f.apply(this,arguments); }; })();"""

# ⚑ ASSAINISSEMENT (30 sept. 2026) — LE NOYAU SE LIT SUR L'IMAGE, JAMAIS DANS L'ÉTAT. On rend l'aperçu sans puis avec le Noyau,
#   l'horloge figée (la Toile ne respire pas entre les deux) : ce qui change EST l'anneau. On en tire son aire et son centre,
#   en fraction de l'aperçu — et on le compare à l'endroit où le DOIGT l'a posé (valeur écrite ici), jamais à `shNyX` que l'app
#   déclare. Les anciennes sondes cherchaient des couleurs d'état retirées (#FFD447, #8FE08F) et lisaient `shNyX`/`shNyY`.
#   Prouvé : aire ≈ 16 000 px, centre à 0,001 près de la pose, identique d'une passe à l'autre. Original : sauvegardes/redteam_geste-avant-assainissement.py
NOYAU = """async()=>{ const cv=document.getElementById('shCanvas'); const pn=performance.now; performance.now=()=>424242;
  const lire=()=>cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
  try{ document.getElementById('shNyOff').click(); shareRender(); await new Promise(r=>setTimeout(r,350)); const a=lire();
       document.getElementById('shNyOn').click(); shareRender(); await new Promise(r=>setTimeout(r,350)); const b=lire();
       let n=0,sx=0,sy=0; const W=cv.width;
       for(let i=0;i<a.length;i+=4){ if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>60){ const p=i/4; n++; sx+=p%W; sy+=(p/W)|0; } }
       return {n:n, cx: n? sx/n/W : null, cy: n? sy/n/cv.height : null}; }
  finally{ performance.now=pn; } }"""
def pres(n, x, y, tol=0.04): return bool(n and n['n'] > 400 and n['cx'] is not None and abs(n['cx'] - x) < tol and abs(n['cy'] - y) < tol)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.add_init_script(PIEGE_TXT)
    pg.goto(_url()); pg.wait_for_timeout(5200)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(2000)
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{document.getElementById('shNyOn').click();}"); pg.wait_for_timeout(1200)
    # LE TIROIR RECOUVRE L'APERCU : on le ferme avant tout geste
    pg.evaluate("()=>{const w=document.getElementById('shTrayWrap');if(w)w.classList.remove('open');document.body.click();}")
    pg.wait_for_timeout(900)
    box=pg.evaluate("()=>{const c=document.getElementById('shCanvas').getBoundingClientRect();return {x:c.x,y:c.y,w:c.width,h:c.height};}")
    def geste(fx0,fy0,fx1,fy1,att=1500):
        x0=box['x']+box['w']*fx0; y0=box['y']+box['h']*fy0
        x1=box['x']+box['w']*fx1; y1=box['y']+box['h']*fy1
        pg.mouse.move(x0,y0); pg.mouse.down(); pg.wait_for_timeout(420)
        for k in range(1,9):
            pg.mouse.move(x0+(x1-x0)*k/8, y0+(y1-y0)*k/8); pg.wait_for_timeout(35)
        pg.wait_for_timeout(400); pg.mouse.up(); pg.wait_for_timeout(att)
    n0=pg.evaluate(NOYAU)
    geste(0.5,0.5,0.30,0.32)
    n1=pg.evaluate(NOYAU)
    t("Ma Toile : le Noyau se deplace au doigt", bool(n0 and n1 and n0['cx'] is not None and n1['cx'] is not None and n1['cx'] < n0['cx']-0.05 and n1['cy'] < n0['cy']-0.05),
      'centre peint %s -> %s' % (n0 and (round(n0['cx'] or 0,3), round(n0['cy'] or 0,3)), n1 and (round(n1['cx'] or 0,3), round(n1['cy'] or 0,3))))
    t("l'anneau est peint a sa nouvelle place", pres(n1, 0.30, 0.32), 'aire %s · centre %s (le doigt : 0.30, 0.32)' % (n1 and n1['n'], n1 and (round(n1['cx'] or 0,3), round(n1['cy'] or 0,3))))
    pg.evaluate("()=>{window.shNyX=0.5;window.shNyY=0.55;shareRender();}"); pg.wait_for_timeout(900)
    geste(0.5,0.55,0.5,0.845)
    nq=pg.evaluate(NOYAU)
    t("l'aimant de la ligne du QR attire", bool(nq and nq['cy'] is not None and abs(nq['cy']-0.84) < 0.05), 'centre peint y=%s' % (nq and nq['cy']))
    pg.evaluate("()=>{document.querySelector('#shMode button[data-mode=mosaic]').click();}"); pg.wait_for_timeout(1600)
    pg.evaluate("()=>{window.shNyBR=1;window.shNyBC=0;shareRender();}"); pg.wait_for_timeout(1300)
    r0=pg.evaluate("()=>[window.shNyBR,window.shNyBC]")
    geste(0.74,0.70,0.74,0.70,1600)
    r1=pg.evaluate("()=>[window.shNyBR,window.shNyBC]")
    t("Mes Promi : le bloc change de case", r1 != r0, '%s -> %s' % (r0, r1))
    n=pg.evaluate("()=>promises.filter(p=>!p.draft&&!p.req).length")
    cols=2 if n<=6 else (3 if n<=12 else (4 if n<=24 else 5))
    t("le bloc reste dans la grille", r1[1] <= cols-2 and r1[0] >= 0, 'col %s / max %d' % (r1[1], cols-2))
    t("un tap simple ne deplace rien", (lambda: (
        pg.evaluate("()=>{window.shNyBR=1;window.shNyBC=0;shareRender();}"),
        pg.wait_for_timeout(1100),
        pg.mouse.click(box['x']+box['w']*0.5, box['y']+box['h']*0.5),
        pg.wait_for_timeout(900),
        pg.evaluate("()=>[window.shNyBR,window.shNyBC]"))[-1] == [1,0])())

    # ---------- Mes Promi : l'anneau et le % sont bien la ----------
    pg.evaluate("()=>{document.querySelector('#shMode button[data-mode=mosaic]').click();}"); pg.wait_for_timeout(1500)
    # ⚑ REPRIS AU NIVEAU DE LA DÉCISION, 18 septembre 2026 (§7). La règle — « l'anneau de
    #   Mes Promi est peint » — est INTACTE. Deux choses étaient fausses, et la seconde depuis
    #   le 29 août :
    #   1 · la sonde cherchait #D0B0FF (208,176,255), l'ancien lilas — périmé par la planche ;
    #   2 · ⚠ L'ANNEAU N'A JAMAIS PORTÉ DE TEINTE DE NATURE ICI. Depuis le lot du 29 août il
    #       porte LES COULEURS D'ÉTAT du §3 (comme sa légende `.klegend` et le cadre 48) — la
    #       première sonde de ce fichier l'avait noté, celle-ci ne l'avait jamais été.
    #       Mesuré par différence, en mosaïque : le Noyau AJOUTE du #8FDE8F, à ΔE 1,3 du menthe
    #       décidé, et rien de lilas.
    #   On mesure donc CE QUE LE NOYAU AJOUTE, pas une couleur absolue : un anneau absent donne
    #   zéro par construction, et le contrat se prouve tout seul.
    #   Version d'avant : sauvegardes/redteam_geste-avant-IDENTITE.py
    # (assainissement : l'ancienne sonde `_ETATS`, qui cherchait #8FE08F / #FFD447 et ne servait plus, est retirée)
    # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7). LA RÈGLE : « l'objet posé dans la planche y
    #   PEINT quelque chose ». L'objet n'est plus le Noyau (Q284) mais la Pelote (Q287) — et
    #   la Pelote n'a pas d'arcs d'état à compter : on mesure LES PIXELS PEINTS dans son bloc,
    #   avec et sans. Même intention, grandeur qui a la forme du nouvel objet.
    #   Original : sauvegardes/redteam_geste-avant-v14.py
    # ⚑ assainissement (30 sept.) — la Pelote se mesure DANS SON BLOC. L'ancienne sonde comptait les pixels « non fond » de TOUT
    #   l'aperçu, avec et sans : poser la Pelote déplace les cases, le compte BAISSAIT (−4 700) alors qu'elle est bien peinte — rouge
    #   à tort, antérieur à l'assainissement. On prend la place du bloc dans la composition publiée (un POINTEUR, pas un verdict) et on
    #   mesure LES PIXELS à cet endroit : au moins 25 % de l'aire du bloc portent de la matière (la Pelote y est un disque).
    _PELPIX = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');const C=window._plancheComp||{};
      const B=C.bloc, G=C.grille; if(!B||!G) return {err:'pas de bloc'};
      const sx=cv.width/G.W, sy=cv.height/G.H, x0=Math.round(B.x*sx), y0=Math.round(B.y*sy), w=Math.round(B.w*sx), h=Math.round(B.h*sy);
      const im=g.getImageData(0,0,cv.width,cv.height).data, f=[im[0],im[1],im[2]]; let n=0,t=0;
      for(let y=y0;y<y0+h;y+=2) for(let x=x0;x<x0+w;x+=2){ const i=(y*cv.width+x)*4; t++;
        if(Math.abs(im[i]-f[0])+Math.abs(im[i+1]-f[1])+Math.abs(im[i+2]-f[2])>40) n++; }
      return {part: t? n/t : 0, n:n, t:t};}"""
    _PEL_ON  = "()=>{const b=document.querySelector('#shNoyauParts [data-pel]'); if(b&&!window.shPelote)b.click();}"
    _PEL_OFF = "()=>{const b=document.querySelector('#shNoyauParts [data-pel]'); if(b&&window.shPelote)b.click();}"
    pg.evaluate(_PEL_ON); pg.wait_for_timeout(1700)
    _pl = pg.evaluate(_PELPIX)
    t("Mon Folio : la Pelote est peinte dans son bloc", (_pl.get('part') or 0) >= 0.25, str(_pl))
    # ⚑ assainissement (30 sept.) — « Mes Promi : le % est peint » est RETIRÉ : règle abandonnée. Depuis Q287 (v14), l'objet posé
    #   dans le Folio est la PELOTE, plus le Noyau — il n'y porte aucun chiffre (vérifié : aucun texte chiffré n'est écrit sur aucun
    #   canevas pendant ce rendu). L'ancien contrôle passait À VIDE : il comptait des pixels orangés, et les trouvait dans les DALLES
    #   de la palette. La Pelote de ce mode est jugée juste au-dessus (« peinte dans son bloc ») ; le % du Noyau, dans Ma Toile, par
    #   redteam_toile (« le % s'affiche », au tracé).
    # ---------- le cadrage ne suit pas le Noyau ----------
    pg.evaluate("()=>{document.querySelector('#shMode button[data-mode=toile]').click();}"); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const w=document.getElementById('shTrayWrap');if(w)w.classList.remove('open');}")
    pg.wait_for_timeout(700)
    pg.evaluate("()=>{window.shZoom=2.2;window.shPanX=0;window.shPanY=0;window.shNyX=0.5;window.shNyY=0.5;shareRender();}")
    pg.wait_for_timeout(700)
    _p0 = pg.evaluate("()=>[window.shPanX,window.shPanY]")
    _x = box['x']+box['w']*0.5; _y = box['y']+box['h']*0.5
    pg.mouse.move(_x,_y); pg.mouse.down(); pg.wait_for_timeout(420)
    for _k in range(1,9): pg.mouse.move(_x-40*_k/8, _y-60*_k/8); pg.wait_for_timeout(35)
    pg.mouse.up(); pg.wait_for_timeout(1300)
    t("le cadrage ne suit pas le Noyau", pg.evaluate("()=>[window.shPanX,window.shPanY]") == _p0, str(_p0))


    # ---------- le Noyau est centre dans son bloc (chantier : hauteur = 2 cases) ----------
    # ⚑ RÉÉCRIT (§7) : le bloc fait toujours DEUX CASES DE HAUT, mais les rangées n'ont plus
    #   la même hauteur (un titre à deux lignes espace la sienne) — la hauteur du bloc est
    #   désormais la SOMME des deux rangées qu'il couvre, et la Pelote y est centrée.
    _ok = pg.evaluate("""()=>{const src=sharePlanche.toString();
      return src.indexOf('hRow[nr]')>=0
          && src.indexOf('by+(bh-D)/2')>=0
          && src.indexOf('bx+(bw-D)/2')>=0;}""")
    t("Mon Folio : la Pelote centrée sur la hauteur de son bloc", _ok)
    _fluide = pg.evaluate("()=>typeof window._shAnim==='function'")
    t("Mes Promi : la reorganisation est animee", _fluide)


    # ---------- la reorganisation produit des images intermediaires ----------
    pg.evaluate("()=>{document.querySelector('#shMode button[data-mode=mosaic]').click();}"); pg.wait_for_timeout(1400)
    if not pg.evaluate("()=>window.shNoyau"):
        pg.evaluate("()=>{document.getElementById('shNyOn').click();}"); pg.wait_for_timeout(1300)
    _HH = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const im=g.getImageData(0,0,cv.width,cv.height).data;let s=0;
      for(let i=0;i+2<im.length;i+=97)s=(s+im[i]*31+im[i+1]*7+im[i+2])%1000000007;return s;}"""
    # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7). LA RÈGLE QUE CE CONTRÔLE ENCODAIT : le bloc
    #   GLISSE d'une case à l'autre, et la planche montre des images intermédiaires. Ce
    #   glissement servait à une chose : le Noyau se DÉPLAÇAIT (il avait ses commandes de
    #   position). LE NOYAU EST SORTI DU PARTAGE (Q284) et la Pelote a UNE place ; il n'y a
    #   plus de déplacement à animer. Ce que Tom demande à sa place (Q287) est vérifiable et
    #   plus fort : « elle prend la place de quatre cases, les autres se réorganisent autour —
    #   rien ne se superpose, rien ne disparaît ». On le mesure sur LA COMPOSITION PUBLIÉE :
    #   le compte de dalles ne bouge pas, aucune case n'est partagée, et la planche déclare
    #   son bloc.
    _CO = """()=>{const c=window._plancheComp; if(!c) return null;
      const vus={}; let doublon=0;
      c.cases.forEach(function(k){ const q=k.x+','+k.y; if(vus[q])doublon++; vus[q]=1; });
      return {n:c.n, pelote:!!c.pelote, doublon:doublon};}"""
    pg.evaluate(_PEL_OFF); pg.wait_for_timeout(1400); _cSans = pg.evaluate(_CO)
    pg.evaluate(_PEL_ON);  pg.wait_for_timeout(1500); _cAvec = pg.evaluate(_CO)
    t("Mon Folio : rien ne disparaît, rien ne se superpose",
      bool(_cSans) and bool(_cAvec) and _cSans['n'] == _cAvec['n']
      and _cAvec['pelote'] and _cSans['doublon'] == 0 and _cAvec['doublon'] == 0,
      'sans %s / avec %s' % (_cSans, _cAvec))
    pg.wait_for_timeout(900)

    t("aucune erreur JS", not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-44s %s  %s'%(n,s,d if s=='KO' else ''))
ok=sum(1 for _,s,_ in R if s=='OK')
print('\n%d/%d'%(ok,len(R)))
sys.exit(0 if ok==len(R) else 1)
