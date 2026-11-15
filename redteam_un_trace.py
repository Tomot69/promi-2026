"""⚑ v203 (Tom, fin de v203, C-279) — UN SEUL LANGAGE VISUEL POUR TRACER ET DÉTRACER : CELUI D'ATKINSON.
« Le tracé et le détracé des textes en Atkinson sont validés. Il devient le seul mécanisme de tracé et de détracé de l'app. Le détracé est l'inverse exact du tracé :
aucun fondu, aucune disparition d'un coup. Juge : pour chaque texte, tracé puis détracé image par image, comparés à la séquence d'Atkinson (même courbe, même durée à
taille égale). »

Le mécanisme d'Atkinson : `variantes/trace-lettres.js` (`TraceLettres.trace`, les chemins `variantes/trace-chemins-atkinson.js`), 40 caractères par seconde, une lettre en
70 à 90 ms, trois au plus en cours ; le détracé est `{inverse:true}` : le même temps, à rebours. WebKit, 390 × 844 ×3, au doigt (banc_tom). Le juge enveloppe
`TraceLettres.trace` (chaque appel : le texte, sa police, ses options, sa durée prévue et réelle) et `Element.prototype.remove`, et suit à chaque image les textes tracés.
Parcours : la page + (l'exemple puis la première lettre, la validation, le sens basculé trois fois, le titre effacé, la parole effacée — le trait et son libellé se
retirent), le Studio (deux mondes glissés), le guide (son rappel, le passage du Studio au +).
  A · aucun appel n'a sa propre cadence (ni `vitesse` ni `cps`) : la cadence d'Atkinson pour tous
  B · la durée prévue d'un tracé et de son détracé est celle d'Atkinson pour le même nombre de caractères (± 10 %, la phrase du guide en Atkinson pour référence)
  C · chaque texte tracé qui quitte l'écran part par son détracé : jamais retiré, vidé ou caché d'une image à l'autre pendant qu'il est entier à l'écran
  D · aucun texte ne s'efface par un fondu (une animation d'opacité sur un élément qui porte du texte)
  E · le détracé est l'inverse du tracé : même durée réelle (± 25 %) pour un même texte
--seq=page,studio,guide"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
SEQ = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--seq=')), ['page', 'studio', 'guide'])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__U={appels:[], secs:[], fondus:[]}; const traces=new WeakSet();
  function txt(e){ return (e && e.textContent || '').replace(/\s+/g,' ').trim(); }
  function vis(e){ if(!e || !e.isConnected) return false; const r=e.getClientRects(); if(!r.length) return false; for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } const cp=getComputedStyle(e).clipPath||''; if(/polygon\(0px 0px, ?0px 0px, ?0px 0px\)/.test(cp)) return false; return true; }
  const SUIVIS=new Map();   // élément tracé → {t, dernier texte vu entier}
  (function arme(){ const T=window.TraceLettres; if(!T || !T.trace){ setTimeout(arme, 100); return; } if(T.__u) return; T.__u=1; const o=T.trace;
    T.trace=function(el, c, op){ op=op||{}; const ctl=o.apply(this, arguments); if(op.preparer) return ctl; try{ const cs=getComputedStyle(el), rec={t:performance.now(), txt:txt(el).slice(0,40), n:txt(el).length, fam:cs.fontFamily.split(',')[0].replace(/['"]/g,''), fs:cs.fontSize, inv:!!op.inverse, opts:Object.keys(op).filter(k=>['vitesse','cps'].indexOf(k)>=0)};
        window.__U.appels.push(rec); if(ctl && ctl.fin) ctl.fin.then(()=>{ rec.prevu=ctl.mesure&&ctl.mesure.prevu; rec.reel=ctl.mesure&&ctl.mesure.reel; });
        if(!op.inverse) SUIVIS.set(el, {t:performance.now(), txt:rec.txt}); else { const s=SUIVIS.get(el); if(s) s.inv=performance.now(); } }catch(_){ } return ctl; }; })();
  const R=Element.prototype.remove; Element.prototype.remove=function(){ try{ const s=SUIVIS.get(this); if(s && !s.inv && vis(this) && performance.now()-s.t>1500 && txt(this)) window.__U.secs.push([Math.round(performance.now()), 'retiré', txt(this).slice(0,30)]); }catch(_){ } return R.apply(this, arguments); };
  (function f(){ try{ SUIVIS.forEach((s, el)=>{ const v=vis(el), x=txt(el); const ec=el.isConnected && el.closest('.screen, .sheet, #createSheet, #detailPoster, #guide, #promiOnb'), ecv=!ec || vis(ec);   /* l'écran qui se ferme emporte ses textes : ce n'est pas un texte qui part */
      if(s.vu && !v && !s.inv && performance.now()-s.t>1500 && el.isConnected && ecv) window.__U.secs.push([Math.round(performance.now()), 'caché ou vidé', s.txt]); if(s.vu && el.isConnected && v && s.x && x!==s.x && !s.inv && performance.now()-s.t>1500 && !el.__trace) window.__U.secs.push([Math.round(performance.now()), 'changé sans détracé', s.x+' → '+x]); s.vu=v; s.x=x; if(!el.isConnected) SUIVIS.delete(el); });
      document.querySelectorAll('#device *').forEach(e=>{ if(!e.getAnimations) return; e.getAnimations().forEach(a=>{ try{ if(a.animationName==='promiBlink' || /blink/.test(String(e.className))) return;   /* le clignotement du I de PROMI et du dernier caractère d'un titre (validés, v153, C-153) : pas un départ */ const k=a.effect.getKeyframes(); if(!k.some(q=>q.opacity!=null)) return; const propre=[].some.call(e.childNodes, n=>n.nodeType===3 && n.nodeValue.trim()), petit=e.querySelectorAll('*').length<6;
          if(propre && petit) window.__U.fondus.push([txt(e).slice(0,30), e.id||e.className]); else if(txt(e)) (window.__U.ecrans=window.__U.ecrans||[]).push(e.id||String(e.className).slice(0,30)); }catch(_){ } }); });   /* un TEXTE en fondu ; un écran entier en fondu est noté à part (C-130, hors de ce juge) */ }catch(_){ } requestAnimationFrame(f); })();
})();"""
def ouvre_nat(pg, nat):
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_un_trace — %s · charge %.1f' % (F, B.charge()))
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(INIT); pg = B.ouvre(ctx, F)
    if 'page' in SEQ:
        ouvre_nat(pg, 'promi')
        for _ in range(4):
            B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(900)
            if pg.evaluate("()=>{const a=document.activeElement;return !!a&&a.id==='phIn';}"): break
        pg.keyboard.type('lire', delay=60); pg.wait_for_timeout(2400); pg.keyboard.press('Enter'); pg.wait_for_timeout(3000)
        if '--sonde' in A: pg.evaluate("()=>{ const t=document.querySelector('#createSheet .pp-trace'); if(t) t.textContent=''; }"); pg.wait_for_timeout(300)   # §7 : un texte tracé vidé d'un coup — C doit rougir
        for _ in range(3): B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(2600)
        B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(800)
        for _ in range(4): pg.keyboard.press('Backspace')
        pg.wait_for_timeout(3000); pg.keyboard.press('Enter'); pg.wait_for_timeout(3000)
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1500)
    if 'studio' in SEQ:
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(3000)
        for _ in range(2): B.glisse(pg, [(320, 400), (220, 400), (70, 400)]); pg.wait_for_timeout(2600)
        B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(1500)
    if 'guide' in SEQ:
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} localStorage.removeItem('promi_guide'); if(window._guide) _guide.attend(false); }")
        pg.wait_for_timeout(5500); B.tap(pg, 200, 380); pg.wait_for_timeout(3200)
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2000); B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(4500)
        B.tap(pg, 200, 380); pg.wait_for_timeout(3500)
    pg.wait_for_timeout(1500)
    U = pg.evaluate("()=>window.__U"); ctx.close(); b.close()
