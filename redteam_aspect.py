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
  D · ⚑ v205 (Tom, C-286 : « un bandeau reste en haut des lettres pendant le détracé ») — chaque phrase DÉTRACÉE pas à pas (le mode manuel du module, 40 pas, de la
      phrase entière à rien) : à chaque pas, aucun pixel de la phrase hors de la boîte d'encre (± 2 px) des lettres pas encore parties — celles qui restent et
      celles en cours ; l'image finale est le fond au pixel (la phrase cachée). Le guide (ses quatre phrases), l'onboarding (prénom, parole, les quatre pas de
      « Promi planté ! »), la page + (la phrase, le libellé du trait) et une fiche (la phrase, le titre). Sur l'app seulement (la version d'avant n'a pas les boîtes).
--ref=<fichier> (défaut zz-ref-f562.html : `git show f56219a:app.html`) · --fichier= · --phrases=guide,onboarding,plus · --sonde (la phrase 2 en Atkinson : A rougit)
· --sonde-reste (le défaut d'avant v205 remis dans le module : D rougit) · --sans-d."""
import sys, os, subprocess, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in A_ if a.startswith('--ref=')), 'zz-ref-f562.html')
PH = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--phrases=')), ['guide', 'onboarding', 'plus'])
SONDE_R = '--sonde-reste' in A_; SANS_D = '--sans-d' in A_
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
# ---- D · le détracé pas à pas (C-286)
BLOCS = r"""(sel)=>{ const root=document.querySelector(sel); if(!root) return []; const out=[]; let n=0;
  const vis=e=>{ const r=e.getBoundingClientRect(); if(!(r.width>1&&r.height>1)) return false; for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } return true; };
  const dt=e=>[...e.childNodes].some(x=>x.nodeType===3 && x.nodeValue.trim());
  const deco=e=>{ const c=getComputedStyle(e); return (c.backgroundColor && c.backgroundColor!=='rgba(0, 0, 0, 0)' && c.backgroundColor!=='transparent') || (parseFloat(c.borderTopWidth)>0 && c.borderTopStyle!=='none') || (parseFloat(c.borderBottomWidth)>0 && c.borderBottomStyle!=='none'); };
  const pris=[]; [root].concat([...root.querySelectorAll('*')]).forEach(e=>{ if(pris.some(p=>p.contains(e))) return; if(!dt(e) || !vis(e) || deco(e)) return; if(e.closest('canvas,svg,button')) return; pris.push(e); });
  pris.forEach(b=>{ b.setAttribute('data-asp-d', String(n)); out.push('[data-asp-d="'+n+'"]'); n++; }); return out; }"""
PAS_D = r"""async (sel)=>{ const el=document.querySelector(sel); const T=window.TraceLettres; if(!el) return {n:0, tx:sel+" (disparu : la phrase s'est rebâtie)", bo:[], er:[0,0,1]}; const ctl=T.trace(el, null, {inverse:true, manuel:true});
  if(ctl && ctl.pret) await ctl.pret; await new Promise(r=>setTimeout(r, 250)); window.__C=ctl; const r=el.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect();
  const deco=[...el.querySelectorAll('*')].filter(e=>{ const c=getComputedStyle(e); return (c.backgroundColor && c.backgroundColor!=='rgba(0, 0, 0, 0)') || (parseFloat(c.borderTopWidth)>0 && c.borderTopStyle!=='none'); }).map(e=>{ const q=e.getBoundingClientRect(); return [q.left-D.left-2, q.top-D.top-2, q.right-D.left+2, q.bottom-D.top+2]; });
  return {n:(ctl.glyphes||[]).length, tx:(el.textContent||'').trim().slice(0,30), bo:(ctl.glyphes||[]).map(g=>g.bo||null), bc:(ctl.glyphes||[]).map(g=>g.bc||null), er:[r.left-D.left, r.top-D.top, el.offsetWidth? r.width/el.offsetWidth : 1], deco:deco}; }"""
def capture_d(pg, D, box):
    from PIL import Image; import io as _io
    return Image.open(_io.BytesIO(pg.screenshot(clip={'x': D[0] + box[0], 'y': D[1] + box[1], 'width': box[2] - box[0], 'height': box[3] - box[1]}))).convert('RGB')
