import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
J = """()=>{ let n=0, s=0, parBloc=[]; for(const sh of document.styleSheets){ let k=0; try{ (function c(rs){ for(const r of rs){ if(r.cssRules && r.type!==1){ c(r.cssRules); } else { k++; } } })(sh.cssRules); }catch(e){} n+=k; s++; parBloc.push([(sh.ownerNode&&sh.ownerNode.id)||'', k]); } return {n:n, s:s, blocs:parBloc}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); R = {}
    for f in sys.argv[1:]:
        pg = b.new_page(); pg.goto('http://127.0.0.1:8752/' + f); pg.wait_for_timeout(2500); R[f] = pg.evaluate(J); print(f, R[f]['n'], 'règles dans', R[f]['s'], 'feuilles'); pg.close()
    a, c = [R[f]['blocs'] for f in sys.argv[1:3]]
    for x, y in zip(a, c):
        if x[1] != y[1]: print('   écart :', x, y)
    b.close()
