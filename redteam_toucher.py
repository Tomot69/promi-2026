#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_toucher.py — v133 (C-058) : SOUS CHAQUE MONDE, TOUCHER UNE DALLE OUVRE SA FICHE.
Tom (5 oct. 2026) : « Sous certains mondes, la Toile ne répond plus au doigt. Sous Ramage notamment, toucher une dalle n'ouvre plus sa
fiche. Vérifie les vingt mondes. Juge : vingt mondes, trois dalles touchées au vrai doigt par monde. »
AU VRAI DOIGT (contexte tactile, `touchscreen.tap`), sur la Toile de l'accueil. Les VINGT mondes sont écrits EN DUR.
Où toucher : le moteur dit quelle parole est sous un point (`Toile.hit`) — ce n'est qu'un POINTEUR (§7) ; on garde, pour trois paroles,
le point le plus au cœur de leur dalle. LE VERDICT vient de l'écran : après le toucher, la fiche de CETTE parole est ouverte (son titre
est celui de la parole), et rien d'autre. Et aucune couche ne recouvre la Toile au point touché.
Usage : python3 redteam_toucher.py [fichier.html] [--mondes=ramage,encre]"""
import sys
from playwright.sync_api import sync_playwright
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
MONDES=['encre','touffe','brouillamini','halin','esquille','mosaique','braille','pixel','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo','gravure','sillons']
NOMS={'encre':'Pochade','touffe':'Touffe','brouillamini':'Brouillamini','halin':'Halin','esquille':'Esquille','mosaique':'Tesselle','braille':'Braille','pixel':'Buvard','ramage':'Ramage','guingois':'Guingois','chantourne':'Chantourné','volubilis':'Volubilis','madrure':'Madrure','chamade':'Chamade','ritournelle':'Ritournelle','bobinette':'Bobinette','mascaret':'Mascaret','terrazzo':'Éclisse','gravure':'Taille-douce','sillons':'Houle'}
sel=next((a.split('=')[1].split(',') for a in sys.argv if a.startswith('--mondes=')), None)
if sel: MONDES=[m for m in MONDES if m in sel]
assert len(NOMS)==20
R=[]
def ok(nom, cond, detail=''):
    R.append((nom,bool(cond))); print(('  ✅ ' if cond else '  ❌ ')+nom+((' — '+str(detail)[:300]) if (detail!='' and not cond) else ''), flush=True)
POINTS=r"""()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(); const kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height;
  const G={}; const pas=6;
  for(let y=dv.top+130;y<dv.bottom-150;y+=pas) for(let x=dv.left+12;x<dv.right-12;x+=pas){ let h=null; try{ h=Toile.hit((x-r.left)*kx,(y-r.top)*ky); }catch(e){} if(h&&h.pid!=null){ (G[h.pid]=G[h.pid]||[]).push([x,y]); } }
  const out=[]; Object.keys(G).forEach(pid=>{ const L=G[pid]; if(L.length<12) return; const set=new Set(L.map(p=>p[0]+','+p[1]));
      /* le point le plus au cœur : celui dont le plus de voisins (rayon 3 pas) sont dans la même dalle */
      let best=null, bs=-1; L.forEach(p=>{ let s=0; for(let a=-3;a<=3;a++) for(let b=-3;b<=3;b++) if(set.has((p[0]+a*pas)+','+(p[1]+b*pas))) s++; if(s>bs){ bs=s; best=p; } });
      const pr=promises.find(q=>q.id===+pid); if(pr) out.push({pid:+pid, x:best[0], y:best[1], n:L.length, coeur:bs, titre:pr.title}); });
  out.sort((a,b)=>b.coeur-a.coeur); return {pts:out.slice(0,3), dalles:out.length, theme:Toile.getTheme()}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    for m in MONDES:
        pg.evaluate("(m)=>{ try{closeAll()}catch(e){} try{ if(typeof setView==='function') setView('toile'); }catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(3200)
        P=pg.evaluate(POINTS)
        if P['theme']!=m or len(P['pts'])<3:
            ok('%s : trois dalles à toucher'%NOMS[m], False, 'monde %s · %d dalle(s) trouvée(s)'%(P['theme'], P['dalles'])); continue
        res=[]
        for q in P['pts']:
            dessus=pg.evaluate("([x,y])=>{const h=document.elementFromPoint(x,y); return h?(h.id||h.className||h.tagName):null}", [q['x'],q['y']])
            pg.touchscreen.tap(q['x'], q['y']); pg.wait_for_timeout(1500)
            e=pg.evaluate("()=>{const dp=document.getElementById('detailPoster'), t=document.getElementById('dptTitre'); return {show:!!(dp&&dp.classList.contains('show')), titre:t?t.textContent.trim():'', cur:(typeof cur!=='undefined'&&cur)?cur.id:null}}")
            res.append({'titre':q['titre'], 'ouvert':e['show'] and e['cur']==q['pid'] and e['titre']==q['titre'], 'vu':e, 'dessus':dessus})
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        bons=sum(1 for r_ in res if r_['ouvert'])
        ok('%s : toucher une dalle ouvre sa fiche (%d sur 3)'%(NOMS[m],bons), bons==3, [(r_['titre'], r_['vu'], r_['dessus']) for r_ in res if not r_['ouvert']])
    ok('aucune erreur de page', not errs, errs[:2]); b.close()
n=sum(1 for _,c in R if c); print('\nredteam_toucher : %d/%d'%(n,len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
