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
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
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
    geste(0.5,0.5,0.30,0.32)
    p1=pg.evaluate("()=>[window.shNyX,window.shNyY]")
    t("Ma Toile : le Noyau se deplace au doigt", p1[0] is not None and abs(p1[0]-0.5)>0.05, str(p1))
    SONDE = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      /* ⚑ REPRIS AU NIVEAU DE LA DÉCISION, 17 septembre 2026 (§7) — DEUX FOIS, et la seconde
         est la bonne. La règle encodée reste « l'anneau est peint à sa nouvelle place ».
         1 · SES COULEURS ont changé : menthe #2BE88C → #8FE08F, périwinkle #8FA0FF → #FFD447,
             orange #F07A2E → #DD4D23.
         2 · ⚠ ET LA SONDE MESURAIT LA TOILE, PAS L'ANNEAU. Elle comptait, dans une petite
             fenêtre centrée sur le Noyau, des pixels d'une couleur d'état — or l'ancienne
             palette du Studio (« Signal ») contenait EXACTEMENT le périwinkle #8FA0FF et le
             menthe #2BE88C : la sonde comptait des DALLES. Les vingt palettes du 17 septembre
             ne les portent plus, et le compte est tombé à zéro sur un anneau parfaitement
             peint (mesuré : le Noyau AJOUTE bien #8FDE8F, à ΔE 1,3 du menthe décidé).
             On mesure donc par DIFFÉRENCE, sur TOUT le canevas : ce que le Noyau ajoute.
         Original : sauvegardes/redteam_geste-avant-IDENTITE.py */
      const im=g.getImageData(0,0,cv.width,cv.height).data; let n=0;
      for(let i=0;i<im.length;i+=8){const r=im[i],v=im[i+1],b=im[i+2];
        if((Math.abs(r-143)<18&&Math.abs(v-224)<18&&Math.abs(b-143)<18)||   /* #8FE08F tenu     */
           (Math.abs(r-255)<18&&Math.abs(v-212)<18&&Math.abs(b-71)<18)||    /* #FFD447 en cours */
           (Math.abs(r-221)<18&&Math.abs(v-77)<18&&Math.abs(b-35)<18))n++;}
      return n;}"""
    _av = pg.evaluate(SONDE)
    pg.evaluate("()=>{document.getElementById('shNyOff').click();}"); pg.wait_for_timeout(1300)
    _sans = pg.evaluate(SONDE)
    pg.evaluate("()=>{document.getElementById('shNyOn').click();}"); pg.wait_for_timeout(1300)
    _avec = pg.evaluate(SONDE)
    t("l'anneau est peint a sa nouvelle place", _avec - _sans > 400,
      'sans %d · avec %d' % (_sans, _avec))
    pg.evaluate("()=>{window.shNyX=0.5;window.shNyY=0.55;shareRender();}"); pg.wait_for_timeout(900)
    geste(0.5,0.55,0.5,0.845)
    y=pg.evaluate("()=>window.shNyY")
    t("l'aimant de la ligne du QR attire", abs(y-0.84) < 0.05, 'y=%.3f' % y)
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
    _ETATS = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const im=g.getImageData(0,0,cv.width,cv.height).data;let n=0;
      for(let i=0;i<im.length;i+=8){const r=im[i],v=im[i+1],b=im[i+2];
        if((Math.abs(r-143)<18&&Math.abs(v-224)<18&&Math.abs(b-143)<18)||   /* #8FE08F tenu     */
           (Math.abs(r-255)<18&&Math.abs(v-212)<18&&Math.abs(b-71)<18)||    /* #FFD447 en cours */
           (Math.abs(r-221)<18&&Math.abs(v-77)<18&&Math.abs(b-35)<18))n++;}return n;}"""
    pg.evaluate("()=>{const b=document.getElementById('shNyOff');if(b)b.click();}"); pg.wait_for_timeout(1400)
    _sans2 = pg.evaluate(_ETATS)
    pg.evaluate("()=>{const b=document.getElementById('shNyOn');if(b)b.click();}"); pg.wait_for_timeout(1500)
    _avec2 = pg.evaluate(_ETATS)
    _an = _avec2 - _sans2
    t("Mes Promi : l'anneau est peint", _an > 300, 'avec %d - sans %d = %d' % (_avec2, _sans2, _an))
    if not pg.evaluate("()=>window.shChiffre"):
        pg.evaluate("()=>{const b=document.getElementById('shNyPct');if(b)b.click();}"); pg.wait_for_timeout(1400)
    t("Mes Promi : le % est peint", pg.evaluate("""()=>{const cv=document.getElementById('shCanvas');
      const g=cv.getContext('2d');const im=g.getImageData(0,0,cv.width,cv.height).data;let n=0;
      for(let i=0;i<im.length;i+=24){if(Math.abs(im[i]-219)<40&&Math.abs(im[i+1]-107)<40)n++;}
      return n>60;}"""))
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
    _ok = pg.evaluate("""()=>{const src=sharePlanche.toString();
      return src.indexOf('var bh=chh*2+gap')>=0
          && src.indexOf('by+(bh-D)/2')>=0
          && src.indexOf('by+bh/2')>=0;}""")
    t("Mes Promi : le Noyau centre sur la hauteur du bloc", _ok)
    _fluide = pg.evaluate("()=>typeof window._shAnim==='function'")
    t("Mes Promi : la reorganisation est animee", _fluide)


    # ---------- la reorganisation produit des images intermediaires ----------
    pg.evaluate("()=>{document.querySelector('#shMode button[data-mode=mosaic]').click();}"); pg.wait_for_timeout(1400)
    if not pg.evaluate("()=>window.shNoyau"):
        pg.evaluate("()=>{document.getElementById('shNyOn').click();}"); pg.wait_for_timeout(1300)
    _HH = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const im=g.getImageData(0,0,cv.width,cv.height).data;let s=0;
      for(let i=0;i+2<im.length;i+=97)s=(s+im[i]*31+im[i+1]*7+im[i+2])%1000000007;return s;}"""
    pg.evaluate("""()=>{window.shNyBR0=1;window.shNyBC0=0;window.shNyBR=3;window.shNyBC=1;
      window.shNyT0=performance.now();if(window._shAnim)_shAnim();}""")
    _hs=[]
    for _k in range(7):
        pg.wait_for_timeout(55); _hs.append(pg.evaluate(_HH))
    # 2 images distinctes suffisent a prouver une transition : le nombre exact
    # depend de la charge de la machine, pas du code.
    t("la reorganisation est progressive", len(set(_hs)) >= 2, '%d images distinctes' % len(set(_hs)))
    pg.wait_for_timeout(900)

    t("aucune erreur JS", not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-44s %s  %s'%(n,s,d if s=='KO' else ''))
ok=sum(1 for _,s,_ in R if s=='OK')
print('\n%d/%d'%(ok,len(R)))
sys.exit(0 if ok==len(R) else 1)
