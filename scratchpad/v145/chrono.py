"""la chronologie d'une plantation sur Toile remplie : chaque image longue, et ce qui a tourné dedans. usage : chrono.py monde n [port] [retirer]"""
import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
m, n = sys.argv[1], int(sys.argv[2]); port = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3].isdigit() else '8752'
PROF = re.search(r'PROF = r"""(.*?)"""', io.open('redteam_evol.py', encoding='utf-8').read(), re.S).group(1).replace('if(d>=1.5)', 'if(d>=0.3)')
st = json.load(io.open('scratchpad/v145/etats/etat-%d.json' % n, encoding='utf-8')); st.pop('promi_theme', None)
E = "try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre='sombre' in sys.argv); ctx.add_init_script(E); ctx.add_init_script(PROF)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:%s/app.html' % port); pg.wait_for_timeout(6500)
    pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(9000)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.getElementById('fTitle').value='tenir bon';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
    pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(4000)
    if 'retirer' in sys.argv:
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); B.tap_sel(pg, '.v16-oui'); pg.wait_for_timeout(4000)
    r = pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice()})"); t0 = r['t0']; F = [f - t0 for f in r['F']]; P = [(e[0] - t0, e[1], e[2]) for e in r['P']]
    eng = [e for e in P if 'image | frame' in e[2] and 0 <= e[0] <= 3500]
    print('boucle du moteur : %d images de %d à %d ms ; travail p50 %.1f · max %.1f ms' % (len(eng), eng[0][0] if eng else 0, eng[-1][0] if eng else 0, sorted(x[1] for x in eng)[len(eng) // 2] if eng else 0, max([x[1] for x in eng] or [0])))
    for i in range(len(F) - 1):
        if 0 <= F[i] <= 3500 and F[i + 1] - F[i] > 20:
            dans = sorted([(round(e[1], 1), e[2][:58]) for e in P if F[i] - 1 <= e[0] < F[i + 1]], reverse=True)[:4]
            print('  image de %3.0f ms à %4.0f ms · travail compté %5.1f ms : %s' % (F[i + 1] - F[i], F[i], sum(e[1] for e in P if F[i] - 1 <= e[0] < F[i + 1]), dans))
    b.close()
