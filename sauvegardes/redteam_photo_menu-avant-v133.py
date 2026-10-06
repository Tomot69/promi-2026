#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_photo_menu.py — LE BOUTON PHOTO D'UNE FICHE PROPOSE DEUX CHOSES (v117, Tom, 1er oct. 2026).

« Sur chaque fiche, le bouton photo doit proposer deux choses : importer une image — le menu du téléphone s'ouvre — ou
remettre la dalle telle qu'elle était à sa création, dans son monde, sa forme et sa couleur d'origine. Par défaut, rien ne
change : la dalle suit le monde et la palette en cours. C'est une option, et elle vaut aussi pour le partage. »

Au doigt (`touchscreen.tap`, WebKit et Chromium), Studio réglé sur un AUTRE monde et une AUTRE palette que la plantation :
  A · toucher le bouton photo d'une fiche ouvre un menu : « Importer une image » et « La dalle d'origine »
  B · « Importer une image » ouvre le sélecteur de fichiers du système (évènement filechooser), dans le geste
  C · PAR DÉFAUT la dalle suit le Studio : un rendu sans monde demandé = le rendu dans le monde du Studio, ≠ plantation
  D · « La dalle d'origine » : le même rendu = celui du monde de plantation (pixels, horloge figée), ≠ Studio ;
      la fiche est REPEINTE (sa matière change) ; l'option est sauvegardée ; le libellé devient « La dalle du Studio »
  E · le partage suit : la planche de Mon Folio réduit à cette parole change avec l'option
  F · la page + garde son geste : toucher le bouton photo ouvre directement le sélecteur, sans menu
Preuve (§7) : copier `sauvegardes/app-avant-v117b.html` À LA RACINE, puis
`APP=http://127.0.0.1:8752/<copie>.html python3 redteam_photo_menu.py` doit ROUGIR (6/8).
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
MOTS = ['Importer une image', 'La dalle d’origine']      # v118 (Tom, Q366 tranchée) : les quatre mots sont décidés
SEUIL = 2.0               # niveaux : en dessous, deux rendus sont « le même » (horloge figée) ; au-dessus, différents
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-64s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-64s KO  %s' % (nom, detail))


# trois rendus de la même dalle, horloge figée : sans monde demandé (le chemin des écrans), monde du Studio, monde de plantation
RENDUS = r"""(id)=>{ const pn=performance.now.bind(performance); performance.now=()=>4242; const R=Math.random; let s=7; Math.random=()=>{s=(s*16807)%2147483647; return s/2147483647;};
  const p=promises.find(p=>p.id===id);
  function px(monde, avec){ const c=document.createElement('canvas'); s=7; const okk=avec?Toile.dalleTrame(c,id,2,monde):Toile.dalleTrame(c,id,2);
    if(!okk||!c.width) return null; const w=64,h=64,d=document.createElement('canvas'); d.width=w; d.height=h; d.getContext('2d').drawImage(c,0,0,w,h);
    return Array.from(d.getContext('2d').getImageData(0,0,w,h).data); }
  const r={nu:px(null,false), studio:px(Toile.mondeCourant(),true), plant:px(p.monde,true)};
  performance.now=pn; Math.random=R; return r; }"""

FICHE = r"""()=>{ const cv=document.getElementById('dpTrameCv'); if(!cv) return null; const w=48,h=96,d=document.createElement('canvas'); d.width=w; d.height=h;
  d.getContext('2d').drawImage(cv,0,0,w,h); return Array.from(d.getContext('2d').getImageData(0,0,w,h).data); }"""

PLANCHE = r"""(id)=>{ openShare(); document.querySelector('#shMode button[data-mode=mosaic]').click();
  const h={}; promises.forEach(p=>{ if(p.id!==id) h[p.id]=true; }); Object.keys(NUE).forEach(k=>h['n:'+k]=true);
  const av=[shareHidden, window.shPelote]; shareHidden=h; window.shPelote=false;
  const pn=performance.now.bind(performance); performance.now=()=>4242; shareRender(); performance.now=pn;
  const cv=document.getElementById('shCanvas'); const w=48,hh=96,d=document.createElement('canvas'); d.width=w; d.height=hh;
  d.getContext('2d').drawImage(cv,0,0,w,hh); const out=Array.from(d.getContext('2d').getImageData(0,0,w,hh).data);
  shareHidden=av[0]; window.shPelote=av[1]; const c=document.querySelector('#shareScreen .closeb'); if(c) c.click(); return out; }"""


def ecart(a, b):
    if not a or not b or len(a) != len(b): return 999.0
    return sum(abs(a[i] - b[i]) for i in range(len(a))) / len(a)


def menu(pg):
    return pg.evaluate("()=>{const m=document.querySelector('.ph-photo-menu'); if(!m) return null; const r=m.getBoundingClientRect();"
                       " return {mots:[...m.querySelectorAll('button')].map(b=>b.textContent), vis:r.width>0&&r.height>0}}")


def tape(pg, sel):
    bb = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width?{x:r.x+r.width/2,y:r.y+r.height/2}:null}", sel)
    if not bb: return False
    pg.touchscreen.tap(bb['x'], bb['y']); pg.wait_for_timeout(700); return True


