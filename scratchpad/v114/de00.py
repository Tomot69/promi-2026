import math
def _lab(c):
    r,g,b=[(x/255/12.92 if x/255<=0.04045 else ((x/255+0.055)/1.055)**2.4) for x in c]
    X=(r*.4124564+g*.3575761+b*.1804375)/0.95047; Y=r*.2126729+g*.7151522+b*.0721750; Z=(r*.0193339+g*.1191920+b*.9503041)/1.08883
    f=lambda t: t**(1/3) if t>216/24389 else (841/108)*t+4/29
    return (116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z)))
def de00(c1,c2):
    L1,a1,b1=_lab(c1); L2,a2,b2=_lab(c2)
    C1=math.hypot(a1,b1); C2=math.hypot(a2,b2); Cb=(C1+C2)/2; G=0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7)))
    a1p=(1+G)*a1; a2p=(1+G)*a2; C1p=math.hypot(a1p,b1); C2p=math.hypot(a2p,b2)
    h1p=math.degrees(math.atan2(b1,a1p))%360; h2p=math.degrees(math.atan2(b2,a2p))%360
    dLp=L2-L1; dCp=C2p-C1p
    dh=h2p-h1p
    if C1p*C2p==0: dh=0
    elif dh>180: dh-=360
    elif dh<-180: dh+=360
    dHp=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dh/2))
    Lbp=(L1+L2)/2; Cbp=(C1p+C2p)/2
    if C1p*C2p==0: hbp=h1p+h2p
    elif abs(h1p-h2p)<=180: hbp=(h1p+h2p)/2
    elif h1p+h2p<360: hbp=(h1p+h2p+360)/2
    else: hbp=(h1p+h2p-360)/2
    T=1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))+0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63))
    dth=30*math.exp(-((hbp-275)/25)**2); RC=2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    SL=1+0.015*(Lbp-50)**2/math.sqrt(20+(Lbp-50)**2); SC=1+0.045*Cbp; SH=1+0.015*Cbp*T; RT=-math.sin(math.radians(2*dth))*RC
    return math.sqrt((dLp/SL)**2+(dCp/SC)**2+(dHp/SH)**2+RT*(dCp/SC)*(dHp/SH))
