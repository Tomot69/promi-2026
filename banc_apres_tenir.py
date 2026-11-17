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
