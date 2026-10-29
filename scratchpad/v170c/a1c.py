"""A1 v170c : chaque image du tracé (canevas ET découpe du texte réel) identique à v170b, Gilbert, Atkinson et PromiLate (mode manuel : le calcul est le même)."""
import sys, hashlib; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
JS="""async a=>{ const [pol,gr,txt,fz]=a; const out=[]; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
 const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:30px;top:60px;width:330px;font:'+gr+' '+fz+'px/1.3 '+pol+';color:#291547;z-index:60'; el.innerHTML=txt; document.body.appendChild(el);
 await document.fonts.load(gr+' '+fz+'px '+pol); TraceLettres._cache={}; const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret;
 for(let i=1;i<24;i++){ C.va(i/24); out.push((C.canevas?C.canevas.toDataURL():'')+'|'+(el.style.getPropertyValue('clip-path')||'')); } C.stop(); el.remove(); return out; }"""
CAS=[('Gilbert','700','Toi, c’est … ?',35),('Atkinson','500','Camille, donc. Quid d’un Promi à toi-même ? <i style="font-weight:700;color:#82AEF8">Chiche</i> é',25),('Atkinson','700','Choisis d’abord le monde qui te ressemble, au',29),('Gilbert','700','TRACE POUR TENIR',19),
     ('PromiLate','400','PRIMO, DEUXIO, TERTIO',25),('PromiLate','400','LA SUITE T’APPARTIENT.',32),('PromiLate','400','STUDIO MONDE',29),('PromiLate','400','TRACE POUR PLANTER',19)]
def run(mod, echelle):
    with sync_playwright() as p:
        b=p.webkit.launch(); ctx=B.contexte(b, vw=390 if echelle==1 else 330, vh=844 if echelle==1 else 714); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
        if mod: pg.add_script_tag(url='http://127.0.0.1:8752/'+mod); pg.wait_for_timeout(300)
        r=[hashlib.md5(''.join(pg.evaluate(JS,list(c))).encode()).hexdigest() for c in CAS]; b.close(); return r
ok=0
for e in (1, 0.79):
    a=run('variantes/zz-trace-lettres-v170b.js', e); n=run('', e)
    for c,x,y in zip(CAS,a,n): print(e, c[0],c[2][:22], 'IDENTIQUE' if x==y else 'DIFFÉRENT', x[:8], y[:8]); ok += x==y
print('%d/%d' % (ok, 2*len(CAS)))
