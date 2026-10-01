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
# ── la sonde : où est le centre du trait, à cette ordonnée / abscisse ? ─────────────────
#
# ⚑ Q74 · ELLE EXCLUT LA ZONE DE MATIÈRE, ET ELLE LE DIT.
#   C'était la cause de l'oscillation 46↔50, et ce n'était PAS « la dernière carte pas
#   encore peinte » : les deux passes de peinture sont synchrones, une carte posée est une
#   carte peinte. La sonde cherchait la couleur d'état à ±40 sur TOUTE la ligne, prenait le
#   PREMIER et le DERNIER pixel trouvés, et en tirait un centre et une épaisseur. Sur une
#   carte « À TENIR » (#F07A2E), la dalle contient des tons chauds qui tombent dans cette
#   fenêtre — et la dalle RESPIRE avec `performance.now()` : d'un rendu à l'autre, ce ne
#   sont pas les mêmes pixels. Le centre sautait, l'épaisseur explosait, la continuité se
#   brisait. Mesuré : les rouges changeaient de carte à chaque passage (carte 2, puis 3 et
#   4, puis 5), toujours « À TENIR », jamais un état à trait vert.
#
#   Deux corrections, aucune n'est un desserrage :
#   1 · **on saute la boîte de matière**, que l'app publie sur le canevas
#       (`data-matiere="x,y,w,h"`, posée par `peintBandeau` et `peintCarte`) ;
#   2 · on prend **la plus longue suite CONTINUE** de la couleur, pas du premier au dernier
#       pixel — un trait est d'un seul tenant, un reste de matière est épars.
#   La tolérance de couleur passe de 40 à 24 : le trait est peint PAR-DESSUS la matière,
#   en aplat, il n'a pas besoin de large.
#
#   Ce que le masque coûte, et il est mesuré : le trait ne rentre dans la boîte de matière
#   qu'à son minimum (x = 111,5 à u = 0,25, boîte jusqu'à x = 115) — **une ordonnée sur 63**.
#   Chaque sonde rend `saute`, le nombre de relevés perdus, et le contrôle l'affiche.

_AIDE = r"""
  /* ⚑ ON SUIT LE TRAIT DE PROCHE EN PROCHE — c'est ce qui le sépare de la matière.
     Ni le masque géométrique ni « la plus longue suite d'une ligne » ne suffisent :
       · la boîte de matière publiée par l'app CHEVAUCHE le trait (le bandeau descend à
         x = 111,5 à u = 0,25, la boîte va jusqu'à 115) — masquer rognait le trait par la
         gauche et poussait l'écart maximal à 3,06 px ;
       · « la plus longue suite de la ligne » retombe sur une tache de dalle dès que le
         MONDE tiré au Studio est chaud — et le monde change d'un chargement à l'autre :
         mesuré, le rouge sautait de la carte 4 à la carte 5 entre deux passages, avec un
         écart de 86 px et 47 ordonnées sans trait. Ce n'était donc ni le rendu inachevé
         ni le hasard : c'était la matière, et la sonde qui la prenait pour le trait.
     Un trait est CONTINU : son centre bouge de moins de 6 px d'une ordonnée à la suivante.
     Une tache ne l'est pas. On relève donc TOUTES les suites de chaque ligne, on les
     enchaîne, et on garde la plus longue chaîne. Aucun seuil n'est desserré. */
  const suites=(hits,epMax)=>{ const out=[]; let cur=null;
    for(const v of hits){ if(cur && v===cur.b+1){ cur.b=v; }
      else { if(cur) out.push(cur); cur={a:v,b:v}; } }
    if(cur) out.push(cur);
    return out.filter(s=>{const e=s.b-s.a+1; return e>=3 && e<=epMax;})
              .map(s=>({c:(s.a+s.b)/2, ep:s.b-s.a+1}));
  };
  const chaine=(lignes)=>{                    /* lignes = [{t, runs:[{c,ep}]}, …] */
    let best=[];
    for(let i=0;i<lignes.length;i++){
      for(const r0 of lignes[i].runs){
        const ch=[[lignes[i].t, r0.c, r0.ep]]; let last=r0.c, prev=i;
        for(let j=i+1;j<lignes.length;j++){
          if(lignes[j].t - lignes[prev].t > 3) break;      /* un trou coupe la chaîne */
          let pick=null;
          for(const r of lignes[j].runs)
            if(Math.abs(r.c-last)<=6 && (!pick || Math.abs(r.c-last)<Math.abs(pick.c-last))) pick=r;
          if(!pick) break;
          ch.push([lignes[j].t, pick.c, pick.ep]); last=pick.c; prev=j;
        }
        if(ch.length>best.length) best=ch;
      }
    }
    return best;
  };
  const proche=(d)=> d[3]>200 && Math.abs(d[0]-R)+Math.abs(d[1]-G)+Math.abs(d[2]-B)<24;
"""

