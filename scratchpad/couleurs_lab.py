# -*- coding: utf-8 -*-
"""Boîte à outils colorimétrique (sRGB ↔ CIELAB ↔ LCh) + transport d'un dérivé d'une ancre à l'autre."""
import math
def hex2rgb(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4))
def rgb2hex(r,g,b):
    f=lambda v:max(0,min(255,int(round(v))))
    return '#%02X%02X%02X'%(f(r),f(g),f(b))
def _lin(c):
    c/=255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def rgb2xyz(r,g,b):
    R,G,B=_lin(r),_lin(g),_lin(b)
    return (R*.4124564+G*.3575761+B*.1804375, R*.2126729+G*.7151522+B*.0721750, R*.0193339+G*.1191920+B*.9503041)
def _f(t): return t**(1/3) if t>216/24389 else (841/108)*t+4/29
def rgb2lab(r,g,b):
    X,Y,Z=rgb2xyz(r,g,b); Xn,Yn,Zn=.95047,1.0,1.08883
    fx,fy,fz=_f(X/Xn),_f(Y/Yn),_f(Z/Zn)
    return (116*fy-16, 500*(fx-fy), 200*(fy-fz))
def _fi(t): return t**3 if t**3>216/24389 else (108/841)*(t-4/29)
def lab2rgb(L,a,bb):
    fy=(L+16)/116; fx=fy+a/500; fz=fy-bb/200
    X,Y,Z=.95047*_fi(fx),1.0*_fi(fy),1.08883*_fi(fz)
    R= X* 3.2404542+Y*-1.5371385+Z*-0.4985314
    G= X*-0.9692660+Y* 1.8760108+Z* 0.0415560
    B= X* 0.0556434+Y*-0.2040259+Z* 1.0572252
    g=lambda c: 12.92*c if c<=0.0031308 else 1.055*(max(c,0)**(1/2.4))-0.055
    return (g(R)*255,g(G)*255,g(B)*255)
def lab2lch(L,a,b):
    C=math.hypot(a,b); h=math.degrees(math.atan2(b,a))%360
    return (L,C,h)
def lch2lab(L,C,h):
    r=math.radians(h); return (L,C*math.cos(r),C*math.sin(r))
def lch(h_):
    return lab2lch(*rgb2lab(*hex2rgb(h_)))
def de(h1,h2):
    a=rgb2lab(*hex2rgb(h1)); b=rgb2lab(*hex2rgb(h2))
    return math.dist(a,b)
def dlum(h1,h2):
    """écart de luminosité au sens du §3 (L* CIELAB)"""
    return abs(rgb2lab(*hex2rgb(h1))[0]-rgb2lab(*hex2rgb(h2))[0])
def transporte(derive, ancre_avant, ancre_apres):
    """le dérivé garde le MÊME rapport (ΔL, ΔC, Δh) à sa nouvelle ancre qu'à l'ancienne"""
    Ld,Cd,hd = lch(derive); La,Ca,ha = lch(ancre_avant); Lb,Cb,hb = lch(ancre_apres)
    L = Lb + (Ld-La)
    C = max(0.0, Cb + (Cd-Ca))
    h = (hb + (hd-ha)) % 360
    L=max(0.0,min(100.0,L))
    r,g,b = lab2rgb(*lch2lab(L,C,h))
    # si ça sort du gamut, on réduit la chroma jusqu'à rentrer
    k=1.0
    while (min(r,g,b)<-0.5 or max(r,g,b)>255.5) and k>0.02:
        k-=0.04; r,g,b=lab2rgb(*lch2lab(L,C*k,h))
    return rgb2hex(r,g,b)
