import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGB'); y=int((float(sys.argv[2])-640)*3); out=[]; prev=None
for x in range(140*3,250*3):
    c=im.getpixel((x,y)); k='#%02X%02X%02X'%tuple(v//24*24 for v in c)
    if k!=prev: out.append((round(x/3,1),'#%02X%02X%02X'%c)); prev=k
print(out)
