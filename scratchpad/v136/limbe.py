# même vue, même tirage : on force le sol et le corps par le stockage (promi_pelote_vue) n'est pas sûr — on compare donc le PROFIL RADIAL :
# la couleur moyenne par anneau, de 0,80 R au bord, et l'écart (ΔE) entre l'intérieur (0,80–0,88 R) et chaque anneau du limbe
from playwright.sync_api import sync_playwright
from PIL import Image
import io, math, sys
def lab(c):
    def lin(v): v/=255; return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
    r,g,b=[lin(v) for v in c]; X=(0.4124*r+0.3576*g+0.1805*b)/0.95047; Y=0.2126*r+0.7152*g+0.0722*b; Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return (116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z)))
def profil(url, th, n=6):
    out=[]
    with sync_playwright() as p:
        b=p.webkit.launch()
        for k in range(n):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6000)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); const s=document.createElement('style'); s.textContent='#auPeloteHalo,#auPeloteOmbre{visibility:hidden!important}'; document.head.appendChild(s); document.getElementById('souffleBtn').click();}",th); pg.wait_for_timeout(5000)
            pg.evaluate("()=>{ try{ _aura.fige(true); }catch(e){} }"); pg.wait_for_timeout(300)
            g=pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
            im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); cx,cy=g[0]*3,g[1]*3; R=121*3
            def anneau(a,b_):
                s=[0,0,0]; m=0
                for ang in range(0,360,3):
                    # hors des îles : on ne prend que le demi-tour gauche et le bas (les îles sont à droite du centre) — et on saute les pixels trop loin de la médiane
                    for rr in (a+(b_-a)*q/3 for q in range(4)):
                        x=int(cx+rr*R*math.cos(math.radians(ang))); y=int(cy+rr*R*math.sin(math.radians(ang))); c=im.getpixel((x,y)); s=[s[i]+c[i] for i in range(3)]; m+=1
                return [v/m for v in s]
            ref=anneau(0.78,0.86); pire=0; ou=0
            for a in (0.88,0.90,0.92,0.94,0.955,0.97):
                c=anneau(a,a+0.012); d=math.dist(lab(ref),lab(c))
                if d>pire: pire,ou=d,a
            out.append((round(pire,1),ou)); ctx.close()
        b.close()
    return out
if __name__=='__main__':
    for th in ('light','dark'):
        for url in sys.argv[1:]: print(th, url, profil(url, th))
