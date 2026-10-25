#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_garder.py — « GARDER DE CÔTÉ » GARDE (v119, Tom, Q370). Au DOIGT, WebKit et Chromium.

« Au toucher, le titre et la personne de la phrase passent au gardé de côté, puis la page + se ferme. »
  A · la page + d'un Promi : on écrit un titre au doigt, on choisit une personne — le lien « garder de côté » paraît et il est joignable
  B · on le touche : la page + se ferme
  C · un gardé de côté de plus existe, avec CE titre et CETTE personne
  D · sans personne choisie, il est gardé « à moi »
  ⚑ v148 (C-149) : E · page vide, le lien est visible et inactif, et son toucher ne fait rien · F · plus aucune phrase « se retourne » ·
  G · une modification faite, il est actif · H · le brouillon est retrouvé dans l'Index · I · une personne ajoutée seule suffit à l'activer
  ⚑ v149 (Tom, C-149 rouvert) : « à droite ; pas souligné ; légèrement penché, 5 à 6° ; toujours visible ; actif seulement après l'ajout d'une personne
  ou une modification. » G ne lit plus le soulignement (actif = la classe et la teinte du lien) ; J · à droite (son bord droit à 24 pt du bord, à sa
  cote 708 ± 2), jamais souligné, penché de 5 à 6° (lu sur la transformation calculée) ; K · toujours visible : aussi pendant un tracé (doigt posé).
  Original : sauvegardes/redteam_garder-avant-v149.py.
  ⚑ v150 (Tom, C-149) : « Garder de côté » 4 pt plus bas (0,6 mm) — sa cote passe de 708 à 712 ; l'inclinaison ne change pas. Original : *-avant-v150.py.
  ⚑ v151 (Tom, C-149) : « encore 1 mm plus bas » — 718 (712 + 6) ; l'inclinaison ne change pas. Original : *-avant-v151.py.
