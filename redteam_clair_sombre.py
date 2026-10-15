#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_clair_sombre.py — MÊME TOILE EN CLAIR ET EN SOMBRE, DANS TOUS LES MONDES (v146, Tom, 14 oct. 2026 — C-131).

« La règle est absolue : c'est EXACTEMENT la même Toile en clair et en sombre (mêmes dalles, même disposition, mêmes formes, mêmes
tailles, mêmes graines), dans les 20 mondes et partout où une Toile s'affiche (accueil, partage, moodboard, onboarding). Seules les
couleurs du thème changent. Vérifie les 20 mondes, avec 1, 5, 25 et 50 paroles. Compare les géométries (positions des germes,
polygones) et pas les pixels. »

On compare la GÉOMÉTRIE, jamais une couleur. Par banc_tom (WebKit, 390 × 844 @3x), sur des Toiles relues de la sauvegarde
(banc-etats/etat-1|5|25|50.json), le thème changé par la porte de l'app (`window.setTheme`, celle des disques SOMBRE / CLAIR du Studio).

  A · L'ACCUEIL, À LA BASCULE — 20 mondes × 4 tailles : clair → sombre → clair sur la même page. Identiques au millième de point :
      le nombre de graines, chaque graine (parole, place, poids), la vue (zoom, décalage), la boîte de chaque dalle ; et LA CARTE DU
      TOUCHER (à quelle parole appartient chaque point d'une grille de 6 pt — pour un monde libre, c'est la dalle PEINTE).
  B · À L'OUVERTURE — l'app ouverte en clair et ouverte en sombre depuis la même sauvegarde (4 tailles, le monde sauvé et
      Ritournelle) : mêmes graines, même vue. Témoin : clair contre clair.
  C · UNE DALLE SEULE (fiche, Index, Fil) — 20 mondes, 3 paroles : la silhouette rendue par le moteur (`dalleTrame`, horloge figée)
      a la même taille et recouvre la même surface en clair et en sombre. Témoin : clair contre clair.
  D · LE STUDIO — le fond et les aperçus des mondes : mêmes graines en clair et en sombre.
  E · PARTAGER — ouvrir Partager, y changer de thème : la Toile lue est la même.
  F · L'IMAGE — après un aller-retour clair → sombre → clair, la Toile est la même image, cellules vides comprises (dix mondes, 5 paroles).
Le tableau monde par monde est écrit dans planche-v146/clair-sombre.md.

