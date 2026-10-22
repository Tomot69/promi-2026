#!/usr/bin/env python3
"""redteam_toile_stable.py — ⚑ v159 (Tom, C-177) : LES DALLES DE LA TOILE NE BOUGENT PAS QUAND ON OUVRE UNE PAGE.

« Sous certains mondes (Éclisse par exemple), les dalles colorées s'empilent. C'est intermittent : parfois on ouvre une page, on revient à la Toile, et les
dalles colorées ne sont plus à leur position. Juge : 20 mondes × {5, 25} paroles × toutes les pages ouvertes puis fermées, en clair et en sombre,
géométrie identique au point près. »

Banc comme Tom (WebKit, 390 × 844 ×3, doigt, webdriver masqué, Toile de 5 ou 25 paroles relue de la sauvegarde, membre Ma Parole !). Pour chaque monde :
la géométrie de la Toile À L'ÉCRAN (chaque dalle colorée : sa graine × la vue — zoom et décalage) est relevée sur l'accueil, puis après chaque page
ouverte et refermée au doigt :
  · le Studio, avec un ALLER-RETOUR (trois mondes d'un côté, trois de l'autre : on revient au même monde — le chemin qui croise les deux familles de semis) ;
  · l'Aura, l'Index, le Fil, les Réglages, une fiche, la page + ;
chaque dalle doit revenir à sa place à l'écran à 1 pt près (et la vue à 1 % près), aucune graine ne doit avoir bougé, le nombre de cellules non plus.
⚠ C'est la VUE qui bougeait (C-177) : après un aller-retour au Studio, Éclisse à 5 paroles gardait le cadrage serré de Bobinette (zoom 1,19 → 1,68,
  les dalles décalées de 267 pt). Preuve : `--fichier=zz-v158.html` rougit (le Studio, aux mondes à 5 paroles).
⚠ PEUT ROUGIR PAR INTERMITTENCE (Q573, le moteur ; 80/80 à la passe complète de v159) : à 25 paroles, les mondes « faits de leurs seules paroles » (semis neuf) qu'un aller-retour au Studio
  fait passer par un ancien monde reviennent ressemés, à 15–56 pt (Ramage) — la place gardée et le relâchement du moteur ; v158 aussi.
Options : `--mondes=a,b` · `--q=?…` · `--n=5,25` · `--themes=clair,sombre` · `--fichier=`.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--%s=' % k)), d)
F = arg('fichier', 'app.html')
MONDES = arg('mondes', 'encre,touffe,brouillamini,halin,esquille,mosaique,braille,pixel,ramage,guingois,chantourne,volubilis,madrure,chamade,ritournelle,bobinette,mascaret,terrazzo,gravure,sillons').split(',')
NS = [int(x) for x in arg('n', '5,25').split(',')]
THEMES = arg('themes', 'clair,sombre').split(',')
PAGES = ['studio', 'aura', 'index', 'fil', 'reglages', 'fiche', 'plus']
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
GEO = """()=>{ var c=Toile_cellules(), v=c.view; return {v:[v.s,v.ox,v.oy], n:c.c.length, th:Toile.getTheme(),
  g:c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid==null?('n'+s.kind):s.pid, s.x, s.y, s.x*v.s+v.ox, s.y*v.s+v.oy])}; }"""
DEVANT = "()=>{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); return !h || h.id==='toileCv'; }"
FERME = """()=>{ try{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42);
  const s=h&&h.closest('.screen, #feedView, #indexSheet, .sheet, .poster'); const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{ closeAll(); }catch(e){} }"""
def ferme(pg):
    for _ in range(4):
        pg.evaluate(FERME); pg.wait_for_timeout(600)
        if pg.evaluate(DEVANT): return True
    return False
def page(pg, p):
    if p == 'studio':
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2200)
        for s in (-1, -1, -1, 1, 1, 1):
            a, b = (300, 90) if s > 0 else (90, 300)
            B.glisse(pg, B.droite([a, 420], [b, 420], 10), pas=16); pg.wait_for_timeout(1300)
        B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(1500)
    elif p == 'fiche':
        g = pg.evaluate(GEO); L = [x for x in g['g'] if isinstance(x[0], int) and 190 < x[4] < 690 and 20 < x[3] < 370]
        if L: B.tap(pg, L[0][3], L[0][4])
        else: pg.evaluate("()=>{ var p=promises.find(p=>!p.draft); if(p) openDetail(p.id); }")
        pg.wait_for_timeout(1800)
    elif p == 'reglages':
        pg.evaluate("()=>{ var b=document.querySelector('#accPlat [aria-label*=églage], #accPlat .acc-reg, #setBtn'); if(b) b.click(); else if(window.openSettings) openSettings(); }"); pg.wait_for_timeout(1800)
    else:
        B.tap_sel(pg, {'aura': '#souffleBtn', 'index': '#indexBtn', 'fil': '#filBtn', 'plus': '#createBtn'}[p]); pg.wait_for_timeout(1800)
    ferme(pg); pg.wait_for_timeout(1200); pose(pg)
POSE = """()=>{ try{ var st=Toile_state(), l=Toile_lecture(), c=l.cible||l.vue; return !st.running && Math.abs(c.s-l.vue.s)<0.0005 && Math.abs(c.ox-l.vue.ox)<0.3 && Math.abs(c.oy-l.vue.oy)<0.3; }catch(e){ return true; } }"""
def pose(pg, t=12000):
    """la Toile posée : la boucle arrêtée et la vue sur sa cible, deux lectures de suite (sous charge, tout prend plus de temps)"""
    n = 0
    for _ in range(int(t / 250)):
        pg.wait_for_timeout(250); n = n + 1 if pg.evaluate(POSE) else 0
        if n >= 3: return True
    return False
def ecart(a, b):
    A = {x[0]: x for x in a['g']}; Bb = {x[0]: x for x in b['g']}
    if set(A) != set(Bb): return 'dalles %d → %d' % (len(A), len(Bb)), 999
    gr = max([max(abs(A[k][1] - Bb[k][1]), abs(A[k][2] - Bb[k][2])) for k in A] or [0])
    ec = max([max(abs(A[k][3] - Bb[k][3]), abs(A[k][4] - Bb[k][4])) for k in A] or [0])
    z = abs(a['v'][0] - b['v'][0]) / a['v'][0]
    d = 'à l\'écran %.1f pt · graines %.1f · zoom %.3f → %.3f · cellules %d → %d · monde %s → %s' % (ec, gr, a['v'][0], b['v'][0], a['n'], b['n'], a['th'], b['th'])
    ok = ec <= 1.0 and gr <= 0.5 and z <= 0.01 and a['n'] == b['n'] and a['th'] == b['th']
    return d, (0 if ok else 1)
with sync_playwright() as p:
    br = p.webkit.launch()
    for th in THEMES:
        for n in NS:
            for m in MONDES:
                ctx = B.contexte(br, sombre=(th == 'sombre'), stockage={'promi_monde': m}); B.toile_pleine(ctx, n); pg = B.ouvre(ctx, F, q=arg('q',''))
                pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", m); pg.wait_for_timeout(2800); pose(pg)
                a = pg.evaluate(GEO); rouges = []
                for pp in PAGES:
                    page(pg, pp); b = pg.evaluate(GEO); d, k = ecart(a, b)
                    if k: rouges.append('%s : %s' % (pp, d))
                    a = b if not k else a
                er = [e for e in pg.erreurs if 'version.json' not in e]
                juge('[%s · %d paroles · %s] sept pages ouvertes puis fermées : chaque dalle à sa place à l\'écran (1 pt)' % (th, n, m), not rouges and not er, (rouges[:2], er[:1]))
                ctx.close()
    br.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
