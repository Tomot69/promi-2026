#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_nuee.py — LE JUGE DE LA FICHE DE NUÉE (PROMI-SPECIFICATIONS.md, partie II).

Les vingt écrans du §12, un par un, dans les deux thèmes. Mêmes cinq lignes de critère que
les juges de section :

    écarts de position > 3 px · écarts de style · collisions · débordements · PRÉSENCE PEINTE

⚠ LA RÉFÉRENCE N'EST PAS DANS CE FICHIER. Elle est extraite de `PROMI-SPECIFICATIONS.md`
   à chaque passage : si le document bouge, le juge bouge avec lui. On ne recopie pas des
   cotes dans un test — c'est ainsi qu'elles divergent.

⚠ L'ÉTAT « DÉFILÉ » EST EXCLU DU CONTRÔLE DE LA FORMULE. §9 : « l'état défilé n'est pas une
   valeur de la formule : c'est LA BUTÉE HAUTE DU DÉFILEMENT. Un contrôle qui vérifie la
   formule doit donc l'exclure, sinon il le comptera comme une erreur. » Il est contrôlé
   pour ce qu'il est : base 58, et un champ réduit à 114 px.

Usage :  python3 redteam_nuee.py [--verbose]
"""
import re
import sys
import io
from playwright.sync_api import sync_playwright

RACINE = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
APP = "http://127.0.0.1:8752/app.html"
SPEC = RACINE + "/PROMI-SPECIFICATIONS.md"
VERBOSE = '--verbose' in sys.argv
TOL = 3

pos, sty, coll, debord, peint = [], [], [], [], []


# ══════════════════════════════════════════════════════════════════════════════════════
# 1 · LA RÉFÉRENCE — extraite du document, jamais recopiée
# ══════════════════════════════════════════════════════════════════════════════════════
def inventaire():
    S = io.open(SPEC, encoding='utf-8').read()
    bloc = S[S.index('## 12 · Inventaire écran par écran'):S.index('## 13 · Le défilement')]
    ecrans = []
    parts = re.split(r'\n### ', bloc)[1:]
    for p in parts:
        titre = p.split('\n')[0].strip()
        m = re.search(r'Fond `(#\w+)` · \*\*trait : base = (\d+), amplitude = (\d+)\*\* · '
                      r'(\d+) Promi ou Chiche · (\d+) ligne', p)
        if not m:
            continue
        e = {'nom': titre, 'fond': m.group(1), 'base': int(m.group(2)),
             'amp': int(m.group(3)), 'n': int(m.group(4)), 'lignes': int(m.group(5)),
             'clair': 'clair' in titre, 'defile': 'défilement' in titre, 'rangs': []}
        for L in p.split('\n'):
            if not L.startswith('| '):
                continue
            cel = [c.strip() for c in L.strip().strip('|').split('|')]
            if len(cel) < 7 or cel[0] in ('type', '---', ':---'):
                continue
            e['rangs'].append(cel)
        ecrans.append(e)
    return ecrans


def nombre(v):
    try:
        return float(v)
    except Exception:
        return None


def attendus(e):
    """Les nœuds que le document donne, traduits en sélecteurs de l'app.

    On ne prend que les rangs dont l'ancrage est SANS AMBIGUÏTÉ : l'entête, les deux
    Noyaux, l'à-qui, le titre, la méta, les cartes du fil, la barre Peaufiner, la Toile.
    Un rang « · dedans » n'a pas de coordonnée propre — le document le dit (« interne ») —
    il est vérifié par le style de son parent."""
    out = []
    fil = []
    for c in e['rangs']:
        t, x, y, w, h = c[0], nombre(c[1]), nombre(c[2]), nombre(c[3]), nombre(c[4])
        style, contenu = c[5], c[6]
        if t == 'TOILE' and x == 0 and y == 0:
            out.append(('la Toile', '#dpTrameCv', 0, 0, 390, h, None))
        elif t == 'bloc' and x == 24 and y == 38:
            # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 3 septembre 2026.
            #   LA RÈGLE QU'IL ENCODAIT : l'entête du §3.1 posé À NU, mot-marque à 24 / 38,
            #   hauteur 34 — c'est ce que le document donne, rang par rang.
            #   LA DÉCISION QUI LA REMPLACE : LOI 1 — le PLATEAU est l'entête de toute
            #   l'app : 24 / 40 / 342 × 60, contour 2 px, padding 26. Le mot-marque vit
            #   DEDANS : 24 + 2 + 26 = 52 en x, centré dans les 60 px posés à 40 → 56,5 ;
            #   sa hauteur est celle de son texte, 27, et non les 34 de la boîte d'avant.
            #   MESURÉ sur les 24 écrans, deux thèmes, avant d'écrire une ligne.
            #   Ce n'est pas un desserrement : on ajoute LE PLATEAU LUI-MÊME au relevé,
            #   vérifié au pixel — sa boîte, sa largeur, sa hauteur. La version d'origine
            #   ne le regardait pas.
            #   Version d'origine : sauvegardes/redteam_nuee-avant-plateau.py
            out.append(('plateau', '#detailPoster .enh', 24, 40, 342, 60, None))
            out.append(('mot-marque', '#dptNat', 52, 56.5, None, 27, None))
        elif t == 'bloc' and x == 24 and w == 82:
            out.append(('noyau toi', '#dAura .kring.kring-moi', 24, y, 82, None, None))
        elif t == 'bloc' and x == 136 and w == 70:
            out.append(('noyau de la Nuée', '#dAura .kring:not(.kring-moi)', 136, y, 70, None, None))
        elif t == 'bloc texte' and x == 24 and contenu.startswith('Avec'):
            out.append(('à qui', '#dptQui', 24, y, None, None, style))
        elif t == 'bloc texte' and x == 24 and 'Bricolage 700 / 38' in style:
            out.append(('titre', '#dptTitre', 24, y, 342, None, style))
        elif t == 'bloc texte' and x == 24 and 'Apfel 500 / 12.5' in style:
            out.append(('méta', '#dptQuand', 24, y, None, None, style))
        elif t == 'bloc' and x == 24 and w == 342 and h == 74:
            fil.append(y)
        elif t == 'bloc' and x == 0 and y == 760:
            out.append(('barre Peaufiner', '#dpDetails .dpd-tog', 0, 760, 390, 84, None))
    # ⚠ `nth-of-type` compte les BALISES, pas les classes : `_ficheNuee` insère un
    #    `.s1b-fil-trait` dans chaque carte, et le compte se décalait — les lignes
    #    sortaient toutes « ABSENT » sur les vingt écrans. On les prend par leur rang
    #    dans la liste des `.nf-item`, qui est ce que le document numérote.
    for i, y in enumerate(sorted(fil)):
        out.append(('ligne de fil %d' % (i + 1), ('NF', i), 24, y, 342, 74, None))
    return out


# ══════════════════════════════════════════════════════════════════════════════════════
# 2 · LA MISE EN SCÈNE — n Promi dans la Nuée, thème, état
# ══════════════════════════════════════════════════════════════════════════════════════
# ⚠ ON ATTEND QUE LA FICHE SOIT ENTRÉE. Rouvrir un poster déjà ouvert relance son
#    animation d'entrée : mesurée en plein vol, la fiche entière sort décalée de ~400 px
#    vers la droite (« mot-marque x : 24 attendu, 424 mesuré ») et TOUT déborde derrière.
#    On ferme, on laisse la sortie finir, on ouvre, puis on attend que le mot-marque soit
#    revenu à sa place — on ne devine pas un délai, on lit l'écran.
FERME = """()=>{ if(window.closeAll) closeAll(); }"""
ENTREE = """()=>{ const dev=document.getElementById('device').getBoundingClientRect();
  const sc=dev.width/390; const e=document.getElementById('dptNat');
  if(!e) return false; const r=e.getBoundingClientRect();
  return Math.abs((r.left-dev.left)/sc - 24) < 3; }"""

SCENE = """(a)=>{
  const k=Object.keys(NUE)[0];
  promises.forEach(q=>{ if(q.nuee===k) q.nuee=null; });
  const libres=promises.filter(q=>!q.draft&&!q.nuee);
  /* on RE-RATTACHE de vraies promesses — jamais d'id inventé, sinon `dalleTrame` échoue et
     le champ sort vide (piège payé une fois, voir scratchpad/mesure_vide.py). Au-delà du
     stock réel on recycle : le semis ne compte pas les Promi (§10.6). */
  for(let i=0;i<a.n;i++){ const q=libres[i]; if(!q) break; q.nuee=k; }
  window._nueeForce = (a.n>libres.length) ? a.n : null;
  openEssaim(k);
  return {k:k, pose:promises.filter(q=>q.nuee===k&&!q.draft).length};}"""

MESURE = """(sel)=>{
  const dev=document.getElementById('device').getBoundingClientRect();
  const sc=dev.width/390;
  const e=document.querySelector(sel); if(!e) return null;
  const c=getComputedStyle(e);
  if(c.display==='none'||c.visibility==='hidden') return {absent:'masqué'};
  const r=e.getBoundingClientRect();
  return {x:(r.left-dev.left)/sc, y:(r.top-dev.top)/sc, w:r.width/sc, h:r.height/sc,
          ff:(c.fontFamily||'').split(',')[0].replace(/["']/g,''),
          fw:c.fontWeight, fs:parseFloat(c.fontSize),
          fill:c.webkitTextFillColor||c.color, op:parseFloat(c.opacity),
          txt:(e.textContent||'').trim().slice(0,24)};}"""

# la présence peinte : le champ, la matière, le trait — lus dans les pixels du canevas
PEINT = """(a)=>{
  const cv=document.getElementById('dpTrameCv'); if(!cv||!cv.width) return {err:'pas de canevas'};
  const g=cv.getContext('2d'); const larg=parseFloat(cv.style.width)||390; const k=cv.width/larg;
  const lire=(x,y)=>{ if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return null;
    const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
    return d[3]>200?[d[0],d[1],d[2]]:null; };
  const lum=c=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
  const NC=[0x8A,0x5C,0xF0];
  const nu=p=>p&&Math.abs(p[0]-NC[0])+Math.abs(p[1]-NC[1])+Math.abs(p[2]-NC[2])<=12;
  const base=a.base, amp=a.amp, per=1.5, mont=amp*0.34, aa=amp*0.62, W=390;
  const y=x=>{const t=Math.min(1,Math.max(0,x/W));return base-mont*t-aa*Math.sin(2*Math.PI*per*t);};
  /* 1 · le champ existe, et il est mauve */
  let champ=0, matiere=0, vide=0, sansMatiere=0;
  for(let x=8;x<W-8;x+=6){
    const bas=Math.round(y(x))-8;
    let dernier=-1, vu=false;
    for(let yy=2;yy<=bas;yy++){ const p=lire(x,yy); if(!p) continue; vu=true;
      if(!nu(p)) dernier=yy; }
    if(vu) champ++;
    if(dernier<0){ sansMatiere++; continue; }
    matiere++;
    if(bas-dernier>24) vide++;
  }
  /* 2 · le trait : la teinte claire de la Nuée, sur l'onde */
  let trait=0;
  for(let x=20;x<W-20;x+=4){ for(let d=-5;d<=5;d++){ const p=lire(x,y(x)+d); if(!p) continue;
    if(Math.abs(p[0]-0xD0)+Math.abs(p[1]-0xB0)+Math.abs(p[2]-0xFF)<40){ trait++; break; } } }
  return {champ:champ, matiere:matiere, vide:vide, sansMatiere:sansMatiere, trait:trait,
          hautChamp:lire(20,20)};}"""

MESURE_FIL = """(i)=>{
  const dev=document.getElementById('device').getBoundingClientRect();
  const sc=dev.width/390;
  const l=[...document.querySelectorAll('#dpNueeFil .nf-item')];
  const e=l[i]; if(!e) return null;
  const c=getComputedStyle(e);
  if(c.display==='none'||c.visibility==='hidden') return {absent:'masqué'};
  const r=e.getBoundingClientRect();
  return {x:(r.left-dev.left)/sc, y:(r.top-dev.top)/sc, w:r.width/sc, h:r.height/sc,
          ff:'', fw:'', fs:0, fill:'', op:parseFloat(c.opacity), txt:(e.textContent||'').trim().slice(0,20)};}"""

SUP = """()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const h=document.getElementById('detailPoster'); if(!h) return [];
  const vis=e=>{const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return false;
    const r=e.getBoundingClientRect(); return r.width>6&&r.height>6;};
  const f=[...h.querySelectorAll('*')].filter(e=>{ if(!vis(e)) return false;
    if(['CANVAS','IMG','SVG'].includes(e.tagName)) return false;
    const t=(e.textContent||'').trim(); if(!t) return false;
    return [...e.children].every(c=>['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(c.tagName));});
  const box=e=>{const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc,y:(r.top-dev.top)/sc,w:r.width/sc,h:r.height/sc};};
  const out=[];
  for(let i=0;i<f.length;i++) for(let j=i+1;j<f.length;j++){
    const a=f[i],b=f[j]; if(a.contains(b)||b.contains(a)) continue;
    const A=box(a),B=box(b);
    const ix=Math.max(0,Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x));
    const iy=Math.max(0,Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y));
    if(ix<3||iy<3) continue;
    if(ix*iy/Math.min(A.w*A.h,B.w*B.h) < 0.4) continue;
    /* LA BARRE PEAUFINER N'EST PAS UNE SUPERPOSITION. §9 : à partir de quatre éléments, la
       QUATRIÈME LIGNE DÉPASSE SOUS LA BARRE de 26 px — « c'est ce dépassement qui dit qu'il
       y en a d'autres ». Le fil défile sous la barre, c'est le §13. */
    const barre=e=>!!e.closest('#dpDetails');
    if(barre(a)||barre(b)) continue;
    out.push(((a.textContent||'').trim().slice(0,18))+' ⨯ '+((b.textContent||'').trim().slice(0,18)));}
  return [...new Set(out)].slice(0,6);}"""


# ══════════════════════════════════════════════════════════════════════════════════════
# 1 bis · LE PEAUFINER D'UNE NUÉE — cadres 84 à 87, lus DANS LE MOODBOARD
# ══════════════════════════════════════════════════════════════════════════════════════
# Le §12 ne décrit que la fiche. Le Peaufiner d'une Nuée n'existe que dans
# `promi-moodboard-H.html`, cadres 84/85 (page haute) et 86/87 (la suite). On y lit ses
# cotes à l'exécution, exactement comme la loi de la carte d'Index avait été retrouvée dans
# les chemins SVG du moodboard : le document ne donne pas tout, le moodboard si.
MB = "http://127.0.0.1:8752/promi-moodboard-H.html"
PAGE = 760          # la hauteur d'une page de Peaufiner (§2 : le défileur va de 0 à 760)

CADRE = """(n)=>{
  const isF=e=>{const s=e.getAttribute('style')||'';
    return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  const F=[...document.querySelectorAll('div')].filter(isF);
  const f=F[n]; if(!f) return null;
  const fr=f.getBoundingClientRect();
  const out=[];
  [...f.querySelectorAll(':scope > div')].forEach(e=>{
    const r=e.getBoundingClientRect();
    out.push({x:Math.round(r.left-fr.left), y:Math.round(r.top-fr.top),
              w:Math.round(r.width), h:Math.round(r.height),
              t:(e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40)});});
  return out;}"""

# quel bloc du moodboard correspond à quel nœud de l'app — par SON TEXTE, jamais par un rang
# page 1 = cadre 84 (défileur au repos) · page 2 = cadre 86 (défileur descendu de 760)
PF_P1 = [
    # ⚠ le texte de l'entête est la CONCATÉNATION de ses deux spans, sans espace entre
    #    eux : « le potager✕  FERMER ». On s'ancre sur le nom seul.
    ('le potager',             '#npTete'),
    ('DESCRIPTION',            '#npDesc'),
    ('MEMBRES',                '#npMemb'),
    ('PIÈCES JOINTES',         '#npFich'),
    ('COMMENTAIRES',           '#npComm'),
]
PF_P2 = [
    ('Planter un Promi dans',  '#nfAdd'),
    ('DISSOUDRE LA NUÉE',      '#npDiss'),
]
PF_MAP = PF_P1 + PF_P2

OUVRE_PF = """()=>{ const k=Object.keys(NUE)[0];
  promises.forEach(q=>{ if(q.nuee===k) q.nuee=null; });
  promises.filter(q=>!q.draft&&!q.nuee).slice(0,3).forEach(q=>{ q.nuee=k; });
  openEssaim(k); return k; }"""


def reference_peaufiner(b):
    """Les cotes des cadres 84 et 86, lues UNE FOIS, AVANT tout le reste.

    ⚠ ON NE LAISSE PAS L'APP EN ARRIÈRE-PLAN. Ouvrir la planche dans un second onglet
    pendant que l'app est mesurée la fait passer en arrière-plan : le navigateur y bride
    `requestAnimationFrame`, et `_fichePose` — qui repeint sur deux rAF — ne repeint plus.
    Résultat mesuré : les six blocs du Peaufiner à « masqué » sur les quatre écrans, alors
    que la même séquence sur un seul onglet les rend tous à leur cote. On lit donc la
    planche d'abord, on ferme son onglet, et on ne mesure qu'ensuite."""
    pgmb = b.new_page(viewport={'width': 1400, 'height': 1000})
    pgmb.goto(MB)
    pgmb.wait_for_timeout(4500)
    ref = {}
    for n in (84, 86):
        for bl in (pgmb.evaluate(CADRE, n) or []):
            for mot, sel in PF_MAP:
                if bl['t'].startswith(mot):
                    ref[sel] = bl
    pgmb.close()
    # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7 de CLAUDE.md) — 2 septembre 2026.
    #    LA RÈGLE QU'IL ENCODAIT : « les cartes du Peaufiner d'une Nuée sont aux cotes des
    #    cadres 84 et 86 ». LA DÉCISION QUI LA COMPLÈTE : Tom, 2 septembre — « le pinceau
    #    se reprend depuis Peaufiner, HAUT DE LISTE, sur une fiche comme sur une Nuée ».
    #    Une rangée « LE TRAIT » de 118 vient donc en tête de la page 1, et les quatre
    #    cartes qui la suivent descendent d'autant, écart de 16 compris : 118 + 16 = 134.
    #    `npDiss` et `nfAdd` vivent sur la page 2 et ne bougent pas.
    #    Ce n'est pas un desserrement : le contrôle vérifie EXACTEMENT la même chose, à la
    #    cote près, et il attrapera tout écart d'un pixel comme avant.
    #    Version d'origine : sauvegardes/redteam_nuee-avant-pinceau.py
    for sel in ('#npDesc', '#npMemb', '#npFich', '#npComm'):
        if sel in ref:
            ref[sel] = dict(ref[sel], y=ref[sel]['y'] + 134)
    # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 13 septembre 2026. Tom : « donne-lui [à la Nuée] son bloc du
    #    Cercle, avec la rangée LA COULEUR ». Le bloc (384) se pose en page 2 sous « Planter » (46 + 68 + 16 = 130), et DISSOUDRE
    #    passe dessous à l'écart de la fiche entre le bloc et SUPPRIMER (104) : 130 + 384 + 104 = 618, soit +494 sur le cadre 86.
    #    EN DUR, comme le +134 du trait. Même sévérité, au pixel. Version d'origine : sauvegardes/redteam_nuee-avant-nuee-cercle.py
    if '#npDiss' in ref:
        ref['#npDiss'] = dict(ref['#npDiss'], y=ref['#npDiss']['y'] + 494)
    return ref


def peaufiner(pg, ref):
    """Les quatre écrans du Peaufiner d'une Nuée."""
    manquants = [s for _, s in PF_MAP if s not in ref]
    if manquants:
        peint.append(('Peaufiner de Nuée', 'MOODBOARD', 'cadres 84/86 : %s introuvable(s)'
                      % ', '.join(manquants)))
        return 0
    vus = 0
    for clair in (False, True):
        nom = 'Peaufiner de Nuée — thème %s' % ('clair' if clair else 'sombre')
        pg.evaluate("(t)=>setTheme(t)", 'light' if clair else 'dark')
        pg.wait_for_timeout(400)
        pg.evaluate(FERME); pg.wait_for_timeout(500)
        pg.evaluate(OUVRE_PF)
        for _ in range(30):
            pg.wait_for_timeout(200)
            if pg.evaluate(ENTREE):
                break
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t) t.click();}")
        # ⚠ ON ATTEND QUE LE PANNEAU SOIT BÂTI, on ne devine pas un délai. Le clic pose la
        #    classe, et c'est la passe de rendu suivante qui construit et cote les cartes.
        for _ in range(20):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>{const c=document.getElementById('npDesc');"
                           "return !!(c && getComputedStyle(c).display!=='none');}"):
                break
        pg.wait_for_timeout(300)
        if not pg.evaluate("()=>{const d=document.getElementById('dpDetails');"
                           "return !!(d&&d.classList.contains('ouvert'));}"):
            peint.append((nom, 'LA BARRE', "toucher la barre n'ouvre pas le panneau (§13)"))
            continue
        # ⚠ DEUX PAGES, ET ON DESCEND DE L'UNE À L'AUTRE (décision Tom, Q65).
        #    Le défileur fait 760 de haut pour 1520 de contenu : au repos c'est le cadre 84,
        #    descendu de 760 c'est le cadre 86, à leurs cotes ABSOLUES de planche. La barre
        #    reste clouée à 760 dans les deux — rien ne monte, rien ne recouvre.
        for page, lot in ((0, PF_P1), (PAGE, PF_P2)):
            pg.evaluate("(y)=>{const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=y;}", page)
            pg.wait_for_timeout(600)
            nomP = nom + (' · page 1' if page == 0 else ' · page 2')
            vus += 1
            for _, sel in lot:
                m = pg.evaluate(MESURE, sel)
                r = ref[sel]
                if m is None or m.get('absent'):
                    peint.append((nomP, sel, m.get('absent') if m else 'ABSENT'))
                    continue
                for cle, att, mes in (('x', r['x'], m['x']), ('y', r['y'], m['y']),
                                      ('largeur', r['w'], m['w']), ('hauteur', r['h'], m['h'])):
                    if abs(mes - att) > TOL:
                        pos.append((nomP, sel + ' ' + cle, att, round(mes, 1)))
            # la barre ne bouge pas d'une page à l'autre (§6) et ne recouvre rien
            mb = pg.evaluate(MESURE, '#dpDetails .dpd-tog')
            if not mb or mb.get('absent'):
                peint.append((nomP, 'la barre Peaufiner', 'absente'))
            elif abs(mb['y'] - 760) > TOL:
                pos.append((nomP, 'barre Peaufiner y', 760, round(mb['y'], 1)))
        # on revient en haut : le cadre 84 ne porte NI Toile, NI Noyaux, NI fil
        pg.evaluate("()=>{const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=0;}")
        pg.wait_for_timeout(400)
        for id_ in ('dpTrameCv', 'dAura', 'dptQui', 'dpNueeFil'):
            m = pg.evaluate(MESURE, '#' + id_)
            if m and not m.get('absent'):
                coll.append((nom, "%s reste visible — le cadre 84 n'en porte pas" % id_))
    # et le bouton revient à son nid quand on replie
    pg.evaluate("()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t) t.click();}")
    pg.wait_for_timeout(900)
    m = pg.evaluate(MESURE, '#nfAdd')
    if not m or m.get('absent') or m['y'] < 300:
        peint.append(('Peaufiner replié', '#nfAdd',
                      'le bouton ne revient pas dans le fil (y=%s)' % (m or {}).get('y')))
    return vus


def main():
    ecrans = inventaire()
    print('══ %d écrans lus dans le §12 ══\n' % len(ecrans))
    vus = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        refPF = reference_peaufiner(b)          # la planche d'abord, l'app ensuite
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for e in ecrans:
            # ⚑ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7) — 13 septembre 2026, Q213.
            #   LA RÈGLE ENCODÉE : le §12 et la planche `promi-nuee-toile` comptent n = Promi ET Chiche de la Nuée —
            #   Nuée vide à 460, un Promi à 374, deux à 288…
            #   LA DÉCISION : Tom — « Planter dans la Nuée » est la dernière ligne du fil ; « le trait remonte en
            #   conséquence, et tout ce qui est entre les deux remonte avec lui. Tu ne touches pas à la règle de hauteur
            #   du trait — c'est le contenu qui s'organise sous elle ». La règle `max(176, 460 − 86 n)` est intacte ;
            #   n compte les LIGNES DU FIL, l'entrée comprise : n + 1. Tout ce qui est sous le trait (Noyaux, à-qui,
            #   titre, méta, cartes du fil, hauteur de la Toile) se décale de la même quantité ; le plateau, le mot-marque
            #   et la barre Peaufiner ne bougent pas. La butée du défilement (58/16) n'est pas une valeur de la formule.
            #   Tolérance inchangée. Version d'origine : sauvegardes/redteam_nuee-avant-nuee-entree.py
            DELTA = 0
            if not e['defile']:
                _nb = max(176, 460 - 86 * (e['n'] + 1))
                DELTA = _nb - e['base']
                e = dict(e, base=_nb)
            pg.evaluate("(t)=>setTheme(t)", 'light' if e['clair'] else 'dark')
            pg.wait_for_timeout(400)
            pg.evaluate(FERME); pg.wait_for_timeout(500)
            r = pg.evaluate(SCENE, {'n': e['n']})
            for _ in range(30):
                pg.wait_for_timeout(200)
                if pg.evaluate(ENTREE):
                    break
            pg.wait_for_timeout(700)
            if e['defile']:
                pg.evaluate("()=>{ if(window._nueeDefile) window._nueeDefile(true); }")
                pg.wait_for_timeout(900)
            vus += 1
            nom = e['nom']
            reel = pg.evaluate("()=>{const s=window._nueeSemis; return s?{base:s.base,amp:s.amp,n:s.n}:null;}")

            # ── la formule du §9, SAUF sur l'état défilé (butée du défilement) ──
            if not e['defile']:
                if not reel:
                    peint.append((nom, 'SEMIS', 'window._nueeSemis absent'))
                else:
                    if abs(reel['base'] - e['base']) > TOL:
                        pos.append((nom, 'base du trait', e['base'], reel['base']))
                    if abs(reel['amp'] - e['amp']) > TOL:
                        pos.append((nom, 'amplitude', e['amp'], reel['amp']))

            # ── les cotes de l'inventaire ──
            for (enom, sel, ex, ey, ew, eh, style) in attendus(e):
                if DELTA and enom not in ('plateau', 'mot-marque', 'barre Peaufiner'):
                    if enom == 'la Toile':
                        eh = (eh + DELTA) if eh is not None else eh
                    elif ey is not None:
                        ey = ey + DELTA
                if isinstance(sel, tuple):
                    m = pg.evaluate(MESURE_FIL, sel[1])
                else:
                    m = pg.evaluate(MESURE, sel)
                if m is None or m.get('absent'):
                    peint.append((nom, enom, m.get('absent') if m else 'ABSENT'))
                    continue
                if ex is not None and abs(m['x'] - ex) > TOL:
                    pos.append((nom, enom + ' x', ex, round(m['x'], 1)))
                if ey is not None and abs(m['y'] - ey) > TOL:
                    pos.append((nom, enom + ' y', ey, round(m['y'], 1)))
                if ew is not None and abs(m['w'] - ew) > TOL:
                    pos.append((nom, enom + ' largeur', ew, round(m['w'], 1)))
                if eh is not None and abs(m['h'] - eh) > TOL:
                    pos.append((nom, enom + ' hauteur', eh, round(m['h'], 1)))
                if style:
                    mf = re.search(r'(Bricolage|Apfel|Fraunces)\s+(\d+)\s*/\s*([\d.]+)', style)
                    if mf:
                        if mf.group(1).lower() not in (m['ff'] or '').lower():
                            sty.append((nom, enom, 'police', mf.group(1), m['ff']))
                        if abs(float(m['fs']) - float(mf.group(3))) > 1:
                            sty.append((nom, enom, 'taille', mf.group(3), m['fs']))
                if m['op'] < 0.72:
                    sty.append((nom, enom, 'opacité', '≥ .72', m['op']))

            # ── la présence peinte ──
            p = pg.evaluate(PEINT, {'base': e['base'] if not e['defile'] else reel['base'],
                                    'amp': e['amp'] if not e['defile'] else reel['amp']})
            if p.get('err'):
                peint.append((nom, 'CHAMP', p['err']))
            else:
                if p['champ'] == 0:
                    peint.append((nom, 'CHAMP', 'aucun aplat peint'))
                if p['sansMatiere'] > 2:
                    peint.append((nom, 'TOILE', '%d abscisses sans matière' % p['sansMatiere']))
                if p['vide'] > p['matiere'] / 2 and p['matiere']:
                    peint.append((nom, 'TOILE', 'bandeau nu au-dessus du trait (%d/%d)'
                                  % (p['vide'], p['matiere'])))
                if p['trait'] == 0:
                    peint.append((nom, 'TRAIT', 'aucune ligne peinte sur l\'onde'))

            # ── collisions et débordements ──
            for s in pg.evaluate(SUP):
                coll.append((nom, s))
            for d in pg.evaluate("""()=>{const dev=document.getElementById('device').getBoundingClientRect();
              const sc=dev.width/390; const out=[];
              document.querySelectorAll('#detailPoster *').forEach(e=>{const c=getComputedStyle(e);
                if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05)return;
                const r=e.getBoundingClientRect(); if(r.width<6||r.height<6)return;
                const x=(r.left-dev.left)/sc, w=r.width/sc;
                if(x<-3||x+w>393) out.push((e.id?'#'+e.id:'.'+(e.className+'').split(' ')[0])
                  +' déborde de '+Math.round(Math.max(-x, x+w-390))+' px');});
              return [...new Set(out)].slice(0,4);}"""):
                debord.append((nom, d))
            if VERBOSE:
                print('  %-40s base %s  n %s' % (nom, (reel or {}).get('base'), (reel or {}).get('n')))
        # ── les quatre écrans du Peaufiner d'une Nuée (cadres 84 à 87) ──
        vus += peaufiner(pg, refPF)
        b.close()

    print('=' * 78)
    print('  LA FICHE DE NUÉE — les cinq lignes du critère, sur %d écrans' % vus)
    print('=' * 78)
    for titre, lst in (('écarts de position > 3 px', pos), ('écarts de style', sty),
                       ('ÉLÉMENTS DÉCLARÉS MAIS PAS PEINTS', peint),
                       ('collisions de blocs', coll), ('débordements', debord)):
        print('  %-36s %d' % (titre + ' ' + '.' * (34 - len(titre)), len(lst)))
        for x in lst[:8]:
            print('       ' + ' · '.join(str(v) for v in x))
    total = len(pos) + len(sty) + len(peint) + len(coll) + len(debord)
    print('=' * 78)
    print('\n  %s  %d écran(s) · %d écart(s)' % ('✅' if total == 0 else '❌', vus, total))
    sys.exit(0 if total == 0 else 1)


main()
