# coût par image de la Pelote à chaque densité — Chromium sur le VRAI GPU, @3x, palier haut, rotation libre, par ?mesure=1 (peinture p50/p95)
import json, statistics
from playwright.sync_api import sync_playwright
R = {}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for dn in (1, 2, 3):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','0')}catch(e){}" + "(function(){ var v; Object.defineProperty(window,'_peloteReglage',{configurable:true, get:function(){return v}, set:function(o){ try{ o.densite=%d; o.facteur=%s; o.epaisseur=%s; o.doux=%s; }catch(e){} v=o; }}); })();" % (dn, {1:1,2:1.5,3:2}[dn], {1:1,2:0.8,3:0.7}[dn], 'false' if dn==1 else 'true'))
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?mesure=1'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click();}")
        for _ in range(60):
            pg.wait_for_timeout(1000)
            m = pg.evaluate("()=>window._peloteMesure||null")
            if m: break
        q = lambda L, c: sorted(L)[min(len(L) - 1, int(c * len(L)))]
        A = m['A']
        R[str(dn)] = {'p50': round(q(A['ms'], .5), 1), 'p95': round(q(A['ms'], .95), 1), 'image_p50': round(q(A['dt'], .5), 1), 'n': len(A['ms'])}
        e = pg.evaluate("()=>{const e=_aura.etat(); return [e.palier, e.vise, (window._peloteMesure||{}).texte||'']}")
        R[str(dn)]['palier'] = e[0]; R[str(dn)]['vise'] = e[1]; R[str(dn)]['releve'] = e[2]
        R[str(dn)]['txt'] = 'peinture %s ms (p50) · %s (p95), Chromium GPU @3x' % (str(R[str(dn)]['p50']).replace('.', ','), str(R[str(dn)]['p95']).replace('.', ','))
        print(dn, R[str(dn)], flush=True); ctx.close()
    b.close()
json.dump(R, open('scratchpad/v123/cout_densite.json', 'w'), ensure_ascii=False, indent=1)
