# C-145 §4 : sur le vrai parcours (onboarding fini au doigt), les deux phrases du guide — leur centre, leurs lignes — contre les dalles colorées de la Toile
# (pixels du canevas de la Toile lus AVANT le flou : chroma OKLCH > 0,06), les icônes (plateau, barre) et la zone nette des flaques. Chromium, 390 × 844.
import io, sys, math; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/' + next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
TH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--theme=')), 'light')
CHROMA = r"""()=>{ const tc=document.getElementById('toileCv'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=tc.getBoundingClientRect(); const s=tc.width/r.width;
  const g=tc.getContext('2d'); const d=g.getImageData(0,0,tc.width,tc.height).data, W=tc.width, H=tc.height; const lin=x=>{x/=255; return x<=0.04045?x/12.92:Math.pow((x+0.055)/1.055,2.4);};
  const C=(R,G,B)=>{ const l=[lin(R),lin(G),lin(B)]; let L=0.4122214708*l[0]+0.5363325363*l[1]+0.0514459929*l[2], M=0.2119034982*l[0]+0.6806995451*l[1]+0.1073969566*l[2], S=0.0883024619*l[0]+0.2817188376*l[1]+0.6299787005*l[2]; L=Math.cbrt(L); M=Math.cbrt(M); S=Math.cbrt(S);
    const a=1.9779984951*L-2.4285922050*M+0.4505937099*S, b=0.0259040371*L+0.7827717662*M-0.8086757660*S; return Math.hypot(a,b); };
  const pts=[]; for(let y=0;y<844;y+=3) for(let x=0;x<390;x+=3){ const X=Math.round(((D.left+x*k)-r.left)*s), Y=Math.round(((D.top+y*k)-r.top)*s); if(X<0||Y<0||X>=W||Y>=H) continue; const i=(Y*W+X)*4; if(C(d[i],d[i+1],d[i+2])>0.06) pts.push([x,y]); }
  return pts; }"""
PH = r"""()=>{ const p=document.getElementById('guidePhrase'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!p) return null; const rg=document.createRange(); rg.selectNodeContents(p);
  const L=[...rg.getClientRects()].filter(q=>q.width>1).map(q=>[(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k]);
  const b=p.getBoundingClientRect(); const ico=[...document.querySelectorAll('.acc-plat svg, .acc-plat button, .acc-plat .acc-mm, #device .acc-barre svg, #device .acc-barre .l, #createBtn')].map(e=>{const q=e.getBoundingClientRect(); return [(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k,(e.id||e.className.baseVal||e.className||e.tagName)+''];}).filter(q=>q[2]-q[0]>2);
  const st=document.querySelector('#guidePhrase .gd-studio'), cl=document.querySelector('#guidePhrase .gd-cle:not(.gd-studio)');
  return {texte:p.textContent, centre:((b.top+b.bottom)/2-D.top)/k, haut:(b.top-D.top)/k, bas:(b.bottom-D.top)/k, lignes:L, ico:ico, trou:(window._guide&&_guide.etat().trou)||null,
    fsStudio:st?parseFloat(getComputedStyle(st).fontSize):null, fsCle:cl?parseFloat(getComputedStyle(cl).fontSize):null, cols:st?[...st.querySelectorAll('.gd-l')].map(e=>getComputedStyle(e).color):null}; }"""
def croise(a, b, m=0): return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, color_scheme='dark' if TH == 'dark' else 'light')
    if TH == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(600); trace(pg, cdp); pg.wait_for_timeout(5200)
    for _ in range(4):
        toucher(cdp, pg, 195, 260); pg.wait_for_timeout(3200)
    pg.evaluate("()=>{ const t=document.querySelector('.onbv-compte .tard'); if(t) t.click(); }")
    dalles = None
    for i in range(80):
        pg.wait_for_timeout(100)
        if dalles is None and pg.evaluate("()=>!document.getElementById('onbV') && !!document.getElementById('toileCv')") and not pg.evaluate("()=>!!document.getElementById('guide')"):
            pg.wait_for_timeout(300); dalles = pg.evaluate(CHROMA)
        if pg.evaluate("()=>{ const g=document.getElementById('guide'); return !!(g && window._guide && _guide.etat().net>=1); }"): break
    if dalles is None: dalles = []
    pg.wait_for_timeout(1500); s = pg.evaluate(PH)
    print('dalles colorées (points lus) :', len(dalles), ' boîte :', (min(x for x, y in dalles), min(y for x, y in dalles), max(x for x, y in dalles), max(y for x, y in dalles)) if dalles else None)
    def bilan(s, nom):
        dd = [q for q in dalles if any(l[0] - 2 <= q[0] <= l[2] + 2 and l[1] - 2 <= q[1] <= l[3] + 2 for l in s['lignes'])]
        ic = [i[4] for i in s['ico'] if any(croise(l, i, 2) for l in s['lignes'])]
        tr = s['trou']; tz = [tr['x'] - tr['w'] / 2, tr['y'] - tr['h'] / 2, tr['x'] + tr['w'] / 2, tr['y'] + tr['h'] / 2] if tr else None
        print('%s : centre %.1f (haut %.1f, bas %.1f) · %s' % (nom, s['centre'], s['haut'], s['bas'], s['texte']))
        print('   lignes', [[round(v, 1) for v in l] for l in s['lignes']])
        print('   points de dalle colorée sous les lignes : %d · icônes croisées : %s · zone nette %s croisée : %s' % (len(dd), ic, [round(v) for v in tz] if tz else None, bool(tz) and any(croise(l, tz, 2) for l in s['lignes'])))
        print('   Studio %s pt (mot-clé %s) · couleurs %s' % (s['fsStudio'], s['fsCle'], s['cols']))
    bilan(s, 'studio'); pg.screenshot(path='scratchpad/v149/guide_studio_%s.png' % TH)
    c = pg.evaluate("()=>{ const e=document.getElementById('guideCible'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(2500)
    cb = pg.evaluate("()=>{ const e=document.querySelector('#studioScreen .closeb'); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2, r.top+r.height/2]:null; }")
    if cb: toucher(cdp, pg, cb[0], cb[1])
    for i in range(80):
        pg.wait_for_timeout(100)
        if pg.evaluate("()=>{ const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && window._guide && _guide.etat().net>=1); }"): break
    pg.wait_for_timeout(1200); s2 = pg.evaluate(PH); bilan(s2, 'plus')
    pg.screenshot(path='scratchpad/v149/guide_plus_%s.png' % TH)
    b.close()
