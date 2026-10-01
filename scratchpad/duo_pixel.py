#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""duo_pixel.py — SUPERPOSER LE CADRE DU MOODBOARD ET LA CAPTURE DE L'APP, ET MESURER.

Les juges comparent des cotes et des couleurs. **Un trait à la bonne position avec la
mauvaise courbe passe à zéro.** Cet outil-ci ne compare rien d'autre que les pixels : il
capture le cadre de la planche et l'écran de l'app, les met l'un sur l'autre, et rend
la part de pixels qui diffèrent — plus une image de différence, à regarder.

Il ne dit pas ce qui ne va pas. Il dit OÙ, et combien. On regarde ensuite.

⚑ Q74 · IL EXCLUT LA ZONE DE MATIÈRE, ET IL LA DÉCLARE.
« Zéro écart » veut dire zéro sur la géométrie, les mots, les couleurs et les formes ;
la matière est exceptée (CLAUDE.md § 8 bis). Une Toile est ENGENDRÉE par le moteur et
respire avec `performance.now()` ; la planche l'a tracée à la main. Elles ne peuvent pas
coïncider, et on n'abandonne pas le moteur.
Le masque n'est pas dessiné ici : c'est **l'app qui déclare où est sa matière**
(`window._zonesMatiere()`, posé par les passes de peinture elles-mêmes). L'outil imprime
sa part de l'écran à chaque ligne — **un masque qui grandit se voit**. Hors de lui, la
cible est zéro, pas « peu ».

