import sys, json, time; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
N = int(sys.argv[2]) if len(sys.argv)>2 else 5
MONDES = sys.argv[3].split(',') if len(sys.argv)>3 else ['encre','touffe','brouillamini','halin','esquille','mosaique','braille','pixel','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo','gravure','sillons']
PAGES = sys.argv[4].split(',') if len(sys.argv)>4 else ['studio','aura','index','fil','reglages','fiche','plus']
GEO = "()=>{var c=Toile_cellules();var pr=Toile_probe();var k=0;return {v:[+c.view.s.toFixed(3),+c.view.ox.toFixed(1),+c.view.oy.toFixed(1)],W:c.W,H:c.H,n:c.c.length,g:c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid,+s.x.toFixed(1),+s.y.toFixed(1)]),pr:pr,th:Toile.getTheme()}}"
FERME = """()=>{ try{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); const s=h&&h.closest('.screen, #feedView, #indexSheet, .sheet, .poster');
    const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{ closeAll(); }catch(e){} }"""
def ouvrir(pg, page):
    if page=='studio':
        tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(2600); tap_sel(pg,'#studioScreen .closeb'); pg.wait_for_timeout(1200); return
    if page=='aura': tap_sel(pg,'#souffleBtn')
    elif page=='index': tap_sel(pg,'#indexBtn')
    elif page=='fil': tap_sel(pg,'#filBtn')
    elif page=='plus': tap_sel(pg,'#createBtn')
    elif page=='reglages': pg.evaluate("()=>{var b=document.querySelector('#accPlat [aria-label*=glage], .acc-plat .acc-reg, #setBtn, #settingsBtn'); if(b) b.click(); else if(window.openSettings) openSettings();}")
    elif page=='fiche': pg.evaluate("()=>{var p=promises.find(p=>!p.draft); if(p) openDetail(p.id);}")
    pg.wait_for_timeout(1800); pg.evaluate(FERME); pg.wait_for_timeout(600); pg.evaluate(FERME); pg.wait_for_timeout(1500)
def diff(a,b):
    if a['v']!=b['v']: return 'vue %s→%s'%(a['v'],b['v'])
    A={x[0]:x for x in a['g']}; B={x[0]:x for x in b['g']}
    if set(A)!=set(B): return 'graines colorées %d→%d'%(len(A),len(B))
    d=[(k,A[k][1:],B[k][1:]) for k in A if abs(A[k][1]-B[k][1])>0.5 or abs(A[k][2]-B[k][2])>0.5]
    if d: return '%d graines déplacées %s'%(len(d),d[:2])
    if a['n']!=b['n']: return 'cellules %d→%d'%(a['n'],b['n'])
    return None
res=[]
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False,):
        for m in MONDES:
            ctx = contexte(b, sombre=sombre, stockage={'promi_monde':m}); toile_pleine(ctx, N); pg = ouvre(ctx, F)
            pg.evaluate("m=>{if(Toile.getTheme()!==m)Toile.setTheme(m)}", m); pg.wait_for_timeout(2500)
            a0 = pg.evaluate(GEO)
            for page in PAGES:
                a = pg.evaluate(GEO); ouvrir(pg, page); bb = pg.evaluate(GEO)
                d = diff(a,bb)
                if d: print('ROUGE', m, N, page, d, flush=True); res.append((m,page,d))
            print(m, 'theme', a0['th'], 'fin', bb['th'], 'n', len(a0['g']), 'erreurs', pg.__dict__['erreurs'][:2], flush=True)
            ctx.close()
    b.close()
print('rouges', len(res))
