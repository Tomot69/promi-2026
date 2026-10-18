#!/usr/bin/env python3
"""
redteam_validation.py — v149 (Tom, 18 oct. 2026) : LA VALIDATION, DU LEVER DU DOIGT À LA FICHE TENUE. Banc comme Tom (WebKit, 390 × 844 ×3, doigt).

  C-155 · « Mesure le délai entre le lever du doigt et la première image. Si le trait est complet au lever, l'animation part DANS L'IMAGE SUIVANTE,
          sans attente de confirmation. Le travail lourd (enregistrement, Toile, Fil) passe APRÈS le départ. » — pour la création et pour la validation.
  C-156 · « 7.1 Tenue d'un coup (seul, ou la dernière part) : au lever le rideau part DIRECTEMENT du trait, un seul mouvement à vitesse constante ; la
          vague intermédiaire est supprimée. 7.2 Ma part sans être la dernière : seulement la vague sous le trait, en amande, pas de rideau ; la fiche
          reste en cours. 7.3 Quand tout le monde a tracé : une entrée dans le Fil de chacun. 7.4 À la première ouverture de chaque participant après ce
          moment, le rideau descend sous ses yeux, la fiche est pleinement tenue ; aux ouvertures suivantes, elle s'ouvre directement tenue. Le « déjà vu »
          se garde par personne et par parole. »

On lit, à chaque image (un rappel d'image posé dans la page), la matière amande sous le trait sur trois colonnes : son haut et son front bas, sur le ruban
(`#tenirRuban`) et le rideau (`#tenirMaree`) réunis ; et, pour la création, l'échelle de la dalle de la page + (`#csTrameCv`).
  A · seul — la première image après le lever montre déjà le front qui descend ; le front ne remonte jamais et ne s'arrête jamais avant la barre (un
      seul mouvement) ; le haut de la matière redescend sur le trait en moins de 160 ms et ne remonte pas ; le ruban s'en va sous le rideau ; la parole
      est tenue ; « déjà vu » posé pour moi. Délai et vitesse régulière : jugés seulement au calme (charge < 4, C-137).
  B · la dernière part (la part de Rachel arrivée avant, fiche fermée) — de même : le rideau part au lever, la parole devient tenue.
  C · ma part, pas la dernière (trois personnes) — aucun rideau, jamais ; la vague amande sous le trait est là après le lever puis se resserre et s'en
      va ; la parole reste en cours ; ma part est écrite.
  D · les deux autres parts arrivent, fiche fermée — la parole est tenue ; une entrée « Chacun a tracé sa part » dans le Fil ; « déjà vu » : pas moi.
      Première ouverture : le rideau descend ; « déjà vu » posé. Seconde ouverture : aucun rideau. L'app rechargée : toujours aucun rideau.
  E · la création (page +) — la première image après le lever montre la dalle qui grandit ; elle grandit à chaque image jusqu'à la coupe ; la Toile
      reçoit la parole APRÈS que la dalle a commencé à grandir. Délai et vitesse régulière : au calme seulement.
  Q · (Q536, tranchée en v149) pendant le tracé, doigt posé, aucun nœud de la fiche ne se floute ni ne passe à demi transparent (lu sur les styles calculés,
      WebKit : la règle d'août floutait cinq nœuds, dont la phrase et le titre).
Preuve : `--fichier=zz-av148.html` rougit (A : le haut de la matière remonte / le rideau part sous le ruban ; C : un rideau ; D : aucun rideau à la
première ouverture ; E : la dalle attend 440 ms).
"""
import os, sys, statistics; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
CHARGE = float(os.popen('sysctl -n vm.loadavg').read().split()[1])
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-118s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
SUIT = r"""()=>{ window.__R=[]; window.__lev=0; window.__add=0; const D=()=>document.getElementById('device').getBoundingClientRect();
  if(!window.__levA){ window.__levA=1; document.addEventListener('touchend',()=>{ window.__lev=performance.now(); },{capture:true});
    try{ const ad=Toile.addPromi; Toile.addPromi=function(){ if(!window.__add) window.__add=performance.now(); return ad.apply(this,arguments); }; }catch(e){} }
  function lit(cv, X){ if(!cv) return null; const r=cv.getBoundingClientRect(), d=D(), k=d.width/390, s=cv.width/(r.width/k), top=(r.top-d.top)/k; const g=cv.getContext('2d'); const out=[];
    for(const x of X){ const col=g.getImageData(Math.round(x*s),0,1,cv.height).data; let a0=-1,a1=-1; for(let j=0;j<cv.height;j++){ const a=col[j*4+3], gg=col[j*4+1], rr=col[j*4]; if(a>128 && gg>180 && rr<200){ if(a0<0) a0=j; a1=j; } } out.push(a0<0?null:[top+a0/s, top+a1/s]); } return out; }
  (function f(){ if(window.__lev){ const t=performance.now()-window.__lev; if(t<1600){ const dc=document.getElementById('csTrameCv'); let sc=null; try{ const m=getComputedStyle(dc).transform.match(/matrix\(([^,]+)/); sc=m?+m[1]:1; }catch(e){}
      window.__R.push([t, lit(document.getElementById('tenirRuban'),[100,195,290]), lit(document.getElementById('tenirMaree'),[100,195,290]), sc, !!document.getElementById('tenirMaree'), !!document.getElementById('tenirRuban')]); } }
    requestAnimationFrame(f); })(); }"""