ap = U['appels']
print('  %d appels (%d détracés) · polices %s' % (len(ap), sum(1 for a in ap if a['inv']), sorted(set(a['fam'] for a in ap))))
juge('A · aucun appel n\'a sa propre cadence (ni vitesse ni cps)', not [a for a in ap if a['opts']], [(a['txt'], a['opts']) for a in ap if a['opts']][:4])
ref = [a for a in ap if a['fam'].startswith('Atkinson') and a.get('prevu') and a['n'] > 8]
rap = (sum(a['prevu'] / a['n'] for a in ref) / len(ref)) if ref else 25.0   # ms par caractère : la cadence d'Atkinson (40 car/s ≈ 25 ms, plus la durée d'une lettre)
ecarts = []
for a in ap:
    if not a.get('prevu') or a['n'] < 3: continue
    att = rap * a['n']; tol = max(0.10 * att, 90)   # 90 ms : la durée d'une lettre (70 à 90 ms) se compte une fois, quel que soit le nombre de caractères
    if abs(a['prevu'] - att) > tol: ecarts.append((a['txt'], a['fam'], a['inv'], a['prevu'], round(att)))
juge('B · la durée prévue de chaque tracé et détracé est celle d\'Atkinson pour son nombre de caractères (± 10 %%) — %.1f ms/car, %d de référence' % (rap, len(ref)), not ecarts, ecarts[:4])
juge('C · aucun texte tracé ne quitte l\'écran sans son détracé (retiré, caché ou vidé d\'une image à l\'autre)', not U['secs'], U['secs'][:6])
fo = sorted(set(tuple(x) for x in U['fondus'])); print('  (des écrans entiers en fondu, hors de ce juge : %s)' % sorted(set(U.get('ecrans') or []))[:6])
juge('D · aucun texte ne s\'efface par un fondu', not fo, fo[:5])
paires = {}
for a in ap:
    if a.get('reel'): paires.setdefault(a['txt'], {}).setdefault('inv' if a['inv'] else 'tr', []).append(a['reel'])
ec2 = [(t, v['tr'][0], v['inv'][0]) for t, v in paires.items() if 'tr' in v and 'inv' in v and abs(v['tr'][0] - v['inv'][0]) > max(0.25 * max(v['tr'][0], v['inv'][0]), 90)]   # 90 ms : la durée d'une lettre (comme B)
juge('E · le détracé dure comme son tracé (± 25 %%) — %d textes tracés puis détracés' % sum(1 for v in paires.values() if 'tr' in v and 'inv' in v), not ec2, ec2[:4])
print('%d/%d' % (sum(RES), len(RES)))