def detrace_d(pg, sel, nom, N=40):
    from PIL import Image, ImageChops, ImageDraw
    D = B.dev(pg); info = pg.evaluate(PAS_D, sel); n = info['n']
    if not n or any(b is None for b in info['bo']): pg.evaluate("()=>{ try{ __C.stop(); }catch(e){} }"); print('   (D non jugé : « %s », %d glyphes)' % (info['tx'], n), flush=True); return None
    er = info['er']; kk = er[2]; BO = [[er[0] + b[0] * kk, er[1] + b[1] * kk, er[0] + b[2] * kk, er[1] + b[3] * kk] for b in info['bo']]
    BC = [([er[0] + b[0] * kk, er[1] + b[1] * kk, er[0] + b[2] * kk, er[1] + b[3] * kk] if b else None) for b in info.get('bc') or [None] * n]   # la boîte d'encre réelle (avec 3 px de marge) : permise aussi
    m = 24; box = [min(b[0] for b in BO) - m, min(b[1] for b in BO) - m, max(b[2] for b in BO) + m, max(b[3] for b in BO) + m]
    pg.evaluate(SEULE, sel); pg.evaluate("()=>{ const s=document.getElementById('__asp'); if(s) s.textContent+=' canvas[data-trace]{visibility:visible!important; opacity:1!important}'; }")   # la phrase seule sur un fond plat, le canevas du tracé compris (le fond de l'app respire)
    pg.evaluate("(s)=>{ __C.va(1); const e=document.querySelector(s); e.__cp=e.style.getPropertyValue('clip-path'); e.__cpP=e.style.getPropertyPriority('clip-path'); e.style.setProperty('clip-path','polygon(0px 0px, 0px 0px, 0px 0px)','important'); }", sel); pg.wait_for_timeout(150)
    vide = capture_d(pg, D, box); pg.evaluate("(s)=>{ const e=document.querySelector(s); if(e.__cp) e.style.setProperty('clip-path', e.__cp, e.__cpP); else e.style.removeProperty('clip-path'); }", sel); pg.wait_for_timeout(120)   # le fond : la phrase entière coupée (une découpe vide coupe aussi les descendants, `visibility` non)   # le fond : la phrase cachée (son style en ligne : l'app y pose ses couleurs en important)
    sc = vide.size[0] / (box[2] - box[0]); mauvais = []
    for i in range(N + 1):
        pg.evaluate("(p)=>{ __C.va(p); }", 1 - i / N); pg.wait_for_timeout(40)
        e = pg.evaluate("()=>__C.etat()"); im = capture_d(pg, D, box)
        pres = [j for j in range(n) if j < e['glyphe'] or j in e['actives']]
        d = ImageChops.difference(im, vide).convert('L').point(lambda v: 255 if v > 40 else 0)
        mk = Image.new('L', d.size, 0); dr = ImageDraw.Draw(mk)
        for j in pres:
            if BC[j]: c = BC[j]; dr.rectangle([(c[0] - box[0]) * sc, (c[1] - box[1]) * sc, (c[2] - box[0]) * sc, (c[3] - box[1]) * sc], fill=255)
        for j in pres: b = BO[j]; dr.rectangle([(b[0] - box[0] - 2) * sc, (b[1] - box[1] - 2) * sc, (b[2] - box[0] + 2) * sc, (b[3] - box[1] + 2) * sc], fill=255)
        for b in info.get('deco') or []: dr.rectangle([(b[0] - box[0]) * sc, (b[1] - box[1]) * sc, (b[2] - box[0]) * sc, (b[3] - box[1]) * sc], fill=255)   # le décor d'un descendant (une pastille) : il part avec la découpe, ce n'est pas une lettre
        h = ImageChops.subtract(d, mk).histogram()[255]
        if h > 4:
            mauvais.append((round(i / N, 2), h))
            if os.environ.get('ASP_D') and len(mauvais) == 3:
                ov = im.copy(); dr2 = ImageDraw.Draw(ov)
                for j in pres: b = BO[j]; dr2.rectangle([(b[0] - box[0] - 2) * sc, (b[1] - box[1] - 2) * sc, (b[2] - box[0] + 2) * sc, (b[3] - box[1] + 2) * sc], outline=(255, 0, 0))
                ov.save('scratchpad/v205/d-%s.png' % info['tx'][:10].replace(' ', '_').replace('’', ''))
                vide.save('scratchpad/v205/v-%s.png' % info['tx'][:10].replace(' ', '_').replace('’', '')); im.save('scratchpad/v205/i-%s.png' % info['tx'][:10].replace(' ', '_').replace('’', ''))
                ImageChops.subtract(d, mk).save('scratchpad/v205/h-%s.png' % info['tx'][:10].replace(' ', '_').replace('’', '')); d.save('scratchpad/v205/dm-%s.png' % info['tx'][:10].replace(' ', '_').replace('’', ''))
    fin = ImageChops.difference(capture_d(pg, D, box), vide).convert('L').point(lambda v: 255 if v > 24 else 0).histogram()[255]
    pg.evaluate(DEFAIT); pg.evaluate("()=>{ try{ __C.stop(); }catch(e){} }"); pg.wait_for_timeout(150)
    juge('%s · D · « %s » : détracé pas à pas, aucun reste hors des lettres pas encore parties ; l’image finale = le fond' % (nom, info['tx']), not mauvais and fin <= 4,
         '%d pas en défaut %s · image finale %d px' % (len(mauvais), mauvais[:3], fin))
    return not mauvais and fin <= 4
