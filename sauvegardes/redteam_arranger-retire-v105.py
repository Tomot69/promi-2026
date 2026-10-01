#!/usr/bin/env python3
"""
redteam_arranger.py — « ARRANGER LA TOILE » RANGE VRAIMENT LA TOILE, ET ELLE SE RÉORGANISE (Tom, 30 sept. 2026 :
« une porte qui mène à une feuille qui ne fait rien est pire que pas de porte » ; « la Toile se réorganise, elle ne saute pas »).

WebKit, au doigt :
  1 · la porte est sur l'accueil, et un toucher ouvre la feuille
  2 · « Date » : les échéances les plus proches montent — corrélation échéance ↔ hauteur de la GRAINE ≥ 0,6
  3 · « Nuée » : les paroles d'une Nuée sont plus hautes que celles sans Nuée
  4 · « Personne » : mes paroles (« moi ») au-dessus de celles des autres
  5 · « Inspi » : chaque dalle revient à sa place d'avant le premier rangement (≤ 2 px)
  6 · LE MOUVEMENT : dans quatre mondes (deux neufs à ressort, deux anciens), la graine au plus long trajet y va en ≥ 6 images et
      aucune image n'en fait plus de 35 % — seuil posé au-dessus du pas NATUREL des mondes anciens (22 %, celui de la plantation)
  7 · l'ordre est gardé : après rechargement, `state.sort` le porte et la Toile est déjà rangée (sans mouvement)
Seuils EN DUR (§7). Prouvé contre sauvegardes/app-avant-v104.html.
"""
import sys, math
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
CORR_MIN = 0.6; INSPI_MAX = 2.0; PAS_MAX = 0.35; IMAGES_MIN = 6
res = []
def t(nom, ok, detail=''):
    res.append(ok); print(('  ✅ ' if ok else '  ❌ ') + nom + ('  — ' + detail if detail else ''))

GR = "()=>{var o={};(window.Toile_graines?Toile_graines():[]).forEach(z=>{if(z[0]!=null)o[z[0]]=[z[1],z[2]];});return o}"
INFO = "()=>{var o={};promises.forEach(p=>{o[p.id]=[p.due,p.nuee||null,p.who||'moi'];});return o}"

def moy(L): return sum(L) / len(L)
def corr(a, b):
    ma, mb = moy(a), moy(b); c = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    d = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)); return c / d if d else 0

