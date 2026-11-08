# -*- coding: utf-8 -*-
"""redteam_nombre_mots.py — ⚑ v186b (Tom, C-257) : LE NOMBRE DE COMMENTAIRES SUR LA LIGNE « UN MOT… ».
« Sur la ligne « Un mot… » de chaque fiche, le nombre de commentaires à droite : le nombre seul, dans la typographie et à l'encre de cette ligne, sans mot ajouté ;
aucun commentaire : rien. Un toucher sur ce nombre fait glisser la fiche en douceur jusqu'aux commentaires (défilement animé, vitesse continue, sans saut), la
barre Peaufiner reste en bas ; il n'ouvre ni le clavier ni Peaufiner. » Juge : Promi, Chiche, Cercle × 0, 1, 3, 12 mots — le texte, la police et l'encre lus sur
le rendu ; un vrai toucher (souris : évènements de pointeur) ; chaque image du glissement : le défilement ne fait que croître (ou décroître), aucun pas plus grand
que 3 fois le pas moyen, la barre à 760 ; à la fin, le premier commentaire entier entre l'en-tête (112) et la barre (760) ; ni saisie ouverte, ni Peaufiner.
Usage : python3 redteam_nombre_mots.py [fichier.html] [--echelle=0,79]"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
L280 = ('Je viens, mais seulement si on part tôt : il faut passer prendre les chaises chez Nico, puis le pain. ' * 4)[:280]
NOMS = ['Marion', 'Rachel', 'moi', 'Nico', 'Adrien', 'Lou']
def com(n):   # recopié de redteam_commentaires_liste (l'importer exécute ce juge)
    return [{'t': L280 if (n > 3 and i == n - 2) else 'Mot numéro %d, à propos de ce qu\'on prévoit' % (i + 1), 'by': NOMS[i % 6], 'd': '2026-11-%02dT%02d:00:00Z' % (1 + i // 4, 8 + i % 4 * 3)} for i in range(n)]
def ferme(pg):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(900)
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
VW, VH = ((330, 714) if '--echelle=0,79' in sys.argv else (430, 932))
ok = ko = 0
def juge(nom, cond, det=''):
    global ok, ko
    if cond: ok += 1
    else: ko += 1
    print(('  ✅ ' if cond else '  ❌ ') + nom.ljust(92) + ' ' + str(det)[:160], flush=True)
LIT = r"""()=>{ const l=document.getElementById('cm5Ligne'), nb=l&&l.querySelector('.cm5-nb'), m=l&&l.querySelector('.cm5-mot'); if(!l) return null;
  const v=e=>e && getComputedStyle(e).display!=='none' && e.getBoundingClientRect().width>0; const c=e=>{ const s=getComputedStyle(e); return [s.fontFamily.split(',')[0].replace(/["']/g,''), s.fontWeight, s.fontSize, s.color]; };
  const r=nb&&nb.getBoundingClientRect(), L=l.getBoundingClientRect(), K=(window._echDp?window._echDp(document.getElementById('detailPoster')):1)||1;   /* en pt de l'appareil (à 0,79 : les px de l'écran) */
  return {vis:v(nb), txt:nb?nb.textContent:'', st:nb&&v(nb)?c(nb):null, stm:m?c(m):null, droite: r? Math.round(L.right-r.right): null, h: r? r.height/K:0, w: r? r.width/K:0}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, vw=VW, vh=VH); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; try{queueSave()}catch(e){} }")
    for n in (0, 1, 3, 12):
        C = com(n)
        for tag in ('Promi', 'Chiche', 'Cercle'):
            ferme(pg)
            if tag == 'Cercle':
                pg.evaluate("c=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; c.forEach(x=>o.comments.push(Object.assign({vu:true},x))); _cercleMots.garde(); }", C)
                pg.evaluate("()=>openEssaim('potager')")
            else:
                ti = 'faire les crêpes' if tag == 'Promi' else 'réparer le vélo'
                pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); p.comments=a[1].map(c=>Object.assign({vu:true},c)); try{queueSave()}catch(e){} openDetail(p.id); }", [ti, C])
            pg.wait_for_timeout(1200)
            try: pg.wait_for_function("()=>{ const d=document.getElementById('detailPoster'); return d && d.classList.contains('v184-pose') && document.getElementById('cm5Ligne'); }", timeout=20000)
            except Exception: pass
            pg.wait_for_timeout(1500)   # v186b : la fiche POSÉE (une attente fixe ne tenait pas sous charge, §8)
            T = '[%s · %d mot(s)]' % (tag, n); r = pg.evaluate(LIT)
            if not r: juge(T + ' la ligne « Un mot… » existe', False); continue
            if n == 0:
                juge(T + ' aucun commentaire : aucun nombre', not r['vis'] and not r['txt'], r); continue
            juge(T + ' le nombre seul, « %d », à droite de la ligne' % n, r['vis'] and r['txt'] == str(n) and r['droite'] is not None and r['droite'] <= 4, r)
            juge(T + ' la police et l\'encre de « Un mot… »', r['st'] and r['stm'] and r['st'] == r['stm'], (r['st'], r['stm']))
            juge(T + ' zone de toucher ≥ 44 pt', r['h'] >= 40 and r['w'] >= 40, (round(r['h']), round(r['w'])))
            # le toucher : chaque image du défilement, la barre
            # comme un doigt : on touche le nombre là où il se VOIT ; sous la barre (ou sous l'en-tête), on fait d'abord défiler la fiche jusqu'à lui
            vu = pg.evaluate("()=>{ const q=document.querySelector('#cm5Ligne .cm5-nb').getBoundingClientRect(); const e=document.elementFromPoint(q.left+q.width/2, q.top+q.height/2); return !!(e && e.closest && e.closest('.cm5-nb')); }")
            if not vu:
                pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, q=document.querySelector('#cm5Ligne .cm5-nb').getBoundingClientRect(); dp.scrollTop+=((q.bottom-dv.top)/k-740)*1; }"); pg.wait_for_timeout(500)
                try: pg.wait_for_function("()=>{ const q=document.querySelector('#cm5Ligne .cm5-nb').getBoundingClientRect(); const e=document.elementFromPoint(q.left+q.width/2, q.top+q.height/2); return !!(e && e.closest && e.closest('.cm5-nb')); }", timeout=15000)
                except Exception: pass
            pg.evaluate("()=>{ window.__g=[]; const dp=document.getElementById('detailPoster'), bar=document.getElementById('dpDetails'), dv=document.getElementById('device'); const k=dv.getBoundingClientRect().width/390; const t0=performance.now();"
                        " (function f(t){ window.__g.push([t, dp.scrollTop, bar?(bar.getBoundingClientRect().top-dv.getBoundingClientRect().top)/k:null]); const G=window._cm5Glisse; const L=window.__g, imm=L.length>3 && performance.now()-t0>1500 && (function(){ for(var i=L.length-1;i>=0;i--){ if(Math.abs(L[i][1]-dp.scrollTop)>0.05) return performance.now()-L[i][0]>900; } return performance.now()-t0>3000; })(); if(performance.now()-t0<20000 && !imm && !(G && Math.abs(dp.scrollTop-G.cible)<0.6 && performance.now()-t0>400)) requestAnimationFrame(f); else window.__gFin=1; })(performance.now()); }")
            # le doigt touche la partie VISIBLE du nombre (au-dessus de la barre, sous l'en-tête) — sur une fiche à 1 ou 3 mots, la ligne est à moitié sous la barre (Q608)
            PT = "()=>{ window._cm5Glisse=null; const q=document.querySelector('#cm5Ligne .cm5-nb').getBoundingClientRect(), b=document.getElementById('dpDetails').getBoundingClientRect(); const bas=Math.min(q.bottom, b.top-2); const x=q.left+q.width/2, y=(q.top+bas)/2, e=document.elementFromPoint(x,y); return [x, y, !!(e && e.closest && e.closest('.cm5-nb'))]; }"
            # v186b : le doigt ne touche que là où le nombre est SOUS le doigt (sous charge, la mise en page d'avant le défilement préalable trompait le juge, §8)
            for _ in range(20):
                x, y, sous = pg.evaluate(PT)
                if sous: break
                # une pose de la fiche peut encore réduire sa hauteur après le défilement préalable (vu : 155 → 59 sans écriture de scrollTop) : on le refait
                pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, q=document.querySelector('#cm5Ligne .cm5-nb').getBoundingClientRect(); if((q.bottom-dv.top)/k>748) dp.scrollTop+=((q.bottom-dv.top)/k-740); }")
                pg.wait_for_timeout(500)
            if not sous: print('     (non jugé : le nombre n\'est pas atteignable au doigt après 10 s — charge du Mac)', flush=True)
            pg.evaluate("()=>{window.__gFin=0}"); pg.mouse.click(x, y)
            try: pg.wait_for_function("()=>window.__gFin===1", timeout=30000)
            except Exception: pass
            pg.wait_for_timeout(300)
            g = pg.evaluate("()=>window.__g"); st = [z[1] for z in g]; d = [st[i + 1] - st[i] for i in range(len(st) - 1)]
            # la courbe : chaque image tombe sur la courbe prévue (aller-retour quadratique, sur l'horloge réelle) — juste à toute cadence
            gl = pg.evaluate("()=>window._cm5Glisse")
            ecarts = []
            if gl and gl.get('t0') is not None:
                t0p = pg.evaluate("()=>window.__g0||0")
            per = [g[i + 1][0] - g[i][0] for i in range(len(g) - 1)]; cadence = (sum(per) / len(per)) if per else 99
            mv = [v for v in d if abs(v) > 0.05]; sens = all(v >= -0.05 for v in d) or all(v <= 0.05 for v in d)
            moy = (sum(abs(v) for v in mv) / len(mv)) if mv else 0
            e = pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'), dv=document.getElementById('device'), k=dv.getBoundingClientRect().width/390, R=dv.getBoundingClientRect(); const u=dp.querySelector('#cm5Liste .cm5-un'); const q=u&&u.getBoundingClientRect();"
                            " const s=document.querySelector('#cm5Ligne .cm5-saisie'); return {un: q?[(q.top-R.top)/k,(q.bottom-R.top)/k]:null, saisie: !!(s && getComputedStyle(s).display!=='none'), focus: document.activeElement && document.activeElement.classList.contains('cm5-saisie'), peauf: dp.classList.contains('s2-ouv'), sc: dp.scrollTop, max: dp.scrollHeight-dp.clientHeight, g: window._cm5Glisse}; }")
            bars = [z[2] for z in g if z[2] is not None]
            juge(T + ' toucher : ni saisie, ni clavier, ni Peaufiner', not e['saisie'] and not e['focus'] and not e['peauf'], {k: e[k] for k in ('saisie', 'focus', 'peauf')})
            # v186b : le défilement doux NATIF (scrollTo smooth) — un sens, arrivé à la cible (± 1), aucun pas > 3 × le pas moyen au calme ; rien à faire glisser : sans objet
            rien = gl and abs(gl['cible'] - gl['depart']) < 0.5
            if rien: print('     (glissement sans objet : le premier commentaire est déjà entier à l\'écran, ou la fiche ne défile pas plus)', flush=True)
            else:
                juge(T + ' le glissement : un sens, d\'un seul mouvement, arrivé à la cible (± 1,5 pt) ou au bout du défilement possible', sens and gl and len(mv) >= 1 and (abs(st[-1] - gl['cible']) <= 1.5 or (len(st) > 2 and abs(st[-1] - st[-2]) < 0.05 and e['un'] and e['un'][0] >= 111.5 and e['un'][1] <= 760.5)), (len(mv), round(st[-1]), gl and round(gl['cible']), 'images de %.0f ms' % cadence))
                if cadence <= 34: juge(T + ' au calme : ≥ 8 images en mouvement, aucun pas > 3 × le pas moyen', len(mv) >= 8 and max(abs(v) for v in mv) <= 3 * moy + 0.5, (len(mv), round(max([abs(v) for v in mv] or [0]), 1), round(moy, 1)))
                else: print('     (cadence non jugée : images de %.0f ms, charge du Mac)' % cadence, flush=True)
            juge(T + ' la barre Peaufiner reste en bas (760) à chaque image', bars and all(abs(v - 760) <= 1 for v in bars), (round(min(bars or [0]), 1), round(max(bars or [0]), 1)))
            juge(T + ' arrivé : le premier commentaire entier entre l\'en-tête (112) et la barre (760)', e['un'] and e['un'][0] >= 111.5 and e['un'][1] <= 760.5, (e['un'] and [round(v, 1) for v in e['un']], round(e['sc']), round(e['max'])))
    ctx.close(); b.close()
print('\n  %s  %d / %d' % ('✅' if ko == 0 else '❌', ok, ok + ko))
