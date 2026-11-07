#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_haut_fiche.py — SENTINELLE PERMANENTE C-255 (Tom, 7 nov. 2026, v184a). Elle fait partie de la porte A1 de TOUS les lots.

« Sur les fiches Cercle, Promi et Chiche, il mesure la position et la présence de chaque élément du haut (en-tête, titre, ligne « Avec … », le +, la ligne
d'état) : à l'ouverture ; pendant et après un défilement vers le bas puis vers le haut ; après 10 allers-retours dans le fil ; après l'ajout d'un commentaire ;
après un dépliage puis un repliage ; après la fermeture puis la réouverture de la fiche. Tout écart avec la position d'ouverture, une fois revenu en haut, fait
échouer le juge. Il est jugé dans Safari iOS avec un défilement tactile, aux échelles 1 et 0,79. »

POURQUOI LES JUGES D'AVANT ÉTAIENT VERTS (C-252, C-243, « collés sous la marge ») : ils faisaient défiler en ÉCRIVANT `scrollTop` puis attendaient 1,5 s au repos.
Écrire `scrollTop` ne fait ni élan, ni rebond, ni défilement asynchrone : la fiche ne changeait jamais de hauteur PENDANT un geste, et l'attente laissait la pose
réparer ce que le doigt aurait laissé. Ici le défilement est NATIF : la molette de WebKit (le défilement que le moteur fait lui-même, asynchrone, image par
image) ; et dans Safari iOS, le doigt (banc-haut-fiche.html, glissés du simulateur). L'enregistreur (haut-fiche-rec.js) relève CHAQUE IMAGE et juge les sauts
pendant le geste, pas seulement le repos.

Usage : python3 redteam_haut_fiche.py [--fichier=app.html] [--nature=cercle|promi|chiche] [--echelle=1|0,79] [--vite]
"""
import sys, json, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = A.get('fichier', 'app.html'); VITE = '--vite' in sys.argv
NAT = [A['nature']] if 'nature' in A else ['cercle', 'promi', 'chiche']
ECH = [A['echelle']] if 'echelle' in A else ['1', '0,79']
TAILLE = {'1': (430, 932), '0,79': (330, 714)}
REC = io.open('haut-fiche-rec.js', encoding='utf-8').read()
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %s  %s' % ('OK' if ok else 'KO', nom, str(d)[:260]), flush=True)

def contexte(b, vw, vh, stockage):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)   # is_mobile=False : la molette (le défilement natif de WebKit) n'existe pas en « mobile »
    s = "try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}"
    s += "try{ if(!sessionStorage.getItem('__hf')){ sessionStorage.setItem('__hf','1'); localStorage.clear(); var E=%s; for(var k in E) localStorage.setItem(k,E[k]);" % json.dumps(stockage)
    s += " localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_veille_off','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_rappel_fin','1'); } }catch(e){}"
    ctx.add_init_script(s); return ctx

def stockage(nature):
    if nature == 'cercle':
        st = json.load(io.open('banc-etats/etat-cercle.json', encoding='utf-8')); st.pop('promi_theme', None); return st
    d = B.etat_tom(); return {k: v for k, v in (d.get('ls') or {}).items() if k not in ('setItem', 'getItem', 'removeItem', 'clear', 'key', 'length')}

OUVRE = {
  'cercle': "()=>{ openEssaim('potager'); return 'potager'; }",
  'promi':  "()=>{ const p=promises.filter(q=>!q.draft&&!q.chiche&&!q.nuee).sort((a,b)=>(b.title||'').length-(a.title||'').length)[0]; openDetail(p.id); return p.title.slice(0,20); }",
  'chiche': "()=>{ const p=promises.filter(q=>!q.draft&&q.chiche)[0]; openDetail(p.id); return p.title.slice(0,20); }",
}

def roule(pg, dy, pas=40, ms=16):
    """défilement NATIF (molette WebKit) de dy pt de l'appareil, par pas réguliers — le moteur défile lui-même, image par image"""
    X, Y = B.pt(pg, 195, 560); pg.mouse.move(X, Y); k = B.dev(pg)[4]
    n = max(1, int(abs(dy) / pas)); s = (1 if dy > 0 else -1) * pas * k
    for _ in range(n): pg.mouse.wheel(0, s); pg.wait_for_timeout(ms)

def st(pg): return pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
def max_st(pg): return pg.evaluate("()=>{const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight;}")

def aller_retour(pg, nat, vite_px=40):
    """du haut jusqu'en bas puis retour, enregistré image par image ; rend le jugement des sauts"""
    m = max_st(pg)
    pg.evaluate("()=>HF.start()")
    roule(pg, m + 60, pas=vite_px); pg.wait_for_timeout(250)
    roule(pg, -(m + 60), pas=vite_px); pg.wait_for_timeout(700)
    fr = pg.evaluate("()=>HF.stop()")
    return pg.evaluate("([f,n])=>HF.sauts(f,n)", [fr, nat]), m

def repos(pg): pg.wait_for_timeout(500); return pg.evaluate("()=>HF.releve()")
def ecart(pg, o, nat): return pg.evaluate("([o,n])=>HF.compare(o,HF.releve(),n)", [o, nat])

if '--lire' in sys.argv:
    # Safari iOS : ce que banc-haut-fiche.html a envoyé au Mac (le défilement au doigt dans le simulateur ou sur l'iPhone)
    L = [json.loads(l) for l in io.open('mesures/appareil.jsonl', encoding='utf-8') if '"haut-fiche"' in l]
    fins = {}
    for d in L:
        if d.get('fin'): fins[d['nature']] = d
    for nat, d in sorted(fins.items()):
        T = '[Safari iOS · %s · échelle %.3f · %s]' % (nat, d.get('echelle') or 0, (d.get('version') or {}).get('commit', '?') if isinstance(d.get('version'), dict) else d.get('version'))
        for c in d['cas']:
            if 'sauts' in c['cas']: juge('%s %s : %d images au doigt, défilé jusqu\'à %.0f pt, aucun saut' % (T, c['cas'], c['images'], c.get('max', 0)), c['n'] == 0 and c['images'] > 30 and c.get('max', 0) > 40, c['defauts'][:3] or ('pire %.2f pt' % c['pire']['v']))
            else: juge('%s %s : tout à sa place d\'ouverture' % (T, c['cas']), not c.get('ecart') and not c.get('erreur'), c.get('ecart') or c.get('erreur') or '')
    if not fins: juge('Safari iOS : aucun bilan reçu', False)
    print('\n%d / %d' % (sum(res), len(res))); sys.exit(0 if res and all(res) else 1)

with sync_playwright() as p:
    b = p.webkit.launch()
    for ech in ECH:
        vw, vh = TAILLE[ech]
        for nat in NAT:
            T = '[%s ×%s]' % (nat, ech)
            ctx = contexte(b, vw, vh, stockage(nat)); pg = B.ouvre(ctx, F); pg.evaluate(REC)
            qui = pg.evaluate(OUVRE[nat]); pg.wait_for_timeout(2600)
            O = repos(pg)
            pres = [c for c in ('tete', 'qui', 'titre', 'etat') + (('plus',) if nat == 'cercle' else ()) if not (O.get(c) and O[c][1])]
            juge('%s ouverture (%s) : en-tête, %s, titre, état%s présents' % (T, qui, 'ligne « Avec … »' if nat == 'cercle' else 'phrase', ', le +' if nat == 'cercle' else ''), not pres and (nat != 'cercle' or O['quiTx'].startswith('Avec ')), pres or O['quiTx'])
            juge('%s ouverture : barre Peaufiner au bas de l\'écran (760)' % T, O['barre'] and abs(O['barre'][0] - 760) <= 0.5, O['barre'])
            # 2 · défilement bas puis haut
            S, m = aller_retour(pg, nat)
            juge('%s défilement natif bas → haut (%d pt, %d images) : aucun saut, en-tête et barre immobiles' % (T, m, S['images']), S['n'] == 0, S['defauts'] or ('pire %.2f pt' % S['pire']['v']))
            e = ecart(pg, O, nat); juge('%s revenu en haut : chaque élément à sa place d\'ouverture, présent' % T, not e, e)
            # 3 · dix allers-retours (deux vitesses : un doigt lent, un doigt vif)
            n_s, n_e, det = 0, 0, []
            for i in range(3 if VITE else 10):
                S, _ = aller_retour(pg, nat, vite_px=(25 if i % 2 else 90))
                e = ecart(pg, O, nat); n_s += 1 if S['n'] else 0; n_e += 1 if e else 0
                if (S['n'] or e) and len(det) < 3: det.append([i, S['defauts'][:2], e])
            juge('%s %d allers-retours : aucun saut, tout à sa place à chaque retour' % (T, 3 if VITE else 10), n_s == 0 and n_e == 0, det)
            # 4 · un commentaire, par la vraie saisie
            pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=d.scrollHeight; }"); pg.wait_for_timeout(500)
            r = B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(500)
            ok_s = pg.evaluate("()=>!!(document.activeElement && document.activeElement.classList.contains('cm5-saisie'))")
            if ok_s: pg.keyboard.type('un mot du juge'); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
            pg.evaluate("()=>{ document.activeElement && document.activeElement.blur && document.activeElement.blur(); }"); pg.wait_for_timeout(600)
            roule(pg, -(max_st(pg) + 100)); pg.wait_for_timeout(900)
            e = ecart(pg, O, nat); juge('%s un commentaire ajouté (saisie %s), revenu en haut : rien n\'a bougé' % (T, 'ouverte' if ok_s else 'NON ouverte'), ok_s and not e, e)
            # 5 · dépliage puis repliage du titre (au doigt)
            coupe = pg.evaluate("()=>!!document.querySelector('#dptTitre[data-coupe]')")
            B.tap_sel(pg, '#dptTitre'); pg.wait_for_timeout(900)
            dep = pg.evaluate("()=>!!window._titreDeplie")
            if dep: S, _ = aller_retour(pg, nat)
            B.tap_sel(pg, '#dptTitre'); pg.wait_for_timeout(1100)
            pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); if(d.scrollTop) d.scrollTop=0; }"); pg.wait_for_timeout(500)
            e = ecart(pg, O, nat); juge('%s dépliage (%s) puis repliage : tout à sa place d\'ouverture' % (T, 'déplié' if dep else ('titre entier : rien à déplier' if not coupe else 'NON déplié')), not e and (dep or not coupe), e)
            # 6 · fermer (le X, au doigt) puis rouvrir
            B.tap_sel(pg, '#detailPoster > .enh .closeb'); pg.wait_for_timeout(900)
            ferme = pg.evaluate("()=>!document.getElementById('detailPoster').classList.contains('show')")
            if not ferme: pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(700)
            pg.evaluate(OUVRE[nat]); pg.wait_for_timeout(2600)
            e = ecart(pg, O, nat); juge('%s fermée (X %s) puis rouverte : tout à sa place d\'ouverture' % (T, 'au doigt' if ferme else 'par script'), not e, e)
            S, _ = aller_retour(pg, nat); e = ecart(pg, O, nat)
            juge('%s rouverte, un aller-retour de plus : aucun saut, tout à sa place' % T, S['n'] == 0 and not e, (S['defauts'][:3], e))
            if pg.erreurs: juge('%s aucune erreur de page' % T, False, pg.erreurs[:3])
            ctx.close()
    b.close()
print('\n%d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