TIENT = r"""async ([pts])=>{ const el0=document.elementFromPoint(pts[0][0],pts[0][1]); const T=(x,y)=>{ const o={identifier:7,target:el0,clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,radiusX:11,radiusY:11,force:.5}; try{return new Touch(o);}catch(e){return o;} };
  const ev=(typ,x,y)=>{ const t=T(x,y), L=[t]; let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,composed:true,touches:L,targetTouches:L,changedTouches:[t]}); if(!e.changedTouches||!e.changedTouches.length) throw 0; }catch(_){ e=new Event(typ,{bubbles:true,cancelable:true,composed:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t]}); } el0.dispatchEvent(e); };
  const pe=(typ,x,y)=>el0.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,composed:true,pointerId:7,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,width:22,height:22,pressure:.5}));
  const att=ms=>new Promise(r=>setTimeout(r,ms)); pe('pointerdown',pts[0][0],pts[0][1]); ev('touchstart',pts[0][0],pts[0][1]);
  for(let i=1;i<pts.length;i++){ await att(30); pe('pointermove',pts[i][0],pts[i][1]); ev('touchmove',pts[i][0],pts[i][1]); } window.__fin=()=>{ const L=pts[pts.length-1]; pe('pointerup',L[0],L[1]); const t=T(L[0],L[1]); let e; try{ e=new TouchEvent('touchend',{bubbles:true,cancelable:true,composed:true,touches:[],targetTouches:[],changedTouches:[t]}); }catch(_){ e=new Event('touchend',{bubbles:true}); Object.defineProperty(e,'changedTouches',{value:[t]}); Object.defineProperty(e,'touches',{value:[]}); } el0.dispatchEvent(e); }; }"""
FLOUS = """()=>[...document.querySelectorAll('#detailPoster, #detailPoster *')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{ const c=getComputedStyle(e); return [e.id||'', c.filter, c.opacity]; }).filter(x=>(x[1]&&x[1]!=='none') || +x[2]<1).map(x=>x.join(' '))"""
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
CREE = """(a)=>{ const [t, de, avec]=a; computeBox(); const np=P(t,'moi',7,2,'encours',undefined,de); np.chiche=true; np.avec=avec; np.x=box.x+box.w/2; np.y=box.y+box.h/2; np.tx=np.x; np.ty=np.y;
  promises.push(np); try{ Toile.addPromi(np.id); }catch(e){} try{ syncAll(); }catch(e){} try{ saveState(); }catch(e){} return np.id; }"""
def union(row, i):
    rb, mr = row[1], row[2]; a = rb[i] if rb else None; m = mr[i] if mr else None; v = [x for x in (a, m) if x]
    return (min(x[0] for x in v), max(x[1] for x in v)) if v else None
def ferme(pg):
    pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(700)
def ouvre_fiche(pg, pid):
    ferme(pg); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2800)
def tenir(pg):
    pg.evaluate(SUIT); z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(2200)
    return pg.evaluate("()=>window.__R")
