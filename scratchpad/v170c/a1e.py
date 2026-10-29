"""v170d : une lettre finie dévoilée par sa boîte donne les MÊMES pixels que par son masque — captures image par image (mode manuel), PromiLate, deux échelles."""
import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import banc_tom as B
PREP="""async a=>{ const [pol,gr,txt,fz,boites]=a; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
 const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:30.37px;top:60.21px;width:330px;font:'+gr+' '+fz+'px/1.3 '+pol+';color:#291547;z-index:9999;background:#F7F0DE'; el.innerHTML=txt; document.body.appendChild(el);
 await document.fonts.load(gr+' '+fz+'px '+pol); TraceLettres.boites=boites; TraceLettres.rangees=boites; window.__C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await window.__C.pret;
 const r=el.getBoundingClientRect(); return [r.left-4,r.top-4,r.width+8,r.height+8]; }"""
CAS=[('PromiLate','400','PRIMO, DEUXIO, TERTIO',25),('PromiLate','400','LA SUITE T’APPARTIENT.',32),('PromiLate','400','STUDIO MONDE COMMENCE',29),('PromiLate','400','TRACE POUR PLANTER',19),('Atkinson','700','Promi, Chiche ou <i style="font-family:PromiLate;font-weight:400;font-style:normal">CERCLE</i> tout',29)]
def run(vw, vh, boites):
    out = {}
    with sync_playwright() as p:
        b=p.webkit.launch(); ctx=B.contexte(b, vw=vw, vh=vh); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
        for c in CAS:
            r = pg.evaluate(PREP, list(c)+[boites]); ims=[]; L=[]
            for i in range(1, 30):
                pg.evaluate("p=>{ window.__C.va(p); }", i/30); pg.wait_for_timeout(30)
                L.append(len(pg.evaluate("()=>document.getElementById('gEl').style.getPropertyValue('clip-path')")))
                ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}))).convert('RGBA'))
            pg.evaluate("()=>{ window.__C.stop(); document.getElementById('gEl').remove(); }")
            out[c[2]] = (ims, max(L))
        b.close()
    return out
ok=0; n=0
for vw, vh in ((390,651),(330,714)):
    A = run(vw, vh, False); Bb = run(vw, vh, True)
    for k in A:
        diffs = [ImageChops.difference(x, y).getbbox() for x, y in zip(A[k][0], Bb[k][0])]
        nd = sum(1 for d in diffs if d); n += 1; ok += (nd == 0)
        print(vw, k[:24], 'IDENTIQUE' if nd == 0 else 'DIFFÉRENT (%d images)' % nd, '· découpe la plus longue %d → %d caractères' % (A[k][1], Bb[k][1]))
print('%d/%d' % (ok, n))
