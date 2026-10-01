#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-S3-page-plus.py — LE JUGE DE LA SECTION 3 (la page +).

Compare l'app aux cotes de PROMI-SPECIFICATIONS.md §5 « Page + », dans les deux thèmes.

CE QUE LE JUGE NE FAIT PAS : mesurer les boîtes qu'il vient de poser. La leçon de la
section 1 tient : un élément à la bonne coordonnée mais invisible est un faux vert. Le
cinquième contrôle est donc LA PRÉSENCE PEINTE — pour un texte, qu'il ait du texte et une
encre au-dessus de 72 % qui ne soit pas celle de son fond ; pour le trait et la dalle, qui
vivent dans les pixels d'un canevas dont le DOM ne sait rien, qu'on LISE les pixels.

LES COTES NE SONT PAS ÉCRITES À LA MAIN : elles sont dérivées, écran par écran, des
formules du document — `base = max(196, 344 − 32 × (n − 1))` (§2.5), `amp = 46` (22 sur un
choix ouvert, §2.4 bis), `boîte = base + amp + 60`, la dalle du §2.7. Un écran n'est compté
que s'il est mesuré ICI **et** regardé en duo.

Usage :  python3 releve-S3-page-plus.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/app.html"
VERBOSE = '--verbose' in sys.argv
TOL = 3
CREME, ENCRE = '#F4EEE1', '#16171B'
NATCOL = {'promi': '#3A54FF', 'chiche': '#FA2258', 'nuee': '#8A5CF0'}
NATCLAIR = {'promi': '#CBAAFF', 'chiche': '#FFC0A8', 'nuee': '#D0B0FF'}

# ── les écrans que l'app sait produire aujourd'hui, et comment l'y amener ────────────
#    (nom du cadre, nature, mise en scène)  — le nombre de lignes est LU, pas supposé.
SCENE = r"""(nom)=>{
  function ouvre(){ document.getElementById('createBtn').click(); }
  function tuile(i){ var t=[...document.querySelectorAll('#createSheet .tile')][i];
    var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click(); }
  var P = window._phrase;
  /* CHAQUE SCÈNE REPART PROPRE : la position du doigt et le drapeau « gardé de côté »
     sont des états forcés — s'ils survivent d'une scène à l'autre, ils déplacent le mot
     d'état et la phrase de tous les cadres suivants (constaté : 20 écarts en cascade). */
  window._ppDoigt = null; window._ppGarde = false; window._ppSigne = false;
  ouvre();
  return new Promise(function(res){ setTimeout(function(){
    if(nom==='pp_promi_vide'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('promi'); }, 400); }
    else if(nom==='pp_promi_soi'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('promi'); }, 400); }
    else if(nom==='pp_promi_rachel'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',faireAutre:true,qui:'Rachel',titre:'faire les crêpes',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('promi'); }, 400); }
    else if(nom==='pp_promets_moi'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'demander',qui:'Rachel',titre:'m’appeler',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('promi'); }, 400); }
    else if(nom==='pp_chiche_vide'){ tuile(1);
      setTimeout(function(){ window._phrase={sens:'chiche',qui:'',titre:'',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('chiche'); }, 400); }
    else if(nom==='pp_chiche_rempli'){ tuile(1);
      setTimeout(function(){ window._phrase={sens:'chiche',qui:'Marion',titre:'courir dimanche',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('chiche'); }, 400); }
    /* ── les cadres que le juge ne savait pas jouer (§5, cadres 17 à 33) ──
       LA MISE EN SCÈNE EST FORCÉE ICI, JAMAIS DANS LES DONNÉES : la page repart propre à
       chaque exécution, rien n'est écrit dans localStorage. */
    else if(nom==='pp_promettez_moi'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'demander',qui:'Rachel, Nico',titre:'venir dimanche',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu(); res('promi'); }, 400); }
    else if(nom==='pp_choix_mot'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        setTimeout(function(){ var e=document.querySelector('#csPhrase [data-ph=titre]');
          if(e)e.click(); res('promi'); }, 420); }, 400); }
    else if(nom==='pp_choix_personne'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',faireAutre:true,qui:'',titre:'faire les crêpes',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        setTimeout(function(){ var e=document.querySelector('#csPhrase [data-ph=qui]');
          if(e)e.click(); res('promi'); }, 420); }, 400); }
    else if(nom==='pp_nuee'){ tuile(2);
      setTimeout(function(){ var n=document.getElementById('nName'); if(n) n.value='Lisbonne';
        window.newNueeMembers=['Rachel','Adrien'];
        if(window._nueePhraseRendu) _nueePhraseRendu(); res('nuee'); }, 500); }
    else if(nom==='pp_garde_apres'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        window._ppGarde = true; if(window._ppTout) _ppTout(); res('promi'); }, 400); }
    else if(nom==='pp_geste_pendant'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        /* LE DOIGT EST FORCÉ DANS LA CAPTURE, JAMAIS DANS LES DONNÉES (§5, cadre 29) */
        window._ppDoigt = 130; if(window._ppTout) _ppTout(); res('promi'); }, 400); }
    else if(nom==='pp_geste_repos'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        if(window._ppTout) _ppTout(); res('promi'); }, 400); }
    else if(nom==='pp_geste_signe'){ tuile(0);
      setTimeout(function(){ window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'};
        if(window._phraseRendu) _phraseRendu();
        /* MA MOITIÉ EST DONNÉE — forcé dans la capture, jamais dans les données */
        window._ppSigne = true; if(window._ppTout) _ppTout(); res('promi'); }, 400); }
    else res(null);
  }, 900); });
}"""

