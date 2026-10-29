import sys, os, re; sys.path.insert(0,'.'); sys.argv=sys.argv[:1]
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
from PIL import ImageDraw
c=os.environ.get('C','S'); fz=float(os.environ.get('FZ','29')); f=float(os.environ.get('F','0.611'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    r=pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'pose']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'arme']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,f])
    cp=pg.evaluate("()=>getComputedStyle(document.getElementById('gEl')).clipPath"); b.close()
d=cp[cp.index('"')+1:cp.rindex('"')]
subs=[s for s in re.split(r'(?=M)', d) if s.strip()]
Z=20; im=Image.new('RGB',(40*Z,50*Z),'white'); dr=ImageDraw.Draw(im); nq=ns=0
for s in subs:
    nums=[float(v) for v in re.findall(r'-?[\d.]+', s)]
    if 'h' in s: x,y,cc=nums[0],nums[1],nums[2]; dr.rectangle([x*Z,y*Z,(x+cc)*Z,(y+cc)*Z], fill=(255,120,0)); ns+=1
    else:
        pts=list(zip(nums[0::2],nums[1::2]))
        if min(q[0] for q in pts)<-100: continue
        dr.polygon([(px*Z,py*Z) for px,py in pts], fill=(80,80,200)); nq+=1
        xs=[q[0] for q in pts]; ys=[q[1] for q in pts]
        if max(xs)-min(xs)>4 and max(ys)-min(ys)>4: print('grand', [(round(a,2),round(b_,2)) for a,b_ in pts])
im.save('scratchpad/v170/qui.png'); print('bandes',nq,'carrés',ns)
