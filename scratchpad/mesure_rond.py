import sys, math
from PIL import Image
# ⚑ LA CIRCULARITE DE LA SILHOUETTE : on tire 360 rayons depuis le centre et on
#   note ou la matiere s'arrete. Un cercle parfait a un ecart-type nul.
def stat(f):
    im=Image.open(f).convert('L'); W,H=im.size; px=im.load()
    cx,cy=W/2.0,H/2.0
    R=[]
    for a in range(360):
        t=a*math.pi/180.0; ca,sa=math.cos(t),math.sin(t)
        r=min(W,H)*0.5-2; last=0
        while r>4:
            x=int(cx+ca*r); y=int(cy+sa*r)
            if 0<=x<W and 0<=y<H and px[x,y]>34: last=r; break
            r-=0.5
        R.append(last)
    m=sum(R)/len(R)
    sd=math.sqrt(sum((v-m)**2 for v in R)/len(R))
    return m,sd,100*sd/max(1,m),min(R),max(R)
for f in sys.argv[1:]:
    m,sd,p,mn,mx=stat(f)
    print("%-16s rayon moyen %6.1f   ecart-type %5.2f (%4.2f %%)   min %5.1f  max %5.1f"
          %(f.split('/')[-1],m,sd,p,mn,mx))