Preuve (§7) : `--sonde` fait dépendre la place d'une graine du thème (une parole décalée de 3 pt en sombre) : A et B rougissent. Et sur la
version d'avant (l'app et SON moteur : `python3 redteam_clair_sombre.py zz-cs-avant.html --tailles=25`, une copie de
sauvegardes/app-avant-v146.html qui charge sauvegardes/promi-moteur-avant-v146.js) : A et D rougissent sur le rang des gris.
Usage : python3 redteam_clair_sombre.py [fichier.html] [--tailles=1,5,25,50] [--mondes=a,b] [--sonde] [--vite]
"""
import sys, io, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); SONDE = '--sonde' in sys.argv; VITE = '--vite' in sys.argv
TAILLES = [int(x) for x in arg('tailles', '1,5,25,50').split(',')]
ORDRE = ['encre', 'touffe', 'brouillamini', 'halin', 'esquille', 'mosaique', 'braille', 'pixel', 'ramage', 'guingois', 'chantourne', 'volubilis',
         'madrure', 'chamade', 'ritournelle', 'bobinette', 'mascaret', 'terrazzo', 'gravure', 'sillons']          # l'ordre du Studio, EN DUR
NOMS = {'pixel': 'Buvard', 'braille': 'Braille', 'sillons': 'Houle', 'gravure': 'Taille-douce', 'mosaique': 'Tesselle', 'encre': 'Pochade', 'terrazzo': 'Éclisse',
        'touffe': 'Touffe', 'esquille': 'Esquille', 'halin': 'Halin', 'brouillamini': 'Brouillamini', 'chamade': 'Chamade', 'volubilis': 'Volubilis',
        'guingois': 'Guingois', 'chantourne': 'Chantourné', 'mascaret': 'Mascaret', 'ramage': 'Ramage', 'bobinette': 'Bobinette', 'ritournelle': 'Ritournelle', 'madrure': 'Madrure'}
MONDES = [m for m in ORDRE if m in arg('mondes', ','.join(ORDRE)).split(',')]
TOL = 0.001          # « identique au point près » : on exige le millième de point
res = []; TAB = {m: {} for m in ORDRE}
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:320]), flush=True)

LIT = """()=>{ const L=window.Toile_lecture(), r=v=>Math.round(v*10000)/10000;
  const g=L.graines.map(s=>[s.pid, s.kind, r(s.x), r(s.y), r(s.w), s.boite?JSON.stringify(s.boite, (k,v)=>typeof v==='number'?r(v):v):null]);
  /* la carte du toucher : à qui appartient chaque point d'une grille de 6 pt (pour un monde libre, la dalle PEINTE) */
  const c=Toile.canvas().getBoundingClientRect ? Toile.taille() : {w:L.W,h:L.H}; let carte='';
  for(let y=3;y<c.h;y+=6){ for(let x=3;x<c.w;x+=6){ let h=null; try{ h=Toile.hit(x,y); }catch(e){} carte+=(h?(h.pid!=null?('p'+h.pid):('n'+(h.nuee||''))):'.')+','; } }
  let rangs=null; try{ rangs=window.Toile_grisRangs?window.Toile_grisRangs().join(','):null; }catch(e){}
  return {vue:[r(L.vue.s),r(L.vue.ox),r(L.vue.oy)], g:g, carte:carte, rangs:rangs, clair:document.getElementById('device').classList.contains('light'), monde:Toile.getTheme()}; }"""
SONDE_JS = """()=>{ const o=window.Toile_lecture; window.Toile_lecture=function(){ const L=o.apply(this,arguments); if(!document.getElementById('device').classList.contains('light')){ const s=L.graines.find(q=>q.pid!=null); if(s) s.x+=3; } return L; }; }"""


def etat(ctx, n, sombre=None):
    st = json.load(io.open('banc-etats/etat-%d.json' % n, encoding='utf-8'))
    if sombre is None: st.pop('promi_theme', None)
    else: st['promi_theme'] = 'dark' if sombre else 'light'
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))


def pose(pg, max_ms=9000):
    """la Toile POSÉE : deux lectures identiques à 350 ms l'une de l'autre"""
    a = None; t = 0
    while t < max_ms:
        pg.wait_for_timeout(350); t += 350
        b = pg.evaluate(LIT)
        if a is not None and a['g'] == b['g'] and a['vue'] == b['vue']: return b
        a = b
    return a


def pose_ferme(pg):
    """la Toile VRAIMENT posée : après un changement de famille de monde (la Toile se ressème), deux lectures identiques ne suffisent pas — le
    relâchement s'arrête à un cheveu de l'équilibre et repart de 0,3 pt à la première repeinte (mesuré sous Tesselle et Éclisse, les deux
    mondes qui suivent un ressemis dans l'ordre du Studio ; le thème n'y est pour rien). On relance le moteur jusqu'à ce qu'une relance ne
    change plus rien."""
    a = pose(pg)
    for _ in range(8):
        pg.evaluate("()=>{ try{ Toile.redraw(); }catch(e){} }"); b = pose(pg)
        if a['g'] == b['g'] and a['vue'] == b['vue']: return b
        a = b
    return a


def ferme_ecran(pg, sel):
    r = pg.evaluate("s=>{ const e=[...document.querySelectorAll(s+' [data-close], '+s+' .closeb')].find(x=>x.getBoundingClientRect().width>4); if(!e) return null; const q=e.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }", sel)
    if r: pg.touchscreen.tap(r[0], r[1])
    pg.wait_for_timeout(900)


def ecart(a, b):
    """la plus grande différence de géométrie entre deux lectures : (graines, vue, boîtes différentes, points de la carte différents)"""
    if len(a['g']) != len(b['g']): return {'graines': 'nombre %d / %d' % (len(a['g']), len(b['g'])), 'vue': 0, 'boites': 0, 'carte': -1, 'gris': -1}
    m = 0.0
    for x, y in zip(a['g'], b['g']):
        if x[0] != y[0] or x[1] != y[1]: return {'graines': 'ordre %s / %s' % (x[:2], y[:2]), 'vue': 0, 'boites': 0, 'carte': -1, 'gris': -1}
        m = max(m, abs(x[2] - y[2]), abs(x[3] - y[3]), abs(x[4] - y[4]))
    ca, cb = a['carte'].split(','), b['carte'].split(',')
    return {'graines': round(m, 4), 'vue': round(max(abs(p - q) for p, q in zip(a['vue'], b['vue'])), 4),
            'boites': sum(1 for x, y in zip(a['g'], b['g']) if x[5] != y[5]), 'carte': sum(1 for p, q in zip(ca, cb) if p != q) if len(ca) == len(cb) else -1,
            # le RANG du gris de chaque cellule vide (la plus claire reste la plus claire) : combien en changent — -1 si l'app ne le publie pas
            'gris': (sum(1 for p, q in zip(a['rangs'].split(','), b['rangs'].split(',')) if p != q) if (a.get('rangs') is not None and b.get('rangs') is not None) else -1)}
def bon(e): return isinstance(e['graines'], float) and e['graines'] <= TOL and e['vue'] <= TOL and e['boites'] == 0 and e['carte'] == 0 and e['gris'] == 0


with sync_playwright() as p:
    b = p.webkit.launch()
    # ── A · l'accueil, à la bascule ─────────────────────────────────────────────────────────────
    for n in TAILLES:
        ctx = B.contexte(b); etat(ctx, n); pg = B.ouvre(ctx, F)
        # ⚠ LA VIE AU REPOS (v126) déplace une dalle d'une fraction de point pendant 1 à 2 s, toutes les 5 à 15 s, puis la rend exactement : lue au
        #   milieu d'un de ces mouvements, la Toile sortait « différente » de 0,3 pt sous Tesselle et Éclisse (25 et 50 paroles) — le thème n'y était
        #   pour rien (prouvé : sans bascule, la même lecture). On la coupe le temps de la mesure (`_vivantOff`, la porte du banc de rendu).
        pg.evaluate("()=>{ window._vivantOff=true; try{ setPremium(true); }catch(e){} }")
        if SONDE: pg.evaluate(SONDE_JS)
        npar = pg.evaluate("()=>promises.length")
        juge('A · %d parole(s) : la Toile relue de la sauvegarde porte ses paroles' % n, npar == n, npar)
        mauvais = []
        for m in MONDES:
            pg.evaluate("m=>Toile.setTheme(m)", m); c1 = pose_ferme(pg)
            pg.evaluate("()=>window.setTheme('dark')"); s = pose(pg)
            pg.evaluate("()=>window.setTheme('light')"); c2 = pose(pg)
            e1, e2 = ecart(c1, s), ecart(c1, c2)
            ok = c1['clair'] and not s['clair'] and c1['monde'] == m and bon(e1) and bon(e2)
            TAB[m][n] = {'graines': len(c1['g']), 'paroles': sum(1 for g in c1['g'] if g[0] is not None), 'ecart': e1['graines'], 'vue': e1['vue'], 'boites': e1['boites'], 'carte': e1['carte'], 'gris': e1['gris'], 'ok': ok}
            if not ok: mauvais.append('%s %s' % (m, e1))
        juge('A · %d parole(s) : dans les %d mondes, clair → sombre → clair ne change ni une graine, ni un poids, ni la vue, ni une boîte, ni un point de la carte du toucher, ni le rang du gris d\'une cellule vide' % (n, len(MONDES)),
             not mauvais, ' · '.join(mauvais)[:300] or '%d graines sous %s, %d sous Ritournelle' % (TAB[MONDES[0]][n]['graines'], NOMS[MONDES[0]], TAB.get('ritournelle', {}).get(n, {}).get('graines', 0)))
        # ── E · Partager : la Toile lue est la même, en clair comme en sombre
        if n == 25 and not VITE:
            pg.evaluate("m=>Toile.setTheme(m)", 'encre'); c0 = pose_ferme(pg)
            pg.evaluate("()=>{ try{ window.ouvrirPartage ? ouvrirPartage() : document.getElementById('shareBtn').click(); }catch(e){} }"); pg.wait_for_timeout(2600)
            ouvert = pg.evaluate("()=>{ const s=document.getElementById('shareScreen'); return !!(s && s.classList.contains('show')); }")
            p1 = pose(pg); pg.evaluate("()=>window.setTheme('dark')"); p2 = pose(pg); pg.evaluate("()=>window.setTheme('light')"); pose(pg)
            e = ecart(c0, p1); e2 = ecart(p1, p2)
            juge('E · Partager : la Toile qu\'on y partage est celle de l\'accueil, en clair comme en sombre', ouvert and bon(e) and bon(e2), 'Partager ouvert %s · accueil/partage %s · clair/sombre %s' % (ouvert, e, e2))
            ferme_ecran(pg, '#shareScreen'); pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
        # ── C · une dalle seule : la silhouette rendue par le moteur, horloge figée
        if n == 5:
            mauvais = []; pire = 1.0
            for m in MONDES:
                pg.evaluate("m=>Toile.setTheme(m)", m); pose(pg)
                r = pg.evaluate("""()=>{ const ids=promises.slice(0,3).map(p=>p.id), T=performance.now(), vrai=performance.now; const out=[];
                    function masque(id){ const cv=document.createElement('canvas'); try{ Toile.dalleTrame(cv, id, 1); }catch(e){ return null; }
                      if(!cv.width||!cv.height) return {w:0,h:0,a:null}; const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, a=new Uint8Array(cv.width*cv.height); let n=0;
                      for(let i=0;i<a.length;i++){ if(d[i*4+3]>32){ a[i]=1; n++; } } return {w:cv.width,h:cv.height,a:a,n:n}; }
                    function iou(p,q){ if(!p||!q||!p.a||!q.a) return 0; if(p.w!==q.w||p.h!==q.h) return 0; let i=0,u=0; for(let k=0;k<p.a.length;k++){ if(p.a[k]&&q.a[k]) i++; if(p.a[k]||q.a[k]) u++; } return u?i/u:1; }
                    try{ performance.now=function(){ return T; };
                      for(const id of ids){ const c1=masque(id); window.setTheme('dark'); const s=masque(id); window.setTheme('light'); const c2=masque(id);
                        out.push({id:id, clair:c1&&[c1.w,c1.h,c1.n], sombre:s&&[s.w,s.h,s.n], cs:iou(c1,s), cc:iou(c1,c2)}); }
                    } finally { performance.now=vrai; }
                    return out; }""")
                pg.wait_for_timeout(250)
                cs = min([x['cs'] for x in r] or [0]); cc = min([x['cc'] for x in r] or [0]); pire = min(pire, cs)
                TAB[m]['dalle'] = {'cs': cs, 'cc': cc}
                # la même silhouette : mêmes dimensions, et un recouvrement au moins égal à celui du témoin clair/clair (à 0,5 % près)
                if not (r and all(x['clair'] and x['sombre'] and x['clair'][:2] == x['sombre'][:2] for x in r) and cs >= min(cc, 1.0) - 0.005 and cs >= 0.985): mauvais.append('%s clair/sombre %.4f (témoin %.4f) %s' % (m, cs, cc, [(x['clair'], x['sombre']) for x in r][:1]))
            juge('C · une dalle rendue seule a la même silhouette en clair et en sombre, dans les %d mondes (3 paroles chacun)' % len(MONDES), not mauvais, ' · '.join(mauvais)[:300] or 'recouvrement le plus faible %.4f' % pire)
        # ── F · L'IMAGE : après un aller-retour clair → sombre → clair, la Toile claire est la MÊME IMAGE (ses cellules vides comprises), et la
        #      sombre de même. C'est le verdict RENDU du rang des gris (le pointeur `Toile_grisRangs` ne sert qu'à nommer la cellule fautive).
        #      Sur la version d'avant : 32 % des pixels changés sous Pochade, 39 % sous Tesselle, 8 à 10 % sous Touffe et Braille.
        if n == 5:
            import numpy as np
            from PIL import Image
            def img(): return np.asarray(Image.open(io.BytesIO(B.capture(pg))).convert('RGB').resize((390, 844))).astype(int)[110:700]
            def part(a, b): return float((np.abs(a - b).sum(axis=2) > 12).mean()) * 100
            mauvais = []; pire = 0.0
            for m in [x for x in ('encre', 'touffe', 'mosaique', 'braille', 'pixel', 'terrazzo', 'gravure', 'sillons', 'chamade', 'halin') if x in MONDES]:
                pg.evaluate("m=>Toile.setTheme(m)", m); pose_ferme(pg); pg.wait_for_timeout(900)
                c1 = img(); pg.wait_for_timeout(600); t = part(c1, img())
                pg.evaluate("()=>window.setTheme('dark')"); pg.wait_for_timeout(1300); s1 = img()
                pg.evaluate("()=>window.setTheme('light')"); pg.wait_for_timeout(1300); c2 = img()
                pg.evaluate("()=>window.setTheme('dark')"); pg.wait_for_timeout(1300); s2 = img()
                pg.evaluate("()=>window.setTheme('light')"); pg.wait_for_timeout(700)
                dc, ds = part(c1, c2), part(s1, s2); pire = max(pire, dc, ds); TAB[m]['image'] = (dc, ds, t)
                if dc > t + 0.5 or ds > t + 0.5: mauvais.append('%s : clair %.1f %% · sombre %.1f %% (témoin %.1f %%)' % (NOMS[m], dc, ds, t))
            juge('F · après un aller-retour clair → sombre → clair, la Toile est la même IMAGE (cellules vides comprises), en clair comme en sombre', not mauvais, ' · '.join(mauvais)[:300] or 'part de pixels changés, au pire : %.2f %%' % pire)
        # ── D · le Studio : sa Toile est VIVANTE (elle plante et retire des paroles pour montrer le monde : en 1,5 s, sans rien toucher, ses
        #      graines bougent de 10 pt) — on ne compare donc pas deux instants. On juge LA BASCULE : dans la tâche même où le thème change,
        #      aucune graine ne bouge, aucune dalle ne change, aucune cellule vide ne change de rang de gris.
        if n == 25 and not VITE:
            ferme_ecran(pg, '#shareScreen'); pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500); B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(4800)
            r = pg.evaluate("""()=>{ const cv=document.getElementById('stBg'); if(!cv||!cv.__c||!cv.__c.seeds) return null;
                const lit=()=>JSON.stringify(cv.__c.seeds.map(s=>[s.kind==='gray'?0:1, Math.round(s.x*100), Math.round(s.y*100), Math.round(s.w*100)]));
                const rg=()=>window.Toile_grisRangs?JSON.stringify(window.Toile_grisRangs(cv)):null;
                const a=lit(), ra=rg(); window.setTheme('dark'); const b=lit(), rb=rg(); window.setTheme('light'); const c=lit(), rc=rg();
                return {n:cv.__c.seeds.length, graines:(a===b && b===c), gris:(ra!==null && ra===rb && rb===rc), publie:ra!==null, monde:cv.__c.th}; }""")
            juge('D · le Studio : à la bascule du thème, sa Toile garde ses graines, ses dalles et le rang de gris de chaque cellule vide', bool(r) and r['graines'] and r['gris'], r)
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }")
        juge('A · %d parole(s) : aucune erreur de page' % n, not pg.erreurs, pg.erreurs[:2]); ctx.close()
    # ── B · à l'ouverture : clair contre sombre, depuis la même sauvegarde ──────────────────────────
    def ouverture(n, sombre, monde):
        ctx = B.contexte(b, sombre=sombre); etat(ctx, n, sombre); pg = B.ouvre(ctx, F, attente=7000)
        pg.evaluate("()=>{ window._vivantOff=true; }")
        if SONDE: pg.evaluate(SONDE_JS)
        if monde: pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} Toile.setTheme(m); }", monde)
        g = pose_ferme(pg); ctx.close(); return g
    if not VITE:
        for n in TAILLES:
            for monde in (None, 'ritournelle'):
                c1 = ouverture(n, False, monde); s1 = ouverture(n, True, monde); c2 = ouverture(n, False, monde)
                e, t = ecart(c1, s1), ecart(c1, c2)
                juge('B · %d parole(s), %s : l\'app ouverte en sombre montre la Toile de l\'app ouverte en clair' % (n, NOMS.get(monde or c1['monde'], monde)), c1['clair'] and not s1['clair'] and bon(e), 'clair/sombre %s · témoin clair/clair %s' % (e, t))
    b.close()

# le tableau, monde par monde
L = ['# Même Toile en clair et en sombre — monde par monde (v146, C-131)', '',
     'Bascule clair → sombre sur la même page, Toile relue de la sauvegarde. Écart = la plus grande différence de place ou de poids d\'une graine, en points ;',
     '« carte » = nombre de points de la grille du toucher (6 pt) qui changent de parole ; « gris » = nombre de cellules vides dont le rang de gris change ; « dalle seule » = recouvrement des silhouettes clair / sombre (témoin clair / clair).', '',
     '| Monde | ' + ' | '.join('%d parole%s' % (n, 's' if n > 1 else '') for n in TAILLES) + ' | Dalle seule | Image après un aller-retour (clair · sombre) | Verdict |', '|---|' + '---|' * (len(TAILLES) + 3)]
for m in ORDRE:
    if m not in MONDES: continue
    c = []
    for n in TAILLES:
        t = TAB[m].get(n)
        c.append('—' if not t else '%d graines · écart %s · vue %s · carte %s · gris %s' % (t['graines'], t['ecart'], t['vue'], t['carte'], t['gris']))
    d = TAB[m].get('dalle'); tout = all(TAB[m].get(n, {}).get('ok') for n in TAILLES)
    im = TAB[m].get('image')
    L.append('| %s | %s | %s | %s | %s |' % (NOMS[m], ' | '.join(c), ('%.4f (%.4f)' % (d['cs'], d['cc'])) if d else '—', ('%.1f %% · %.1f %%' % (im[0], im[1])) if im else '—', 'identique' if tout else 'DIFFÉRENT'))
try: io.open('planche-v146/clair-sombre.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
except Exception: pass
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1500])
sys.exit(0 if ok == len(res) else 1)
