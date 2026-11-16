# -*- coding: utf-8 -*-
"""⚑ v203 clôture (Tom, C-285) — GARDE-FOU PERMANENT DE LA PORTE A1 : L'ASPECT AU REPOS NE CHANGE PAS SANS DEMANDE.
« Pour CHAQUE phrase et CHAQUE écran touchés par un lot, une capture au repos (fin d'animation) comparée au pixel à la version d'avant, sur la police, la
couleur, la taille et la place. Tout écart non demandé fait échouer A1. Commence par toutes les phrases du guide et de l'onboarding, contre f56219a. »

WebKit, 390 × 844 ×3, au doigt (banc_tom). Pour chaque phrase, AU REPOS (son tracé fini, plus rien ne bouge depuis 600 ms) :
  A · chaque morceau de texte (le plus petit élément qui porte du texte) : son texte, sa police, sa taille, sa graisse, sa couleur (color et -webkit-text-fill-color),
      sa place (± 0,5 pt) — identiques à la version d'avant ;
  B · l'image de la phrase seule (tout le reste de l'écran rendu transparent, sur un fond plat) : au plus 0,5 % de pixels qui diffèrent de plus de 24 niveaux.
Phrases : le guide (Studio, +, Partager, « Le reste s'explore à ton rythme ! ») ; l'onboarding (« Toi, c'est ton prénom ? », la page de la parole, « Promi planté ! »
et ses trois pas, dont « La suite t'appartient. »).
--ref=<fichier> (défaut zz-ref-f562.html : `git show f56219a:app.html`) · --fichier= · --phrases=guide,onboarding · --sonde (la phrase 2 en Atkinson : A rougit)."""
import sys, os, subprocess, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in A_ if a.startswith('--ref=')), 'zz-ref-f562.html')
PH = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--phrases=')), ['guide', 'onboarding'])
SONDE = '--sonde' in A_
if REF == 'zz-ref-f562.html' and not os.path.exists(REF):
    open(REF, 'w', encoding='utf-8').write(subprocess.run(['git', 'show', 'f56219a:app.html'], capture_output=True, text=True).stdout)
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
# le relevé : chaque morceau de texte visible d'un conteneur
RELEVE = r"""(sel)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, root=document.querySelector(sel); if(!root) return null;
  const out=[]; const vis=e=>{ for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } return true; };
  const tw=document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n; while((n=tw.nextNode())){ const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t) continue; const e=n.parentElement; if(!e || !vis(e)) continue;
    const rg=document.createRange(); rg.selectNodeContents(n); const r=rg.getBoundingClientRect(); if(!(r.width>0.5)) continue; const c=getComputedStyle(e);
    out.push({t:t, f:c.fontFamily.split(',')[0].replace(/['"]/g,'').trim(), s:+(parseFloat(c.fontSize)*(parseFloat(c.scale)||1)).toFixed(2), w:c.fontWeight, st:c.fontStyle, c:c.color, fc:c.webkitTextFillColor, x:+((r.left-D.left)/k).toFixed(1), y:+((r.top-D.top)/k).toFixed(1), l:+(r.width/k).toFixed(1)}); }
  const R=root.getBoundingClientRect(); return {m:out, b:[(R.left-D.left)/k, (R.top-D.top)/k, R.width/k, R.height/k]}; }"""
# C · pendant le DÉTRACÉ (la phrase qui part, `.gd-part`) : chaque morceau garde la police, la taille, la graisse et les couleurs qu'il avait au repos (C-284 §2 : la phrase
#   de Partager retombait en Atkinson pendant son départ) — relevé à chaque image, après la peinture
DEPART = r"""(rest)=>{ window.__DEP={n:0, ec:[]}; const t0=performance.now(), mc=new MessageChannel();
  mc.port1.onmessage=()=>{ document.querySelectorAll('#guide .gd-part').forEach(p=>{ const L=[]; const tw=document.createTreeWalker(p, NodeFilter.SHOW_TEXT); let n; while((n=tw.nextNode())){ const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t) continue; const e=n.parentElement, c=getComputedStyle(e); L.push({t:t, f:c.fontFamily.split(',')[0].replace(/['"]/g,'').trim(), s:+(parseFloat(c.fontSize)*(parseFloat(c.scale)||1)).toFixed(2), w:c.fontWeight, c:c.color, fc:c.webkitTextFillColor}); }
      const R=rest.filter(x=>L.some(y=>y.t===x.t)); window.__DEP.n++; L.forEach(y=>{ const x=rest.find(r=>r.t===y.t); if(!x) return; ['f','s','w','c','fc'].forEach(k=>{ if(x[k]!==y[k] && !(k==='s'&&Math.abs(x[k]-y[k])<=0.1)) { const m='« '+y.t.slice(0,16)+' » '+k+' : '+x[k]+' → '+y[k]; if(window.__DEP.ec.indexOf(m)<0) window.__DEP.ec.push(m); } }); }); }); };
  (function f(){ mc.port2.postMessage(0); if(performance.now()-t0<2500) requestAnimationFrame(f); })(); }"""
