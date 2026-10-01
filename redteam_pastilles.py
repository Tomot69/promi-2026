#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_pastilles.py — LE CONTRÔLE QUI TOUCHE.

Une pastille qui ne change rien est morte, et aucun juge de cote ne le voit : elle est à la
bonne place, dans la bonne police, et elle ne sert à rien. Celui-ci TOUCHE chaque pastille
de chaque écran et vérifie qu'ELLE CHANGE QUELQUE CHOSE — sa propre marque, une donnée, ou
un mot à l'écran.

Une pastille est bonne quand les deux sont vraies :
  1 · elle est ATTEIGNABLE   (visible, non nulle, dans le cadre, cliquable)
  2 · elle a un EFFET        (l'état de l'app n'est plus le même après)

Usage :  python3 redteam_pastilles.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-56s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-56s KO  %s' % (nom, detail))


# l'empreinte de l'écran : ce qui doit bouger quand une pastille a un effet
EMPREINTE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const mots=[];
  document.querySelectorAll('body *').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    if([...e.children].some(x=>!['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(x.tagName))) return;
    const t=(e.textContent||'').trim(); if(!t) return;
    const r=e.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    if(x<-2||x>392||y<-2||y>846) return;
    mots.push(Math.round(y)+':'+t.slice(0,24));});
  const on=[...document.querySelectorAll('.chip.on,.is.on,.on')].map(e=>(e.textContent||'').trim().slice(0,14));
  /* ⚠ L'EMPREINTE DOIT VOIR CE QUE PORTE L'ÉCRAN, pas seulement ses mots. Toucher un
     créneau de la phrase OUVRE un panneau : ça pose `pp-ouvert` sur la feuille et ça ne
     change aucun mot. Sans les classes des hôtes, la pastille passait pour morte. */
  const hotes=['createSheet','detailPoster','indexSheet','feedView','device']
    .map(id=>{const e=document.getElementById(id);
      return e?(id+':'+(e.className||'').split(' ').filter(Boolean).filter(c=>!/^gs\d+$/.test(c)).sort().join('.')):'';}).join('|');
  let don=''; try{ don=JSON.stringify(window._phrase||{})
    +((typeof cur!=='undefined'&&cur)?JSON.stringify({w:cur.who,d:cur.due,s:cur.status,n:cur.nuee}):''); }catch(e){}
  return mots.sort().join('|')+'##'+on.sort().join(',')+'##'+don+'##'+hotes;}"""

# toutes les pastilles atteignables de l'écran courant
PASTILLES = r"""(racine)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const h=racine?document.querySelector(racine):document.body; if(!h) return [];
  const out=[];
  /* `.ph-o` est l'option d'un choix ouvert (une personne, une date) : elle manquait, et
     un panneau déplié passait pour vide. */
  h.querySelectorAll('.chip,.is,.seg button,.ph-m,.ph-b,.ph-o,[data-w],[data-s],[data-due],[data-ph],[data-np]').forEach((e,i)=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.3) return;
    const r=e.getBoundingClientRect(); if(r.width<6||r.height<6) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    if(x<-2||x>390||y<-2||y>844) return;
    if(c.pointerEvents==='none') return;
    e.setAttribute('data-rtp', 'p'+i);
    out.push({cle:'p'+i, mot:(e.textContent||'').trim().slice(0,22),
              pos:Math.round(x)+','+Math.round(y)});});
  return out;}"""


OUVRE_REGLAGES = r"""(racine)=>{
  /* ⚠ DANS PEAUFINER, UN RÉGLAGE SE DÉPLIE (§3.3). Ses pastilles vivent dans un `.s2-ctl`
     masqué tant qu'on n'a pas touché le réglage : les chercher sans l'ouvrir donnait
     « 0 pastille » et faisait croire qu'on ne pouvait plus poser d'échéance. On ouvre donc
     chaque réglage AVANT de compter — c'est ce que fait un doigt. */
  const h=document.querySelector(racine); if(!h) return 0;
  /* ⚠ ON N'OUVRE QUE CE QUI SE DÉPLIE, ET JAMAIS CE QUI DÉTRUIT. « SUPPRIMER CE PROMI »
     est un réglage comme les autres au regard du DOM : le toucher efface la promesse et
     ferme la fiche sous le contrôle. On nomme donc ce qu'on évite. */
  const regs=[...h.querySelectorAll('.s2-reg')].filter(r=>{
    const lab=((r.querySelector('.s2-lab')||{}).textContent||'').toUpperCase();
    if(/SUPPRIMER|RELANCER|BROUILLON|PLANTER/.test(lab)) return false;
    return !!r.querySelector('.s2-ctl');});
  regs.forEach(r=>{ if(!r.classList.contains('s2-ouv')) r.click(); });
  return regs.length;}"""


REGLAGES = r"""(racine)=>{
  const h=document.querySelector(racine); if(!h) return [];
  return [...h.querySelectorAll('.s2-reg')].map((r,i)=>{
    const lab=((r.querySelector('.s2-lab')||{}).textContent||'').trim();
    if(/SUPPRIMER|RELANCER|BROUILLON|PLANTER/i.test(lab)) return null;
    if(!r.querySelector('.s2-ctl')) return null;
    r.setAttribute('data-rtr','r'+i); return {cle:'r'+i, lab:lab.slice(0,20)};}).filter(Boolean);}"""


def touche_peaufiner(pg, nom, racine):
    """⚠ DANS PEAUFINER, ON VA RÉGLAGE PAR RÉGLAGE. Les ouvrir tous puis toucher leurs
       pastilles en série ne marche pas : le premier clic referme les autres, et toutes
       passaient pour mortes — alors qu'elles posent bien l'échéance et la Nuée (vérifié).
       Un doigt ouvre UN réglage, choisit, passe au suivant. Le contrôle fait pareil."""
    regs = pg.evaluate(REGLAGES, racine)
    t('%s · des réglages qui se déplient' % nom, len(regs) >= 2, '%d réglages' % len(regs))
    morts = []
    for rg in regs[:6]:
        pg.evaluate("""(k)=>{const r=document.querySelector('[data-rtr='+k+']');
          if(r && !r.classList.contains('s2-ouv')) r.click();}""", rg['cle'])
        pg.wait_for_timeout(600)
        lot = pg.evaluate("""(k)=>{const r=document.querySelector('[data-rtr='+k+']'); if(!r) return [];
          return [...r.querySelectorAll('.chip,.is,button,.ph-o')]
            .filter(e=>e.getBoundingClientRect().width>6
                    && !e.classList.contains('on') && !e.classList.contains('ph-on'))
            .map((e,i)=>{e.setAttribute('data-rtp','q'+i);
              return {cle:'q'+i, mot:(e.textContent||'').trim().slice(0,16)};});}""", rg['cle'])
        if not lot: continue
        q = lot[0]
        av = pg.evaluate(EMPREINTE)
        pg.evaluate("""(a)=>{const r=document.querySelector('[data-rtr='+a.r+']');
          const e=r&&r.querySelector('[data-rtp='+a.q+']'); if(e)e.click();}""",
                    {'r': rg['cle'], 'q': q['cle']})
        pg.wait_for_timeout(600)
        if av == pg.evaluate(EMPREINTE):
            morts.append('%s → « %s »' % (rg['lab'], q['mot']))
    t('%s · leurs pastilles ont un effet' % nom, not morts,
      ('sans effet : ' + ' · '.join(morts[:5])) if morts else '%d réglages essayés' % len(regs[:6]))


def touche(pg, nom, racine, attendu_min, peaufiner=False):
    if peaufiner:
        return touche_peaufiner(pg, nom, racine)
    lot = pg.evaluate(PASTILLES, racine)
    t('%s · des pastilles à toucher' % nom, len(lot) >= attendu_min,
      '%d trouvées (au moins %d attendues)' % (len(lot), attendu_min))
    morts = []
    # ⚠ ON RE-MARQUE AVANT CHAQUE TOUCHE. Toucher un créneau de la phrase RECONSTRUIT
    #   `#csPhrase` : les marques `data-rtp` posées au premier relevé sont détruites, le
    #   clic suivant ne trouve plus rien, et toutes les pastilles passaient pour mortes.
    #   Un doigt ne mémorise pas des nœuds : il regarde l'écran à chaque fois.
    for i in range(min(len(lot), 14)):
        frais = pg.evaluate(PASTILLES, racine)
        if i >= len(frais): break
        q = frais[i]
        # ⚠ UN VERBE SANS ALTERNATIVE N'OUVRE RIEN, ET C'EST JUSTE. Sur un Promi, le verbe
        #   bascule le sens (« Je promets » ↔ « Promets-moi »). Un **Chiche** n'a pas
        #   d'autre sens : un Chiche est un Chiche. Sa pastille de verbe n'est donc pas une
        #   pastille morte — c'est une pastille sans choix. La compter morte réclamait, en
        #   creux, une fonction que le produit n'a pas (changer la nature après coup) :
        #   ce serait trancher un point de produit depuis un contrôle.
        sansChoix = pg.evaluate("""(k)=>{const e=document.querySelector('[data-rtp='+k+']');
          if(!e) return false;
          const estVerbe = e.getAttribute('data-ph')==='sens' || e.classList.contains('ph-b');
          if(!estVerbe) return false;
          const cs=document.getElementById('createSheet');
          return !!cs && (cs.classList.contains('pp-chiche')||cs.classList.contains('pp-nuee'));}""",
                                q['cle'])
        if sansChoix: continue
        # une pastille DÉJÀ CHOISIE ne change rien, et c'est juste.
        deja = pg.evaluate("""(k)=>{const e=document.querySelector('[data-rtp='+k+']');
          return !!e && (e.classList.contains('on')||e.classList.contains('ph-on'));}""", q['cle'])
        if deja: continue
        av = pg.evaluate(EMPREINTE)
        pg.evaluate("(k)=>{const e=document.querySelector('[data-rtp='+k+']');if(e)e.click();}", q['cle'])
        pg.wait_for_timeout(500)
        ap = pg.evaluate(EMPREINTE)
        if av == ap: morts.append('« %s » @%s' % (q['mot'], q['pos']))
    t('%s · toutes ont un effet' % nom, not morts,
      ('sans effet : ' + ' · '.join(morts[:6])) if morts else '%d touchées' % len(lot[:14]))


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    def page_plus(i):
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
        pg.evaluate("(i)=>{const t=[...document.querySelectorAll('#createSheet .tile')][i];if(t)t.click();}", i)
        pg.wait_for_timeout(1100)

    # ⚠ Q28 · LA PHRASE EST À DEUX LIGNES — le verbe et l'objet. L'échéance a QUITTÉ la
    #   phrase, elle vit dans Peaufiner. Attendre trois créneaux était une erreur de ma part :
    #   je réclamais un « quand » que le produit a retiré il y a plusieurs lots.
    print('\n── la page + · Promi ──'); page_plus(0)
    touche(pg, 'page + Promi', '#createSheet', 2)

    print('\n── la page + · Promi, choix ouvert ──'); page_plus(0)
    pg.evaluate("()=>{const e=document.querySelector('[data-ph=titre]');if(e)e.click();}"); pg.wait_for_timeout(900)
    touche(pg, 'page + choix ouvert', '#createSheet', 2)

    print('\n── la page + · Chiche ──'); page_plus(1)
    touche(pg, 'page + Chiche', '#createSheet', 2)

    print('\n── la page + · Peaufiner ──'); page_plus(0)
    pg.evaluate("()=>{const x=document.querySelector('#createSheet #csBotBar,#createSheet .cbb-lab');if(x)x.click();}")
    pg.wait_for_timeout(1300)
    touche(pg, 'page + Peaufiner', '#createSheet', 4, peaufiner=True)

    print('\n── une fiche · Peaufiner ──')
    pg.evaluate("""()=>{if(window.closeAll)closeAll();
      openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}"""); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}")
    pg.wait_for_timeout(1300)
    touche(pg, 'fiche Peaufiner', '#detailPoster', 4, peaufiner=True)

    # ── Q28 · L'ÉCHÉANCE VIT DANS PEAUFINER, ET NULLE PART AILLEURS. C'est donc le SEUL
    #    endroit où on la pose : si ce réglage est mort, une promesse ne peut pas avoir de
    #    date. Le contrôle le vérifie de bout en bout — on ouvre, on choisit, on relit.
    pg.reload(); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{if(window.closeAll)closeAll();
      openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}"""); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}")
    pg.wait_for_timeout(1300)
    pg.evaluate("""()=>{const r=[...document.querySelectorAll('#detailPoster .s2-reg')]
      .filter(e=>/AVANT/.test((e.querySelector('.s2-lab')||{}).textContent||''))[0];
      if(r && !r.classList.contains('s2-ouv')) r.click();}"""); pg.wait_for_timeout(900)
    n = pg.evaluate("""()=>[...document.querySelectorAll('#detailPoster .s2-reg.s2-ouv .chip,'
      +'#detailPoster .s2-reg.s2-ouv button')].filter(c=>c.getBoundingClientRect().width>4).length""")
    t('l\'échéance · le réglage s\'ouvre et propose ses dates', n >= 4, '%d dates proposées' % n)
    av = pg.evaluate("()=>(typeof cur!=='undefined'&&cur)?cur.due:null")
    pg.evaluate("""()=>{const b=[...document.querySelectorAll('#detailPoster .s2-reg.s2-ouv .chip,'
      +'#detailPoster .s2-reg.s2-ouv button')].filter(c=>c.getBoundingClientRect().width>4
      && /5 j/.test(c.textContent||''))[0]; if(b)b.click();}"""); pg.wait_for_timeout(900)
    ap = pg.evaluate("()=>(typeof cur!=='undefined'&&cur)?cur.due:null")
    t('l\'échéance · choisir une date la POSE', ap == 5 and ap != av, '%s → %s' % (av, ap))

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nCE QUI NE MARCHE PAS :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
