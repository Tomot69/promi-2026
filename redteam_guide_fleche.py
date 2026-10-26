#!/usr/bin/env python3
"""redteam_guide_fleche.py — ⚑ v166 (Tom, C-203 §2) : LE GUIDE — UNE FLÈCHE ORANGE VERS CHAQUE ICÔNE.

« Dans les phrases du Studio, du + et de Partager, ajoute la MÊME flèche que celle de la page +, à côté de « TRACE POUR PLANTER » (pointe et trait de départ,
même dessin, même épaisseur ×1,3), en orange #FB4C0D. Elle part de la phrase et pointe vers l'icône, sans jamais la toucher ni la recouvrir, à l'intérieur ou au
bord de la zone nette. Fixe, sans clignotement. Elle paraît avec la zone nette, et disparaît en flaques avec elle. Juge : flèche présente sur les 3 étapes,
orientée vers l'icône à ± 10°, aucun recouvrement, clair et sombre, échelles 1 et 0,79. »

Le vrai parcours du guide (banc WebKit, stockage vierge, onboarding passé) : l'étape du Studio, le Studio ouvert puis refermé, l'étape du +, un toucher ailleurs,
l'étape de Partager, un toucher ailleurs, la phrase 2. Tout se LIT sur le canevas de la flèche (`#guideFleche`, ×3) et sur celui de l'eau :
  A · la flèche est là, à l'orange #FB4C0D (le cœur de son encre) ;
  B · son axe (l'axe principal de son encre, de la queue vers la pointe) vise le centre de l'icône à ± 10° ;
  C · aucune encre sur l'icône (sa boîte), ni sur la phrase, ni hors de l'écran ;
  D · sa pointe est au bord de la zone nette (≤ 2 pt d'un point net) ;
  E · elle est fixe : deux lectures à 700 ms, la même encre au pixel près (± 0,5 %) ;
  F · elle part avec la zone : à la phrase 2, plus aucune encre ;
  G · son épaisseur : la queue fait 2,2 × 13 pt (28,6 ± 1,5) — le dessin de la page + à × 1,3.
Preuve : `--fichier=zz-v165.html` rougit (aucune flèche).
"""
import sys, types; sys.path.insert(0, '.')
src = open('redteam_guide_cloture.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0]
src = src.replace("F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')", "F = 'app.html'")
m = types.ModuleType('g'); exec(compile(src, 'g', 'exec'), m.__dict__)
from playwright.sync_api import sync_playwright
m.F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
LIT = """(quoi)=>{ const cv=document.getElementById('guideFleche'); if(!cv||!cv.width) return {n:0, absent:true}; const d=cv.width/390, W=cv.width, H=cv.height;
  const px=cv.getContext('2d').getImageData(0,0,W,H).data; let n=0, sx=0, sy=0, sxx=0, syy=0, sxy=0, x0=1e9, y0=1e9, x1=-1e9, y1=-1e9; const P=[], C=[];
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const R=s=>{ const e=document.querySelector(s); if(!e) return null; let a=1e9,b=1e9,c=-1e9,dd=-1e9; [...e.querySelectorAll('svg, .l')].forEach(q=>{ const r=q.getBoundingClientRect(); if(r.width<2) return; a=Math.min(a,r.left); b=Math.min(b,r.top); c=Math.max(c,r.right); dd=Math.max(dd,r.bottom); });
    if(!(c>a)){ const r=e.getBoundingClientRect(); a=r.left; b=r.top; c=r.right; dd=r.bottom; } return [(a-D.left)/k,(b-D.top)/k,(c-D.left)/k,(dd-D.top)/k]; };
  const ic=R({studio:'#studioBtn', plus:'#createBtn', partage:'#shareBtn'}[quoi]);
  const ph=document.getElementById('guidePhrase'); let pr=null; if(ph){ const rg=document.createRange(); rg.selectNodeContents(ph); const r=rg.getBoundingClientRect(); pr=[(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k]; }
  let surIc=0, surPh=0;
  for(let y=0;y<H;y++) for(let x=0;x<W;x++){ const i=(y*W+x)*4; if(px[i+3]<128) continue; const X=(x+0.5)/d, Y=(y+0.5)/d; n++; sx+=X; sy+=Y; sxx+=X*X; syy+=Y*Y; sxy+=X*Y;
    if(X<x0)x0=X; if(X>x1)x1=X; if(Y<y0)y0=Y; if(Y>y1)y1=Y; if((n%7)===0) P.push([X,Y]); if(px[i+3]===255 && (n%3)===0) C.push([px[i],px[i+1],px[i+2]]);
    if(ic && X>=ic[0] && X<=ic[2] && Y>=ic[1] && Y<=ic[3]) surIc++; if(pr && X>=pr[0] && X<=pr[2] && Y>=pr[1] && Y<=pr[3]) surPh++; }
  if(!n) return {n:0};
  const mx=sx/n, my=sy/n, a=sxx/n-mx*mx, b=sxy/n-mx*my, c=syy/n-my*my, th=0.5*Math.atan2(2*b, a-c); let ux=Math.cos(th), uy=Math.sin(th);
  const cx=(ic[0]+ic[2])/2, cy=(ic[1]+ic[3])/2; if(ux*(cx-mx)+uy*(cy-my)<0){ ux=-ux; uy=-uy; }
  let tip=null, tq=-1e9, tail=null, tl=1e9; P.forEach(p=>{ const q=(p[0]-mx)*ux+(p[1]-my)*uy; if(q>tq){ tq=q; tip=p; } if(q<tl){ tl=q; tail=p; } });
  /* la largeur de la queue : l'étendue de l'encre en travers de l'axe, près du bout de la queue */
  let qm=1e9; for(let y=0;y<H;y++) for(let x=0;x<W;x++){ if(px[(y*W+x)*4+3]<128) continue; const X=(x+0.5)/d, Y=(y+0.5)/d, q=(X-mx)*ux+(Y-my)*uy; if(q<qm) qm=q; }
  let lo=1e9, hi=-1e9; for(let y=0;y<H;y++) for(let x=0;x<W;x++){ if(px[(y*W+x)*4+3]<128) continue; const X=(x+0.5)/d, Y=(y+0.5)/d, q=(X-mx)*ux+(Y-my)*uy; if(q<qm+1.2){ const t=-(X-mx)*uy+(Y-my)*ux; lo=Math.min(lo,t); hi=Math.max(hi,t); } }
  const vx=cx-mx, vy=cy-my, ang=Math.acos(Math.max(-1,Math.min(1,(ux*vx+uy*vy)/Math.sqrt(vx*vx+vy*vy))))*57.2958;
  C.sort((p,q)=>p[0]-q[0]); const med=C.length?C[C.length>>1]:null;
  /* la pointe au bord de la zone nette : un point de l'eau transparent (net) à 2 pt au plus */
  const ev=document.getElementById('guideEau'); let dz=null; if(ev && tip){ const de=ev.width/390, e=ev.getContext('2d').getImageData(Math.max(0,Math.round((tip[0]-6)*de)), Math.max(0,Math.round((tip[1]-6)*de)), Math.round(12*de), Math.round(12*de)), w=Math.round(12*de);
    for(let j=0;j<w;j++) for(let i=0;i<w;i++){ if(e.data[(j*w+i)*4+3]<60){ const X=(Math.max(0,Math.round((tip[0]-6)*de))+i+0.5)/de, Y=(Math.max(0,Math.round((tip[1]-6)*de))+j+0.5)/de, dd=Math.hypot(X-tip[0],Y-tip[1]); if(dz===null||dd<dz) dz=dd; } } }
  return {n:n, boite:[x0,y0,x1,y1].map(v=>Math.round(v*10)/10), ang:Math.round(ang*10)/10, surIc:surIc, surPh:surPh, med:med, tip:tip&&tip.map(v=>Math.round(v*10)/10), dz:dz===null?null:Math.round(dz*10)/10, queue:Math.round((hi-lo)*10)/10, icone:ic&&ic.map(v=>Math.round(v*10)/10)}; }"""
def etape(pg, T, quoi):
    a = pg.evaluate(LIT, quoi); pg.wait_for_timeout(700); b = pg.evaluate(LIT, quoi)
    juge('[%s · %s] A · la flèche est là, orange #FB4C0D' % (T, quoi), a.get('n', 0) > 300 and a.get('med') and sum(abs(x - y) for x, y in zip(a['med'], (251, 76, 13))) <= 12, {'n': a.get('n'), 'coeur': a.get('med')})
    if not a.get('n'): return
    juge('[%s · %s] B · son axe vise l\'icône (± 10°)' % (T, quoi), a['ang'] <= 10, '%s°' % a['ang'])
    bx = a['boite']; dedans = bx[0] >= 0 and bx[1] >= 0 and bx[2] <= 390 and bx[3] <= 844
    juge('[%s · %s] C · aucune encre sur l\'icône, ni sur la phrase, ni hors de l\'écran' % (T, quoi), a['surIc'] == 0 and a['surPh'] == 0 and dedans, {'sur icône': a['surIc'], 'sur phrase': a['surPh'], 'boîte': bx, 'icône': a['icone']})
    juge('[%s · %s] D · sa pointe au bord de la zone nette (≤ 2 pt)' % (T, quoi), a['dz'] is not None and a['dz'] <= 2, {'pointe': a['tip'], 'au net': a['dz']})
    juge('[%s · %s] E · fixe : la même encre à 700 ms (± 0,5 %%)' % (T, quoi), abs(b.get('n', 0) - a['n']) <= 0.005 * a['n'] and b.get('boite') == a['boite'], {'n': [a['n'], b.get('n')], 'boîte': [a['boite'], b.get('boite')]})
    juge('[%s · %s] G · la queue : 28,6 pt (± 1,5) — le dessin de la page + à × 1,3' % (T, quoi), abs(a['queue'] - 28.6) <= 1.5, '%s pt' % a['queue'])
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre, vw, vh, ech in ((False, 390, 844, '1'), (True, 390, 844, '1'), (False, 330, 714, '0,79'), (True, 330, 714, '0,79')):
        T = '%s %s' % ('sombre' if sombre else 'clair', ech)
        ctx, pg, er = m.page(b, sombre, vw, vh)
        pg.evaluate("()=>{ _guide.attend(false); }")
        e = m.attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&+g.getAttribute('data-net')>=1 ? _guide.etat() : null;}", 170)
        if not e: juge('[%s] l\'étape du Studio' % T, False); ctx.close(); continue
        pg.wait_for_timeout(900); etape(pg, T, 'studio')
        m.tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600); m.tap_sel(pg, '#studioScreen .closeb')
        if m.attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1);}", 150):
            pg.wait_for_timeout(900); etape(pg, T, 'plus')
        else: juge('[%s] l\'étape du +' % T, False)
        pg.wait_for_timeout(300); m.tap_pt(pg, 200, 520)
        if m.attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='partage' && +g.getAttribute('data-net')>=1);}", 120):
            pg.wait_for_timeout(900); etape(pg, T, 'partage')
        else: juge('[%s] l\'étape de Partager' % T, False)
        m.tap_pt(pg, 200, 560)
        if m.attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='reste' && +g.getAttribute('data-net')>=1);}", 80):
            f = pg.evaluate(LIT, 'partage'); juge('[%s] F · à la phrase 2, plus aucune flèche' % T, f.get('n', 0) == 0, f.get('n'))
        else: juge('[%s] la phrase 2' % T, False)
        juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
