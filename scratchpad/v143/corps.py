# §8 — le corps de la Pelote a toujours une autre couleur que le pelage : chaque palette, dix ouvertures (ΔE00 entre le corps et le poil tirés)
import sys, math, re, io
from playwright.sync_api import sync_playwright
def lab(c):
    r,g,b=[v/255.0 for v in c]; f=lambda u: ((u+0.055)/1.055)**2.4 if u>0.04045 else u/12.92; r,g,b=f(r),f(g),f(b)
    x=(0.4124*r+0.3576*g+0.1805*b)/0.95047; y=0.2126*r+0.7152*g+0.0722*b; z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    h=lambda t: t**(1/3.0) if t>0.008856 else 7.787*t+16/116.0; return (116*h(y)-16, 500*(h(x)-h(y)), 200*(h(y)-h(z)))
def de00(c1,c2):
    L1,a1,b1=lab(c1); L2,a2,b2=lab(c2); C1=math.hypot(a1,b1); C2=math.hypot(a2,b2); Cm=(C1+C2)/2; G=0.5*(1-math.sqrt(Cm**7/(Cm**7+25**7)))
    a1p=(1+G)*a1; a2p=(1+G)*a2; C1p=math.hypot(a1p,b1); C2p=math.hypot(a2p,b2); h1=math.degrees(math.atan2(b1,a1p))%360; h2=math.degrees(math.atan2(b2,a2p))%360
    dL=L2-L1; dC=C2p-C1p; dh=h2-h1; dh=dh-360 if dh>180 else (dh+360 if dh<-180 else dh); dH=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dh/2))
    Lm=(L1+L2)/2; Cmp=(C1p+C2p)/2; hm=(h1+h2)/2 if abs(h1-h2)<=180 else (h1+h2+360)/2
    T=1-0.17*math.cos(math.radians(hm-30))+0.24*math.cos(math.radians(2*hm))+0.32*math.cos(math.radians(3*hm+6))-0.20*math.cos(math.radians(4*hm-63))
    Sl=1+0.015*(Lm-50)**2/math.sqrt(20+(Lm-50)**2); Sc=1+0.045*Cmp; Sh=1+0.015*Cmp*T; Rc=2*math.sqrt(Cmp**7/(Cmp**7+25**7)); Rt=-Rc*math.sin(math.radians(60*math.exp(-((hm-275)/25)**2)))
    return math.sqrt((dL/Sl)**2+(dC/Sc)**2+(dH/Sh)**2+Rt*(dC/Sc)*(dH/Sh))
N=int(sys.argv[1]) if len(sys.argv)>1 else 10
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); out=[]
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s');localStorage.setItem('geste_vu_pelote','1');}catch(e){}"%th)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
        P=pg.evaluate("()=>{ const m=/var PALS=\\{/.exec(''); try{ return Object.keys(Toile.palettes?Toile.palettes():{}) }catch(e){ return [] } }")
        if not P:
            S=io.open('promi-moteur.js',encoding='utf-8').read(); i=S.index('var PALS={'); P=re.findall(r"(\w+):\{name:'", S[i:i+9000])
        for pal in P:
            L=[]
            for k in range(N):
                pg.evaluate("(p)=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); try{Toile.setPalette(p)}catch(e){} }",pal); pg.wait_for_timeout(250)
                pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(900)
                c=pg.evaluate("()=>{try{const c=_aura.corps(); return [c.rgb,c.poil]}catch(e){return null}}")
                if c: L.append(de00(c[0],c[1]))
            out.append((th,pal,min(L) if L else -1, sorted(L)[len(L)//2] if L else -1, len(L)))
            print('%-6s %-14s ΔE00 corps ↔ pelage : plus faible %5.1f · médiane %5.1f · %d ouvertures %s'%(th,pal,out[-1][2],out[-1][3],out[-1][4],'' if out[-1][2]>=15 else '  ← SOUS 15'),flush=True)
        ctx.close()
    b.close()
print('\npalettes × thèmes : %d · sous le plancher (15) : %d · plus faible : %.1f'%(len(out),sum(1 for o in out if o[2]<15),min(o[2] for o in out)))
