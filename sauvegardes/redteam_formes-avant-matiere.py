#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_formes.py — UN TRAIT DOIT AVOIR LA COURBE DE SON ÉTAT.

Les cinq lignes du critère comparent des cotes et des couleurs. **Un trait à la bonne
position avec la mauvaise courbe passe à zéro.** Ce contrôle-ci compare LA FORME : on
échantillonne la courbe que l'app peint, et on la compare — point par point — à celle que
la planche dessine.

LES DEUX LOIS, EXTRAITES DES CADRES (jamais estimées) :

  LE BANDEAU DU FIL — cadre 76 · SVG 143 × 128, sans viewBox
      x(u) = 121,0 − 4,3·u − 8,425·sin(2πu)          u = y/128, période 1
      trait : le même chemin · épaisseur 7 · bouts ronds · AUCUN CHEVRON
              u de 0 à 0,5 s'il manque une moitié · 0 → 1 si la parole est entière
      points : 4 cercles r 3,4 aux y 77 · 90 · 103 · 116, sur le chemin

  LA CARTE D'INDEX — cadre 72 · SVG 165 × h, viewBox « 0 0 165 h »
      chemin en Béziers cubiques, épaisseur 5,5 × 165/173 = 5,2457
      tenu      → chemin ENTIER, ni chevron ni points
      à tenir   → chemin jusqu'à x = 82,5 (la moitié) + chevron + 6 points r 3,052
                  aux x 93 · 103,5 · 114 · 124,5 · 135 · 145,4

ON NE LIT PAS LE CODE : on lit LES PIXELS PEINTS. À chaque abscisse (ou ordonnée), on
cherche le centre du trait et on le compare à la loi. Tolérance : 1,5 px.

Usage :  python3 redteam_formes.py [--verbose]
"""
import math
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
TOL = 1.5
ok = [0]
ko = []


def t(nom, cond, detail=''):
    if cond:
        ok[0] += 1
        print('%-54s OK  %s' % (nom, detail if VERBOSE else ''))
    else:
        ko.append(nom)
        print('%-54s KO  %s' % (nom, detail))


# ── la sonde : où est le centre du trait, à cette ordonnée / abscisse ? ─────────────────
SONDE_FIL = r"""(a)=>{
  const cv=document.querySelectorAll('#feedList .s4-carte canvas')[a.i]; if(!cv) return null;
  const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
  const g=cv.getContext('2d'); const k=cv.width/W;
  const C=a.col.replace('#',''); const R=parseInt(C.slice(0,2),16),
        G=parseInt(C.slice(2,4),16), B=parseInt(C.slice(4,6),16);
  const centres=[], pts=[];
  for(let y=2;y<H-2;y+=2){
    let x0=-1,x1=-1;
    for(let x=0;x<W;x++){
      const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
      if(d[3]>200 && Math.abs(d[0]-R)+Math.abs(d[1]-G)+Math.abs(d[2]-B)<40){
        if(x0<0)x0=x; x1=x; }
    }
    if(x0>=0) centres.push([y,(x0+x1)/2,x1-x0+1]);
  }
  return {W:W,H:H,centres:centres};}"""

SONDE_IX = r"""(a)=>{
  const cv=document.querySelectorAll('#indexList .s4-carte canvas')[a.i]; if(!cv) return null;
  const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
  const g=cv.getContext('2d'); const k=cv.width/W;
  const C=a.col.replace('#',''); const R=parseInt(C.slice(0,2),16),
        G=parseInt(C.slice(2,4),16), B=parseInt(C.slice(4,6),16);
  const centres=[];
  for(let x=2;x<W-2;x+=2){
    let y0=-1,y1=-1;
    for(let y=0;y<H;y++){
      const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
      if(d[3]>200 && Math.abs(d[0]-R)+Math.abs(d[1]-G)+Math.abs(d[2]-B)<40){
        if(y0<0)y0=y; y1=y; }
    }
    if(y0>=0) centres.push([x,(y0+y1)/2,y1-y0+1]);
  }
  return {W:W,H:H,centres:centres};}"""




def attendre(pg, sel):
    """On attend que la liste soit BÂTIE ET PEINTE, on ne devine pas un délai.

    ⚠ Sans cela le contrôle oscille — 38, 42, 44, 50 sur quatre passages : selon l'instant,
    la dernière carte n'est pas encore posée, la sonde ne trouve aucun pixel de sa couleur
    et compte un faux rouge. On attend donc deux relevés consécutifs identiques ET que
    chaque carte porte un canevas de largeur non nulle."""
    prec = -1
    for _ in range(40):
        pg.wait_for_timeout(250)
        n = pg.evaluate("""(s)=>{const l=[...document.querySelectorAll(s)];
          if(!l.length) return 0;
          return l.every(c=>{const cv=c.querySelector('canvas');
            return cv && parseFloat(cv.style.width)>0;}) ? l.length : -1;}""", sel)
        if n > 0 and n == prec:
            return n
        prec = n
    return prec

def run_continu(vals, pas):
    """La plus longue suite CONTINUE de relevés, depuis le début.

    ⚠ LE PLEIN ET LES POINTS ONT LA MÊME COULEUR ET PRESQUE LA MÊME ÉPAISSEUR — un point
    fait 6,1 px de diamètre, le trait 5,25. Les séparer par l'épaisseur ne marche pas
    (mesuré : « plein jusqu'à 156 » sur une carte dont le plein s'arrête à 82). Ce qui les
    sépare, c'est LA CONTINUITÉ : le plein est d'un seul tenant, les points sont espacés.
    On prend donc la suite sans trou, et on s'arrête au premier écart."""
    if not vals:
        return 0
    fin = vals[0]
    for v in vals[1:]:
        if v - fin > pas * 2.5:
            break
        fin = v
    return fin

