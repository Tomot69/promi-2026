# -*- coding: utf-8 -*-
"""LA DOUCEUR SE MESURE EN CONTRASTE À HAUTE FRÉQUENCE — un pelage de lapin fond
   ses fibres, une boule piquante les détache. On rend, à vue figée :
     · l'écart-type LOCAL de la luminance (3x3) — le « piquant »
     · la part de pixels très clairs (moy + 2σ) — les « éclats blancs »
     · le contraste poil/peau (p95 − p05)
   Et on enregistre une capture agrandie du disque."""
import sys, json, base64
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
NOM = sys.argv[2] if len(sys.argv)>2 else 'avant'
JS = r"""()=>{
  const cv=document.getElementById('auBoule'); if(!cv) return null;
  const W=cv.width, g=cv.getContext('2d'), d=g.getImageData(0,0,W,W).data;
  const CX=W/2, CY=W/2; let R=0;
  for(let x=W-1;x>CX;x--){ if(d[((CY|0)*W+x)*4+3]>8){ R=x-CX; break; } }
  const r2=(R*0.90)*(R*0.90);
  const L=new Float64Array(W*W), IN=new Uint8Array(W*W); let n=0, s=0;
  for(let y=0;y<W;y++) for(let x=0;x<W;x++){
    const dx=x-CX, dy=y-CY; if(dx*dx+dy*dy>r2) continue;
    const i=(y*W+x)*4, l=0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2];
    L[y*W+x]=l; IN[y*W+x]=1; n++; s+=l; }
  const moy=s/n; let v=0; for(let k=0;k<W*W;k++) if(IN[k]) v+=(L[k]-moy)*(L[k]-moy);
  const ec=Math.sqrt(v/n);
  /* écart-type LOCAL 3x3 : le piquant */
  let sl=0, nl=0, clair=0;
  for(let y=1;y<W-1;y++) for(let x=1;x<W-1;x++){
    const k=y*W+x; if(!IN[k]) continue;
    if(L[k]>moy+2*ec) clair++;
    let m=0,q=0,ok=1;
    for(let j=-1;j<=1;j++) for(let i2=-1;i2<=1;i2++){ const kk=k+j*W+i2; if(!IN[kk]){ok=0;break;} m+=L[kk]; }
    if(!ok) continue; m/=9;
    for(let j=-1;j<=1;j++) for(let i2=-1;i2<=1;i2++){ const kk=k+j*W+i2; q+=(L[kk]-m)*(L[kk]-m); }
    sl+=Math.sqrt(q/9); nl++; }
  const tri=[]; for(let k=0;k<W*W;k++) if(IN[k]) tri.push(L[k]); tri.sort((a,b)=>a-b);
  return {R:Math.round(R), n:n, lumMoy:+moy.toFixed(1), ecart:+ec.toFixed(2),
    piquant:+(sl/nl).toFixed(2), partClaire:+(100*clair/n).toFixed(2),
    p05:+tri[(n*0.05)|0].toFixed(0), p50:+tri[(n*0.5)|0].toFixed(0), p95:+tri[(n*0.95)|0].toFixed(0),
    etendue:+(tri[(n*0.95)|0]-tri[(n*0.05)|0]).toFixed(0)};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5500)
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1000)
        pg.evaluate("()=>{try{_aura.fige(true); _aura.vue(2.9,0.32);}catch(e){}}"); pg.wait_for_timeout(1600)
        print(th, json.dumps(pg.evaluate(JS), ensure_ascii=False))
        open('scratchpad/boule-%s-%s.png'%(NOM,th),'wb').write(pg.query_selector('#auBoule').screenshot())
    b.close()
print('captures : scratchpad/boule-%s-*.png' % NOM)
