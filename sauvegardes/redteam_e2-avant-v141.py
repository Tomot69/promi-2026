#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_e2.py — E2 « LE PREMIER PROMI, TENU EN UNE MINUTE » et E2bis « L'INTERFACE SE DÉVOILE » (v140, Tom, 10 oct. 2026 ; C-075, C-076).

« Juge : le parcours E2 complet, stockage vierge, au plus 5 touchers et 1 trait jusqu'au premier tenu ; E2bis, tout est visible à la fin,
et tout est visible d'emblée après “Plus tard”. Captures de chaque étape, en clair et en sombre. »

Chromium, AU VRAI DOIGT (CDP `Input.dispatchTouchEvent`), stockage vierge. Le parcours, après l'identification (le prénom) :
  le principe → la vraie page + (phrase fantôme) → le trait qui plante → la fiche → le trait qui tient → la dernière ligne → le compte.
Ce qui est jugé :
  P · chaque étape paraît, avec ses textes (ceux de TEXTES_ENGAGEMENT.e2, lus à l'écran) ;
  F · la phrase fantôme est l'une des trois (EN DUR), un toucher la remplit ; rien d'autre n'est montré sur la page + ;
  R · la parole plantée est RÉELLE (un id, dans `promises`), puis TENUE ; `ob_fini` est posé ; rechargée, l'app ne rejoue rien ;
  C · le compte des gestes de l'étape du principe au premier tenu : touchers ≤ 5 (EN DUR) ; les traits sont comptés et DITS (planter est un
      trait, tenir en est un autre) ;
  M · la main fantôme accompagne le trait qui plante et le trait qui tient ;
  S · R6 — une sortie visible, sous le doigt, à CHAQUE étape (le prénom compris) ;
  A · A2 — tout nœud `data-eng` à l'écran est opaque (lui et ses ancêtres), sans transition ni animation ; A3 — aucun texte du parcours à l'impératif ;
  D · E2bis — la barre : le + seul au départ ; l'Index après la plantation ; l'Aura après le tenu (la main la désigne) ; le Studio au retour de
      l'Aura ; le Fil à la première parole adressée ; rien ne disparaît d'une étape à l'autre ; à la fin TOUT est visible ;
  T · « Plus tard » à chacune des quatre étapes : un toucher, l'accueil, TOUT est visible d'emblée, `ob_fini` posé, rien n'est rejoué.
