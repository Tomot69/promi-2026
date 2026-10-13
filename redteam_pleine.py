#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_pleine.py — SUR UNE TOILE REMPLIE, RIEN D'AUTRE QUE LA TOILE NE TRAVAILLE PENDANT QU'UNE DALLE ARRIVE OU PART (v145, Tom, 13 oct. 2026 — C-112, RÉCIDIVE).

« Ça saccade toujours partout », en plantant comme en retirant. LA CAUSE (mesurée sur 25 paroles relues de la sauvegarde ; le juge de v144,
`redteam_evol`, plantait trois paroles sur une Toile vide et ne pouvait pas la voir) : à chaque plantation, `syncAll` repeignait les vignettes du
Fil et de l'Index FERMÉS ; la dalle qui grandit change de cellule à chaque image, sa vignette n'était jamais « prête » : 25 passages de 41 à
67 ms, 48 rendus de dalle, 1,2 s de travail pendant l'apparition — puis leurs canevas relus d'une traite (`_teinterFil`, jusqu'à 780 ms).

Par banc_tom (WebKit, 390 × 844 @3x), Toile de 25 paroles (banc-etats/etat-25.json, relue à l'ouverture comme sur un téléphone), sous trois mondes,
planter puis retirer une parole par les vrais boutons :
  A · PENDANT LE MOUVEMENT (du toucher à la Toile posée), aucun passage des vignettes ne RENd une dalle, et aucun rendu de dalle n'est demandé
      hors du moteur — un COMPTE, qui ne dépend pas de la charge de la machine (v144 : 40 à 50 rendus) ;
  B · la passe de teinte du Fil ne tourne pas quand le Fil est fermé ;
  C · le Fil et l'Index, ouverts ENSUITE, sont à jour : la parole plantée y est, sa vignette est peinte (C-049 tient) ;
  D · le travail : aucun rappel hors de la boucle du moteur au-delà de 20 ms pendant le mouvement (valeur décidée) ;
  E · les images : au plus 3 images au-delà de 33,4 ms (deux images) du toucher à la fin du mouvement (v144 : 18 à 47) ; les images de 20 à
      33,4 ms sont COMPTÉES et affichées (la cible de Tom est zéro ; le banc au repos en donne 0 à 2 par 3,5 s).
  D et E sont des DURÉES : jugées seulement machine au calme (charge < 4 avant ET après) ; sinon elles sont affichées « non jugé ».
Rouge sur v144 (servie sur un autre port : --port=8762).     Usage : python3 redteam_pleine.py [fichier.html] [--mondes=encre,touffe,ritournelle] [--n=25] [--port=8752]
"""
import sys, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
MONDES = arg('mondes', 'encre,touffe,ritournelle').split(','); N = int(arg('n', '25')); PORT = arg('port', '8752')
TRAVAIL_MAX, DEUX_IMAGES, LONGUES_MAX, CALME = 20.0, 33.4, 3, 4.0
PROF = re.search(r'PROF = r"""(.*?)"""', io.open('redteam_evol.py', encoding='utf-8').read(), re.S).group(1)
# le compteur des rendus de dalle et des passages de vignettes (posé une fois la page chargée)
COMPTE = r"""()=>{ window.__pm=[]; window.__rd=[]; window.__tf=0; var f=window.peintMinis, g=window._rendDalle, h=window._teinterFil;
  window.peintMinis=function(r){ var n0=window.__rd.length, t=performance.now(), x=f.apply(this,arguments); window.__pm.push([t, performance.now()-t, window.__rd.length-n0]); return x; };
  if(g) window._rendDalle=function(id,w,h_,o){ var pret=false; try{ pret=!!g.call(this,id,w,h_,{siPret:1}); }catch(e){} if(o&&o.siPret) return g.apply(this,arguments);
    var t=performance.now(), x=g.apply(this,arguments), d=performance.now()-t; if(!pret && d>=3) window.__rd.push([t, d, id]); return x; };   /* un vrai rendu : la dalle n'était pas prête ET l'appel a coûté (un appel qui rend la main sans rien peindre ne compte pas) */
  if(h) window._teinterFil=function(){ window.__tf++; return h.apply(this,arguments); }; }"""
res = []
def juge(nom, cond, detail=''):
    res.append((nom, cond)); print('%s  %s  %s' % ('OK' if cond else ('··' if cond is None else 'KO'), nom, detail), flush=True)
def releve(pg):
    r = pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice(),pm:window.__pm,rd:window.__rd,tf:window.__tf})"); t0 = r['t0']
    P = [(e[0] - t0, e[1], e[2]) for e in r['P'] if 0 <= e[0] - t0 <= 3500]
    eng = [e[0] for e in P if 'image | frame' in e[2]]; fin = max(1600.0, (max(eng) + 20) if eng else 1600.0)      # la fin du mouvement : la dernière image du moteur
    I = [(r['F'][i] - t0, r['F'][i + 1] - r['F'][i]) for i in range(len(r['F']) - 1) if 0 <= r['F'][i] - t0 <= fin]
    hors = [e for e in P if e[0] <= fin and 'image | frame' not in e[2] and not (e[0] < 60 and 'écouteur' in e[2])]
    rd = [x for x in r['rd'] if 0 <= x[0] - t0 <= fin]; pm = [x for x in r['pm'] if 0 <= x[0] - t0 <= fin and x[2] > 0]
    return {'fin': fin, 'I': I, 'hors': hors, 'rd': rd, 'pm': pm, 'tf': r['tf']}
def controle(m, quoi, R, calme):
    juge('A · [%s, %s] pendant le mouvement, aucun rendu de dalle hors du moteur, aucun passage de vignettes qui rend' % (m, quoi), len(R['rd']) == 0 and len(R['pm']) == 0,
         '%d rendu(s) de dalle (%.0f ms en tout) · %d passage(s) de vignettes qui rendent · mouvement fini à %d ms' % (len(R['rd']), sum(x[1] for x in R['rd']), len(R['pm']), R['fin']))
    juge('B · [%s, %s] la passe de teinte du Fil ne tourne pas (Fil fermé)' % (m, quoi), R['tf'] == 0, '%d appel(s)' % R['tf'])
    pire = max(R['hors'], key=lambda e: e[1]) if R['hors'] else (0, 0, '')
    lg = [x for x in R['I'] if x[1] > DEUX_IMAGES]; m20 = [x for x in R['I'] if x[1] > 20]
    juge('D · [%s, %s] aucun rappel hors du moteur au-delà de %d ms pendant le mouvement' % (m, quoi, TRAVAIL_MAX), (pire[1] <= TRAVAIL_MAX) if calme else None, '%s le plus long %.1f ms à %d ms (%s)' % ('' if calme else 'NON JUGÉ, machine chargée ·', pire[1], pire[0], pire[2][:60]))
    juge('E · [%s, %s] au plus %d images au-delà de %.1f ms pendant le mouvement' % (m, quoi, LONGUES_MAX, DEUX_IMAGES), (len(lg) <= LONGUES_MAX) if calme else None,
         '%s%d image(s) au-delà de 33,4 ms (la plus longue %.0f ms) · %d au-delà de 20 ms sur %d' % ('' if calme else 'NON JUGÉ, machine chargée · ', len(lg), max([x[1] for x in R['I']] or [0]), len(m20), len(R['I'])))
with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MONDES:
        c0 = B.charge(); ctx = B.contexte(b); B.toile_pleine(ctx, N); ctx.add_init_script(PROF)
        pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500)
        pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(4500); pg.evaluate(COMPTE)
        n0 = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{document.getElementById('fTitle').value='tenir bon';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
        pg.evaluate("()=>{ window.__pm.length=0; window.__rd.length=0; window.__tf=0; window.__Pon(true); window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(4200)
        R1 = releve(pg); n1 = pg.evaluate("()=>promises.filter(p=>!p.draft).length"); c1 = B.charge()
        juge('· [%s] la Toile porte %d paroles, la plantation en ajoute une' % (m, N), n0 == N and n1 == N + 1, '%d → %d' % (n0, n1))
        controle(m, 'planter', R1, max(c0, c1) < CALME)
        # C · le Fil puis l'Index, ouverts ensuite, sont à jour
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(2500)
        B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(3500)
        fil = pg.evaluate("""()=>{ var fv=document.getElementById('feedView'), fl=document.getElementById('feedList'), ouvert=!!(fv && (fv.classList.contains('in')||fv.classList.contains('show')));
            var B=[...fl.querySelectorAll('.s4-carte, .s4-bandeau, .fd-item, [class*="s4-b"]')].filter(e=>/tenir bon/i.test(e.textContent)), it=B.sort((a,b)=>a.textContent.length-b.textContent.length)[0];
            if(!it) return {ouvert:ouvert, la:/tenir bon/i.test(fl.textContent), bandeau:false};
            var cv=it.querySelector('canvas'), peint=0; if(cv){ try{ var d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; for(var i=3;i<d.length;i+=40) if(d[i]>10) peint++; }catch(e){ peint=-1; } }
            return {ouvert:ouvert, la:true, bandeau:true, canevas:!!cv, peint:peint}; }""")
        juge('C · [%s] le Fil, ouvert ensuite, porte la parole plantée, sa dalle peinte' % m, bool(fil.get('ouvert')) and bool(fil.get('la')) and (not fil.get('canevas') or fil.get('peint', 0) > 20), str(fil))
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{ window.ouvrirIndex(); }"); pg.wait_for_timeout(3500)
        idx = pg.evaluate("()=>{ var L=[...document.querySelectorAll('#indexList .s4-carte')]; return {n:L.length, la:L.some(e=>/tenir bon/i.test(e.textContent))}; }")
        juge('C · [%s] l\'Index, ouvert ensuite, porte la parole plantée' % m, bool(idx.get('la')) and idx.get('n', 0) >= N + 1, str(idx))
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(3000)
        c2 = B.charge()
        pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ window.__pm.length=0; window.__rd.length=0; window.__tf=0; window.__Pon(true); window.__t0=performance.now(); }"); B.tap_sel(pg, '.v16-oui'); pg.wait_for_timeout(4200)
        R2 = releve(pg); n2 = pg.evaluate("()=>promises.filter(p=>!p.draft).length"); c3 = B.charge()
        juge('· [%s] le retrait rend %d paroles' % (m, N), n2 == N, '%d' % n2)
        controle(m, 'retirer', R2, max(c2, c3) < CALME)
        juge('aucune erreur de page [%s]' % m, not pg.erreurs, str(pg.erreurs[:2]))
        print('    (charge de la machine : %.1f → %.1f → %.1f → %.1f)' % (c0, c1, c2, c3), flush=True)
        ctx.close()
    b.close()
ok = sum(1 for r in res if r[1] is True); nj = sum(1 for r in res if r[1] is None); ko = [r[0] for r in res if r[1] is False]
print('\n%d / %d%s' % (ok, len(res) - nj, (' · %d contrôle(s) de durée NON JUGÉS (machine chargée) : à repasser au calme' % nj) if nj else ''))
if ko: print('KO :', ' · '.join(ko)[:900])
sys.exit(1 if ko else 0)
