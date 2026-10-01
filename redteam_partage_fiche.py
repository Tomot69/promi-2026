#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_partage_fiche.py — LE ROND « PARTAGER » D'UNE FICHE PARTAGE, AU DOIGT (v117, Tom, 1er oct. 2026).

« Les boutons Partager des fiches ne font rien — Promi, Chiche, Cercle. Corrige. Et vérifie que l'image produite
ressemble à ce que donne Mon Folio quand on ne garde qu'une dalle. »

Pour un Promi, un Chiche et un Cercle, au VRAI DOIGT (WebKit : `touchscreen.tap` ; Chromium : CDP `Input.dispatchTouchEvent`)
puis à la souris (témoin) :
  A · le toucher sur le rond ouvre l'écran Partager (`#shareScreen.show`), sujet « Mon Folio » (`shareMode = mosaic`)
  B · la planche composée porte EXACTEMENT les paroles de la fiche (un Promi : sa case seule ; un Cercle : ses Promi),
      sans la Pelote — lu dans la composition publiée (pointeur), puis VÉRIFIÉ sur les `fillText` réellement tracés
  C · l'image exportée = celle de Mon Folio réduit à la main aux mêmes paroles (mêmes peintres) : horloge figée pendant
      les deux exports, écart moyen ≤ ECART_MAX niveaux sur l'image réduite au 1/8
  D · à la fermeture, l'écran Partager PERD `.show`, et ce que l'utilisateur avait choisi (`shareHidden`, le sujet,
      la Pelote) est rendu à l'identique ; rien de la réduction n'a été sauvegardé entre-temps
