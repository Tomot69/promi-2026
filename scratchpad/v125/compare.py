# compare, dans la même page, à la même vue et au même souffle, le peintre d'origine et la carte graphique : ΔE00 par pixel
import sys, json
from playwright.sync_api import sync_playwright
MOT = sys.argv[1] if len(sys.argv)>1 else 'webkit'
JS = r"""async (th)=>{
  const A=window._aura; A.fige(true); A.vue(3.1,0.32);
  const cv=document.getElementById('auBoule');
  const lit=()=>{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; return d; };
  const att=(ms)=>new Promise(r=>setTimeout(r,ms));
  window._peloteGL=false; A.pelote(); await att(500); const a=new Uint8ClampedArray(lit()); const n0=cv.__gl||0;
  window._peloteGL=true;  A.pelote(); await att(500); const b=new Uint8ClampedArray(lit()); const n1=cv.__gl||0;
  // ΔE00 (CIELAB) par pixel, composé sur le fond de la page
  const bg=getComputedStyle(document.getElementById('auraScreen')).backgroundColor.match(/\d+/g).map(Number);
  function lab(r,g,b){ const f=v=>{v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; r=f(r);g=f(g);b=f(b);
    let x=(r*0.4124+g*0.3576+b*0.1805)/0.95047, y=r*0.2126+g*0.7152+b*0.0722, z=(r*0.0193+g*0.1192+b*0.9505)/1.08883;
    const h=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116; x=h(x);y=h(y);z=h(z); return [116*y-16,500*(x-y),200*(y-z)]; }
  function de00(A,B){ const [L1,a1,b1]=A,[L2,a2,b2]=B, rad=Math.PI/180; const C1=Math.hypot(a1,b1),C2=Math.hypot(a2,b2),Cm=(C1+C2)/2;
    const G=0.5*(1-Math.sqrt(Math.pow(Cm,7)/(Math.pow(Cm,7)+Math.pow(25,7)))); const a1p=a1*(1+G),a2p=a2*(1+G);
    const C1p=Math.hypot(a1p,b1),C2p=Math.hypot(a2p,b2); let h1=Math.atan2(b1,a1p)/rad; if(h1<0)h1+=360; let h2=Math.atan2(b2,a2p)/rad; if(h2<0)h2+=360;
    const dL=L2-L1,dC=C2p-C1p; let dh=h2-h1; if(C1p*C2p===0)dh=0; else if(dh>180)dh-=360; else if(dh<-180)dh+=360;
    const dH=2*Math.sqrt(C1p*C2p)*Math.sin(dh*rad/2); const Lm=(L1+L2)/2,Cpm=(C1p+C2p)/2; let hm=h1+h2; if(C1p*C2p!==0){ if(Math.abs(h1-h2)>180) hm+= (hm<360?360:-360); hm/=2; }
    const T=1-0.17*Math.cos((hm-30)*rad)+0.24*Math.cos(2*hm*rad)+0.32*Math.cos((3*hm+6)*rad)-0.20*Math.cos((4*hm-63)*rad);
    const Sl=1+0.015*(Lm-50)**2/Math.sqrt(20+(Lm-50)**2),Sc=1+0.045*Cpm,Sh=1+0.015*Cpm*T; const dt=30*Math.exp(-(((hm-275)/25)**2));
    const Rc=2*Math.sqrt(Math.pow(Cpm,7)/(Math.pow(Cpm,7)+Math.pow(25,7))),Rt=-Rc*Math.sin(2*dt*rad);
    return Math.sqrt((dL/Sl)**2+(dC/Sc)**2+(dH/Sh)**2+Rt*(dC/Sc)*(dH/Sh)); }
  const W=cv.width; let n=0, s=0, mx=0, sup2=0, sup5=0, difA=0; const ma=[0,0,0], mb=[0,0,0]; const L=[];
  for(let i=0;i<a.length;i+=4){ const aa=a[i+3]/255, ab=b[i+3]/255; if(!a[i+3] && !b[i+3]) continue; n++;
    if(Math.abs(a[i+3]-b[i+3])>8) difA++;
    const ca=[0,1,2].map(k=>a[i+k]*aa+bg[k]*(1-aa)), cb=[0,1,2].map(k=>b[i+k]*ab+bg[k]*(1-ab));
    for(let k=0;k<3;k++){ ma[k]+=ca[k]; mb[k]+=cb[k]; }
    const d=de00(lab(...ca),lab(...cb)); s+=d; if(d>mx)mx=d; if(d>2)sup2++; if(d>5)sup5++; }
  // à l'échelle de l'œil : moyenne par blocs de 8 px du tampon (≈ 4 pt)
  const BL=8; let bs=0,bn=0,bmx=0,b2=0;
  for(let y=0;y<W;y+=BL) for(let x=0;x<W;x+=BL){ const sa=[0,0,0], sb=[0,0,0]; let c=0, vis=0;
    for(let j=0;j<BL;j++) for(let i2=0;i2<BL;i2++){ const o=((y+j)*W+x+i2)*4; const aa=a[o+3]/255, ab=b[o+3]/255; if(a[o+3]||b[o+3]) vis++;
      for(let k=0;k<3;k++){ sa[k]+=a[o+k]*aa+bg[k]*(1-aa); sb[k]+=b[o+k]*ab+bg[k]*(1-ab); } c++; }
    if(!vis) continue; const d=de00(lab(sa[0]/c,sa[1]/c,sa[2]/c),lab(sb[0]/c,sb[1]/c,sb[2]/c)); bs+=d; bn++; if(d>bmx)bmx=d; if(d>2)b2++; }
  return {th, gl:n1-n0, err:window._peloteGLErreur||null, W, pixels:n, moyenne:+(s/n).toFixed(3), max:+mx.toFixed(2), 'part>2':+(sup2/n*100).toFixed(2), 'part>5':+(sup5/n*100).toFixed(2), alphaDiff:difA,
    moyA:ma.map(v=>+(v/n).toFixed(2)), moyB:mb.map(v=>+(v/n).toFixed(2)), blocs:{n:bn, moyenne:+(bs/bn).toFixed(3), max:+bmx.toFixed(2), 'n>2':b2}};
}"""
with sync_playwright() as p:
    b = (p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t); try{ _peloteLumiere.recalibre(); }catch(e){} }", th); pg.wait_for_timeout(600)
        pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
        pg.wait_for_timeout(4500)
        print(MOT, json.dumps(pg.evaluate(JS, th), ensure_ascii=False))
        pg.evaluate("()=>{_aura.fige(false); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(800)
    b.close()
