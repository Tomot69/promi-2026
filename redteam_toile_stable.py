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
⚑ v160 (Tom, C-177 — « les dalles sont ENCORE entassées dès l'ouverture, et ça persiste ») — LA CAUSE ÉTAIT DANS LES DONNÉES : la parole de l'onboarding
  recevait en dur la place [0.42, 0.74] (v146), l'onboarding rejoué la redonnait à chaque parole ; le moteur rend chacune à la cellule vide la plus proche
  de sa place → six dalles collées (écart mini 1,3 à 5,5 pt) dans TOUTES les versions de v152 à v160a. Le juge porte maintenant, en plus :
  T · L'ÉTAT EXACT DE TOM (`--tom=etats/tom-….json` ; par défaut le dernier export qui porte des paroles) : aucune paire de dalles entassée à l'ouverture
      (moins de 0,3 × l'écart moyen des cellules), puis trois réouvertures : les places enregistrées identiques, les graines à 1 pt, la vue à 4 pt
      (⚠ la vue de cette Toile hésite entre deux cadrages, zoom 1 ou 1,004 — 3,8 pt —, selon l'ouverture, EN v158 AUSSI : le cadrage d'origine au bord
      du zoom 1, non corrigé) ; rouge sur v160a ;
  X · DES DONNÉES ABÎMÉES EXPRÈS (places empilées, à zéro, hors de [0, 1], non numériques) : réparées à l'ouverture — chaque place valide, aucune
      place prise deux fois, aucune dalle entassée, stable sur trois réouvertures ;
  S · UNE TOILE SAINE : rien n'est réparé, rien n'est réécrit, les graines identiques à `--ref=` (v160a servie à côté) à 0,5 pt. ⚠ PAS AU PIXEL PAR CE
      CHEMIN : chargée en temps réel, une Toile de 25 paroles prend plusieurs images d'une ouverture à l'autre, et un fichier plus long d'un simple
      commentaire (aucun code) en change la répartition (mesuré : 4 écarts sur 8 contre v160a) — la preuve au pixel est `banc_rendu` (horloge pilotée) ;
  M · 20 mondes × {1, 5, 9, 25, 50} paroles : à l'ouverture à froid, aucune dalle entassée ; puis les sept pages (comme v159).
      ⚠ ROUGE PAR DÉFAUTS CONNUS, IDENTIQUES SUR v160a (84/100 à la naissance) : Terrazzo à 1 et 5 paroles après le Studio (la vue d'un autre monde, Q574) ;
      Esquille, Mosaïque, Braille à 1 parole après le Studio (le ressemis, Q573) ; à 50 paroles, les douze mondes « faits de leurs seules paroles » posent
      deux dalles à 0,1–0,2 pt (le moteur en semis neuf, Q575).
Options : `--mondes=a,b` · `--q=?…` · `--n=1,5,9,25,50` · `--themes=sombre` (clair,sombre pour les deux) · `--fichier=` · `--ref=zz-v160a.html` ·
`--parties=T,X,S,M` · `--tom=`.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--%s=' % k)), d)
F = arg('fichier', 'app.html')
MONDES = arg('mondes', 'encre,touffe,brouillamini,halin,esquille,mosaique,braille,pixel,ramage,guingois,chantourne,volubilis,madrure,chamade,ritournelle,bobinette,mascaret,terrazzo,gravure,sillons').split(',')
NS = [int(x) for x in arg('n', '1,5,9,25,50').split(',')]
THEMES = arg('themes', 'sombre').split(',')
REF = arg('ref', 'zz-v160a.html'); PARTIES = arg('parties', 'T,X,S,M').split(',')
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
import json, io, glob, os
def etat(n):
    """la Toile de n paroles relue de la sauvegarde (banc-etats) ; 9 = celle de 10, sa dernière parole retirée"""
    st = json.load(io.open('banc-etats/etat-%d.json' % (10 if n == 9 else n), encoding='utf-8')); st.pop('promi_theme', None)
    if n == 9:
        S0 = json.loads(st['promi_state']); S0['promises'] = S0['promises'][:-1]; st['promi_state'] = json.dumps(S0)
    return st
def studio(m): return {'promi_studio': json.dumps({'m': m, 'p': 'signal', 'h': 0, 'libre': True, 'acquis': {}})}   # le monde posé AVANT l'ouverture : une vraie ouverture à froid dans ce monde
AMORCE = """(()=>{ let a=20261023>>>0; Math.random=function(){ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1);
  t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; window._vivantOff=true; })();"""
def pose_etat(ctx, st):
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
ENTASSE = """()=>{ var c=Toile_cellules(), v=c.view, col=c.c.filter(s=>s.kind!=='gray'), P=col.map(s=>[s.x*v.s+v.ox, s.y*v.s+v.oy]);
  var seuil=0.3*Math.sqrt(390*844/Math.max(1,c.c.length))*v.s, pr=[], dm=1e9;
  for(var i=0;i<P.length;i++) for(var j=i+1;j<P.length;j++){ var d=Math.hypot(P[i][0]-P[j][0],P[i][1]-P[j][1]); dm=Math.min(dm,d); if(d<seuil) pr.push(d.toFixed(1)); }
  return {n:P.length, seuil:+seuil.toFixed(1), dmin:+dm.toFixed(1), paires:pr}; }"""
PLACES = """()=>{ var S=JSON.parse(localStorage.getItem('promi_state')||'{}'); return (S.promises||[]).filter(p=>!p.draft).map(p=>[p.id, p.place==null?null:p.place]); }"""
def places_ok(pl):
    """chaque place valide ([0, 1], finie, pas (0, 0)) et aucune prise deux fois dans la même famille"""
    v = [x[1] for x in pl if x[1] is not None]; bad = [x for x in pl if x[1] is not None and not (isinstance(x[1], list) and 2 <= len(x[1]) <= 3 and all(isinstance(t, (int, float)) for t in x[1][:2]) and 0 <= x[1][0] <= 1 and 0 <= x[1][1] <= 1 and not (x[1][0] == 0 and x[1][1] == 0))]
    dup = [(a, b) for i, a in enumerate(v) for b in v[i+1:] if not bad and (a[2] if len(a) > 2 else 0) == (b[2] if len(b) > 2 else 0) and abs(a[0]-b[0]) < 0.003 and abs(a[1]-b[1]) < 0.003]
    return not bad and not dup, 'invalides %s · prises deux fois %s · sans place %d (le semis neuf n\'en note pas : rien d\'anormal)' % (bad[:2], dup[:2], len(pl) - len(v))
def entasse_ok(pg):
    e = pg.evaluate(ENTASSE); return not e['paires'], '%d dalles · écart mini %s pt (seuil %s) · paires entassées %s' % (e['n'], e['dmin'], e['seuil'], e['paires'][:6])
def reouvre(pg, n=3):
    """trois réouvertures : les places enregistrées, les graines (à 1 pt) et la vue (à 4 pt) ne bougent plus"""
    a = (pg.evaluate(PLACES), pg.evaluate(GEO)); d = []
    for k in range(n):
        pg.reload(timeout=180000); pg.wait_for_timeout(6500); pose(pg)
        b = (pg.evaluate(PLACES), pg.evaluate(GEO))
        if b[0] != a[0]: d.append('ouverture %d : places %s → %s' % (k + 2, [x for x in a[0] if x not in b[0]][:2], [x for x in b[0] if x not in a[0]][:2]))
        A = {x[0]: x for x in a[1]['g']}; Bb = {x[0]: x for x in b[1]['g']}
        gr = max([max(abs(A[q][1] - Bb[q][1]), abs(A[q][2] - Bb[q][2])) for q in A if q in Bb] or [0]); ec = max([max(abs(A[q][3] - Bb[q][3]), abs(A[q][4] - Bb[q][4])) for q in A if q in Bb] or [0])
        if set(A) != set(Bb) or gr > 1.0 or ec > 4.0: d.append('ouverture %d : graines %.1f pt · à l\'écran %.1f pt' % (k + 2, gr, ec))
        ok, t = entasse_ok(pg)
        if not ok: d.append('ouverture %d : %s' % (k + 2, t))
    return not d, d
def pixels(pg):
    pg.evaluate("()=>{ window._vivantOff=true; }"); pg.wait_for_timeout(400); pose(pg)
    return pg.evaluate("()=>{ var c=document.getElementById('toileCv'), d=c.getContext('2d').getImageData(0,0,c.width,c.height).data, h=2166136261; for(var i=0;i<d.length;i+=1){ h^=d[i]; h=Math.imul(h,16777619)>>>0; } return [c.width,c.height,h]; }")
with sync_playwright() as p:
    br = p.webkit.launch()
    # ── T · L'ÉTAT EXACT DE TOM ──
    if 'T' in PARTIES:
        tom = arg('tom', '')
        if not tom:
            L = [f for f in sorted(glob.glob('etats/tom-*.json')) if json.loads(json.load(io.open(f, encoding='utf-8')).get('ls', {}).get('promi_state', '{}') or '{}').get('promises')]
            tom = L[-1] if L else ''
        if not tom: juge('[T] l\'état exporté de Tom existe (etats/tom-*.json, avec des paroles)', False, 'aucun')
        else:
          for ech in (None, 1):   # sa fenêtre réelle (Safari, échelle ≈ 0,75), puis l'échelle 1 (A3)
            ctx, d = B.contexte_tom(br, tom, echelle=ech); pg = ctx.new_page(); E = 'sa fenêtre %s × %s' % (d['ecran'].get('largeur'), d['ecran'].get('hauteur')) if ech is None else 'échelle 1'
            pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(6500); pose(pg)
            ok, t = entasse_ok(pg); juge('[T · %s · %s · %s] à l\'ouverture, aucune dalle entassée' % (os.path.basename(tom), d['toile'].get('monde'), E), ok, t)
            ok, t = places_ok(pg.evaluate(PLACES)); juge('[T · %s] les places enregistrées sont valides et distinctes' % E, ok, t)
            ok, t = reouvre(pg); juge('[T · %s] trois réouvertures : les mêmes places, les graines à 1 pt, la vue à 4 pt, rien d\'entassé' % E, ok, t[:3])
            ctx.close()
    # ── X · DES DONNÉES ABÎMÉES EXPRÈS ──
    if 'X' in PARTIES:
        ABIMES = [('empilées', 5, lambda i: [0.42, 0.74]), ('à zéro', 5, lambda i: [0, 0]), ('hors de [0, 1]', 5, lambda i: [[1.7, -0.4], [-0.2, 0.5], [0.5, 3], [9, 9], [0.3, 1.2]][i % 5]),
                  ('non numériques', 5, lambda i: [['a', 'b'], [None, 0.5], [0.5], [0.1, 0.2, 7], 'x'][i % 5]), ('empilées, 25 paroles', 25, lambda i: [0.5, 0.5, 0])]
        for nom, n, f in ABIMES:
            for m in ('encre', 'mascaret'):
                st = etat(n); S0 = json.loads(st['promi_state'])
                for i, q in enumerate(S0['promises']): q['place'] = f(i)
                st['promi_state'] = json.dumps(S0)
                ctx = B.contexte(br, sombre=True, stockage=studio(m)); pose_etat(ctx, st); pg = B.ouvre(ctx, F, attente=6500)
                pose(pg); pg.wait_for_timeout(900)
                o1, t1 = entasse_ok(pg); o2, t2 = places_ok(pg.evaluate(PLACES)); o3, t3 = reouvre(pg)
                juge('[X · %s · %s] réparées à l\'ouverture : rien d\'entassé, places valides et distinctes, stables sur trois réouvertures' % (nom, m), o1 and o2 and o3, (t1, t2, t3[:2]))
                ctx.close()
    # ── S · UNE TOILE SAINE : RIEN NE CHANGE ──
    if 'S' in PARTIES:
        for n in (5, 25):
            for m in ('encre', 'mascaret'):
                vus = {}
                for fic in (REF, F):
                    ctx = B.contexte(br, sombre=True, stockage=studio(m)); pose_etat(ctx, etat(n)); ctx.add_init_script(AMORCE); pg = B.ouvre(ctx, fic, attente=6500)   # le hasard amorcé et la vie au repos coupée DÈS le chargement (comme banc_rendu) : sans cela le même fichier donne trois images d'une ouverture à l'autre
                    pose(pg)
                    vus[fic] = (pg.evaluate(GEO), pg.evaluate(PLACES), pg.evaluate("()=>JSON.stringify(window._placesReparees||null)")); ctx.close()
                av = [[q['id'], q.get('place')] for q in json.loads(etat(n)['promi_state'])['promises'] if not q.get('draft')]
                A = {x[0]: x for x in vus[REF][0]['g']}; Bb = {x[0]: x for x in vus[F][0]['g']}
                gr = max([max(abs(A[q][1] - Bb[q][1]), abs(A[q][2] - Bb[q][2])) for q in A if q in Bb] or [0]) if set(A) == set(Bb) else 999
                juge('[S · %d paroles · %s] une Toile saine : rien réparé, les places inchangées, les graines identiques à %s (0,5 pt)' % (n, m, REF),
                     vus[F][2] == 'null' and vus[F][1] == av and gr <= 0.5, 'réparé %s · places inchangées %s · graines %.2f pt' % (vus[F][2], vus[F][1] == av, gr))
    for th in (THEMES if 'M' in PARTIES else []):
        for n in NS:
            for m in MONDES:
                ctx = B.contexte(br, sombre=(th == 'sombre'), stockage=studio(m)); pose_etat(ctx, etat(n)); pg = B.ouvre(ctx, F, q=arg('q',''))
                pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} }", m); pose(pg)
                if pg.evaluate("()=>Toile.getTheme()") != m: juge('[M · %s · %d paroles · %s] le monde est posé à l\'ouverture' % (th, n, m), False, pg.evaluate("()=>Toile.getTheme()")); ctx.close(); continue
                o, t = entasse_ok(pg); rouges = [] if o else ['à froid : ' + t]
                a = pg.evaluate(GEO)
                for pp in PAGES:
                    page(pg, pp); b = pg.evaluate(GEO); d, k = ecart(a, b)
                    if k: rouges.append('%s : %s' % (pp, d))
                    o, t = entasse_ok(pg)
                    if not o: rouges.append('%s : %s' % (pp, t))
                    a = b if not k else a
                er = [e for e in pg.erreurs if 'version.json' not in e]
                juge('[M · %s · %d paroles · %s] à froid rien d\'entassé ; sept pages ouvertes puis fermées : chaque dalle à sa place à l\'écran (1 pt)' % (th, n, m), not rouges and not er, (rouges[:2], er[:1]))
                ctx.close()
    br.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
