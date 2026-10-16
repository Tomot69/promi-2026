"""C-136 — sonde : la Toile vide sort-elle colorée au chargement ? Qui la colore ?
python3 scratchpad/v147/c136_sonde.py N [onb|accueil] [port]"""
import sys, json, time
sys.path.insert(0, '.')
import banc_tom
from playwright.sync_api import sync_playwright
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
MODE = sys.argv[2] if len(sys.argv) > 2 else 'onb'
PORT = sys.argv[3] if len(sys.argv) > 3 else '8752'
HOOK = r"""(function(){ window.__c136=[]; window.__c136t=[];
 function arme(){ var T=window.Toile; if(!T||!T.colored){ return setTimeout(arme,5); }
   if(T.__arme) return; T.__arme=1;
   Object.keys(T).forEach(function(k){ var f=T[k]; if(typeof f!=='function'||k==='colored') return;
     T[k]=function(){ var a=-1,b=-1; try{a=T.colored();}catch(e){} var r=f.apply(this,arguments); try{b=T.colored();}catch(e){}
       if(a===0&&b>0) window.__c136.push({f:k,t:performance.now()|0,b:b,pile:(new Error()).stack.split('\n').slice(1,7).join(' | ')});
       return r; }; });
   var der=-2; (function tic(){ var c=-1; try{c=T.colored();}catch(e){} if(c!==der){ window.__c136t.push([performance.now()|0,c]); der=c; } setTimeout(tic,40); })();
 } arme(); })();"""
res = []
with sync_playwright() as p:
    CHR = len(sys.argv) > 4 and sys.argv[4] == 'chromium'
    b = p.chromium.launch() if CHR else p.webkit.launch()
    for i in range(N):
        if CHR:
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        else:
            ctx = banc_tom.contexte(b, onb=(MODE != 'onb'), guide=True)
        ctx.add_init_script(HOOK)
        pg = ctx.new_page()
        pg.goto('http://127.0.0.1:%s/app.html' % PORT)
        pg.wait_for_timeout(int(sys.argv[5]) if len(sys.argv)>5 else 9000)
        e = pg.evaluate("()=>({n:((typeof promises!=='undefined'&&promises)||[]).filter(p=>!p.draft).length, c:window.Toile.colored(), g:(window.Toile.graines?window.Toile.graines():null), h:window.__c136, t:window.__c136t, th:(window.Toile.mondeCourant?window.Toile.mondeCourant():null)})")
        col = e['c']
        res.append(e)
        print(i, 'paroles', e['n'], 'colorées', col, 'graines', e['g'], 'monde', e['th'], 'tl', e['t'][:8], flush=True)
        for h in e['h']: print('    COLORE PAR', h['f'], h['t'], h['b'], h['pile'][:400], flush=True)
        ctx.close()
    b.close()
k = sum(1 for e in res if e['c'] and e['n'] == 0)
print('Toile vide colorée : %d / %d' % (k, N))