Preuve (§7) : copier `sauvegardes/app-avant-v117b.html` À LA RACINE (depuis sauvegardes/, promi-moteur.js n'est pas trouvé)
puis `APP=http://127.0.0.1:8752/<copie>.html python3 redteam_partage_fiche.py` doit ROUGIR (12/30).
"""
import os, sys, json
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
ECART_MAX = 4.0           # niveaux (0–255), moyenne sur l'image réduite — décidé ici : même composition, mêmes peintres
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-66s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-66s KO  %s' % (nom, detail))


PIEGE = r"""()=>{ if(window.__ftPiege) return; window.__ftPiege=true; window.__ft=[];
  const f=CanvasRenderingContext2D.prototype.fillText;
  CanvasRenderingContext2D.prototype.fillText=function(s,x,y){ if(this.canvas && this.canvas.id==='shCanvas') window.__ft.push(String(s)); return f.apply(this,arguments); }; }"""

EXPORT = r"""()=>{ const pn=performance.now.bind(performance); performance.now=()=>123456;
  let cv=null; try{ cv=window._shExporteCanevas(); }catch(e){} performance.now=pn;
  if(!cv) return null; const w=Math.round(cv.width/8), h=Math.round(cv.height/8);
  const c=document.createElement('canvas'); c.width=w; c.height=h; const g=c.getContext('2d');
  g.drawImage(cv,0,0,w,h); return {w:cv.width,h:cv.height,d:Array.from(g.getImageData(0,0,w,h).data)}; }"""


def ouvre_fiche(pg, cible):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(600)
    if cible.startswith('n:'): pg.evaluate("(k)=>openNueeDetail(k)", cible[2:])
    else: pg.evaluate("(i)=>openDetail(i)", int(cible))
    pg.wait_for_timeout(1800)


def touche(pg, cdp, mode):
    bb = pg.evaluate("()=>{const e=document.querySelector('#dpDetails .dpd-part'); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width}}")
    if not bb or not bb['w']: return False
    if mode == 'doigt' and cdp is None:
        pg.touchscreen.tap(bb['x'], bb['y'])
    elif mode == 'doigt':
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': bb['x'], 'y': bb['y']}]})
        pg.wait_for_timeout(80)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    else:
        pg.mouse.click(bb['x'], bb['y'])
    pg.wait_for_timeout(1800)
    return True


def passe(b, mode):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=(mode == 'doigt'), accept_downloads=True)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.wait_for_timeout(800)
    cdp = ctx.new_cdp_session(pg) if b.browser_type.name == 'chromium' else None
    pg.evaluate(PIEGE)
    # un choix de l'utilisateur à rendre : un Promi masqué, la Pelote dans le Folio, sujet Ma Toile
    pg.evaluate("()=>{shareHidden={139:true,'n:potager':true}; window.shPelote=true; shareMode='toile'; try{saveState();}catch(e){}}")
    avant = pg.evaluate("()=>JSON.stringify({h:shareHidden,m:shareMode,p:!!window.shPelote})")
    cas = pg.evaluate("""()=>{const P=promises.filter(p=>!p.draft&&!p.req);
        const pr=P.find(p=>!p.chiche&&!p.nuee&&!p.photo), ch=P.find(p=>p.chiche&&!p.nuee);
        const k=Object.keys(NUE).find(k=>P.some(p=>p.nuee===k));
        return [['Promi',''+pr.id,[pr.id]],['Chiche',''+ch.id,[ch.id]],['Cercle','n:'+k,P.filter(p=>p.nuee===k).map(p=>p.id)]];}""")
    for nat, cible, ids in cas:
        tag = '[%s · %s]' % (mode, nat)
        ouvre_fiche(pg, cible)
        pg.evaluate("()=>{window.__ft=[];}")
        if not touche(pg, cdp, mode):
            t(tag + ' A · le rond Partager est là', False, 'introuvable'); continue
        e = pg.evaluate("""()=>{const s=document.getElementById('shareScreen'); const C=window._plancheComp||{};
            return {show:!!(s&&s.classList.contains('show')), mode:(typeof shareMode!=='undefined'?shareMode:null),
                    ids:(C.cases||[]).map(c=>c.id), mots:(C.cases||[]).map(c=>c.mot), pel:!!C.pelote, ft:(window.__ft||[]).slice()};}""")
        t(tag + ' A · l\'écran Partager s\'ouvre, sur Mon Folio', e['show'] and e['mode'] == 'mosaic', '%s %s' % (e['show'], e['mode']))
        traces = all(any(w in s for s in e['ft'] for w in m.split(' ')[:1]) for m in e['mots']) if e['mots'] else False
        t(tag + ' B · la planche porte exactement ces paroles, sans Pelote',
          sorted(e['ids']) == sorted(ids) and not e['pel'] and traces, 'composées %s attendues %s · tracés %s' % (sorted(e['ids']), sorted(ids), traces))
        sauve = pg.evaluate("()=>{try{return JSON.stringify(JSON.parse(localStorage.getItem('promi_state')).shareHidden)}catch(e){return null}}")
        pg.evaluate("()=>{try{saveState();}catch(e){}}")
        sauve2 = pg.evaluate("()=>{try{return JSON.stringify(JSON.parse(localStorage.getItem('promi_state')).shareHidden)}catch(e){return null}}")
        t(tag + ' D · la réduction n\'est jamais sauvegardée', sauve2 == json.dumps(json.loads(avant)['h'], separators=(',', ':')) or sauve2 == sauve, sauve2)
        if not e['show']: continue
        A = pg.evaluate(EXPORT)
        # fermeture
        pg.evaluate("()=>{const c=document.querySelector('#shareScreen .closeb'); if(c) c.click();}"); pg.wait_for_timeout(1200)
        apres = pg.evaluate("()=>JSON.stringify({h:shareHidden,m:shareMode,p:!!window.shPelote})")
        ferme = pg.evaluate("()=>!document.getElementById('shareScreen').classList.contains('show')")
        t(tag + ' D · fermé, le choix de l\'utilisateur est rendu', ferme and apres == avant, '%s · %s' % (ferme, apres))
        # la référence : Mon Folio réduit À LA MAIN aux mêmes paroles
        pg.evaluate("""(ids)=>{openShare(); document.querySelector('#shMode button[data-mode=mosaic]').click();
            const h={}; promises.forEach(p=>{ if(ids.indexOf(p.id)<0) h[p.id]=true; }); Object.keys(NUE).forEach(k=>h['n:'+k]=true);
            shareHidden=h; window.shPelote=false; shareRender();}""", ids)
        pg.wait_for_timeout(1500)
        B = pg.evaluate(EXPORT)
        if A and B and A['w'] == B['w'] and len(A['d']) == len(B['d']):
            n = len(A['d']); ec = sum(abs(A['d'][i] - B['d'][i]) for i in range(n)) / n
            t(tag + ' C · l\'image = Mon Folio réduit à la main', ec <= ECART_MAX, 'écart moyen %.2f niveaux · %d × %d' % (ec, A['w'], A['h']))
        else:
            t(tag + ' C · l\'image = Mon Folio réduit à la main', False, 'export %s / %s' % (A and (A['w'], A['h']), B and (B['w'], B['h'])))
        # on rend l'état de départ
        pg.evaluate("""(av)=>{const a=JSON.parse(av); shareHidden=a.h; window.shPelote=a.p;
            const c=document.querySelector('#shareScreen .closeb'); if(c) c.click(); shareMode=a.m;}""", avant)
        pg.wait_for_timeout(800)
    t('[%s] aucune erreur JS' % mode, not er, '; '.join(er)[:200])
    ctx.close()


with sync_playwright() as p:
    for moteur in ('webkit', 'chromium'):
        b = getattr(p, moteur).launch()
        print('=== %s' % moteur)
        for mode in ('doigt', 'souris'):
            if moteur == 'chromium' and mode == 'souris': continue
            passe(b, mode)
        b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ', '.join(ko)); sys.exit(1)
print('✅ le rond Partager d\'une fiche partage son Folio')
