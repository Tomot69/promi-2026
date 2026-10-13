import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
PROF = re.search(r'PROF = r"""(.*?)"""', io.open('redteam_evol.py', encoding='utf-8').read(), re.S).group(1)
st = json.load(io.open('scratchpad/v145/etats/etat-25.json', encoding='utf-8')); st.pop('promi_theme', None)
E = "try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st)
with sync_playwright() as p:
    b = p.webkit.launch()
    for nom, init in (('page vide (about:blank + rAF)', None), ('app, 25 paroles, Pochade', E)):
        ctx = B.contexte(b)
        if init: ctx.add_init_script(init); ctx.add_init_script(PROF)
        pg = ctx.new_page()
        if init: pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(16000)
        else:
            pg.goto('about:blank'); pg.evaluate("()=>{ window.__F=[]; window.__P=[]; window.__Pon=function(){}; (function b(){ window.__F.push(performance.now()); requestAnimationFrame(b); })(); }"); pg.wait_for_timeout(1500)
        for passe in range(3):
            pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); pg.wait_for_timeout(3600)
            r = pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice()})"); t0 = r['t0']
            I = [r['F'][i + 1] - r['F'][i] for i in range(len(r['F']) - 1) if t0 <= r['F'][i] <= t0 + 3500]
            P = sorted([(round(e[1], 1), round(e[0] - t0), e[2][:70]) for e in r['P'] if 0 <= e[0] - t0 <= 3500 and e[1] > 8], reverse=True)[:4]
            print('%-32s passe %d : %d images · >20 ms : %d · >33 : %d · pire %.0f ms · rappels > 8 ms : %s' % (nom, passe, len(I), sum(1 for x in I if x > 20), sum(1 for x in I if x > 33.4), max(I or [0]), P), flush=True)
        ctx.close()
    b.close()
