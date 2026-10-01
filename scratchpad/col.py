# -*- coding: utf-8 -*-
import math
def h2r(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def r2h(r): return '#%02X%02X%02X'%tuple(max(0,min(255,int(round(x)))) for x in r)
def _lin(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    r,g,b=h2r(h) if isinstance(h,str) else h
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def L255(h):
    """luminosité 0-255 au sens du §3 (Δlum seuil 42)"""
    r,g,b=h2r(h) if isinstance(h,str) else h
    return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=lum(a),lum(b)
    if la<lb: la,lb=lb,la
    return (la+0.05)/(lb+0.05)
def xyz(h):
    r,g,b=h2r(h) if isinstance(h,str) else h
    r,g,b=_lin(r),_lin(g),_lin(b)
    return (r*.4124564+g*.3575761+b*.1804375,
            r*.2126729+g*.7151522+b*.0721750,
            r*.0193339+g*.1191920+b*.9503041)
WP=(0.95047,1.0,1.08883)
def lab(h):
    X,Y,Z=xyz(h)
    def f(t): return t**(1/3) if t>0.008856 else (7.787*t+16/116)
    fx,fy,fz=f(X/WP[0]),f(Y/WP[1]),f(Z/WP[2])
    return (116*fy-16, 500*(fx-fy), 200*(fy-fz))
def lab2rgb(L,a,bb):
    fy=(L+16)/116; fx=fy+a/500; fz=fy-bb/200
    def inv(t): return t**3 if t**3>0.008856 else (t-16/116)/7.787
    X,Y,Z=inv(fx)*WP[0],inv(fy)*WP[1],inv(fz)*WP[2]
    r= X*3.2404542+Y*-1.5371385+Z*-0.4985314
    g= X*-0.9692660+Y*1.8760108+Z*0.0415560
    b= X*0.0556434+Y*-0.2040259+Z*1.0572252
    def s(c):
        c=max(0.0,min(1.0,c))
        return 12.92*c if c<=0.0031308 else 1.055*c**(1/2.4)-0.055
    return r2h((s(r)*255,s(g)*255,s(b)*255))
def lch(h):
    L,a,b=lab(h); return (L, math.hypot(a,b), math.degrees(math.atan2(b,a))%360)
def lch2hex(L,C,H):
    return lab2rgb(L, C*math.cos(math.radians(H)), C*math.sin(math.radians(H)))
def dE(a,b):
    la,lb=lab(a),lab(b)
    return math.sqrt(sum((x-y)**2 for x,y in zip(la,lb)))
def dlum(a,b): return abs(L255(a)-L255(b))
