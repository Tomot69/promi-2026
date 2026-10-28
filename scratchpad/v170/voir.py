import re, json, sys, os
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
src=open('variantes/trace-chemins-promilate.js',encoding='utf-8').read()
js=src[src.index('var D=')+6: src.rindex('};')+1]
# js object -> json: keys unquoted
j=re.sub(r'([{,])(\w+):', r'\1"\2":', js)
D=json.loads(j)
F=TTFont('Polices Promi/PromiLate-Regular.otf'); cm=F.getBestCmap(); gs=F.getGlyphSet()
from fontTools.pens.basePen import BasePen
class P(BasePen):
    def __init__(s,gs): super().__init__(gs); s.c=[]; s.cur=[]
    def _moveTo(s,p): s.cur=[p]
    def _lineTo(s,p): s.cur.append(p)
    def _curveToOne(s,a,b,c):
        p0=s.cur[-1]
        for t in [i/12 for i in range(1,13)]:
            u=1-t; s.cur.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0], u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
    def _qCurveToOne(s,a,b):
        p0=s.cur[-1]
        for t in [i/10 for i in range(1,11)]:
            u=1-t; s.cur.append((u*u*p0[0]+2*u*t*a[0]+t*t*b[0], u*u*p0[1]+2*u*t*a[1]+t*t*b[1]))
    def _closePath(s): s.c.append(s.cur); s.cur=[]
    _endPath=_closePath
cars=sys.argv[1]; k=float(os.environ.get("K","0.3")); tiles=[]
for ch in cars:
    g=D['g'].get(ch); 
    pen=P(gs); gs[cm[ord(ch)]].draw(pen)
    W=int((F["hmtx"][cm[ord(ch)]][0]+80)*k); H=int(1000*k); im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    T=lambda x,y:(x*k+20, H-(y+200)*k)
    for c in pen.c: d.polygon([T(*p) for p in c], fill=(200,190,220))
    if g:
        cols=[(220,40,40),(40,140,40),(40,40,220),(200,120,0),(0,150,150),(150,0,150),(100,100,0)]
        for i,e in enumerate(g['e']):
            pts=[T(e[1+2*m],e[2+2*m]) for m in range((len(e)-1)//2)]
            d.line(pts, fill=cols[i%7], width=3); d.text(pts[0],str(i+1),fill=cols[i%7])
            d.ellipse([pts[0][0]-3,pts[0][1]-3,pts[0][0]+3,pts[0][1]+3],fill=cols[i%7])
        d.text((4,4), ch+' '+json.dumps(g.get('h',g.get('b')))[:60], fill=(0,0,0))
    tiles.append(im)
out=Image.new('RGB',(sum(t.width for t in tiles),tiles[0].height),'white'); x=0
for t in tiles: out.paste(t,(x,0)); x+=t.width
out.save(sys.argv[2]); print(out.size)
