"""v170d contre v170b (module servi à côté) : chaque image du tracé, lue À L'ÉCRAN (capture), Gilbert, Atkinson, PromiLate, deux échelles."""
import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import banc_tom as B
PREP="""async a=>{ const [pol,gr,txt,fz]=a; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
 const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:30.37px;top:60.21px;width:330px;font:'+gr+' '+fz+'px/1.3 '+pol+';color:#291547;z-index:9999;background:#F7F0DE'; el.innerHTML=txt; document.body.appendChild(el);
 await document.fonts.load(gr+' '+fz+'px '+pol); TraceLettres._cache={}; window.__C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await window.__C.pret;
 const r=el.getBoundingClientRect(); return [r.left-4,r.top-4,r.width+8,r.height+8]; }"""
CAS=[('Gilbert','700','Toi, c’est … ?',35),('Atkinson','500','Camille, donc. Quid d’un Promi à toi-même ?',25),('Atkinson','700','Choisis d’abord le monde qui te ressemble, au',29),
     ('PromiLate','400','PRIMO, DEUXIO, TERTIO',25),('PromiLate','400','LA SUITE T’APPARTIENT.',32),('PromiLate','400','STUDIO MONDE COMMENCE',29),('PromiLate','400','TRACE POUR PLANTER',19)]
def run(vw, vh, mod):
    out = {}
    with sync_playwright() as p:
        b=p.webkit.launch(); ctx=B.contexte(b, vw=vw, vh=vh); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
        if mod: pg.add_script_tag(url='http://127.0.0.1:8752/'+mod); pg.wait_for_timeout(300)
        for c in CAS:
            r = pg.evaluate(PREP, list(c)); ims=[]
            for i in range(1, 25):
                pg.evaluate("p=>{ window.__C.va(p); }", i/24); pg.wait_for_timeout(20)
                ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}))).convert('RGBA'))
            pg.evaluate("()=>{ window.__C.stop(); document.getElementById('gEl').remove(); }")
            out[c[2]] = ims
        b.close()
    return out
ok=0; n=0
for vw, vh in ((390,651),(330,714)):
    A = run(vw, vh, 'variantes/zz-trace-lettres-v170b.js'); N = run(vw, vh, '')
    for k in A:
        nd = sum(1 for x, y in zip(A[k], N[k]) if ImageChops.difference(x, y).getbbox()); n += 1; ok += (nd == 0)
        print(vw, k[:26], 'IDENTIQUE' if nd == 0 else 'DIFFÉRENT (%d images sur 24)' % nd)
print('%d/%d' % (ok, n))
