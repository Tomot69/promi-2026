import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
PROF = open('scratchpad/v143/profil.py', encoding='utf-8').read().split('PROF = r"""')[1].split('"""')[0]
VU = """()=>{ window.__V={t0:0,vu:null,img:0,ecran:null}; document.addEventListener('touchstart', e=>{ const V=window.__V; V.t0=performance.now(); V.vu=null; V.img=0; V.ecran=null; let p0=0; try{ p0=_aura.etat().peints; }catch(e){}
    (function f(){ const t=performance.now()-V.t0; V.img++; let p=0; try{ p=_aura.etat().peints; }catch(e){} const s=document.getElementById('auraScreen');
      if(V.ecran==null && s.classList.contains('show') && parseFloat(getComputedStyle(s).opacity)>0.5) V.ecran=[+t.toFixed(1), V.img];
      if(p>p0 && V.vu==null){ V.vu=[+t.toFixed(1), V.img]; } if(t<5000 && V.vu==null) requestAnimationFrame(f); })(); }, true); }"""
def ferme(pg):
    r = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#auraScreen [data-close], #auraScreen .closeb')].find(x=>x.getBoundingClientRect().width>4); if(!e) return null; const q=e.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }")
    if r: pg.touchscreen.tap(r[0], r[1])
    pg.wait_for_timeout(1600); return pg.evaluate("()=>document.getElementById('auraScreen').classList.contains('show')")
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); ctx.add_init_script(PROF); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ promises.slice(0,6).forEach(p=>{ p.status='tenu'; p.keptAt=Date.now(); }); try{ syncAll(); }catch(e){} }"); pg.wait_for_timeout(1500)
    pg.evaluate(VU)
    for k in range(1, 6):
        pg.evaluate("()=>window.__Pon(true)")
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(3600)
        r = pg.evaluate("()=>({V:window.__V, P:window.__P.slice()})"); V = r['V']; t0 = V['t0']
        L = [(round(e[0] - t0), e[1], e[2]) for e in r['P'] if -20 <= e[0] - t0 <= (V['vu'][0] if V['vu'] else 4000) + 30]
        print('\nOUVERTURE %d — écran visible à %s · première image de Pelote à %s ms (image n° %s) · travail compté avant elle %.0f ms' % (k, V['ecran'], V['vu'] and V['vu'][0], V['vu'] and V['vu'][1], sum(e[1] for e in L)), flush=True)
        for t, d, n in sorted(L, key=lambda e: -e[1])[:9]: print('   %5d ms  %6.1f ms  %s' % (t, d, re.sub(r'\s+', ' ', n)[:150]))
        encore = ferme(pg)
        if encore: print('   ⚠ l\'Aura ne s\'est pas fermée')
    b.close()