Options : --r6 (la seule ligne R6, pour redteam_engagement) · --vite (sans le sombre ni les quatre « Plus tard »).
Preuve : rouge sur l'état d'avant (python3 redteam_e2.py zz-av140.html).
"""
import sys, re, os
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); URL = 'http://127.0.0.1:8752/' + F
R6 = '--r6' in sys.argv; VITE = '--vite' in sys.argv or R6
FANTOMES = ['boire un verre d’eau', 'ouvrir la fenêtre', 'm’étirer trente secondes']; TOUCHERS_MAX = 5
IMPERATIFS = ('fais faites faisons reviens revenez dis dites ajoute ajoutez lance lancez commence commencez change changez plante plantez trace tracez touche touchez '
              'écris écrivez essaie essaye essayez viens venez va allez allons regarde regardez tiens tenez choisis choisissez prends prenez pose posez garde gardez ouvre ouvrez '
              'appuie appuyez glisse glissez continue continuez promets promettez raconte racontez envoie envoyez invite invitez partage partagez découvre découvrez pense pensez '
              'laisse laissez mets mettez donne donnez montre montrez reprends reprenez').split()
IMP = re.compile(r"(?:^|[.!?…:;]\s+|,\s+|\b(?:puis|et)\s+)(%s)(?![a-zàâçéèêëîïôûùüÿœ])" % '|'.join(IMPERATIFS), re.I)
IMP2 = re.compile(r"[a-zàâçéèêëîïôûùüÿœ]+(?:e|s|ons|ez|a)-(?:le|la|les|lui|leur|toi|moi|nous|y|en)(?![a-zàâçéèêëîïôûùüÿœ])", re.I)
ok = 0; ko = []; sorties = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    if not R6: print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
ETAT = r"""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, vis=(e)=>{ if(!e) return false; const r=e.getBoundingClientRect(), c=getComputedStyle(e); if(!(r.width>6&&r.height>6&&c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.05)) return false;
    if(r.bottom<D.top||r.top>D.bottom||r.right<D.left||r.left>D.right) return false; for(let q=e.parentElement; q&&q.nodeType===1; q=q.parentElement){ const s=getComputedStyle(q); if(+s.opacity<0.05||s.visibility==='hidden'||s.display==='none') return false; if(q.id==='device') break; } return true; };
  const haut=(e)=>{ if(!vis(e)) return false; const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!(h&&(h===e||e.contains(h)||h.contains(e))); };
  const onb=document.getElementById('promiOnb'), onbV=!!(onb&&!onb.classList.contains('gone')&&getComputedStyle(onb).display!=='none');
  const S=[]; document.querySelectorAll('#onbTard, #e2Tard, .onbv-compte .tard, #detailPoster .closeb, #createSheet .closeb, #detailPoster .dp-fermer, [data-onb="plus-tard"]').forEach(e=>{ if(haut(e)) S.push(((e.textContent||'')+' '+(e.getAttribute('aria-label')||'')).trim().replace(/\s+/g,' ').slice(0,20)); });
  const E=[], mauvais=[]; document.querySelectorAll('[data-eng]').forEach(e=>{ if(!vis(e)) return; E.push(e.getAttribute('data-eng'));
    for(let q=e; q&&q.id!=='device'&&q.nodeType===1; q=q.parentElement){ const c=getComputedStyle(q); if(+c.opacity<1){ mauvais.push((e.getAttribute('data-eng'))+' : opacité '+c.opacity+' sur '+(q.id||q.className)); break; } }
    const c=getComputedStyle(e); if((c.transitionDuration||'0s').split(',').some(t=>parseFloat(t)>0)) mauvais.push(e.getAttribute('data-eng')+' : transition '+c.transitionDuration); if(c.animationName&&c.animationName!=='none') mauvais.push(e.getAttribute('data-eng')+' : animation '+c.animationName); });
  const B={}; [['plus','createBtn'],['index','indexBtn'],['aura','souffleBtn'],['studio','studioBtn'],['fil','filBtn']].forEach(([n,i])=>{ const e=document.getElementById(i); B[n]=!!(e&&e.closest('#accBarre')&&vis(e)); });
  const bf=document.getElementById('accBarreFond'), br=document.getElementById('accBarre'); let fond=null; if(bf&&vis(bf)){ const r=bf.getBoundingClientRect(); fond=[Math.round((r.left-D.left)/k), Math.round((r.right-D.left)/k)]; } else if(br&&vis(br)){ const r=br.getBoundingClientRect(); fond=[Math.round((r.left-D.left)/k), Math.round((r.right-D.left)/k)]; }
  const T=[]; document.querySelectorAll('[data-eng]').forEach(e=>{ if(vis(e)&&!e.childElementCount){ const t=(e.textContent||'').trim(); if(t) T.push(t); } });
  const gf=document.getElementById('gesteFantome');
  let e2=null; try{ e2=window._e2?window._e2.etat():null; }catch(_){}
  return {onb:onbV, sorties:S, eng:E, a2:mauvais, barre:B, fond:fond, textes:T, main:gf?gf.getAttribute('data-geste'):null, e2:e2, obfini:localStorage.getItem('ob_fini'), verrou:localStorage.getItem('promi_onb'),
    cs:!!(document.querySelector('#createSheet.show')), dp:!!(document.querySelector('#detailPoster.show')), compte:!!document.querySelector('.onbv-compte'),
    n:(typeof promises!=='undefined'?promises.filter(p=>!p.draft).length:-1), tenu:(typeof promises!=='undefined'?promises.filter(p=>p.status==='tenu').length:-1) }; }"""
def point(pg, sel):
    # le premier rectangle de l'élément : une pastille sur deux lignes a un creux au milieu de sa boîte
    return pg.evaluate("(s)=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getClientRects()[0]||e.getBoundingClientRect(); if(r.width<4) return null; return [r.left+r.width/2, r.top+r.height/2]; }", sel)
def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def tracer(cdp, pg, P):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': P[0][0], 'y': P[0][1]}]}); pg.wait_for_timeout(120)
    for (x, y) in P[1:]:
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(22)
    pg.wait_for_timeout(120); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
ONDE_PP = "()=>{ const e=window._ppEcran&&window._ppEcran(), cv=document.getElementById('csTrameCv'); if(!e||!cv||!e.base) return null; const r=cv.getBoundingClientRect(), k=r.width/390, f=window._onde.onde(e.base,e.amp), P=[]; for(let x=30;x<=360;x+=11) P.push([r.left+x*k, r.top+f(x)*k]); return P; }"
ONDE_FI = "()=>{ const cv=document.getElementById('dpTrameCv'), t=cv&&(cv.getAttribute('data-trait')||'').split(','); if(!t||t.length<4) return null; const r=cv.getBoundingClientRect(), k=r.width/390, f=window._onde.onde(+t[0],+t[1]), P=[]; for(let x=30;x<=360;x+=11) P.push([r.left+x*k, r.top+f(x)*k]); return P; }"
def ouvre(b, th):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    if th == 'dark': ctx.add_init_script("try{ if(!localStorage.getItem('promi_theme')) localStorage.setItem('promi_theme','dark'); }catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto(URL); pg.wait_for_timeout(6800)
    return ctx, pg, ctx.new_cdp_session(pg), er
def prenom(pg, cdp):
    p = point(pg, '[data-onb="prenom"]')
    if not p: return False
    toucher(cdp, pg, p[0], p[1]); pg.wait_for_timeout(350); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(250)
    s = point(pg, '[data-onb="suite"]')
    if s: toucher(cdp, pg, s[0], s[1])
    else: pg.keyboard.press('Enter')
    pg.wait_for_timeout(1300); return True
def cap(pg, nom):
    if R6: return
    os.makedirs('planche-e2', exist_ok=True)
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
    pg.screenshot(path='planche-e2/%s.png' % nom, clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})
def sortie(nom, e): sorties.append((nom, bool(e['sorties']), e['sorties']))
def a3(textes): return [t for t in textes if IMP.search(t) or IMP2.search(t)]
def parcours(b, th):
    T = 'clair' if th == 'light' else 'sombre'; plein = (th == 'light')
    ctx, pg, cdp, er = ouvre(b, th)
    barres = []; touchers = 0; traits = 0; A2 = []; TX = []
    def note(e): A2.extend(e['a2']); TX.extend(e['textes']); barres.append(dict(e['barre']))
    e = pg.evaluate(ETAT); sortie('1 · le prénom', e); cap(pg, '1-prenom-' + th)
    juge('[%s] P · stockage vierge : l\'onboarding s\'ouvre sur le prénom, avec sa sortie' % T, e['onb'] and bool(e['sorties']), str(e['sorties']))
    prenom(pg, cdp)
    e = pg.evaluate(ETAT); note(e); sortie('2 · le principe', e); cap(pg, '2-principe-' + th)
    juge('[%s] P · après le prénom : le principe (titre, trois lignes, un bouton, « Plus tard »)' % T, e['onb'] and 'principe-titre' in e['eng'] and e['eng'].count('principe-ligne') == 3 and 'principe-bouton' in e['eng'] and bool(e['sorties']), str(e['textes'][:6]))
    if R6 and not e['onb']: return
    p = point(pg, '[data-onb="e2-suite"]')
    if p: toucher(cdp, pg, p[0], p[1]); touchers += 1
    try: pg.wait_for_function("()=>{const s=document.getElementById('createSheet'); return s&&s.classList.contains('show')&&s.classList.contains('pp-promi')&&!s.classList.contains('acc-passe')&&!!document.querySelector('#csPhrase [data-ph=titre]')}", timeout=9000)
    except Exception: pass
    pg.wait_for_timeout(1200)
    e = pg.evaluate(ETAT); note(e); sortie('3 · la page +', e); cap(pg, '3-page-plus-' + th)
    ft = pg.evaluate("()=>{ const m=document.querySelector('#csPhrase [data-ph=titre]'); const v=(s)=>{const e=document.querySelector(s); if(!e) return false; const r=e.getBoundingClientRect(), c=getComputedStyle(e); return r.width>4&&r.height>4&&c.display!=='none'&&c.visibility!=='hidden';}; return {txt:m?m.textContent.trim():null, vide:m?m.classList.contains('ph-vide'):null, verbe:(document.querySelector('#csPhrase .ph-b')||{}).textContent, autres:['#csBotBar','#csPinceau','#createSheet .ph-hint','#createSheet .ph-photo-btn','#createSheet .ph-b svg','#createSheet .pp-garder'].filter(v)}; }")
    juge('[%s] S · sur la page +, « Plus tard » est là, sous le doigt' % T, any('Plus tard' in s for s in e['sorties']), str(e['sorties']))
    juge('[%s] P · la vraie page + s\'ouvre sur un Promi à soi, onboarding refermé (verrou posé)' % T, e['cs'] and not e['onb'] and e['verrou'] == '1' and ft and 'Je me promets' in (ft['verbe'] or ''), str(ft))
    juge('[%s] F · la phrase fantôme est l\'une des trois, en pastille vide' % T, bool(ft) and ft['txt'].replace(' ','') in [x.replace(' ','') for x in FANTOMES] and ft['vide'] is True, str(ft and ft['txt']))
    juge('[%s] F · rien d\'autre n\'est montré (ni Peaufiner, ni pinceau, ni photo, ni retournement)' % T, bool(ft) and not ft['autres'], str(ft and ft['autres']))
    juge('[%s] D · au départ, la barre ne porte que le +' % T, e['barre'] == {'plus': True, 'index': False, 'aura': False, 'studio': False, 'fil': False} or not e['barre']['plus'], str(e['barre']))
    p = point(pg, '#csPhrase [data-ph=titre]')
    if p: toucher(cdp, pg, p[0], p[1]); touchers += 1
    pg.wait_for_timeout(900)
    ft2 = pg.evaluate("()=>{ const m=document.querySelector('#csPhrase [data-ph=titre]'); return {txt:m?m.textContent.trim():null, vide:m?m.classList.contains('ph-vide'):null, t:(window._phrase||{}).titre, f:(document.getElementById('fTitle')||{}).value, choix:!!document.querySelector('#csChoix.ouvert, #createSheet.pp-ouvert')}; }")
    juge('[%s] F · un toucher sur le fantôme le remplit (la phrase, le champ)' % T, bool(ft) and ft2['t'] in FANTOMES and ft2['t'].replace(' ','') == ft['txt'].replace(' ','') and ft2['f'] == ft2['t'] and ft2['vide'] is False, str(ft2))
    pg.wait_for_timeout(1500); m1 = pg.evaluate(ETAT)['main']; cap(pg, '4-page-plus-remplie-' + th)
    au = pg.evaluate("()=>{ const v=(s)=>{const e=document.querySelector(s); if(!e) return false; const r=e.getBoundingClientRect(), c=getComputedStyle(e); return r.width>4&&r.height>4&&c.display!=='none'&&c.visibility!=='hidden';}; return ['#csBotBar','#csPinceau','#createSheet .ph-hint','#createSheet .ph-photo-btn','#createSheet .ph-b svg','#createSheet .pp-garder'].filter(v); }")
    juge('[%s] F · la phrase remplie : toujours rien d\'autre (ni « garder de côté »)' % T, not au, str(au))
    juge('[%s] M · la main fantôme accompagne le trait qui plante' % T, m1 == 'planter', str(m1))
    P = pg.evaluate(ONDE_PP)
    if P: tracer(cdp, pg, P); traits += 1
    try: pg.wait_for_function("()=>{const d=document.getElementById('detailPoster'); return d&&d.classList.contains('show')&&typeof cur!=='undefined'&&cur&&!!document.getElementById('e2Ligne')}", timeout=12000)
    except Exception: pass
    pg.wait_for_timeout(1600)
    e = pg.evaluate(ETAT); note(e); sortie('4 · la fiche', e); cap(pg, '5-fiche-' + th)
    info = pg.evaluate("()=>{ try{ return {id:cur.id, titre:cur.title, st:cur.status, dans:promises.some(p=>p.id===cur.id), who:cur.who}; }catch(e){ return null; } }")
    juge('[%s] R · la parole est RÉELLE : plantée, un id, dans les paroles ; sa fiche est ouverte, une ligne dessous' % T, e['dp'] and e['n'] == 1 and bool(info) and info['dans'] and info['id'] is not None and info['st'] != 'tenu' and 'ligne' in e['eng'], str(info))
    juge('[%s] S · sur la fiche, « Plus tard » est là, sous le doigt, et le Fil n\'est pas encore paru' % T, any('Plus tard' in s for s in e['sorties']) and not e['barre']['fil'], '%s · %s' % (e['sorties'], e['barre']))
    juge('[%s] D · après la plantation, l\'Index est dans la barre' % T, e['barre']['index'] and not e['barre']['aura'], str(e['barre']))
    pg.wait_for_timeout(1400); m2 = pg.evaluate(ETAT)['main']
    juge('[%s] M · la main fantôme accompagne le trait qui tient' % T, m2 == 'tenir', str(m2))
    if m2: cap(pg, '6-fiche-main-' + th)
    P = pg.evaluate(ONDE_FI)
    if P: tracer(cdp, pg, P); traits += 1
    try: pg.wait_for_function("()=>{ try{ return cur&&cur.status==='tenu'&&!window._tenirAnime&&window._e2.etat().etat==='fin'; }catch(e){ return false; } }", timeout=12000)
    except Exception: pass
    pg.wait_for_timeout(900)
    e = pg.evaluate(ETAT); note(e); sortie('5 · la dernière ligne', e); cap(pg, '7-tenu-' + th)
    juge('[%s] R · le trait TIENT la parole ; la dernière ligne paraît' % T, e['tenu'] == 1 and 'ligne' in e['eng'] and e['e2'] and e['e2']['etat'] == 'fin', '%s · %s' % (e['tenu'], e['textes']))
    juge('[%s] C · du principe au premier tenu : %d toucher(s) (≤ %d) et %d trait(s) — planter est un trait, tenir en est un autre' % (T, touchers, TOUCHERS_MAX, traits), touchers <= TOUCHERS_MAX and traits == 2 and e['tenu'] == 1, '')
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left+r.width/2, r.top+r.height*0.5]}")
    toucher(cdp, pg, d[0], d[1]); pg.wait_for_timeout(1400)
    e = pg.evaluate(ETAT); note(e); sortie('6 · le compte', e); cap(pg, '8-compte-' + th)
    juge('[%s] R · un toucher ferme : `ob_fini` posé, le compte « Garder ta Toile » se propose' % T, e['obfini'] == '1' and not e['dp'] and e['compte'], '%s · %s' % (e['obfini'], e['sorties']))
    p = point(pg, '.onbv-compte .tard')
    if p: toucher(cdp, pg, p[0], p[1])
    pg.wait_for_timeout(2600)
    try: pg.wait_for_function("()=>{ const m=document.querySelector('#gesteFantome [data-main]'); return !!m && m.getAttribute('visibility')!=='hidden'; }", timeout=6000)
    except Exception: pass
    e = pg.evaluate(ETAT); note(e); cap(pg, '9-accueil-aura-' + th)
    juge('[%s] D · après le premier tenu, l\'Aura est dans la barre, et la main la désigne' % T, e['barre']['plus'] and e['barre']['index'] and e['barre']['aura'] and e['main'] == 'aura-apparait', '%s · main %s · fond %s' % (e['barre'], e['main'], e['fond']))
    if plein:
        p = point(pg, '#souffleBtn'); toucher(cdp, pg, p[0], p[1]); pg.wait_for_timeout(4500)
        x = point(pg, '#auraScreen .closeb')
        if x: toucher(cdp, pg, x[0], x[1])
        else: pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }")
        pg.wait_for_timeout(2800)
        e = pg.evaluate(ETAT); note(e); cap(pg, '10-accueil-studio-' + th)
        juge('[%s] D · au retour de l\'Aura, le Studio paraît, avec son invitation' % T, e['barre']['studio'] and 'invite' in e['eng'], '%s · %s' % (e['barre'], [t for t in e['textes'] if 'Studio' in t]))
        pg.evaluate("()=>{ document.querySelector('#accChoix .acc-pil[data-k=promi]').click(); }"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{ const P=window._phrase; const b=document.querySelector('#csPhrase [data-ph=sens]'); if(b) b.click(); }"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ window._phrase.titre='venir dimanche'; window._phrase.qui='Marion'; const t=document.getElementById('fTitle'); t.value='venir dimanche'; t.dispatchEvent(new Event('input',{bubbles:true})); const w=document.getElementById('fWho'); if(w){ w.value='Marion'; w.dispatchEvent(new Event('input',{bubbles:true})); } try{ window.newWhoSel=['Marion']; }catch(e){} try{ _phraseRendu(); }catch(e){} document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(1500)
        e = pg.evaluate(ETAT); note(e); cap(pg, '11-accueil-tout-' + th)
        qui = pg.evaluate("()=>promises.filter(p=>!p.draft).map(p=>p.who)")
        juge('[%s] D · à la première parole adressée à quelqu\'un, le Fil paraît : à la fin, TOUT est visible' % T, all(e['barre'].values()) and e['fond'] == [24, 366], '%s · fond %s · à %s' % (e['barre'], e['fond'], qui))
        perdus = [i for i in range(1, len(barres)) for k in barres[i] if barres[i - 1].get(k) and not barres[i][k] and (barres[i]['plus'] and barres[i - 1]['plus'])]
        juge('[%s] D · rien ne disparaît d\'une étape à l\'autre' % T, not perdus, str(perdus))
        pg.reload(); pg.wait_for_timeout(6800); e = pg.evaluate(ETAT)
        juge('[%s] R · rechargée : aucun onboarding, les paroles et la barre sont là' % T, not e['onb'] and e['n'] == 2 and all(e['barre'].values()) and e['e2'] and e['e2']['etat'] is None, '%s · %d parole(s)' % (e['barre'], e['n']))
    juge('[%s] A · A2 — aucun nœud du chantier n\'est transparent, en fondu ou animé' % T, not A2, ' | '.join(sorted(set(A2))[:5]))
    mauvais = a3(sorted(set(TX)))
    juge('[%s] A · A3 — aucun texte du parcours à l\'impératif (%d textes)' % (T, len(set(TX))), len(set(TX)) >= 6 and not mauvais, ' | '.join(mauvais[:4]))
    juge('[%s] aucune erreur de page' % T, not er, str(er[:2]))
    ctx.close()
def plus_tard(b, etape):
    ctx, pg, cdp, er = ouvre(b, 'light')
    if etape >= 2: prenom(pg, cdp)
    if etape >= 3:
        p = point(pg, '[data-onb="e2-suite"]'); toucher(cdp, pg, p[0], p[1])
        try: pg.wait_for_function("()=>{const s=document.getElementById('createSheet'); return s&&s.classList.contains('show')&&s.classList.contains('pp-promi')&&!s.classList.contains('acc-passe')&&!!document.getElementById('e2Tard')}", timeout=9000)
        except Exception: pass
        pg.wait_for_timeout(900)
    if etape >= 4:
        p = point(pg, '#csPhrase [data-ph=titre]'); toucher(cdp, pg, p[0], p[1]); pg.wait_for_timeout(1200)
        P = pg.evaluate(ONDE_PP); tracer(cdp, pg, P)
        try: pg.wait_for_function("()=>{const d=document.getElementById('detailPoster'); return d&&d.classList.contains('show')&&!!document.getElementById('e2Ligne')}", timeout=12000)
        except Exception: pass
        pg.wait_for_timeout(1500)
    sel = '#onbTard' if etape <= 2 else '#e2Tard'
    p = point(pg, sel)
    if p: toucher(cdp, pg, p[0], p[1])
    pg.wait_for_timeout(2600)
    e = pg.evaluate(ETAT); nom = ['', 'au prénom', 'au principe', 'sur la page +', 'sur la fiche'][etape]
    juge('T · « Plus tard » %s : un toucher, l\'accueil, TOUT est visible d\'emblée, `ob_fini` posé' % nom, bool(p) and not e['onb'] and not e['cs'] and not e['dp'] and all(e['barre'].values()) and e['obfini'] == '1' and e['verrou'] == '1', '%s · ob_fini %s' % (e['barre'], e['obfini']))
    if etape in (1, 4):
        pg.reload(); pg.wait_for_timeout(6800); e = pg.evaluate(ETAT)
        juge('T · « Plus tard » %s, rechargée : rien n\'est rejoué ni redemandé' % nom, not e['onb'] and all(e['barre'].values()) and not e['cs'], str(e['barre']))
    ctx.close()
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    parcours(b, 'light')
    if not VITE:
        parcours(b, 'dark')
        for n in (1, 2, 3, 4): plus_tard(b, n)
    b.close()
sans = [n for n, c, _ in sorties if not c]
juge('S · R6 — une sortie visible, sous le doigt, à chaque étape (%d étapes)' % len(sorties), len(sorties) >= 6 and not sans, 'sans sortie : %s' % (sans or 'aucune'))
if R6:
    print('R6 %s · %d étapes · sans sortie : %s' % ('OK' if (len(sorties) >= 6 and not sans) else 'KO', len(sorties), sans or 'aucune'))
    for n, c, s in sorties: print('     R6 · %-26s %s' % (n, ('sortie : ' + ', '.join(s)) if c else 'AUCUNE sortie visible'))
    sys.exit(0 if (len(sorties) >= 6 and not sans) else 1)
for n, c, s in sorties: print('     R6 · %-26s %s' % (n, ('sortie : ' + ', '.join(s)) if c else 'AUCUNE sortie visible'))
print('\n%d/%d' % (ok, ok + len(ko)))
if ko: sys.exit(1)
