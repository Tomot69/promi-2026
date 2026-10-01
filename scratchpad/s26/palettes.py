# -*- coding: utf-8 -*-
"""Mesure des palettes du Studio : ecart perceptuel entre les quatre tons (DeltaE 2000),
   et distance d'une palette a toutes les autres (moyenne symetrique des plus proches)."""
import json, math, itertools, sys

def srgb2lin(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def rgb2lab(rgb):
    r,g,b=[srgb2lin(v) for v in rgb]
    X=r*0.4124564+g*0.3575761+b*0.1804375
    Y=r*0.2126729+g*0.7151522+b*0.0721750
    Z=r*0.0193339+g*0.1191920+b*0.9503041
    Xn,Yn,Zn=0.95047,1.0,1.08883
    def f(t): return t**(1/3.) if t>0.008856 else (7.787*t+16/116.)
    fx,fy,fz=f(X/Xn),f(Y/Yn),f(Z/Zn)
    return (116*fy-16, 500*(fx-fy), 200*(fy-fz))
def de2000(l1,l2):
    L1,a1,b1=l1; L2,a2,b2=l2
    C1=math.hypot(a1,b1); C2=math.hypot(a2,b2); Cb=(C1+C2)/2
    G=0.5*(1-math.sqrt(Cb**7/(Cb**7+25.0**7))) if Cb>0 else 0.5
    a1p=(1+G)*a1; a2p=(1+G)*a2
    C1p=math.hypot(a1p,b1); C2p=math.hypot(a2p,b2)
    h1p=math.degrees(math.atan2(b1,a1p))%360 if (a1p or b1) else 0
    h2p=math.degrees(math.atan2(b2,a2p))%360 if (a2p or b2) else 0
    dLp=L2-L1; dCp=C2p-C1p
    if C1p*C2p==0: dhp=0
    else:
        d=h2p-h1p
        dhp=d if abs(d)<=180 else (d-360 if d>180 else d+360)
    dHp=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dhp)/2)
    Lbp=(L1+L2)/2; Cbp=(C1p+C2p)/2
    if C1p*C2p==0: hbp=h1p+h2p
    else:
        s=h1p+h2p
        hbp=(s/2) if abs(h1p-h2p)<=180 else ((s+360)/2 if s<360 else (s-360)/2)
    T=1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))+ \
      0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63))
    dth=30*math.exp(-((hbp-275)/25.)**2)
    Rc=2*math.sqrt(Cbp**7/(Cbp**7+25.0**7)) if Cbp>0 else 0
    Sl=1+(0.015*(Lbp-50)**2)/math.sqrt(20+(Lbp-50)**2)
    Sc=1+0.045*Cbp; Sh=1+0.015*Cbp*T
    Rt=-math.sin(math.radians(2*dth))*Rc
    return math.sqrt((dLp/Sl)**2+(dCp/Sc)**2+(dHp/Sh)**2+Rt*(dCp/Sc)*(dHp/Sh))

def labs(p): return [rgb2lab(c) for c in p]
def interne(p):
    L=labs(p)
    return min(de2000(L[i],L[j]) for i,j in itertools.combinations(range(4),2))
def dist(p,q):
    A,B=labs(p),labs(q)
    d1=sum(min(de2000(a,b) for b in B) for a in A)/4.0
    d2=sum(min(de2000(b,a) for a in A) for b in B)/4.0
    return (d1+d2)/2.0
