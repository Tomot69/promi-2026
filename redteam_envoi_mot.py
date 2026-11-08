# -*- coding: utf-8 -*-
"""⚑ v189b (Tom, C-260) — ENVOYER UN COMMENTAIRE : IMMÉDIAT, AVEC UN SENTIMENT DE VALIDATION.
Banc WebKit (banc_tom), Toile du Cercle, fiches Promi, Chiche, Cercle (échelle 0,79 : PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79).
Le doigt est envoyé DANS la page (PointerEvent sur la flèche) : l'heure du lever et celle des images se lisent sur la même horloge.
  A · la première image après le lever porte le changement, la tâche du lever ≤ 4 ms ; au calme (charge < 4) elle vient < 16,7 ms après le lever ; dans cette image le champ est vide, le texte est sur sa copie, la flèche est pressée (une animation de 140 à 180 ms) ;
      le doigt posé ne retire pas le focus du champ ;
  B · la copie part du champ et se pose sur le texte du mot neuf, en tête de la liste (± 1 pt), puis disparaît : le mot se découvre ;
      son chemin (cotes dans la fiche) ne revient jamais en arrière ; durée 200 à 300 ms ; départ vif (la moitié du chemin dans le premier tiers du temps), arrivée douce ;
      à la fin le mot neuf se voit (entre 112 et le bas visible) ; la cadence n'est jugée qu'au calme (charge < 4) ;
  C · aucune couleur nouvelle (la copie a la couleur du champ, puis celle du mot), aucun filtre, aucune opacité animée ;
  D · le nombre à droite de « Un mot… » est le nouveau total ; le Fil porte « Tu as commenté » ;
  E · rechargée 100 ms après l'envoi, la parole garde son mot ; aucune erreur de page.
Rouge sur v189a (zz-v189a.html) : A et B."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-110s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True); return ok
def _calme(): return B.charge() < 4
class _C:
    def __bool__(self): return _calme()
CALME = _C()
def ferme(pg): pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(900)
def ouvre(pg, nat):
    ferme(pg)
    if nat == 'cercle': pg.evaluate("()=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; o.comments.push({t:'Premier mot du potager', by:'Marion', d:'2026-11-01T09:00:00Z', vu:true}); _cercleMots.garde(); openEssaim('potager'); }")
    else:
        t = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}[nat]
        pg.evaluate("t=>{ var p=promises.find(x=>x.title===t); p.comments=[{t:'Un premier mot', by:'Marion', d:'2026-11-01T09:00:00Z', vu:true}]; saveState(true); openDetail(p.id); }", t)
    pg.wait_for_timeout(2600)
TEXTE = 'Je passe demain matin avec les œufs'
ENVOIE = r"""async (texte)=>{ const dp=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const l=document.getElementById('cm5Ligne'); if(!l) return {err:'pas de ligne'};
  const r0=l.getBoundingClientRect(); const pe=(el,typ,x,y)=>el.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,composed:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,pressure:typ==='pointerup'?0:.5,buttons:typ==='pointerup'?0:1}));
  const att=ms=>new Promise(r=>setTimeout(r,ms));
  const m=l.querySelector('.cm5-mot'); const cx=r0.left+60, cy=r0.top+r0.height/2; pe(m||l,'pointerdown',cx,cy); pe(m||l,'pointerup',cx,cy); await att(500);
  const s=l.querySelector('.cm5-saisie'); if(!s) return {err:'pas de saisie'}; s.focus(); s.value=texte; s.dispatchEvent(new Event('input',{bubbles:true})); await att(300);
  const f=l.querySelector('.cm5-va'), rf=f.getBoundingClientRect(), fx=rf.left+rf.width/2, fy=rf.top+rf.height/2, svg=f.querySelector('svg');
  const IM=[]; let fin=false, tUp=null, tDown=null;
  const lit=()=>{ const n=dp.querySelector('.cm5-vol'), R=dp.getBoundingClientRect(); let v=null;
    if(n){ const rn=n.getBoundingClientRect(), c=getComputedStyle(n); v={x:(rn.left-R.left)/k, y:(rn.top-R.top)/k+dp.scrollTop, sy:(rn.top-D.top)/k, col:c.webkitTextFillColor||c.color, op:c.opacity, fil:c.filter, txt:n.textContent}; }
    const st=svg?getComputedStyle(svg).transform:'none', an=svg&&svg.getAnimations?svg.getAnimations().map(a=>a.effect&&a.effect.getComputedTiming?a.effect.getComputedTiming().duration:0):[];
    return {t:performance.now(), val:s.value, vol:v, sv:st, an:an, foc:document.activeElement===s, sc:dp.scrollTop}; };
  const boucle=()=>{ if(fin) return; IM.push(lit()); requestAnimationFrame(boucle); }; requestAnimationFrame(boucle);
  await att(40);
  tDown=performance.now(); pe(f,'pointerdown',fx,fy); const focApresDown=document.activeElement===s, presseApresDown=svg&&svg.getAnimations?svg.getAnimations().length:0;
  await att(70); tUp=performance.now(); pe(f,'pointerup',fx,fy); const tache=performance.now()-tUp;
  await att(1300); fin=true;
  const un=document.querySelector('#cm5Liste .cm5-un'), t=un&&un.querySelector('.cm5-t'), R=dp.getBoundingClientRect(); let cible=null;
  if(t){ const rt=t.getBoundingClientRect(), c=getComputedStyle(t); cible={x:(rt.left-R.left)/k, y:(rt.top-R.top)/k+dp.scrollTop, sy:(rt.top-D.top)/k, sb:(rt.bottom-D.top)/k, txt:t.textContent, vis:c.visibility, col:c.webkitTextFillColor||c.color}; }
  const nb=l.querySelector('.cm5-nb'), vv=window.visualViewport;
  return {IM, tUp, tache, tDown, focApresDown, presseApresDown, cible, nb:nb?nb.textContent:null, champCol:getComputedStyle(s).webkitTextFillColor||getComputedStyle(s).color,
    reste:dp.querySelectorAll('.cm5-vol').length, info:window._cm5Vol||null, fil:(typeof FEED!=='undefined'&&FEED[0])?String(FEED[0].text||FEED[0].t||FEED[0].txt||JSON.stringify(FEED[0])):'' , n:(courantMots()), bas:Math.min(760,(vv?(vv.offsetTop+vv.height-D.top)/k:844)) };
  function courantMots(){ try{ return window._comm && _comm.etat().pid; }catch(e){ return null; } } }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
    erreurs = []; pg.on('pageerror', lambda e: erreurs.append(str(e)[:160]))
    pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; }")
    for nat in ('promi', 'chiche', 'cercle'):
        T = '[%s]' % nat
        ouvre(pg, nat); r = pg.evaluate(ENVOIE, TEXTE + ' · ' + nat)
        if r.get('err'): juge(T + ' la ligne s\'ouvre', False, r['err']); continue
        IM = r['IM']; apres = [i for i in IM if i['t'] > r['tUp']]
        p0 = apres[0] if apres else None
        dt = p0 and p0['t'] - r['tUp']
        juge(T + ' A · la PREMIÈRE image après le lever porte le changement (champ vide, texte sur sa copie) ; la tâche du lever ≤ 4 ms', p0 and p0['val'] == '' and p0['vol'] and p0['vol']['txt'] == TEXTE + ' · ' + nat and r['tache'] <= 4, (p0 and p0['val'][:12], p0 and bool(p0['vol']), round(r['tache'], 2)))
        if CALME: juge(T + ' A · du lever à cette image < 16,7 ms (au calme)', dt is not None and dt < 16.7, dt and round(dt, 1))
        else: print('  ·  %s A · du lever à la première image : %.1f ms — NON JUGÉ (charge %.1f)' % (T, dt or -1, B.charge()))
        juge(T + ' A · la flèche se presse dès le doigt posé (une animation de 140 à 180 ms) ; le focus reste au champ', r['presseApresDown'] >= 1 and any(140 <= d <= 180 for i in IM if i['t'] > r['tDown'] for d in i['an']) and r['focApresDown'],
             (r['presseApresDown'], sorted(set(d for i in IM for d in i['an'])), r['focApresDown']))
        vols = [i for i in apres if i['vol']]
        c = r['cible']
        fa = (r['info'] or {}).get('a')   # l'arrivée que la copie vise (la dernière image lue peut précéder la fin sous charge : elle n'est pas le verdict)
        juge(T + ' B · la copie vise le texte du mot neuf (± 1 pt), puis disparaît ; le mot se voit', c and c['txt'] == TEXTE + ' · ' + nat and fa and abs(fa[0] - c['x']) <= 1 and abs(fa[1] - c['y']) <= 1 and r['reste'] == 0 and c['vis'] == 'visible' and c['sy'] >= 112 and c['sb'] <= r['bas'] + 0.5,
             (c and [round(c['x'], 1), round(c['y'], 1), round(c['sy'], 1), round(c['sb'], 1)], fa and [round(fa[0], 1), round(fa[1], 1)], vols and [round(vols[-1]['vol']['x'], 1), round(vols[-1]['vol']['y'], 1)], r['reste'], c and c['vis'], round(r['bas'], 1)))
        if vols and c:
            d0 = ((vols[0]['vol']['x'] - c['x']) ** 2 + (vols[0]['vol']['y'] - c['y']) ** 2) ** 0.5
            ds = [((v['vol']['x'] - c['x']) ** 2 + (v['vol']['y'] - c['y']) ** 2) ** 0.5 for v in vols]
            if os.environ.get('TRACE'): print('   TRACE', [(round(v['t'] - r['tUp']), round(d, 1)) for v, d in zip(vols, ds)])
            mono = all(ds[i + 1] <= ds[i] + 0.3 for i in range(len(ds) - 1))
            # le départ du mouvement : la première image où la copie a bougé de plus de 0,5 pt
            dep = next((i for i, d in enumerate(ds) if d < d0 - 0.5), None)
            juge(T + ' B · son chemin ne revient jamais en arrière', mono and dep is not None, ([round(x, 1) for x in ds[:16]], d0 and round(d0, 1)))
            if dep is not None and d0 > 4:
                t0 = vols[dep - 1]['t'] if dep > 0 else vols[0]['t']; tf = vols[-1]['t']
                fin = next((i for i, d in enumerate(ds) if d <= 0.3), len(ds) - 1); tfin = vols[fin]['t']
                dur = tfin - t0
                tiers = [d for v, d in zip(vols, ds) if v['t'] - t0 <= dur / 3]
                vif = tiers and (d0 - min(tiers)) >= d0 * 0.5
                pas = [ds[i] - ds[i + 1] for i in range(dep - 1 if dep > 0 else 0, fin)]
                doux = pas and pas[-1] <= d0 * 0.08
                maxpas = max(pas) / d0 if pas else 1
                if CALME:
                    juge(T + ' B · 200 à 300 ms, départ vif, arrivée douce, aucun pas de plus d\'un tiers du chemin (au calme)', 200 <= dur <= 300 and vif and doux and maxpas <= 0.36, (round(dur), vif, doux, round(maxpas, 2)))
                else:
                    print('  ·  %s B · cadence NON JUGÉE (charge %.1f) : %d ms, vif %s, doux %s, plus grand pas %.2f' % (T, B.charge(), dur, vif, doux, maxpas))
        cols = set(i['vol']['col'] for i in vols)
        juge(T + ' C · aucune couleur nouvelle, aucun filtre ni opacité', vols and cols <= {r['champCol'], c and c['col']} and all(i['vol']['op'] in ('1', 1) and i['vol']['fil'] in ('none', '') for i in vols), (cols, r['champCol'], c and c['col']))
        juge(T + ' D · le nombre est le nouveau total (2) ; le Fil porte « Tu as commenté »', (r['nb'] or '').strip() == '2' and 'comment' in r['fil'], (r['nb'], r['fil'][:60]))
    # E · rechargée 100 ms après l'envoi
    for nat in ('promi', 'chiche', 'cercle'):
        ouvre(pg, nat)
        pg.evaluate("""async (t)=>{ const l=document.getElementById('cm5Ligne'), m=l.querySelector('.cm5-mot'), r=l.getBoundingClientRect();
          const pe=(el,typ,x,y)=>el.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y}));
          pe(m,'pointerdown',r.left+60,r.top+20); pe(m,'pointerup',r.left+60,r.top+20); await new Promise(z=>setTimeout(z,400));
          const s=l.querySelector('.cm5-saisie'); s.value=t; const f=l.querySelector('.cm5-va'), q=f.getBoundingClientRect();
          pe(f,'pointerdown',q.left+20,q.top+20); pe(f,'pointerup',q.left+20,q.top+20); setTimeout(()=>location.reload(), 100); }""", 'Rechargé vite · ' + nat)
        pg.wait_for_timeout(7000)
        ok = pg.evaluate("""a=>{ if(a[0]==='cercle'){ try{ return (JSON.parse(localStorage.getItem('promi_cercle_mots')||'{}').potager||[]).some(c=>c.t===a[1]); }catch(e){ return false; } }
          var p=promises.find(x=>x.title===(a[0]==='promi'?'faire les crêpes':'réparer le vélo')); return !!(p && (p.comments||[]).some(c=>c.t===a[1])); }""", [nat, 'Rechargé vite · ' + nat])
        juge('[%s] E · rechargée 100 ms après l\'envoi, la parole garde son mot' % nat, ok)
        pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; }")
    juge('aucune erreur de page', not [e for e in erreurs if 'Load failed' not in e and 'cancelled' not in e], erreurs[:3])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
