#!/usr/bin/env python3
"""Capture les cadres de la planche et cherche les recouvrements — CADRE PAR CADRE.

⚠ POURQUOI CADRE PAR CADRE, et pas en une passe.
`document.elementsFromPoint` travaille en coordonnées de FENÊTRE. Une planche fait
plusieurs milliers de pixels de haut : les cadres du bas sont HORS de la fenêtre, et
la confirmation au doigt y rend une liste VIDE — donc aucun recouvrement, jamais.
L'outil annonçait « 0 » sur des cadres qu'il n'avait pas regardés.
Prouvé : deux textes superposés à dessein dans un cadre du bas n'étaient PAS pris.
On amène donc chaque cadre dans la fenêtre avant de l'interroger.
Preuve que l'outil mord : scratchpad/preuve_collisions.py
"""
import json
from playwright.sync_api import sync_playwright

REGLE = r"""(fi)=>{
  const f = document.querySelectorAll('.fr')[fi];
  const out = [];
  const ns = [...f.querySelectorAll('*')].filter(n=>{
    const cs=getComputedStyle(n), r=n.getBoundingClientRect();
    if(cs.display==='none'||cs.visibility==='hidden'||r.width<1||r.height<1) return false;
    if(n.children.length===0) return true;
    // ⚠ UNE BOÎTE PEINTE COMPTE, MÊME SI ELLE A DES ENFANTS.
    // Le bouton « Partager mon Noyau » chevauchait la dernière rangée de la moisson,
    // et l'outil n'a rien dit : il ne regardait que les FEUILLES, et un bouton bordé
    // porte un <span>. Un cadre de 2 px qui passe sur une dalle est un recouvrement.
    const b = parseFloat(cs.borderTopWidth)||0;
    const fond = cs.backgroundColor && !/^rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor);
    return b > 0 || fond;
  });
  const SURF = n => n.tagName==='CANVAS' || n.ownerSVGElement || n.tagName==='svg';
  const dedans = (p,q) => p.left<=q.left+1 && p.top<=q.top+1
                       && p.right>=q.right-1 && p.bottom>=q.bottom-1;
  for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++){
    if(ns[i].contains(ns[j])||ns[j].contains(ns[i]))continue;
    const a=ns[i].getBoundingClientRect(), b=ns[j].getBoundingClientRect();
    // UNE MARQUE POSÉE SUR SA SURFACE N'EST PAS UN RECOUVREMENT : une dalle peinte
    // sur la frise, un visage tracé dans son anneau. On n'exempte QUE la containment
    // géométrique, et seulement sur une SURFACE (canevas ou SVG) : un texte qui
    // DÉBORDE d'un canevas reste pris, deux textes restent comparés intégralement.
    if(dedans(a,b) && SURF(ns[i])) continue;
    if(dedans(b,a) && SURF(ns[j])) continue;
    // ⚠ DEUX PARTIES DU MÊME OBJET NE SE PERCUTENT PAS, ELLES SE COMPOSENT.
    // La lune d'une personne passe au-dessus du carré de son propre anneau : le
    // dessin est juste (elle dégage le cercle de 4,5 px), c'est la BOÎTE du canevas
    // qui la croise dans son coin. Un objet est déclaré par data-role ; ses parties
    // internes sont exemptées entre elles, et entre elles SEULEMENT.
    const o1=ns[i].closest('[data-role]'), o2=ns[j].closest('[data-role]');
    if(o1 && o1===o2) continue;
    // ⚠ LA MASSE EST UNE SURFACE DE POINTS, PAS UNE BOÎTE. Son canevas couvre
    // 352 × 352 : au test boîte-contre-boîte elle recouvre TOUT, et un vert obtenu
    // en l'exemptant ne voudrait rien dire. On la sort de CE test — qui ne mesure
    // rien pour elle — et on la juge au PIXEL ailleurs : combien de points pose-t-elle
    // dans la boîte d'un prénom, combien devant un anneau. C'est plus dur, et c'est
    // prouvé contre un défaut planté (ctrl_sphere.py, la preuve à la fin).
    const masse = n => n.dataset && n.dataset.role==='masse';
    if(masse(ns[i])||masse(ns[j])) continue;
    // ⚠ LE CAPTEUR DU DOIGT EST UNE SURFACE TRANSPARENTE qui couvre la sphère : il
    // ne peint RIEN. Au test boîte-contre-boîte il « recouvre » les six anneaux et
    // ton Noyau — 91 faux recouvrements. On le sort de ce test, et sa vraie question
    // (les deux gestes sont-ils distingués ?) est mesurée ailleurs, au geste :
    // scratchpad/mesure_doigt.py, toucher immobile / 4 px / 41 px.
    const capteur = n => n.classList && n.classList.contains('prise');
    if(capteur(ns[i])||capteur(ns[j])) continue;
    // ⚠ EN 3D, DEUX PERSONNES SE RECOUVRENT — C'EST LE SUJET : l'une passe devant
    // l'autre. Ce n'est plus un défaut, c'est la profondeur. On l'EXEMPTE, et on met
    // à la place un contrôle plus dur : aucun anneau ne touche jamais ton Noyau,
    // vérifié sur 72 positions du tour (_verifOrbite).
    // ⚠ ON N'EXEMPTE QUE LES ANNEAUX ENTRE EUX. Deux anneaux qui se croisent, c'est
    // la profondeur — le sujet même. Deux NOMS qui se croisent, ou un nom sur un
    // anneau, c'est une faute : illisible. La première version exemptait les deux et
    // laissait passer une moitié d'écran illisible.
    const h1=o1&&o1.dataset.role==='pers', h2=o2&&o2.dataset.role==='pers';
    if(h1&&h2) continue;
    // ⚠ UN ANNEAU QUI PASSE DERRIÈRE TON NOYAU EST MASQUÉ PAR LUI — c'est le sujet.
    // Ton Noyau est à z 40 ; une personne derrière est sous 20. Le recouvrement est
    // alors une PROFONDEUR, pas une faute. Devant (z ≥ 20), il reste interdit, et
    // c'est _verifOrbite qui le mesure sur 72 positions.
    // ⚠ LE SEUIL ÉTAIT 20, IL EST 40 — ET C'EST LA MÊME RÈGLE, PAS UN ASSOUPLISSEMENT.
    // « Derrière ton Noyau » veut dire « d'un rang inférieur au sien ». Son rang est
    // 40 ; une personne va de 8 à 32. Depuis que le doigt peut amener n'importe qui
    // sur l'axe du regard, une personne PASSE derrière ton Noyau — Tom l'a écrit :
    // « quelqu'un de proche est près du centre, donc partiellement masqué par ton
    // Noyau, et c'est juste ». Le contrôle qui compte ça comme une faute est périmé ;
    // celui qui compte, et qui est plus dur, est dans ctrl_sphere.py : aucun anneau
    // n'atteint jamais le rang 40, sur 72 positions ET quatre points de vue, et au
    // doigt, sur neuf points du disque de ton Noyau, c'est bien LUI qu'on touche.
    const derriere = o => o && o.dataset.role==='pers' && (+o.style.zIndex||99) < 40;
    const centre = n => { const p=n.parentElement;
      return n.dataset && n.dataset.forme==='anneau' && p && !p.classList.contains('orb'); };
    if(centre(ns[i]) && derriere(o2)) continue;
    if(centre(ns[j]) && derriere(o1)) continue;
    // UNE LUNE QUI PASSE DERRIÈRE UN NOM NE CACHE RIEN. Le nom est à z 45, la lune
    // dans sa personne, bien plus bas : c'est elle qui disparaît un instant, pas le
    // nom. Le contrôle protège ce qui est COUVERT, pas ce qui couvre.
    const estLune = n => n.classList && n.classList.contains('lune');
    const estNom  = n => n.dataset && n.dataset.role==='nom';
    if((estLune(ns[i])&&estNom(ns[j]))||(estLune(ns[j])&&estNom(ns[i]))) continue;
    const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left);
    const oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    if(ox<=2||oy<=2) continue;
    // ⚠ UNE BOÎTE CARRÉE N'EST PAS LA FORME PEINTE QUAND LA FORME PEINTE EST UN ANNEAU.
    // Un canevas d'anneau déclare data-forme="anneau" et son rayon : on mesure alors
    // la distance du rectangle au CERCLE, pas au carré. Ce n'est pas un assouplissement,
    // c'est une mesure juste — et la preuve pose un texte VRAIMENT sur l'anneau pour
    // vérifier qu'il est toujours pris.
    const anneauLoin=(A,B)=>{                       // A = le canevas d'anneau
      const R=+A.dataset.rayon, ra=A.getBoundingClientRect(), rb=B.getBoundingClientRect();
      const cx=ra.left+ra.width/2, cy=ra.top+ra.height/2;
      const px=Math.max(rb.left,Math.min(cx,rb.right));
      const py=Math.max(rb.top,Math.min(cy,rb.bottom));
      return Math.hypot(px-cx,py-cy) > R+1;          // le rectangle ne touche pas le disque
    };
    if(ns[i].dataset && ns[i].dataset.forme==='anneau' && anneauLoin(ns[i],ns[j])) continue;
    if(ns[j].dataset && ns[j].dataset.forme==='anneau' && anneauLoin(ns[j],ns[i])) continue;
    const cx=(Math.max(a.left,b.left)+Math.min(a.right,b.right))/2;
    const cy=(Math.max(a.top,b.top)+Math.min(a.bottom,b.bottom))/2;
    if(cx<0||cy<0||cx>innerWidth||cy>innerHeight){ out.push(fi+' :: HORS FENÊTRE — non confirmé'); continue; }
    const els=document.elementsFromPoint(cx,cy);
    if(els.indexOf(ns[i])>=0 && els.indexOf(ns[j])>=0)
      out.push(fi+' :: '+(ns[i].className||ns[i].tagName)+' « '+(ns[i].textContent||'').trim().slice(0,20)+' »'
               +'  ⨯  '+(ns[j].className||ns[j].tagName)+' « '+(ns[j].textContent||'').trim().slice(0,20)+' »'
               +'  ('+Math.round(ox)+'x'+Math.round(oy)+')');
  }
  return out;
}"""

