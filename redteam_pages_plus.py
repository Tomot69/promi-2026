#!/usr/bin/env python3
"""
redteam_pages_plus.py — v150 (Tom, 18 oct. 2026) : LES PAGES +, AU POINT, CONTRE v149 SERVIE À CÔTÉ. Banc comme Tom (WebKit, 390 × 844 ×3), clair et sombre.

  C-157 · « Pages + seulement : le texte « TRACE POUR PLANTER » (Promi) et celui qui contient « LANCER » (Chiche) descendent de 6 à 9 pt pour s'aligner
          sur la flèche, et se décalent de 3 pt vers la droite. NE TOUCHE PAS AUX FICHES. »
          → le mot du trait : +6 à +9 pt en y, +3 pt (± 0,5) en x, Promi et Chiche ; le Cercle ne bouge pas.
          → les fiches (Promi, Chiche) : sous le haut de l'onde, l'image est IDENTIQUE AU PIXEL à v149 (même hasard, même heure) — hors des 3 pt du bord de
            l'appareil, au-dessus de ses coins arrondis du bas (800 pt ; la barre Peaufiner comprise) et à un niveau près : v149 contre ELLE-MÊME diffère
            de 9 à 12 pixels, d'un seul niveau, sur la colonne du bord et dans les coins (le bruit du rendu).
  ⚑ v164b : `?trait=` est retiré (×1,3 figé) — le trait est neutralisé par `window.__TRAIT_BANC=1`, posé avant la page.
  ⚑ v163 (C-184) : la version jugée est servie sous `?trait=1` — le trait plus épais et ce qui descend sous son mot (le pas du trait) sont jugés par
          redteam_trait_k ; ici tout le reste se compare à v149. Original : *-avant-v163.py.
  C-149 · « Garder de côté » 4 pt plus bas (± 0,5), dans les trois pages + ; l'inclinaison ne change pas.
          ⚑ v151 (Tom) : « encore 1 mm (6 pt) plus bas » — 10 pt plus bas que v149 (± 0,5).
  C-157 · ⚑ v151 (Tom) : « TRACE POUR PLANTER / TRACE POUR LANCER passe en orange #FB4C0D, comme la flèche, en clair et en sombre » — les trois pages +
          (le Cercle porte le même texte) ; les fiches ne bougent pas (le contrôle au pixel ci-dessus). Original : sauvegardes/redteam_pages_plus-avant-v151.py.
  C-158 · « Page + du Chiche : seule la phrase remonte de 10 pt ; le choix du trait et « Garder de côté » ne bougent pas. Page + du Cercle : sa phrase prend
          EXACTEMENT la même hauteur et le même placement que celle du Chiche après ce déplacement. »
          → la phrase du Chiche : −10 pt (± 0,5) ; le rail du pinceau : inchangé (± 0,5) ; le trait (la base de l'onde) : inchangé ;
          → la phrase du Cercle : l'encre de sa première ligne à la hauteur de celle du Chiche (± 0,5), même boîte à gauche (la première ligne d'un Chiche,
            « à qui ose ? », commence en retrait par dessin) ; son rail et son trait inchangés ;
          → la phrase du Promi, son rail et son trait : inchangés.
  LA BASCULE (trouvée en composant la capture, v150) : sur dix ouvertures de la page + d'un Chiche (phrase tirée au hasard), le mot du trait et la phrase
          sont posés pour le nombre de lignes que la phrase a VRAIMENT (le mot à base + 38,5, la phrase à base + 92) — avant, une phrase dont la taille
          faisait basculer le nombre de lignes laissait le mot d'une composition sur les points de l'autre (v149 : 1 fois sur 8 ; v150 avant correction : 3).
Le hasard est semé à l'identique dans les deux pages (les suggestions de la phrase sont tirées au hasard). Preuve : `--fichier=zz-av149.html` rougit.
"""
import io, os, sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = 'zz-av149.html'
if not os.path.exists(REF): os.system('git show 3d032b8:app.html > %s' % REF)
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
SEME = """(function(){ var s=20261018; Math.random=function(){ s|=0; s=s+0x6D2B79F5|0; var t=Math.imul(s^s>>>15,1|s); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; })();"""
LIT = r"""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const cs=document.getElementById('createSheet');
  const bx=e=>{ if(!e) return null; const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden') return null; const r=e.getBoundingClientRect(); if(!r.width) return null; return [(r.left-D.left)/k, (r.top-D.top)/k, (r.right-D.left)/k, (r.bottom-D.top)/k]; };
  const ph=[...cs.querySelectorAll('#csPhrase, #nueePhrase')].find(e=>getComputedStyle(e).display!=='none' && e.getBoundingClientRect().height>0), tx=ph&&ph.querySelector('.ph-txt');
  let l1=null; if(tx){ const rg=document.createRange(); rg.selectNodeContents(tx); const q=[...rg.getClientRects()].filter(r=>r.width>1).sort((a,b)=>a.top-b.top)[0]; if(q) l1=[(q.left-D.left)/k, (q.top-D.top)/k]; }
  const g=cs.querySelector('.pp-garder'), m=g?(getComputedStyle(g).transform.match(/matrix\(([^)]+)\)/)):null;
  return {texte:tx?tx.textContent:null, l1:l1, boite:bx(ph), trace:bx(cs.querySelector('.pp-trace')), rail:bx(document.getElementById('csPinceau')), garder:g?[g.offsetLeft, g.offsetTop]:null,
    penche:m?+(-Math.atan(+m[1].split(',')[2])*180/Math.PI).toFixed(2):0, ink:(function(e){ if(!e) return null; const rg=document.createRange(); rg.selectNodeContents(e); const q=[...rg.getClientRects()].filter(r=>r.width>1); return q.length?[Math.min(...q.map(r=>r.top)), Math.max(...q.map(r=>r.bottom))].map(v=>(v-D.top)/k):null; })(ph), garder_ink:(function(e){ if(!e) return null; const rg=document.createRange(); rg.selectNodeContents(e); const q=[...rg.getClientRects()].filter(r=>r.width>1); return q.length?[Math.min(...q.map(r=>r.top)), Math.max(...q.map(r=>r.bottom))].map(v=>(v-D.top)/k):null; })(g), barre:(function(){ const e=document.getElementById('csBotBar'); return e?(e.getBoundingClientRect().top-D.top)/k:null; })(), col:(cs.querySelector('.pp-trace')?getComputedStyle(cs.querySelector('.pp-trace')).webkitTextFillColor:null), base:(window._ppEcran&&_ppEcran())?_ppEcran().base:null}; }"""
