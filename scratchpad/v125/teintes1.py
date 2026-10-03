# §3 — les teintes de corps tirées sur 20 ouvertures, par palette, et CE QUI CHANGE À L'ÉCRAN d'une ouverture à l'autre
import sys, json, importlib.util, os
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
src = open('redteam_corps.py', encoding='utf-8').read()
import math
ns = {'math': math}
exec(src[src.index('def '):src.index('LIT = r')].replace('sys.exit','#'), ns)   # dE00, kaki…
dE00 = ns['dE00']
PAL = ['signal']
LIT = r"""()=>{ const cv=document.getElementById('auBoule'); _aura.fige(true); _aura.vue(3.1,0.32); _aura.pelote(); const W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data;
  let s=[0,0,0], n=0; for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const i=(y*W+x)*4; if(d[i+3]<250) continue; if(Math.hypot(x-W/2,y-W/2)>W*0.36) continue; n++; s[0]+=d[i]; s[1]+=d[i+1]; s[2]+=d[i+2]; }
  const c=_aura.corps?_aura.corps():null; const so=_aura.sol?_aura.sol():null;
  return {moy:s.map(v=>v/n), corps:c&&(c.rgb||c.corps||c), poil:c&&c.poil, idx:c&&c.idx, sol:so}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark',):
        for pal in PAL:
            L=[]
            for i in range(20):
                pg.evaluate("([t,p])=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); setTheme(t); try{Toile.setPalette(p)}catch(e){} }", [th, pal]); pg.wait_for_timeout(300)
                pg.evaluate("()=>{ document.querySelectorAll('.screen.show').forEach(s=>{ if(s.id!=='auraScreen'&&s.id!=='studioScreen') s.classList.remove('show'); }); document.getElementById('souffleBtn').click(); }")
                pg.wait_for_timeout(1500)
                L.append(pg.evaluate(LIT))
            for m in L: print('   corps', m['corps'], 'poil', m['poil'], 'idx', m['idx'], 'sol', json.dumps(m['sol']), 'boule', [round(v) for v in m['moy']])
            corps=[tuple(round(v) for v in (m['corps'] if isinstance(m['corps'],list) else m['corps'].get('rgb',[0,0,0]))) for m in L]
            dist=sorted(set(corps), key=corps.count, reverse=True)
            suc=[dE00(L[i]['moy'],L[i+1]['moy']) for i in range(19)]
            cc=[dE00(corps[i],corps[i+1]) for i in range(19)]
            print('%-5s %-13s corps distincts %d : %s' % (th, pal, len(dist), ' '.join('#%02X%02X%02X×%d' % (c+(corps.count(c),)) for c in dist)))
            print('      ΔE00 entre deux ouvertures — du CORPS tiré : médiane %.1f max %.1f · de la BOULE rendue (moyenne du disque) : médiane %.2f max %.2f · poil %s' % (sorted(cc)[9], max(cc), sorted(suc)[9], max(suc), L[0].get('poil')))
    b.close()