Preuve (§7) : sur une copie de `sauvegardes/app-avant-v119.html` à la racine (APP=…), C et D ROUGISSENT (v118 fermait la page sans rien garder).
"""
import os, sys
from playwright.sync_api import sync_playwright
APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
TITRE = 'aller voir la mer'; QUI = 'Rachel'
ok = [0]; ko = []
def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-70s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-70s KO  %s' % (nom, detail))
def centre(pg, js):
    return pg.evaluate("(f)=>{const e=(new Function('return ('+f+')'))(); if(!e) return null; const q=(getComputedStyle(e).display==='inline'&&e.getClientRects().length)?e.getClientRects()[0]:e.getBoundingClientRect(); return q.width?{x:q.left+q.width/2,y:q.top+q.height/2}:null}", js)
def tape(pg, js, attente=800):
    c = centre(pg, js)
    if not c: return False
    pg.touchscreen.tap(c['x'], c['y']); pg.wait_for_timeout(attente); return True
GEO = """()=>{const g=document.querySelector('#createSheet .pp-garder'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!g) return null;
  const s=getComputedStyle(g), m=(s.transform||'').match(/matrix\(([^)]+)\)/), c=m?+m[1].split(',')[2]:0;
  /* la boîte AVANT la transformation : offsetLeft/Top dans la feuille (390 pt), le penché lu sur la matrice (skewX : c = tan θ) */
  const cs=document.getElementById('createSheet'), R=cs.getBoundingClientRect(), kk=R.width/(cs.offsetWidth||390);
  return {droite:+((g.offsetLeft+g.offsetWidth)).toFixed(1), haut:+g.offsetTop.toFixed(1), souligne:s.textDecorationLine, penche:+(-Math.atan(c)*180/Math.PI).toFixed(2), vu:s.display!=='none'&&s.visibility!=='hidden'&&g.getBoundingClientRect().width>4};}"""
TIENT_COURS = """async ()=>{ const z=document.getElementById('planterZone'); if(!z) return null; const r=z.getBoundingClientRect(), x0=r.left+r.width*0.12, y=r.top+r.height*0.45;
  const T=(x)=>{ const o={identifier:9,target:z,clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,radiusX:11,radiusY:11,force:.5}; try{return new Touch(o);}catch(e){return o;} };
  const ev=(typ,x)=>{ const t=T(x), L=typ==='touchend'?[]:[t]; let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,composed:true,touches:L,targetTouches:L,changedTouches:[t]}); if(!e.changedTouches||!e.changedTouches.length) throw 0; }catch(_){ e=new Event(typ,{bubbles:true,cancelable:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t]}); } z.dispatchEvent(e); };
  const att=ms=>new Promise(r=>setTimeout(r,ms)); ev('touchstart',x0); for(let i=1;i<=3;i++){ await att(40); ev('touchmove',x0+i*6); } await att(260);
  const cs=document.getElementById('createSheet'), g=cs.querySelector('.pp-garder'), s=getComputedStyle(g);
  const out={cours:cs.classList.contains('pp-cours'), vu:s.display!=='none'&&s.visibility!=='hidden'&&g.getBoundingClientRect().width>4, droite:+((g.offsetLeft+g.offsetWidth)).toFixed(1)};
  ev('touchend',x0+18); await att(400); return out; }"""
def passe(b, moteur, avec_qui):
    tag = '[%s%s]' % (moteur, '' if avec_qui else ', sans personne')
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light');}")
    avant = pg.evaluate("()=>promises.filter(p=>p.draft).length")
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2600)
    # ⚑ v148 (Tom, C-149) — « Tom ne voit pas “Garder de côté”. Rends-le visible dans la page +. Il n'est actif que si l'on a ajouté au moins une
    #   personne ou fait au moins une modification. Avant cela, il ne fait rien. »
    v0 = pg.evaluate("()=>{const g=document.querySelector('#createSheet .pp-garder'); if(!g) return null; const r=g.getBoundingClientRect(), s=getComputedStyle(g); return {vu:s.display!=='none'&&r.width>4, inactif:g.classList.contains('inactif'), aria:g.getAttribute('aria-disabled'), souligne:s.textDecorationLine}; }")
    t(tag + ' E · page vide : le lien est VISIBLE et INACTIF (non souligné, aria-disabled)', bool(v0) and v0['vu'] and v0['inactif'] and v0['aria'] == 'true' and v0['souligne'] == 'none', str(v0))
    tape(pg, "document.querySelector('#createSheet .pp-garder')", 1200)
    rien = pg.evaluate("(n)=>document.getElementById('createSheet').classList.contains('show') && promises.filter(p=>p.draft).length===n", avant)
    t(tag + ' E · page vide : le toucher ne fait rien (la page reste, aucun gardé de côté)', rien)
    hint = pg.evaluate("()=>[...document.querySelectorAll('#createSheet .ph-hint')].filter(h=>getComputedStyle(h).display!=='none'&&h.getBoundingClientRect().height>0).map(h=>h.textContent)")
    corps = pg.evaluate("()=>document.getElementById('createSheet').innerText")
    t(tag + ' F · plus aucune phrase « se retourne » (C-149)', not hint and 'se retourne' not in corps, str(hint))
    if avec_qui: tape(pg, "document.querySelector('#csPhrase [data-ph=sens]')", 1100)      # « Je me promets » → « Je promets … à qui ? »
    tape(pg, "document.querySelector('#csPhrase [data-ph=titre]')", 900); pg.keyboard.type(TITRE); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
    if avec_qui:
        tape(pg, "document.querySelector('#csPhrase [data-ph=qui]')", 1000)
        choisi = tape(pg, 'document.querySelector(\'#createSheet .gn .ph-o[data-v="%s"]\')' % QUI, 900)
        # on referme le choix : toucher hors du panneau et hors de la phrase
        pg.touchscreen.tap(215, 180); pg.wait_for_timeout(1100)
        sel = pg.evaluate("()=>JSON.stringify(window.newWhoSel||[])")
        t(tag + ' la personne est choisie au doigt', choisi and QUI in sel, sel)
    act = pg.evaluate("()=>{const g=document.querySelector('#createSheet .pp-garder'); return g?{inactif:g.classList.contains('inactif'), aria:g.getAttribute('aria-disabled'), souligne:getComputedStyle(g).textDecorationLine}:null; }")
    t(tag + ' G · une modification faite : le lien est ACTIF (ni inactif ni aria-disabled)', bool(act) and not act['inactif'] and act['aria'] != 'true', str(act))
    geo = pg.evaluate(GEO)
    t(tag + ' J · à droite (bord droit à 366 ± 1,5 pt), à sa cote (haut 718 ± 0,5, v151), jamais souligné, penché de 5 à 6°', bool(geo) and abs(geo['droite'] - 366) <= 1.5 and abs(geo['haut'] - 718) <= 0.5 and geo['souligne'] == 'none' and 5 <= geo['penche'] <= 6, str(geo))
    tient = pg.evaluate(TIENT_COURS)
    t(tag + ' K · toujours visible : pendant un tracé (doigt posé, page en cours de geste), le lien reste à sa place', bool(tient) and tient['cours'] and tient['vu'] and abs(tient['droite'] - 366) <= 1.5, str(tient))
    lien = pg.evaluate("()=>{const g=document.querySelector('#createSheet .pp-garder'); if(!g) return null; const r=g.getBoundingClientRect(); if(!r.width) return {vu:false}; const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return {vu:true, joignable:h===g||g.contains(h), mot:g.textContent}}")
    t(tag + ' A · le lien « garder de côté » paraît, et il est joignable', bool(lien) and lien.get('vu') and lien.get('joignable') and lien.get('mot') == 'garder de côté', str(lien))
    tape(pg, "document.querySelector('#createSheet .pp-garder')", 3200)
    ferme = pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('show')")
    t(tag + ' B · la page + se ferme', ferme)
    g = pg.evaluate("(t)=>{const L=promises.filter(p=>p.draft); const p=L.find(p=>p.title===t); return {n:L.length, trouve:!!p, qui:p?p.who:null, titres:L.map(p=>p.title)}}", TITRE)
    t(tag + ' C · un gardé de côté de plus, avec le titre de la phrase', g['n'] == avant + 1 and g['trouve'], '%d → %d · %s' % (avant, g['n'], g['titres']))
    if avec_qui: t(tag + ' C · avec la personne de la phrase', g['trouve'] and (g['qui'] or '').lower() == QUI.lower(), str(g['qui']))
    else: t(tag + ' D · sans personne choisie : gardé « à moi »', g['trouve'] and (g['qui'] or '').lower() in ('moi', ''), str(g['qui']))
    # H · le brouillon est retrouvé : une carte « GARDÉ DE CÔTÉ » de ce titre dans l'Index
    pg.evaluate("()=>{ closeAll(); setView('toile'); ouvrirIndex(); }"); pg.wait_for_timeout(2600)
    carte = pg.evaluate("(t)=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>(c.textContent||'').replace(/\\s+/g,' ')).filter(x=>x.indexOf(t)>=0)", TITRE)
    t(tag + ' H · le brouillon est retrouvé : sa carte est dans l\'Index', bool(carte), str(carte)[:120])
    ctx.close()
def passe_qui_seul(b, moteur):
    # I · une personne ajoutée, rien d'autre : le lien devient actif
    tag = '[%s, une personne seule]' % moteur
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light');}")
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2600)
    tape(pg, "document.querySelector('#csPhrase [data-ph=sens]')", 1100)
    tape(pg, "document.querySelector('#csPhrase [data-ph=qui]')", 1000)
    tape(pg, 'document.querySelector(\'#createSheet .gn .ph-o[data-v="%s"]\')' % QUI, 900)
    pg.touchscreen.tap(215, 180); pg.wait_for_timeout(1100)
    act = pg.evaluate("()=>{const g=document.querySelector('#createSheet .pp-garder'); return g?{vu:getComputedStyle(g).display!=='none', inactif:g.classList.contains('inactif')}:null; }")
    t(tag + ' I · une personne ajoutée, sans rien d\'autre : le lien est actif', bool(act) and act['vu'] and not act['inactif'], str(act))
    ctx.close()
with sync_playwright() as p:
    for moteur in ('webkit', 'chromium'):
        b = getattr(p, moteur).launch(); passe(b, moteur, True); passe(b, moteur, False); passe_qui_seul(b, moteur); b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
