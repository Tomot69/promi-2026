#!/usr/bin/env python3
"""redteam_moi_douceur.py — ⚑ v200 (Tom, C-271 « aucun changement sec », C-269 « moi » dans la phrase : LA TRANSITION).
« L'encart en pointillés RESTE en place. L'ancien texte se DÉTRACE (tracé inversé, même système que C-125, même cadence). Pendant ce temps, l'encart s'adapte
en douceur à la largeur du nouveau mot, la suite de la phrase glisse avec lui. Puis « moi » se TRACE. Même chose dans l'autre sens et quand on ajoute une
personne. Sur les trois natures, sur la page + et sur la fiche. »
Banc comme Tom (WebKit, ×3, doigt), la vraie saisie, la page relevée À CHAQUE IMAGE (un relevé dans la page, `requestAnimationFrame`) :
page + (Promi « je promets », Chiche, Cercle) : la validation (« qui ? » / « qui ose ? » / « tout le monde » → « moi »), Rachel ajoutée (« moi » → « Rachel »),
Rachel retirée (→ « moi ») ; fiche (Promi, Chiche ; Cercle) : la phrase change (une personne ajoutée) :
  A · aucune image où le mot change d'un coup : il ne change qu'entièrement découpé (rien de lui à l'écran) à l'image d'avant ET à celle d'après ; l'ancien passe
      par un détracé (≥ 2 images, la plume du module en cours) et le nouveau par un tracé (≥ 2) ;
  B · la largeur de l'encart est continue (aucune image ne fait plus de 40 % du chemin, + 2 pt) ; sur la fiche, le titre glisse de même ;
  C · les pointillés présents à chaque image tant que personne n'est ajouté ; à l'ajout, ils partent en ≥ 3 images (le filet s'amincit), la pastille se remplit
      en flaques ; au retrait, l'inverse ;
  D · la cadence de C-125 : chaque tracé et détracé de ces mots a la durée prévue à 40 car/s (le module, sans vitesse imposée) — la durée réelle jugée au calme seulement.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,nuee').split(',')
VUE = {'1': (430, 932), '0,79': (330, 714), 'tom': (390, 651)}[next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--vue=')), '1')]
res = []
def juge(nom, cond, detail=''):
    res.append(bool(cond)); print('  %s %-104s %s' % ('✅' if cond else '❌', nom, str(detail)[:320]), flush=True)
src = open('redteam_phrase_lignes.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0]; ns = {}; exec(compile(src, 'pl', 'exec'), ns)
pose, stable = ns['pose'], ns['stable']
VIDE = 'polygon(0px 0px, 0px 0px, 0px 0px)'
ENR = """a=>{ window.__fr=[]; const D=document.getElementById('device');
  (function f(){ const e=document.querySelector(a.sel); const s=D.getBoundingClientRect().width/(D.offsetWidth||390);
    if(e){ const i=a.fiche?e:(e.querySelector(':scope > .v200-mt')||e), cs=getComputedStyle(e), ci=getComputedStyle(i), cv=e.querySelector(':scope > canvas.v200-fl'), r=e.getBoundingClientRect(), ti=document.getElementById('dptTitre');
      window.__fr.push({t:performance.now(), txt:(i.textContent||'').trim(), clip:ci.clipPath||ci.webkitClipPath||'none', w:r.width/s, bs:cs.borderTopStyle, bw:parseFloat(cs.borderTopWidth)||0,
        bg:cs.backgroundColor, cv:cv?+cv.getAttribute('data-u'):null, tr:!!i.__trace, tcv:!!document.querySelector('canvas[data-trace-canevas]'), ti:ti?ti.getBoundingClientRect().top/s:null}); }
    if(window.__fr.length<5000 && !window.__frStop) requestAnimationFrame(f); })(); }"""
def stop(pg): pg.evaluate("()=>{ window.__frStop=true; }"); fr = pg.evaluate("()=>window.__fr"); pg.evaluate("()=>{ window.__frStop=false; }"); return fr
def cache(c): return c == VIDE or c.replace(' ', '') == VIDE.replace(' ', '')
def partiel(c): return c not in ('none', '') and not cache(c)
def juge_seq(T, fr, de, vers, vide_avant, vide_apres, fiche=False):
    if not fr: juge(T + ' relevé', False, 'aucune image'); return
    txts = [f['txt'] for f in fr]
    nz = lambda s: s.replace('\u202f', ' ').replace('\xa0', ' ').strip(', ')
    juge(T + ' : départ « %s », arrivée « %s »' % (de, vers), nz(txts[0]) == nz(de) and nz(txts[-1]) == nz(vers), '%s → %s' % (txts[0], txts[-1]))
    sauts = []; ip = None
    for i in range(1, len(fr)):
        if fr[i]['txt'] != fr[i - 1]['txt']:
            ip = i
            if not (cache(fr[i]['clip']) and cache(fr[i - 1]['clip'])): sauts.append((round(fr[i]['t'] - fr[0]['t']), fr[i - 1]['txt'], fr[i]['txt'], fr[i - 1]['clip'][:14], fr[i]['clip'][:14]))
    det = sum(1 for f in fr[:ip or 0] if f['tr']); tra = sum(1 for f in fr[ip or 0:] if f['tr'])   # le tracé en cours (sa plume) : la découpe ou le canevas du module
    juge(T + ' A · le mot ne change jamais d\'un coup (découpé tout entier de part et d\'autre) ; détracé puis tracé', not sauts and det >= 2 and tra >= 2, 'sauts %s · détracé %d images · tracé %d' % (sauts[:2], det, tra))
    if not fiche:
        ws = [f['w'] for f in fr]; tot = abs(ws[-1] - ws[0])
        pas = [(round(abs(ws[i] - ws[i - 1]), 1), round(fr[i]['t'] - fr[i - 1]['t'])) for i in range(1, len(ws))]
        if os.environ.get("DBG"): print([(round(f["t"]-fr[0]["t"]), round(f["w"],1), f["txt"], f["tr"], f["bw"]) for f in fr][:60])
        trop = [x for x in pas if x[0] > tot * min(1, x[1] / 110.0) + 2]   # à la vitesse : un pas d'image ne fait jamais plus que 110 ms de chemin (le plus rapide : 320 ms, la courbe douce culmine à ~1,6 × la vitesse moyenne)
        juge(T + ' B · la largeur de l\'encart est continue (à la vitesse : ≤ le chemin de 110 ms par image)', not trop, '%.1f → %.1f pt · pas trop grands %s · plus grand %s' % (ws[0], ws[-1], trop[:3], max(pas) if pas else None))
    else:
        fi = [f for f in fr if f['ti'] is not None]; tot = abs(fi[-1]['ti'] - fi[0]['ti']) if fi else 0
        trop = [(round(abs(fi[i]['ti'] - fi[i - 1]['ti']), 1), round(fi[i]['t'] - fi[i - 1]['t'])) for i in range(1, len(fi)) if abs(fi[i]['ti'] - fi[i - 1]['ti']) > tot * min(1, (fi[i]['t'] - fi[i - 1]['t']) / 110.0) + 2]
        juge(T + ' B · le titre glisse à sa nouvelle place (à la vitesse)', not trop, 'titre %.1f → %.1f pt · pas trop grands %s' % (fi[0]['ti'] if fi else 0, fi[-1]['ti'] if fi else 0, trop[:3]))
        return
    if vide_avant and vide_apres:
        pas = [f for f in fr if not (f['bs'] == 'dashed' and abs(f['bw'] - 3) < 0.05)]
        juge(T + ' C · les pointillés là, entiers, à chaque image', not pas, '%d images sans eux %s' % (len(pas), pas[:1]))
    elif vide_avant != vide_apres:
        bws = sorted(set(round(f['bw'], 2) for f in fr if 0.05 < f['bw'] < 2.95)); cvs = sorted(set(round(f['cv'], 2) for f in fr if f['cv'] is not None and 0 < f['cv'] < 1))
        net = [f for f in fr if (f['bs'] != 'dashed' and f['bw'] > 0.05)]
        juge(T + ' C · les pointillés %s en douceur (le filet ≥ 3 épaisseurs entre 0 et 3 px) et la pastille %s en flaques (≥ 3 images)' % ('partent' if vide_avant else 'reviennent', 'se remplit' if vide_avant else 'se vide'),
             len(bws) >= 3 and len(cvs) >= 3 and not net, 'filet %s · flaques %s' % (bws[:6], cvs[:6]))
def juge_cadence(pg, T):
    j = pg.evaluate("()=>(window.TraceLettres&&TraceLettres.journal||[]).filter(e=>e.type==='trace-fin'||e.quoi==='trace-fin'||(e.prevu!=null&&e.reel!=null)).slice(-30)")
    cal = B.charge() < 4
    mauvais = [e for e in j if e.get('reel') and e.get('prevu') and not (0.7 <= e['reel'] / max(1, e['prevu']) <= 2.5)]
    if cal: juge(T + ' D · la cadence de C-125 (durée réelle 0,7 à 2,5 × la prévue, à 40 car/s)', j and not mauvais, '%d tracés · hors cadence %s' % (len(j), mauvais[:2]))
    else: print('  ·  %s D · cadence NON JUGÉE (charge %.1f)' % (T, B.charge()))
def page(b, k, t):
    ctx = B.contexte(b, vw=VUE[0], vh=VUE[1]); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ Math.random=(function(){ let s=7; return ()=>{ s=(s*16807)%2147483647; return (s-1)/2147483646; }; })(); }")
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600)
    if k == 'promi': B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(900)
    return ctx, pg
ATT = {'promi': 'qui ?', 'chiche': 'qui ose ?', 'nuee': 'tout le monde'}
with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_moi_douceur — %s, vue %s, charge %.1f' % (F, VUE, B.charge()), flush=True)
    for k in NATS:
        sel = '#nueePhrase .ph-m[data-np="avec"]' if k == 'nuee' else '#csPhrase .ph-m[data-ph="qui"]'; T = '[page + · %s]' % k
        ctx, pg = page(b, k, 'lire un livre'); a = {'sel': sel}
        pg.evaluate(ENR, a); pose(pg, k, 'lire un livre'); stable(pg, k)
        for _ in range(60):
            if pg.evaluate("()=>{ try{ return _ppInvite.etat().visible; }catch(e){ return false; } }"): break
            pg.wait_for_timeout(200)
        pg.wait_for_timeout(2500); fr = stop(pg)
        i0 = next((i for i, f in enumerate(fr) if f['txt'] != fr[0]['txt'] or f['tr'] or partiel(f['clip'])), 0); fr = fr[max(0, i0 - 2):]
        juge_seq(T + ' validation', fr, ATT[k].replace(' ', ' '), 'moi', True, True)
        B.tap_sel(pg, sel); pg.wait_for_timeout(1300); pg.evaluate(ENR, a)
        B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(2500); fr = stop(pg)
        i0 = next((i for i, f in enumerate(fr) if f['txt'] != fr[0]['txt'] or f['tr'] or partiel(f['clip'])), 0); fr = fr[max(0, i0 - 2):]
        juge_seq(T + ' Rachel ajoutée', fr, 'moi', 'Rachel', True, False)
        pg.evaluate(ENR, a); B.tap_sel(pg, '#createSheet .gn .gn-liste .ph-o.on[data-v="Rachel"] .ppo-x'); pg.wait_for_timeout(2600); fr = stop(pg)
        i0 = next((i for i, f in enumerate(fr) if f['txt'] != fr[0]['txt'] or f['tr'] or partiel(f['clip'])), 0); fr = fr[max(0, i0 - 2):]
        juge_seq(T + ' Rachel retirée', fr, 'Rachel', 'moi', False, True)
        juge_cadence(pg, T)
        err = [x for x in pg.erreurs if 'version.json' not in x]; juge(T + ' aucune erreur de page', not err, err[:2]); ctx.close()
    # LA FICHE : la phrase change (une personne ajoutée, par l'écrivain de la fiche)
    for k in [n for n in NATS if n in ('promi', 'chiche')]:
        T = '[fiche · %s]' % k; ctx = B.contexte(b, vw=VUE[0], vh=VUE[1]); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
        pid = pg.evaluate("k=>{ const p=promises.find(x=>x.status==='encours' && !x.draft && (k==='chiche'?true:!x.chiche)); p.who='moi'; delete p.parts; if(k==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } else { p.chiche=false; } closeAll(); openDetail(p.id); return p.id; }", k)
        pg.wait_for_timeout(3000); de = pg.evaluate("()=>document.getElementById('dptQui').textContent.trim()")
        pg.evaluate(ENR, {'sel': '#dptQui', 'fiche': True})
        pg.evaluate("i=>{ const p=promises.find(x=>x.id===i); p.who='Rachel'; window._fichePose && _fichePose(); }", pid); pg.wait_for_timeout(2600); fr = stop(pg)
        vers = pg.evaluate("()=>document.getElementById('dptQui').textContent.trim()")
        i0 = next((i for i, f in enumerate(fr) if f['txt'] != fr[0]['txt'] or f['tr'] or partiel(f['clip'])), 0); fr = fr[max(0, i0 - 2):]
        juge(T + ' la phrase a changé (« %s » → « %s »)' % (de, vers), de != vers and 'Rachel' in vers, '')
        juge_seq(T + ' Rachel ajoutée', fr, de, vers, False, False, fiche=True)
        err = [x for x in pg.erreurs if 'version.json' not in x]; juge(T + ' aucune erreur de page', not err, err[:2]); ctx.close()
    b.close()
ok = sum(res); print('\n  %s %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
