"""v170d : un texte repris du cache (restes, cartes) donne EXACTEMENT les mêmes images qu'un texte calculé — la découpe (clip-path) et le canevas, pas à pas."""
import sys, hashlib; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
JS="""async a=>{ const [pol,gr,txt,fz,vide]=a; const out=[]; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
 const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:30.37px;top:60.21px;width:330px;font:'+gr+' '+fz+'px/1.3 '+pol+';color:#291547;z-index:60'; el.innerHTML=txt; document.body.appendChild(el);
 await document.fonts.load(gr+' '+fz+'px '+pol); if(vide){ TraceLettres._cache={}; TraceLettres._cacheR={}; } const h0=TraceLettres.mesures.cacheR;
 const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret;
 for(let i=1;i<24;i++){ C.va(i/24); out.push((C.canevas?C.canevas.toDataURL():'')+'|'+(el.style.getPropertyValue('clip-path')||'')); } C.stop(); el.remove(); return [out.join('#'), TraceLettres.mesures.cacheR-h0]; }"""
CAS=[('PromiLate','400','PRIMO, DEUXIO, TERTIO',25),('PromiLate','400','LA SUITE T’APPARTIENT.',32),('PromiLate','400','STUDIO MONDE',29),('PromiLate','400','TRACE POUR PLANTER',19),('Atkinson','700','Choisis d’abord le monde qui te ressemble, au',29),('Gilbert','700','Toi, c’est … ?',35)]
with sync_playwright() as p:
    ok=0
    for vw,vh in ((390,651),(330,714)):
        b=p.webkit.launch(); ctx=B.contexte(b, vw=vw, vh=vh); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
        for c in CAS:
            a,_=pg.evaluate(JS, list(c)+[True]); bb,hits=pg.evaluate(JS, list(c)+[False])
            same = hashlib.md5(a.encode()).hexdigest()==hashlib.md5(bb.encode()).hexdigest(); ok+=same
            print(vw, c[0], c[2][:22], 'IDENTIQUE' if same else 'DIFFÉRENT', 'lettres reprises du cache des restes :', hits)
        b.close()
    print('%d/%d' % (ok, 2*len(CAS)))