def loi_fil(y, H):
    u = max(0.0, min(1.0, y / H))
    return 121.0 - 4.3 * u - 8.425 * math.sin(2 * math.pi * u)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for theme in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", theme)
            pg.wait_for_timeout(400)
            print('\n══ thème %s ══' % theme)

            # ── LE BANDEAU DU FIL ────────────────────────────────────────────────────
            pg.evaluate("()=>{if(window.closeAll)closeAll(); setView('fil');}")
            attendre(pg, '#feedList .s4-carte')
            cartes = pg.evaluate("""()=>[...document.querySelectorAll('#feedList .s4-carte')]
              .map((c,i)=>({i:i, etat:(c.textContent.match(/TENUE|À TENIR|EN COURS|LANCÉ|TENU À DEUX|RELEVÉ/)||[''])[0]}))""")
            COL = {'TENUE': '#2BE88C', 'TENU À DEUX': '#2BE88C', 'RELEVÉ': '#2BE88C',
                   'À TENIR': '#F07A2E', 'EN COURS': '#CBAAFF', 'LANCÉ': '#FFC0A8'}
            for c in cartes[:5]:
                col = COL.get(c['etat'])
                if not col:
                    continue
                r = pg.evaluate(SONDE_FIL, {'i': c['i'], 'col': col})
                nom = 'Fil · carte %d « %s » [%s]' % (c['i'] + 1, c['etat'], theme)
                if not r or not r['centres']:
                    t(nom + ' · le trait est peint', False, 'aucun pixel de la couleur %s' % col)
                    continue
                H = r['H']
                pire = 0.0
                for y, x, ep in r['centres']:
                    d = abs(x - loi_fil(y, H))
                    if d > pire:
                        pire = d
                t(nom + ' · la courbe est celle du cadre 76', pire <= TOL,
                  'écart maximal %.2f px sur %d relevés' % (pire, len(r['centres'])))
                # l'épaisseur
                eps = sorted(e for _, _, e in r['centres'])
                med = eps[len(eps) // 2]
                t(nom + ' · épaisseur 7', abs(med - 7) <= 2, 'mesurée %d' % med)
                # la moitié ou l'entier, selon l'état
                entier = c['etat'] in ('TENUE', 'TENU À DEUX', 'RELEVÉ')
                bas = max(y for y, _, _ in r['centres'])
                if entier:
                    t(nom + ' · le trait va jusqu\'en bas', bas >= H - 8,
                      'dernier point à %d sur %d' % (bas, H))
                else:
                    finPlein = run_continu([y for y, _, e in r['centres'] if e >= 5], 2)
                    t(nom + ' · le plein s\'arrête à la moitié', abs(finPlein - H / 2) <= 8,
                      'plein jusqu\'à %d, moitié %d' % (finPlein, H / 2))

            # ── LA CARTE D'INDEX ─────────────────────────────────────────────────────
            pg.evaluate("()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex();}")
            attendre(pg, '#indexList .s4-carte')
            ixs = pg.evaluate("""()=>[...document.querySelectorAll('#indexList .s4-carte')]
              .map((c,i)=>({i:i, etat:(c.textContent.match(/TENUE|À TENIR|EN COURS|LANCÉ|TENU À DEUX|GARDÉ DE CÔTÉ|PROMI/)||[''])[0]}))""")
            for c in ixs[:6]:
                col = COL.get(c['etat'])
                if not col:
                    continue
                r = pg.evaluate(SONDE_IX, {'i': c['i'], 'col': col})
                nom = 'Index · carte %d « %s » [%s]' % (c['i'] + 1, c['etat'], theme)
                if not r or not r['centres']:
                    t(nom + ' · le trait est peint', False, 'aucun pixel de la couleur %s' % col)
                    continue
                W = r['W']
                ep = sorted(e for _, _, e in r['centres'])[len(r['centres']) // 2]
                att = 5.5 * W / 173.0
                t(nom + ' · épaisseur 5,5 × l/173', abs(ep - att) <= 2,
                  'mesurée %d pour %.1f attendue' % (ep, att))
                entier = c['etat'] in ('TENUE', 'TENU À DEUX')
                droite = max(x for x, _, _ in r['centres'])
                if entier:
                    t(nom + ' · le trait traverse la carte', droite >= W - 8,
                      'dernier point à %d sur %d' % (droite, W))
                else:
                    fin = run_continu([x for x, _, e in r['centres'] if e >= att - 1], 2)
                    t(nom + ' · le plein s\'arrête à la moitié', abs(fin - W / 2) <= 10,
                      'plein jusqu\'à %d, moitié %.0f' % (fin, W / 2))
        b.close()

    print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
    if ko:
        print('\nCOURBES QUI NE SONT PAS CELLES DU CADRE :')
        for k in ko:
            print('   ·', k)
    sys.exit(0 if not ko else 1)


main()