Usage :  python3 scratchpad/duo_pixel.py <sortie> [nom ...]
"""
import base64
import json
import os
import sys

from playwright.sync_api import sync_playwright

RACINE = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
APP = "http://127.0.0.1:8752/app.html"
MBH = "http://127.0.0.1:8752/promi-moodboard-H.html"
NUT = "http://127.0.0.1:8752/promi-nuee-toile.html"

MARQUE = """()=>{const isF=e=>{const s=e.getAttribute('style')||'';
  return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  [...document.querySelectorAll('div')].filter(isF).forEach((f,i)=>f.setAttribute('data-cadre',i));}"""

# ── LES ÉCRANS : nom, planche, n° de cadre (sombre, clair), mise en scène dans l'app ──
ECRANS = [
    ('index-2',   MBH, (72, 73), "()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
    ('fil',       MBH, (76, 77), "()=>{if(window.closeAll)closeAll(); setView('fil');}"),
    ('fiche-encours', MBH, (46, 47), "()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&!q.req&&!q.chiche&&q.status==='encours'&&(!q.who||q.who==='moi'))[0]; if(p)openDetail(p.id);}"),
    ('fiche-tenue',   MBH, (48, 49), "()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&q.status==='tenu')[0]; if(p)openDetail(p.id);}"),
    ('page-plus',     MBH, (2, 3),   "()=>{if(window.closeAll)closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
    # ⚠ LA NUÉE SE COMPARE AU CADRE 58, PAS À `promi-nuee-toile`.
    #   LES DEUX PLANCHES NE MONTRENT PAS LE MÊME POTAGER, et c'est mesuré :
    #     moodboard-H cadre 58   « le potager · 6 PROMI · 1 TENU »
    #                            arroser tous les soirs (TENU) · semer les radis (À TENIR)
    #     promi-nuee-toile c. 6  « le potager · 3 PROMI · 2 TENUS »
    #                            monter la serre avant les gelées · reprendre l'arrosage
    #                            automatique · récupérer les plants de tomates
    #   `promi-nuee-toile.html` est l'étude de LA TOILE d'une Nuée à 1, 3, 4 et 7 éléments
    #   (§9 à §13) — une planche de géométrie, pas un jeu de données. Le jeu de démonstration
    #   suit le moodboard : on compare donc au cadre qui montre CE potager-là.
    #   ⚠ ET LA GÉOMÉTRIE SE COMPARE À `promi-nuee-toile`, PAS AU CADRE 58.
    #     Les deux planches ne s'accordent pas sur la LOI DU CHAMP :
    #       promi-nuee-toile  n = 0·1·2·3·4·7  →  base 460·374·288·202·176·176
    #                         six points sur six pour `base = max(176, 460 − 86 n)` — la loi
    #                         du §9, celle que l'app porte et que `redteam_nuee` vérifie.
    #       moodboard-H c. 58  « 6 PROMI »     →  base 232, qu'aucun n ne produit.
    #     Le cadre 58 est donc ANTÉRIEUR à la loi. Notre potager a 6 Promi → base 176,
    #     exactement celle des cadres 8 et 10 de `promi-nuee-toile` (n = 4 et 7). On compare
    #     donc là : même loi, même champ. Les titres diffèrent (ce sont les données de
    #     l'autre planche) — ils sont dans des boîtes de texte, donc hors du « hors glyphe ».
    ('nuee',          NUT, (10, 11), "()=>{if(window.closeAll)closeAll(); openEssaim('potager');}"),
    #   ⚠ ET LA NUÉE VIDE AUSSI. Le cadre 60 du moodboard H donne **base 282** pour zéro
    #     Promi ; `promi-nuee-toile`, cadre 0, donne **460** — la valeur de la loi à n = 0.
    #     Même famille d'erreur que le cadre 58 (voir ECARTS-MOODBOARD § 0 bis).
    ('nuee-vide',     NUT, (0, 1),   "()=>{if(window.closeAll)closeAll(); openEssaim('atelier');}"),
    #   ⚠ L'INDEX 3 PAR LIGNE SE MESURE SUR SES DEUX PREMIÈRES RANGÉES.
    #     Le cadre 74 porte DOUZE cartes dont les quatre dernières RÉPÈTENT les quatre
    #     premières — planter, crêpes, potager, courir une seconde fois. C'est un artifice
    #     de planche pour remplir la grille ; l'Index réel en a huit, et son entête écrit
    #     « 12 », le nombre de Promi. On mesure donc jusqu'au bas de la rangée 2 (y = 474,
    #     soit 341 + 133), et la fenêtre est IMPRIMÉE à chaque ligne : elle se voit.
    ('index-3',       MBH, (74, 75), "()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}", (0, 474)),
]

# les écrans qui se mesurent sur une FENÊTRE d'ordonnées, et pourquoi : voir ECRANS.
FEN = {e[0]: e[4] for e in ECRANS if len(e) > 4}

DIFF = """(a)=>new Promise(res=>{
  const A=new Image(), B=new Image(); let n=0;
  function pret(){ if(++n<2) return;
    const W=390, H=844;
    const c1=document.createElement('canvas'); c1.width=W; c1.height=H;
    const c2=document.createElement('canvas'); c2.width=W; c2.height=H;
    c1.getContext('2d').drawImage(A,0,0,W,H);
    c2.getContext('2d').drawImage(B,0,0,W,H);
    const d1=c1.getContext('2d').getImageData(0,0,W,H).data;
    const d2=c2.getContext('2d').getImageData(0,0,W,H).data;
    const out=document.createElement('canvas'); out.width=W; out.height=H;
    const go=out.getContext('2d'); const im=go.createImageData(W,H); const dd=im.data;
    let diff=0, tot=0, masque=0, diffHG=0, totHG=0;
    const Z=a.zones||[], T=a.textes||[];
    const dedans=(L,x,y)=>{ for(const q of L)
      if(x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]) return true; return false; };
    const dansMatiere=(x,y)=>dedans(Z,x,y);
    const dansTexte=(x,y)=>dedans(T,x,y);
    /* par bandes de 20 px : où ça diffère, pas seulement combien */
    const bandes=new Array(Math.ceil(H/20)).fill(0);
    const parBande=new Array(Math.ceil(H/20)).fill(0);
    for(let i=0;i<d1.length;i+=4){
      const p=i/4, y=Math.floor(p/W), x=p%W;
      if(a.fen && (y<a.fen[0] || y>=a.fen[1])){
        /* hors de la fenêtre DÉCLARÉE : peinte en gris très sourd, comptée nulle part */
        dd[i]=18; dd[i+1]=18; dd[i+2]=22; dd[i+3]=255; continue; }
      if(dansMatiere(x,y)){ masque++;
        /* la matière exceptée se peint en bleu sourd : on VOIT ce qui est exclu */
        dd[i]=30; dd[i+1]=60; dd[i+2]=120; dd[i+3]=255; continue; }
      const dr=Math.abs(d1[i]-d2[i]), dg=Math.abs(d1[i+1]-d2[i+1]), db=Math.abs(d1[i+2]-d2[i+2]);
      const e=(dr+dg+db)>a.seuil;
      tot++; if(e) diff++;                       /* « écart » : hors matière, texte compris */
      if(dansTexte(x,y)){
        /* boîte de texte : peinte en vert sourd, différence ou non — l'image ne montre
           alors QUE ce qui n'est ni matière ni glyphe. Elle reste comptée dans « écart ». */
        dd[i]=e?70:34; dd[i+1]=e?96:52; dd[i+2]=e?46:34; dd[i+3]=255; continue;
      }
      totHG++; parBande[Math.floor(y/20)]++;      /* « hors glyphe » et ses bandes */
      if(e){ diffHG++; bandes[Math.floor(y/20)]++;
             dd[i]=255; dd[i+1]=0; dd[i+2]=90; dd[i+3]=255; }
      else { const g=(d1[i]*0.3+d1[i+1]*0.6+d1[i+2]*0.1);
             dd[i]=dd[i+1]=dd[i+2]=Math.round(40+g*0.35); dd[i+3]=255; }
    }
    go.putImageData(im,0,0);
    res({part: tot?Math.round(1000*diff/tot)/10:0, diff:diff, tot:tot,
         hg: totHG?Math.round(1000*diffHG/totHG)/10:0,
         masque: Math.round(1000*masque/(W*H))/10,
         bandes:bandes.map((v,k)=>[k*20, parBande[k]?Math.round(1000*v/parBande[k])/10:0])
                      .filter(b=>b[1]>2),
         png:out.toDataURL('image/png')});
  }
  A.onload=pret; B.onload=pret; A.src=a.a; B.src=a.b;
})"""


def main():
    sortie = sys.argv[1]
    voulus = sys.argv[2:]
    os.makedirs(sortie, exist_ok=True)
    res = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        # ── les cadres de la planche, capturés une fois ──
        cadres = {}
        for url in (MBH, NUT):
            pg = b.new_page(viewport={'width': 1400, 'height': 1000}, device_scale_factor=2)
            pg.goto(url)
            pg.wait_for_timeout(4500)
            pg.evaluate(MARQUE)
            for E in ECRANS:
                nom, u, (cs, cl) = E[0], E[1], E[2]
                if u != url:
                    continue
                for th, n in (('dark', cs), ('light', cl)):
                    el = pg.query_selector('[data-cadre="%d"]' % n)
                    if el:
                        cadres[(nom, th)] = base64.b64encode(el.screenshot()).decode()
            pg.close()

        # ── l'app ──
        app = {}
        # ⚠ 430 × 932, PAS 390 × 844 — ET C'EST UNE CORRECTION DE MESURE, PAS UN CONFORT.
        #   `.frame` se met à l'échelle pour tenir dans la fenêtre : à 390 × 844, `#device`
        #   sort à **363,87 × 787,45**, soit 0,933. Les juges le savent (ils divisent par
        #   `dev.width/390`) ; le comparateur PIXEL, lui, ré-échantillonnait toute la
        #   capture de 0,933 à 1 — chaque glyphe se retrouvait entre deux pixels, et
        #   AUCUN écran ne pouvait tomber à zéro, quoi qu'on corrige.
        #   Mesuré : 430 × 932 donne `#device` **390 × 844 exactement**.
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th)
            pg.wait_for_timeout(400)
            for E in ECRANS:
                nom, u, js = E[0], E[1], E[3]
                if voulus and nom not in voulus:
                    continue
                pg.evaluate("()=>{if(window.closeAll)closeAll();}")
                pg.wait_for_timeout(400)
                try:
                    pg.evaluate(js)
                except Exception as e:
                    print('  ⚠ mise en scène %s : %s' % (nom, e))
                # ⚠ ON ATTEND QUE L'ÉCRAN SOIT COMPOSÉ, ON NE DEVINE PAS UN DÉLAI.
                #   À 2 000 ms, la capture de « fiche-tenue » sortait SANS SA DALLE et SANS
                #   sa barre Peaufiner — deux nœuds que l'app pose après coup (`_ficheDalle`
                #   repeint sur deux rAF, `_ficheCotes` pose ses `display` en ligne).
                #   On attend donc deux relevés identiques de ce qui est réellement peint.
                #   ⚠ ET UN PLANCHER DE 2 200 ms AVANT DE COMMENCER À COMPTER. Le compte
                #     de nœuds visibles se stabilise AVANT que tout soit peint : la barre
                #     Peaufiner d'une fiche entrait en transition et la capture partait
                #     sans elle — mesuré, et **reproductible** : « fiche-tenue clair »
                #     sortait à 15,9 % deux fois de suite, contre 4,7 % la même fiche
                #     capturée après 2 600 ms. Le nombre de nœuds ne dit pas qu'ils sont
                #     PEINTS ; le plancher, lui, laisse la transition finir.
                pg.wait_for_timeout(2200)
                prec = None
                for _ in range(24):
                    pg.wait_for_timeout(250)
                    etat = pg.evaluate("""()=>{
                      const n=[...document.querySelectorAll('#device canvas')]
                        .filter(c=>c.getBoundingClientRect().width>4).length;
                      const t=[...document.querySelectorAll('#device *')]
                        .filter(e=>{const r=e.getBoundingClientRect();
                          return r.width>4&&r.height>4&&getComputedStyle(e).visibility!=='hidden';}).length;
                      return n+':'+t;}""")
                    if etat == prec:
                        break
                    prec = etat
                pg.wait_for_timeout(600)
                zones = pg.evaluate("()=>window._zonesMatiere?window._zonesMatiere():{zones:[],part:0}")
                textes = pg.evaluate("()=>window._zonesTexte?window._zonesTexte():{zones:[],part:0}")
                app[(nom, th)] = (base64.b64encode(
                    pg.query_selector('#device').screenshot()).decode(), zones, textes)
        pg.close()

        # ── la différence, calculée en canvas ──
        pg = b.new_page(viewport={'width': 500, 'height': 900})
        pg.goto('about:blank')
        for (nom, th), (img, zones, textes) in sorted(app.items()):
            ref = cadres.get((nom, th))
            if not ref:
                print('  ⚠ pas de cadre pour %s [%s]' % (nom, th))
                continue
            r = pg.evaluate(DIFF, {'a': 'data:image/png;base64,' + ref,
                                   'b': 'data:image/png;base64,' + img,
                                   'seuil': 60, 'zones': zones['zones'],
                                   'textes': textes['zones'], 'fen': FEN.get(nom)})
            res.append((nom, th, r['part'], r['bandes'], r['masque'], r['hg']))
            for etq, data in (('mb', ref), ('app', img), ('diff', r['png'].split(',', 1)[1])):
                io = open(os.path.join(sortie, '%s_%s_%s.png' % (nom, th, etq)), 'wb')
                io.write(base64.b64decode(data))
                io.close()
        b.close()

    print('\n%-16s %-6s %8s %9s %8s   bandes qui diffèrent (y, %%)'
          % ('écran', 'thème', 'écart', 'h. glyphe', 'matière'))
    print('-' * 96)
    for nom, th, part, bandes, masque, hg in sorted(res, key=lambda x: -x[5]):
        b3 = ' '.join('%d:%.0f%%' % (y, p) for y, p in bandes[:6])
        if os.environ.get('DUO_BANDES'): b3 = ' '.join('%d:%.0f%%' % (y, p) for y, p in bandes)
        fen = FEN.get(nom)
        marque = ('  [y %d→%d]' % fen) if fen else ''
        print('%-16s %-6s %7.1f%% %8.1f%% %7.1f%%   %s%s' % (nom, th, part, hg, masque, b3, marque))
    print('\n« écart »     : hors matière — matière = la zone que l\'app déclare (`_zonesMatiere`),')
    print('                peinte en bleu sourd sur l\'image de diff.')
    print('« h. glyphe » : hors matière ET hors boîtes de texte (`_zonesTexte`). La planche est')
    print('                composée en Hanken Grotesk et Bricolage Grotesque (Google) ; l\'app porte')
    print('                ses six faces EMBARQUÉES (CLAUDE.md §6). Les dessins de glyphes ne peuvent')
    print('                pas coïncider — la BOÎTE du texte, elle, le doit, et les juges la mesurent.')
    print('\nimages dans', sortie)


main()
