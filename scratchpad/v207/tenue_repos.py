# v208 §1 : la fiche tenue au repos (et pendant l'instant « juste après »), au pixel, contre la version d'avant ; horloge figée par la vue de banc_jonction
import sys, io, os; sys.path.insert(0,'.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
def capture(F, nat, etat):
    with sync_playwright() as p:
        b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)
        ctx.add_init_script("try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){} Math.random=(function(){var s=7;return function(){s=(s*16807)%2147483647;return (s-1)/2147483646;};})();")
        B.toile_pleine(ctx,'cercle'); pg=B.ouvre(ctx,F)
        pg.evaluate("([n,e])=>{ const p=promises.filter(x=>!x.draft&&!x.nuee&&!x.chiche)[1]; if(n==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.status=e; p.comments=[]; delete p.parts; closeAll(); openDetail(p.id); }", [nat, etat])
        pg.wait_for_timeout(3500); d=B.dev(pg)
        info=pg.evaluate("()=>{ const q=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round(r.top),Math.round(r.height)];}; return {titre:q('#dptTitre'), qui:q('#dptQui'), etat:q('#dpEtat, .dpt-etat'), noyaux:q('#dAura'), mot:q('#cm5Ligne'), colle:q('#v192Colle'), barre:q('#dpDetails'), h:document.getElementById('detailPoster').scrollHeight, disp:getComputedStyle(document.getElementById('detailPoster')).display}; }")
        png=pg.screenshot(clip={'x':d[0],'y':d[1],'width':390*d[4],'height':844*d[4]}); b.close()
        return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16), info
for nat in ('promi','chiche'):
    a,ia=capture(sys.argv[1], nat, 'tenu'); c,ic=capture(sys.argv[2], nat, 'tenu')
    diff=np.abs(a-c).max(axis=2); print(nat, 'pixels écartés (>24)', int((diff>24).sum()), '\n  avant', ia, '\n  après', ic)