def depart(pg, rest, toucher):
    pg.evaluate(DEPART, rest); toucher(); pg.wait_for_timeout(2700); return pg.evaluate("()=>window.__DEP")
# la phrase seule : tout le reste transparent, un fond plat
SEULE = r"""(sel)=>{ const root=document.querySelector(sel); if(!root) return false; const st=document.createElement('style'); st.id='__asp';
  st.textContent='body *{visibility:hidden!important} html, body, body *, body *::before, body *::after{background:transparent!important; background-image:none!important; box-shadow:none!important; filter:none!important; backdrop-filter:none!important; -webkit-backdrop-filter:none!important} html, body{background:#808080!important} canvas{opacity:0!important} '+sel+', '+sel+' *{visibility:visible!important} '+sel+' canvas{opacity:1!important}';
  document.head.appendChild(st); document.getElementById('device').style.setProperty('background','#808080','important'); return true; }"""
DEFAIT = "()=>{ const s=document.getElementById('__asp'); if(s) s.remove(); document.getElementById('device').style.removeProperty('background'); }"
REPOS = r"""(sel)=>new Promise(res=>{ const t0=performance.now(); let av=null, calme=performance.now();
  (function f(){ const r=document.querySelector(sel); const T=window.TraceLettres, act=T && T.actif && T.actif(); let s=r?JSON.stringify([r.getBoundingClientRect().top, r.innerHTML.length, getComputedStyle(r).opacity]):'';
    if(s!==av || act){ av=s; calme=performance.now(); } if(performance.now()-calme>600 && r) return res(true); if(performance.now()-t0>9000) return res(false); requestAnimationFrame(f); })(); })"""
def photo(pg, sel):
    b = pg.evaluate(RELEVE, sel)
    if not b: return None, None
    pg.evaluate(SEULE, sel); pg.wait_for_timeout(120)
    D = pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390]; }")
    x, y, w, h = b['b']; k = D[2]
    img = pg.screenshot(clip={'x': D[0] + (x - 4) * k, 'y': D[1] + (y - 4) * k, 'width': (w + 8) * k, 'height': (h + 8) * k})
    pg.evaluate(DEFAIT); return b['m'], img
def diff_img(a, b):
    from PIL import Image, ImageChops; import io as _io
    A = Image.open(_io.BytesIO(a)).convert('RGB'); Bi = Image.open(_io.BytesIO(b)).convert('RGB')
    if A.size != Bi.size: Bi = Bi.resize(A.size)
    d = ImageChops.difference(A, Bi).convert('L'); h = d.histogram(); n = sum(h); return sum(h[25:]) / max(1, n)
# ---- les parcours
def guide(b, fichier):
    """rend {nom: (morceaux, image)} pour les quatre phrases du guide"""
    ctx = B.contexte(b, onb=True, guide=False); pg = B.ouvre(ctx, fichier)
    if SONDE and fichier == F: pg.add_style_tag(content="#guide[data-guide=reste] #guidePhrase, #guide[data-guide=reste] #guidePhrase *{font-family:Atkinson!important}")
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(300); out = {}
    def at(js, n=200):
        for _ in range(n):
            if pg.evaluate(js): return True
            pg.wait_for_timeout(100)
        return False
    pg.evaluate("()=>{ _guide.attend(false); }")
    if not at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='studio' && g.getAttribute('data-entier') && document.getElementById('guidePhrase'); }"): ctx.close(); return out
    pg.evaluate(REPOS, '#guidePhrase'); out['guide · Studio'] = photo(pg, '#guidePhrase')
    e = pg.evaluate("()=>_guide.etat()"); out['départ · Studio'] = depart(pg, out['guide · Studio'][0], lambda: B.tap(pg, e['trou']['x'], e['trou']['y'])); B.tap_sel(pg, '#studioScreen .closeb')
    if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1 && document.getElementById('guidePhrase'); }"):
        pg.evaluate(REPOS, '#guidePhrase'); out['guide · +'] = photo(pg, '#guidePhrase')
        out['départ · +'] = depart(pg, out['guide · +'][0], lambda: B.tap(pg, 195, 300))
        if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='partage' && document.getElementById('guidePhrase'); }"):
            pg.wait_for_timeout(400); pg.evaluate(REPOS, '#guidePhrase'); out['guide · Partager'] = photo(pg, '#guidePhrase')
            out['départ · Partager'] = depart(pg, out['guide · Partager'][0], lambda: B.tap(pg, 195, 300))
            if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='reste' && document.getElementById('guidePhrase'); }"):
                pg.wait_for_timeout(300); pg.evaluate(REPOS, '#guidePhrase'); out['guide · « Le reste s’explore »'] = photo(pg, '#guidePhrase')
                out['départ · « Le reste s’explore »'] = depart(pg, out['guide · « Le reste s’explore »'][0], lambda: B.tap(pg, 195, 300))
    ctx.close(); return out
