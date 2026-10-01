#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-S5-instant.py — LE JUGE DE LA SECTION 5 (L'instant, cadres 96 à 101).

Compare l'app aux cotes de PROMI-SPECIFICATIONS.md §5 « L'instant », dans les deux thèmes.
base = 300, amplitude = 44, boîte SVG = 384 — les trois écrans, sans exception.

CINQUIÈME CONTRÔLE — LA PRÉSENCE PEINTE. Le champ, la dalle et la ligne vivent dans les
pixels d'un canevas dont le DOM ne sait rien : on les LIT.
   · « l'autre moitié arrive » : champ de NATURE, ma moitié en terracotta jusqu'au milieu,
     la moitié de l'autre en MENTHE au-delà, et des points terracotta encore plus loin.
   · « le trait se referme »   : champ MENTHE PLEIN — l'exception unique du produit.
   · « juste après »           : champ de NATURE, ligne MENTHE entière.

Usage :  python3 releve-S5-instant.py [--verbose]
"""
import sys

# ⚠ « APFEL 500 » N'EXISTE PAS — CONTRÔLE MIS À JOUR LE 19 AOÛT 2026 (CLAUDE.md §7).
#    L'inventaire écrit « Apfel 500 / 12.5 ». Cette face n'est PAS embarquée : les six
#    seules le sont Fraunces 600 (normal + italique), Bricolage 600, Bricolage 700,
#    Apfel 400 et ApfelMid 500. La graisse 500 existe bel et bien — dans ApfelMid, la
#    famille qui la porte. Le lot « polices » reporte donc `Apfel 500` sur `ApfelMid 500`,
#    et c'est CE couple qu'on attend ici. Le seuil ne bouge pas, la taille non plus :
#    seul le nom de la famille qui porte la graisse change. Voir QUESTIONS.md · Q68.
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
TOL = 3
CREME, ENCRE = '#F4EEE1', '#16171B'
MENTHE, TERRA, BLEU = '#2BE88C', '#F07A2E', '#3A54FF'

#  nom, cotes attendues (§5 · cadres 96 à 101)
ECRANS = {
    'arrive': {
        'dalle': (105, 91, 180, 150),
        'trace': {'y': 388, 'x': 24, 'w': 342, 'ff': 'Bricolage', 'fw': '700', 'fs': 17,
                  'col': MENTHE, 'mot': 'l’autre moitié arrive'},
        'aura': 432, 'qui': (556, 21, TERRA), 'titre': 586, 'quand': None,
        'tenue': None},
    'referme': {
        'dalle': (81, 88, 228, 190),
        'trace': None, 'aura': None, 'qui': None, 'titre': None, 'quand': None,
        'tenue': {'y': 388, 'fs': 64, 'sous': 472, 'sousFs': 20}},
    'apres': {
        'dalle': (105, 91, 180, 150),
        'trace': None, 'aura': 388, 'qui': (512, 21, MENTHE), 'titre': 542,
        # ⚠ CONTRAT MIS À JOUR (CLAUDE.md §7) — décision Tom du 29 août : les textes
        #   centraux montent d'un cran, l'état passe de 12,5 à 13,5. La règle vaut pour
        #   TOUTES les fiches et toutes les natures ; l'instant en est une.
        #   Original : sauvegardes/releve-S5-instant-avant-29aout.py
        'quand': (607, 13.5, MENTHE), 'tenue': None},
}

MESURE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const dp=document.getElementById('detailPoster'); if(!dp||!dp.classList.contains('show')) return null;
  const R=e=>{ if(!e) return null; const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden') return null;
    const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc, y:(r.top-dev.top)/sc, w:r.width/sc, h:r.height/sc}; };
  const S=e=>{ if(!e) return null; const c=getComputedStyle(e);
    return {ff:(c.fontFamily||'').split(',')[0].replace(/["']/g,''), fw:c.fontWeight,
            fs:parseFloat(c.fontSize), ls:c.letterSpacing, lh:c.lineHeight,
            fill:c.webkitTextFillColor||c.color, op:parseFloat(c.opacity), disp:c.display}; };
  const q=s=>dp.querySelector(s);
  const cv=document.getElementById('dpTrameCv');
  return {
    /* ⚠ la boîte du trait se MESURE dans le repère du cadre, comme tout le reste. La lire
       dans `style.height` mélangeait deux échelles : #device est mis à l'échelle par une
       transformation, donc `clientWidth` vaut 390 quand la boîte rendue en fait 364. Le
       juge sortait 412 sur un canevas de 384 — un faux rouge. */
    boite: R(cv) ? R(cv).h : null,
    boiteCss: cv?cv.style.height:null,
    marque:{g:R(document.getElementById('dptNat')), s:S(document.getElementById('dptNat')),
            t:(document.getElementById('dptNat')||{}).textContent},
    fermer:{g:R(q('.closeb')), s:S(q('.closeb'))},
    trace:{g:R(document.getElementById('dptTrace')), s:S(document.getElementById('dptTrace')),
           t:((document.getElementById('dptTrace')||{}).textContent||'').trim()},
    aura:{g:R(document.getElementById('dAura'))},
    qui:{g:R(document.getElementById('dptQui')), s:S(document.getElementById('dptQui'))},
    titre:{g:R(document.getElementById('dptTitre')), s:S(document.getElementById('dptTitre'))},
    quand:{g:R(document.getElementById('dptQuand')), s:S(document.getElementById('dptQuand')),
           t:((document.getElementById('dptQuand')||{}).textContent||'').trim()},
    tenue:{g:R(document.getElementById('instTenue')), s:S(document.getElementById('instTenue')),
           t:((document.getElementById('instTenue')||{}).textContent||'').trim()},
    sous:{g:R(document.getElementById('instSous')), s:S(document.getElementById('instSous')),
          t:((document.getElementById('instSous')||{}).textContent||'').trim()},
    geste:{g:R(q('.geste-env'))},
    corps:{g:R(document.getElementById('dpCorps'))},
    barre:{g:R(document.getElementById('dpDetails')),
           bg:(function(){const b=document.querySelector('#dpDetails .dpd-tog');
                return b?getComputedStyle(b).backgroundColor:null;})()},
    /* tout ce qui est peint et sort de l'écran */
    hors:[].slice.call(dp.querySelectorAll('*')).filter(e=>{
        const c=getComputedStyle(e);
        if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false;
        const r=e.getBoundingClientRect();
        if(r.width<4||r.height<4) return false;
        return (r.bottom-dev.top)/sc > 845 || (r.left-dev.left)/sc < -1 || (r.right-dev.left)/sc > 391;
      }).map(e=>(e.id?'#'+e.id:'.'+(e.className+'').split(' ')[0])).slice(0,6)
  };
}"""

