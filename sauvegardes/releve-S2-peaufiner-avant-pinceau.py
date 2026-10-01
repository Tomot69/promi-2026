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
TOL = 3

CREME, ENCRE = '#F4EEE1', '#16171B'
BLEU, FRAMB, MAUVE = '#3A54FF', '#FA2258', '#8A5CF0'
CLAIRP, CLAIRC, CLAIRN = '#CBAAFF', '#FFC0A8', '#D0B0FF'
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
#                                             §3.4 (104 ou 118), §3.6 (62), §3.8 (304)
PROMI = flux([('À QUI', 64), ('AVANT', 64), ('DANS UNE NUÉE', 64), ('NOTE', 118),
              ('PIÈCES JOINTES', 92), ('COMMENTAIRES', 118), ('RELANCER', 64),
              ('cercle', 304), ('SUPPRIMER CE PROMI', 64)])
CHICHE = flux([('À QUI JE LANCE', 64), ('AVEC', 64), ('AVANT', 64), ('NOTE', 118),
               ('PIÈCES JOINTES', 92), ('COMMENTAIRES', 104), ('RELANCER', 64),
               ('cercle', 304), ('SUPPRIMER CE CHICHE', 64)])
NUEE = flux([('DESCRIPTION', 104), ('MEMBRES', 64), ('PIÈCES JOINTES', 92),
             ('COMMENTAIRES', 104), ('bouton', 62), ('DISSOUDRE LA NUÉE', 64)])

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
    if(!t){ bad.push((e.className||'')+' : AUCUN TEXTE'); return; }
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


def hexa(c):
    m = [int(x) for x in (c or '').replace('rgba(', '').replace('rgb(', '').replace(')', '').split(',')[:3] if x.strip()]
    return ('#%02X%02X%02X' % tuple(m)) if len(m) == 3 else c