COPIES = r"""(sel)=>{ const root=document.querySelector(sel); if(!root) return null; const dev=document.getElementById('device'), D=dev.getBoundingClientRect(), k=D.width/390;
  const box=document.createElement('div'); box.id='__aspCopies'; box.style.cssText='position:absolute;left:0;top:0;width:390px;height:844px;pointer-events:none;z-index:2147483000;';
  const tw=document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n, i=0;
  while((n=tw.nextNode())){ const t=(n.nodeValue||''); if(!t.trim()) continue; const e=n.parentElement, c=getComputedStyle(e); if(c.visibility==='hidden'||+c.opacity<0.05) continue;
    const rg=document.createRange(); rg.selectNodeContents(n); const R=[...rg.getClientRects()].filter(r=>r.width>0.5); if(R.length!==1) continue; const r=R[0];
    const s=document.createElement('span'); s.textContent=t.trim(); s.setAttribute('data-asp-d', String(i++));
    ['position:absolute','white-space:pre','margin:0','padding:0','border:0','background:transparent','line-height:normal','font-family:'+c.fontFamily,'font-size:'+(parseFloat(c.fontSize)*(r.height?1:1))+'px','font-weight:'+c.fontWeight,'font-style:'+c.fontStyle,'letter-spacing:'+c.letterSpacing,'color:'+c.color,'-webkit-text-fill-color:'+(c.webkitTextFillColor||c.color)].forEach(d=>{ const j=d.indexOf(':'); s.style.setProperty(d.slice(0,j), d.slice(j+1), 'important'); });
    box.appendChild(s); s.__r=r; }
  dev.appendChild(box); const sc=box.getBoundingClientRect().width/390;
  [...box.children].forEach(s=>{ const r=s.__r, q=s.getBoundingClientRect(); s.style.setProperty('left', ((r.left-D.left)/sc)+'px','important'); s.style.setProperty('top', ((r.top-D.top)/sc)+'px','important'); const q2=s.getBoundingClientRect(); s.style.setProperty('left', ((r.left-D.left)/sc + (r.left-q2.left)/sc)+'px','important'); s.style.setProperty('top', ((r.top-D.top)/sc + (r.top-q2.top)/sc)+'px','important'); });
  return [...box.children].map(s=>'#__aspCopies [data-asp-d="'+s.getAttribute('data-asp-d')+'"]'); }"""
def copies_d(pg, root, nom, fichier):
    if SANS_D or fichier != F: return
    pg.evaluate("()=>{ window._vivantOff=1; }")
    if SONDE_R: pg.evaluate("()=>{ TraceLettres.__sondeReste=1; }")
    L = pg.evaluate(COPIES, root) or []
    if not L: print('   (D : aucun mot sous %s)' % root, flush=True)
    for s in L: detrace_d(pg, s, nom)
    pg.evaluate("()=>{ const b=document.getElementById('__aspCopies'); if(b) b.remove(); }")