PEINT = r"""(nom)=>{
  const bad=[];
  const cv=document.getElementById('dpTrameCv'); if(!cv) return ['aucun canevas'];
  const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
  const lire=(x,y)=>{const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;return [d[0],d[1],d[2],d[3]];};
  const prox=(p,h)=>Math.abs(p[0]-parseInt(h.slice(1,3),16))+Math.abs(p[1]-parseInt(h.slice(3,5),16))
                   +Math.abs(p[2]-parseInt(h.slice(5,7),16));
  /* 1 · LE CHAMP.
     ⚠ SONDE RÉÉCRITE LE 19 AOÛT 2026 — la règle est intacte ; c'est le NŒUD VISÉ qui a
     bougé. On lisait le champ en (20,20) « loin de la dalle et du trait » ; depuis que LA
     MATIÈRE REMPLIT LE CHAMP (décision Tom), ce pixel EST de la matière. Le champ se lit
     désormais sur LE POURTOUR du cadre — le seul endroit qu'une matière centrée et mise en
     couverture ne recouvre pas — et on en prend la couleur DOMINANTE. On reste au pixel :
     aucune constante du test n'entre ici. Voir CLAUDE.md §7. */
  const pourtour=()=>{ const t={}; let n=0;
    const pt=[]; for(let x=2;x<388;x+=4){ pt.push([x,2]); }
    for(let y=2;y<200;y+=4){ pt.push([2,y]); pt.push([387,y]); }
    pt.forEach(([x,y])=>{ const p=lire(x,y); if(p[3]<200) return;
      const c=p[0]+','+p[1]+','+p[2]; t[c]=(t[c]||0)+1; n++; });
    let best=null,m=0; for(const c in t) if(t[c]>m){m=t[c];best=c;}
    return best? best.split(',').map(Number).concat([255]) : lire(20,20); };
  const haut=pourtour();
  if(haut[3]<200) bad.push('aucun aplat peint en haut du champ');
  if(nom==='referme'){ if(prox(haut,'#2BE88C')>30)
      bad.push('LE CHAMP N\'EST PAS MENTHE : rgb('+haut.slice(0,3)+') — c\'est l\'exception du produit'); }
  else { if(prox(haut,'#2BE88C')<30) bad.push('le champ est menthe hors de l\'instant qui se referme'); }
  /* 2 · la dalle, au centre de sa boîte */
  const b = (nom==='referme') ? [81,88,228,190] : [105,91,180,150];
  const c=lire(b[0]+b[2]/2, b[1]+b[3]/2);
  if(c[3]<200) bad.push('DALLE : rien de peint au centre de sa boîte');
  if(Math.abs(c[0]-haut[0])<6&&Math.abs(c[1]-haut[1])<6&&Math.abs(c[2]-haut[2])<6)
    bad.push('DALLE : le centre a exactement la couleur du champ — rien n\'y est dessiné');
  /* 3 · la ligne : on longe l'onde et on compte ce qui s'y peint */
  const per=1.5, amp=44, mont=amp*0.34, a=amp*0.62, base=300;
  const y=x=>{const t=Math.min(1,Math.max(0,x/390));return base-mont*t-a*Math.sin(2*Math.PI*per*t);};
  /* ⚠ ON LIT LE CENTRE DE LA LIGNE, PAS SON VOISINAGE. Chercher « le premier pixel menthe
     à ±9 px » rendait la sonde aveugle sur « le trait se referme » : là, TOUT le champ
     au-dessus de l'onde est menthe, et la ligne d'encre passait pour menthe. Le trait fait
     10 px d'épaisseur : son centre est en y(x), et il n'y a qu'une couleur à cet endroit. */
  function couleurA(x){ const votes={};
    for(let d=-2;d<=2;d+=1){ const p=lire(x,y(x)+d); if(p[3]<200) continue;
      if(prox(p,'#16171B')<40) votes.encre=(votes.encre||0)+1;
      else if(prox(p,'#2BE88C')<40) votes.menthe=(votes.menthe||0)+1;
      else if(prox(p,'#F07A2E')<40) votes.terra=(votes.terra||0)+1; }
    let best=null,n=0; for(const k in votes) if(votes[k]>n){n=votes[k];best=k;}
    return best; }
  if(nom==='arrive'){
    if(couleurA(80)!=='terra') bad.push('ma moitié n\'est pas terracotta à x=80 ('+couleurA(80)+')');
    if(couleurA(230)!=='menthe') bad.push('la moitié de l\'autre n\'est pas menthe à x=230 ('+couleurA(230)+')');
    let pts=0; for(let x=300;x<385;x+=6) if(couleurA(x)==='terra') pts++;
    if(pts<3) bad.push('les points ne sont pas peints après le doigt ('+pts+')');
  } else if(nom==='referme'){
    if(couleurA(80)!=='encre') bad.push('la ligne n\'est pas à l\'encre à x=80 ('+couleurA(80)+')');
    if(couleurA(340)!=='encre') bad.push('la ligne n\'est pas à l\'encre à x=340 ('+couleurA(340)+')');
  } else {
    if(couleurA(80)!=='menthe') bad.push('la ligne n\'est pas menthe à x=80 ('+couleurA(80)+')');
    if(couleurA(340)!=='menthe') bad.push('la ligne n\'est pas menthe à x=340 ('+couleurA(340)+')');
  }
  /* 4 · l'encre des textes contre le fond RÉELLEMENT peint dessous */
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const dp=document.getElementById('detailPoster');
  const rgb=s=>{const m=(s||'').match(/[\d.]+/g);return m?m.slice(0,3).map(Number):null;};
  const lum=c=>c?(0.2126*c[0]+0.7152*c[1]+0.0722*c[2]):0;
  const fondSous=e=>{ const r=e.getBoundingClientRect();
    const x=(r.left+Math.min(r.width/2,40)-dev.left)/sc, yy=(r.top+r.height/2-dev.top)/sc;
    if(yy*k<cv.height){ const d=g.getImageData(Math.round(x*k),Math.round(yy*k),1,1).data;
      if(d[3]>200) return [d[0],d[1],d[2]]; }
    return rgb(getComputedStyle(dp).backgroundColor); };
  ['#dptNat','.closeb','#dptTrace','#dptQui','#dptTitre','#dptQuand','#instTenue','#instSous']
    .forEach(s=>{ const e=dp.querySelector(s); if(!e) return;
      const cs=getComputedStyle(e); if(cs.display==='none') return;
      const t=(e.textContent||'').trim(); if(!t) return;
      if(parseFloat(cs.opacity)<0.72) bad.push(s+' : opacité '+cs.opacity);
      const enc=rgb(cs.webkitTextFillColor||cs.color), ref=fondSous(e);
      if(enc&&ref&&Math.abs(lum(enc)-lum(ref))<42)
        bad.push(s+' « '+t.slice(0,18)+' » : ton sur ton (Δ'+Math.round(Math.abs(lum(enc)-lum(ref)))+')');
    });
  return bad;
}"""


