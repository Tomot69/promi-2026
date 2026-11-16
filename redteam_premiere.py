"""⚑ v203 clôture (Tom, C-282 régression) — À LA PREMIÈRE LETTRE, LA PHRASE TAPÉE NE SE SUPERPOSE JAMAIS À L'EXEMPLE QUI PART.
« Pour le détracé déclenché par la première lettre : il dure deux fois moins que le détracé standard, avec la même courbe ; la zone où s'écrit la lettre tapée est
libérée en premier ; la fin s'éteint en douceur, sans coupure sèche à la dernière image ; la lettre tapée paraît immédiatement ; à aucune image elle ne chevauche une
lettre de l'exemple. Le même code pour l'onboarding et la page +. Juge : taper la première lettre à 0, 50, 150 et 400 ms après la fin du tracé de l'exemple, puis
taper vite 5 lettres. À chaque image, aucun rectangle de lettre tapée ne recouvre un pixel de l'exemple. Durée du détracé égale à la moitié du standard. Dernière image
sans saut d'opacité. Dans l'onboarding et sur la page +. »
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé. Onboarding (la parole) et page + d'un Promi (le titre), ×4 délais. Relevé dans la page, à chaque image :
la boîte du texte tapé (`.v203-txt`, curseur compris), la découpe du conteneur de la copie (`.v203-exw`), l'encre restante sur le canevas du détracé.
  A · la lettre tapée est dans la place à l'image qui suit la touche
  B · à chaque image, la boîte du texte tapé est DANS la zone retirée de la copie (rien de l'exemple ne peut la recouvrir)
  C · la durée du détracé = la moitié de celle d'un tracé standard du même texte (± 15 %)
  D · la fin s'éteint en douceur : à la dernière image peinte, l'encre restante du canevas est ≤ 6 % de son maximum pendant le détracé (aucune coupure sèche)
--sonde (le conteneur sans découpe : B rougit) · --fichier="""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__P={traces:[]}; (function a(){ const T=window.TraceLettres; if(!T||!T.trace){ setTimeout(a,50); return; } if(T.__p) return; T.__p=1; const o=T.trace;
  T.trace=function(el, c, op){ const r=o.apply(this, arguments); try{ if(!(op&&op.preparer) && el && el.closest && (el.closest('.v203-ex') || el.closest('#onbPh .onbv-pm, #csPhrase [data-ph=titre]'))){ const rec={t:performance.now(), inv:!!(op&&op.inverse), ex:!!el.closest('.v203-ex'), n:(el.textContent||'').trim().length, vit:(op&&op.vitesse)||1};
      window.__P.traces.push(rec); if(r && r.fin) r.fin.then(()=>{ rec.fin=performance.now(); rec.prevu=r.mesure&&r.mesure.prevu; rec.reel=r.mesure&&r.mesure.reel; }); } }catch(e){} return r; }; })(); })();"""
SONDE = "(()=>{ const o=CSSStyleDeclaration.prototype.setProperty; CSSStyleDeclaration.prototype.setProperty=function(k,v,p){ if(/clip-path/.test(k) && /evenodd/.test(String(v))) return; return o.call(this,k,v,p); }; })();"   # la copie sans sa découpe (aucune zone retirée)
REC = r"""(sel)=>{ window.__I=[]; window.__K=null; document.addEventListener('input', function k(){ if(window.__K==null) window.__K=performance.now(); }, true);
  const t0=performance.now(), mc=new MessageChannel(); mc.port1.onmessage=()=>lis(); function f(){ mc.port2.postMessage(0); } function lis(){ const now=performance.now(), w=document.querySelector('.v203-exw'), pl=document.querySelector(sel);   /* lu APRÈS l'image (v123) : l'état peint */
    let hole=null, ink=null, tb=null;
    if(w){ const cp=getComputedStyle(w).clipPath||''; const W=w.getBoundingClientRect(), k=(window.__sc||1); hole=[];
      const re=/M\s*([-\d.]+)\s+([-\d.]+)\s+H\s*([-\d.]+)\s+V\s*([-\d.]+)/g; let m; while((m=re.exec(cp))){ if(+m[1]<=-9999) continue; hole.push([W.left+(+m[1])*k, W.top+(+m[2])*k, W.left+(+m[3])*k, W.top+(+m[4])*k]); }
      const cv=w.querySelector('canvas[data-trace]'); if(cv && cv.width){ try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>40) n++; ink=n; }catch(e){} } }
    if(pl){ const rg=document.createRange(); rg.selectNodeContents(pl); const Q=[...rg.getClientRects()].filter(q=>q.width>0.5&&q.height>0.5); if(Q.length) tb=Q.map(q=>[q.left,q.top,q.right,q.bottom]); }
    window.__I.push({t:now, w:!!w, hole:hole, ink:ink, tb:tb, txt:pl?(pl.textContent||'').trim().slice(0,12):''});
    if(now-t0<2500) requestAnimationFrame(f); } requestAnimationFrame(f); }"""
def scenario(pg, sel, champ, ouvrir, delai, nom):
    for _ in range(4):
        if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
        ouvrir(); pg.wait_for_timeout(900)
    # l'exemple vient de se tracer : on l'efface en tapant, puis on attend la fin de son retour
    n0 = pg.evaluate("()=>window.__P.traces.filter(x=>!x.inv && !x.ex).length")
    pg.keyboard.press('x'); pg.wait_for_timeout(500); pg.keyboard.press('Backspace')
    pg.wait_for_function("(n)=>{ const t=window.__P.traces.filter(x=>!x.inv && !x.ex); return t.length>n && t[t.length-1].fin; }", arg=n0, timeout=8000)   # l'exemple revenu : son tracé standard, FINI
    pg.wait_for_timeout(delai)
    std = pg.evaluate("()=>{ const t=window.__P.traces.filter(x=>!x.inv && !x.ex); return t[t.length-1].prevu; }")
    n1 = pg.evaluate("()=>window.__P.traces.length")
    pg.evaluate("()=>{ window.__sc=(document.getElementById('device').getBoundingClientRect().width/390)||1; }")   # l'échelle de l'appareil : la découpe est en pt
    pg.evaluate(REC, sel); pg.keyboard.press('m'); pg.wait_for_timeout(16); pg.keyboard.type('arche', delay=35); pg.wait_for_timeout(2600)
    I = pg.evaluate("()=>window.__I"); K = pg.evaluate("()=>window.__K")
    ex = [x for x in pg.evaluate("()=>window.__P.traces")[n1:] if x['ex'] and x['inv']][:1]   # le détracé de la touche « m »
    apres = [x for x in I if K and x['t'] >= K]
    a_ok = bool(apres) and apres[0]['txt'].startswith('m')
    mauvais = []
    for x in apres:
        if not x['w'] or not x['tb']: continue
        H, TB = x['hole'] or [], x['tb']
        for tb in TB:   # chaque ligne du texte tapé est dans une zone retirée
            if not any(tb[0] >= h[0] - 0.5 and tb[1] >= h[1] - 0.5 and tb[2] <= h[2] + 0.5 and tb[3] <= h[3] + 0.5 for h in H): mauvais.append((round(x['t'] - K), [[round(v) for v in h] for h in H][:2], [round(v) for v in tb])); break
    inks = [x['ink'] for x in apres if x['w'] and x['ink'] is not None]
    juge('[%s · %d ms] A · la lettre tapée tout de suite' % (nom, delai), a_ok, apres[0]['txt'] if apres else None)
    juge('[%s · %d ms] B · à chaque image, le texte tapé est dans la zone retirée de l\'exemple' % (nom, delai), not mauvais and any(x['w'] for x in apres), mauvais[:3])
    if ex and ex[0].get('prevu') and std:
        juge('[%s · %d ms] C · le détracé dure la moitié du tracé standard (%s ms pour %s)' % (nom, delai, ex[0]['prevu'], std), abs(ex[0]['prevu'] - std / 2) <= 0.15 * std / 2 and ex[0]['vit'] == 2)
    else: juge('[%s · %d ms] C · le détracé relevé' % (nom, delai), False, {'ex': ex, 'std': std})
    mx = max(inks) if inks else 0
    juge('[%s · %d ms] D · la fin s\'éteint en douceur (encre du canevas : au plus %s, à la dernière image %s)' % (nom, delai, mx, inks[-1] if inks else None), len(inks) >= 3 and mx > 0 and inks[-1] <= 0.06 * mx + 2)
    for _ in range(6): pg.keyboard.press('Backspace'); pg.wait_for_timeout(40)
    pg.wait_for_timeout(2500)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_premiere — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    for lieu in ('onboarding', 'page +'):
        if lieu == 'onboarding':
            ctx = B.contexte(b, onb=False, guide=False)
        else:
            ctx = B.contexte(b); B.toile_pleine(ctx, 10)
        ctx.add_init_script(CLAV); ctx.add_init_script(INIT)
        if '--sonde' in A_: ctx.add_init_script(SONDE)
        pg = B.ouvre(ctx, F, attente=7000)
        if lieu == 'onboarding':
            B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000); B.attend_parole(pg)
            sel, champ, ouvrir = '#onbPh .onbv-pm[data-onb=parole]', 'onbIn', (lambda: B.tap_sel(pg, '#onbPh [data-onb="parole"]'))
        else:
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
            sel, champ, ouvrir = '#csPhrase [data-ph=titre]', 'phIn', (lambda: B.tap_sel(pg, '#csPhrase [data-ph=titre]'))
        for d in (0, 50, 150, 400): scenario(pg, sel, champ, ouvrir, d, lieu)
        ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