def rideau(R, T):
    """A1–A5 sur les relevés après le lever"""
    L = [r for r in R if r[0] >= 0]
    if not L: juge('%s le relevé après le lever existe' % T, False); return
    fr = [union(r, 1) for r in L]; avec = [(r[0], f) for r, f in zip(L, fr) if f]
    juge('%s la première image après le lever montre déjà la matière, et le rideau est posé' % T, bool(avec) and avec[0][0] == L[0][0] and L[0][4], 'première image +%.0f ms · rideau %s' % (L[0][0], L[0][4]))
    if len(avec) < 6: juge('%s assez d\'images pour juger' % T, False, len(avec)); return
    f0 = avec[0][1][1]; f1 = avec[1][1][1]
    juge('%s 7.1 · le front descend DÈS la première image (aucune attente sous le ruban : la vague intermédiaire n\'existe plus)' % T, f1 > f0 + 0.3 or (len(avec) > 2 and avec[0][1][1] > 0 and avec[1][1][1] > avec[0][1][1]), 'front %.1f → %.1f pt' % (f0, f1))
    bas = [f[1] for _, f in avec]; arr = next((i for i, v in enumerate(bas) if v >= 740), len(bas))
    recul = [bas[i] - bas[i + 1] for i in range(min(arr, len(bas) - 1))]; arrets = sum(1 for i in range(1, min(arr, len(bas) - 1)) if bas[i + 1] - bas[i] < 0.3 and bas[i] - bas[i - 1] < 0.3)
    juge('%s 7.1 · un seul mouvement : le front ne remonte jamais, et ne s\'arrête jamais deux images de suite avant la barre' % T, (max(recul) if recul else 0) <= 0.6 and arrets == 0, 'recul max %.1f pt · arrêts %d · %d images jusqu\'à la barre' % (max(recul) if recul else 0, arrets, arr))
    hauts = [(t, f[0]) for t, f in avec]; h0 = hauts[0][1]; hfin = min(h for _, h in hauts[-5:]) if len(hauts) > 5 else hauts[-1][1]
    pose = next((t for t, h in hauts if h >= hfin - 0.6), None); monte = max([hauts[i][1] - hauts[i + 1][1] for i in range(len(hauts) - 1)] or [0])
    juge('%s 7.1 · le haut de la matière redescend sur le trait en moins de 160 ms, sans jamais remonter' % T, pose is not None and pose <= 160 and monte <= 0.6, 'haut %.1f → %.1f pt en %s ms · remontée max %.1f' % (h0, hfin, None if pose is None else round(pose), monte))
    plus_ruban = next((r[0] for r in L if not r[5]), None)
    juge('%s 7.1 · le ruban s\'en va sous le rideau (avant 300 ms)' % T, plus_ruban is not None and plus_ruban <= 300, plus_ruban)
    if CHARGE < 4:
        juge('%s C-155 · délai lever → première image ≤ 20 ms (charge %.1f)' % (T, CHARGE), L[0][0] <= 20, '%.1f ms' % L[0][0])
        v = [(bas[i + 1] - bas[i]) / max(1, avec[i + 1][0] - avec[i][0]) for i in range(1, min(arr, len(bas) - 1))]; m = statistics.median(v) if v else 0
        juge('%s 7.1 · vitesse constante : chaque image à ± 30 %% de la vitesse médiane (charge %.1f)' % (T, CHARGE), v and all(abs(x - m) <= 0.3 * m for x in v), 'médiane %.2f pt/ms · %s' % (m, [round(x, 2) for x in v][:10]))
    else: print('  ·  %s délai (%.0f ms) et vitesse : non jugés, charge %.1f (C-137)' % (T, L[0][0], CHARGE))

