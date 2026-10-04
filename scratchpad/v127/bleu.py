import sys
from PIL import Image
def bleu(f):
    im=Image.open(f).convert('RGB'); px=im.load(); W,H=im.size; x0=y0=10**9; x1=y1=-1; n=0
    for y in range(0,H,1):
        for x in range(0,W,1):
            r,g,b=px[x,y]
            if b>200 and r<190 and g<215 and b-r>50: 
                n+=1
                if x<x0:x0=x
                if x>x1:x1=x
                if y<y0:y0=y
                if y>y1:y1=y
    return [round(x0/3,1),round(y0/3,1),round((x1-x0+1)/3,1),round((y1-y0+1)/3,1)], round(n/9)
for f in sys.argv[1:]: print(f, *bleu(f))
