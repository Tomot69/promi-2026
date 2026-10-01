# DEUX MESURES qui décident des corrections 1 et 2 :
#  1 · dalleTrame(cv, id, k, monde) sait-elle peindre à la TAILLE FINALE (k < 1) ? Si oui : plus aucun
#      redimensionnement pour les pastilles — le moteur peint directement à 16 px.
#  2 · QUEL MONDE laisse voir le fond ? On rend chaque monde seul et on compte les pixels transparents.
#      Si la Touffe est ajourée, c'est elle la cause du fond visible — pas l'espacement des germes.
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile6.html'
Q=r"""()=>{
  const o={k:[], opacite:[]};
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=window.Toile.mondeCourant()||{};
  const d0=window.Toile.dalleAbs(ids[0]);
  /* 1 · l'échelle k */
  [1, 0.5, 0.25, 0.16, 0.10].forEach(k=>{
    const c=document.createElement('canvas'); let ok=false;
    try{ ok=window.Toile.dalleTrame(c, ids[0], k, {m:'sillons', p:base.p, h:base.h}); }catch(e){}
    let peints=0, n=0;
    if(ok&&c.width){ const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
      for(let i=3;i<d.length;i+=4){ n++; if(d[i]>10) peints++; } }
    o.k.push({k, ok:!!ok, px:[c.width,c.height], part:n?+(100*peints/n).toFixed(1):0});
  });
  o.cellule={w:+d0.w.toFixed(1), h:+d0.h.toFixed(1)};
  /* 2 · l'opacité de chaque monde, sur le MÊME semis */
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const A=document.createElement('canvas'); A.width=Math.round(W*dpr); A.height=Math.round(H*dpr);
  window.Toile.preview(A,'encre',W,H);
  const tpl=(A.__c.seeds.filter(s=>s.kind!=='gray')[0])||A.__c.seeds[0];
  const PAL=window.Toile.cols()||[];
  const gc=14, gr=9, cw=W/gc, ch=H/gr, seeds=[];
  for(let r=0;r<gr;r++) for(let c=0;c<gc;c++){
    const s={}; for(const k in tpl) s[k]=tpl[k];
    s.x=cw*(c+.5); s.y=ch*(r+.5); s.tx=s.x; s.ty=s.y; s.px=null; s.py=null; s.w=0; s.wt=0; s.t0=-99999; s.gc=null;
    s.kind='promi'; s.ci=(Math.random()*PAL.length)|0; s.c=PAL[s.ci]; seeds.push(s);
  }
  ['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'].forEach(w=>{
    const cv=document.createElement('canvas'); cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    cv.__c={seeds:seeds.map(s=>Object.assign({},s)), th:w, pw:W, ph:H};
    window.Toile.repaint(cv);
    const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    let opa=0,n=0; for(let i=3;i<d.length;i+=20){ n++; if(d[i]>200) opa++; }
    o.opacite.push({monde:w, opaque:+(100*opa/n).toFixed(1)});
  });
  return o; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(500)
    R=pg.evaluate(Q)
    print('cellule de référence : %s' % R['cellule'])
    print('1 · dalleTrame à l’échelle k :')
    for e in R['k']: print('     k=%-5s ok=%-5s canevas %-12s peint %s %%' % (e['k'], e['ok'], e['px'], e['part']))
    print('2 · part OPAQUE de chaque monde, même semis :')
    for e in sorted(R['opacite'], key=lambda x:x['opaque']): print('     %-10s %5.1f %%' % (e['monde'], e['opaque']))
    br.close()
