import math
def lin(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(h): r,g,b=[int(h[i:i+2],16) for i in (1,3,5)]; return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def cr(a,b): x,y=sorted((L(a),L(b)),reverse=True); return (x+0.05)/(y+0.05)
def lab(h):
    r,g,b=[lin(int(h[i:i+2],16)) for i in (1,3,5)]
    X=(0.4124*r+0.3576*g+0.1805*b)/0.95047; Y=0.2126*r+0.7152*g+0.0722*b; Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return 116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z))
def dE(a,b): return math.dist(lab(a),lab(b))
for nom,c in (('encre (titre, texte)','#201908'),('à tenir #DD4D23 (texte et trait)','#DD4D23'),('en cours #291547','#291547'),('tenu #00341A (mention, arc)','#00341A'),('crête tenue #0B4A2A','#0B4A2A'),('trait Promi #022140','#022140'),('trait Chiche #3D0F23','#3D0F23'),('violet Cercle #291547','#291547'),('brun encre Cercle #43291C','#43291C')):
    print('%-36s sur #F7F0DE : %5.2f:1 · ΔE %5.1f   →   sur #EAD9B9 : %5.2f:1 · ΔE %5.1f'%(nom,cr(c,'#F7F0DE'),dE(c,'#F7F0DE'),cr(c,'#EAD9B9'),dE(c,'#EAD9B9')))
for nom,c in (('bande Promi #82AEF8','#82AEF8'),('bande Chiche #FFB8D2','#FFB8D2'),('bande Cercle #C9A8F5','#C9A8F5'),('carte du Cercle #F7F0DE','#F7F0DE')):
    print('%-36s contre corps : ΔE %5.1f → %5.1f'%(nom,dE(c,'#F7F0DE'),dE(c,'#EAD9B9')))