HORS = r"""(fi)=>{
  const f=document.querySelectorAll('.fr')[fi], F=f.getBoundingClientRect(), out=[];
  f.querySelectorAll('*').forEach(n=>{const cs=getComputedStyle(n),r=n.getBoundingClientRect();
    if(cs.display==='none'||r.width<1)return;
    if(r.left<F.left-0.5||r.right>F.right+0.5||r.top<F.top-0.5||r.bottom>F.bottom+0.5)
      out.push(fi+' :: '+(n.className||n.tagName)+' « '+(n.textContent||'').trim().slice(0,22)+' » x'
        +Math.round(r.left-F.left)+'→'+Math.round(r.right-F.left)
        +' / y'+Math.round(r.top-F.top)+'→'+Math.round(r.bottom-F.top));});
  return out;}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1800, 'height': 1400}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-SPHERE.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=120000)
    pg.wait_for_timeout(2500)
    # on FIGE l'orbite : une capture d'un objet animé ne se compare pas.
    # on FIGE l'orbite avant de capturer : une capture d'un objet anime ne se compare pas.
    pg.evaluate("()=>{window.__fige=true;}"); pg.wait_for_timeout(300)
    # les prenoms a leur CIBLE : on juge l etat pose, pas le transit du glissement
    pg.evaluate("()=>{window._nomsALaCible&&window._nomsALaCible();}")
    pg.wait_for_timeout(120)
    figs = pg.query_selector_all('figure')
    noms, recouv, hors = [], [], []
    for i, fg in enumerate(figs):
        cap = fg.query_selector('figcaption').inner_text()
        fr = fg.query_selector('.fr')
        fr.scroll_into_view_if_needed()          # ← LE CORRECTIF : le cadre entre dans la fenêtre
        pg.wait_for_timeout(180)
        path = 'scratchpad/sphere/%02d.png' % i
        bb=fr.bounding_box()
        pg.screenshot(path=path, clip=bb)   # clip : pas d'attente de stabilité
        noms.append((path, cap))
        recouv += pg.evaluate(REGLE, i)
        hors += pg.evaluate(HORS, i)
    for path, cap in noms:
        print('  %-28s %s' % (path, cap))
    print('\n── RECOUVREMENTS CONFIRMÉS AU DOIGT :', len(recouv))
    for r in recouv[:40]: print('   ', r)
    print('\n── HORS CADRE :', len(hors))
    for r in hors[:20]: print('   ', r)
    # ── LA LOI DE L'ORBITE : meme rayon, memes anneaux. Un classement dessine se mesure.
    v = pg.evaluate("()=>window._verifOrbite()")
    print('\n── AUCUN ANNEAU *DEVANT* TON NOYAU (72 positions) :', v['total'], 'ecart(s)')
    for r in v['ecarts']: print('   ', r)
    print('\n── LA PROFONDEUR : le plus petit %s px, le plus gros %s px  →  rapport %s'
          % (v['petit'], v['gros'], v['rapport']))
    print('   la boite de l\'orbite sur un tour : %s' % v['boite'])
    print('\n── LES SIX SONT-ILS DEDANS ? silhouette %s px · enveloppe %s px · sorties %d / 432'
          % (v['silhouette'], v['enveloppe'], v['dehors']))
    b.close()