SONDE_FIL = r"""(a)=>{
  const cv=document.querySelectorAll('#feedList .s4-carte canvas')[a.i]; if(!cv) return null;
  if(!cv.getAttribute('data-peint')) return null;
  const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
  const g=cv.getContext('2d'); const k=cv.width/W;
  const im=g.getImageData(0,0,cv.width,cv.height).data;
  const px=(x,y)=>{const i=((Math.round(y*k)*cv.width)+Math.round(x*k))*4;
    return [im[i],im[i+1],im[i+2],im[i+3]];};
  const C=a.col.replace('#',''); const R=parseInt(C.slice(0,2),16),
        G=parseInt(C.slice(2,4),16), B=parseInt(C.slice(4,6),16);
""" + _AIDE + r"""
  const lignes=[]; let saute=0;
  for(let y=2;y<H-2;y+=2){
    const hits=[];
    for(let x=0;x<W;x++){ if(proche(px(x,y))) hits.push(x); }
    const rs=suites(hits,a.epMax);
    if(!rs.length){ saute++; continue; }
    lignes.push({t:y, runs:rs});
  }
  const centres=chaine(lignes);
  /* ⚠ `centres` EST LA CHAÎNE — elle s'arrête au premier trou, c'est ce qui la rend
     insensible à la matière. Mais un trait « tenu à deux » est un DUO : deux moitiés
     séparées de 8 px (§2.6). La chaîne s'arrête donc au milieu, et « le trait traverse
     la carte » criait au rouge sur une carte parfaitement dessinée.
     On rend donc AUSSI `dernier` : la dernière ordonnée (ou abscisse) où une suite
     plausible existe. Le « plein s'arrête à la moitié » lit la chaîne ; « traverse la
     carte » lit `dernier`. Deux questions, deux mesures. */
  const dernier = lignes.length ? lignes[lignes.length-1].t : -1;
  return {W:W,H:H,centres:centres,saute:saute,lignes:lignes.length,dernier:dernier};}"""

