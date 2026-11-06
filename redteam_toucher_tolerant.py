#!/usr/bin/env python3
"""redteam_toucher_tolerant.py — ⚑ v181a (Tom, 6 nov. 2026, C-239) : « un toucher ouvre la dalle de parole la plus proche si elle est à 22 pt ou
moins du doigt. Si deux dalles sont à égale distance, aucune ne s'ouvre. Rien ne change à l'écran ; le moteur n'est pas touché. Juge sur mon état
exporté : chaque dalle de parole s'ouvre au doigt. »

L'état exporté de Tom (etats/tom-*.json), Touffe forcé, vue recadrée ; sa fenêtre (échelle de Safari) et 430 × 932 (échelle 1). La carte des
dalles est lue par le toucher du moteur (`Toile.hit`, pas de 2 pt, y 110 → 700) ; chaque toucher est un vrai doigt (`touchscreen.tap`, WebKit).
  A · chaque dalle de parole s'ouvre touchée en son milieu (le témoin : ce qui marchait marche encore) ;
  B · chaque dalle de parole de moins de 44 pt (le plus grand carré qu'elle contient) s'ouvre touchée HORS d'elle, sur une case vide à 6 – 18 pt d'elle, où elle est seule la plus proche
      (la seconde à 6 pt au moins plus loin) ;
  C · un toucher sur une case vide à égale distance (± 0,5 pt sur la grille de 2 pt) de deux dalles, à 18 pt au plus, n'ouvre rien ;
  D · un toucher à plus de 28 pt de toute dalle de parole n'ouvre rien ;
  E · le moteur n'a pas changé (empreinte de promi-moteur.js = celle de v180b) ; aucune erreur de page.
Rouge sur v180b (`--fichier=zz-v180b.html`) : B.
"""
import sys, hashlib, subprocess; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
CARTE = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), f=cv.clientWidth/r.width;
  const cle=h=>!h?null:(h.kind==='nuee'&&h.nuee)?('n:'+h.nuee):(h.pid!=null?('p:'+h.pid):null); const G={}, V=[];
  for(let y=110;y<=700;y+=2) for(let x=4;x<=386;x+=2){ const h=window.Toile.hit((D.left+x*k-r.left)*f,(D.top+y*k-r.top)*f), c=cle(h); if(c) (G[c]=G[c]||[]).push([x,y]); else V.push([x,y]); }
  const out={}; for(const c in G){ const P=G[c], xs=P.map(p=>p[0]), ys=P.map(p=>p[1]); let mx=xs.reduce((a,b)=>a+b)/P.length, my=ys.reduce((a,b)=>a+b)/P.length;
    let best=P[0], bd=1e9; for(const p of P){ const d=Math.hypot(p[0]-mx,p[1]-my); if(d<bd){bd=d;best=p;} }   /* le point de la dalle le plus près de son centre de masse */
    const S=new Set(P.map(p=>p[0]+','+p[1])); let sq=0; for(const p of P){ let a=sq+2; while(true){ let ok=true; for(let yy=p[1];yy<=p[1]+a&&ok;yy+=2) for(let xx=p[0];xx<=p[0]+a;xx+=2){ if(!S.has(xx+','+yy)){ ok=false; break; } } if(!ok) break; sq=a; a+=2; } }
    out[c]={mil:best, carre:sq, P:P}; }
  /* chaque case vide : ses deux dalles les plus proches */
  const vides=[]; for(let i=0;i<V.length;i+=2){ const v=V[i]; const ds=Object.keys(out).map(c=>{ let m=1e9; for(const p of out[c].P){ const d=Math.hypot(p[0]-v[0],p[1]-v[1]); if(d<m) m=d; } return [m,c]; }).sort((a,b)=>a[0]-b[0]); vides.push([v[0],v[1],ds[0],ds[1]]); }
  for(const c in out) delete out[c].P; return {dalles:out, vides:vides}; }"""
OUVERT = """()=>{ const d=document.getElementById('detailPoster'); if(!d||!d.classList.contains('show')) return null; if(d.classList.contains('dp-mode-nuee')||d.classList.contains('dp-nuee')) return 'n:'+(typeof curNuee!=='undefined'?curNuee:'?'); return (typeof cur!=='undefined'&&cur)?'p:'+cur.id:'?'; }"""
def touche(pg, x, y):
    pg.evaluate("()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); window._tapVide=null; }"); pg.wait_for_timeout(700)
    B.tap(pg, x, y); pg.wait_for_timeout(1100); o = pg.evaluate(OUVERT)
    pg.evaluate("()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(500); return o
moteur = hashlib.sha1(open('promi-moteur.js', 'rb').read()).hexdigest()
ref = hashlib.sha1(subprocess.run(['git', 'show', 'a7ef44c:promi-moteur.js'], capture_output=True).stdout).hexdigest()
juge('E · le moteur n\'est pas touché (promi-moteur.js = v180b)', moteur == ref, (moteur[:8], ref[:8]))
with sync_playwright() as p:
    b = p.webkit.launch()
    for ech in (None, 1):
        ctx, d = B.contexte_tom(b, echelle=ech); T = '[%s]' % ('Tom' if ech is None else '×1')
        pg = B.ouvre(ctx, F, 7000)
        pg.evaluate("()=>{ Toile.setTheme('touffe'); }"); pg.wait_for_timeout(3500); pg.evaluate("()=>{ Toile_recadre(); }"); pg.wait_for_timeout(3000)
        C = pg.evaluate(CARTE); D = C['dalles']; print('  %s état %s · %d dalles de parole · tailles %s' % (T, d['_fichier'], len(D), sorted(v['carre'] for v in D.values())), flush=True)
        ka = [c for c in D if touche(pg, *D[c]['mil']) == c]
        juge(T + ' A · chaque dalle de parole s\'ouvre touchée en son milieu', len(ka) == len(D), '%d/%d %s' % (len(ka), len(D), sorted(set(D) - set(ka))))
        petites = [c for c in D if D[c]['carre'] < 44]; kb = []; manque = []
        for c in petites:
            cand = sorted([v for v in C['vides'] if v[2][1] == c and 6 <= v[2][0] <= 18 and (v[3] is None or v[3][0] - v[2][0] >= 6)], key=lambda v: -v[2][0])
            if not cand: manque.append(c); continue
            v = cand[0]; o = touche(pg, v[0], v[1])
            (kb.append(c) if o == c else manque.append((c, round(v[2][0], 1), o)))
        juge(T + ' B · chaque petite dalle (< 44 pt) s\'ouvre touchée hors d\'elle, à 6 – 18 pt', petites and len(kb) == len(petites), '%d/%d petites · ratées %s' % (len(kb), len(petites), manque))
        eg = [v for v in C['vides'] if v[3] and v[3][0] - v[2][0] <= 0.5 and v[2][0] <= 18 and v[2][0] >= 4]
        if eg:
            o = [touche(pg, v[0], v[1]) for v in eg[:3]]
            juge(T + ' C · à égale distance de deux dalles, rien ne s\'ouvre', all(x is None for x in o), list(zip([(v[0], v[1], round(v[2][0], 1)) for v in eg[:3]], o)))
        else: juge(T + ' C · à égale distance de deux dalles (aucune case vide de ce genre sur cette Toile)', True, 'non trouvée')
        loin = [v for v in C['vides'] if v[2][0] > 28]
        o = [touche(pg, v[0], v[1]) for v in loin[::max(1, len(loin) // 3)][:3]]
        juge(T + ' D · à plus de 28 pt de toute dalle, rien ne s\'ouvre', loin and all(x is None for x in o), o)
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
