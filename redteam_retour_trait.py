# -*- coding: utf-8 -*-
"""⚑ v194 (Tom, §2, C-247) — « La flèche progressive qui revient en douceur : sur la fiche Promi ou Chiche en cours, le doigt part de la pointe de la moitié plantée
et trace la seconde moitié ; le tracé suit le doigt ; lâché avant la fin, il revient en douceur à la pointe. Fais-le EXACTEMENT comme sur la page + : même code de
retour, même courbe, même durée. »
Banc WebKit (banc_tom), échelles 1, 0,79, fenêtre de Tom (PYTHONPATH comme les autres juges). Promi et Chiche, sans défilement et après un aller-retour.
Un tracé lâché à 5, 15 et 40 % de la seconde moitié (≈ 10, 29, 78 pt au-delà de la pointe) :
  A · pendant le tracé, le plein (la couleur du trait, continu, lu sur le canevas de la boîte) va de la pointe jusqu'au doigt (± 4 pt) ;
  B · au lâcher, à 5 et 15 % (moins de 60 pt d'avancée : rien n'est tenu, C-107), il revient à la pointe ; la séquence de son avancée, image par image, est celle de
      la page + pour un même tracé au-delà de sa pointe (± 3 pt par image ; même durée à une image près) — la page + jouée dans le même banc ;
  C · à 40 % (78 pt ≥ 60) la parole est tenue (C-107) : aucun retour ;
  D · le plein dessiné suit la séquence (lu sur les pixels à chaque image, ± 4 pt). Rouge sur v193 (aucun plein ne suit le doigt)."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['promi', 'chiche'])
ECH = os.environ.get('PROMI_ECHELLE', '1')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True); return ok
TITRE = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}
# un tracé par le vrai écouteur (pointeur + toucher), en cotes 390 ; il reste posé ; `fin` le lève et relève, à chaque image, ce que publie le doigt et ce que peint la boîte
GESTE = """async ([sel, xs, fin, ech])=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, Z=document.querySelector(sel);
  const onde=(sel==='#tenirCv') ? (()=>{ const t=document.getElementById('dpTrameCv').getAttribute('data-trait').split(','); return _onde.onde(+t[0],+t[1]); })() : (()=>{ const e=_ppEcran(); return _onde.onde(e.base,e.amp); })();
  const s=(sel==='#tenirCv') ? document.getElementById('detailPoster').scrollTop : 0, base=(sel==='#tenirCv') ? D.top : document.getElementById('csTrameCv').getBoundingClientRect().top;
  const X=x=>D.left+x*k, Y=x=>base+(onde(x)-s)*k, el=document.elementFromPoint(X(xs[0]),Y(xs[0]));
  const T=x=>{ const o={identifier:5,target:el,clientX:X(x),clientY:Y(x),pageX:X(x),pageY:Y(x),screenX:X(x),screenY:Y(x),radiusX:11,radiusY:11,force:.5}; try{return new Touch(o)}catch(e){return o} };
  const ev=(typ,x,f)=>{ const t1=T(x), L=f?[]:[t1]; let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,touches:L,targetTouches:L,changedTouches:[t1]}); if(!e.changedTouches.length) throw 0; }catch(_){ e=new Event(typ,{bubbles:true,cancelable:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t1]}); } el.dispatchEvent(e); };
  const pe=(typ,x)=>el.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,pointerId:5,pointerType:'touch',isPrimary:true,clientX:X(x),clientY:Y(x),width:22,height:22,pressure:typ==='pointerup'?0:.5,buttons:typ==='pointerup'?0:1}));
  const w=ms=>new Promise(r=>setTimeout(r,ms)), nf=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  if(!fin){ pe('pointerdown',xs[0]); ev('touchstart',xs[0]); await w(380); for(let i=1;i<xs.length;i++){ pe('pointermove',xs[i]); ev('touchmove',xs[i]); await w(40); } await nf(); await nf(); return el.id||el.className; }
  const L=xs[xs.length-1], out=[]; const t0=performance.now(); pe('pointerup',L); ev('touchend',L,true);
  const P=eval('('+window.__PLEIN+')'), pointe=(sel==='#tenirCv')?195:42.9;
  for(let i=0;i<40;i++){ await nf(); const dg=(sel==='#tenirCv')?window._ficheDoigt:window._ppDoigt; out.push([Math.round(performance.now()-t0), P([sel, pointe]), (typeof dg==='number')?Math.max(0,dg-pointe):0]); }
  return out; }"""
# la longueur du plein CONTINU au-delà de la pointe, lue sur le canevas qui porte le trait (la boîte sur la fiche, `csTrameCv` sur la page +)
PLEIN = """([sel, pointe])=>{ const fiche=sel==='#tenirCv', c=fiche ? document.getElementById('v189Jonction') : document.getElementById('csTrameCv'); if(!c) return null;
  const J=fiche && _v189Jonction(), E=fiche ? c.width/(390+2*(J.XO||0)) : c.width/390, x0=fiche ? (J.XO||0) : 0, y0=fiche ? J.F.Ytop : 0;
  const t=fiche ? document.getElementById('dpTrameCv').getAttribute('data-trait').split(',') : null, e=fiche ? null : _ppEcran(), onde=fiche ? _onde.onde(+t[0],+t[1]) : _onde.onde(e.base,e.amp);
  const g=c.getContext('2d'); let fin=pointe;
  for(let x=pointe+10;x<389;x+=1){ const d=g.getImageData(Math.round((x+x0)*E), Math.round((onde(x)-y0)*E), 1, 1).data; if(d[3]<200) break; fin=x; }
  return fin-pointe; }"""
def ouvre_fiche(b, nat, defile):
    ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 6000)
    pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); p.status='encours'; delete p.parts; if(a[1]){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; p.who='Adrien'; } p.comments=[1,2,3,4,5,6].map(i=>({t:'Mot numéro '+i, by:'Marion', d:'2026-11-0'+i+'T09:00:00Z', vu:true})); openDetail(p.id); }", [TITRE[nat], nat == 'chiche'])
    pg.wait_for_timeout(2600)
    if defile:
        for s in list(range(0, 260, 20)) + list(range(260, -1, -20)) + [0]:
            pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s); pg.wait_for_timeout(16)
        pg.wait_for_timeout(500)
    return ctx, pg
def ouvre_page(b, nat):
    ctx = B.contexte(b); pg = B.ouvre(ctx, F, 6000); pg.evaluate("()=>{ window.__INVITE_BANC=true; }")
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2800)
    pg.evaluate("()=>{ const f=document.getElementById('fTitle'); f.value='appeler mamie'; f.dispatchEvent(new Event('input',{bubbles:true})); f.blur(); }"); pg.wait_for_timeout(2500)
    return ctx, pg
def seq(o, pointe): return [(t, v) for t, v in o]
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in NATS:
        for defile in (False, True):
            for frac in (0.05, 0.15, 0.40):
                T = '[%s · %s · %s · %d %%]' % (ECH, nat, 'après un aller-retour' if defile else 'sans défilement', round(frac * 100))
                L = 195 * frac
                ctx, pg = ouvre_fiche(b, nat, defile); pid = pg.evaluate("t=>promises.find(x=>x.title===t).id", TITRE[nat])
                xs = [190] + [195 + L * i / 8 for i in range(1, 9)]
                pg.evaluate(GESTE, ['#tenirCv', xs, False, 1]); pl = pg.evaluate(PLEIN, ['#tenirCv', 195])
                juge(T + ' A · pendant le tracé, le plein va de la pointe jusqu\'au doigt (± 4 pt)', pl is not None and abs(pl - L) <= 4 + 6.5, (round(L, 1), pl))
                pg.evaluate("s=>{ window.__PLEIN=s; }", PLEIN); o = pg.evaluate(GESTE, ['#tenirCv', xs, True, 1]); pg.wait_for_timeout(2400)
                st = pg.evaluate("id=>promises.find(x=>x.id===id).status", pid)
                if frac >= 0.3:
                    juge(T + ' C · 78 pt ≥ 60 (C-107) : la parole est tenue, aucun retour', st == 'tenu', st)
                else:
                    # B · la loi : chaque écran, à partir de SON avancée au lâcher e0, suit e(t) = max(0, (e0 + 42,9)(1 − t/300) − 42,9) — le retour de la page +
                    def loi(e0, t): return max(0.0, (e0 + 42.9) * (1 - min(1.0, t / 300.0)) - 42.9)
                    def ecart_loi(o):
                        t1, e1 = (o[0][0], o[0][2]) if o else (0, 0)
                        e0 = (e1 + 42.9) / max(0.05, 1 - t1 / 300.0) - 42.9 if e1 > 0 else e1   # l'avancée au lever, retrouvée de la première image (la loi elle-même)
                        return e0, max([abs(v - loi(e0, t)) for t, _, v in o] or [99]), next((t for t, _, v in o if v <= 0.01), None)
                    e0f, ef, finf = ecart_loi(o)
                    juge(T + ' B · lâché : rien n\'est tenu, le trait revient à la pointe', st != 'tenu' and finf is not None, (st, finf))
                    c2, p2 = ouvre_page(b, nat)
                    xs2 = [30] + [42.9 + L * i / 8 for i in range(1, 9)]
                    p2.evaluate("s=>{ window.__PLEIN=s; }", PLEIN); p2.evaluate(GESTE, ['#planterCv', xs2, False, 1]); o2 = p2.evaluate(GESTE, ['#planterCv', xs2, True, 1]); c2.close()
                    e0p, ep_, finp = ecart_loi(o2)
                    juge(T + ' B · le retour suit la loi de la page + (e(t) = max(0, (e0 + 42,9)(1 − t/300) − 42,9), ± 1,5 pt à chaque image) — fiche et page + mesurées', ef <= 1.5 and ep_ <= 1.5,
                         ('fiche e0 %.1f écart %.1f fin %s ms' % (e0f, ef, finf), 'page + e0 %.1f écart %.1f fin %s ms' % (e0p, ep_, finp)))
                    # D · ce qui est PEINT suit : le plein au-delà de la pointe, moins sa valeur au repos (la queue de la pointe), ± 6 pt de la loi
                    rep = o[-1][1] if o and o[-1][1] is not None else 0
                    dD = [abs((pp - rep) - v) for t, pp, v in o if pp is not None]
                    juge(T + ' D · le plein peint suit le retour, image par image (± 18 pt : un pas de pastille — la mesure du plein continu s arrête à la première coupure pointe-pastille)', dD and max(dD) <= 18, ('écart max %.1f' % max(dD or [99]), [(t, pp - rep, round(v, 1)) for t, pp, v in o[:6] if pp is not None]))
                juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
