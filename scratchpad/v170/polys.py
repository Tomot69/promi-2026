import sys, os, re; sys.path.insert(0,'.'); sys.argv=sys.argv[:1]
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
from PIL import ImageDraw
c=os.environ.get('C','L'); fz=float(os.environ.get('FZ','19')); f=float(os.environ.get('F','0.5278'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'pose']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'arme']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,f])
    cp=pg.evaluate("()=>getComputedStyle(document.getElementById('gEl')).clipPath")
    b.close()
d=cp[cp.index('"')+1:cp.rindex('"')]
subs=[s for s in re.split(r'(?=M)', d) if s.strip()]
Z=30; im=Image.new('RGB',(40*Z,50*Z),'white'); dr=ImageDraw.Draw(im)
cols=[(255,0,0),(0,120,255),(0,160,0),(200,0,200),(255,140,0)]
big=[]
for k,s in enumerate(subs):
    nums=[float(v) for v in re.findall(r'-?[\d.]+', s)]
    if 'h' in s:   # carré : M x y h c v c h -c Z
        x,y,cc=nums[0],nums[1],nums[2]; pts=[(x,y),(x+cc,y),(x+cc,y+cc),(x,y+cc)]
    else: pts=list(zip(nums[0::2],nums[1::2]))
    if min(p[0] for p in pts)<-100: continue
    big.append(pts)
    dr.polygon([(px*Z,py*Z) for px,py in pts], outline=cols[k%5])
im.save('scratchpad/v170/polys.png'); print(len(subs))
for pts in big[:40]: print([(round(a,2),round(b_,2)) for a,b_ in pts])