def passe(b, moteur):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.wait_for_timeout(800)
    tag = '[%s]' % moteur
    pid = pg.evaluate("()=>{const p=promises.find(p=>!p.draft&&!p.req&&!p.nuee&&!p.photo&&p.monde&&p.monde.m); return p?p.id:null}")
    # le Studio sur un AUTRE monde et une AUTRE palette que la plantation
    pg.evaluate("""(id)=>{const p=promises.find(p=>p.id===id); const autres=['pixel','braille','mosaique','touffe','encre'].filter(m=>m!==p.monde.m);
        Toile.setTheme(autres[0]); try{Toile.setPalette(p.monde.p==='irascible'?'allegre':'irascible');}catch(e){} }""", pid)
    pg.wait_for_timeout(1200)
    R = pg.evaluate(RENDUS, pid)
    t(tag + ' C · par défaut la dalle suit le Studio', ecart(R['nu'], R['studio']) <= SEUIL < ecart(R['nu'], R['plant']),
      'nu↔Studio %.2f · nu↔plantation %.2f' % (ecart(R['nu'], R['studio']), ecart(R['nu'], R['plant'])))
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
    pg.evaluate("(i)=>openDetail(i)", pid); pg.wait_for_timeout(2200)
    tape(pg, '#detailPoster .ph-photo-btn')
    m = menu(pg)
    # ⚑ v132 (Tom, C-042) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_photo_menu-avant-v132.py) : « Dessiner » est en tête du menu, sur la
    #   fiche ET sur la page + (v128 ③, construit en v132) ; les deux choix de v117 suivent, dans le même ordre.
    t(tag + ' A · le bouton photo d\'une fiche ouvre son menu : « Dessiner » en tête, puis les deux choix', bool(m) and m['vis'] and m['mots'] == ['Dessiner'] + MOTS, str(m))
    if m:
        try:
            with pg.expect_file_chooser(timeout=2500) as fc:
                tape(pg, '.ph-photo-menu button:nth-child(2)')
            t(tag + ' B · « Importer une image » ouvre le sélecteur du système', fc.value is not None)
        except Exception as e:
            t(tag + ' B · « Importer une image » ouvre le sélecteur du système', False, str(e)[:120])
        pg.evaluate("()=>{const pn=performance.now.bind(performance); window.__pn=pn; performance.now=()=>4242;}")
        F0 = pg.evaluate(FICHE)
        pg.evaluate("()=>{performance.now=window.__pn;}")
        tape(pg, '#detailPoster .ph-photo-btn')
        tape(pg, '.ph-photo-menu button:nth-child(3)')
        pg.wait_for_timeout(1500)
        etat = pg.evaluate("(id)=>{const p=promises.find(p=>p.id===id); let s=null; try{s=JSON.parse(localStorage.getItem('promi_state')).promises.find(q=>q.id===id).dalleOrigine}catch(e){} return {o:!!p.dalleOrigine, s:s}}", pid)
        pg.evaluate("()=>{performance.now=()=>4242;}")
        pg.evaluate("()=>{try{window._ficheDalle&&_ficheDalle();}catch(e){}}"); pg.wait_for_timeout(300)
        F1 = pg.evaluate(FICHE)
        pg.evaluate("()=>{performance.now=window.__pn;}")
        R2 = pg.evaluate(RENDUS, pid)
        t(tag + ' D · « La dalle d\'origine » : rendu = monde de plantation',
          etat['o'] and ecart(R2['nu'], R2['plant']) <= SEUIL < ecart(R2['nu'], R2['studio']),
          'option %s · nu↔plantation %.2f · nu↔Studio %.2f' % (etat['o'], ecart(R2['nu'], R2['plant']), ecart(R2['nu'], R2['studio'])))
        t(tag + ' D · la fiche est repeinte, l\'option sauvegardée', ecart(F0, F1) > SEUIL and etat['s'] is True,
          'matière de la fiche %.2f niveaux · sauvegardé %s' % (ecart(F0, F1), etat['s']))
        tape(pg, '#detailPoster .ph-photo-btn'); m2 = menu(pg)
        t(tag + ' D · le libellé devient « La dalle du Studio »', bool(m2) and 'La dalle du Studio' in m2['mots'], str(m2))
        pg.evaluate("()=>{window._photoMenuFerme&&_photoMenuFerme();}")
        P1 = pg.evaluate(PLANCHE, pid); pg.wait_for_timeout(600)
        pg.evaluate("(id)=>{promises.find(p=>p.id===id).dalleOrigine=false;}", pid)
        P0 = pg.evaluate(PLANCHE, pid); pg.wait_for_timeout(600)
        t(tag + ' E · le partage suit l\'option', ecart(P0, P1) > SEUIL, 'planche avec ↔ sans %.2f niveaux' % ecart(P0, P1))
    # F · la page + : import direct
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{const t=document.querySelector('#createSheet .tile[data-kind=promi]'); if(t) t.click();}"); pg.wait_for_timeout(1500)
    # v132 : la page + ouvre le même menu — « Dessiner », puis « Importer une image », qui ouvre le sélecteur
    tape(pg, '#createSheet .ph-photo-btn'); mp = menu(pg)
    t(tag + ' F · page + : le bouton ouvre le menu, « Dessiner » en tête puis « Importer une image »', bool(mp) and mp['mots'][:2] == ['Dessiner', 'Importer une image'], str(mp))
    try:
        with pg.expect_file_chooser(timeout=2500) as fc:
            tape(pg, '.ph-photo-menu button:nth-child(2)')
        t(tag + ' F · page + : « Importer une image » ouvre le sélecteur', fc.value is not None)
    except Exception as e:
        t(tag + ' F · page + : « Importer une image » ouvre le sélecteur', False, str(e)[:120])
    t(tag + ' aucune erreur JS', not er, '; '.join(er)[:200])
    ctx.close()


with sync_playwright() as p:
    for moteur in ('webkit', 'chromium'):
        b = getattr(p, moteur).launch(); passe(b, moteur); b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ', '.join(ko)); sys.exit(1)
print('✅ le bouton photo propose ses deux choix, et la dalle d\'origine se tient partout')
