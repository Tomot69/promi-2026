#!/usr/bin/env python3
"""redteam_suite_libelle.py — ⚑ v158 (Tom, C-176, Q567) : LE BOUTON → NE RECOUVRE PLUS « TRACE POUR PLANTER ».

« Clavier ouvert, le bouton → recouvre la fin de “trace pour planter”. Le texte doit rester entier et lisible, clavier ouvert comme fermé, sur toutes les
pages + et dans l'onboarding. Juge : aucun recouvrement entre le bouton et le libellé, clavier ouvert. »

Banc comme Tom (WebKit, 390 × 844 ×3, doigt), stockage vierge, le vrai parcours ; le clavier d'iOS SIMULÉ (`visualViewport` descend de 336 pt au focus,
comme dans redteam_clavier_onb), clair et sombre, une parole courte et une parole de trois lignes :
  A · clavier ouvert, la parole écrite : le bouton → (s'il est là) ne touche AUCUNE ligne de texte de la page — « trace pour planter », la phrase,
      « Petite ou grande promesse » — 4 pt d'air au moins ; il ne descend jamais sous la consigne (le trait est dessous) ; « trace pour planter » est entier ;
  B · clavier refermé : de même ;
  C · les pages + (Promi, Chiche, Cercle) : aucun bouton → ni autre bouton ne recouvre le libellé « trace pour … », clavier ouvert sur la phrase.
  D · ⚑ v159 (chef de chantier, Q568) : au-delà de trois lignes la parole se réduit (comme sur la page +) : elle tient en trois lignes, « Petite ou grande
      promesse » reste, au-dessus de la consigne, rien ne passe sur le trait. Une parole de cinq lignes est jugée (rouge sur v158 : 5 lignes à 35 px).
Preuve : `--fichier=zz-av157.html` rougit (A).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
CLAVIER = """(()=>{ const H=844, K=336, D=280; let h=H; const vv=new EventTarget(); Object.defineProperty(vv,'height',{get:()=>h}); Object.defineProperty(vv,'width',{get:()=>390});
  Object.defineProperty(vv,'scale',{get:()=>1}); Object.defineProperty(vv,'offsetTop',{get:()=>0}); Object.defineProperty(vv,'pageTop',{get:()=>0});
  try{ Object.defineProperty(window,'visualViewport',{get:()=>vv, configurable:true}); }catch(e){}
  let anim=0; function vers(c){ const h0=h, t0=performance.now(); cancelAnimationFrame(anim); (function f(){ const u=Math.min(1,(performance.now()-t0)/D); h=Math.round(h0+(c-h0)*(1-Math.pow(1-u,3))); vv.dispatchEvent(new Event('resize')); if(u<1) anim=requestAnimationFrame(f); })(); }
  document.addEventListener('focusin', e=>{ if(e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) setTimeout(()=>vers(H-K), 40); }, true);
  document.addEventListener('focusout', e=>{ if(e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) setTimeout(()=>vers(H), 30); }, true);
})()"""
MESURE = """(o)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const L=[];
  o.textes.forEach(id=>{ const e=document.querySelector(id); if(!e||getComputedStyle(e).display==='none'||getComputedStyle(e).visibility==='hidden') return; const rg=document.createRange(); rg.selectNodeContents(e);
    [...rg.getClientRects()].forEach(q=>{ if(q.width>1) L.push([id, (q.left-D.left)/k, (q.top-D.top)/k, (q.right-D.left)/k, (q.bottom-D.top)/k]); }); });
  const bt=[]; o.boutons.forEach(s=>document.querySelectorAll(s).forEach(b=>{ const c=getComputedStyle(b); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return; const r=b.getBoundingClientRect(); if(r.width<2) return; bt.push([s,(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k]); }));
  const tr=document.querySelector(o.libelle); let entier=null; if(tr && getComputedStyle(tr).display!=='none'){ const r=tr.getBoundingClientRect(); entier=(r.left-D.left)/k>=0 && (r.right-D.left)/k<=390 && tr.scrollWidth<=tr.clientWidth+1; }
  const touche=[]; bt.forEach(b=>L.forEach(l=>{ if(b[3]>l[1]-4 && b[1]<l[3]+4 && b[4]>l[2]-4 && b[2]<l[4]+4) touche.push(b[0]+' / '+l[0]+' '+l.slice(1).map(v=>Math.round(v)).join(',')); }));
  const lb=tr?(tr.getBoundingClientRect().bottom-D.top)/k:844; const dessous=bt.filter(b=>b[4]>lb+0.5).map(b=>b[0]);
  return {dessous:dessous, touche:touche, boutons:bt.map(b=>b[0]+' '+b.slice(1).map(v=>Math.round(v)).join(',')), entier:entier, n:L.length}; }"""
GEOM = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const ph=document.getElementById('onbPh'), so=document.getElementById('onbSous'), tt=document.getElementById('onbTrace'), tr=document.getElementById('onbTrait');
  const cs=getComputedStyle(ph), lh=parseFloat(cs.lineHeight), r=ph.getBoundingClientRect(), y=q=>(q-D.top)/k; const rs=so&&getComputedStyle(so).display!=='none'?so.getBoundingClientRect():null;
  const rg=document.createRange(); rg.selectNodeContents(ph); const tops=[...rg.getClientRects()].filter(q=>q.width>1).map(q=>q.top+q.height/2).sort((a,b)=>a-b); let L=0, der=-1e9; tops.forEach(t=>{ if(t-der>lh*k/2){ L++; der=t; } });
  return {lignes:Math.max(L, Math.round(r.height/lh)), fs:cs.fontSize, phBas:y(r.bottom), sous:!!rs, sousHaut:rs?y(rs.top):0, sousBas:rs?y(rs.bottom):0, traceHaut:y(tt.getBoundingClientRect().top), trait:y(tr.getBoundingClientRect().top)}; }"""
