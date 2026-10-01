#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_accueil.py — L'ACCUEIL, DIRECTION B (PLANCHE-ACCUEIL-2, décisions Tom Q212 · Q213, 13 sept. 2026). AU DOIGT.

  1 · LE CHROME À SES COTES (en dur, §7) — plateau 24·40·342×60 (v95, Tom : « refais le PROMI pour qu'il soit harmonieux dans son encart » — original sauvegardes/redteam_accueil-avant-v95.py) · barre 24·736·342×88 · + 68 à 161·746, sur la ligne
      des entrées (écart de centre ≤ 1) · entrées centrées 70 · 124 | 266 · 320 · libellés 12 · plus aucune paire sous 8
  2 · LES PORTES, AU DOIGT — Studio, Aura, Index, Fil, Partager, Réglages ouvrent leur écran
  3 · LE + S'OUVRE SUR PLACE — il ne quitte pas l'écran, il reste un + ; chaque nature ouvre SA phrase, dans trois ordres
  4 · CE QUI PART — barre d'état, sélecteur Toile/Index, rond du Cercle, libellé vertical, voiles et flous du chrome
  5 · LES PORTES CACHÉES SONT FERMÉES — l'appui long sur la Toile n'ouvre pas le Studio ; un mode signature enregistré
      ne se rallume pas au chargement
  6 · « N paroles · N Nuées » — la même ligne que l'Index
  7 · TOUTE DALLE RESTE ATTEIGNABLE sous le nouveau chrome, à dix zooms (le calcul exact de l'audit)

Preuve (§7) : `APP_ACC=http://127.0.0.1:8752/sauvegardes/app-avant-lot-accueil.html` doit ROUGIR.
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_ACC', "http://127.0.0.1:8752/app.html")
ok = [0]; ko = []
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad', 'accueil_audit.py')).read().split('CMDS = [')[0].split('APP = ')[0])
exec('MASK_JS = ' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad', 'accueil_audit.py')).read().split('MASK_JS = ')[1].split('# D —')[0])
exec('REACH_JS = ' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad', 'accueil_audit.py')).read().split('REACH_JS = ')[1].split('CMDS = [')[0])


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-60s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-60s KO  %s' % (nom, detail))


GEO = r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
 const B=e=>{if(!e)return null;const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden')return null;const r=e.getBoundingClientRect();if(r.width<2)return null;return {x:(r.left-D.left)/k,y:(r.top-D.top)/k,w:r.width/k,h:r.height/k};};
 const ink=e=>{const rg=document.createRange();rg.selectNodeContents(e);const r=rg.getBoundingClientRect();return {x0:(r.left-D.left)/k,x1:(r.right-D.left)/k,y0:(r.top-D.top)/k,y1:(r.bottom-D.top)/k};};
 const ids=['studioBtn','souffleBtn','indexBtn','filBtn'];
 const ent=ids.map(i=>{const e=document.getElementById(i);const b=B(e);const l=e&&e.querySelector('.l');return {i,b,lab:l?ink(l):null,fs:l?getComputedStyle(l).fontSize:null};});
 const vis=s=>{const e=document.querySelector(s);if(!e)return false;const c=getComputedStyle(e);const r=e.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.05&&r.width>2&&r.height>2;};
 const flou=[...document.querySelectorAll('#accPlat, #accBarre, #accBarre *, #accPlat *')].filter(e=>{const c=getComputedStyle(e);return (c.backdropFilter&&c.backdropFilter!=='none')||(c.webkitBackdropFilter&&c.webkitBackdropFilter!=='none');}).length;
 return {plat:B(document.getElementById('accPlat')),barre:B(document.getElementById('accBarre')),plus:B(document.getElementById('createBtn')),ent,
   statusbar:vis('#device .statusbar'),viewSwitch:vis('#viewSwitch'),cercle:vis('#cercleTopBtn'),sidelabel:vis('#sidelabel'),fades:vis('.stage-fade-b')||vis('.stage-fade-t'),flou,
   ligne:(document.getElementById('accLigne')||{}).textContent||null,
   attendu:(()=>{const n=promises.filter(p=>!p.req&&!p.draft).length,m=Object.keys(NUE).length;return n+' parole'+(n>1?'s':'')+' · '+m+' Nuée'+(m>1?'s':'');})()};}"""


def ouvre(b, th, sig=False):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    if sig:
        # ⚠ l'amorce du premier lancement allume PUIS ÉTEINT le mode : sans `promi_sigdemo`, la sonde passait sur la version
        #   fautive. On joue le cas réel — quelqu'un qui a déjà vu l'amorce et laissé le mode allumé.
        ctx.add_init_script("try{localStorage.setItem('promi_sig','1');localStorage.setItem('promi_sigdemo','1');}catch(e){}")
    pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);}", th)
    pg.wait_for_timeout(1500)
    return ctx, pg, ctx.new_cdp_session(pg)


def doigt(pg, cdp, sel, duree=0):
    pt = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}", sel)
    if not pt: return False
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt[0], 'y': pt[1]}]})
    if duree: pg.wait_for_timeout(duree)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    return True


with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        T = 'clair' if th == 'light' else 'sombre'
        ctx, pg, cdp = ouvre(b, th)
        g = pg.evaluate(GEO)
        pl, br, pu = g['plat'], g['barre'], g['plus']
        c1 = bool(pl and br and pu) and abs(pl['x'] - 24) <= 1 and abs(pl['y'] - 40) <= 1 and abs(pl['w'] - 342) <= 1 and abs(pl['h'] - 60) <= 1 \
            and abs(br['x'] - 24) <= 1 and abs(br['y'] - 736) <= 1 and abs(br['w'] - 342) <= 1 and abs(br['h'] - 88) <= 1 \
            and abs(pu['w'] - 68) <= 1 and abs(pu['x'] - 161) <= 1 and abs(pu['y'] - 746) <= 1
        t('[%s] 1 · plateau, barre, + à leurs cotes' % T, c1, 'plateau %s · barre %s · + %s' % (pl, br, pu))
        cent = [round(e['b']['x'] + e['b']['w'] / 2, 1) if e['b'] else None for e in g['ent']]
        ligne_ok = all(e['b'] for e in g['ent']) and all(abs(c - v) <= 1.5 for c, v in zip(cent, [70, 124, 266, 320]))
        cy_ent = [e['b']['y'] + e['b']['h'] / 2 for e in g['ent'] if e['b']]
        cy_plus = pu['y'] + pu['h'] / 2 if pu else 0
        t('[%s] 1 · entrées centrées 70·124|266·320, + sur leur ligne' % T, ligne_ok and cy_ent and all(abs(c - cy_plus) <= 1 for c in cy_ent), 'centres %s · écart de ligne %s' % (cent, [round(c - cy_plus, 1) for c in cy_ent]))
        labs = [e['lab'] for e in g['ent']]
        airs = []
        if all(labs):
            airs.append(labs[1]['x0'] - labs[0]['x1']); airs.append(labs[3]['x0'] - labs[2]['x1'])
            airs.append(labs[0]['x0'] - (br['x'] + 2)); airs.append((br['x'] + br['w'] - 2) - labs[3]['x1'])
            airs.append((br['y'] + br['h'] - 2) - max(l['y1'] for l in labs))
        t('[%s] 1 · libellés 12, aucune paire sous 8' % T, all(e['fs'] == '12px' for e in g['ent']) and airs and min(airs) >= 8, 'airs %s' % [round(a, 1) for a in airs])
        t('[%s] 4 · ce qui part : barre d\'état, Toile/Index, Cercle, libellé vertical, voiles, flous' % T,
          not (g['statusbar'] or g['viewSwitch'] or g['cercle'] or g['sidelabel'] or g['fades']) and g['flou'] == 0,
          'statusbar %s · viewSwitch %s · cercle %s · sidelabel %s · voiles %s · flous %d' % (g['statusbar'], g['viewSwitch'], g['cercle'], g['sidelabel'], g['fades'], g['flou']))
        # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (v89, Tom 27 sept. — Q347) : la phrase « N paroles · N Nuées » est retirée de l'accueil.
        _lv = pg.evaluate("()=>{const e=document.getElementById('accLigne'); if(!e) return false; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return c.display!=='none'&&c.visibility!=='hidden'&&r.width>1&&r.height>1;}")
        t('[%s] 6 · la ligne « N paroles · N Nuées » est retirée (Q347)' % T, not _lv)
        # 2 · les portes
        portes = [('#studioBtn', "()=>document.getElementById('studioScreen').classList.contains('show')"),
                  ('#souffleBtn', "()=>document.getElementById('auraScreen').classList.contains('show')"),
                  ('#indexBtn', "()=>document.getElementById('indexSheet').classList.contains('show')"),
                  ('#filBtn', "()=>document.getElementById('feedView').classList.contains('in')"),
                  ('#shareBtn', "()=>document.getElementById('shareScreen').classList.contains('show')"),
                  ('#settingsBtn', "()=>document.getElementById('settingsScreen').classList.contains('show')")]
        mortes = []
        for sel, test in portes:
            pg.evaluate("()=>{try{setView('toile')}catch(e){}; if(window.quitteVues)quitteVues(); document.querySelectorAll('.screen.show').forEach(x=>x.classList.remove('show'));}")
            pg.wait_for_timeout(700)
            if not doigt(pg, cdp, sel): mortes.append(sel + ' absent'); continue
            pg.wait_for_timeout(1500)
            if not pg.evaluate(test): mortes.append(sel)
        t('[%s] 2 · les six portes ouvrent leur écran, au doigt' % T, not mortes, 'mortes : %s' % mortes)
        pg.evaluate("()=>{try{setView('toile')}catch(e){}; if(window.quitteVues)quitteVues(); document.querySelectorAll('.screen.show').forEach(x=>x.classList.remove('show'));}")
        pg.wait_for_timeout(800)
        # 3 · le + sur place
        doigt(pg, cdp, '#createBtn'); pg.wait_for_timeout(900)
        st = pg.evaluate("()=>{const c=document.getElementById('accChoix');const s=document.getElementById('createSheet');const svg=document.querySelector('#createBtn svg');return {ouvert:!!c&&c.classList.contains('ouvert'),sheet:s.classList.contains('show'),tr:svg?getComputedStyle(svg).transform:null};}")
        t('[%s] 3 · le + ouvre les natures sur place, reste un +' % T, st['ouvert'] and not st['sheet'] and st['tr'] in ('none', None), str(st))
        VERBE = {'promi': 'Je me promets', 'chiche': 'Chiche', 'nuee': 'Je lance une Nuée'}
        rates = []
        for ordre in (['promi', 'chiche', 'nuee'], ['nuee', 'promi', 'chiche'], ['chiche', 'nuee', 'promi']):
            for k in ordre:
                pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(800)
                if not pg.evaluate("()=>{const c=document.getElementById('accChoix');return !!c&&c.classList.contains('ouvert');}"):
                    doigt(pg, cdp, '#createBtn'); pg.wait_for_timeout(900)
                if not doigt(pg, cdp, '.acc-pil[data-k=%s]' % k): rates.append(k + ' sans tuile'); continue
                pg.wait_for_timeout(2600)
                r = pg.evaluate("""()=>{const s=document.getElementById('createSheet');const v=s.classList.contains('pp-nuee')?document.querySelector('#nueePhrase'):document.querySelector('#csPhrase .ph-b');
                    return {k:s.dataset.kind,cls:[...s.classList].filter(c=>/^pp/.test(c)),v:v?(v.innerText||'').trim().split('\\n')[0]:''};}""")
                if not (r['k'] == k and ('pp-' + k) in r['cls'] and 'pp-choix' not in r['cls'] and r['v'].startswith(VERBE[k])):
                    rates.append('%s→%s' % (k, r))
        t('[%s] 3 · chaque nature ouvre SA phrase, trois ordres, au doigt' % T, not rates, 'ratées : %s' % rates[:3])
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(800)
        # 5 · l'appui long
        pt = pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;return [D.left+195*k, D.top+440*k];}")
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt[0], 'y': pt[1]}]})
        pg.wait_for_timeout(900)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(900)
        studio = pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('show')")
        t('[%s] 5 · l\'appui long sur la Toile n\'ouvre pas le Studio' % T, not studio, 'Studio ouvert : %s' % studio)
        pg.evaluate("()=>{if(window.quitteVues)quitteVues(); document.querySelectorAll('.screen.show').forEach(x=>x.classList.remove('show'));}")
        # 7 · l'atteinte
        pg.wait_for_timeout(800)
        m = pg.evaluate(MASK_JS)
        A = pg.evaluate(REACH_JS, [m['rows'], [0.4, 0.48, 0.6, 0.8, 1.0, 1.25, 1.5, 2, 3, 5]])
        inat = {s: len(z['inatteignables']) for s, z in A['zooms'].items() if z['inatteignables']}
        t('[%s] 7 · toute dalle atteignable, dix zooms' % T, not inat and A['zooms'], '%d dalles · inatteignables %s' % (next(iter(A['zooms'].values()))['n'], inat))
        ctx.close()
        # 5 · le mode signature enregistré ne revient pas
        ctx, pg, cdp = ouvre(b, th, sig=True)
        pg.wait_for_timeout(1500)
        sg = pg.evaluate("()=>document.getElementById('device').classList.contains('sigmode')")
        t('[%s] 5 · un mode signature enregistré ne se rallume pas' % T, not sg, 'sigmode %s' % sg)
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
