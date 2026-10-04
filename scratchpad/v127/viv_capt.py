# trois captures par monde (avant, pendant, après) autour de la dalle tirée, @3x, + la différence amplifiée
import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageDraw, ImageFont
MONDES=sys.argv[1:]; NOMS={'madrure':'Madrure','chamade':'Chamade','terrazzo':'Éclisse','sillons':'Houle','encre':'Pochade'}
rows=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for m in MONDES:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("window._vivantFixe=600000;try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(m);}", m); pg.wait_for_timeout(8000)
        clip={'x':20,'y':44,'width':390,'height':844}
        A=pg.screenshot(clip=clip); open('scratchpad/v127/viv-%s-0.png'%m,'wb').write(A)
        j=pg.evaluate("()=>{ Toile.vivant.force(); const J=Toile.vivant.journal(); const j=J[J.length-1]; const cv=document.getElementById('toileCv'), R=cv.getBoundingClientRect(), k=R.width/cv.clientWidth; const B=j.pid.map(id=>{const a=Toile.dalleAbs(id); return a?[R.left+a.minx*k,R.top+a.miny*k,a.w*k,a.h*k]:null}); return {d:j.d,B:B}; }")
        best=None; 
        for i in range(5):
            pg.wait_for_timeout(int(j['d']/7)); pg.screenshot(path='scratchpad/v127/viv-%s-m%d.png'%(m,i), clip=clip)
        pg.wait_for_timeout(int(j['d'])+600); pg.screenshot(path='scratchpad/v127/viv-%s-2.png'%m, clip=clip)
        a=Image.open('scratchpad/v127/viv-%s-0.png'%m).convert('RGB'); z=Image.open('scratchpad/v127/viv-%s-2.png'%m).convert('RGB')
        mids=[Image.open('scratchpad/v127/viv-%s-m%d.png'%(m,i)).convert('RGB') for i in range(5)]
        def nd(u,v): return sum(1 for q in ImageChops.difference(u,v).convert('L').getdata() if q>8)
        sc=[nd(a,x) for x in mids]; mid=mids[sc.index(max(sc))]
        bx=[q for q in j['B'] if q][0]; x0=max(0,int((bx[0]-20-14)*3)); y0=max(0,int((bx[1]-44-14)*3)); x1=min(a.width,int((bx[0]-20+bx[2]+14)*3)); y1=min(a.height,int((bx[1]-44+bx[3]+14)*3))
        print(m, 'pendant: %d px changés ; retour: %d px ; boîte %s'%(max(sc), nd(a,z), [round(q) for q in bx]))
        d=ImageChops.difference(a,mid).point(lambda v:min(255,v*6))
        rows.append((m,[u.crop((x0,y0,x1,y1)) for u in (a,mid,z,d)])); ctx.close()
    b.close()
try: ft=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',40)
except: ft=None
M=40; T=70; cw=max(r[1][0].width for r in rows); H=sum(r[1][0].height+T+M for r in rows)+M
P=Image.new('RGB',(cw*4+M*5,H),(240,236,226)); d=ImageDraw.Draw(P); y=M
for m,cr in rows:
    for i,(c,t) in enumerate(zip(cr,('avant','pendant','après','écart avant/pendant ×6'))):
        x=M+i*(cw+M); d.text((x,y),'%s · %s'%(NOMS.get(m,m),t),fill=(32,25,8),font=ft); P.paste(c,(x,y+T))
    y+=cr[0].height+T+M
P.save('planche-v127/vie-au-repos-%s.png'%('-'.join(MONDES)))
