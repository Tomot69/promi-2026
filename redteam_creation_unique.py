#!/usr/bin/env python3
"""⚑ v211 (C-306, Tom, 19 nov. 2026) — « quand je crée un Cercle, un Promi brouillon apparaît dans le Fil, et deux dalles sont créées ».
Critère de Tom : créer un Cercle crée UNIQUEMENT le Cercle — une parole, une dalle, une ligne de Fil. Et de même pour chaque chemin de création.

Chaque chemin, par le VRAI chemin (la pilule de l'accueil, la saisie de la phrase, le trait tracé ; « + Planter dans le Cercle », son menu, le trait), sur un état
vierge et sur l'état exporté de Tom : on compte, avant et après (la page + fermée, 2,5 s après) —
  · les paroles (promesses non gardées de côté) + les Cercles nommés : exactement +1 (le Cercle compte pour sa parole) ;
  · les gardés de côté (brouillons) : +0 ;
  · les dalles de la Toile (graines reliées à une parole ou à un Cercle) : exactement +1 ;
  · les lignes du Fil : exactement +1.
`--fichier=` sert une autre version (bissection) ; `--seul=` un chemin (promi, chiche, nuee, cercle-promi, cercle-chiche) ; `--etats=vierge,tom`."""
import sys, json
from playwright.sync_api import sync_playwright
import banc_tom as B

F = 'app.html'; SEUL = None; ETATS = ['vierge', 'tom']
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
    if a.startswith('--seul='): SEUL = a.split('=', 1)[1].split(',')
    if a.startswith('--etats='): ETATS = a.split('=', 1)[1].split(',')
CHEMINS = ['nuee', 'promi', 'chiche', 'cercle-promi', 'cercle-chiche']
if SEUL: CHEMINS = [c for c in CHEMINS if c in SEUL]
COMPTE = """()=>{ const P=promises.filter(p=>!p.draft), D=promises.filter(p=>p.draft), N=Object.keys(NUE||{}).filter(k=>NUE[k]);
  let g=[]; try{ g=(window.Toile_graines?Toile_graines():[]).filter(s=>s[3]!=='gray' && (s[0]!=null || s[3]==='nuee')); }catch(e){}
  let f=null; try{ f=(typeof FEED!=='undefined'&&FEED)?FEED.length:null; }catch(e){}
  return {paroles:P.length, cercles:N.length, brouillons:D.length, dalles:g.length, fil:f, titres:P.slice(-3).map(p=>p.title+(p.nuee?'@'+p.nuee:'')), br:D.slice(-3).map(p=>p.title)}; }"""
OUVRE = """async (nat)=>{ const w=ms=>new Promise(r=>setTimeout(r,ms)); try{closeAll()}catch(e){} await w(400);
  if(nat.startsWith('cercle-')){ const k=Object.keys(NUE).filter(k=>NUE[k])[0]; if(!k) return 'pas de Cercle'; window.openNueeDetail(k); await w(2500);
    const b=document.getElementById('nqAddPromi')||[...document.querySelectorAll('#detailPoster button,#detailPoster div')].find(e=>/Planter dans le Cercle/.test(e.textContent||'')&&e.children.length<4);
    if(!b) return 'pas de bouton'; b.click(); await w(700);
    const m=nat.endsWith('chiche')?'chiche':'promi', c=[...document.querySelectorAll('#cpChoix [data-k], #cpChoix .acc-pil')].find(e=>(e.dataset.k||'')===m || new RegExp(m,'i').test(e.textContent||''));
    if(!c) return 'pas de menu'; c.click(); }
  else { const p=document.querySelector('#accChoix .acc-pil[data-k='+nat+']'); if(!p){ document.getElementById('createBtn').click(); await w(700); } (document.querySelector('#accChoix .acc-pil[data-k='+nat+']')).click(); }
  const k=nat==='nuee'?'nuee':(nat.endsWith('chiche')?'chiche':'promi');
  for(let i=0;i<80;i++){ await w(60); const c=document.getElementById('createSheet'); if(c.classList.contains('show')&&c.classList.contains('pp-'+k)&&!c.classList.contains('acc-passe')) break; }
  await w(700); return 'ok'; }"""