def tout_d(pg, root, nom, fichier):
    if SANS_D or fichier != F: return
    pg.evaluate("()=>{ window._vivantOff=1; }")
    if SONDE_R: pg.evaluate("()=>{ TraceLettres.__sondeReste=1; }")
    L = pg.evaluate(BLOCS, root)
    if not L: print('   (D : aucun texte sous %s)' % root, flush=True)
    for s in L: detrace_d(pg, s, nom)
    pg.evaluate("()=>{ document.querySelectorAll('[data-asp-d]').forEach(e=>e.removeAttribute('data-asp-d')); }")
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
    pg.evaluate(REPOS, '#guidePhrase'); out['guide · Studio'] = photo(pg, '#guidePhrase'); tout_d(pg, '#guidePhrase', 'guide · Studio', fichier)
    e = pg.evaluate("()=>_guide.etat()"); out['départ · Studio'] = depart(pg, out['guide · Studio'][0], lambda: B.tap(pg, e['trou']['x'], e['trou']['y'])); B.tap_sel(pg, '#studioScreen .closeb')
    if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1 && document.getElementById('guidePhrase'); }"):
        pg.evaluate(REPOS, '#guidePhrase'); out['guide · +'] = photo(pg, '#guidePhrase'); tout_d(pg, '#guidePhrase', 'guide · +', fichier)
        out['départ · +'] = depart(pg, out['guide · +'][0], lambda: B.tap(pg, 195, 300))
        if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='partage' && document.getElementById('guidePhrase'); }"):
            pg.wait_for_timeout(400); pg.evaluate(REPOS, '#guidePhrase'); out['guide · Partager'] = photo(pg, '#guidePhrase'); tout_d(pg, '#guidePhrase', 'guide · Partager', fichier)
            out['départ · Partager'] = depart(pg, out['guide · Partager'][0], lambda: B.tap(pg, 195, 300))
            if at("()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='reste' && document.getElementById('guidePhrase'); }"):
                pg.wait_for_timeout(300); pg.evaluate(REPOS, '#guidePhrase'); out['guide · « Le reste s’explore »'] = photo(pg, '#guidePhrase')
                out['départ · « Le reste s’explore »'] = depart(pg, out['guide · « Le reste s’explore »'][0], lambda: B.tap(pg, 195, 300))
    ctx.close(); return out
exec(open('redteam_onb_toucher.py', encoding='utf-8').read().split('def jusquau_titre')[1].split('with sync_playwright')[0].join(['def jusquau_titre', '']))
def onboarding(b, fichier):
    ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, fichier, attente=7000); out = {}
    pg.evaluate(REPOS, '#onbV'); pg.wait_for_timeout(500); out['onb · prénom'] = photo(pg, '#onbV'); tout_d(pg, '#onbV', 'onb · prénom', fichier)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1600)
    B.attend_parole(pg); pg.evaluate(REPOS, '#onbV'); out['onb · la parole'] = photo(pg, '#onbV'); tout_d(pg, '#onbV', 'onb · la parole', fichier)
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
        if i == 3: tout_d(pg, '#onbFin', 'onb · Promi planté !', fichier)
        if i < 3: B.tap(pg, 195, 300); pg.wait_for_timeout(1500)
    ctx.close(); return out
def plus(b, fichier):
    """D seulement : la phrase de la page + d'un Promi, puis la phrase et le titre d'une fiche"""
    if fichier != F or SANS_D: return {}
    ctx = B.contexte(b); pg = B.ouvre(ctx, fichier); B.plante_doigt(pg, 'appeler Marion dimanche')
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(350)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(650); B.tap_sel(pg, '.acc-pil[data-k=promi]')
    for _ in range(40):
        pg.wait_for_timeout(120)
        if pg.evaluate("()=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-promi') && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }"): break
    pg.wait_for_timeout(1500); pg.evaluate(REPOS, '#createSheet .ph-txt'); copies_d(pg, '#createSheet .ph-txt', 'page + · Promi', fichier)
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ var p=promises.filter(x=>!x.brouillon)[0]; if(p) openDetail(p.id); }"); pg.wait_for_timeout(2500)
    pg.evaluate(REPOS, '#dptTitre'); tout_d(pg, '#dptQui', 'fiche · la phrase', fichier); tout_d(pg, '#dptTitre', 'fiche · le titre', fichier)
    ctx.close(); return {}
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
    if 'plus' in PH: plus(b, F)
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