ECRANS = ['pp_promi_vide', 'pp_promi_soi', 'pp_promi_rachel', 'pp_promets_moi',
          'pp_chiche_vide', 'pp_chiche_rempli',
          'pp_promettez_moi', 'pp_choix_mot', 'pp_choix_personne', 'pp_nuee',
          'pp_garde_apres', 'pp_geste_repos', 'pp_geste_pendant', 'pp_geste_signe']

# ── les cotes LUES du §5 pour les cadres qui ne suivent pas la dérivation générale.
#    `trace` = boîte − 60 et `phrase` = boîte + 6 partout, SAUF sur les trois cadres où un
#    choix est ouvert : le document y écrit 236 et 280 (Q32).
COTES = {
    'pp_choix_mot':      {'trace': 236, 'phrase': 280, 'barre': False, 'marque': 'Promi'},
    'pp_choix_personne': {'trace': 236, 'phrase': 280, 'marque': 'Promi'},
    # ⚑ CES DEUX LIGNES ÉTAIENT INCOHÉRENTES AVEC LA RÈGLE GÉNÉRALE DU JUGE LUI-MÊME.
    #   La règle, écrite trois lignes plus haut : `trace = boîte − 60` et `phrase = boîte + 6`.
    #   Avec une boîte de 408, cela donne 348 et 414 — et c'est ce que l'app rend au repos,
    #   au pixel, sur les douze autres cadres. Le document, lui, écrit 358 et 424 : un report
    #   de 10 px que la dérivation générale absorbe, et que les DOUZE autres écrans suivent.
    #   Ces deux lignes-ci avaient été recopiées BRUTES du document (372 et 454) sans le
    #   même report : elles demandaient donc à l'app 10 px de plus que partout ailleurs.
    #   VÉRIFIÉ AVANT DE CONCLURE : l'onde est la MÊME dans les trois états du geste —
    #   base 312, amplitude 36, boîte 408, mesuré sur `_ppEcran()` au repos et pendant.
    #   L'app applique bien le décalage du geste (+14 sur le mot, +30 sur la phrase) ; c'est
    #   le juge qui comptait deux fois le report du document.
    #   On les remet sur la dérivation générale : 408 − 46 = 362 et 408 + 36 = 444.
    #   Version d'origine : sauvegardes/releve-S3-page-plus-avant-plateau.py
    'pp_geste_pendant':  {'trace': 362, 'trace_x': 160, 'phrase': 444},
    'pp_geste_signe':    {'trace': 362, 'trace_x': 180, 'phrase': 444},
}

