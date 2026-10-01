#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-S2-peaufiner.py — LE JUGE DE LA SECTION 2 (Peaufiner).

Compare l'app aux cotes de PROMI-SPECIFICATIONS.md §5 « Peaufiner », dans les deux thèmes.

CE QUE LE JUGE SAIT, ET QUI A ÉTÉ VÉRIFIÉ AVANT D'ÊTRE CODÉ :
les neuf cadres « Peaufiner » du moodboard ne sont pas neuf écrans mais QUATRE PAGES qui
défilent, découpées en pages de dessin. La preuve est arithmétique : chaque cote d'un cadre
« bas / suite » se déduit du précédent par l'écart de 16 px du §3.3, sans exception —
Promi : 46 → 180 → 260 (118+16, 64+16) · Chiche : 46 → 126 (64+16) · Nuée : 46 → 124.
Le juge mesure donc UNE liste continue, à partir de 110, et vérifie que chaque écart y est.
Le seul écart qui n'est pas 16 est celui que l'inventaire pose APRÈS le bloc du Cercle :
104 px (Promi 564 → 668, Chiche 430 → 534). Il est attendu tel quel.

Les cinq lignes du critère (AUTONOMIE-CLAUDE-CODE.md §2) :
    écarts de position > 3 px .................. 0
    écarts de style ............................ 0
    collisions de blocs ........................ 0   (sauf l'encart du Cercle, §3.8)
    éléments hors cadre ........................ 0
    batteries redteam .......................... au vert  (hors de ce script)

Le sixième contrôle, hérité de la section 1 : LA PRÉSENCE PEINTE. Une cote juste sur un
élément invisible est un faux vert.

Usage :  python3 releve-S2-peaufiner.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/app.html"
VERBOSE = '--verbose' in sys.argv
# ⚑ LA BASCULE DU RAYON (Tom, 11 sept. 2026, Q203) — mesurée sur l'encre, écrite EN DUR : rayon = hauteur ÷ 2 jusqu'à
#   94,5, 30 au-delà. Le juge porte la décision ; l'app doit la déclarer (`window._seuilPilule`).
SEUIL_PILULE = 94.5
TOL = 3

# ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 29 septembre 2026 (v98, Tom : « releve-S2 est périmé : remets-le au
#   niveau de la décision — il attend encore Bricolage, Apfel et l'ancienne crème »).
#   LES RÈGLES QU'IL ENCODAIT : la palette d'avant le 16 septembre (crème #F4EEE1, encre #16171B, libellés en couleur de
#   nature pleine en clair, en clair de nature #CBAAFF/#FFC0A8/#D0B0FF en sombre) et les polices Bricolage / Apfel.
#   LES DÉCISIONS QUI LES REMPLACENT, écrites EN DUR (un juge ne lit pas la valeur qu'il vérifie) :
#   · crème #F7F0DE, encre du clair #201908 (16 sept., puis v7 du 20 sept.) ;
#   · libellé en clair = le COMPAGNON SOMBRE de la nature (Q221, 17 sept.) : Promi #022140, Chiche #3D0F23 ; la Nuée prend le
#     brun encre #43291C (v7, 20 sept. : « le violet quitte le rôle d'encre, le brun encre le prend ») ;
#   · libellé en sombre = NATCLAIR (CLAUDE §2.1 bis : « NATCLAIR garde les libellés ») : #C4A2F5, #F5AC9E, et #C9A8F5 pour la Nuée ;
#   · Bricolage → Gilbert (une seule graisse : « ce qui était Bricolage 600 passe en Gilbert 700 », §6), Apfel → Atkinson ;
#   · FERMER à 13 (le plancher typographique du 2 septembre, `echelle()`), plus 12,5 ;
#   · la rangée qui SUPPRIME (v16, Q296) : pas de pilule (contour transparent), libellé terracotta #DD4D23, pas de valeur.
#   La tolérance ne bouge pas (0,6 px sur les tailles, égalité stricte sur les couleurs). Version d'origine :
#   sauvegardes/releve-S2-peaufiner-avant-v98.py
CREME, ENCRE = '#F7F0DE', '#201908'
BLEU, FRAMB, MAUVE = '#022140', '#3D0F23', '#43291C'
CLAIRP, CLAIRC, CLAIRN = '#C4A2F5', '#F5AC9E', '#C9A8F5'   # NATCLAIR, qui « garde les libellés » (CLAUDE §2.1 bis) ; la Nuée y vaut #C9A8F5
DANGER = '#DD4D23'
TITRE, TEXTE = 'Gilbert', 'Atkinson'
def gilbert(s, taille):   # Gilbert n'a qu'une graisse : 600 demandé se peint en 700 (§6)
    return s['ff'] == TITRE and s['fw'] in ('600', '700') and abs(s['fs'] - taille) <= 0.6
DALLE3 = {'promi': '#AE86F2', 'chiche': '#F2977A', 'nuee': '#C2A4F7'}


def flux(items):
    """La liste continue : premier réglage à 110, écart 16 — 104 après le bloc du Cercle."""
    out, y = [], 110
    prev = None
    for it in items:
        nom, h = it[0], it[1]
        if prev == 'cercle':
            y += 104 - 16
        out.append((nom, y, h))
        y += h + 16
        prev = nom
    return out


# ── les inventaires, écran par écran ──────────────────────────────────────────────────
#  (nom du bloc, hauteur)          hauteurs : §3.3 (64), §3.3 variante (92),
#                                             §3.4 (104 ou 118), §3.6 (62), §3.8 (384 — 5 réglages, 13 sept.)
# ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7 de CLAUDE.md) — 2 septembre 2026.
#    LA RÈGLE QU'IL ENCODAIT : « Peaufiner d'une fiche est la suite de blocs des cadres
#    78 à 83, dans cet ordre, à partir de 110 ». LA DÉCISION QUI LA COMPLÈTE : Tom,
#    2 septembre — « le pinceau se reprend depuis Peaufiner, HAUT DE LISTE, sur une fiche
#    comme sur une Nuée » (variante D : la rangée de 64 garde le rythme de Peaufiner).
#    « LE TRAIT » est donc un bloc de 64 en tête, et tout le reste descend de 80 —
#    l'écart de 16 compris. La Nuée, elle, porte SA carte (`#npTrait`), et
#    `redteam_nuee` la connaît : rien à ajouter ici, sa liste est celle de l'app.
#    Ce n'est pas un desserrement : ordre, hauteurs et cotes restent vérifiés au pixel.
#    Version d'origine : sauvegardes/releve-S2-peaufiner-avant-pinceau.py
PROMI = flux([('LE TRAIT', 64), ('À QUI', 64), ('AVANT', 64), ('DANS UN CERCLE', 64), ('NOTE', 118),
              ('PIÈCES JOINTES', 92), ('COMMENTAIRES', 118), ('RELANCER', 64),
              ('cercle', 384), ('SUPPRIMER CE PROMI', 64)])
CHICHE = flux([('LE TRAIT', 64), ('À QUI JE LANCE', 64), ('AVEC', 64), ('AVANT', 64), ('NOTE', 118),
               ('PIÈCES JOINTES', 92), ('COMMENTAIRES', 104), ('RELANCER', 64),
               ('cercle', 384), ('SUPPRIMER CE CHICHE', 64)])
#    ⚠ ICI LA RANGÉE FAIT 64, ET C'EST BIEN LA NUÉE DE LA SECTION 2. Une Nuée a DEUX
#    Peaufiner : celui de la section 2, en flux dans `.s2-liste` — c'est celui que ce juge
#    mesure — et celui que `lot-NUEE-PEAUFINER` bâtit en cotes ABSOLUES (`#npTrait`,
#    `#npDesc`…), que `redteam_nuee` mesure sur les cadres 84/86. Le premier prend la
#    rangée de 64 comme une fiche ; le second une carte de 118, parce que ses cartes sont
#    clouées à cote fixe et qu'un dépliage y recouvrirait la suivante. Mesuré, les deux :
#    110/190/310/390/498 ici, 110/244/364/444/552 là-bas.
NUEE = flux([('LE TRAIT', 64), ('DESCRIPTION', 104), ('MEMBRES', 64), ('PIÈCES JOINTES', 92),
             ('COMMENTAIRES', 104), ('bouton', 62), ('DISSOUDRE LE CERCLE', 64)])

ECRANS = {'promi': PROMI, 'chiche': CHICHE, 'nuee': NUEE}
TEINTE = {'promi': (CLAIRP, BLEU), 'chiche': (CLAIRC, FRAMB), 'nuee': (CLAIRN, MAUVE)}

SCENE = r"""(nom)=>{
  function tr(pred){ for(var i=0;i<promises.length;i++){ var p=promises[i]; if(pred(p)) return p; } return null; }
  var p=null;
  if(nom==='promi'){
    p = tr(function(q){return !q.draft && q.status==='encours';}); if(!p) return null;
    delete p.chiche; delete p.avec; p.who='Rachel'; p.from=null;
  } else if(nom==='chiche'){
    p = tr(function(q){return !q.draft && q.status==='encours';}); if(!p) return null;
    p.chiche=true; p.who='Marion'; delete p.avec; delete p.nuee; p.from=null;
  } else if(nom==='nuee'){
    var k=null; try{ for(var q in NUE){ k=q; break; } }catch(e){}
    if(!k) return null; openNueeDetail(k); return 'nuee';
  }
  openDetail(p.id); return p.id;
}"""

MESURE = r"""()=>{
  const dev=document.querySelector('#device'); const fb=dev.getBoundingClientRect();
  const sc=fb.width/390;
  const corps=document.getElementById('dpdCorps');
  const liste=corps?corps.querySelector('.s2-liste'):null;
  if(!liste) return null;
  const y0=corps.getBoundingClientRect().top;
  const R=(e)=>{const b=e.getBoundingClientRect();
    return {x:(b.left-fb.left)/sc, y:(b.top-y0)/sc + corps.scrollTop, w:b.width/sc, h:b.height/sc};};
  const S=(e)=>{const c=getComputedStyle(e);
    /* ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 20 août 2026.
       Règle encodée : « ce libellé est en Apfel 500 », transcrite du moodboard.
       Décision qui l'a remplacée : **AUCUNE GRAISSE HORS DES SIX FACES EMBARQUÉES**
       (CLAUDE.md §6, lot du 19 août). `Apfel 500` N'EXISTE PAS ; la graisse 500 vit dans
       `ApfelMid`, et la table de report l'y envoie. Le document écrit « Apfel 500 » à
       plusieurs endroits — c'est la GRAISSE voulue, pas la face qui la porte (QUESTIONS · Q68).
       Le juge lisait donc la famille RÉELLE et criait 39 à 48 écarts sur un produit juste.
       On applique la table de report avant de comparer : même intention, bon nœud.
       Version d'origine : sauvegardes/releve-S2-avant-polices.py */
    const REPORT = {'apfelmid|500':'Apfel', 'apfelmid|400':'Apfel'};
    const _ff0 = (c.fontFamily||'').split(',')[0].replace(/['"]/g,'');
    const _ffR = REPORT[_ff0.toLowerCase()+'|'+c.fontWeight] || _ff0;
    return {ff:_ffR, ffReel:_ff0, fw:c.fontWeight,
            fs:parseFloat(c.fontSize), col:c.color, fill:c.webkitTextFillColor||c.color,
            ls:c.letterSpacing, op:parseFloat(c.opacity),
            bw:parseFloat(c.borderTopWidth), bc:c.borderTopColor, bs:c.borderTopStyle,
            br:parseFloat(c.borderTopLeftRadius), bg:c.backgroundColor, fil:c.filter};};
  const blocs=[...liste.children].map(e=>{
    const cl=(typeof e.className==='string'?e.className:'');
    let nom='?';
    if(cl.indexOf('s2-tete')>=0) nom='tete';
    else if(cl.indexOf('s2-cercle')>=0) nom='cercle';
    else if(cl.indexOf('s2-bouton')>=0) nom='bouton';
    else { const l=e.querySelector('.s2-lab'); nom=l?l.textContent.trim():'?'; }
    const o={nom:nom, geo:R(e), sty:S(e), cls:cl};
    const l=e.querySelector('.s2-lab'), v=e.querySelector('.s2-val'),
          vi=e.querySelector('.s2-vis'), tx=e.querySelector('.s2-txt');
    if(l) o.lab={t:l.textContent.trim(), s:S(l), g:R(l)};
    if(v) o.val={t:v.textContent.trim(), s:S(v), g:R(v)};
    if(vi) o.vis={t:vi.textContent.trim(), s:S(vi), g:R(vi)};
    if(tx) o.txt={t:(tx.value!==undefined?(tx.value||tx.placeholder||''):tx.textContent.trim()), s:S(tx), g:R(tx)};
    if(nom==='cercle'){
      o.regs=[...e.querySelectorAll('.s2-reg')].map(r=>{const l2=r.querySelector('.s2-lab');
        return {t:l2?l2.textContent.trim():'', geo:R(r), sty:S(r)};});
      const en=e.querySelector('.s2-encart');
      if(en){ const t=en.querySelector('.s2-enc-t'), s=en.querySelector('.s2-enc-s');
        o.encart={geo:R(en), sty:S(en), t:t?{t:t.textContent.trim(),s:S(t)}:null,
                  s2:s?{t:s.textContent.trim(),s:S(s)}:null}; }
    }
    if(nom==='bouton') o.mot=e.textContent.trim();
    if(nom==='tete'){ const a=e.querySelector('.s2-titre'), f=e.querySelector('.s2-fermer');
      o.titre=a?{t:a.textContent.trim(),s:S(a),g:R(a)}:null;
      o.fermer=f?{t:f.textContent.trim(),s:S(f),g:R(f)}:null; }
    return o;});
  /* la barre Peaufiner : elle ne bouge jamais (§6) */
  const bar=document.querySelector('#dpDetails .dpd-tog');
  const bg=bar?(()=>{const b=bar.getBoundingClientRect();
    return {x:(b.left-fb.left)/sc,y:(b.top-fb.top)/sc,w:b.width/sc,h:b.height/sc};})():null;
  /* débordement latéral et hauteur totale de la liste */
  const lb=liste.getBoundingClientRect();
  /* RIEN D'AUTRE NE SE PEINT DANS LE CORPS. L'ancien tiroir y déversait les blocs de la
     Nuée : ils repassaient SOUS la page sans qu'aucune cote ne bouge. */
  const intrus=[...corps.children].filter(e=>!e.classList.contains('s2-liste'))
    .filter(e=>{const c=getComputedStyle(e); const b=e.getBoundingClientRect();
      return c.display!=='none' && c.visibility!=='hidden' && b.height>2 && b.width>2;})
    .map(e=>(e.id||e.className||e.tagName)+'');
  return {blocs:blocs, barre:bg, intrus:intrus, hliste:liste.scrollHeight/sc,
          hcorps:corps.clientHeight/sc, xliste:(lb.left-fb.left)/sc, wliste:lb.width/sc};}"""

PEINT = r"""()=>{
  /* LA PRÉSENCE PEINTE : un texte qui n'a pas de texte, ou dont l'encre passe sous 72 %,
     ou qui a la couleur de son fond, est un faux vert. */
  const corps=document.getElementById('dpdCorps');
  const liste=corps?corps.querySelector('.s2-liste'):null; if(!liste) return [];
  const fond=getComputedStyle(corps).backgroundColor;
  const rgb=(s)=>{const m=(s||'').match(/[\d.]+/g); return m?m.slice(0,3).map(Number):null;};
  const lum=(c)=>c?(0.2126*c[0]+0.7152*c[1]+0.0722*c[2]):0;
  const F=rgb(fond);
  const bad=[];
  liste.querySelectorAll('.s2-lab,.s2-val,.s2-vis,.s2-txt,.s2-titre,.s2-fermer,.s2-enc-t,.s2-enc-s').forEach(e=>{
    const c=getComputedStyle(e);
    const t=(e.value!==undefined?(e.value||e.placeholder||''):e.textContent).trim();
    const dans=e.closest('.s2-cercle');           /* le bloc du Cercle est flouté exprès */
    if(!t){ if(e.classList.contains('s2-val') && e.closest('.v16-danger')) return;   /* v98 : la rangée qui supprime n'a pas de valeur (v16, Q296) */
      bad.push((e.className||'')+' : AUCUN TEXTE'); return; }
    const o=parseFloat(c.opacity);
    if(o<0.72) bad.push((e.className||'')+' « '+t.slice(0,22)+' » : opacité '+o);
    const enc=rgb(c.webkitTextFillColor||c.color);
    if(!enc) return;
    /* sur quel fond ? l'encart a le sien */
    const bloc=e.closest('.s2-encart')||e.closest('.s2-bouton')||corps;
    const B=rgb(getComputedStyle(bloc).backgroundColor);
    const ref=(B&&B.length&&getComputedStyle(bloc).backgroundColor!=='rgba(0, 0, 0, 0)')?B:F;
    if(!dans && ref && Math.abs(lum(enc)-lum(ref))<42)
      bad.push((e.className||'')+' « '+t.slice(0,22)+' » : ton sur ton (Δlum '+Math.round(Math.abs(lum(enc)-lum(ref)))+')');
  });
  return bad;}"""


def transparent(c):   # 'rgba(r, g, b, 0)' — un contour qu'on ne voit pas
    m = (c or '').replace('rgba(', '').replace(')', '').split(',')
    return (c or '').startswith('rgba(') and len(m) == 4 and float(m[3]) == 0

def hexa(c):
    m = [int(x) for x in (c or '').replace('rgba(', '').replace('rgb(', '').replace(')', '').split(',')[:3] if x.strip()]
    return ('#%02X%02X%02X' % tuple(m)) if len(m) == 3 else c


# ── LA CONDITION DE POSE ────────────────────────────────────────────────────
# Ce que « posé » veut dire, mesuré et pas supposé : la liste de Peaufiner
# occupe sa largeur (≥ 300 sur un cadre de 390) et porte au moins deux blocs
# qui ont une hauteur. Tant que ce n'est pas vrai, il n'y a rien à mesurer.
POSE = r"""()=>{
  const c = document.getElementById('dpdCorps');
  const l = c && c.querySelector('.s2-liste');
  if(!l) return false;
  if(l.getBoundingClientRect().width < 300) return false;
  let n = 0;
  [].forEach.call(l.children, function(e){ if(e.getBoundingClientRect().height > 4) n++; });
  return n >= 2;
}"""


def _empreinte(m):
    """Ce que le juge COMPARE, et rien d'autre : la géométrie ET le style.

    ⚠ Une première version ne prenait que la géométrie. Elle sortait « posé »
    alors que le PLANCHER TYPOGRAPHIQUE n'était pas encore passé : la boîte
    ne bougeait plus, mais les libellés étaient encore à 11,5 et montaient à
    13 juste après. Le juge annonçait alors 30 à 39 écarts de style, **et pas
    les mêmes d'un passage à l'autre** — l'ancienne oscillation déplacée de la
    position vers le style. Une empreinte doit couvrir tout ce qu'on juge."""
    if not m:
        return None

    def sty(o):
        if not o:
            return None
        s = o.get('s') or o.get('sty') or {}
        return (s.get('ff'), s.get('fw'), s.get('fs'), s.get('col'), s.get('ls'))

    out = []
    for b in m.get('blocs', []):
        g = b.get('geo') or {}
        out.append((b.get('nom'),
                    round(g.get('x', 0), 1), round(g.get('y', 0), 1),
                    round(g.get('w', 0), 1), round(g.get('h', 0), 1),
                    sty(b), sty(b.get('lab')), sty(b.get('val')),
                    sty(b.get('vis')), sty(b.get('txt'))))
    return tuple(out)


def juge():
    pos, sty, coll, hors, peint = [], [], [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        er = []
        pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto('file://' + APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        seuil_app = pg.evaluate("()=>window._seuilPilule")
        if seuil_app != SEUIL_PILULE:
            sty.append('SEUIL DU RAYON : l’app déclare %r, la décision est %.1f (Q203)' % (seuil_app, SEUIL_PILULE))
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            light = (th == 'light')
            for nom, attendu in ECRANS.items():
                if not pg.evaluate(SCENE, nom):
                    pos.append('%s [%s] : ÉCRAN ABSENT' % (nom, th)); continue
                pg.wait_for_timeout(1100)
                pg.evaluate("()=>{ if(window._s2Ouvre) window._s2Ouvre(true); }")
                # ── ON ATTEND QUE L'ÉCRAN SOIT POSÉ, on ne compte plus sur une durée ──
                # Le Peaufiner d'une NUÉE sortait mesuré 0 × 0 une fois sur deux, et le
                # thème fautif changeait d'un passage à l'autre : ce n'était pas une
                # régression de l'app mais une course de construction dans le juge.
                # Un délai fixe ne peut pas la gagner. On attend une CONDITION —
                # la liste a sa largeur, ses blocs ont une hauteur — puis on exige
                # DEUX relevés identiques, comme le duo pixel (CLAUDE.md §8).
                try:
                    pg.wait_for_function(POSE, timeout=6000)
                except Exception:
                    pos.append('%s [%s] : ÉCRAN JAMAIS POSÉ (liste 0 × 0 après 6 s)'
                               % (nom, th)); continue
                m = pg.evaluate(MESURE)
                for _ in range(14):
                    pg.wait_for_timeout(150)
                    m2 = pg.evaluate(MESURE)
                    if m2 and m and _empreinte(m2) == _empreinte(m):
                        break
                    m = m2
                if not m:
                    pos.append('%s [%s] : LISTE ABSENTE' % (nom, th)); continue
                clair, plein = TEINTE[nom]
                tlab = plein if light else clair       # le libellé (§5, deux thèmes)
                tval = ENCRE if light else CREME
                bord = ENCRE if light else CREME
                E = '  %-22s [%s]' % (nom, th)

                blocs = [x for x in m['blocs'] if x['nom'] != 'tete']
                tete = [x for x in m['blocs'] if x['nom'] == 'tete']
                # ── l'entête à 24 / 36, hauteur 40 ──
                if not tete:
                    pos.append(E + ' entête ABSENTE')
                else:
                    t = tete[0]
                    if abs(t['geo']['x'] - 24) > TOL or abs(t['geo']['y'] - 36) > TOL:
                        pos.append(E + ' entête (%.0f,%.0f) au lieu de (24,36)' % (t['geo']['x'], t['geo']['y']))
                    if t.get('titre'):
                        s = t['titre']['s']
                        if not gilbert(s, 26):
                            sty.append(E + ' titre : %s %s/%s au lieu de Gilbert 700/26' % (s['ff'], s['fw'], s['fs']))
                        if hexa(s['fill']) != (ENCRE if light else CREME):
                            sty.append(E + ' titre : encre %s au lieu de %s' % (hexa(s['fill']), ENCRE if light else CREME))
                    if t.get('fermer'):
                        s = t['fermer']['s']
                        if s['ff'] != TEXTE or abs(s['fs'] - 13) > 0.6:
                            sty.append(E + ' FERMER : %s /%s au lieu de Atkinson 13' % (s['ff'], s['fs']))

                # ── les blocs, un par un, à leur cote ──
                if len(blocs) != len(attendu):
                    pos.append(E + ' %d blocs au lieu de %d : %s' %
                               (len(blocs), len(attendu), [x['nom'] for x in blocs]))
                for i, (att, got) in enumerate(zip(attendu, blocs)):
                    nomA, yA, hA = att
                    g = got['geo']
                    if abs(g['x'] - 24) > TOL:
                        pos.append(E + ' %s : x=%.0f au lieu de 24' % (got['nom'], g['x']))
                    if abs(g['w'] - 342) > TOL:
                        pos.append(E + ' %s : largeur %.0f au lieu de 342' % (got['nom'], g['w']))
                    if abs(g['y'] - yA) > TOL:
                        pos.append(E + ' %s : y=%.0f au lieu de %d' % (got['nom'], g['y'], yA))
                    if abs(g['h'] - hA) > TOL:
                        pos.append(E + ' %s : hauteur %.0f au lieu de %d' % (got['nom'], g['h'], hA))
                    if nomA not in ('cercle', 'bouton') and not got['nom'].startswith(nomA[:6]):
                        pos.append(E + ' rang %d : « %s » au lieu de « %s »' % (i + 1, got['nom'], nomA))
                    # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 2 septembre 2026.
                    #    LA RÈGLE QU'IL ENCODAIT : « un réglage a un contour de 3 et un rayon
                    #    de 22 » (§3.3, tel que les cadres 78 à 83 le dessinent).
                    #    LA DÉCISION QUI LA REMPLACE : LA GRAMMAIRE DES CONTOURS (loi 2, Tom,
                    #    2 septembre) — « trait 2, couleur du corps, RAYON = HAUTEUR ÷ 2 ; le
                    #    cadre ne se soustrait pas, c'est le reste qui monte jusqu'à lui »,
                    #    étendue à Peaufiner d'un coup sur Q157 : « laisser deux grammaires
                    #    dans le produit est pire ».
                    #    Ce n'est pas un desserrement : le rayon est vérifié CONTRE LA HAUTEUR
                    #    ATTENDUE (`hA`, celle de l'inventaire), pas contre la hauteur rendue —
                    #    une cote se calcule, jamais sur elle-même. Un rayon faux d'un pixel
                    #    est pris comme avant.
                    #    Version d'origine : sauvegardes/releve-S2-peaufiner-avant-contours.py
                    if nomA not in ('cercle', 'bouton'):
                        s = got['sty']
                        if abs(s['bw'] - 2) > 0.6:
                            sty.append(E + ' %s : contour %.1f au lieu de 2' % (got['nom'], s['bw']))
                        # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 11 septembre 2026.
                        #    LA RÈGLE QU'IL ENCODAIT : « tout champ a rayon = hauteur ÷ 2 » (la grammaire des
                        #    contours, Q157), y compris les zones de texte du §3.4.
                        #    LA DÉCISION QUI LA REMPLACE : Tom, 11 sept. (Q202) — « Prends P, pas T. […] Le rayon à
                        #    30 tient l'écart constant sans toucher à l'interligne — applique-le partout. » Un champ
                        #    de TROIS LIGNES ET PLUS (libellé, texte, visibilité : NOTE, COMMENTAIRES, DESCRIPTION)
                        #    prend le rayon 30 du grand panneau ; les autres gardent hauteur ÷ 2.
                        #    Ce n'est pas un desserrement : la valeur attendue change, la tolérance (0,6) non — un
                        #    rayon de 29 ou de 59 sur une zone est pris. Prouvé sur l'app d'avant le lot (rouge).
                        #    Version d'origine : sauvegardes/releve-S2-peaufiner-avant-cercle-mur.py
                        # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 11 septembre 2026, second passage.
                        #    LA RÈGLE QU'IL ENCODAIT : celle de Q202 ci-dessus — « trois lignes et plus → 30 », une règle de CLASSE
                        #    (NOTE, COMMENTAIRES, DESCRIPTION par leur nom).
                        #    LA DÉCISION QUI LA REMPLACE : Tom, 11 sept. — « rayon = moitié de la hauteur jusqu'à [la hauteur où la
                        #    pilule commence à manger le texte], 30 au-delà […] pose la bascule là, pas à un nombre de lignes
                        #    arbitraire. » Bascule MESURÉE sur l'encre : 94,5 (Q203, sauvegardes/audit-cercle/seuil_encre*.py).
                        #    Elle est écrite EN DUR (CLAUDE §7 : un juge qui lit la valeur qu'il vérifie ne vérifie rien) ; le juge
                        #    vérifie AUSSI que l'app la déclare (`window._seuilPilule`, plus haut). Même tolérance (0,6), même
                        #    hauteur ATTENDUE hA : LE TRAIT d'une Nuée (118) attend désormais 30, PIÈCES JOINTES (92) toujours 46.
                        #    Version d'origine : sauvegardes/releve-S2-peaufiner-avant-seuil.py
                        rA = hA / 2.0 if hA <= SEUIL_PILULE else 30.0
                        if abs(s['br'] - rA) > 0.6:
                            sty.append(E + ' %s : rayon %.0f au lieu de %.0f (%s)'
                                       % (got['nom'], s['br'], rA, ('hauteur %d ÷ 2' % hA) if hA <= SEUIL_PILULE else 'hauteur %d au-delà de 94,5 : 30' % hA))
                        danger = 'v16-danger' in (got.get('cls') or '')
                        if danger:   # la rangée qui supprime : pas de pilule (v16, Q296)
                            if s['bs'] == 'solid' and s['bw'] > 0 and not transparent(s['bc']):
                                sty.append(E + ' %s : contour %s au lieu de transparent' % (got['nom'], s['bc']))
                        elif s['bs'] == 'solid' and hexa(s['bc']) != bord:
                            sty.append(E + ' %s : contour %s au lieu de %s' % (got['nom'], hexa(s['bc']), bord))
                        # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 3 septembre 2026.
                        #    LA RÈGLE QU'IL ENCODAIT : « un libellé de réglage est en
                        #    Apfel 500 / 11,5 » — la cote des cadres 78 à 87 (§3.3 et §3.4).
                        #    LA DÉCISION QUI LA REMPLACE : Tom, 3 septembre — « les sept
                        #    passent à 13. Ils doivent être identiques, et le §6 interdit
                        #    11,5. Ce n'est pas le cadre qui gagne, c'est la loi. »
                        #    Le §6 de CLAUDE.md est formel : « Tailles minimales : rien en
                        #    dessous de 12 px ». 11,5 est SOUS le minimum du produit — le
                        #    cadre le dessine, mais un cadre ne peut pas contredire la loi :
                        #    c'est une ERREUR DE DESSIN, recensée dans ECARTS-MOODBOARD § 0 bis.7.
                        #    13 est le plancher typographique déjà en vigueur (`max(13, taille)`,
                        #    décision du 2 septembre) : les sept libellés le prennent tous.
                        #    Ce n'est PAS un desserrement — la tolérance reste 0,6, et un
                        #    libellé à 12 ou à 14 est pris comme avant. C'est la valeur
                        #    attendue qui change, pas la sévérité.
                        #    Version d'origine : sauvegardes/releve-S2-peaufiner-avant-libelles-13.py
                        if got.get('lab'):
                            ls = got['lab']['s']
                            if ls['ff'] != TEXTE or ls['fw'] != '500' or abs(ls['fs'] - 13) > 0.6:
                                sty.append(E + ' %s libellé : %s %s/%s au lieu de Atkinson 500/13'
                                           % (got['nom'], ls['ff'], ls['fw'], ls['fs']))
                            if hexa(ls['fill']) != (DANGER if danger else tlab):
                                sty.append(E + ' %s libellé : %s au lieu de %s' % (got['nom'], hexa(ls['fill']), DANGER if danger else tlab))
                        if got.get('val') and 's2-vide' not in got['cls']:
                            vs = got['val']['s']
                            if not gilbert(vs, 18):
                                sty.append(E + ' %s valeur : %s %s/%s au lieu de Gilbert 700/18'
                                           % (got['nom'], vs['ff'], vs['fw'], vs['fs']))
                            if hexa(vs['fill']) != tval:
                                sty.append(E + ' %s valeur : %s au lieu de %s' % (got['nom'], hexa(vs['fill']), tval))
                        if got.get('vis'):
                            ws = got['vis']['s']
                            if not gilbert(ws, 14):
                                sty.append(E + ' %s visibilité : %s %s/%s au lieu de Gilbert 700/14'
                                           % (got['nom'], ws['ff'], ws['fw'], ws['fs']))
                        if got.get('txt'):
                            xs = got['txt']['s']
                            if not gilbert(xs, 18):
                                sty.append(E + ' %s contenu : %s %s/%s au lieu de Gilbert 700/18'
                                           % (got['nom'], xs['ff'], xs['fw'], xs['fs']))
                    # le bloc du Cercle (§3.8)
                    if nomA == 'cercle':
                        rs = got.get('regs') or []
                        # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 13 septembre 2026. Tom : « LA COULEUR » est un
                        #    cinquième réglage du Cercle ; « vérifie que le bloc tient à cinq ». Bloc 5 × 64 + 4 × 16 = 384, encart
                        #    centré à (384 − 90) ÷ 2 = 147. Même sévérité. Version d'origine :
                        #    sauvegardes/releve-S2-peaufiner-avant-cercle-couleur.py
                        if len(rs) != 5:
                            pos.append(E + ' Cercle : %d réglages au lieu de 5' % len(rs))
                        mots = [r['t'] for r in rs]
                        # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 11 septembre 2026. L'ordre de
                        #    l'inventaire (C'EST IMPORTANT ? en tête) est remplacé par celui de Tom (Q202) :
                        #    « récurrence · rappels · importance · mémoire » — la récurrence se comprend tout de suite,
                        #    la mémoire, la plus abstraite, ne vend rien en tête de liste. Même sévérité : un ordre
                        #    différent est pris. Version d'origine : sauvegardes/releve-S2-peaufiner-avant-cercle-mur.py
                        att4 = ['RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE', 'LA COULEUR']
                        if mots != att4:
                            pos.append(E + ' Cercle : %s au lieu de %s' % (mots, att4))
                        # ⚑ v104 (Tom, 30 sept. 2026) — « les encarts qui disent LE CERCLE disparaissent ; un réglage verrouillé est
                        #    simplement flouté, sans explication » + « deux fois plus flou » (2,4 → 4,8). Réécrit au niveau de la
                        #    décision : l'encart doit être ABSENT, le flou à 4,8. Version d'origine : sauvegardes/releve-S2-peaufiner-avant-v104.py
                        for r in rs:
                            if 'blur(4.8px)' not in (r['sty']['fil'] or ''):
                                sty.append(E + ' Cercle : flou « %s » au lieu de blur(4.8px)' % r['sty']['fil'])
                        en = got.get('encart')
                        if en and en['geo']['w'] > 1 and en['geo']['h'] > 1:
                            pos.append(E + ' Cercle : un encart est encore peint (%.0f × %.0f) — il doit avoir disparu' % (en['geo']['w'], en['geo']['h']))
                    if nomA == 'bouton':
                        if abs(got['sty']['br'] - 31) > 0.6:
                            sty.append(E + ' bouton : rayon %.0f au lieu de 31' % got['sty']['br'])
                        if got.get('mot') != 'Planter un Promi dans le Cercle':   # v106 : la Nuée s'affiche « Cercle »
                            pos.append(E + ' bouton : « %s »' % got.get('mot'))

                # ── collisions : rien ne se chevauche, sauf l'encart du Cercle ──
                boites = [(x['nom'], x['geo']) for x in m['blocs']]
                for i in range(len(boites)):
                    for j in range(i + 1, len(boites)):
                        a, c = boites[i][1], boites[j][1]
                        if (a['x'] < c['x'] + c['w'] - 1 and c['x'] < a['x'] + a['w'] - 1
                                and a['y'] < c['y'] + c['h'] - 1 and c['y'] < a['y'] + a['h'] - 1):
                            coll.append(E + ' %s ∩ %s' % (boites[i][0], boites[j][0]))

                # ── hors cadre : marge latérale 24, rien ne sort ; la liste dégage la barre ──
                if abs(m['xliste']) > 0.6 or abs(m['wliste'] - 390) > 1:
                    hors.append(E + ' liste %.0f de large à x=%.0f (attendu 390 à 0)' % (m['wliste'], m['xliste']))
                dernier = m['blocs'][-1]['geo']
                reste = m['hliste'] - (dernier['y'] + dernier['h'])
                if reste < 30:
                    hors.append(E + ' dernier bloc à %.0f px du bas de la liste (consigne 30)' % reste)
                if m['barre'] and (abs(m['barre']['y'] - 760) > TOL or abs(m['barre']['h'] - 84) > TOL):
                    pos.append(E + ' barre Peaufiner à y=%.0f h=%.0f au lieu de 760 / 84'
                               % (m['barre']['y'], m['barre']['h']))

                for x in (m.get('intrus') or []):
                    coll.append(E + ' bloc étranger peint dans le corps : ' + x)

                # ── la présence peinte ──
                for x in pg.evaluate(PEINT):
                    peint.append(E + ' ' + x)

                if VERBOSE:
                    print(E)
                    for x in m['blocs']:
                        print('      %-24s y=%7.1f h=%6.1f x=%5.1f w=%5.1f'
                              % (x['nom'][:24], x['geo']['y'], x['geo']['h'], x['geo']['x'], x['geo']['w']))
        if er:
            peint.append('  ERREURS JS : ' + ' | '.join(er[:3]))
        b.close()
    return pos, sty, coll, hors, peint


if __name__ == '__main__':
    pos, sty, coll, hors, peint = juge()
    for titre, L in (('ÉCARTS DE POSITION (> 3 px)', pos), ('ÉCARTS DE STYLE', sty),
                     ('COLLISIONS', coll), ('HORS CADRE', hors), ('PRÉSENCE PEINTE', peint)):
        print('\n── %s : %d' % (titre, len(L)))
        for x in L[:40]:
            print('   ' + x)
        if len(L) > 40:
            print('   … et %d autres' % (len(L) - 40))
    print('\n%s  position %d · style %d · collisions %d · hors cadre %d · peinture %d'
          % ('✅ SECTION 2 AU CRITÈRE' if not (pos or sty or coll or hors or peint) else '❌',
             len(pos), len(sty), len(coll), len(hors), len(peint)))
