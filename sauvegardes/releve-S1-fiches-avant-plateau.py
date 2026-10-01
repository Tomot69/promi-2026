#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-S1-fiches.py — LE JUGE DE LA SECTION 1 (les fiches).

Compare l'app aux coordonnées absolues de PROMI-SPECIFICATIONS.md §5, écran par écran,
dans les deux thèmes. Ne mesure rien « à l'œil » : chaque cote attendue est celle du
document. Les cinq lignes du critère d'arrêt (AUTONOMIE-CLAUDE-CODE.md §2) :

    écarts de position > 3 px .................. 0
    écarts de style (police, taille, couleur) .. 0
    collisions de blocs ........................ 0
    éléments au-delà de y = 844 ................ 0
    batteries redteam .......................... au vert  (hors de ce script)

Usage :  python3 releve-S1-fiches.py [--verbose]
"""
import sys, math
from playwright.sync_api import sync_playwright

APP = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/app.html"
VERBOSE = '--verbose' in sys.argv
TOL = 3          # px — la tolérance du protocole

# ── les cotes attendues, LUES dans l'inventaire §5 ────────────────────────────────────
# clef : (écran, thème) ; valeur : liste (nom, sélecteur, x, y, w, h, style attendu)
# w/h à None = non contraint. Le style : (famille, graisse, taille, couleur)
CREME, ENCRE = '#F4EEE1', '#16171B'
TERRA, MENTHE = '#F07A2E', '#2BE88C'
BLEU, FRAMB, MAUVE = '#3A54FF', '#FA2258', '#8A5CF0'
CLAIRP, CLAIRC, CLAIRN = '#CBAAFF', '#FFC0A8', '#D0B0FF'


def fiche(nat, etat_col_dark, etat_col_light, base, amp, yn, ytrace, yqui, ytitre,
          quifs=23, titrefs=None, deuxieme=True, yetat=None, trait_dark=None, trait_light=None):
    """Le gabarit commun d'une fiche : ce que TOUS les inventaires §5 partagent."""
    boite = base + amp + 40
    natcol = {'promi': BLEU, 'chiche': FRAMB, 'nuee': MAUVE}[nat]
    trait_dark = trait_dark or etat_col_dark
    trait_light = trait_light or etat_col_dark   # le trait garde la teinte claire (§2.1 bis)
    out = []
    out.append(('mot-marque', '#dpTete .dpt-nat', 24, 38, None, 34,
                ('Fraunces', 600, 27, CREME)))
    out.append(('fermer', '#detailPoster .closeb', None, 38, None, 34, None))
    if yn is not None:
        out.append(('noyau toi', '#dAura .kring.kring-moi', 24, yn, 82, None, None))
        out.append(('anneau toi', '#dAura .kring.kring-moi .kr-wrap', None, yn, 78, 78, None))
        if deuxieme:
            out.append(('noyau personne', '#dAura .kring:not(.kring-moi)', 136, yn + 10, 70, None, None))
            out.append(('anneau personne', '#dAura .kring:not(.kring-moi) .kr-wrap', None, yn + 10, 58, 58, None))
            out.append(('visage personne', '#dAura .kring:not(.kring-moi) .s1b-visage', None, None, 36, 36, None))
        out.append(('visage toi', '#dAura .kring.kring-moi .s1b-visage', None, None, 48, 48, None))
    if ytrace is not None:
        out.append(('trace', '#dptTrace', 24, ytrace, 342, None,
                    ('Bricolage', 700, 17, None)))
    out.append(('à qui', '#dptQui', 24, yqui, None, None, ('Bricolage', 600, quifs, None)))
    # ⚠ LE TITRE : « un cran, sauf si la ligne casse ». La décision dit 42 ; la règle dit
    #   aussi « ça doit rester respirant », donc un titre qui passerait à deux lignes
    #   redescend d'un point à la fois, plancher 38 (la valeur d'avant le cran). Le juge
    #   vérifie donc la RÈGLE, pas un nombre : taille dans [38, 42] ET une seule ligne.
    #   Un titre à 30, ou un titre sur deux lignes, échoue toujours.
    out.append(('titre', '#dptTitre', 24, ytitre, 342, None, ('Bricolage', 700, None, None)))
    out.append(('état', '#dptQuand', 24, yetat, None, None, ('Apfel', 500, 13.5, None)))
    out.append(('barre Peaufiner', '#dpDetails .dpd-tog', 0, 760, 390, 84, None))
    out.append(('mot Peaufiner', '#dpDetails .dpd-mot', None, None, None, None,
                ('Bricolage', 700, 21, CREME)))
    out.append(('cercle Partager', '#dpDetails .dpd-part', None, None, 46, 46, None))
    dh = min(300, (base - amp) - 88 - 12)
    dw = min(320, int(1.2 * dh))
    return {'nat': nat, 'natcol': natcol, 'base': base, 'amp': amp, 'boite': boite,
            'elements': out, 'etat': (etat_col_dark, etat_col_light),
            'dalle': ((390 - dw) // 2, 88, dw, dh), 'trait': (trait_dark, trait_light)}


# Les écrans de la section 1 que l'app sait produire aujourd'hui.
# ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — TOM, 29 AOÛT 2026.
#   Trois corrections de dessin, valables pour TOUTES les fiches et toutes les natures :
#     1 · « trace pour tenir » remonte ENTRE LE TRAIT ET LES DISQUES, centré. Il était
#         124 px SOUS les Noyaux ; « sous les disques il n'a plus de sens — le geste
#         appartient au trait ».
#     2 · Les textes centraux montent D'UN CRAN : à-qui 21 → 23 (19 → 21 sur un Chiche
#         relevé), titre 38 → 42, état 12,5 → 13,5. « Un cran, pas plus. »
#     3 · Sans mot du geste (une fiche tenue), le bloc REMONTE de 24 px : l'air entre le
#         bas de la vague et les disques passe de ~60 à ~35. « Resserre un peu, garde
#         de l'air. »
#   Les cotes ne sont donc plus recopiées une par une : elles se DÉDUISENT de la règle,
#   à partir de la boîte de chaque écran (base + amp + 40), qui n'a pas bougé. Un chiffre
#   faux se verrait ici comme ailleurs — mais on n'a plus deux endroits à tenir d'accord.
#   L'original figé est en sauvegardes/releve-S1-fiches-avant-29aout.py

def cotes29(base, amp, avec_trace, quifs=23):
    """Les quatre cotes d'une fiche, telles que les décisions du 29 août les posent."""
    boite = base + amp + 40
    if avec_trace:
        ytrace = boite + 4          # juste sous le trait
        yn     = ytrace + 44        # 19 px de texte + 25 d'air
    else:
        ytrace = None
        yn     = boite - 24         # on resserre, on garde de l'air
    yqui   = yn + 124
    # ⚠ L'AIR NE SE FIGE PAS, IL SE CALCULE (décision Tom du 29 août, au soir).
    #   Le 30 du §5 n'est pas un espace : c'est « hauteur du bloc à-qui + air ». À 21 px,
    #   Bricolage 600 rend 23,1, donc l'air vaut 6,9. Monter l'à-qui à 23 sans toucher au 30
    #   mangeait 2,2 px — mesuré sur les cinq états, deux thèmes. La cote suit la taille ;
    #   à 21 la formule redonne 30 au dixième, le moodboard ne bouge pas.
    ytitre = round(yqui + quifs * 1.10 + 6.9, 1)
    return yn, ytrace, yqui, ytitre


def _f(nat, cd, cl, base, amp, avec_trace, **kw):
    yn, ytr, yq, yt = cotes29(base, amp, avec_trace, kw.get('quifs', 23))
    return fiche(nat, cd, cl, base, amp, yn, ytr, yq, yt, **kw)


ECRANS = {
    'promi_atenir':  _f('promi',  TERRA,  TERRA,  262, 44, True),
    'promi_encours': _f('promi',  CLAIRP, BLEU,   262, 44, True,  deuxieme=False),
    'promi_tenue':   _f('promi',  MENTHE, MENTHE, 376, 48, False, deuxieme=False),
    'chiche_lance':  _f('chiche', CLAIRC, FRAMB,  262, 44, True),
    'chiche_releve': _f('chiche', TERRA,  TERRA,  262, 44, True,  quifs=21),
    'chiche_duo':    _f('chiche', MENTHE, MENTHE, 372, 44, False),
}

# Comment amener l'app dans chaque état (aucune invention : on manipule les données).
MISE_EN_SCENE = r"""(nom)=>{
  function trouve(pred){ for(var id=1;id<=220;id++){ try{ var p=promises.filter(function(q){return q.id===id;})[0];
      if(p&&!p.draft&&pred(p)) return id; }catch(e){} } return null; }
  var id=null, p=null;
  function net(q){ delete q.chiche; delete q.avec; }
  if(nom==='promi_atenir'){ id=trouve(function(q){return q.status==='rate'&&!q.nuee&&q.who&&q.who!=='moi';}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; net(p);} }
  if(nom==='promi_encours'){ id=trouve(function(q){return q.status==='encours'&&!q.nuee;}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; net(p); p.who='moi';} }
  if(nom==='promi_tenue'){ id=trouve(function(q){return q.status==='tenu'&&!q.nuee;}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; net(p); p.who='moi'; p.note=''; p.comments=[];} }
  if(nom==='chiche_lance'){ id=trouve(function(q){return q.status==='encours'&&!q.nuee;}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; net(p); p.chiche=true; p.who='Marion';} }
  if(nom==='chiche_releve'){ id=trouve(function(q){return q.status==='rate'&&!q.nuee;}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; p.chiche=true; p.who='Marion'; p.avec='Rachel';} }
  if(nom==='chiche_duo'){ id=trouve(function(q){return q.status==='tenu'&&!q.nuee;}); if(id){p=promises.filter(function(q){return q.id===id;})[0]; p.chiche=true; p.who='Marion'; p.avec='Rachel'; p.note=''; p.comments=[];} }
  if(!id) return null;
  openDetail(id); return id;
}"""

MESURE = r"""(sels)=>{
  const dev=document.querySelector('#device'); const fb=dev.getBoundingClientRect();
  const sc=fb.width/390;
  const dp=document.getElementById('detailPoster');
  const out={};
  for(const [nom,sel] of sels){
    let e=null;
    try{ e = sel.startsWith('#detailPoster') ? document.querySelector(sel) : dp.querySelector(sel); }catch(err){}
    if(!e){ out[nom]=null; continue; }
    const b=e.getBoundingClientRect(); const cs=getComputedStyle(e);
    if(cs.display==='none'||b.width<0.5){ out[nom]=null; continue; }
    out[nom]={x:(b.left-fb.left)/sc, y:(b.top-fb.top)/sc, w:b.width/sc, h:b.height/sc,
      ff:(cs.fontFamily||'').split(',')[0].replace(/['"]/g,''), fw:cs.fontWeight,
      fs:parseFloat(cs.fontSize),   /* la taille de police n'est PAS mise à l'échelle par le transform du cadre */ col:cs.color, fill:cs.webkitTextFillColor||cs.color,
      ls:cs.letterSpacing};
  }
  /* collisions + débordements : sur les blocs POSÉS de la fiche seulement */
  const zone=[...dp.querySelectorAll('#dptTrace,#dptQui,#dptTitre,#dptQuand,#dAura,#dpMsg,#dpDetails .dpd-tog,#dpTete .dpt-nat,.geste-env')]
    .filter(e=>{const cs=getComputedStyle(e); const b=e.getBoundingClientRect();
                return cs.display!=='none'&&cs.visibility!=='hidden'&&b.width>1&&b.height>1;})
    .map(e=>{const b=e.getBoundingClientRect();
      return {n:(e.id||e.className||e.tagName)+'', x:(b.left-fb.left)/sc, y:(b.top-fb.top)/sc,
              w:b.width/sc, h:b.height/sc};});
  const coll=[];
  for(let i=0;i<zone.length;i++) for(let j=i+1;j<zone.length;j++){
    const a=zone[i],c=zone[j];
    const ox=Math.min(a.x+a.w,c.x+c.w)-Math.max(a.x,c.x);
    const oy=Math.min(a.y+a.h,c.y+c.h)-Math.max(a.y,c.y);
    if(ox>2&&oy>2) coll.push([a.n,c.n,Math.round(ox),Math.round(oy)]);
  }
  const deb=zone.filter(z=>z.y+z.h>845.5).map(z=>[z.n,Math.round(z.y+z.h)]);
  /* ── PRÉSENCE PEINTE ────────────────────────────────────────────────────────────────
     Un élément à la bonne coordonnée mais invisible doit faire ÉCHOUER. On ne mesure plus
     la boîte : on regarde l'encre réellement posée.
     · pour un nœud de texte : il a du texte, il n'est ni transparent ni de la couleur de
       son fond ;
     · pour un canevas : combien de pixels opaques, et sur quelle étendue le dessin porte
       réellement (c'est ce contrôle qui manquait — l'anneau remplissait sa boîte à 80 %).  */
  function encre(e){ const cs=getComputedStyle(e);
    const c=(cs.webkitTextFillColor||cs.color||'').match(/[\d.]+/g)||[];
    const a=c.length>3?parseFloat(c[3]):1;
    return {txt:(e.innerText||'').trim().length, alpha:a*parseFloat(cs.opacity||'1')}; }
  function dessin(cv){ try{ const g=cv.getContext('2d');
      const d=g.getImageData(0,0,cv.width,cv.height).data;
      let n=0,x0=1e9,x1=-1,y0=1e9,y1=-1;
      for(let y=0;y<cv.height;y++) for(let x=0;x<cv.width;x++){ const i=(y*cv.width+x)*4;
        if(d[i+3]>24){ n++; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
      if(n===0) return {n:0,w:0,h:0};
      const r=cv.getBoundingClientRect(), k=r.width/cv.width;
      return {n, w:+((x1-x0+1)*k/sc).toFixed(1), h:+((y1-y0+1)*(r.height/cv.height)/sc).toFixed(1)};
    }catch(e){ return null; } }
  const peint={};
  for(const [nom,sel] of sels){
    let e=null; try{ e = sel.startsWith('#detailPoster') ? document.querySelector(sel) : dp.querySelector(sel); }catch(_){}
    if(!e) continue;
    peint[nom] = (e.tagName==='CANVAS') ? dessin(e)
               : (e.querySelector && e.querySelector('canvas')) ? dessin(e.querySelector('canvas'))
               : (e.querySelector && e.querySelector('svg')) ? {svg:1, n:1}
               : encre(e);
  }
  return {out, coll, deb, peint, cls:dp.className};
}"""



# ── LA DALLE ET LE TRAIT sont peints dans le canevas du champ : le DOM n'en sait rien.
#    On lit donc les pixels, à l'emplacement que l'inventaire leur donne.
ENCRE_CHAMP = r"""(a)=>{
  const [dx,dy,dw,dh,base,amp,fond] = a;
  const cv=document.getElementById('dpTrameCv'); if(!cv) return {err:'pas de canevas'};
  const g=cv.getContext('2d'); const k=cv.width/390;
  function bloc(x,y,w,h){
    const d=g.getImageData(Math.round(x*k),Math.round(y*k),Math.max(1,Math.round(w*k)),Math.max(1,Math.round(h*k))).data;
    const t={}; let n=0;
    for(let i=0;i<d.length;i+=4*7){ if(d[i+3]<200) continue; n++;
      const c=d[i]+','+d[i+1]+','+d[i+2]; t[c]=(t[c]||0)+1; }
    const top=Object.entries(t).sort((x,y)=>y[1]-x[1]);
    return {n, dom:top[0]?top[0][0]:null, part:top[0]?top[0][1]/Math.max(1,n):0};
  }
  const dalle = bloc(dx,dy,dw,dh);
  // le trait : une bande de 24 px centrée sur l'onde, à trois abscisses
  const per=1.5, mont=amp*0.34, aa=amp*0.62;
  const y=(x)=>base - mont*Math.max(0,Math.min(1,x/390)) - aa*Math.sin(2*Math.PI*per*Math.max(0,Math.min(1,x/390)));
  const ligne = [40,120,300].map(x=>bloc(x-6, y(x)-12, 12, 24));
  return {dalle, ligne, fond};
}"""

def hexrgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgbof(s):
    m = [int(float(x)) for x in __import__('re').findall(r'[\d.]+', s or '')][:3]
    return tuple(m) if len(m) == 3 else None


def main():
    ecarts, styles, colls, debs, absents = [], [], [], [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.goto('file://' + APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        try:
            pg.evaluate("()=>document.fonts.ready")
        except Exception:
            pass
        for theme in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", theme)
            pg.wait_for_timeout(400)
            for nom, spec in ECRANS.items():
                got = pg.evaluate(MISE_EN_SCENE, nom)
                if not got:
                    print("  ⚠ %-16s %-5s : aucun Promi de cet état dans le jeu de données" % (nom, theme))
                    continue
                pg.wait_for_timeout(900)
                sels = [(e[0], e[1]) for e in spec['elements']]
                r = pg.evaluate(MESURE, sels)
                etat = spec['etat'][0 if theme == 'dark' else 1]
                encre = ENCRE if theme == 'light' else CREME
                for (enom, sel, ex, ey, ew, eh, est) in spec['elements']:
                    m = r['out'].get(enom)
                    if m is None:
                        ecarts.append((theme, nom, enom, 'ABSENT', '', ''))
                        continue
                    for lbl, att, val in (('x', ex, m['x']), ('y', ey, m['y']),
                                          ('w', ew, m['w']), ('h', eh, m['h'])):
                        if att is None:
                            continue
                        if abs(val - att) > TOL:
                            ecarts.append((theme, nom, enom, lbl, att, round(val, 1)))
                    if est:
                        fam, fw, fs, col = est
                        if fam and fam.lower() not in m['ff'].lower():
                            styles.append((theme, nom, enom, 'police', fam, m['ff']))
                        if fw and abs(int(m['fw']) - fw) > 0:
                            styles.append((theme, nom, enom, 'graisse', fw, m['fw']))
                        if fs and abs(m['fs'] - fs) > 0.6:
                            styles.append((theme, nom, enom, 'taille', fs, round(m['fs'], 1)))
                        # ⚠ LE TITRE N'A PAS UNE TAILLE, IL A UNE RÈGLE (décision Tom,
                        #   29 août) : 42, sauf si la ligne casse — alors on redescend d'un
                        #   point à la fois, plancher 38. On vérifie donc la règle : taille
                        #   dans [38, 42] ET une seule ligne. Un titre à 30, ou sur deux
                        #   lignes, échoue.
                        if enom == 'titre' and fs is None:
                            t = round(m['fs'], 1)
                            if not (37.4 <= t <= 42.6):
                                styles.append((theme, nom, enom, 'taille',
                                               'entre 38 et 42', t))
                            elif m.get('h') and m['h'] > t * 1.35:
                                styles.append((theme, nom, enom, 'lignes', 1,
                                               round(m['h'] / (t * 1.02), 1)))
                        cible = col
                        if cible is None:
                            cible = etat if enom in ('trace', 'à qui', 'état') else encre
                        g = rgbof(m['fill'])
                        w_ = hexrgb(cible)
                        # ⚠ CONTRÔLE RÉÉCRIT LE 19 AOÛT 2026 — LE MOT-MARQUE A DEUX ENCRES.
                        # Le §10.6 le pose déjà : « la Toile vide étant crème dans les deux
                        # thèmes, le mot “Nuée” et “✕ FERMER” passent à l'encre #16171B —
                        # sinon c'est blanc sur blanc ; dès qu'un Promi est planté, le champ
                        # redevient mauve et ils repassent en crème ». Depuis que LA MATIÈRE
                        # REMPLIT LE CHAMP (décision Tom du 19 août), n'importe quel monde
                        # clair peut passer sous le mot-marque : la règle n'est plus « il est
                        # crème », c'est « il est LISIBLE, de l'une des DEUX encres du
                        # produit ». Le contrôle de présence peinte, lui, mesure toujours son
                        # écart de 42 au fond réellement peint : rien n'est desserré.
                        if enom == 'mot-marque':
                            if g and min(max(abs(g[k] - hexrgb(c)[k]) for k in range(3))
                                         for c in (CREME, ENCRE)) > 10:
                                styles.append((theme, nom, enom, 'couleur',
                                               '%s ou %s' % (CREME, ENCRE), m['fill']))
                        elif g and max(abs(g[k] - w_[k]) for k in range(3)) > 10:
                            styles.append((theme, nom, enom, 'couleur', cible, m['fill']))
                # ── LE CONTRÔLE DE PRÉSENCE PEINTE ────────────────────────────────────
                # Un élément à la bonne coordonnée mais invisible fait ÉCHOUER. On regarde
                # l'encre réellement posée, pas la boîte.
                for (enom, sel, ex, ey, ew, eh, est) in spec['elements']:
                    p = r['peint'].get(enom)
                    if p is None:
                        absents.append((theme, nom, enom, 'aucun nœud'))
                        continue
                    if 'txt' in p:                       # un bloc de texte
                        if p['txt'] == 0:
                            absents.append((theme, nom, enom, 'texte vide'))
                        elif p['alpha'] < 0.72:          # §6 : aucune opacité sous 72 %
                            absents.append((theme, nom, enom, 'opacité %.2f' % p['alpha']))
                    elif 'n' in p and not p.get('svg'):  # un canevas
                        if p['n'] == 0:
                            absents.append((theme, nom, enom, 'canevas vide'))
                        else:
                            # l'anneau doit REMPLIR sa boîte : c'est le contrôle qui manquait.
                            att = {'anneau toi': 78, 'anneau personne': 58}.get(enom)
                            if att and abs(p['w'] - att) > TOL:
                                absents.append((theme, nom, enom,
                                                'dessin %.0f px pour %d attendus' % (p['w'], att)))

                # ── LA DALLE ET LE TRAIT, lus dans les pixels du champ ────────────────
                dx, dy, dw, dh = spec['dalle']
                ch = pg.evaluate(ENCRE_CHAMP, [dx, dy, dw, dh, spec['base'], spec['amp'],
                                               spec['natcol']])
                if ch.get('err'):
                    absents.append((theme, nom, 'DALLE', ch['err']))
                else:
                    d = ch['dalle']
                    fond = hexrgb(spec['natcol'])
                    dom = rgbof(d['dom']) if d['dom'] else None
                    # la dalle doit couvrir son rectangle d'autre chose que l'aplat de nature
                    if d['n'] == 0:
                        absents.append((theme, nom, 'DALLE', 'rien de peint'))
                    elif dom and max(abs(dom[k] - fond[k]) for k in range(3)) <= 10 and d['part'] > 0.90:
                        absents.append((theme, nom, 'DALLE',
                                        'le rectangle ne porte que l\'aplat de nature'))
                    cibleT = hexrgb(spec['trait'][0 if theme == 'dark' else 1])
                    vues = 0
                    for seg in ch['ligne']:
                        c = rgbof(seg['dom']) if seg['dom'] else None
                        if c and max(abs(c[k] - cibleT[k]) for k in range(3)) <= 24:
                            vues += 1
                    if vues == 0:
                        absents.append((theme, nom, 'TRAIT',
                                        'la ligne n\'est pas de la couleur attendue %s'
                                        % spec['trait'][0 if theme == 'dark' else 1]))

                for c in r['coll']:
                    colls.append((theme, nom, c))
                for d in r['deb']:
                    debs.append((theme, nom, d))
                if VERBOSE:
                    print("  · %-16s %-5s" % (nom, theme))
        b.close()

    print()
    print("=" * 78)
    print("  SECTION 1 — LES FICHES · les cinq lignes du critère")
    print("=" * 78)
    print("  écarts de position > %d px ............ %d" % (TOL, len(ecarts)))
    print("  écarts de style ...................... %d" % len(styles))
    print("  ÉLÉMENTS DÉCLARÉS MAIS PAS PEINTS .... %d" % len(absents))
    print("  collisions de blocs .................. %d" % len(colls))
    print("  éléments au-delà de y = 844 .......... %d" % len(debs))
    print("=" * 78)
    for a in absents:
        print("  ✗ PEINT %-5s %-15s %-16s %s" % a)
    for e in ecarts:
        print("  ✗ POS  %-5s %-15s %-16s %-3s attendu %-6s mesuré %s" % e)
    for s in styles:
        print("  ✗ STY  %-5s %-15s %-16s %-8s attendu %-9s mesuré %s" % s)
    for c in colls:
        print("  ✗ COL  %-5s %-15s %s" % c)
    for d in debs:
        print("  ✗ DEB  %-5s %-15s %s" % d)
    total = len(ecarts) + len(styles) + len(colls) + len(debs) + len(absents)
    print()
    print(("  ✅  SECTION 1 AU VERT." if total == 0 else "  ❌  %d écarts restants." % total))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