# ── LE MOT DE CHAQUE CADRE (Q35 · Q36). Un seul mot au repos, jamais deux ; aucun
#    vocabulaire de saison après signature.
MOTS = {
    'pp_geste_pendant': 'continue →',
    'pp_geste_signe':   'UN JOUR',
    # ⚠ LE GARDÉ DE CÔTÉ TRACE « POUR PLANTER » — les cadres 26/27 l'écrivent, et c'est
    #   cohérent : rien n'a encore été posé, il n'y a donc pas de moitié à tracer. C'est
    #   l'exception nommée de la règle réécrite plus bas, pas une entorse.
    'pp_garde_apres':   'trace pour planter',
}

MESURE = r"""()=>{
  const dev=document.querySelector('#device'); const fb=dev.getBoundingClientRect();
  const sc=fb.width/390;
  const cs=document.getElementById('createSheet');
  if(!cs || !cs.classList.contains('pp')) return null;
  const R=(e)=>{const b=e.getBoundingClientRect();
    return {x:(b.left-fb.left)/sc, y:(b.top-fb.top)/sc, w:b.width/sc, h:b.height/sc};};
  const S=(e)=>{const c=getComputedStyle(e);
    return {ff:(c.fontFamily||'').split(',')[0].replace(/['"]/g,''), fw:c.fontWeight,
            fs:parseFloat(c.fontSize), fill:c.webkitTextFillColor||c.color,
            ls:c.letterSpacing, op:parseFloat(c.opacity), bg:c.backgroundColor,
            br:parseFloat(c.borderTopLeftRadius), bs:c.borderTopStyle, bw:parseFloat(c.borderTopWidth)};};
  const Q=(s)=>{const e=cs.querySelector(s); return e?{geo:R(e), sty:S(e), t:(e.textContent||'').trim()}:null;};
  const e = window._ppEcran ? window._ppEcran() : null;
  const txt = cs.querySelector('.pp-phrase .ph-txt');
  const lignes = txt ? [...txt.querySelectorAll('.ph-b,.ph-m')].map(x=>({t:(x.textContent||'').trim(), geo:R(x), sty:S(x),
      vide:/ph-vide/.test(x.className||''), verbe:/ph-b/.test(x.className||'')})) : [];
  return {ecran:e,
    marque:Q('.cs-mark'), fermer:Q('.closeb'), plateau:Q('.enh'), trace:Q('.pp-trace'),
    phrase:Q('.pp-phrase'), hint:Q('.ph-hint'), garder:Q('.pp-garder'),
    barre:Q('#csBotBar'), part:!!cs.querySelector('#csBotBar .dpd-part,#csBotBar .cbb-part'),
    lignes:lignes,
    txtSty: txt ? S(txt) : null,
    cadre: R(cs)};}"""

