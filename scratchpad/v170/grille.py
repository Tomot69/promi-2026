import sys, os; sys.path.insert(0,'scratchpad/v146/trace')
import squelette as S
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw
F=TTFont('Polices Promi/PromiLate-Regular.otf'); cm=F.getBestCmap()
cars=sys.argv[1]; k=0.32; tiles=[]
for ch in cars:
    cts=S.contours(F, cm[ord(ch)]); adv=F['hmtx'][cm[ord(ch)]][0]
    W=int((adv+100)*k); H=int(900*k); im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    T=lambda x,y:((x+50)*k, H-(y+100)*k)
    for gx in range(0,adv+1,100):
        d.line([T(gx,-100),T(gx,800)],fill=(225,225,225)); d.text(T(gx+3,-95),str(gx//100),fill=(150,150,150))
    for gy in range(-100,801,100):
        d.line([T(-50,gy),T(adv+50,gy)],fill=(225,225,225)); d.text(T(-48,gy+20),str(gy//100),fill=(150,150,150))
    img,x0,y1=S.image(cts)
    m=Image.new('L',(W,H),0); dm=ImageDraw.Draw(m)
    # fill via even-odd per contour stacking (approx: draw outlines)
    for c in cts: d.line([T(*p) for p in c]+[T(*c[0])], fill=(60,40,110), width=2)
    d.text((3,3),ch,fill=(200,0,0))
    tiles.append(im)
out=Image.new('RGB',(sum(t.width for t in tiles),tiles[0].height),'white'); x=0
for t in tiles: out.paste(t,(x,0)); x+=t.width
out.save(sys.argv[2]); print(out.size)
