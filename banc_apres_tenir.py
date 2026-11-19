"""⚑ v207 (C-297, Tom, 17 nov. 2026) — « après tenir, le trait ne réagit plus au défilement vers le haut et la dalle bugue ». Le cas, partagé par redteam_un_trait et
redteam_repos_fiche : une fiche Promi « en cours » (six mots : elle défile), tenue au doigt ; 600 ms après le lever, pendant que le vert est posé :
  T1 · on défile à la molette jusqu'à 200 pt : la fiche défile, le trait la suit (la boîte de la vague + le défilement ne bouge pas), et la nappe verte ne monte JAMAIS
       au-dessus de la bande d'en-tête (aucun pixel amande dans 0 → 108 pt) ;
  T2 · un doigt posé (touchstart) : le vert remonte (`_tenirVite`), et le DÉBUT du geste n'est pas annulé (`defaultPrevented` faux) — annulé, il tuait le défilement
       natif de tout le geste (la cause : v154, C-167) ; la fin du geste et le clic restent avalés.
Rouge sur v205 (T1 : la nappe à z 40 passe sur l'en-tête ; T2 : le touchstart annulé)."""
import io
import numpy as np
from PIL import Image
import banc_tom as B
MOTS = "Array.from({length:6},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true}))"
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
INFO = "()=>{ const d=document.getElementById('detailPoster'), c=document.getElementById('v192Colle'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [d.scrollTop, c?(c.getBoundingClientRect().top-D.top)/k:null]; }"
DOIGT = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, x=D.left+300*k, y=D.top+560*k, el=document.elementFromPoint(x,y)||document.body;
  const t={identifier:31,target:el,clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,radiusX:11,radiusY:11,rotationAngle:0,force:0.5};
  const mk=(typ,L)=>{ let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,composed:true,touches:L,targetTouches:L,changedTouches:[new Touch(t)]}); }catch(_){ e=new Event(typ,{bubbles:true,cancelable:true,composed:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t]}); } return e; };
  const v0=window._tenirVite||0, e=mk('touchstart',[t]); el.dispatchEvent(e); const pd=e.defaultPrevented; el.dispatchEvent(mk('touchend',[]));
  return {annule:pd, remonte:(window._tenirVite||0)>v0}; }"""
def roule(pg, d, dy, pas=8, ms=16):
    pg.mouse.move(d[0] + 195 * d[4], d[1] + 600 * d[4]); n = max(1, int(abs(dy) / pas)); s = dy / n
    for _ in range(n): pg.mouse.wheel(0, s); pg.wait_for_timeout(ms)
def cas(b, F, juge, vw=390, vh=844, nom='après tenir'):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__at')){ sessionStorage.setItem('__at','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); p.who='moi'; p.comments=%s; delete p.parts; closeAll(); openDetail(p.id); }" % MOTS)
    pg.wait_for_timeout(3000); d = B.dev(pg)
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(600)
    i0 = pg.evaluate(INFO); roule(pg, d, 200); i1 = pg.evaluate(INFO)
    png = pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': 390 * d[4], 'height': 108 * d[4]}); a = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
    am = int(((np.abs(a[..., 0] - 143) < 18) & (np.abs(a[..., 1] - 224) < 18) & (np.abs(a[..., 2] - 143) < 18)).sum())
    suit = i0[1] is not None and i1[1] is not None and abs((i1[1] + i1[0]) - (i0[1] + i0[0])) <= 0.6
    juge('[%s] T1 · défiler pendant le vert : la fiche défile (%.0f → %.0f), le trait suit, la nappe sous l’en-tête (%d pixels amande au-dessus de 108)' % (nom, i0[0], i1[0], am), i1[0] - i0[0] > 150 and suit and am == 0, (i0, i1))
    r = pg.evaluate(DOIGT)
    juge('[%s] T2 · un doigt posé fait remonter le vert sans annuler le défilement natif' % nom, r['remonte'] and not r['annule'], r)
    ctx.close()

# ⚑ v208 (Tom, C-297 : « après tenir, le trait passe sous le bandeau du haut au lieu de s'y accrocher ») — LA JONCTION DANS QUATRE ÉTATS : en cours, tenu juste
# après la célébration, tenu après rechargement, date passée. Une fiche Promi qui défile (six mots) ; le défilement posé pas à pas (4 pt, une image chacun), de 0 au
# bout. À CHAQUE IMAGE :
#   J1 · la fiche est dans la mise en page de la fiche en cours (flex, colonne — la cause : une règle d'août la passait en bloc une fois tenue) ;
#   J2 · le trait plat est à la jonction (110 pt), et la boîte de la vague suit le contenu (sa place + le défilement ne bouge pas, ± 0,6 pt) ;
#   J3 · dès que le creux de la vague a passé la jonction (le trait plat découvert en entier) : le trait plat est PEINT (au moins 90 % de ses colonnes) et RIEN n'est posé dessus (au doigt, à 114 pt, cinq
#        abscisses : le premier nœud touché est le trait plat ou la fenêtre qui le porte) — le trait accroché, jamais sous le bandeau.
# Rouge sur v207 (J1 dans les états tenus).
GEO = """()=>{ const d=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, c=document.getElementById('v192Colle'),
  pl=document.getElementById('v195Plat'), J=window._v189Jonction&&_v189Jonction(), cv=pl&&(pl.tagName==='CANVAS'?pl:pl.querySelector('canvas'));
  let peint=null; try{ if(cv&&cv.width){ const g=cv.getContext('2d'), h=cv.height, w=cv.width, im=g.getImageData(0,0,w,h).data; let n=0, m=0; for(let x=0;x<w;x+=Math.max(1,Math.floor(w/80))){ m++; for(let y=0;y<h;y++){ if(im[(y*w+x)*4+3]>40){ n++; break; } } } peint=n/m; } }catch(e){}
  let ech=[]; try{ if(cv&&cv.width){ const r=cv.getBoundingClientRect(), g=cv.getContext('2d'), w=cv.width, h=cv.height, im=g.getImageData(0,0,w,h).data, sx=r.width/w, sy=r.height/h;
      for(let x=2;x<w;x+=Math.max(1,Math.floor(w/60))){ let best=-1, ya=0; for(let y=0;y<h;y++){ const a=im[(y*w+x)*4+3]; if(a>230){ if(best<0) best=y; ya=y; } } if(best<0) continue; const y=Math.round((best+ya)/2), i=(y*w+x)*4;
        if(r.top+y*sy-D.top>=112*k+1) ech.push([(r.left+x*sx-D.left)/k, (r.top+y*sy-D.top)/k, im[i], im[i+1], im[i+2]]); } } }catch(e){}
  const dessus=ech;
  return {s:d.scrollTop, smax:d.scrollHeight-d.clientHeight, disp:getComputedStyle(d).display, colle:c?(c.getBoundingClientRect().top-D.top)/k:null, plat:pl?(pl.getBoundingClientRect().top-D.top)/k:null,
    platVu:pl?getComputedStyle(pl).visibility!=='hidden'&&getComputedStyle(pl).display!=='none':false, min:J&&J.F?J.F.min:null, max:J&&J.F?J.F.max:null, peint:peint, dessus:dessus, tenue:d.classList.contains('f-tenue')}; }"""
def jonction(b, F, juge, vw=390, vh=844, nom=''):
    for etat in ('en cours', 'tenu juste après', 'tenu rechargé', 'date passée'):
        ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__jn')){ sessionStorage.setItem('__jn','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
        B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        pid = pg.evaluate("(e)=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); p.who='moi'; p.comments=%s; delete p.parts; if(e==='date passée'){ p.ech={iso:'2026-10-12', due:-30}; p.due=-30; } saveState(true); closeAll(); openDetail(p.id); return p.id; }" % MOTS, etat)
        pg.wait_for_timeout(3000)
        if etat.startswith('tenu'):
            z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
            B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(5000)
        if etat == 'tenu rechargé':
            pg.evaluate("()=>saveState(true)"); pg.reload(); pg.wait_for_timeout(6500); pg.evaluate("id=>{ closeAll(); openDetail(id); }", pid); pg.wait_for_timeout(3000)
        pg.evaluate("()=>{ window._ficheSure=function(t){return t;}; const d=document.getElementById('detailPoster'); d.style.scrollBehavior='auto'; }")
        g0 = pg.evaluate(GEO); R = []
        fin = min(g0['smax'], 320)
        for s in range(0, int(fin) + 1, 4):
            g = pg.evaluate("v=>new Promise(r=>{ document.getElementById('detailPoster').scrollTop=v; requestAnimationFrame(()=>requestAnimationFrame(()=>r((%s)()))); })" % GEO, s)
            R.append(g)
        T = '[%s · %s]' % (nom, etat)
        j1 = [r['s'] for r in R if r['disp'] != 'flex']
        juge(T + ' J1 · la fiche dans la mise en page d’une fiche en cours (flex), à chaque image', not j1 and len(R) > 10, '%d images en %s' % (len(j1), R[0]['disp']) if j1 else '%d images' % len(R))
        c0 = g0['colle'] + g0['s'] if g0['colle'] is not None else None
        j2 = [(round(r['s']), r['plat'] and round(r['plat'], 1), r['colle'] and round(r['colle'] + r['s'], 1)) for r in R if r['plat'] is None or abs(r['plat'] - 110) > 0.6 or not r['platVu'] or c0 is None or r['colle'] is None or abs(r['colle'] + r['s'] - c0) > 0.6]
        juge(T + ' J2 · le trait plat à la jonction (110 pt), la vague qui suit le contenu', not j2, j2[:4])
        acc = [r for r in R if r['max'] is not None and r['max'] - r['s'] <= 108]   # le creux de la vague passé la jonction : le trait plat découvert en entier
        j3 = []
        for r in acc[::2]:
            if (r['peint'] or 0) < 0.9 or len(r['dessus']) < 10: j3.append((round(r['s']), 'peint %s, %d points lus' % (r['peint'], len(r['dessus'])))); continue
            pg.evaluate("v=>new Promise(z=>{ document.getElementById('detailPoster').scrollTop=v; requestAnimationFrame(()=>requestAnimationFrame(z)); })", r['s'])
            d = B.dev(pg); k = d[4]; png = pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': 390 * k, 'height': 160 * k}); a = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(int)
            ok = 0; e = a.shape[1] / 390.0   # pixels de la capture par point de l'appareil (échelle × densité)
            for x, y, R_, G_, B_ in r['dessus']:
                if x < 1 or x > 389: ok += 1; continue
                px = a[min(a.shape[0] - 1, int(y * e)), min(a.shape[1] - 1, int(x * e))]
                ok += abs(px[0] - R_) + abs(px[1] - G_) + abs(px[2] - B_) < 60
            if ok < 0.9 * len(r['dessus']): j3.append((round(r['s']), '%d/%d points du trait plat vus à l’écran' % (ok, len(r['dessus']))))
        juge(T + ' J3 · une fois la vague à la jonction (%d images), le trait plat peint et VU à l’écran (rien dessus)' % len(acc), acc and not j3, j3[:3])
        ctx.close()