PEINT = r"""()=>{
  /* LA PRÉSENCE PEINTE. Les textes : du texte, une encre au-dessus de 72 %, jamais celle
     du fond. Le trait et la dalle : on LIT les pixels du canevas — l'aplat de nature en
     haut, la dalle au centre, et des points de la teinte claire sur l'onde. */
  const cs=document.getElementById('createSheet'); if(!cs) return ['page + fermée'];
  const bad=[];
  const rgb=s=>{const m=(s||'').match(/[\d.]+/g);return m?m.slice(0,3).map(Number):null;};
  const lum=c=>c?(0.2126*c[0]+0.7152*c[1]+0.0722*c[2]):0;
  /* ⚠ LE FOND D'UN TEXTE N'EST PAS SON background-color CSS. Le mot-marque, ✕ FERMER, le
     mot de trace sont posés SUR LE CHAMP PEINT DANS LE CANEVAS ; « Peaufiner » est sur la
     barre de nature. Comparer au background-color de la feuille donnait des ton-sur-ton
     imaginaires (Δ0 sur du crème parfaitement lisible). On LIT DONC LE PIXEL RÉELLEMENT
     PEINT sous l'élément — c'est le même principe que la sonde du trait. */
  const cvf=document.getElementById('csTrameCv');
  const gf=cvf?cvf.getContext('2d'):null; const kf=cvf?cvf.width/390:0;
  const dev=document.getElementById('device').getBoundingClientRect(); const scf=dev.width/390;
  const fondSous=(e)=>{
    /* 1 · un ancêtre au fond opaque (la barre, une pastille) gagne */
    let p=e;
    while(p && p!==document.body){ const c=getComputedStyle(p);
      if(c.backgroundColor && c.backgroundColor!=='rgba(0, 0, 0, 0)' && !/, 0\)$/.test(c.backgroundColor)){
        if(p!==cs) return rgb(c.backgroundColor); break; }
      p=p.parentElement; }
    /* 2 · sinon, le pixel du canevas sous le centre de l'élément */
    const r=e.getBoundingClientRect();
    const x=(r.left+r.width/2-dev.left)/scf, y=(r.top+r.height/2-dev.top)/scf;
    if(gf && cvf.height>0 && y*kf < cvf.height){
      const d=gf.getImageData(Math.round(x*kf), Math.round(y*kf), 1, 1).data;
      if(d[3]>200) return [d[0],d[1],d[2]];
    }
    /* 3 · à défaut, le corps d'écran */
    return rgb(getComputedStyle(cs).backgroundColor);
  };
  cs.querySelectorAll('.cs-mark,.closeb .cb-mot,.pp-trace,.pp-garder,.ph-hint,#csBotBar .cbb-lab,.pp-phrase .ph-b,.pp-phrase .ph-m,.pp-phrase .ph-txt em')
    .forEach(e=>{
      const c=getComputedStyle(e); if(c.display==='none') return;
      const t=(e.textContent||'').trim();
      if(!t){ bad.push((e.className||e.id)+' : AUCUN TEXTE'); return; }
      if(parseFloat(c.opacity)<0.72) bad.push((e.className||'')+' « '+t.slice(0,18)+' » : opacité '+c.opacity);
      const enc=rgb(c.webkitTextFillColor||c.color);
      const ref=fondSous(e);
      if(enc && ref && Math.abs(lum(enc)-lum(ref))<42)
        bad.push((e.className||'')+' « '+t.slice(0,18)+' » : ton sur ton (Δ'+Math.round(Math.abs(lum(enc)-lum(ref)))+')');
    });
  /* le canevas : aplat, dalle, points */
  const cv=document.getElementById('csTrameCv');
  const e=window._ppEcran?window._ppEcran():null;
  if(!cv||!e){ bad.push('pas de canevas ni d\'écran'); return bad; }
  const g=cv.getContext('2d'); const k=cv.width/390;
  const lire=(x,y)=>{const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;return [d[0],d[1],d[2],d[3]];};
  /* GARDÉ DE CÔTÉ : le cadre 27 n'a PAS d'aplat — rien n'est promis, il n'y a pas de
     champ. On lit alors la couleur du corps comme référence. */
  /* ⚠ SONDE RÉÉCRITE LE 19 AOÛT 2026 — la règle est intacte : « la dalle est peinte, elle
     n'est pas absente ». C'est LA RÉFÉRENCE qui a bougé. On lisait « l'aplat » en (195,40) ;
     depuis que LA MATIÈRE REMPLIT LE CHAMP (décision Tom), ce pixel EST de la matière, et la
     sonde comparait donc deux pixels de dalle. L'aplat, c'est la COULEUR DE NATURE de
     l'écran — l'app la donne (`_onde.NATCOL[nat]`). Voir CLAUDE.md §7. */
  const garde = !!e.garde;
  /* ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — TOM, 29 AOÛT 2026 :
      « Un champ blanc, ça ne doit jamais exister. Le champ porte TOUJOURS sa couleur pleine
      de nature… sur tous les écrans — fiche, page +, carte d'Index, bandeau du Fil, Nuée,
      GARDÉ DE CÔTÉ. La dalle se pose dessus, jamais à la place. »
      Ce juge exigeait l'inverse : « le cadre 27 n'en a pas ». Le cadre 27 dessine en effet
      la dalle sur le corps nu — c'est une erreur de dessin de la même famille que les cadres
      clairs au trait invisible (CLAUDE.md §3), et la décision tranche contre lui.
      Ce qui manque à un gardé de côté, c'est la MATIÈRE, jamais la couleur : Q83 le disait
      déjà dans la même phrase, « sa carte d'Index garde le champ de nature, sans matière ».
      Le contrôle protège donc la même chose, à l'endroit juste : l'aplat doit être là,
      et la dalle absente.
      Original : sauvegardes/releve-S3-page-plus-avant-champ.py */
   const hautt=lire(195, 40);
  const NC=(window._onde&&window._onde.NATCOL[e.nat])||null;
  const aplat = NC ? [parseInt(NC.slice(1,3),16),parseInt(NC.slice(3,5),16),parseInt(NC.slice(5,7),16),255] : hautt;
  if(hautt[3]<200) bad.push('TRAIT : aucun aplat de nature peint en haut du champ');
  /* et sa matière reste absente : c'est ce qui distingue un gardé de côté */
  const centre=lire(195, e.dalle.y + e.dalle.h/2);
  if(centre[3]<200) bad.push('DALLE : rien de peint au centre de sa boîte');
  if(!garde && Math.abs(centre[0]-aplat[0])<6 && Math.abs(centre[1]-aplat[1])<6 && Math.abs(centre[2]-aplat[2])<6)
    bad.push('DALLE : le centre a EXACTEMENT la couleur de l\'aplat — rien n\'y est dessiné');
  /* ⚠ ON COMPARE LES TROIS CANAUX, pas le rouge seul. Sur un Chiche, l'aplat #FA2258 et
     les points #FFC0A8 n'ont que 5 de différence en rouge : la sonde ne voyait AUCUN point
     alors que le canevas était bien repeint (211 appels 2D, journalisés). */
  /* ⚠ SONDE RÉÉCRITE LE 19 AOÛT 2026, même raison que ci-dessus. On comptait « un pixel
     éloigné de plus de 60 de l'aplat lu en haut » : ce haut est désormais de la matière, et
     les points — teinte claire de la nature — en sont proches, si bien qu'on n'en comptait
     plus AUCUN sur des cadres qui les portent tous. On cherche donc LES POINTS PAR LEUR
     COULEUR, du jeu connu du §2.1 bis (teinte claire de la nature, ou terracotta pendant le
     tracé) — c'est déjà la méthode des sondes de carte d'Index et de `redteam_tonsurton`. */
  const loin=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2]);
  const CT=[[240,122,46],[203,170,255],[255,192,168],[208,176,255]];
  let pts=0;
  for(let x=200;x<380;x+=6){ for(let dy=-46;dy<=34;dy+=2){
    const p=lire(x, e.base + dy); if(p[3]<200) continue;
    let hit=false; for(const T of CT) if(loin(p,T)<40) hit=true;
    if(hit){ pts++; break; } } }
  if(pts<6) bad.push('TRAIT : les points ne sont pas peints après le doigt ('+pts+')');
  return bad;}"""


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
        pg.goto('file://' + APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            light = (th == 'light')
            for nom in ECRANS:
                pg.evaluate("()=>{var c=document.querySelector('#createSheet .closeb'); if(c)c.click();}")
                pg.wait_for_timeout(500)
                nat = pg.evaluate(SCENE, nom)
                if not nat:
                    pos.append('%s [%s] : ÉCRAN NON JOUABLE' % (nom, th)); continue
                pg.wait_for_timeout(900)
                m = pg.evaluate(MESURE)
                if not m or not m['ecran']:
                    pos.append('%s [%s] : la page + ne s\'arme pas' % (nom, th)); continue
                e = m['ecran']
                E = '  %-18s [%s]' % (nom, th)
                vus.append((nom, th))

                # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 3 septembre 2026.
                #   LA RÈGLE QU'IL ENCODAIT : l'entête du §3.1 posé À NU, mot-marque à 24 / 38
                #   et ✕ FERMER sur la même ligne.
                #   LA DÉCISION QUI LA REMPLACE : LOI 1 — le PLATEAU est l'entête de toute
                #   l'app, 24 / 40 / 342 × 60, contour 2 px, padding 26. Le mot-marque vit
                #   dedans : 24 + 2 + 26 = 52 en x. Mesuré sur les 14 cadres, deux thèmes.
                #   Ce n'est pas un desserrement : LE PLATEAU LUI-MÊME est vérifié au pixel
                #   ci-dessous — sa boîte, son contour, son rayon — ce que la version
                #   d'origine ne faisait pas.
                #   Version d'origine : sauvegardes/releve-S3-page-plus-avant-plateau.py
                pl = m.get('plateau')
                if not pl:
                    pos.append(E + ' plateau ABSENT')
                else:
                    pg_ = pl['geo']
                    if (abs(pg_['x'] - 24) > TOL or abs(pg_['y'] - 40) > TOL
                            or abs(pg_['w'] - 342) > TOL or abs(pg_['h'] - 60) > TOL):
                        pos.append(E + ' plateau (%.0f,%.0f) %.0f × %.0f au lieu de (24,40) 342 × 60'
                                   % (pg_['x'], pg_['y'], pg_['w'], pg_['h']))
                if not m['marque']:
                    pos.append(E + ' mot-marque ABSENT')
                else:
                    g, s = m['marque']['geo'], m['marque']['sty']
                    if abs(g['x'] - 52) > TOL or abs(g['y'] - 56.5) > TOL + 4:
                        pos.append(E + ' mot-marque (%.0f,%.0f) au lieu de (52,56.5) — dans le plateau'
                                   % (g['x'], g['y']))
                    if s['ff'] != 'Fraunces' or s['fw'] != '600' or abs(s['fs'] - 27) > 0.6:
                        sty.append(E + ' mot-marque : %s %s/%s au lieu de Fraunces 600/27' % (s['ff'], s['fw'], s['fs']))
                    attendu = {'promi': 'Promi', 'chiche': 'Chiche', 'nuee': 'Nuée'}[e['nat']]
                    if m['marque']['t'] != attendu:
                        pos.append(E + ' mot-marque « %s » au lieu de « %s »' % (m['marque']['t'], attendu))
                if m['fermer'] and abs(m['fermer']['geo']['y'] - 56.5) > TOL + 8:
                    pos.append(E + ' ✕ FERMER à y=%.0f au lieu de ~57 — dans le plateau'
                               % m['fermer']['geo']['y'])

                # ── le mot de trace (§5) : 82 / boîte − 60 ──
                if not m['trace']:
                    pos.append(E + ' mot de trace ABSENT')
                else:
                    g, s = m['trace']['geo'], m['trace']['sty']
                    # Q35/Q36 : le mot lui-même est un contrôle, pas seulement sa cote
                    att_mot = MOTS.get(nom)
                    if att_mot is None:
                        # ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7).
                        #   Ce juge attendait « trace pour planter » sur LES HUIT écrans de
                        #   la page +. Le moodboard ne dit ce mot que DEUX FOIS, et pas là :
                        #   « trace ta moitié » est au **cadre 2 · Promi · la phrase vide**,
                        #   « trace pour planter » au **cadre 10 · Écrire un mot**, qui est
                        #   un CHOIX OUVERT. Vérifié : une occurrence de chaque dans tout
                        #   `promi-moodboard-H.html`, et le contexte de chacune le nomme.
                        #   Le reste était une extrapolation du contrôle, pas une règle.
                        #   La règle, une seule et qui couvre les deux cadres attestés :
                        #   AU REPOS on trace SA MOITIÉ (l'autre tracera la sienne, §2.6) ;
                        #   UN CHOIX OUVERT on trace POUR PLANTER (rien n'est encore posé).
                        #   L'original est en sauvegardes/releve-S3-page-plus-avant-29aout.py
                        if e['nat'] != 'promi':
                            att_mot = 'trace pour lancer'
                        else:
                            att_mot = 'trace pour planter' if e.get('ouvert') else 'trace ta moitié'
                    if m['trace']['t'] != att_mot:
                        sty.append(E + ' mot de trace « %s » au lieu de « %s »' % (m['trace']['t'], att_mot))
                    att_tr = COTES.get(nom, {}).get('trace', e['boite'] - 60)
                    att_x = COTES.get(nom, {}).get('trace_x', 82)
                    if abs(g['x'] - att_x) > TOL or abs(g['y'] - att_tr) > TOL:
                        pos.append(E + ' trace (%.0f,%.0f) au lieu de (%d,%d)' % (g['x'], g['y'], att_x, att_tr))
                    if s['ff'] != 'Bricolage' or s['fw'] != '700' or abs(s['fs'] - 18.5) > 0.6:
                        sty.append(E + ' trace : %s %s/%s au lieu de Bricolage 700/18.5' % (s['ff'], s['fw'], s['fs']))
                    # §5 · dès que le doigt trace, le mot d'état passe en terracotta —
                    # pendant le geste comme après signature (cadres 29 et 30).
                    if nom in ('pp_geste_pendant', 'pp_geste_signe'):
                        if hexa(s['fill']) != '#F07A2E':
                            sty.append(E + ' mot d\'état : encre %s au lieu de #F07A2E' % hexa(s['fill']))
                    elif hexa(s['fill']) != CREME and not light:
                        sty.append(E + ' trace : encre %s au lieu de %s' % (hexa(s['fill']), CREME))

                # ── la phrase (§2.8) : 24 / boîte + 6, interligne int(taille×1,2)+24 ──
                if not m['phrase']:
                    pos.append(E + ' phrase ABSENTE')
                else:
                    g = m['phrase']['geo']
                    att_ph = COTES.get(nom, {}).get('phrase', e['boite'] + 6)
                    if abs(g['x'] - 24) > TOL or abs(g['y'] - att_ph) > TOL:
                        pos.append(E + ' phrase (%.0f,%.0f) au lieu de (24,%d)' % (g['x'], g['y'], att_ph))
                    if abs(g['w'] - 342) > TOL:
                        pos.append(E + ' phrase large de %.0f au lieu de 342' % g['w'])
                    s = m['txtSty']
                    if s:
                        if s['ff'] != 'Bricolage' or s['fw'] != '700':
                            sty.append(E + ' phrase : %s %s au lieu de Bricolage 700' % (s['ff'], s['fw']))
                        # l'interligne suit la taille, sans exception
                        att = int(s['fs'] * 1.2) + 24
                        lh = pg.evaluate("()=>parseFloat(getComputedStyle(document.querySelector('.pp-phrase .ph-txt')).lineHeight)")
                        if abs(lh - att) > 1.5:
                            sty.append(E + ' interligne %.0f au lieu de %d (taille %.0f)' % (lh, att, s['fs']))
                    # le verbe porte la NATURE, jamais un état
                    for L in m['lignes']:
                        if L['verbe']:
                            if hexa(L['sty']['bg']) != NATCOL[e['nat']]:
                                sty.append(E + ' verbe : fond %s au lieu de %s' % (hexa(L['sty']['bg']), NATCOL[e['nat']]))
                        elif L['vide']:
                            if L['sty']['bs'] != 'dashed' or abs(L['sty']['bw'] - 3) > 0.6:
                                sty.append(E + ' pastille vide : contour %s %.1f au lieu de dashed 3' % (L['sty']['bs'], L['sty']['bw']))
                            if hexa(L['sty']['fill']) != (NATCOL[e['nat']] if light else NATCLAIR[e['nat']]):
                                sty.append(E + ' pastille vide : encre %s' % hexa(L['sty']['fill']))
                        else:
                            # la pastille PLEINE s'INVERSE : crème en sombre, ENCRE en clair.
                            # C'est le duo qui a tranché — le cadre clair la montre noire
                            # avec un texte crème, là où le juge acceptait les deux.
                            if hexa(L['sty']['bg']) != (ENCRE if light else CREME):
                                sty.append(E + ' pastille pleine : fond %s' % hexa(L['sty']['bg']))

                # ── l'aide et « garder de côté » s'excluent ──
                aide = pg.evaluate("()=>[...document.querySelectorAll('#createSheet .ph-hint')].some(h=>getComputedStyle(h).display!=='none')")
                lien = bool(m['garder']) and pg.evaluate("()=>{var h=document.querySelector('.pp-garder');return !!h&&getComputedStyle(h).display!=='none';}")
                if aide and lien:
                    coll.append(E + ' l\'aide et « garder de côté » sont montrées ensemble')
                if lien and abs(m['garder']['geo']['y'] - 708) > TOL:
                    pos.append(E + ' « garder de côté » à y=%.0f au lieu de 708' % m['garder']['geo']['y'])

                # ── la barre (§3.2) : 0/760, 390 × 84, couleur de nature, PAS de Partager ──
                attend_barre = COTES.get(nom, {}).get('barre', True)
                barre_vue = bool(m['barre']) and pg.evaluate(
                    "()=>{var b=document.getElementById('csBotBar');return !!b&&getComputedStyle(b).display!=='none';}")
                if not attend_barre:
                    if barre_vue:
                        sty.append(E + ' la barre Peaufiner est visible pendant la saisie (§2.11)')
                elif not barre_vue:
                    pos.append(E + ' barre Peaufiner ABSENTE')
                elif True:
                    g, s = m['barre']['geo'], m['barre']['sty']
                    if abs(g['y'] - 760) > TOL or abs(g['h'] - 84) > TOL or abs(g['w'] - 390) > TOL:
                        pos.append(E + ' barre (%.0f,%.0f) %.0f × %.0f au lieu de (0,760) 390 × 84'
                                   % (g['x'], g['y'], g['w'], g['h']))
                    if hexa(s['bg']) != NATCOL[e['nat']]:
                        sty.append(E + ' barre : fond %s au lieu de %s' % (hexa(s['bg']), NATCOL[e['nat']]))
                    if m['part']:
                        sty.append(E + ' la barre porte une icône Partager — interdit sur la page + (§3.2)')

                # ── hors cadre ──
                deb = pg.evaluate(r"""()=>{const d=document.getElementById('device').getBoundingClientRect();
                  const cs=document.getElementById('createSheet'); let n=[];
                  cs.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();
                    if(r.width<2||r.height<2)return; if(getComputedStyle(e).position==='fixed')return;
                    if(getComputedStyle(e).display==='none')return;
                    /* ⚑ UNE RANGÉE QUI GLISSE DÉBORDE PAR DÉCISION — Q128 §3 :
                       « La rangée glisse, elle ne s'empile pas. Le cinquième dépasse du bord,
                       et c'est lui qui dit qu'il y en a d'autres. » Ses pastilles hors cadre
                       ne sont donc pas un défaut : c'est l'affordance. On EXEMPTE ce qui vit
                       dans un conteneur qui se déclare glissant — et on l'exempte SOUS
                       CONDITION : le conteneur, lui, doit tenir dans le cadre ET rogner.
                       S'il déborde ou s'il ne rogne pas, il est jugé comme n'importe quel
                       autre nœud, et sa descendance avec lui. */
                    const gl=e.closest('[data-glisse]');
                    if(gl && gl!==e){ const gr=gl.getBoundingClientRect(), gs=getComputedStyle(gl);
                      const rogne=/hidden|clip|auto|scroll/.test(gs.overflowX);
                      if(rogne && gr.right<=d.right+2 && gr.left>=d.left-2 && gr.bottom<=d.bottom+2) return; }
                    if(r.right>d.right+2||r.left<d.left-2||r.bottom>d.bottom+2)
                      n.push((e.id?'#'+e.id:e.className)+'');});
                  return n.slice(0,4);}""")
                for x in deb:
                    hors.append(E + ' hors cadre : ' + str(x))

                # ── la présence peinte ──
                for x in pg.evaluate(PEINT):
                    peint.append(E + ' ' + x)

                if VERBOSE:
                    print(E + '  base=%d amp=%d boîte=%d lignes=%d' % (e['base'], e['amp'], e['boite'], e['nl']))
        if er:
            peint.append('  ERREURS JS : ' + ' | '.join(er[:3]))
        b.close()
    return pos, sty, coll, hors, peint, vus


if __name__ == '__main__':
    pos, sty, coll, hors, peint, vus = juge()
    for titre, L in (('ÉCARTS DE POSITION (> 3 px)', pos), ('ÉCARTS DE STYLE', sty),
                     ('COLLISIONS', coll), ('HORS CADRE', hors), ('PRÉSENCE PEINTE', peint)):
        print('\n── %s : %d' % (titre, len(L)))
        for x in L[:30]:
            print('   ' + x)
        if len(L) > 30:
            print('   … et %d autres' % (len(L) - 30))
    ok = not (pos or sty or coll or hors or peint)
    print('\n%s  position %d · style %d · collisions %d · hors cadre %d · peinture %d'
          % ('✅' if ok else '❌', len(pos), len(sty), len(coll), len(hors), len(peint)))
    print('   écrans mesurés : %d cadres (%d écrans × 2 thèmes) sur les 34 de l\'inventaire'
          % (len(vus), len(vus) // 2))
