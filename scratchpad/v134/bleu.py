import math
def h2(h): h=h.lstrip('#'); return [int(h[i:i+2],16) for i in (0,2,4)]
def hx(c): return '#%02X%02X%02X'%tuple(max(0,min(255,round(v))) for v in c)
def lin(v): v/=255; return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
def gam(v): v=max(0,min(1,v)); return 255*(12.92*v if v<=0.0031308 else 1.055*v**(1/2.4)-0.055)
def L(c): r,g,b=[lin(v) for v in c]; return 0.2126*r+0.7152*g+0.0722*b
def K(a,b): la,lb=L(a),L(b); return (max(la,lb)+0.05)/(min(la,lb)+0.05)
def oklab(c):
    r,g,b=[lin(v) for v in c]; l=(0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m=(0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s=(0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return [0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s]
def rgb(o):
    Lq,a,b=o; l=(Lq+0.3963377774*a+0.2158037573*b)**3; m=(Lq-0.1055613458*a-0.0638541728*b)**3; s=(Lq-0.0894841775*a-1.2914855480*b)**3
    return [gam(4.0767416621*l-3.3077115913*m+0.2309699292*s), gam(-1.2684380046*l+2.6097574011*m-0.3413193965*s), gam(-0.0041960863*l-0.7034186147*m+1.7076147010*s)]
def ajuste(c,f,k):
    o=oklab(c); Lq=o[0]
    while Lq<1:
        r=[round(v) for v in rgb([Lq,o[1],o[2]])]
        if K(r,f)>=k: return r
        Lq+=0.001
    return [255,255,255]
def lab(c):
    r,g,b=[lin(v) for v in c]; X=(0.4124*r+0.3576*g+0.1805*b)/0.95047; Y=0.2126*r+0.7152*g+0.0722*b; Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return [116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z))]
def dE(a,b): A,B=lab(a),lab(b); return math.dist(A,B)
def lum(c): return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
for B in ('#1A52F0','#0E78F2'):
    f=h2(B); print(B,'crème %.2f:1'%K(h2('#F7F0DE'),f),'| orange→',hx(ajuste(h2('#FB4C0D'),f,3)),'%.2f'%K(ajuste(h2('#FB4C0D'),f,3),f),'| lilas→',hx(ajuste(h2('#C4A2F5'),f,4.5)),'%.2f'%K(ajuste(h2('#C4A2F5'),f,4.5),f))
    for n,c in (('à tenir','#DD4D23'),('en cours','#291547'),('en cours clair','#A77CF7'),('tenu','#00341A'),('tenu clair','#33BA6C'),('amande','#8FE08F'),('trait Promi','#022140'),('bande','#82AEF8'),('crème','#F7F0DE'),('encre','#201908')):
        print('   %-15s %s  ΔE %.1f  Δlum %.1f  contraste %.2f:1'%(n,c,dE(h2(c),f),abs(lum(h2(c))-lum(f)),K(h2(c),f)))
print('---- éclaircir en gardant la teinte (chroma réduite quand la couleur sort du gamut)')
def rgbl(o):
    Lq,a,b=o; l=(Lq+0.3963377774*a+0.2158037573*b)**3; m=(Lq-0.1055613458*a-0.0638541728*b)**3; s=(Lq-0.0894841775*a-1.2914855480*b)**3
    return [4.0767416621*l-3.3077115913*m+0.2309699292*s, -1.2684380046*l+2.6097574011*m-0.3413193965*s, -0.0041960863*l-0.7034186147*m+1.7076147010*s]
def dans(o):
    k=1.0
    while k>0:
        v=rgbl([o[0],o[1]*k,o[2]*k])
        if all(-0.0005<=x<=1.0005 for x in v): return [round(gam(x)) for x in v],k
        k-=0.01
    return [round(gam(x)) for x in rgbl([o[0],0,0])],0
def eclaircit(c,f,k):
    o=oklab(c); Lq=o[0]; best=None
    while Lq<=1.0:
        r,kc=dans([Lq,o[1],o[2]])
        if K(r,f)>=k: return r,kc,Lq
        best=(r,kc,Lq); Lq+=0.002
    return best
f=h2('#0E78F2')
for nom,c,k in (('orange Ma Parole 3:1','#FB4C0D',3),('lilas 4,5:1','#C4A2F5',4.5),('lilas au niveau de la crème 3,70:1','#C4A2F5',K(h2('#F7F0DE'),f)),('lilas 4:1','#C4A2F5',4.0)):
    r,kc,Lq=eclaircit(h2(c),f,k); o0=oklab(h2(c)); o1=oklab(r)
    print('%-36s %s  %.2f:1  chroma gardée %.0f %%  (C %.3f → %.3f, teinte %.0f° → %.0f°)'%(nom,hx(r),K(r,f),kc*100,math.hypot(o0[1],o0[2]),math.hypot(o1[1],o1[2]),math.degrees(math.atan2(o0[2],o0[1]))%360,math.degrees(math.atan2(o1[2],o1[1]))%360))
print('blanc %.2f:1'%K([255,255,255],f))