with sync_playwright() as p:
    b = p.webkit.launch()
    print('charge %.1f' % CHARGE)
    # ── A · seul
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    B.plante(pg, 'rendre le livre'); pid = pg.evaluate("()=>promises[promises.length-1].id"); ouvre_fiche(pg, pid)
    av = set(pg.evaluate(FLOUS)); z = pg.evaluate(ZONE, 'tenirZone')
    pg.evaluate(TIENT, [[list(B.pt(pg, 200 + 4 * i, z[1] + z[3] * 0.45)) for i in range(11)]]); pg.wait_for_timeout(700)
    pend = [x for x in pg.evaluate(FLOUS) if x not in av]; tr_ = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('tracant')")
    pg.evaluate("()=>window.__fin()"); pg.wait_for_timeout(900)
    juge('[Q] Q536 · pendant le tracé (doigt posé), rien de la fiche ne se floute ni ne devient transparent', tr_ and not pend, 'tracant %s · %s' % (tr_, pend[:4]))
    print('A · une parole à moi seul'); rideau(tenir(pg), '[A]')
    s = pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); return {st:p.status, vu:p.vuTenue||null}; }", pid)
    juge('[A] la parole est tenue ; « déjà vu » posé pour moi', s['st'] == 'tenu' and bool(s['vu'] and s['vu'].get('moi')), s)
    ctx.close()
    # ── B · la dernière part, puis C, D · à trois
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    pid = pg.evaluate(CREE, ['relever le défi du lac', 'Marion', 'Rachel']); pg.wait_for_timeout(900)
    pg.evaluate("id=>_parts.arrive(promises.find(p=>p.id===id),'Rachel')", pid); pg.wait_for_timeout(600)
    st = pg.evaluate("id=>promises.find(p=>p.id===id).status", pid)
    ouvre_fiche(pg, pid); print('B · la dernière part (Rachel a tracé avant, fiche fermée)'); rideau(tenir(pg), '[B]')
    s = pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); return {st:p.status, parts:p.parts}; }", pid)
    juge('[B] avant : en cours ; après mon trait : tenue, toutes les parts écrites', st == 'encours' and s['st'] == 'tenu' and s['parts'] and 'moi' in s['parts'] and 'Rachel' in s['parts'], (st, s))
    pid = pg.evaluate(CREE, ['traverser la baie à la nage', 'Marion', 'Rachel, Nico']); pg.wait_for_timeout(900)
    ouvre_fiche(pg, pid); print('C · ma part, pas la dernière (Rachel et Nico n\'ont pas tracé)')
    R = tenir(pg); L = [r for r in R if r[0] >= 0]
    jamais = not any(r[4] for r in L)
    juge('[C] 7.2 · aucun rideau, jamais (2 s après le lever)', jamais and len(L) >= 20, '%d images · rideau vu %s' % (len(L), not jamais))
    vague = [r for r in L if 120 <= r[0] <= 420 and r[5] and union(r, 1)]
    tr = pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'); return (c.getAttribute('data-trait')||'').split(',').map(Number); }")
    sous = [union(r, 1)[1] for r in vague]
    juge('[C] 7.2 · la vague amande SOUS le trait est là après le lever (120 à 420 ms)', len(vague) >= 4 and min(sous) > (tr[0] if tr else 0) + 20, 'bas de la vague %s pt · trait base %s' % ([round(v) for v in sous[:5]], tr[:2] if tr else None))
    fin = next((r[0] for r in L if r[0] > 420 and not r[5]), None)
    juge('[C] 7.2 · puis elle se resserre sur le trait et s\'en va (%s)' % ('avant 1,2 s' if CHARGE < 4 else 'la durée n\'est jugée qu\'au calme, C-137 ; ici : avant 3 s'), fin is not None and fin <= (1200 if CHARGE < 4 else 3000), fin)
    s = pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); return {st:p.status, parts:p.parts}; }", pid)
    juge('[C] 7.2 · la parole reste en cours ; ma part est écrite', s['st'] == 'encours' and s['parts'] and 'moi' in s['parts'], s)
    # D
    ferme(pg); n0 = pg.evaluate("()=>FEED.length")
    pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); _parts.arrive(p,'Rachel'); _parts.arrive(p,'Nico'); }", pid); pg.wait_for_timeout(900)
    s = pg.evaluate("a=>{ const p=promises.find(x=>x.id===a[0]); return {st:p.status, vu:p.vuTenue||null, fil:FEED.slice(0, FEED.length-a[1]).map(f=>f.text)}; }", [pid, n0])
    juge('[D] 7.3 · tout le monde a tracé : la parole est tenue, une entrée « Chacun a tracé sa part » dans le Fil', s['st'] == 'tenu' and any('Chacun a tracé sa part' in t and 'traverser la baie' in t for t in s['fil']), s['fil'][:2])
    juge('[D] 7.4 · « déjà vu » : celui qui a tracé la dernière part (Nico), pas moi', bool(s['vu']) and 'Nico' in s['vu'] and 'moi' not in s['vu'], s['vu'])
    def ouverture(nom, attendu):
        ferme(pg); pg.evaluate("id=>openDetail(id)", pid); vu = False
        for _ in range(30):
            pg.wait_for_timeout(80)
            if pg.evaluate("()=>!!document.getElementById('tenirMaree')"): vu = True; break
        pg.wait_for_timeout(2600 if vu else 1200)
        e = pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); return {st:p.status, vu:p.vuTenue||null, dp:document.getElementById('detailPoster').className.indexOf('show')>=0}; }", pid)
        juge('[D] 7.4 · %s : %s' % (nom, 'le rideau descend sous les yeux, puis la fiche tenue ; « déjà vu » posé pour moi' if attendu else 'AUCUN rideau, la fiche s\'ouvre directement tenue'),
             vu == attendu and e['dp'] and e['st'] == 'tenu' and bool(e['vu'] and e['vu'].get('moi')), 'rideau %s · %s' % (vu, e))
    ouverture('première ouverture', True); ouverture('seconde ouverture', False)
    ferme(pg); pg.wait_for_timeout(1500); pg.reload(); pg.wait_for_timeout(6500)
    ouverture('après un rechargement', False)
    ctx.close()
    # ── E · la création
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ document.getElementById('fTitle').value='lire un livre'; window._csEnLair=true; window._csDueISO=null; try{ if(window._phrase) _phrase.titre='lire un livre'; }catch(e){} }"); pg.wait_for_timeout(600)
    pg.evaluate(SUIT); z = pg.evaluate("()=>_ppEcran().base")
    B.glisse(pg, [[40 + 220 * i / 12, z + 8] for i in range(13)], pas=30, tenue=0); pg.wait_for_timeout(1800)
    R = pg.evaluate("()=>window.__R"); add = pg.evaluate("()=>window.__add ? window.__add - window.__lev : null"); L = [r for r in R if r[0] >= 0]
    print('E · la création (page +)')
    sc = [(r[0], r[3]) for r in L if r[3] is not None]; coupe = next((i for i, (t, s_) in enumerate(sc) if i > 0 and s_ <= 1.0001 and sc[i - 1][1] > 1.5), len(sc))
    juge('[E] C-155 · la première image après le lever montre la dalle qui GRANDIT (aucune attente)', bool(sc) and sc[0][1] > 1.001, 'échelle %s à +%.0f ms' % (sc[0][1] if sc else None, sc[0][0] if sc else -1))
    g = [sc[i + 1][1] - sc[i][1] for i in range(max(0, coupe - 1))]
    juge('[E] elle grandit à chaque image jusqu\'à la coupe', g and min(g) > 0, '%d images · %s' % (len(g), [round(x, 2) for x in g][:10]))
    juge('[E] C-155 · le travail lourd après le départ : la Toile reçoit la parole après que la dalle a commencé à grandir', add is not None and sc and add > sc[0][0], 'Toile.addPromi à +%s ms · première image +%.0f ms' % (None if add is None else round(add), sc[0][0] if sc else -1))
    if CHARGE < 4:
        juge('[E] délai lever → première image ≤ 20 ms (charge %.1f)' % CHARGE, sc and sc[0][0] <= 20, '%.1f ms' % sc[0][0])
        v = [g[i] / max(1, sc[i + 1][0] - sc[i][0]) for i in range(len(g))]; m = statistics.median(v) if v else 0
        juge('[E] vitesse constante : chaque image à ± 30 %% de la vitesse médiane (charge %.1f)' % CHARGE, v and all(abs(x - m) <= 0.3 * m for x in v[1:]), [round(x, 4) for x in v][:10])
    else: print('  ·  [E] délai (%.0f ms) et vitesse : non jugés, charge %.1f (C-137)' % (sc[0][0] if sc else -1, CHARGE))
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