ONB = {'textes': ['#onbTrace', '#onbPh', '#onbSous', '#onbDit', '#onbQuid'], 'boutons': ['#onbSuite'], 'libelle': '#onbTrace'}
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        for parole in ('marcher une heure', 'appeler ma grand-mère chaque dimanche', 'appeler ma grand-mère chaque dimanche avant le déjeuner sans faute'):
            T = '%s · %s' % ('sombre' if sombre else 'clair', 'courte' if len(parole) < 20 else ('moyenne' if len(parole) < 40 else 'cinq lignes — Q568'))
            ctx = B.contexte(b, sombre=sombre, onb=False, guide=False); ctx.add_init_script(CLAVIER)
            pg = B.ouvre(ctx, F, attente=7000)
            B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
            B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(600); pg.keyboard.type(parole, delay=15); pg.wait_for_timeout(1500)
            m = pg.evaluate(MESURE, ONB); kb = pg.evaluate("()=>window.visualViewport.height")
            juge('[%s] A · clavier ouvert (%d pt visibles) : le bouton → ne touche aucune ligne de texte ; « trace pour planter » entier' % (T, kb), m['boutons'] and not m['touche'] and m['entier'] and not m['dessous'],
                 'bouton %s · touché : %s · entier %s · sous la consigne (sur le trait) : %s · %d lignes' % (m['boutons'], m['touche'][:3], m['entier'], m['dessous'], m['n']))
            g = pg.evaluate(GEOM)
            juge('[%s] D · la parole tient en trois lignes au plus (Q568) ; « Petite ou grande promesse » reste, au-dessus de la consigne ; rien sur le trait' % T,
                 g['lignes'] <= 3 and g['sous'] and g['sousBas'] <= g['traceHaut'] - 4 and g['phBas'] <= g['sousHaut'],
                 '%d lignes à %s px · phrase → %.1f · « Petite… » %.1f → %.1f · consigne %.1f · trait %.1f' % (g['lignes'], g['fs'], g['phBas'], g['sousHaut'], g['sousBas'], g['traceHaut'], g['trait']))
            pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(900)
            m = pg.evaluate(MESURE, ONB)
            juge('[%s] B · clavier refermé : de même' % T, not m['touche'] and m['entier'] is not False, 'bouton %s · touché : %s · entier %s' % (m['boutons'], m['touche'][:3], m['entier']))
            er = [e for e in pg.erreurs if 'version.json' not in e]; juge('[%s] aucune erreur de page' % T, not er, er[:2]); ctx.close()
    # C · les pages +
    for nat in ('promi', 'chiche', 'nuee'):
        ctx = B.contexte(b); ctx.add_init_script(CLAVIER); pg = B.ouvre(ctx, F)
        pg.evaluate("(n)=>{ closeAll(); if(window.openCreate) openCreate(n); else { const c=document.getElementById('createBtn'); if(c) c.click(); } }", nat); pg.wait_for_timeout(2500)
        t = pg.evaluate("(n)=>{ const e=document.querySelector('#accChoix [data-kind=\"'+n+'\"], #createSheet [data-kind=\"'+n+'\"]'); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null; }", nat)
        if t: pg.touchscreen.tap(t[0], t[1]); pg.wait_for_timeout(2000)
        lib = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#createSheet *')].find(x=>/^trace (pour|ta)/i.test([...x.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('').trim())); if(!e) return null; if(!e.id) e.id='__lib'; return '#'+e.id; }")
        mot = pg.evaluate("()=>{ const e=document.querySelector('#createSheet .pp-mot, #createSheet [data-mot]'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if mot: pg.touchscreen.tap(mot[0], mot[1]); pg.wait_for_timeout(1200)
        if lib:
            m = pg.evaluate(MESURE, {'textes': [lib], 'boutons': ['#createSheet button', '#createSheet [role=button]', '#createSheet .closeb', '#onbSuite'], 'libelle': lib})
            juge('[page + %s] C · clavier ouvert : aucun bouton ne recouvre « trace pour … »' % nat, not m['touche'] and m['entier'] is not False, 'touché : %s · entier %s' % (m['touche'][:3], m['entier']))
        else: juge('[page + %s] C · le libellé « trace pour … » est trouvé' % nat, False, 'absent')
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