def page_plus(b, fichier, nat, sombre):
    ctx = B.contexte(b, sombre=sombre); ctx.add_init_script(SEME); ctx.add_init_script('window.__TRAIT_BANC=1;' if fichier == F else ''); pg = B.ouvre(ctx, fichier)   # ⚑ v163 (C-184) : le trait neutralisé (son pas, et ce qui descend sous lui, sont jugés par redteam_trait_k)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2800)
    r = pg.evaluate(LIT); ctx.close(); return r
def fiche(b, fichier, nature, sombre):
    ctx = B.contexte(b, sombre=sombre); ctx.add_init_script(SEME); ctx.add_init_script('window.__TRAIT_BANC=1;' if fichier == F else ''); pg = B.ouvre(ctx, fichier)   # ⚑ v163 (C-184) : le trait neutralisé (son pas, et ce qui descend sous lui, sont jugés par redteam_trait_k)
    B.plante(pg, 'rendre le livre', qui='Marion', nature=nature)
    pg.evaluate("()=>{ window._TRAIT_K=1; closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3200)   # ⚑ v162 (C-184) : le trait × 1,05 est voulu (son juge : redteam_trait_105) — ici on le neutralise pour juger tout le reste contre v149
    t = pg.evaluate("()=>{ const v=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','); return [+v[0], +v[1]]; }")
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    ctx.close(); y0 = int((d[1] + (t[0] - t[1] - 8) * d[2]) * 3); x0 = int((d[0] + 3 * d[2]) * 3); return im.crop((x0, y0, x0 + int(384 * d[2] * 3), int((d[1] + 800 * d[2]) * 3))), t   # au-dessus des coins arrondis du bas de l'appareil (rayon ≈ 44 pt : leur lissage varie d'un rendu à l'autre)
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'
        A, N = {}, {}
        for n_ in ('promi', 'chiche', 'nuee'):
            # ⚑ v151 : la phrase est tirée au hasard, et le hasard semé ne suffit pas (le nombre de tirages avant l'ouverture dépend des images) — on
            #   rouvre les deux pages (quatre fois au plus) jusqu'à deux compositions comparables (même base de l'onde = autant de lignes)
            for _ in range(4):
                A[n_], N[n_] = page_plus(b, REF, n_, sombre), page_plus(b, F, n_, sombre)
                if A[n_]['base'] is not None and A[n_]['base'] == N[n_]['base']: break
        for n, nom in (('promi', 'Promi'), ('chiche', 'Chiche'), ('nuee', 'Cercle')):
            a, c = A[n], N[n]
            if not (a['trace'] and c['trace'] and a['l1'] and c['l1'] and a['rail'] and c['rail'] and a['garder'] and c['garder']):
                juge('[%s] page + %s : tout se lit' % (T, nom), False, (a, c)); continue
            # la suggestion tirée peut différer (le tirage n'est pas tout entier dans Math.random) : les cotes ne dépendent que du nombre de lignes, que dit la base de l'onde
            juge('[%s] page + %s : même trait (base %s, autant de lignes) qu\'en v149 — la comparaison vaut' % (T, nom, c['base']), a['base'] == c['base'] and a['base'] is not None, (a['texte'][:30], c['texte'][:30], a['base'], c['base']))
            dy, dx = c['trace'][1] - a['trace'][1], c['trace'][0] - a['trace'][0]
            if n == 'nuee': juge('[%s] C-157 · page + Cercle : le mot du trait ne bouge pas' % T, abs(dy) <= 0.5 and abs(dx) <= 0.5, 'Δy %.1f · Δx %.1f' % (dy, dx))
            else: juge('[%s] C-157 · page + %s : « %s » descend de 6 à 9 pt et va 3 pt à droite' % (T, nom, (c.get('texte') and '') or 'le mot du trait'), 6 <= dy <= 9 and abs(dx - 3) <= 0.5, 'Δy %.1f · Δx %.1f' % (dy, dx))
            gy = c['garder'][1] - a['garder'][1]
            juge('[%s] C-149 · page + %s : « garder de côté » 10 pt plus bas (4 + 6), même place à droite, même inclinaison' % (T, nom), abs(gy - 10) <= 0.5 and abs(c['garder'][0] - a['garder'][0]) <= 0.5 and abs(c['penche'] - a['penche']) < 0.05, 'Δy %.1f · penché %s°' % (gy, c['penche']))
            juge('[%s] C-157 · page + %s : « %s » en orange #FB4C0D' % (T, nom, ((c.get('texte') or '') and '') or 'le mot du trait'), c.get('col') == 'rgb(251, 76, 13)', str(c.get('col')))
            ry = c['rail'][1] - a['rail'][1]
            juge('[%s] C-158 · page + %s : le choix du trait (le rail du pinceau) ne bouge pas' % (T, nom), abs(ry) <= 0.5, 'Δy %.1f' % ry)
            py = c['l1'][1] - a['l1'][1]
            if n == 'chiche': juge('[%s] C-158 · page + Chiche : la phrase remonte de 10 pt' % T, abs(py + 10) <= 0.5 and abs(c['l1'][0] - a['l1'][0]) <= 0.5, 'Δy %.1f' % py)
            elif n == 'promi': juge('[%s] page + Promi : la phrase ne bouge pas' % T, abs(py) <= 0.5, 'Δy %.1f' % py)
        if N['nuee']['l1'] and N['chiche']['l1']:
            dl = N['nuee']['l1'][1] - N['chiche']['l1'][1]
            # ⚑ v162 (Tom, C-183) : la phrase du Cercle descend de 10 pt — elle est maintenant 10 pt SOUS celle du Chiche (C-158 : à la même hauteur)
            juge('[%s] C-183 · page + Cercle : sa phrase 10 pt plus bas que celle du Chiche (l\'encre de la première ligne), même placement à gauche' % T, abs(dl - 10) <= 0.5 and N['nuee']['boite'] and N['chiche']['boite'] and abs(N['nuee']['boite'][0] - N['chiche']['boite'][0]) <= 0.5, 'Δy %.1f' % dl)
            ink = N['nuee'].get('ink'); gd = N['nuee'].get('garder_ink'); bar = N['nuee'].get('barre')
            juge('[%s] C-183 · page + Cercle : la phrase ne touche ni « Garder de côté » ni la barre du bas' % T, ink and gd and bar and ink[1] < gd[0] and ink[1] < bar,
                 'bas de la phrase %s · « Garder de côté » %s (espace %.1f pt) · barre %s (espace %.1f pt)' % (ink and ink[1], gd and gd[0], (gd[0] - ink[1]) if ink and gd else 0, bar, (bar - ink[1]) if ink and bar else 0))
        for nature, nom in ((0, 'Promi'), (1, 'Chiche')):
            ia, ta = fiche(b, REF, nature, sombre); ic, tc = fiche(b, F, nature, sombre)
            bb = ImageChops.difference(ia, ic).getbbox() if ia.size == ic.size else (0, 0, 1, 1)
            # ⚑ v155 (Tom, C-169 §4.2) : sur une fiche à moitié tracée, le départ de la seconde moitié (les 43 pt du trait avant la pointe du milieu) est
            #   ORANGE — c'est la seule différence admise, nommément : la bande du trait de 140 à 200 pt ; ailleurs, identique au pixel (original :
            #   sauvegardes/redteam_pages_plus-avant-v155.py)
            k_ = ia.size[0] / 384.0; zx0, zx1 = int((140 - 3) * k_), int((200 - 3) * k_); zy1 = int((2 * ta[1] + 30) * k_) if ta and ta[1] else 0
            n_, nz, org = 0, 0, 0
            if ia.size == ic.size:
                D_ = ImageChops.difference(ia, ic).convert('L'); W_ = ia.size[0]; pc = ic.load()
                for i_, px in enumerate(D_.getdata()):
                    if px <= 1: continue
                    x_, y_ = i_ % W_, i_ // W_
                    if zx0 <= x_ <= zx1 and y_ <= zy1:
                        nz += 1; q_ = pc[x_, y_]
                        if abs(q_[0] - 251) + abs(q_[1] - 76) + abs(q_[2] - 13) < 120: org += 1
                    else: n_ += 1
            else: n_ = -1
            juge('[%s] C-157 · la fiche %s n\'a pas bougé : du haut de l\'onde au bas de l\'écran, identique au pixel à v149 — hors du départ orange de la seconde moitié (C-169)' % (T, nom), ta == tc and n_ == 0 and nz > 0 and org >= nz * 0.4, 'trait %s/%s · %d pixel(s) différents hors du départ · %d dans le départ (%d orange) %s' % (ta, tc, n_, nz, org, bb or ''))
    # la bascule : dix ouvertures, phrase tirée au hasard (sans semer)
    faux = []
    for i in range(10):
        ctx = B.contexte(b); ctx.add_init_script('window.__TRAIT_BANC=1;'); pg = B.ouvre(ctx, F)   # v163 : le trait neutralisé
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=chiche]'); pg.wait_for_timeout(3500)
        r = pg.evaluate("""()=>{ const e=_ppEcran(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, tr=document.querySelector('#createSheet .pp-trace'), ph=document.getElementById('csPhrase');
          return [e.nl, e.base, +((tr.getBoundingClientRect().top-D.top)/k).toFixed(1), +((ph.getBoundingClientRect().top-D.top)/k).toFixed(1)]; }""")
        if abs(r[2] - (r[1] + 38.5)) > 0.6 or abs(r[3] - (r[1] + 92)) > 0.6: faux.append(r)
        ctx.close()
    juge('la bascule : sur 10 ouvertures de la page + d\'un Chiche, le mot du trait et la phrase sont posés pour le nombre de lignes réel', not faux, '%d faux %s' % (len(faux), faux[:3]))
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
