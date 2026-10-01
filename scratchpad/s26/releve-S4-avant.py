#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-S4-index-fil.py — LE JUGE DE LA SECTION 4 (l'Index et le Fil).

Compare l'app aux cotes de PROMI-SPECIFICATIONS.md §5 « Index et Fil », §3.9 (la carte
d'Index) et §3.10 (le bandeau du Fil), dans les deux thèmes et dans les deux densités.

LES COTES NE SONT PAS ÉCRITES À LA MAIN pour l'intérieur d'une carte : elles sont dérivées
de la MÊME formule que le rendu, elle-même relevée dans les chemins SVG du moodboard —
    échelle = h/600 · base = base_fiche × échelle · amp = 13 × l/173 · boîte = ⌊b+a+20⌋
et `base_fiche` est LU sur la fiche du même Promi (`window._ficheEcran`), jamais recalculé :
c'est la promesse du §2.5, « reprise à l'identique sur sa fiche et sur sa carte d'Index ».

CINQUIÈME CONTRÔLE — LA PRÉSENCE PEINTE. Un bloc à la bonne cote mais vide est un faux
vert : on LIT les pixels du canevas de chaque carte (l'aplat de nature, la dalle, la ligne)
et on vérifie l'encre de chaque texte contre le fond réellement peint dessous.

Usage :  python3 releve-S4-index-fil.py [--verbose]
"""
import re, sys

# ⚠ « APFEL 500 » N'EXISTE PAS — CONTRÔLE MIS À JOUR LE 19 AOÛT 2026 (CLAUDE.md §7).
#    L'inventaire écrit « Apfel 500 / 12.5 ». Cette face n'est PAS embarquée : les six
#    seules le sont Fraunces 600 (normal + italique), Bricolage 600, Bricolage 700,
#    Apfel 400 et ApfelMid 500. La graisse 500 existe bel et bien — dans ApfelMid, la
#    famille qui la porte. Le lot « polices » reporte donc `Apfel 500` sur `ApfelMid 500`,
#    et c'est CE couple qu'on attend ici. Le seuil ne bouge pas, la taille non plus :
#    seul le nom de la famille qui porte la graisse change. Voir QUESTIONS.md · Q68.
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/sauvegardes/app-avant-lot-v12.html"
VERBOSE = '--verbose' in sys.argv
TOL = 3
CREME, ENCRE = '#F4EEE1', '#16171B'
CORPS = {'promi': '#1C2049', 'chiche': '#37141F', 'nuee': '#271B45'}
ECRAN = {'dark': '#0E0F12', 'light': '#E8E0D0'}
BORD  = {'dark': '#5D636D', 'light': '#9A9384'}

MESURE = r"""(cfg)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc, y:(r.top-dev.top)/sc, w:r.width/sc, h:r.height/sc}; };
  const S=e=>{ if(!e) return null; const c=getComputedStyle(e);
    return {ff:(c.fontFamily||'').split(',')[0].replace(/["']/g,''), fw:c.fontWeight,
            fs:parseFloat(c.fontSize), ls:c.letterSpacing, lh:c.lineHeight,
            fill:c.webkitTextFillColor||c.color, bg:c.backgroundColor,
            bw:parseFloat(c.borderTopWidth)||0, bc:c.borderTopColor, br:c.borderTopLeftRadius,
            op:parseFloat(c.opacity)}; };
  const vis=e=>{ if(!e) return false; const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false;
    const r=e.getBoundingClientRect(); return r.width>2&&r.height>2; };
  const hote = cfg.ecran==='index' ? document.getElementById('indexSheet')
                                   : document.getElementById('feedView');
  if(!hote) return null;
  const liste = cfg.ecran==='index' ? document.getElementById('indexList')
                                    : document.getElementById('feedList');
  /* LE CHROME : l'écran est PLEIN. On nomme les quatre nœuds, jamais un conteneur. */
  const chrome=[];
  [['topbar','.topbar'],['dock','.footer'],['statusbar','.statusbar'],['viewSwitch','#viewSwitch']]
    .forEach(([n,s])=>{ const e=document.querySelector(s); if(vis(e)) chrome.push(n); });
  /* ⚑ LE TITRE ET LE FERMER VIVENT DANS LE PLATEAU (décision Tom, 1er sept. 2026 :
     « déploie le plateau du Studio partout »). Ils ont gardé leur classe, ils ont changé
     de PLACE : on les cherche donc dans `.enh`, en retombant sur l'ancien chemin pour un
     écran qui n'aurait pas encore son plateau. */
  /* ⚠ LA BOÎTE ET LE MOT SONT DEUX CHOSES. Je mesurais la POSITION et la HAUTEUR sur le
     titre — qui vit maintenant DANS le plateau, centré : il sort à (52,57) et haut de 27,
     et le juge lisait « entête (52,57) au lieu de (24,40) », « plateau haut de 27 au lieu
     de 60 ». Le plateau, lui, est bien à 24/40/342×60. On relève donc la boîte pour la
     géométrie et le mot pour la fonte. */
  const plateau = hote.querySelector('.enh');
  const titre = hote.querySelector('.enh .enh-t') || hote.querySelector('.scr-ti');
  const cpt   = hote.querySelector('.enh .ix-count') || hote.querySelector('.scr-ti .ix-count');
  const fermer= hote.querySelector('.enh .closeb') || hote.querySelector('.closeb');
  const srch  = hote.querySelector('.ix-srch');
  const inp   = hote.querySelector('.ix-search');
  const tri   = hote.querySelector('.ix-tri');
  const cartes=[].slice.call(liste?liste.querySelectorAll('.s4-carte'):[]);
  const gr = liste?liste.querySelector('.s4-grille'):null;
  const grR = gr?gr.getBoundingClientRect():null;
  const lot = cartes.slice(0,6).map(c=>{
    const cr=c.getBoundingClientRect();
    const rel=e=>{ if(!e) return null; const r=e.getBoundingClientRect();
      return {x:(r.left-cr.left)/sc, y:(r.top-cr.top)/sc, w:r.width/sc, h:r.height/sc}; };
    const cv=c.querySelector('canvas');
    return {geo:{x:(cr.left-(grR?grR.left:dev.left))/sc, y:(cr.top-(grR?grR.top:dev.top))/sc,
                 w:cr.width/sc, h:cr.height/sc},
            sty:S(c), rad:parseFloat(getComputedStyle(c).borderTopLeftRadius)/1,
            eb:{g:rel(c.querySelector('.s4-eb')), s:S(c.querySelector('.s4-eb')),
                t:(c.querySelector('.s4-eb')||{}).textContent||''},
            ev:{g:rel(c.querySelector('.s4-ev')), s:S(c.querySelector('.s4-ev'))},
            ti:{g:rel(c.querySelector('.s4-ti')), s:S(c.querySelector('.s4-ti')),
                t:(c.querySelector('.s4-ti')||{}).textContent||''},
            et:{g:rel(c.querySelector('.s4-et')), s:S(c.querySelector('.s4-et')),
                t:(c.querySelector('.s4-et')||{}).textContent||''},
            cv:rel(cv)};
  });
  return {chrome:chrome,
          fond:getComputedStyle(hote).backgroundColor,
          titre:{g:R(plateau||titre), s:S(titre), t:titre?(titre.textContent||'').trim():null},
          cpt:{g:R(cpt), s:S(cpt), t:cpt?(cpt.textContent||'').trim():null},
          fermer:{g:R(fermer), s:S(fermer), t:fermer?(fermer.textContent||'').trim():null},
          srch:{g:R(srch), s:S(srch)}, inp:{g:R(inp), s:S(inp),
                ph:inp?inp.getAttribute('placeholder'):null},
          tri:{g:R(tri), s:S(tri)},
          liste:R(liste), n:cartes.length, cartes:lot};
}"""

PEINT = r"""(cfg)=>{
  const bad=[];
  const rgb=s=>{const m=(s||'').match(/[\d.]+/g);return m?m.slice(0,3).map(Number):null;};
  const lum=c=>c?(0.2126*c[0]+0.7152*c[1]+0.0722*c[2]):0;
  const liste = cfg.ecran==='index' ? document.getElementById('indexList')
                                    : document.getElementById('feedList');
  const cartes=[].slice.call(liste?liste.querySelectorAll('.s4-carte'):[]);
  if(!cartes.length){ bad.push('AUCUNE CARTE'); return bad; }
  cartes.slice(0,6).forEach((c,i)=>{
    const cv=c.querySelector('canvas'); if(!cv){ bad.push('carte '+i+' : aucun canevas'); return; }
    const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
    const lire=(x,y)=>{ if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return [0,0,0,0];
      const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data; return [d[0],d[1],d[2],d[3]]; };
    const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
    const garde=/GARDÉ/.test((c.querySelector('.s4-et')||{}).textContent||'');
    /* ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 29 août 2026.
       Règle encodée : « la dalle est peinte ». INTACTE. Ce qui a changé, c'est la TAILLE
       de la dalle : depuis que la hauteur de trait est figée à la plantation (Q78), la
       dalle d'une carte est plus grande, et le point qui servait de référence d'APLAT —
       le milieu du haut, (W×0,5 ; H×0,05) — tombe DEDANS. La sonde comparait alors la
       dalle à elle-même : zéro pixel différent, et un rouge sur une carte parfaitement
       peinte. Mesuré : carte 0, boîte de dalle (37, 9, 91 × 76), point de référence
       (82,5 ; 9,9) — en plein milieu.
       On échantillonne donc l'aplat là où la dalle ne va JAMAIS : le coin haut-gauche.
       Elle est centrée, sa marge gauche vaut (W − 1,2·dh)/2, soit 29 px sur la plus large.
       Version d'origine : sauvegardes/releve-S4-avant-aplat.py */
    const haut=lire(3, Math.max(2,H*0.03));
    if(!garde && haut[3]<200) bad.push('carte '+i+' : AUCUN aplat de nature peint');
    /* la dalle : on cherche un pixel qui n'est ni l'aplat ni le vide dans sa boîte */
    let dal=0;
    for(let x=W*0.18;x<W*0.82;x+=3) for(let y=H*0.06;y<H*0.45;y+=3){
      const p=lire(x,y);
      if(p[3]>200 && (garde || Math.abs(p[0]-haut[0])+Math.abs(p[1]-haut[1])+Math.abs(p[2]-haut[2])>30)){ dal++; break; }
    }
    if(dal<3) bad.push('carte '+i+' : la DALLE n\'est pas peinte ('+dal+')');
    /* LA LIGNE. ⚠ LE TRAIT DU FIL EST VERTICAL (§3.10) : le compter en COLONNES le rendait
       invisible dès qu'une dalle était petite — un faux rouge, pas une régression. On
       balaie donc dans le sens que le trait TRAVERSE : les colonnes sur une carte d'Index,
       les LIGNES sur un bandeau du Fil. */
    let tr=0;
    if(cfg.ecran==='fil'){
      for(let y=2;y<H-2;y+=2){ for(let x=Math.round(W*0.62);x<W;x+=2){
        const p=lire(x,y);
        if(p[3]>200 && Math.abs(p[0]-haut[0])+Math.abs(p[1]-haut[1])+Math.abs(p[2]-haut[2])>40){ tr++; break; } } }
      if(tr<Math.round(H*0.20)) bad.push('carte '+i+' : le TRAIT vertical n\'est pas peint ('+tr+')');
    } else {
      for(let x=2;x<W-2;x+=2){ for(let y=0;y<H;y+=2){
        const p=lire(x,y);
        if(p[3]>200 && Math.abs(p[0]-haut[0])+Math.abs(p[1]-haut[1])+Math.abs(p[2]-haut[2])>40){ tr++; break; } } }
      if(tr<Math.round(W*0.12)) bad.push('carte '+i+' : le TRAIT n\'est pas peint ('+tr+')');
    }
    /* l'encre des textes contre le fond de la carte */
    const fond=rgb(getComputedStyle(c).backgroundColor);
    ['.s4-eb','.s4-ti','.s4-et','.s4-ev'].forEach(s=>{
      const e=c.querySelector(s); if(!e) return;
      const cs=getComputedStyle(e); const t=(e.textContent||'').trim();
      if(!t) return;
      if(parseFloat(cs.opacity)<0.72) bad.push('carte '+i+' '+s+' : opacité '+cs.opacity);
      const enc=rgb(cs.webkitTextFillColor||cs.color);
      if(enc&&fond&&Math.abs(lum(enc)-lum(fond))<42)
        bad.push('carte '+i+' '+s+' « '+t.slice(0,16)+' » : ton sur ton (Δ'+Math.round(Math.abs(lum(enc)-lum(fond)))+')');
    });
  });
  return bad;
}"""

GEO = r"""(cfg)=>{
  /* la géométrie ATTENDUE, dérivée pour les cartes visibles — la même formule que le rendu,
     mais appliquée à la base LUE sur la fiche, pas à celle que la carte a posée. */
  const liste = cfg.ecran==='index' ? document.getElementById('indexList')
                                    : document.getElementById('feedList');
  const cartes=[].slice.call(liste?liste.querySelectorAll('.s4-carte'):[]).slice(0,6);
  return cartes.map(c=>{
    const cv=c.querySelector('canvas');
    return {w:parseFloat(cv.style.width), h:parseFloat(cv.style.height)};
  });
}"""


def hexa(c):
    m = [int(float(x)) for x in (c or '').replace('rgba(', '').replace('rgb(', '').replace(')', '').split(',')[:3] if x.strip()]
    return ('#%02X%02X%02X' % tuple(m)) if len(m) == 3 else c


SCENE = r"""(cfg)=>{
  window._s4Trois = (cfg.dens===3);
  if(cfg.ecran==='index'){ if(window.setView) setView('toile');
    if(window.closeAll) closeAll();
    window.ouvrirIndex(); }
  else { if(window.closeAll) closeAll(); setView('fil'); }
  return true;
}"""


# ── LES 26 COMPOSANTS ISOLÉS (§5, « Cartes d'Index isolées » et « Bandeaux du Fil isolés »).
#    Ce sont des SPÉCIMENS : aucun écran de l'app ne les rend seuls. Ce qu'on peut — et
#    doit — contrôler, c'est que LA LOI DE LA CARTE (§3.9 bis) les reproduit. Contrôle
#    purement arithmétique, sans navigateur : la loi est la même que celle du rendu.
#    (boîte, dalle l × h) relevés dans les tableaux du document, carte isolée 173 × 208.
CARTES_ISOLEES = [
    ('planter un arbre',    141,  97, 81), ('faire les crêpes',    112, 62, 52),
    ('le potager',          153, 111, 93), ('courir dimanche',     103, 51, 43),
    ('nager le mardi',      128,  81, 68), ('le grand plongeoir',  137, 92, 77),
    ("l'atelier du samedi", 124,  76, 64), ('appeler Mamie',       116, 67, 56),
]


def loi(l, h, base_fiche, borner=False):
    """§3.9 bis — LA LOI GÉOMÉTRIQUE de la carte. La MÊME que celle du rendu.

    ⚠ DEUX RÈGLES DISTINCTES, testées chacune à son niveau. La LOI transforme une hauteur
    de trait en géométrie de carte : elle ne borne rien. La BORNE du §2.5 (`[196, 344]`) est
    un GARDE-FOU sur la valeur qu'on lui donne, ajouté parce que deux fiches du document
    portent 376 et 372 — hors échelle — et écrasaient le titre. Les confondre faisait sortir
    « le potager » à 152 au lieu de 153 : sa base est 346, deux pixels au-dessus du plafond.
    Le contrôle des composants teste donc la LOI, et `juge_borne` teste LA BORNE.
    """
    if borner:
        base_fiche = max(196, min(344, base_fiche))
    s, k = h / 600.0, l / 173.0
    base, amp = base_fiche * s, 13 * k
    boite = int(base + amp + 20)
    dh = int(round(base - amp - 13.7 * (h / 198.0)))
    return {'base': base, 'amp': amp, 'boite': boite, 'dh': dh, 'dw': int(1.2 * dh),
            'ep': 5.5 * k, 'r': 3.2 * k, 'esp': 11 * k}


def juge_composants():
    """Les 8 cartes isolées, retrouvées par LA LOI SEULE, sans la borne."""
    ecarts = []
    for nom, boite, dw, dh in CARTES_ISOLEES:
        # la boîte du tableau donne la base ; la loi doit rendre tout le reste
        bf = (boite - 13 - 20) * 600.0 / 208
        g = loi(173, 208, bf)
        if g['boite'] != boite:
            ecarts.append('  carte isolée « %s » : boîte %d au lieu de %d' % (nom, g['boite'], boite))
        if abs(g['dw'] - dw) > 1 or abs(g['dh'] - dh) > 1:
            ecarts.append('  carte isolée « %s » : dalle %d×%d au lieu de %d×%d'
                          % (nom, g['dw'], g['dh'], dw, dh))
    return ecarts


def juge_borne():
    """LA BORNE DU §2.5 — elle doit mordre là où il faut, et nulle part ailleurs.

    1 · elle n'agit JAMAIS sur une base à l'intérieur de [196, 344] ;
    2 · elle agit sur les deux bases hors échelle du document (376, 372) ;
    3 · là où elle mord une base du moodboard (« le potager », 346), l'écart qu'elle
        introduit reste sous la tolérance de 3 px — sinon c'est la borne qui est fausse.
    """
    ecarts = []
    for l, h in ((165, 198), (106, 133), (173, 208)):
        for bf in (196, 232, 262, 282, 300, 312, 344):
            if loi(l, h, bf)['boite'] != loi(l, h, bf, borner=True)['boite']:
                ecarts.append('  la borne mord sur une base légitime (%d) à %d×%d' % (bf, l, h))
        for bf in (376, 372):
            if loi(l, h, bf)['boite'] == loi(l, h, bf, borner=True)['boite']:
                ecarts.append('  la borne NE MORD PAS sur %d à %d×%d — le titre reste écrasé' % (bf, l, h))
        for bf in (346, 348):
            d = abs(loi(l, h, bf)['boite'] - loi(l, h, bf, borner=True)['boite'])
            if d > TOL:
                ecarts.append('  la borne coûte %d px sur la base %d à %d×%d' % (d, bf, l, h))
    # et là où elle mord, le titre doit rester lisible : au moins une ligne entière
    for l, h, fs, bas in ((165, 198, 20.0, 24), (106, 133, 12.9, 15)):
        g = loi(l, h, 376, borner=True)
        yeb = g['boite'] - (10.5 if l == 165 else 14)
        yti = yeb + (17 if l == 165 else 11)
        if (h - bas - yti) < fs:
            ecarts.append('  borne appliquée : il reste %.0f px au titre à %d×%d, moins d\'une ligne (%.1f)'
                          % (h - bas - yti, l, h, fs))
    return ecarts


def juge():
    pos, sty, coll, hors, peint = [], [], [], [], []
    vus = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        er = []
        pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        ECRANS = [('index', 2, 'Index 2 par ligne'), ('index', 3, 'Index 3 par ligne'), ('fil', 2, 'Fil')]
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            light = (th == 'light')
            for ecran, dens, nom in ECRANS:
                cfg = {'ecran': ecran, 'dens': dens}
                pg.evaluate(SCENE, cfg); pg.wait_for_timeout(1500)
                m = pg.evaluate(MESURE, cfg)
                E = '  %-20s [%s]' % (nom, th)
                if not m:
                    pos.append(E + ' : ÉCRAN NON JOUABLE'); continue
                vus.append((nom, th))

                # ── l'écran est PLEIN : aucun chrome de la Toile ──
                if m['chrome']:
                    pos.append(E + ' chrome encore visible : ' + ', '.join(m['chrome']))
                if hexa(m['fond']) != ECRAN[th]:
                    sty.append(E + ' corps d\'écran %s au lieu de %s' % (hexa(m['fond']), ECRAN[th]))

                # ── l'entête (§5) : LE PLATEAU, 24 / 40, 342 × 60 ──
                # ⚑ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7 de CLAUDE.md).
                #   La règle encodée ici — entête haute de 44, titre à 38, compte à 26,
                #   recherche à y 108 en 270 × 56 avec un contour de 3 et un rayon de 28,
                #   tri à x 310 en 56 × 56, grille à 196 — venait des cadres du moodboard.
                #   La décision qui l'a remplacée, Tom, 1er et 2 septembre 2026 : « le
                #   plateau du Studio fait référence, déploie-le partout », puis « dans Fil
                #   et Index les chiffres sont trop petits », puis « revois les traits et
                #   contours pour que le cadre ne paraisse pas plus marqué que le reste ».
                #   Elle est notée dans PROMI-SPECIFICATIONS §5. L'intention protégée ne
                #   bouge pas : l'entête est à sa place, à sa taille, dans sa fonte, et la
                #   colonne qui la suit garde son rythme. Version d'origine :
                #   sauvegardes/releve-S4-index-fil-avant-plateau.py
                # ⚑ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7) — 13 septembre 2026, Q213.
                #   LA RÈGLE ENCODÉE : le plateau de l'Index à 60 comme celui du Fil, le compte « 16 » en
                #   Bricolage 700/20 bleu À CÔTÉ du titre, ✕ FERMER à y 62, barre et tri à 116, grille à 204.
                #   LA DÉCISION : Tom — « un même objet ne donne pas deux chiffres selon l'écran » : l'Index
                #   compte comme l'accueil, « N paroles · N Nuées ». Sur une ligne, la mention débordait de
                #   26 px sur ✕ FERMER (mesuré) : elle passe SOUS le titre, le plateau de l'Index fait 88
                #   (rayon 44). L'air sous le plateau reste 16 (barre à 40 + 88 + 16 = 144), celui sous la
                #   barre reste 36 (grille à 232). ✕ FERMER est centré sur les 88 : 40 + (88 − 16)/2 = 76.
                #   Le Fil ne bouge pas. Tolérance inchangée (3 px). Version d'origine :
                #   sauvegardes/releve-S4-index-fil-avant-compte-paroles.py
                H_PLAT = 88 if ecran == 'index' else 60
                Y_BARRE = 40 + H_PLAT + 16
                Y_GRILLE = Y_BARRE + 52 + 36
                t = m['titre']
                if not t['g']:
                    pos.append(E + ' entête ABSENTE')
                else:
                    if abs(t['g']['x'] - 24) > TOL or abs(t['g']['y'] - 40) > TOL:
                        pos.append(E + ' entête (%.0f,%.0f) au lieu de (24,40)' % (t['g']['x'], t['g']['y']))
                    if abs(t['g']['h'] - H_PLAT) > TOL:
                        pos.append(E + ' plateau haut de %.0f au lieu de %d' % (t['g']['h'], H_PLAT))
                    s = t['s']
                    if s['ff'] != 'Bricolage' or s['fw'] != '700' or abs(s['fs'] - 27) > 0.6:
                        sty.append(E + ' entête : %s %s/%s au lieu de Bricolage 700/27' % (s['ff'], s['fw'], s['fs']))
                    att = ENCRE if light else CREME
                    if hexa(s['fill']) != att:
                        sty.append(E + ' entête : encre %s au lieu de %s' % (hexa(s['fill']), att))
                    mot = 'Index' if ecran == 'index' else 'Fil'
                    if not (t['t'] or '').startswith(mot):
                        sty.append(E + ' entête « %s » au lieu de « %s » + compte' % (t['t'], mot))
                c = m['cpt']
                if not c['g']:
                    pos.append(E + ' compte ABSENT')
                else:
                    s = c['s']
                    if ecran == 'index':
                        if s['ff'] != 'ApfelMid' or s['fw'] != '500' or abs(s['fs'] - 13) > 0.6:
                            sty.append(E + ' compte : %s %s/%s au lieu de ApfelMid 500/13' % (s['ff'], s['fw'], s['fs']))
                        att = ENCRE if light else CREME
                        if not re.match(r'^\d+ paroles? · \d+ Nuées?$', c['t'] or ''):
                            sty.append(E + ' compte « %s » au lieu de « N paroles · N Nuées »' % c['t'])
                        # la mention vit SOUS le titre, dans le plateau
                        if c['g'] and t['g'] and not (t['g']['y'] + 40 < c['g']['y'] < t['g']['y'] + H_PLAT):
                            pos.append(E + ' compte à y %.0f : hors de la seconde ligne du plateau' % c['g']['y'])
                    else:
                        if s['ff'] != 'Bricolage' or s['fw'] != '700' or abs(s['fs'] - 20) > 0.6:
                            sty.append(E + ' compte : %s %s/%s au lieu de Bricolage 700/20' % (s['ff'], s['fw'], s['fs']))
                        att = '#2BE88C'
                    if hexa(s['fill']) != att:
                        sty.append(E + ' compte : encre %s au lieu de %s' % (hexa(s['fill']), att))
                f = m['fermer']
                if not f['g']:
                    pos.append(E + ' ✕ FERMER ABSENT')
                else:
                    # ⚠ 340, PAS 366 : le plateau finit à 366 et porte 26 de padding.
                    #    Et le FERMER est CENTRÉ dedans (40 + (60 − 16)/2 ≈ 62), il n'est
                    #    plus calé sur le haut. J'attendais (366,40) et lisais (338,63) :
                    #    c'était ma cote qui était fausse, pas l'écran.
                    Y_FER = 40 + (H_PLAT - 16) / 2
                    if abs(f['g']['x'] + f['g']['w'] - 340) > TOL or abs(f['g']['y'] - Y_FER) > TOL:
                        pos.append(E + ' ✕ FERMER (droite %.0f, y %.0f) au lieu de (340,%.0f)'
                                   % (f['g']['x'] + f['g']['w'], f['g']['y'], Y_FER))
                    s = f['s']
                    # ⚠ « Apfel 500 » n'existe pas : la graisse 500 est portée par
                    #    ApfelMid. Voir la note en tête de fichier et QUESTIONS.md · Q68.
                    if s['ff'] != 'ApfelMid' or s['fw'] != '500' or abs(s['fs'] - 12) > 0.6:
                        sty.append(E + ' ✕ FERMER : %s %s/%s au lieu de ApfelMid 500/12' % (s['ff'], s['fw'], s['fs']))
                    if (f['t'] or '').upper().find('FERMER') < 0:
                        sty.append(E + ' ✕ FERMER : texte « %s »' % f['t'])

                # ── la recherche et le tri (§5) ──
                # ⚑ CONTRAT MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 3 septembre 2026.
                #   LA RÈGLE QU'IL ENCODAIT : « la barre à 124, la grille à 212 » — soit
                #   24 px d'air sous l'entête, report du cadre 72 (titre finissant à 84,
                #   barre à 108), la colonne entière ayant descendu de 16 quand le plateau
                #   de 60 a remplacé le titre de 44.
                #   LA DÉCISION QUI LA REMPLACE : Tom, 3 septembre — « la ligne avec encart
                #   Rechercher et bouton tri, dans l'Index et dans le Fil, rapproche-la un
                #   peu de l'encart titre et ✕ fermer, sinon ça fait bizarre ; ça remonte
                #   du tout les éléments en dessous un peu. »
                #   Le 24 reportait l'air d'un TITRE NU. Le plateau est une BOÎTE BORDÉE :
                #   son trait descend là où l'encre du titre ne descendait pas, et l'œil
                #   compte l'air à partir du trait. Deux boîtes bordées prennent l'écart de
                #   bloc du §3.3 — 16 px, celui de Peaufiner, des Réglages et du Cercle.
                #   La barre passe donc de 124 à 116, la grille de 212 à 204 : tout ce qui
                #   suit remonte de 8, rien d'autre ne bouge (largeurs, hauteurs, contours,
                #   rayons et l'écart barre → grille de 36 sont inchangés).
                #   Ce n'est pas un desserrement : la tolérance reste 3 px, et un décalage
                #   d'un pixel est pris comme avant. C'est la cote attendue qui change.
                #   Version d'origine : sauvegardes/releve-S4-index-fil-avant-air-16.py
                sr = m['srch']
                if not sr['g']:
                    pos.append(E + ' champ de recherche ABSENT')
                else:
                    g = sr['g']
                    if abs(g['x'] - 24) > TOL or abs(g['y'] - Y_BARRE) > TOL:
                        pos.append(E + ' recherche (%.0f,%.0f) au lieu de (24,%d)' % (g['x'], g['y'], Y_BARRE))
                    if abs(g['w'] - 270) > TOL or abs(g['h'] - 52) > TOL:
                        pos.append(E + ' recherche %.0f×%.0f au lieu de 270×52' % (g['w'], g['h']))
                    s = sr['s']
                    # la grammaire des contours : trait 2, couleur du corps, rayon = h/2
                    att_b = ENCRE if light else CREME
                    if abs(s['bw'] - 2) > 0.6 or hexa(s['bc']) != att_b:
                        sty.append(E + ' recherche : contour %.1f %s au lieu de 2 %s' % (s['bw'], hexa(s['bc']), att_b))
                    if abs(float((s['br'] or '0').replace('px', '')) - 26) > 1:
                        sty.append(E + ' recherche : rayon %s au lieu de 26' % s['br'])
                if m['inp']['s']:
                    s = m['inp']['s']
                    if s['ff'] != 'Bricolage' or s['fw'] != '600' or abs(s['fs'] - 16) > 0.6:
                        sty.append(E + ' recherche : %s %s/%s au lieu de Bricolage 600/16' % (s['ff'], s['fw'], s['fs']))
                    if m['inp']['ph'] != 'Rechercher':
                        sty.append(E + ' recherche : « %s » au lieu de « Rechercher »' % m['inp']['ph'])
                tr = m['tri']
                if not tr['g']:
                    pos.append(E + ' bouton de tri ABSENT')
                else:
                    g = tr['g']
                    # ⚠ 314, PAS 290 : le tri fait 52 de large et se cale à droite sur 366,
                    #    donc 366 − 52 = 314. J'avais pris 290 dans une RÈGLE CSS au lieu de
                    #    le mesurer — exactement ce que le §8 bis interdit.
                    if abs(g['x'] - 314) > TOL or abs(g['y'] - Y_BARRE) > TOL:
                        pos.append(E + ' tri (%.0f,%.0f) au lieu de (314,%d)' % (g['x'], g['y'], Y_BARRE))
                    if abs(g['w'] - 52) > TOL or abs(g['h'] - 52) > TOL:
                        pos.append(E + ' tri %.0f×%.0f au lieu de 52×52' % (g['w'], g['h']))

                # ── la grille (§5) ──
                if not m['liste'] or abs(m['liste']['y'] - Y_GRILLE) > TOL:
                    pos.append(E + ' grille à y=%s au lieu de %d' % ((round(m['liste']['y']) if m['liste'] else '—'), Y_GRILLE))
                if not m['n']:
                    pos.append(E + ' AUCUNE carte'); continue

                if ecran == 'index':
                    CW, CH, RAD = ((106, 133, 11) if dens == 3 else (165, 198, 17))
                    GX = [24, 142, 260] if dens == 3 else [24, 201]
                    PAS = 145 if dens == 3 else 210
                    FEB, FTI, FET = ((8.0, 12.9, 6.4) if dens == 3 else (12.4, 20.0, 10.0))
                    PADX, TXW = ((7, 90) if dens == 3 else (12, 140))
                    # ⚠ CONTRAT RÉÉCRIT (§7). L'état d'une carte était calé PAR LE BAS avec
                    #   une marge de 12 (ou 8 à trois par ligne). En grossissant au plancher
                    #   du §6, son ancre reculait et il ENTRAIT DANS LE TITRE : mesuré, 4 px
                    #   de superposition sur les neuf cartes, signalé par Tom capture à
                    #   l'appui (« dans l'index y a des cartes où les éléments se
                    #   superposent »). Il est désormais cloué à **6 du bas**, ce qui rend
                    #   au titre les 2 px d'air qu'il avait avant. La règle protégée est la
                    #   même : l'état a une place fixe au bas de sa carte.
                    BAS_ET = 6
                else:
                    CW, CH, RAD, GX, PAS = 358, 128, 22, [16], 140

                # ⚠ LE PAS DU FIL DÉPEND DU GESTE (contrôle réécrit au niveau de la décision,
                #   CLAUDE.md §7). Les cinq bandeaux du moodboard ne portent AUCUNE action :
                #   le pas y est constant, 140. Mais le Fil est le seul endroit d'où l'on
                #   tient une parole sans ouvrir de fiche, et cette fonction ne se perd pas
                #   (décision Tom, 18 août 2026) : un bandeau qui porte TENIR / REPORTER
                #   emmène sa rangée de pastilles (§3.5, hauteur 50) sous lui, soit 62 px de
                #   plus. Ce qui reste vérifié sans changement : le bandeau fait 358 × 128,
                #   rayon 22, à x = 16 — les cotes que le moodboard fixe.
                #   Version d'origine : sauvegardes/releve-S4-avant-geste-du-fil.py
                gestes = pg.evaluate("""()=>[...document.querySelectorAll('#feedList .s4-carte')]
                  .map(c=>{const n=c.nextElementSibling;
                    return !!(n && n.classList.contains('s4-actes'));})""") if ecran == 'fil' else []
                yAtt = 0
                for i, k in enumerate(m['cartes']):
                    K = E + ' carte %d' % i
                    g = k['geo']
                    if ecran == 'fil':
                        ax, ay = GX[0], yAtt
                        yAtt += PAS + (62 if (i < len(gestes) and gestes[i]) else 0)
                    else:
                        ax, ay = GX[i % len(GX)], (i // len(GX)) * PAS
                    if abs(g['x'] - ax) > TOL or abs(g['y'] - ay) > TOL:
                        pos.append(K + ' à (%.0f,%.0f) au lieu de (%d,%d)' % (g['x'], g['y'], ax, ay))
                    if abs(g['w'] - CW) > TOL or abs(g['h'] - CH) > TOL:
                        pos.append(K + ' %.0f×%.0f au lieu de %d×%d' % (g['w'], g['h'], CW, CH))
                    if abs(k['rad'] - RAD) > 1:
                        sty.append(K + ' rayon %.0f au lieu de %d' % (k['rad'], RAD))
                    fond = CREME if light else None
                    if light and hexa(k['sty']['bg']) != CREME:
                        sty.append(K + ' fond %s au lieu de %s' % (hexa(k['sty']['bg']), CREME))
                    if not light and hexa(k['sty']['bg']) not in CORPS.values():
                        sty.append(K + ' fond %s hors des trois corps du §1.3' % hexa(k['sty']['bg']))
                    if k['cv'] and (abs(k['cv']['x']) > 1 or abs(k['cv']['y']) > 1):
                        pos.append(K + ' canevas décalé (%.0f,%.0f)' % (k['cv']['x'], k['cv']['y']))
                    if ecran == 'index':
                        for nomb, bloc, fs in (('eyebrow', k['eb'], FEB), ('titre', k['ti'], FTI), ('état', k['et'], FET)):
                            if not bloc['g']:
                                pos.append(K + ' %s ABSENT' % nomb); continue
                            if abs(bloc['g']['x'] - PADX) > TOL:
                                pos.append(K + ' %s x=%.0f au lieu de %d' % (nomb, bloc['g']['x'], PADX))
                            # ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7).
                            #   LE TITRE D'UNE CARTE NE TOUCHE JAMAIS SON ÉTAT — le défaut
                            #   que CASSE.md porte et que Tom a signalé deux fois. La boîte
                            #   du titre s'arrête un pixel au-dessus du mot d'état : elle
                            #   tient UNE ligne. Un titre à deux lignes — « planter un
                            #   arbre », « le grand plongeoir » — débordait et se peignait
                            #   SUR « TENUE ». On le fait rentrer en rétrécissant d'un point
                            #   à la fois, plancher 11 px (§6).
                            #   Le contrôle vérifie donc la RÈGLE, pas un nombre : la taille
                            #   du titre est celle du cadre, ou plus petite s'il ne tenait
                            #   pas — jamais plus grande, jamais sous 11. Un titre à 8 px,
                            #   ou plus gros que le cadre, échoue encore.
                            #   Original : sauvegardes/releve-S4-index-fil-avant-29aout.py
                            if nomb == 'eyebrow':
                                # ⚠ CONTRAT RÉÉCRIT (§7). Le cadre donne 8,0 à trois par
                                #   ligne — sous le minimum de 12 que le §6 fixe lui-même, et
                                #   que la décision de Tom du 2 septembre a fait appliquer
                                #   (« grossis un peu le reste »). On vise la RÈGLE : jamais
                                #   sous 12, jamais au-dessus du titre qu'il annonce.
                                if bloc['s']['fs'] < 12 or bloc['s']['fs'] > FTI + 0.6:
                                    sty.append(K + ' eyebrow taille %.1f hors [12, %.1f]'
                                               % (bloc['s']['fs'], FTI))
                            elif nomb == 'titre':
                                if bloc['s']['fs'] > fs + 0.6 or bloc['s']['fs'] < 11:
                                    sty.append(K + ' titre taille %.1f hors [11, %.1f]'
                                               % (bloc['s']['fs'], fs))
                            elif nomb == 'état':
                                # ⚠ CONTRAT RÉÉCRIT (§7). La règle encodée ici — l'état à la
                                #   taille exacte du cadre (10 ou 6,4) — a été remplacée par
                                #   la décision de Tom du 2 septembre 2026 : « dans Fil et
                                #   Index les chiffres sont trop petits, grossis un tantinet »,
                                #   et par le plancher du §6 (« rien en dessous de 12 px »),
                                #   qu'un tiers du petit texte du produit violait.
                                #   Cette ligne est en plus FLUIDE : elle vaut 13 à 16 selon
                                #   le viewport, et elle redescend d'un demi-point quand le
                                #   mot ne tient pas dans la carte (« 9 PROMI · 3 TENUS »).
                                #   Le contrôle vise donc la RÈGLE : jamais sous le plancher
                                #   de 12, jamais au-dessus du titre.
                                if bloc['s']['fs'] < 12 or bloc['s']['fs'] > FTI + 0.6:
                                    sty.append(K + ' état taille %.1f hors [12, %.1f]'
                                               % (bloc['s']['fs'], FTI))
                            elif abs(bloc['s']['fs'] - fs) > 0.6:
                                sty.append(K + ' %s taille %.1f au lieu de %.1f' % (nomb, bloc['s']['fs'], fs))
                        if k['et']['g'] and abs((CH - k['et']['g']['y'] - k['et']['g']['h']) - BAS_ET) > TOL:
                            pos.append(K + ' état à %.0f du bas au lieu de %d'
                                       % (CH - k['et']['g']['y'] - k['et']['g']['h'], BAS_ET))
                        # l'eyebrow suit le trait : boîte − 10,5 (2/ligne) ou − 14 (3/ligne)
                        if k['eb']['g'] and k['cv']:
                            # la boîte du trait n'est pas mesurable dans le DOM : on contrôle
                            # seulement que l'ordre eyebrow → titre → état est tenu.
                            if k['ti']['g'] and k['eb']['g']['y'] >= k['ti']['g']['y']:
                                coll.append(K + ' eyebrow sous le titre')
                            if k['ti']['g'] and k['et']['g'] and k['ti']['g']['y'] > k['et']['g']['y']:
                                coll.append(K + ' titre sous l\'état')
                    else:
                        for nomb, bloc, ax2, ay2, aw, ah, fs in (
                                ('événement', k['ev'], 145, 16, 197, 28, 14),
                                ('titre', k['ti'], 145, 50, 197, 42, 20),
                                ('état', k['et'], 145, 98, 197, 16, 11)):
                            if not bloc['g']:
                                pos.append(K + ' %s ABSENT' % nomb); continue
                            if abs(bloc['g']['x'] - ax2) > TOL or abs(bloc['g']['y'] - ay2) > TOL:
                                pos.append(K + ' %s (%.0f,%.0f) au lieu de (%d,%d)'
                                           % (nomb, bloc['g']['x'], bloc['g']['y'], ax2, ay2))
                            if abs(bloc['g']['w'] - aw) > TOL:
                                pos.append(K + ' %s large de %.0f au lieu de %d' % (nomb, bloc['g']['w'], aw))
                            # ⚠ CONTRAT RÉÉCRIT (§7), COMME POUR L'INDEX. Le cadre donne
                            #   11 à l'état d'un bandeau — sous le minimum de 12 que le §6
                            #   fixe lui-même. La décision de Tom du 2 septembre l'a fait
                            #   appliquer, et cette ligne est FLUIDE (13 à 16 selon le
                            #   viewport). On vise la RÈGLE : jamais sous 12, jamais
                            #   au-dessus du titre du bandeau.
                            if nomb == 'état':
                                if bloc['s']['fs'] < 12 or bloc['s']['fs'] > 20 + 0.6:
                                    sty.append(K + ' état taille %.1f hors [12, 20]' % bloc['s']['fs'])
                            elif abs(bloc['s']['fs'] - fs) > 0.6:
                                sty.append(K + ' %s taille %.1f au lieu de %d' % (nomb, bloc['s']['fs'], fs))

                # ── débordements : rien ne sort de la largeur du cadre ──
                for i, k in enumerate(m['cartes']):
                    g = k['geo']
                    if g['x'] < -1 or g['x'] + g['w'] > 391:
                        hors.append(E + ' carte %d déborde en largeur (%.0f → %.0f)' % (i, g['x'], g['x'] + g['w']))

                # ── LE GESTE DU FIL NE SE PERD PAS ──
                # ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 20 août, Q75.
                #   Règle encodée : « TENIR et REPORTER sont à l'écran dans le Fil ». Elle
                #   est INTACTE dans son intention — le Fil reste le seul endroit d'où l'on
                #   tient une parole sans ouvrir de fiche — mais **le cadre 76 montre cinq
                #   bandeaux NUS**, et Tom a tranché : la rangée est un AJOUT VALIDÉ, HORS
                #   INVENTAIRE ; le repos est celui du cadre, le geste apparaît AU BESOIN.
                #   Le juge de section mesure L'ÉCRAN AU REPOS : il vérifie donc l'inverse —
                #   aucune rangée au repos — et laisse `redteam_fonctions` vérifier que
                #   l'appui maintenu la fait paraître et qu'elle tient vraiment la parole.
                #   Version d'origine : sauvegardes/releve-S4-avant-q75.py
                if ecran == 'fil':
                    att = pg.evaluate("""()=>[...document.querySelectorAll('#feedList .s4-carte')].length""")
                    n = pg.evaluate("""()=>[...document.querySelectorAll('#feedList .s4-acte,#feedList .s4-actes')]
                      .filter(e=>e.getBoundingClientRect().width>4).length""")
                    if att and n:
                        coll.append(E + ' le Fil AU REPOS porte %d élément(s) de rangée : '
                                        'le cadre 76 n\'en a aucun (Q75)' % n)
                    # et la fonction, elle, est bien là : la composition la publie
                    if att and not pg.evaluate(
                            """()=>((window._filComp||[]).some(f=>f.actes&&f.actes.some(a=>a.quoi==='keep')))"""):
                        coll.append(E + ' AUCUN geste dans le Fil : plus un seul bandeau ne porte TENIR')

                # ── la présence peinte ──
                for msg in pg.evaluate(PEINT, cfg):
                    peint.append(E + ' ' + msg)

        if er:
            peint.append('  ERREURS JS : ' + ' | '.join(er[:3]))
        b.close()

    comp, born = juge_composants(), juge_borne()
    sty.extend(comp); sty.extend(born)
    print('\n═══ SECTION 4 · INDEX ET FIL — %d écrans mesurés ═══' % len(vus))
    print('    les 8 cartes isolées du §5, par la loi du §3.9 bis  : %s'
          % ('8/8' if not comp else '%d/8' % (8 - len(comp))))
    print('    la borne du §2.5 mord où il faut, et nulle part ailleurs : %s\n'
          % ('oui' if not born else 'NON'))
    for nom, lst in (('écarts de position > 3 px', pos), ('écarts de style', sty),
                     ('collisions', coll), ('débordements', hors), ('présence peinte', peint)):
        print('%-28s %d' % (nom, len(lst)))
        if lst and (VERBOSE or len(lst) <= 40):
            for l in lst: print('   ', l)
    total = len(pos) + len(sty) + len(coll) + len(hors) + len(peint)
    print('\n%s' % ('✅  SECTION 4 AU VERT' if total == 0 else '❌  %d ÉCARTS' % total))
    return total


if __name__ == '__main__':
    sys.exit(0 if juge() == 0 else 1)
