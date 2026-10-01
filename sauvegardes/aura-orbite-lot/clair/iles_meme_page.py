# Vérifier l'INSTRUMENT avant de croire un chiffre : dans la MÊME page, pour chaque île réelle,
#   · son centre projeté, marqué sur l'image entière (le numéro de l'île) — la projection est-elle juste ?
#   · la composante du masque retenue (aire, écart moyen) — et son rectangle, tracé sur l'image
#   · l'écart mesuré dans un DISQUE autour du centre (sans seuil ni composante) : moyenne de |Δlum| et signe
#   python3 iles_meme_page.py URL DOSSIER [chargements]
import sys, os, base64, io
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; K = int(sys.argv[3]) if len(sys.argv) > 3 else 2; os.makedirs(OUT, exist_ok=True)
INV = r"""([fond])=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=window.__i_avec, s0=window.__i_sans, c=W/2, R=W*0.392;
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b, comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  // CIELAB (D65), depuis le sRGB composé sur le fond de la page
  const lin=v=>{ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); }, fl=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;
  const lab=(r,g,b)=>{ r=lin(r); g=lin(g); b=lin(b); const X=(0.4124*r+0.3576*g+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g+0.0722*b, Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;
    const fx=fl(X), fy=fl(Y), fz=fl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; };
  const S=2, G=Math.ceil(W/S), M=new Float32Array(G*G).fill(-1);
  for(let y=0;y<W;y+=S) for(let x=0;x<W;x+=S){ if(Math.hypot(x-c,y-c)/R>0.90) continue; const i=(y*W+x)*4, e=Math.abs(lum(d,i)-lum(s0,i)); if(e>12) M[(y/S)*G+(x/S)]=e; }
  const lbl=new Int32Array(G*G).fill(-1), comps=[];
  for(let k=0;k<G*G;k++){ if(M[k]<0||lbl[k]>=0) continue; const id=comps.length; let pile=[k], n=0, s=0, x0=1e9,y0=1e9,x1=-1,y1=-1; lbl[k]=id;
    while(pile.length){ const q=pile.pop(); n++; s+=M[q]; const qx=q%G, qy=(q/G)|0; x0=Math.min(x0,qx); x1=Math.max(x1,qx); y0=Math.min(y0,qy); y1=Math.max(y1,qy);
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const nx=qx+dx, ny=qy+dy; if(nx<0||ny<0||nx>=G||ny>=G) continue; const z=ny*G+nx;
        if(M[z]>=0&&lbl[z]<0){ lbl[z]=id; pile.push(z); } } }
    comps.push({n:n, ecart:s/n, box:[x0*S,y0*S,(x1+1)*S,(y1+1)*S]}); }
  const e=_aura.etat(), B=OrbiteMoteur.batIles(_auraComp.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan);
  const iles=B.iles.map((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct;
    const px=c+X*R, py=c+Y*R, g=((py/S)|0)*G+((px/S)|0);
    let id=(g>=0&&g<G*G)?lbl[g]:-1, cherche=false;
    if(id<0){ cherche=true; let best=1e9; for(let dy=-12;dy<=12;dy++) for(let dx=-12;dx<=12;dx++){ const z=g+dy*G+dx; if(z>=0&&z<G*G&&lbl[z]>=0){ const dd=dx*dx+dy*dy; if(dd<best){best=dd; id=lbl[z];} } } }
    // disque : rayon 0,5 × le rayon de l'île projeté (le cœur de la dalle), tous pixels, sans seuil
    const rd=Math.max(6, I.r*R*0.5*Math.max(0.3,Z)); let n=0, sa=0, ss=0, la=0, ls=0, de=0; const LA=[0,0,0], LS=[0,0,0];
    for(let y=Math.floor(py-rd); y<=py+rd; y++) for(let x=Math.floor(px-rd); x<=px+rd; x++){ if(x<0||y<0||x>=W||y>=W||Math.hypot(x-px,y-py)>rd) continue;
      const i=(y*W+x)*4, a=lum(d,i), b=lum(s0,i); n++; sa+=Math.abs(a-b); ss+=a-b; la+=a; ls+=b;
      const A=lab(comp(d,i,0),comp(d,i,1),comp(d,i,2)), Bb=lab(comp(s0,i,0),comp(s0,i,1),comp(s0,i,2));
      for(let t=0;t<3;t++){ LA[t]+=A[t]; LS[t]+=Bb[t]; } de+=Math.hypot(A[0]-Bb[0],A[1]-Bb[1],A[2]-Bb[2]); }
    const dEm=Math.hypot(LA[0]/n-LS[0]/n, LA[1]/n-LS[1]/n, LA[2]/n-LS[2]/n);
    return {k:k, x:px, y:py, z:+Z.toFixed(2), r:I.r*R, comp:id, cherche:cherche, aire:id>=0?comps[id].n:0, ecart:id>=0?+comps[id].ecart.toFixed(1):null, box:id>=0?comps[id].box:null,
            disque:+(sa/n).toFixed(1), signe:+(ss/n).toFixed(1), lumIle:+(la/n).toFixed(0), lumSol:+(ls/n).toFixed(0), dE:+dEm.toFixed(1), dEpix:+(de/n).toFixed(1)}; });
  const grandes=comps.map((q,i)=>({i:i,n:q.n,ecart:+q.ecart.toFixed(1),box:q.box})).filter(q=>q.n>=100);
  return {iles:iles, grandes:grandes}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for ch in range(1, K + 1):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        def peintes(n=8):
            p0 = pg.evaluate("()=>_aura.etat().peints")
            for _ in range(300):
                if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
                pg.wait_for_timeout(50)
        for th, fond in (('dark', (22, 23, 27)), ('light', (244, 238, 225))):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
            pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(80):
                pg.wait_for_timeout(250)
                if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__i_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__u=cv.toDataURL('image/png');}")
            pg.evaluate("()=>_aura.sansIles(true)"); peintes()
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__i_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
            pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
            r = pg.evaluate(INV, [list(fond)]); u = pg.evaluate("()=>window.__u"); pg.evaluate("()=>_aura.fige(false)")
            im = Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
            f = Image.new('RGBA', im.size, fond + (255,)); f.alpha_composite(im); f = f.convert('RGB'); dr = ImageDraw.Draw(f)
            for q in r['grandes']: dr.rectangle(q['box'], outline=(255, 200, 0), width=2)
            for I in r['iles']:
                dr.ellipse([I['x'] - 10, I['y'] - 10, I['x'] + 10, I['y'] + 10], outline=(255, 0, 0), width=4)
                dr.text((I['x'] + 14, I['y'] - 10), str(I['k']), fill=(255, 0, 0))
            f.save(os.path.join(OUT, 'ch%d-%s-marques.png' % (ch, th)))
            print('chargement %d · %s' % (ch, th))
            for I in r['iles']:
                print('   île %d z %.2f  composante %3s%s aire %4d écart %5s  |  disque |Δlum| %5.1f  Δlum des moyennes %+6.1f  (île %s / sol %s)  ΔE des moyennes %5.1f  ΔE moyen %5.1f' % (
                    I['k'], I['z'], I['comp'], ' (cherchée)' if I['cherche'] else '', I['aire'], I['ecart'], I['disque'], I['signe'], I['lumIle'], I['lumSol'], I['dE'], I['dEpix']))
            print('   composantes ≥ 100 cellules :', [(q['i'], q['n'], q['ecart']) for q in r['grandes']])
        pg.close()
    b.close()