SONDE_IX = r"""(a)=>{
  const cv=document.querySelectorAll('#indexList .s4-carte canvas')[a.i]; if(!cv) return null;
  if(!cv.getAttribute('data-peint')) return null;
  const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
  const g=cv.getContext('2d'); const k=cv.width/W;
  const im=g.getImageData(0,0,cv.width,cv.height).data;
  const px=(x,y)=>{const i=((Math.round(y*k)*cv.width)+Math.round(x*k))*4;
    return [im[i],im[i+1],im[i+2],im[i+3]];};
  const C=a.col.replace('#',''); const R=parseInt(C.slice(0,2),16),
        G=parseInt(C.slice(2,4),16), B=parseInt(C.slice(4,6),16);
""" + _AIDE + r"""
  const lignes=[]; let saute=0;
  for(let x=2;x<W-2;x+=2){
    const hits=[];
    for(let y=0;y<H;y++){ if(proche(px(x,y))) hits.push(y); }
    const rs=suites(hits,a.epMax);
    if(!rs.length){ saute++; continue; }
    lignes.push({t:x, runs:rs});
  }
  const centres=chaine(lignes);
  /* ⚠ `centres` EST LA CHAÎNE — elle s'arrête au premier trou, c'est ce qui la rend
     insensible à la matière. Mais un trait « tenu à deux » est un DUO : deux moitiés
     séparées de 8 px (§2.6). La chaîne s'arrête donc au milieu, et « le trait traverse
     la carte » criait au rouge sur une carte parfaitement dessinée.
     On rend donc AUSSI `dernier` : la dernière ordonnée (ou abscisse) où une suite
     plausible existe. Le « plein s'arrête à la moitié » lit la chaîne ; « traverse la
     carte » lit `dernier`. Deux questions, deux mesures. */
  const dernier = lignes.length ? lignes[lignes.length-1].t : -1;
  return {W:W,H:H,centres:centres,saute:saute,lignes:lignes.length,dernier:dernier};}"""


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
            return cv && parseFloat(cv.style.width)>0
                   && cv.getAttribute('data-peint');}) ? l.length : -1;}""", sel)
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
            # ⚑ REPRIS LE 18 SEPTEMBRE 2026 (§7). La règle — « le trait est peint » — est
            #   INTACTE ; ce sont les COULEURS que le juge reconnaît. Le menthe #2BE88C passe à
            #   #8FE08F et l'orange #F07A2E à #DD4D23 (planche des correspondances) ; « EN COURS »
            #   et « LANCÉ » portaient les teintes CLAIRES du §2.1 bis, mortes sur un champ pastel
            #   (Δlum 1,6 et 5,0) : elles deviennent les compagnons SOMBRES.
            #   Version d'avant : sauvegardes/redteam_formes-avant-IDENTITE.py
            COL = {'TENUE': '#8FE08F', 'TENU À DEUX': '#8FE08F', 'RELEVÉ': '#8FE08F',
                   'À TENIR': '#DD4D23', 'EN COURS': '#022140', 'LANCÉ': '#3D0F23'}
            for c in cartes[:5]:
                col = COL.get(c['etat'])
                if not col:
                    continue
                r = pg.evaluate(SONDE_FIL, {'i': c['i'], 'col': col, 'epMax': 14})
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
                  'écart maximal %.2f px sur %d relevés · %d ordonnée(s) sans trait'
                  % (pire, len(r['centres']), r.get('saute', 0)))
                # l'épaisseur
                eps = sorted(e for _, _, e in r['centres'])
                med = eps[len(eps) // 2]
                t(nom + ' · épaisseur 7', abs(med - 7) <= 2, 'mesurée %d' % med)
                # la moitié ou l'entier, selon l'état
                entier = c['etat'] in ('TENUE', 'TENU À DEUX', 'RELEVÉ')
                bas = r.get('dernier', max(y for y, _, _ in r['centres']))
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
                r = pg.evaluate(SONDE_IX, {'i': c['i'], 'col': col, 'epMax': 12})
                nom = 'Index · carte %d « %s » [%s]' % (c['i'] + 1, c['etat'], theme)
                if not r or not r['centres']:
                    t(nom + ' · le trait est peint', False, 'aucun pixel de la couleur %s' % col)
                    continue
                W = r['W']
                ep = sorted(e for _, _, e in r['centres'])[len(r['centres']) // 2]
                att = 5.5 * W / 173.0
                t(nom + ' · épaisseur 5,5 × l/173', abs(ep - att) <= 2,
                  'mesurée %d pour %.1f attendue · %d abscisse(s) sans trait'
                  % (ep, att, r.get('saute', 0)))
                entier = c['etat'] in ('TENUE', 'TENU À DEUX')
                droite = r.get('dernier', max(x for x, _, _ in r['centres']))
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
