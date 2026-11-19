#!/usr/bin/env python3
"""⚑ v211 (C-297, Tom, 19 nov. 2026) — « dans une fiche tenue, en défilant, le trait passe sous le bandeau du haut au lieu de s'y accrocher ».

CE QUE DIT LE RELEVÉ DE L'iPHONE (mesures/appareil.jsonl, `quoi:'c297'`, séances du 18 et du 19 nov.) : le trait plat (`#v195Plat`, collé à 110 pt) quitte
la jonction SEULEMENT quand le défilement dépasse le défilement possible — au rebond du bas d'iOS (le doigt qui tire au-delà du bout, l'élan qui rebondit) :
s = 229 pour un bout à 143, s = 195 pour un bout à 117 ; le trait plat monte alors à 32 pt, sous le bandeau. Sa boîte collante est bornée par la FENÊTRE qui le
porte (`#v200Fenetre`, v200) : sa hauteur suivait « le défilement possible + 48 pt » — au-delà, le bas de la fenêtre pousse le trait plat vers le haut.
Le banc (WebKit de bureau) ne rebondit pas : le juge lit la GÉOMÉTRIE qui fait le défaut, celle que le relevé montre.

À CHAQUE FICHE (Promi en cours, Promi tenu, Chiche tenu, Cercle ; courtes, comme celles de Tom) :
  R1 · le trait plat reste à la jonction jusqu'à un défilement de « bout + 300 pt » (le rebond d'iOS, relevé jusqu'à +88 pt) : le bas de ce qui le borne,
       moins 150, est au-delà ;
  R2 · la fenêtre ne porte pas le défilement (le défilement possible est le même avec et sans elle) ;
  R3 · de 0 au bout, pas à pas, le trait plat est à 110 ± 0,6 pt.
`--fichier=` sert une autre version (bissection). Rouge sur 120a363 (R1)."""
import sys, json
from playwright.sync_api import sync_playwright
import banc_tom as B

F = 'app.html'; NAT = ['promi', 'promi-tenu', 'chiche-tenu', 'cercle']
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
    if a.startswith('--natures='): NAT = a.split('=', 1)[1].split(',')
OV = 300
GEO = """()=>{ const d=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, pl=document.getElementById('v195Plat');
  if(!pl) return {pl:false, s:d.scrollTop, smax:d.scrollHeight-d.clientHeight};
  const c=pl.parentElement, dr=d.getBoundingClientRect(), cr=c.getBoundingClientRect();
  const bas=(cr.bottom-dr.top)/k + d.scrollTop;   /* le bas de ce qui borne le trait plat, en coordonnées du contenu */
  return {pl:true, s:d.scrollTop, smax:d.scrollHeight-d.clientHeight, sh:d.scrollHeight, ch:d.clientHeight, bas:bas, lim:bas-150, plat:(pl.getBoundingClientRect().top-D.top)/k, parent:c.id||c.tagName}; }"""
SANS = """()=>{ const d=document.getElementById('detailPoster'), w=document.getElementById('v200Fenetre'); if(!w) return [d.scrollHeight, d.scrollHeight];
  const a=d.scrollHeight, o=w.style.getPropertyValue('display'), p=w.style.getPropertyPriority('display'); w.style.setProperty('display','none','important'); const b=d.scrollHeight;
  if(o) w.style.setProperty('display',o,p); else w.style.removeProperty('display'); return [a,b]; }"""
OUV = """(n)=>{ const P=promises.filter(x=>!x.draft&&!x.nuee); let p;
  if(n==='cercle'){ const k=Object.keys(NUE||{})[0]; closeAll(); window.openNueeDetail(k); return 'cercle '+k; }
  p = n.startsWith('chiche') ? P.find(x=>x.chiche) : P.find(x=>!x.chiche&&x.status==='encours');
  p.status='encours'; p.who='moi'; delete p.parts; delete p.vuTenue; p.comments=Array.from({length:2},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true})); saveState(true); closeAll(); openDetail(p.id); return p.id; }"""
R = []
def juge(nom, ok, det=''):
    R.append(ok); print(('✅' if ok else '❌'), nom, '' if ok else det, flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    for n in NAT:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__jr')){ sessionStorage.setItem('__jr','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
        B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        try:
            pg.evaluate(OUV, n); pg.wait_for_timeout(3000)
            if n.endswith('-tenu'):
                z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
                y = z[1] + z[3] * 0.45
                B.glisse(pg, [[30 + 330 * i / 14, y] for i in range(15)], pas=30, tenue=380); pg.wait_for_timeout(5000)
                if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('f-tenue')"):
                    B.glisse(pg, [[200 + 160 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(5000)
            pg.evaluate("()=>{ window._ficheSure=function(t){return t;}; const d=document.getElementById('detailPoster'); d.style.scrollBehavior='auto'; d.style.scrollSnapType='none'; }")
            T = '[%s]' % n
            tenu = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('f-tenue')")
            if n.endswith('-tenu'): juge(T + ' la fiche est tenue', tenu)
            Rs = []
            g0 = pg.evaluate(GEO)
            for s in range(0, int(g0['smax']) + 1, 4):
                Rs.append(pg.evaluate("v=>new Promise(r=>{ document.getElementById('detailPoster').scrollTop=v; requestAnimationFrame(()=>requestAnimationFrame(()=>r((%s)()))); })" % GEO, s))
            g = Rs[-1] if Rs else g0
            if not g.get('pl'): juge(T + ' le trait plat existe', False, g); ctx.close(); continue
            juge(T + ' R1 · le trait plat tient à la jonction jusqu’au bout + %d pt (rebond d’iOS) — il tient jusqu’à %.0f, le bout à %.0f (borné par %s)' % (OV, g['lim'], g['smax'], g['parent']), g['lim'] >= g['smax'] + OV, g)
            a, b2 = pg.evaluate(SANS)
            juge(T + ' R2 · la fenêtre ne porte pas le défilement (%d avec, %d sans)' % (a, b2), a == b2)
            hors = [(r['s'], round(r['plat'], 1)) for r in Rs if r.get('pl') and r['s'] > 60 and abs(r['plat'] - 110) > 0.6]
            juge(T + ' R3 · de 0 au bout (%d images), le trait plat à 110 pt dès qu’il est découvert' % len(Rs), not hors, hors[:5])
        except Exception as e:
            juge('[%s] le cas se joue' % n, False, str(e)[:300])
        ctx.close()
    b.close()
print('\n%d/%d' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