exec(open('redteam_onb_toucher.py', encoding='utf-8').read().split('def jusquau_titre')[1].split('with sync_playwright')[0].join(['def jusquau_titre', '']))
def onboarding(b, fichier):
    ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, fichier, attente=7000); out = {}
    pg.evaluate(REPOS, '#onbV'); pg.wait_for_timeout(500); out['onb · prénom'] = photo(pg, '#onbV')
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1600)
    B.attend_parole(pg); pg.evaluate(REPOS, '#onbV'); out['onb · la parole'] = photo(pg, '#onbV')
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500); pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(4500)
    pg.evaluate(REPOS, '#onbV'); out['onb · la parole validée'] = photo(pg, '#onbV')
    z = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {l:(r.left-D.left)/k+0, t:(r.top-D.top)/k, k:1, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee'), L:r.left, T:r.top, K:k}; }")
    if not z or not z.get('dep') or not z.get('arr'): ctx.close(); return out
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0], z['t'] + a[1], z['l'] + (e[0] + 6), z['t'] + e[1]
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
    try: pg.wait_for_function("()=>!!document.getElementById('onbFin')", timeout=30000)
    except Exception: ctx.close(); return out
    pg.wait_for_timeout(5600)
    for i in range(4):
        for _ in range(60):
            if not pg.evaluate("()=>{ const f=_onbFinPas(); return f&&f.enCours; }"): break
            pg.wait_for_timeout(200)
        pg.evaluate(REPOS, '#onbFin'); pg.wait_for_timeout(300); out['onb · Promi planté ! · pas %d' % i] = photo(pg, '#onbFin')
        if i < 3: B.tap(pg, 195, 300); pg.wait_for_timeout(1500)
    ctx.close(); return out
def compare(nom, a, r):
    ma, ia = a; mr, ir = r
    if ma is None or mr is None: juge(nom + ' · relevé', False, 'app %s · réf %s' % (ma is not None, mr is not None)); return
    ecarts = []
    if len(ma) != len(mr): ecarts.append('%d morceaux contre %d' % (len(ma), len(mr)))
    for x, y in zip(ma, mr):
        for c in ('t', 'f', 's', 'w', 'st', 'c', 'fc'):
            if x[c] != y[c] and not (c == 's' and abs(x[c] - y[c]) <= 0.1): ecarts.append('« %s » %s : %s → %s' % (y['t'][:24], c, y[c], x[c]))
        for c in ('x', 'y', 'l'):
            if abs(x[c] - y[c]) > 0.5: ecarts.append('« %s » %s : %s → %s' % (y['t'][:24], c, y[c], x[c]))
    juge(nom + ' · A · police, taille, couleur, place de chaque morceau', not ecarts, ecarts[:6])
    if os.environ.get('ASP_GARDE'):
        n2 = nom.replace(' ', '_').replace('«', '').replace('»', '').replace('’', '')[:40]; open('scratchpad/v204/asp-%s-app.png' % n2, 'wb').write(ia); open('scratchpad/v204/asp-%s-ref.png' % n2, 'wb').write(ir)
    try: p = diff_img(ia, ir)
    except Exception as ex: p = None
    juge(nom + ' · B · la phrase seule, au pixel (≤ 0,5 %)', p is not None and p <= 0.005, p if p is None else '%.2f %%' % (100 * p))
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_aspect — %s contre %s · charge %.1f' % (F, REF, B.charge()), flush=True)
    for nomp, fn in (('guide', guide), ('onboarding', onboarding)):
        if nomp not in PH: continue
        A = fn(b, F); R = fn(b, REF)
        for k in R:
            if k.startswith('départ'):
                d = A.get(k); juge(k + ' · C · pendant le détracé, chaque morceau garde son aspect du repos', d and d['n'] > 3 and not d['ec'], d and (d['ec'][:4] or '%d images' % d['n']))
                continue
            if k in A: compare(k, A[k], R[k])
            else: juge(k + ' · présente', False, 'absente de l’app')
        for k in A:
            if k not in R and not k.startswith('départ'): juge(k + ' · présente dans la référence', False, 'absente de la référence')
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
sys.exit(0 if all(RES) else 1)