def juge():
    pos, sty, coll, hors, peint = [], [], [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        er = []
        pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto('file://' + APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            light = (th == 'light')
            for nom, attendu in ECRANS.items():
                if not pg.evaluate(SCENE, nom):
                    pos.append('%s [%s] : ÉCRAN ABSENT' % (nom, th)); continue
                pg.wait_for_timeout(1100)
                pg.evaluate("()=>{ if(window._s2Ouvre) window._s2Ouvre(true); }")
                pg.wait_for_timeout(700)
                m = pg.evaluate(MESURE)
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
                        if s['ff'] != 'Bricolage' or s['fw'] != '700' or abs(s['fs'] - 26) > 0.6:
                            sty.append(E + ' titre : %s %s/%s au lieu de Bricolage 700/26' % (s['ff'], s['fw'], s['fs']))
                        if hexa(s['fill']) != (ENCRE if light else CREME):
                            sty.append(E + ' titre : encre %s au lieu de %s' % (hexa(s['fill']), ENCRE if light else CREME))
                    if t.get('fermer'):
                        s = t['fermer']['s']
                        if s['ff'] != 'Apfel' or abs(s['fs'] - 12.5) > 0.6:
                            sty.append(E + ' FERMER : %s /%s au lieu de Apfel 12.5' % (s['ff'], s['fs']))

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
                    # style du réglage (§3.3) : contour 3, rayon 22
                    if nomA not in ('cercle', 'bouton'):
                        s = got['sty']
                        if abs(s['bw'] - 3) > 0.6:
                            sty.append(E + ' %s : contour %.1f au lieu de 3' % (got['nom'], s['bw']))
                        if abs(s['br'] - 22) > 0.6:
                            sty.append(E + ' %s : rayon %.0f au lieu de 22' % (got['nom'], s['br']))
                        if s['bs'] == 'solid' and hexa(s['bc']) != bord:
                            sty.append(E + ' %s : contour %s au lieu de %s' % (got['nom'], hexa(s['bc']), bord))
                        if got.get('lab'):
                            ls = got['lab']['s']
                            if ls['ff'] != 'Apfel' or ls['fw'] != '500' or abs(ls['fs'] - 11.5) > 0.6:
                                sty.append(E + ' %s libellé : %s %s/%s au lieu de Apfel 500/11.5'
                                           % (got['nom'], ls['ff'], ls['fw'], ls['fs']))
                            if hexa(ls['fill']) != tlab:
                                sty.append(E + ' %s libellé : %s au lieu de %s' % (got['nom'], hexa(ls['fill']), tlab))
                        if got.get('val') and 's2-vide' not in got['cls']:
                            vs = got['val']['s']
                            if vs['ff'] != 'Bricolage' or vs['fw'] != '700' or abs(vs['fs'] - 18) > 0.6:
                                sty.append(E + ' %s valeur : %s %s/%s au lieu de Bricolage 700/18'
                                           % (got['nom'], vs['ff'], vs['fw'], vs['fs']))
                            if hexa(vs['fill']) != tval:
                                sty.append(E + ' %s valeur : %s au lieu de %s' % (got['nom'], hexa(vs['fill']), tval))
                        if got.get('vis'):
                            ws = got['vis']['s']
                            if ws['ff'] != 'Bricolage' or ws['fw'] != '600' or abs(ws['fs'] - 14) > 0.6:
                                sty.append(E + ' %s visibilité : %s %s/%s au lieu de Bricolage 600/14'
                                           % (got['nom'], ws['ff'], ws['fw'], ws['fs']))
                        if got.get('txt'):
                            xs = got['txt']['s']
                            if xs['ff'] != 'Bricolage' or xs['fw'] != '600' or abs(xs['fs'] - 18) > 0.6:
                                sty.append(E + ' %s contenu : %s %s/%s au lieu de Bricolage 600/18'
                                           % (got['nom'], xs['ff'], xs['fw'], xs['fs']))
                    # le bloc du Cercle (§3.8)
                    if nomA == 'cercle':
                        rs = got.get('regs') or []
                        if len(rs) != 4:
                            pos.append(E + ' Cercle : %d réglages au lieu de 4' % len(rs))
                        mots = [r['t'] for r in rs]
                        att4 = ["C'EST IMPORTANT ?", 'RÉCURRENCE', 'RAPPEL', 'LA MÉMOIRE']
                        if mots != att4:
                            pos.append(E + ' Cercle : %s au lieu de %s' % (mots, att4))
                        for r in rs:
                            if 'blur(2.4px)' not in (r['sty']['fil'] or ''):
                                sty.append(E + ' Cercle : flou « %s » au lieu de blur(2.4px)' % r['sty']['fil'])
                        en = got.get('encart')
                        if not en:
                            pos.append(E + ' Cercle : encart ABSENT')
                        else:
                            dy = en['geo']['y'] - g['y']
                            if abs(dy - 108) > TOL:
                                pos.append(E + ' encart : %.0f px sous le bloc au lieu de 108' % dy)
                            if abs(en['geo']['h'] - 90) > TOL or abs(en['geo']['w'] - 342) > TOL:
                                pos.append(E + ' encart : %.0f × %.0f au lieu de 342 × 90' % (en['geo']['w'], en['geo']['h']))
                            if abs(en['sty']['br'] - 26) > 0.6:
                                sty.append(E + ' encart : rayon %.0f au lieu de 26' % en['sty']['br'])
                            if hexa(en['sty']['bg']) != (ENCRE if light else CREME):
                                sty.append(E + ' encart : fond %s au lieu de %s' % (hexa(en['sty']['bg']), ENCRE if light else CREME))
                            if en.get('t'):
                                ts = en['t']['s']
                                if ts['ff'] != 'Bricolage' or ts['fw'] != '700' or abs(ts['fs'] - 22) > 0.6:
                                    sty.append(E + ' encart titre : %s %s/%s au lieu de Bricolage 700/22'
                                               % (ts['ff'], ts['fw'], ts['fs']))
                                if en['t']['t'] != '✦ Le Cercle':
                                    pos.append(E + ' encart titre : « %s »' % en['t']['t'])
                            if en.get('s2') and en['s2']['t'] != 'importance, récurrence, rappels, mémoire':
                                pos.append(E + ' encart sous-titre : « %s »' % en['s2']['t'])
                    if nomA == 'bouton':
                        if abs(got['sty']['br'] - 31) > 0.6:
                            sty.append(E + ' bouton : rayon %.0f au lieu de 31' % got['sty']['br'])
                        if got.get('mot') != 'Planter un Promi dans la Nuée':
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
