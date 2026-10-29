#!/usr/bin/env python3
"""
redteam_etat_fiche.py — v171 (Tom, 29 oct. 2026, C-207) : LA LIGNE D'ÉTAT D'UNE FICHE NE BOUGE PAS D'UNE OUVERTURE À L'AUTRE, NI D'UNE ÉCHELLE À L'AUTRE.

« La ligne d'état d'une fiche (« LANCÉ », « EN COURS ») sort à deux hauteurs qui diffèrent de 2 pt, selon l'ouverture, à l'échelle 0,79. Rends sa
position stable. Juge : 10 ouvertures, même position au pixel, aux échelles 1 et 0,79. »

La cause (v171) : le poseur de la fiche divisait ses mesures d'écran par `dp.clientWidth / 390` — une cote de mise en page, 1 à toutes les échelles.
À 0,79 la hauteur et le jambage du titre entraient réduits dans la cote de la ligne d'état (9 à 12 pt plus haut qu'à l'échelle 1), et l'arrondi de
ces valeurs réduites dépendait de l'instant de la mesure.

Le juge : WebKit, banc comme Tom (doigt, webdriver masqué), une Toile relue de la sauvegarde (un Promi en cours, un Chiche lancé). Dix ouvertures,
CHACUNE SUR UNE PAGE FRAÎCHE, à trois échelles — 1 (430 × 932), 0,79 (330 × 714) et l'état exporté de Tom (sa fenêtre) ; chaque fiche ouverte au
doigt depuis l'Index. On lit la ligne d'état À L'ÉCRAN, en pixels de l'appareil : la même aux dix ouvertures ; et en points de l'écran 390, la même aux
trois échelles (± un pixel de l'appareil, l'arrondi de la réduction). Les valeurs décidées ne sont pas lues dans l'app : la position de référence est
celle de l'échelle 1.
Rouge sur v170d (`git show 9b4fc45:app.html > zz-v170d.html` ; `--fichier=zz-v170d.html`).
"""
import sys, io, os, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
N = int(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--n=')), '10'))
ETAT = 'banc-etats/etat-v171-fiches.json'
res = []
def _tom():   # le dernier état exporté QUI PORTE DES PAROLES (v160 : un onglet vide exporte une Toile vide)
    import glob
    for f in sorted(glob.glob('etats/tom-*.json'))[::-1]:
        try:
            d = json.load(io.open(f, encoding='utf-8')); s = json.loads(d['ls'].get('promi_state') or '{}')
            if (s.get('promises') if isinstance(s, dict) else s): return f
        except Exception: pass
TOM = _tom()
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-80s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
LIT = """()=>{ const q=document.getElementById('dptQuand'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=q.getBoundingClientRect();
  const P=document.getElementById('detailPoster').getBoundingClientRect();
  return {txt:q.textContent.trim(), top:q.style.top, pt:+((r.top-P.top)/k).toFixed(2), px:Math.round((r.top-P.top)*devicePixelRatio), k:+k.toFixed(4), pose:Math.abs(P.top-D.top)<0.5}; }"""
CARTES = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return [...document.querySelectorAll('#indexList .s4-carte')].filter(c=>c.getAttribute('data-etat')!=='tenu' && c.getAttribute('data-etat')!=='garde')
    .slice(0,2).map(c=>{ const r=c.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height*0.3-D.top)/k, (c.textContent||'').trim().slice(0,40)]; }); }"""
def prepare(b):
    if os.path.exists(ETAT): return
    ctx = B.contexte(b, False, vw=430, vh=932); pg = B.ouvre(ctx)
    B.plante_doigt(pg, 'écrire à Lou', 'moi', 0); B.plante_doigt(pg, 'nager dans le lac', 'moi', 1); pg.wait_for_timeout(1500)
    st = pg.evaluate("()=>{ const o={}; for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); o[k]=localStorage.getItem(k); } return o; }")
    for k in ('promi_theme', 'promi_veille_off'): st.pop(k, None)
    io.open(ETAT, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False)); ctx.close()
def une_ouverture(b, cfg):
    if cfg == 'tom':
        ctx, d = B.contexte_tom(b, TOM)
        if not ctx: return None
    else:
        vw, vh = cfg; ctx = B.contexte(b, False, vw=vw, vh=vh)
        st = json.load(io.open(ETAT, encoding='utf-8'))
        ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
    pg = B.ouvre(ctx, F); out = []
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2500)
    for x, y, t in pg.evaluate(CARTES):
        # l'Index rouvert et la carte sous le doigt AVANT de toucher (sous charge, l'Index met plus de 1,8 s à revenir : le doigt tombait sur la Toile)
        for _ in range(30):
            if pg.evaluate("([x,y,t])=>{ const ix=document.getElementById('indexSheet'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.elementFromPoint(D.left+x*k, D.top+y*k), c=e&&e.closest?e.closest('.s4-carte'):null; return !!(ix && ix.classList.contains('show') && c && (c.textContent||'').trim().slice(0,40)===t); }", [x, y, t]): break
            pg.wait_for_timeout(300)
        B.tap(pg, x, y); v = None; av = None
        # la ligne se lit fiche POSÉE : ouverte, arrivée en haut de l'appareil, sa cote écrite, et deux lectures identiques à 300 ms (sous charge, la fiche glisse
        # encore à 2,4 s) ; la ligne se lit DANS la fiche (son haut), en pixels de l'appareil
        for _ in range(40):
            pg.wait_for_timeout(300)
            if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"): continue
            v = pg.evaluate(LIT)
            if v['top'] and v['pose'] and av and av['px'] == v['px'] and av['top'] == v['top']: break
            av = v
        else: v = None
        if v is None:
            out.append(('?', t, pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(), P=dp.getBoundingClientRect(), ix=document.getElementById('indexSheet'); return {fiche:dp.classList.contains('show'), haut:+((P.top-D.top)/(D.width/390)).toFixed(1), index:!!(ix&&ix.classList.contains('show')), charge:0}; }"), round(B.charge(), 1))); continue
        v['carte'] = t; out.append(v)
        pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(700)
        B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(1800)
    ctx.close(); return out
with sync_playwright() as p:
    b = p.webkit.launch(); prepare(b)
    print('redteam_etat_fiche — %s, %d ouvertures par échelle, charge %.1f' % (F, N, B.charge()))
    TOUT = {}
    for nom, cfg in (('1', (430, 932)), ('0,79', (330, 714)), ('Tom', 'tom')):
        L = [une_ouverture(b, cfg) for _ in range(N)]
        if L[0] is None: print('  — pas d\'état exporté de Tom'); continue
        print('  échelle %s : %s' % (nom, '; '.join('%s %s' % (v['txt'], v['top']) for v in L[0] if isinstance(v, dict))))
        juge('échelle %s : chaque fiche s\'ouvre au doigt depuis l\'Index, aux %d ouvertures' % (nom, N), all(len(o) == 2 and all(isinstance(v, dict) for v in o) for o in L),
             [o for o in L if not (len(o) == 2 and all(isinstance(v, dict) for v in o))][:2])
        for i in range(2):
            vs = [o[i] for o in L if len(o) > i and isinstance(o[i], dict)]
            if not vs: continue
            pxs = sorted(set(v['px'] for v in vs)); tops = sorted(set(v['top'] for v in vs))
            juge('échelle %s, « %s » : la même ligne au pixel aux %d ouvertures' % (nom, vs[0]['txt'], len(vs)), len(pxs) == 1 and len(tops) == 1,
                 'pixels de l\'appareil %s · cotes %s' % (pxs, tops))
            TOUT.setdefault((cfg == 'tom', i), []).append((nom, vs[0]))
    for (tom, i), L in TOUT.items():
        if tom: continue
        ref = L[0][1]
        for nom, v in L[1:]:
            tol = 1 / (v['k'] * 3) + 0.01   # un pixel de l'appareil, ramené en points 390
            juge('« %s » : à l\'échelle %s, la ligne à la même place qu\'à l\'échelle 1 (en pt 390)' % (ref['txt'], nom),
                 abs(v['pt'] - ref['pt']) <= tol and v['top'] == ref['top'], '%.2f pt contre %.2f (cote %s contre %s)' % (v['pt'], ref['pt'], v['top'], ref['top']))
    b.close()
print('%d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
