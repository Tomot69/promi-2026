#!/usr/bin/env python3
"""⚑ v212 (C-311, Tom, 19 nov. 2026) — « dans une fiche qui a des commentaires, au moment de tenir, « Parole tenue ! » (ou « Défi relevé ! ») monte. Il doit rester
fixe, à la même place que dans une fiche sans commentaire. »
Critère : la place du texte de célébration identique au demi-point près, avec 0, 1, 3 et 12 commentaires, sur les trois natures (Promi, Chiche, un Promi d'un Cercle),
aux échelles 1 (390 × 844) et 0,79 (330 × 714).
L'ENCRE de la phrase est lue DANS la nappe, à chaque image, dans l'image même où elle est peinte (`window._mareeReleve`), et rapportée à l'écran par le rectangle
de la nappe ET le défilement du moment. Chaque cas est tracé deux fois : la fiche au repos, puis la fiche défilée de 40 pt avant de tracer (une fiche à mots défile).
  A · à chaque image où la phrase est peinte, son haut d'encre est à la même place (± 0,5 pt) ;
  B · cette place est la même pour tous les cas (± 0,5 pt) — la valeur de référence est écrite EN DUR : 391,3 pt (v211, fiche sans mot, non défilée).
`--fichier=`, `--natures=promi,chiche,cercle`. Rouge sur v211 (la phrase à 307 pt sur une fiche défilée de 42)."""
import sys
from playwright.sync_api import sync_playwright
import banc_tom as B
F = 'app.html'; NAT = ['promi', 'chiche', 'cercle']
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
    if a.startswith('--natures='): NAT = a.split('=', 1)[1].split(',')
REF = 391.3
NS = [0, 1, 3, 12]
OUV = """(a)=>{ const [n,nat]=a; const P=promises.filter(x=>!x.draft); let p = nat==='chiche' ? P.find(x=>x.chiche&&!x.nuee) : nat==='cercle' ? P.find(x=>x.nuee&&!x.chiche) : P.find(x=>!x.chiche&&!x.nuee);
  if(!p) return null; p.status='encours'; p.who='moi'; p.from='moi'; delete p.parts; delete p.vuTenue; delete p.avec;
  p.comments=Array.from({length:n},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true})); saveState(true); closeAll(); openDetail(p.id); return p.id; }"""
REC = r"""()=>{ window.__ce=[]; const D=document.getElementById('device'), dp=document.getElementById('detailPoster');
 window._mareeReleve=function(g, cv){ const W=cv.width, H=cv.height, s=W/390, k=D.getBoundingClientRect().width/390, cr=cv.getBoundingClientRect(), dr=D.getBoundingClientRect();
   const x0=Math.round(100*s), x1=Math.round(290*s), im=g.getImageData(x0,0,x1-x0,H).data; let top=-1;
   for(let r=0;r<H && top<0;r++){ for(let c=0;c<x1-x0;c+=2){ const i=(r*(x1-x0)+c)*4; if(im[i+3]>200 && im[i]<70 && im[i+1]<60 && im[i+2]<50){ top=r; break; } } }
   window.__ce.push([dp.scrollTop, top<0?null:((cr.top-dr.top)/k + top/s*(cr.height/k)/(H/s))]); }; }"""
R = []
def juge(nom, ok, det=''):
    R.append(ok); print(('✅' if ok else '❌'), nom, '' if ok else det, flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((390, 844, '1'), (330, 714, '0,79')):
        for nat in NAT:
            places = []
            for pre in (0, 40):
                for n in NS:
                    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
                    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__jr')){ sessionStorage.setItem('__jr','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
                    B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
                    T = '[%s · %s · %d mots · %s]' % (ech, nat, n, 'défilée de %d' % pre if pre else 'au repos')
                    try:
                        if not pg.evaluate(OUV, [n, nat]): juge(T + ' une parole de cette nature', False); ctx.close(); continue
                        pg.wait_for_timeout(3000)
                        if pre: pg.evaluate("v=>{ window._ficheSure=function(t){return t;}; const d=document.getElementById('detailPoster'); d.style.scrollBehavior='auto'; d.scrollTop=v; }", pre); pg.wait_for_timeout(600)
                        s0 = pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
                        z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
                        y = z[1] + z[3] * 0.45; pg.evaluate(REC)
                        B.glisse(pg, [[30 + 330 * i / 14, y] for i in range(15)], pas=30, tenue=380); pg.wait_for_timeout(2600)
                        fr = pg.evaluate("()=>{ window._mareeReleve=null; return __ce; }")
                        ys = [r[1] for r in fr if r[1] is not None]; ss = sorted(set(round(r[0]) for r in fr))
                        if not ys: juge(T + ' la phrase est peinte', False, 'défil. %s, %d images' % (s0, len(fr))); ctx.close(); continue
                        juge(T + ' A · fixe sur %d images (%.1f → %.1f pt ; défilement %s)' % (len(ys), min(ys), max(ys), ss[:5]), max(ys) - min(ys) <= 0.5, ys[:8])
                        places.append((T, (min(ys) + max(ys)) / 2))
                    except Exception as e:
                        juge(T + ' le cas se joue', False, str(e)[:300])
                    ctx.close()
            if places:
                ec = [(t, round(v, 1)) for t, v in places if abs(v - REF) > 0.5]
                juge('[%s · %s] B · la même place dans les %d cas, %.1f pt (référence %.1f)' % (ech, nat, len(places), places[0][1], REF), not ec, ec[:4])
    b.close()
print('\n%d/%d' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