SAISIT = """async (a)=>{ const [nat,t]=a, w=ms=>new Promise(r=>setTimeout(r,ms)), n=nat==='nuee';
  const m=document.querySelector(n?'#nueePhrase .ph-m[data-np="nom"]':'#csPhrase .ph-m[data-ph="titre"]'); if(!m) return 'pas de place'; m.click(); await w(300);
  const i=document.getElementById(n?'nueeNomIn':'phIn'); i.value=t; if(i.oninput) i.oninput(); i.dispatchEvent(new Event('input',{bubbles:true})); await w(200); i.blur(); await w(1600); return 'ok'; }"""
TRACE = """async (nat)=>{ const w=ms=>new Promise(r=>setTimeout(r,ms)), z=document.getElementById(nat==='nuee'?'planterZoneN':'planterZone'); if(!z) return 'pas de zone';
  const c=z.querySelector('canvas')||z, r=c.getBoundingClientRect(), y=r.top+r.height/2, x0=r.left+20, L=r.width-40;
  const ev=(n,x)=>new MouseEvent(n,{bubbles:true,cancelable:true,clientX:x,clientY:y,view:window});
  z.dispatchEvent(ev('mousedown',x0)); for(let i=1;i<=24;i++){ window.dispatchEvent(ev('mousemove',x0+L*i/24)); await w(16); } window.dispatchEvent(ev('mouseup',x0+L)); await w(3500); try{closeAll()}catch(e){} await w(1500); return 'ok'; }"""
R = []
def juge(nom, ok, det=''):
    R.append(ok); print(('✅' if ok else '❌'), nom, '' if ok else det, flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    for etat in ETATS:
        for ch in CHEMINS:
            if etat == 'tom':
                ctx, d = B.contexte_tom(b, echelle=1)
                if not ctx: juge('[tom] un état exporté', False); continue
            else:
                ctx = B.contexte(b, vw=430, vh=932, stockage={'promi_rappel_fin': '1'})
                ctx.add_init_script("try{ if(!sessionStorage.getItem('__v0')){ sessionStorage.setItem('__v0','1'); localStorage.removeItem('promi_state'); } }catch(e){}")
            pg = B.ouvre(ctx, F)
            T = '[%s · %s]' % (etat, ch)
            try:
                if ch.startswith('cercle-') and not pg.evaluate("()=>Object.keys(NUE||{}).filter(k=>NUE[k]).length"):
                    pg.evaluate(OUVRE, 'nuee'); pg.evaluate(SAISIT, ['nuee', 'le potager']); pg.evaluate(TRACE, 'nuee'); pg.wait_for_timeout(800)
                a = pg.evaluate(COMPTE)
                o = pg.evaluate(OUVRE, ch)
                nat = 'nuee' if ch == 'nuee' else 'promi'
                t = 'essai %s %d' % (ch, len(R))
                s = pg.evaluate(SAISIT, [nat, t]); tr = pg.evaluate(TRACE, nat)
                z = pg.evaluate(COMPTE)
                dp = (z['paroles'] + z['cercles']) - (a['paroles'] + a['cercles']) if ch == 'nuee' else z['paroles'] - a['paroles']
                det = 'chemin %s/%s/%s · avant %s · après %s' % (o, s, tr, a, z)
                juge(T + ' une parole de plus (%+d), aucun gardé de côté (%+d)' % (dp, z['brouillons'] - a['brouillons']), dp == 1 and z['brouillons'] == a['brouillons'] and (ch != 'nuee' or z['paroles'] == a['paroles']), det)
                juge(T + ' une dalle de plus (%+d)' % (z['dalles'] - a['dalles']), z['dalles'] - a['dalles'] == 1, det)
                juge(T + ' une ligne de Fil de plus (%+s)' % ((z['fil'] - a['fil']) if z['fil'] is not None else '?'), z['fil'] is not None and z['fil'] - a['fil'] == 1, det)
            except Exception as e:
                juge(T + ' le chemin se joue', False, str(e)[:300])
            ctx.close()
    b.close()
print('\n%d/%d' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
