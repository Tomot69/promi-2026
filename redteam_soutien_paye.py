#!/usr/bin/env python3
"""redteam_soutien_paye.py — v214b (Tom, 19 nov. 2026, C-319) : « Soutenir Promi », le paiement validé.
Décisions EN DUR : payé (un montant de la rangée, un palier, un montant tapé), il ne reste QUE le prix payé, remonté sous le texte et centré ; dessous, « Un grand » en Gilbert
et « Merci » en PromiLate, centré. Aucun changement sec (C-271) : à l'image qui suit le geste, les autres montants sont encore là (ils se referment), le prix payé glisse
d'un seul mouvement. Clair et sombre, échelles 1 (430 × 932) et 0,79 (330 × 714). Rouvert, l'écran est celui d'avant. `--sonde` : la transition retirée (tout change d'un coup)."""
import sys
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
SONDE = '--sonde' in sys.argv
OK = []; KO = []
def juge(nom, c, det=''):
    (OK if c else KO).append(nom); print(('  ✅ ' if c else '  ❌ ') + nom + ('' if c else '  — ' + str(det)))
RELEVE = """()=>{ window.__pR=[]; var s=document.getElementById('soutienScreen'), t0=performance.now();
  (function f(){ var k=s.getBoundingClientRect().width/(s.offsetWidth||1), L=[].slice.call(s.querySelectorAll('.so-m')).filter(function(e){ var r=e.getBoundingClientRect(); return r.height>1 && getComputedStyle(e).visibility!=='hidden'; }).map(function(e){ var r=e.getBoundingClientRect(); return {c:e.classList.contains('so-copie'), g:e.classList.contains('so-glisse'), p:e.classList.contains('so-paye-m'), x:r.left/k, y:r.top/k, h:r.height/k}; });
    window.__pR.push({t:performance.now()-t0, n:L.length, L:L}); if(performance.now()-t0<1200) requestAnimationFrame(f); })(); }"""
FIN = """()=>{ var s=document.getElementById('soutienScreen'), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, cx=(d.left+d.right)/2;
  var vis=[].slice.call(s.querySelectorAll('.so-m, .so-autre')).filter(function(e){ var r=e.getBoundingClientRect(); return r.height>1 && getComputedStyle(e).visibility!=='hidden'; });
  var pm=s.querySelector('.so-paye-m'), m=s.querySelector('.so-merci'), tx=s.querySelector('.so-tx'), r=pm.getBoundingClientRect(), rm=m.getBoundingClientRect(), rt=tx.getBoundingClientRect();
  var g=getComputedStyle(m.querySelector('.so-mg')).fontFamily, pl=getComputedStyle(m.querySelector('.so-mm')).fontFamily;
  return {n:vis.length, txt:pm.textContent, mt:m.textContent.replace(/\\s+/g,' ').trim(), dpm:((r.left+r.right)/2-cx)/k, dm:((rm.left+rm.right)/2-cx)/k, air1:(r.top-rt.bottom)/k, air2:(rm.top-r.bottom)/k,
    vis:getComputedStyle(m).visibility, g:g, pl:pl, dans: rm.bottom<=d.bottom && r.left>=d.left && r.right<=d.right, copies:s.querySelectorAll('.so-copie').length}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre, vw, vh, ech in ((False, 430, 932, '1'), (True, 430, 932, '1'), (False, 330, 714, '0,79'), (True, 330, 714, '0,79')):
        for mode in ('rangée', 'palier', 'tapé'):
            tag = '%s · %s · %s' % ('sombre' if sombre else 'clair', ech, mode)
            ctx = B.contexte(b, sombre=sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, 'app.html'); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
            if SONDE: pg.evaluate("()=>{Element.prototype.animate=function(){ var a={onfinish:null, cancel:function(){}}; setTimeout(()=>a.onfinish&&a.onfinish(),0); return a; };}")
            pg.evaluate("()=>{closeAll(); document.getElementById('settingsBtn').click(); setTimeout(()=>window._soutienPage(),600)}"); pg.wait_for_timeout(1800)
            att = {'rangée': '50 €', 'palier': '200 €', 'tapé': '42 €'}[mode]
            if mode == 'rangée': pg.evaluate(RELEVE); B.tap_sel(pg, '#soutienScreen .so-mts .so-m:nth-child(4)')
            elif mode == 'palier': B.tap_sel(pg, '#soutienScreen .so-autre'); pg.wait_for_timeout(900); pg.evaluate(RELEVE); B.tap_sel(pg, '#soutienScreen .so-autres .so-m:nth-child(6)')
            else: B.tap_sel(pg, '#soutienScreen .so-autre'); pg.wait_for_timeout(700); pg.keyboard.type('42'); pg.evaluate(RELEVE); pg.keyboard.press('Enter')
            pg.wait_for_timeout(2600)
            R = pg.evaluate("()=>window.__pR")
            i0 = next((i for i, f in enumerate(R) if any(x['c'] for x in f['L'])), None)
            juge(tag + ' : à l\'image qui suit le geste, les autres montants sont encore là (ils se referment, rien ne disparaît d\'un coup)', i0 is not None and R[i0]['n'] >= 3, [f['n'] for f in R[:6]])
            P = [next((x for x in f['L'] if x.get('g')), None) for f in R]
            ys = [x['y'] for x in P if x] if i0 is not None else []
            mv = (max(ys) - min(ys)) if ys else 0
            pas = max([abs(ys[i+1] - ys[i]) for i in range(len(ys)-1)] or [0])
            if mode != 'rangée' or mv > 2:
                juge(tag + ' : le prix payé glisse d\'un seul mouvement (%.0f pt, au moins 5 images, aucun pas > 45 %%)' % mv, len(ys) >= 5 and pas <= 0.45 * max(mv, 1), (len(ys), pas, mv))
            F = pg.evaluate(FIN)
            juge(tag + ' : il ne reste que le prix payé (%s)' % att, F['n'] == 1 and F['txt'] == att.replace(' ', ' ') and F['copies'] == 0, F)
            juge(tag + ' : le prix payé et « Un grand Merci » centrés (± 0,5 pt), le prix 28 pt sous le texte, le merci 24 pt sous le prix', abs(F['dpm']) <= 0.5 and abs(F['dm']) <= 0.5 and abs(F['air1'] - 28) <= 1 and abs(F['air2'] - 24) <= 1, F)
            juge(tag + ' : « Un grand » en Gilbert, « Merci » en PromiLate, visible, dans l\'écran', F['mt'] == 'Un grand Merci' and F['g'].startswith('Gilbert') and F['pl'].startswith('PromiLate') and F['vis'] == 'visible' and F['dans'], F)
            pg.evaluate("()=>{ document.querySelector('#soutienScreen .closeb').click(); setTimeout(()=>window._soutienPage(),500); }"); pg.wait_for_timeout(1200)
            juge(tag + ' : rouvert, l\'écran d\'avant (six montants, « Autre montant », pas de merci)', pg.evaluate("()=>{var s=document.getElementById('soutienScreen'); return !s.classList.contains('so-paye') && s.querySelectorAll('.so-mts .so-m').length>=6 && s.querySelector('.so-autre').getBoundingClientRect().height>1 && getComputedStyle(s.querySelector('.so-merci')).visibility==='hidden'}"))
            juge(tag + ' : aucune erreur de page', not err, err[:2])
            ctx.close()
    b.close()
print('\n%d/%d' % (len(OK), len(OK) + len(KO)))
sys.exit(1 if KO else 0)