with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000)
    info = pg.evaluate(INFO); h = pg.evaluate(GR)

    # 1 · la porte, au doigt
    r = pg.evaluate("()=>{const e=document.getElementById('accArranger'); if(!e) return null; const q=e.getBoundingClientRect(); const v=getComputedStyle(e); return {x:q.left+q.width/2,y:q.top+q.height/2,vu:v.visibility!=='hidden'&&v.display!=='none'&&+v.opacity>0.5&&q.width>20}}")
    ouvert = False
    if r and r['vu']:
        pg.touchscreen.tap(r['x'], r['y']); pg.wait_for_timeout(700)
        ouvert = pg.evaluate("()=>document.getElementById('arrangeSheet').classList.contains('show')")
    t('1 · la porte est sur l\'accueil et ouvre la feuille, au doigt', bool(r and r['vu'] and ouvert), str(r))

    def choisir(m, suivre=False):
        if not pg.evaluate("()=>document.getElementById('arrangeSheet').classList.contains('show')"):
            pg.evaluate("()=>{buildArrange();openSheet(document.getElementById('arrangeSheet'))}"); pg.wait_for_timeout(500)
        q = pg.evaluate("m=>{const e=document.querySelector('#arrangeSheet .arr[data-mode='+m+']');const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}", m)
        if suivre: pg.evaluate("()=>{window.__tr=[];const t0=performance.now();(function f(){__tr.push([performance.now()-t0,(window.Toile_graines?Toile_graines():[]).map(z=>[z[0],z[1],z[2]])]);if(performance.now()-t0<2600)requestAnimationFrame(f);})();}")
        pg.touchscreen.tap(q[0], q[1]); pg.wait_for_timeout(2800)
        return pg.evaluate(GR)

    d = choisir('date')
    v = [(info[k][0], d[k][1]) for k in d if k in info and isinstance(info[k][0], (int, float))]
    c = corr([x[0] for x in v], [x[1] for x in v]) if len(v) > 2 else 0
    t('2 · « Date » : les plus proches en haut (corrélation échéance ↔ hauteur ≥ %.1f)' % CORR_MIN, c >= CORR_MIN, 'corrélation %.2f sur %d paroles' % (c, len(v)))

    n = choisir('nuee')
    avec = [n[k][1] for k in n if k in info and info[k][1]]; sans = [n[k][1] for k in n if k in info and not info[k][1]]
    t('3 · « Nuée » : les paroles d\'une Nuée au-dessus des autres', bool(avec and sans and moy(avec) < moy(sans)),
      'avec %.0f · sans %.0f' % (moy(avec) if avec else -1, moy(sans) if sans else -1))

    pe = choisir('personne')
    moi = [pe[k][1] for k in pe if k in info and info[k][2] == 'moi']; aut = [pe[k][1] for k in pe if k in info and info[k][2] != 'moi']
    t('4 · « Personne » : mes paroles au-dessus de celles des autres', bool(moi and aut and moy(moi) < moy(aut)),
      'moi %.0f · autres %.0f' % (moy(moi) if moi else -1, moy(aut) if aut else -1))

    i = choisir('inspi')
    e = [math.hypot(h[k][0] - i[k][0], h[k][1] - i[k][1]) for k in h if k in i]
    t('5 · « Inspi » : chaque dalle revient à sa place (≤ %.0f px)' % INSPI_MAX, bool(e) and max(e) <= INSPI_MAX, 'écart max %.1f px' % (max(e) if e else -1))

    # 6 · le mouvement, monde par monde
    for m in ['esquille', 'madrure', 'encre', 'braille']:
        pg.evaluate("m=>Toile.setTheme(m)", m); pg.wait_for_timeout(3000)
        choisir('date' if m in ('esquille', 'encre') else 'personne', suivre=True)
        tr = pg.evaluate("()=>__tr")
        def pos(f, k):
            for z in f[1]:
                if z[0] == k: return (z[1], z[2])
        ids = [z[0] for z in tr[0][1] if z[0] is not None] if tr else []
        def long(k):
            a, z = pos(tr[0], k), pos(tr[-1], k); return math.hypot(z[0] - a[0], z[1] - a[1]) if a and z else 0
        best = max(ids, key=long) if ids else None
        pts = [pos(f, best) for f in tr if pos(f, best)] if best is not None else []
        tot = long(best) if best is not None else 0
        pas = [math.hypot(pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]) for j in range(len(pts) - 1)]
        nb = sum(1 for x in pas if x > 0.5)
        ok = tot > 40 and nb >= IMAGES_MIN and max(pas) <= PAS_MAX * tot
        t('6 · %s : la Toile se réorganise, elle ne saute pas' % m, ok,
          'trajet %.0f px en %d images, plus grand pas %.0f %%' % (tot, nb, 100 * max(pas) / tot if tot and pas else 0))
        choisir('inspi')

    # 7 · l'ordre gardé
    pg.evaluate("()=>Toile.setTheme('encre')"); pg.wait_for_timeout(2500)
    choisir('date'); avant = pg.evaluate(GR)
    pg.reload(); pg.wait_for_timeout(7500)
    s = pg.evaluate("()=>state.sort"); apres = pg.evaluate(GR); info = pg.evaluate(INFO)
    v = [(info[k][0], apres[k][1]) for k in apres if k in info and isinstance(info[k][0], (int, float))]
    c = corr([x[0] for x in v], [x[1] for x in v]) if len(v) > 2 else 0
    t('7 · après rechargement l\'ordre est gardé et la Toile déjà rangée', s == 'date' and c >= CORR_MIN, 'state.sort %s · corrélation %.2f' % (s, c))
    b.close()

n = len(res); k = sum(res)
print('\n%d/%d' % (k, n))
sys.exit(0 if k == n else 1)
