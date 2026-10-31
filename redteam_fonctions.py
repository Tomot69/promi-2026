#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_fonctions.py — L'INVENTAIRE DES FONCTIONS.

Ce que le produit SAIT FAIRE. Aucune refonte, aucun portage, aucun « écran écrit depuis son
inventaire » n'a le droit de faire disparaître une de ces lignes. C'est arrivé : la section 4
a remplacé le contenu du Fil et a emporté TENIR et REPORTER — le seul endroit d'où l'on
tient une parole sans ouvrir une fiche. Aucune batterie ne l'a vu, parce qu'aucune ne savait
que cette fonction existait.

Chaque ligne dit : le geste, et ce qui doit en résulter DANS LA DONNÉE.

Usage :  python3 redteam_fonctions.py [--verbose]
"""
import sys, re
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-58s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-58s KO  %s' % (nom, detail))


def trace(pg, sel):
    r = pg.evaluate("""(s)=>{const e=document.querySelector(s);if(!e)return null;
      const b=e.getBoundingClientRect();
      if(b.width<10||b.height<10) return null;
      return {x:b.left,y:b.top,w:b.width,h:b.height};}""", sel)
    if not r: return False
    y = r['y'] + r['h'] / 2
    pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
    for i in range(1, 26):
        pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
    pg.mouse.up(); pg.wait_for_timeout(1300)
    return True


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def raz(): pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(700)

    # ── 1 · PLANTER ─────────────────────────────────────────────────────────────────
    print('\n── planter ──')
    raz(); n0 = pg.evaluate("()=>promises.length")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1000)
    t('le + ouvre la page de création', pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"))
    # une parole sans mot ne se plante pas (`promiRequis`) : on donne d'abord un titre.
    pg.evaluate("""()=>{const f=document.getElementById('fTitle'); if(f){f.value='aller voir la mer';
      f.dispatchEvent(new Event('input',{bubbles:true}));}
      if(window._phrase){window._phrase.titre='aller voir la mer';
        if(window._phraseRendu)_phraseRendu();}}"""); pg.wait_for_timeout(600)
    trace(pg, '#planterCv')
    t('on plante un Promi au geste', pg.evaluate("()=>promises.length") > n0,
      '%d → %d' % (n0, pg.evaluate("()=>promises.length")))
    raz(); n0 = pg.evaluate("()=>promises.length")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1000)
    # ⚠ ON ACTIONNE LA BASCULE AVANT DE MESURER. Le bouton « planter » n'existe pas au
    #   repos — et c'est voulu : au repos on TRACE. C'est `#planterAlt` qui bascule du
    #   trait vers le bouton, et c'est ce que `redteam_verbe` actionne (6/6). Mon contrôle
    #   exigeait le bouton sans toucher la bascule : il visait le mauvais état, et les deux
    #   batteries semblaient se contredire. Aucune des deux n'avait tort sur la fonction.
    pg.evaluate("()=>{const a=document.getElementById('planterAlt');if(a)a.click();}")
    pg.wait_for_timeout(700)
    t('la bascule mène à un vrai bouton « planter »', pg.evaluate("""()=>{
      const b=document.getElementById('addPromi'); if(!b) return false;
      const c=getComputedStyle(b), r=b.getBoundingClientRect();
      return c.display!=='none' && r.width>20 && r.height>10;}"""),
      pg.evaluate("""()=>{const b=document.getElementById('addPromi');if(!b)return 'ABSENT';
        const r=b.getBoundingClientRect();return getComputedStyle(b).display+' '+Math.round(r.width)+'×'+Math.round(r.height);}"""))

    # ── 2 · TENIR ───────────────────────────────────────────────────────────────────
    print('\n── tenir sa parole ──')
    # état propre : la section précédente a planté et basculé la page +. Un geste se trace
    # sur une page qui n'a rien en travers.
    pg.reload(); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    raz()
    # on force une parole à tenir, ordinaire : ni Chiche, ni brouillon, ni demande — la
    # section précédente vient d'en planter une, et le premier « rate » venu pouvait être
    # d'une nature qui ne porte pas le geste.
    pid = pg.evaluate("""()=>{const p=promises.filter(x=>!x.draft&&!x.req&&!x.chiche)[0];
      if(p){p.status='encours'; p.due=-1;} return p?p.id:null;}""")
    # la fiche doit être REDESSINÉE après qu'on a changé le statut : `cur` porte l'ancien.
    pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(900)
    t('le geste est à l\'écran sur une fiche à tenir', pg.evaluate("""()=>{
      const z=document.getElementById('tenirCv'); if(!z) return false;
      const c=getComputedStyle(z), r=z.getBoundingClientRect();
      return c.display!=='none' && c.pointerEvents!=='none' && r.width>40 && r.height>40;}"""))
    trace(pg, '#tenirCv')
    t('on tient sa parole au geste, depuis la fiche',
      pg.evaluate("(i)=>promises.find(p=>p.id===i).status", pid) == 'tenu')

    print('\n── le FIL : TRACER mène à la fiche, rien ne s\'y tient ──')
    # ⚑ v163b (25 oct. 2026, C-189 — audit 15, point 1) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7).
    #   La règle encodée depuis le 20 août (Q75) : « le Fil est le seul endroit d'où l'on tient une parole sans ouvrir une fiche ».
    #   LA DÉCISION QUI LA REMPLACE (brief v163, §8) : « supprimer TENIR du Fil — une parole ne se tient que par le trait ». Le geste
    #   du Fil reste (l'appui maintenu déplie la rangée, le repos est celui du cadre 76), mais son acte fort est TRACER, qui ouvre la
    #   fiche, et RIEN dans le Fil n'écrit « tenu ». Même intention (le geste agit sur un bandeau DÉSIGNÉ, l'état lu avant et après).
    #   Version d'avant : sauvegardes/redteam_fonctions-avant-v163b.py
    raz()
    # ⚑ v173 (C-210) : TRACER · REPORTER sont portés par une parole en cours dont la date est passée
    pg.evaluate("""()=>{ const ids=new Set((typeof FEED!=='undefined'?FEED:[]).map(f=>f.pid)); const p=promises.filter(x=>ids.has(x.id)&&!x.draft&&!x.req&&!x.chiche&&x.status==='encours')[0]; if(p){ p.due=-1; delete p.ech; } if(typeof buildFeed==='function') buildFeed(); }""")
    pg.evaluate("()=>{setView('fil');}"); pg.wait_for_timeout(1900)

    t('le Fil au repos est celui du cadre 76 — aucune rangée',
      pg.evaluate("""()=>[...document.querySelectorAll('#feedList .s4-actes,#feedList .s4-acte')]
        .filter(e=>e.getBoundingClientRect().width>4).length === 0"""),
      '%s rangée(s) au repos' % pg.evaluate("()=>document.querySelectorAll('#feedList .s4-actes').length"))

    cible = pg.evaluate("""()=>{const C=window._filComp||[];
      for(const F of C){ if(!F.actes.some(a=>a.quoi==='tracer')||!F.actes.some(a=>a.quoi==='post')) continue;   /* v173 (C-210) : une parole dont la date est passée */
        const p=promises.find(q=>q.id===F.pid); if(!p||p.draft||p.status==='tenu') continue;
        return {i:F.rang, pid:F.pid, titre:p.title, statut:p.status||''}; }
      return null;}""")
    t('le Fil sait quel bandeau porte « TRACER »', bool(cible), str(cible))
    t('aucun bandeau du Fil ne porte plus « TENIR » ni de réaction',
      pg.evaluate("()=>!(window._filComp||[]).some(F=>F.actes.some(a=>a.quoi==='keep'||a.quoi==='react'))"), '')

    r = None
    if cible:
        r = pg.evaluate("""(i)=>{const c=[...document.querySelectorAll('#feedList .s4-carte')][i];
          if(!c) return null; c.scrollIntoView({block:'center'}); const b=c.getBoundingClientRect(); return {x:b.left+40,y:b.top+b.height/2};}""",
          cible['i'])
    if r:
        pg.wait_for_timeout(500)
        r = pg.evaluate("""(i)=>{const c=[...document.querySelectorAll('#feedList .s4-carte')][i]; const b=c.getBoundingClientRect(); return {x:b.left+40,y:b.top+b.height/2};}""", cible['i'])
        pg.mouse.move(r['x'], r['y']); pg.mouse.down(); pg.wait_for_timeout(750); pg.mouse.up()
        pg.wait_for_timeout(900)
    VIS = """()=>[...document.querySelectorAll('#feedList .s4-acte')].filter(e=>e.getBoundingClientRect().width>4).map(e=>(e.textContent||'').trim())"""
    actes = pg.evaluate(VIS)
    t('l\'appui maintenu fait paraître « TRACER » et « REPORTER », jamais « TENIR »',
      any(re.search('TRACER', a, re.I) for a in actes) and any(re.search('REPORTER', a, re.I) for a in actes) and not any(re.search(r'\bTENIR\b', a, re.I) for a in actes), str(actes))
    if cible and any(re.search('TRACER', a, re.I) for a in actes):
        av = pg.evaluate("(i)=>(promises.find(p=>p.id===i)||{}).status", cible['pid'])
        pg.evaluate("""()=>{const b=[...document.querySelectorAll('#feedList .s4-acte')].filter(e=>e.getBoundingClientRect().width>4).find(e=>/TRACER/i.test(e.textContent||'')); if(b)b.click();}""")
        pg.wait_for_timeout(2400)
        ap = pg.evaluate("(i)=>(promises.find(p=>p.id===i)||{}).status", cible['pid'])
        fiche = pg.evaluate("(i)=>{const d=document.getElementById('detailPoster'); return !!(d&&d.classList.contains('show')&&typeof cur!=='undefined'&&cur&&cur.id===i);}", cible['pid'])
        t('« TRACER » ouvre la fiche de cette parole, sans la tenir', fiche and ap == av and ap != 'tenu', '« %s » : %s → %s · fiche %s' % (cible['titre'], av, ap, fiche))
    else:
        t('« TRACER » ouvre la fiche de cette parole, sans la tenir', False, 'aucun « TRACER » après l\'appui')
    try: pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(500)
    except Exception: pass

    # ── 3 · CHERCHER ET TRIER ───────────────────────────────────────────────────────
    print('\n── chercher, trier ──')
    raz(); pg.evaluate("()=>ouvrirIndex()"); pg.wait_for_timeout(1700)
    n0 = pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte,#indexList .ix-bloc').length")
    pg.evaluate("""()=>{const e=document.getElementById('ixSearch');e.focus();e.value='zzzzzz';
      e.dispatchEvent(new Event('input',{bubbles:true}));}"""); pg.wait_for_timeout(1200)
    t('on cherche dans l\'Index',
      pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte,#indexList .ix-bloc').length") < n0,
      '%d cartes au départ' % n0)
    pg.evaluate("""()=>{const e=document.getElementById('ixSearch');e.value='';
      e.dispatchEvent(new Event('input',{bubbles:true}));}"""); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const b=document.getElementById('ixTriBtn');if(b)b.click();}"); pg.wait_for_timeout(1100)
    t('le tri de l\'Index s\'ouvre', pg.evaluate("""()=>{const m=document.getElementById('ixMenu')||document.getElementById('ixSort');
      return !!m && getComputedStyle(m).display!=='none';}"""))
    # ⚠ ON MESURE LE PANNEAU, PAS LE VOILE. `#ixMenu` est le voile plein écran, transparent
    #   (390 × 844, fond `rgba(0,0,0,0)`) : le mesurer faisait dire au contrôle que le menu
    #   couvrait les cartes. Le PANNEAU, lui, est `.ix-menu-p` — 346 × 604, fond opaque, et
    #   il ne couvre rien qu'il ne doive couvrir. C'était le contrôle qui visait à côté.
    t('le menu de tri ne couvre pas tout l\'écran', pg.evaluate("""()=>{
      const p=document.querySelector('#ixMenu .ix-menu-p, #ixSort .ix-menu-p'); if(!p) return false;
      const r=p.getBoundingClientRect();
      const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
      const c=getComputedStyle(p);
      const opaque = c.backgroundColor && !/rgba\(.*,\s*0\)/.test(c.backgroundColor);
      return (r.height/sc) < 700 && opaque;}"""),
      pg.evaluate("""()=>{const p=document.querySelector('#ixMenu .ix-menu-p, #ixSort .ix-menu-p');
        if(!p) return 'ABSENT'; const r=p.getBoundingClientRect();
        const dev=document.getElementById('device').getBoundingClientRect();
        return Math.round(r.height/(dev.width/390))+' px de haut, fond '+getComputedStyle(p).backgroundColor;}"""))

    # ── 4 · OUVRIR ──────────────────────────────────────────────────────────────────
    print('\n── ouvrir ──')
    raz(); pg.evaluate("()=>ouvrirIndex()"); pg.wait_for_timeout(1700)
    pg.evaluate("()=>{const c=document.querySelector('#indexList .s4-carte,#indexList .ix-bloc');if(c)c.click();}")
    pg.wait_for_timeout(1500)
    t('une carte d\'Index ouvre sa fiche',
      pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
    # ⚠ MÊME RÉÉCRITURE : on vise un bandeau QUI PORTE UNE PAROLE, pas « le premier
    #   nœud trouvé ». L'ancien contrôle fabriquait un événement de type `missed` que
    #   l'app ne modélise pas : son bandeau n'avait pas de parole, donc pas de fiche à
    #   ouvrir, et le contrôle accusait le Fil de l'avoir perdue.
    raz(); pg.evaluate("()=>setView('fil')"); pg.wait_for_timeout(1700)
    cb = pg.evaluate("""()=>{const L=[...document.querySelectorAll('#feedList .s4-carte')];
      for(let i=0;i<L.length;i++){ if(L[i].onclick) return i; } return -1;}""")
    t('un bandeau du Fil porte l\'ouverture de sa fiche', cb >= 0, 'bandeau n° %s' % cb)
    if cb >= 0:
        pg.evaluate("(i)=>{[...document.querySelectorAll('#feedList .s4-carte')][i].click();}", cb)
        pg.wait_for_timeout(1500)
    t('un bandeau du Fil ouvre sa fiche',
      pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))

    # ── 5 · PEAUFINER ───────────────────────────────────────────────────────────────
    print('\n── peaufiner ──')
    raz(); pg.evaluate("()=>openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id)"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1300)
    t('Peaufiner s\'ouvre sur une fiche', pg.evaluate("""()=>[...document.querySelectorAll('#detailPoster .s2-reg')]
      .filter(e=>e.getBoundingClientRect().height>10).length >= 4"""))
    t('Peaufiner se referme', (pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();return 1;}")
       and pg.wait_for_timeout(1200) is None
       and pg.evaluate("""()=>[...document.querySelectorAll('#detailPoster .s2-reg')]
         .filter(e=>e.getBoundingClientRect().height>10).length === 0""")))

    # ── 6 · LES QUATRE ÉCRANS DU DOCK ───────────────────────────────────────────────
    print('\n── les écrans du dock ──')
    for nom, bid, sel in (('Studio', 'studioBtn', '#studioScreen'), ('Aura', 'souffleBtn', '#auraScreen'),
                          ('Partager', 'shareBtn', '#shareScreen'), ('Réglages', 'settingsBtn', '#settingsScreen')):
        raz(); pg.evaluate("(b)=>{const x=document.getElementById(b);if(x)x.click();}", bid); pg.wait_for_timeout(1500)
        t('%s s\'ouvre' % nom, pg.evaluate("(s)=>{const e=document.querySelector(s);return !!e&&e.classList.contains('show');}", sel))

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nFONCTIONS PERDUES OU CASSÉES :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
