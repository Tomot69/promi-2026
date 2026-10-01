# LISIBILITÉ contre SATURATION. Mesures : fond visible, teintes, et LONGUEUR MOYENNE DES PLAGES d'une même
# couleur sur une ligne — courte = confetti, longue = grosses dalles lisibles.
# Et un ORDRE : les mondes qui REMPLISSENT en dessous, les ajourés au-dessus (la Touffe se lit posée sur autre chose).
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toileA.html'
Q=r"""([COTE,N1,N2,N3])=>{
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const PLEIN=['encre','terrazzo','pixel','mosaique'], LIGNE=['braille','sillons','gravure'], HAUT=['touffe'];
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=window.Toile.mondeCourant()||{};
  const cache={};
  function dalle(id,m,cote){
    const cle=id+'|'+m+'|'+cote; if(cache[cle]!==undefined) return cache[cle];
    let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
    if(!d||!d.w) return (cache[cle]=null);
    const k=cote/Math.max(d.w,d.h), cv=document.createElement('canvas');
    let ok=false; try{ ok=window.Toile.dalleTrame(cv,id,k,{m:m,p:base.p,h:base.h}); }catch(e){}
    return (cache[cle]=(ok&&cv.width)?cv:null);
  }
  const cible=document.createElement('canvas'); cible.width=Math.round(W*dpr); cible.height=Math.round(H*dpr);
  const G=cible.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
  const t0=performance.now();
  function couche(mondes, n, cote){
    for(let i=0;i<n;i++){
      const id=ids[(Math.random()*ids.length)|0], m=mondes[(Math.random()*mondes.length)|0];
      const c=Math.round(cote*(0.85+Math.random()*0.3/0.3*0.0001+ (i%2?0.22:0)));   /* deux tailles seulement : le cache tient */
      const cv=dalle(id,m,c); if(!cv) continue;
      const w=cv.width/dpr, h=cv.height/dpr;
      G.save(); G.translate(Math.random()*W, Math.random()*H); G.rotate(Math.random()*6.2832);
      G.drawImage(cv,-w/2,-h/2,w,h); G.restore();
    }
  }
  couche(PLEIN, N1, COTE);
  couche(LIGNE, N2, COTE);
  couche(HAUT,  N3, COTE);
  const ms=Math.round(performance.now()-t0);
  const px=G.getImageData(0,0,cible.width,cible.height).data;
  const Wp=cible.width, Hp=cible.height;
  let vide=0,n=0; const cnt={};
  for(let i=3;i<px.length;i+=32){ n++; if(px[i]<20) vide++; }
  /* longueur moyenne des plages d'une même couleur quantifiée, sur une ligne */
  let runs=0, total=0;
  for(let y=4;y<Hp;y+=8){
    let prev=-1, len=0;
    for(let x=0;x<Wp;x++){ const o=(y*Wp+x)*4;
      const q=((px[o]>>4)<<8)|((px[o+1]>>4)<<4)|(px[o+2]>>4);
      cnt[q]=1;
      if(q===prev) len++; else { if(prev>=0){ runs++; total+=len; } prev=q; len=1; }
    }
    runs++; total+=len;
  }
  return {cote:COTE, poses:N1+N2+N3, rendus:Object.keys(cache).length, ms,
          fond:+(100*vide/n).toFixed(2), teintes:Object.keys(cnt).length,
          plage:+(total/Math.max(1,runs)).toFixed(1)}; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    print('  côté · poses · rendus · coût · FOND · teintes · PLAGE moyenne (px) — plus long = plus lisible')
    for cote,n1,n2,n3 in ((70,300,250,210),(110,30,18,14),(110,40,24,18),(130,26,14,12),(150,20,12,10),(130,34,18,16)):
        r=pg.evaluate(Q,[cote,n1,n2,n3])
        print('   %3d · %4d · %3d rendus · %4d ms · fond %5.2f %% · %3d teintes · plage %5.1f'
              % (r['cote'], r['poses'], r['rendus'], r['ms'], r['fond'], r['teintes'], r['plage']))
    br.close()