def hexa(c):
    m = [int(float(x)) for x in (c or '').replace('rgba(', '').replace('rgb(', '').replace(')', '').split(',')[:3] if x.strip()]
    return ('#%02X%02X%02X' % tuple(m)) if len(m) == 3 else c


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
        pid = pg.evaluate("""()=>{var p=promises.filter(function(q){return !q.draft&&!q.req&&q.who&&q.who!=='moi';})[0]
          ||promises.filter(function(q){return !q.draft&&!q.req;})[0]; return p?p.id:null;}""")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            light = (th == 'light')
            for nom, A in ECRANS.items():
                pg.evaluate("(id)=>{if(window.closeAll)closeAll();openDetail(id);}", pid)
                pg.wait_for_timeout(1100)
                pg.evaluate("(k)=>window._instantJoue(k)", nom); pg.wait_for_timeout(800)
                m = pg.evaluate(MESURE)
                E = '  %-9s [%s]' % (nom, th)
                if not m:
                    pos.append(E + ' : ÉCRAN NON JOUABLE'); continue
                vus.append((nom, th))

                # ── la boîte du trait : base 300 + amp 44 + 40 = 384 (§2.4 bis) ──
                if m['boite'] is not None and abs(m['boite'] - 384) > TOL:
                    pos.append(E + ' boîte du trait %.0f au lieu de 384' % m['boite'])

                # ── l'entête (§3.1) : 24 / 38, hauteur 34 ──
                g = m['marque']['g']
                if not g:
                    pos.append(E + ' mot-marque ABSENT')
                else:
                    if abs(g['x'] - 24) > TOL or abs(g['y'] - 38) > TOL:
                        pos.append(E + ' mot-marque (%.0f,%.0f) au lieu de (24,38)' % (g['x'], g['y']))
                    s = m['marque']['s']
                    if s['ff'] != 'Fraunces' or s['fw'] != '600' or abs(s['fs'] - 27) > 0.6:
                        sty.append(E + ' mot-marque : %s %s/%s au lieu de Fraunces 600/27' % (s['ff'], s['fw'], s['fs']))
                    att = ENCRE if nom == 'referme' else CREME
                    if hexa(s['fill']) != att:
                        sty.append(E + ' mot-marque : encre %s au lieu de %s' % (hexa(s['fill']), att))
                if m['fermer']['g'] and abs(m['fermer']['g']['y'] - 38) > TOL:
                    pos.append(E + ' ✕ FERMER à y=%.0f au lieu de 38' % m['fermer']['g']['y'])

                def bloc(cle, mes, ax, ay, aw=None, ff=None, fw=None, fs=None, col=None, mot=None):
                    if not mes['g']:
                        pos.append(E + ' %s ABSENT' % cle); return
                    gg = mes['g']
                    if abs(gg['x'] - ax) > TOL or abs(gg['y'] - ay) > TOL:
                        pos.append(E + ' %s (%.0f,%.0f) au lieu de (%d,%d)' % (cle, gg['x'], gg['y'], ax, ay))
                    if aw and abs(gg['w'] - aw) > TOL:
                        pos.append(E + ' %s large de %.0f au lieu de %d' % (cle, gg['w'], aw))
                    ss = mes['s']
                    if ff and (ss['ff'] != ff or ss['fw'] != fw or abs(ss['fs'] - fs) > 0.6):
                        sty.append(E + ' %s : %s %s/%s au lieu de %s %s/%s' % (cle, ss['ff'], ss['fw'], ss['fs'], ff, fw, fs))
                    if col and hexa(ss['fill']) != col:
                        sty.append(E + ' %s : encre %s au lieu de %s' % (cle, hexa(ss['fill']), col))
                    if mot is not None and mes.get('t', '').strip() != mot:
                        sty.append(E + ' %s « %s » au lieu de « %s »' % (cle, mes.get('t', '')[:28], mot))

                T = A['trace']
                if T:
                    bloc('mot de l\'instant', m['trace'], T['x'], T['y'], T['w'],
                         T['ff'], T['fw'], T['fs'], T['col'], T['mot'])
                elif m['trace']['g']:
                    pos.append(E + ' mot de l\'instant PEINT alors que le cadre n\'en porte pas')

                if A['aura']:
                    if not m['aura']['g']:
                        pos.append(E + ' Noyaux ABSENTS')
                    elif abs(m['aura']['g']['x'] - 24) > TOL or abs(m['aura']['g']['y'] - A['aura']) > TOL:
                        pos.append(E + ' Noyaux (%.0f,%.0f) au lieu de (24,%d)'
                                   % (m['aura']['g']['x'], m['aura']['g']['y'], A['aura']))
                elif m['aura']['g']:
                    pos.append(E + ' Noyaux PEINTS alors que le cadre n\'en porte pas')

                if A['qui']:
                    y, fs, col = A['qui']
                    bloc('à-qui', m['qui'], 24, y, 342, 'Bricolage', '600', fs,
                         col if not (nom == 'arrive' and False) else col)
                elif m['qui']['g']:
                    pos.append(E + ' à-qui PEINT alors que le cadre n\'en porte pas')

                if A['titre']:
                    bloc('titre', m['titre'], 24, A['titre'], 342, 'Bricolage', '700', 38,
                         ENCRE if light else CREME)
                elif m['titre']['g']:
                    pos.append(E + ' titre PEINT alors que le cadre n\'en porte pas')

                if A['quand']:
                    y, fs, col = A['quand']
                    bloc('état', m['quand'], 24, y, 342, 'ApfelMid', '500', fs, col,
                         'TENUE À DEUX · À L’INSTANT')
                elif m['quand']['g']:
                    pos.append(E + ' état PEINT alors que le cadre n\'en porte pas')

                if A['tenue']:
                    U = A['tenue']
                    bloc('« tenue. »', m['tenue'], 24, U['y'], 342, 'Bricolage', '700', U['fs'],
                         ENCRE if light else CREME, 'tenue.')
                    bloc('le mot qui suit', m['sous'], 24, U['sous'], 342, 'Bricolage', '600',
                         U['sousFs'], ENCRE if light else CREME)
                    if m['sous']['s'] and abs(float(m['sous']['s']['lh'].replace('px', '')) - U['sousFs'] * 1.3) > 1.5:
                        sty.append(E + ' le mot qui suit : interligne %s au lieu de %.0f'
                                   % (m['sous']['s']['lh'], U['sousFs'] * 1.3))
                else:
                    if m['tenue']['g']:
                        pos.append(E + ' « tenue. » PEINT alors que le cadre n\'en porte pas')

                # ── le geste et la zone de message ne sont sur AUCUN des trois cadres ──
                if m['geste']['g']:
                    coll.append(E + ' le geste est encore à l\'écran (aucun cadre n\'en porte)')
                if m['corps']['g']:
                    coll.append(E + ' la zone de message est encore à l\'écran')

                # ── la barre Peaufiner (§3.2) : 0 / 760, 390 × 84, fond de NATURE ──
                gb = m['barre']['g']
                if not gb:
                    pos.append(E + ' barre Peaufiner ABSENTE')
                else:
                    if abs(gb['y'] - 760) > TOL or abs(gb['h'] - 84) > TOL:
                        pos.append(E + ' barre Peaufiner (y %.0f, h %.0f) au lieu de (760,84)' % (gb['y'], gb['h']))
                    if hexa(m['barre']['bg']) != BLEU:
                        sty.append(E + ' barre Peaufiner : fond %s au lieu de %s (la NATURE, jamais l\'état)'
                                   % (hexa(m['barre']['bg']), BLEU))

                if m['hors']:
                    hors.append(E + ' hors cadre : ' + ', '.join(m['hors']))
                for msg in pg.evaluate(PEINT, nom):
                    peint.append(E + ' ' + msg)

        # ── LA SÉQUENCE : une seconde de menthe, puis le retour à la nature ──
        pg.evaluate("(id)=>{if(window.closeAll)closeAll();openDetail(id);}", pid); pg.wait_for_timeout(1100)
        pg.evaluate("()=>{window._instantTenue();}"); pg.wait_for_timeout(300)
        a = pg.evaluate("()=>window._instant")
        pg.wait_for_timeout(1200)
        b2 = pg.evaluate("()=>window._instant")
        if a != 'referme':
            peint.append('  la séquence : à 300 ms l\'écran est « %s » au lieu de « referme »' % a)
        if b2 != 'apres':
            peint.append('  la séquence : à 1,5 s l\'écran est « %s » au lieu de « apres »' % b2)

        if er:
            peint.append('  ERREURS JS : ' + ' | '.join(er[:3]))
        b.close()

    print('\n═══ SECTION 5 · L\'INSTANT — %d écrans mesurés ═══\n' % len(vus))
    for nom, lst in (('écarts de position > 3 px', pos), ('écarts de style', sty),
                     ('collisions', coll), ('débordements', hors), ('présence peinte', peint)):
        print('%-28s %d' % (nom, len(lst)))
        if lst and (VERBOSE or len(lst) <= 40):
            for l in lst: print('   ', l)
    total = len(pos) + len(sty) + len(coll) + len(hors) + len(peint)
    print('\n%s' % ('✅  SECTION 5 AU VERT' if total == 0 else '❌  %d ÉCARTS' % total))
    return total


if __name__ == '__main__':
    sys.exit(0 if juge() == 0 else 1)
