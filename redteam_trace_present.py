#!/usr/bin/env python3
"""redteam_trace_present — v170c (Tom, C-206) : « sur l'iPhone, les textes apparaissent d'un coup ; ton banc était vert : il ne voyait pas ce que voit l'iPhone ».

Pour chaque texte TRACÉ de l'onboarding (la page du prénom, celle de la parole, « trace pour planter ») et du guide (Studio, +, Partager, la phrase 2) :
  ① il n'est JAMAIS entièrement visible à la première image du tracé ;
  ② il est partiellement dévoilé pendant au moins trois images ;
  ③ sa durée d'apparition correspond au tracé à 40 car/s (EN DUR) : une lettre part toutes les 25 ms, une espace compte 0,4, la dernière dure 70 ms au
     moins — attendu = ((lettres − 1) + 0,4 × espaces) × 25 + 70 ms ; le texte entier paraît entre 0,7 × attendu et 2,5 × attendu + 1,5 s (un tracé
     qui attend sans fin, ou qui saute, rougit) ;
  ④ (le guide, phrase du Studio) À L'IMAGE : à 35 % de la durée attendue, la phrase à l'écran diffère de la phrase finie (le texte n'est pas déjà là).
Le moment où le texte est « entièrement visible » se lit sur ce que le navigateur rend : la découpe (`clip-path`) de l'élément retirée et le canevas
du tracé parti — pas sur ce que le module déclare.

QUATRE NAVIGATEURS, tous WebKit : `normal` ; `ios` — Worker et OffscreenCanvas désactivés (donc aucune police chargée dans un Worker) ; `muet` — un
Worker qui ne répond jamais ; `lent` — un Worker dont chaque réponse arrive 2 s plus tard (mesuré dans Safari iOS 26.1 sur v170b : 27,7 s d'attente
pour un mot de 0,17 s). Rouge sur v170b (`--fichier=zz-v170b.html`) : `muet` et `lent`.
`--modes=normal,ios` pour une passe courte.
"""
import io, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import banc_tom as B

F = 'app.html'; MODES = ['normal', 'ios', 'muet', 'lent']
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
    if a.startswith('--modes='): MODES = a.split('=', 1)[1].split(',')
CPS, ESPACE, DMIN = 40, 0.4, 70                      # la décision (v154, C-125) : 40 car/s, une espace = 0,4, une lettre dure 70 ms au moins
INIT = {
  'normal': '',
  'ios': "try{ Object.defineProperty(window,'Worker',{value:undefined,configurable:true,writable:true}); Object.defineProperty(window,'OffscreenCanvas',{value:undefined,configurable:true,writable:true}); }catch(e){}",
  'muet': "try{ window.Worker=function(){ this.postMessage=function(){}; this.terminate=function(){}; }; }catch(e){}",
  'lent': "try{ var W0=window.Worker; window.Worker=function(u){ var w=new W0(u), self_=this; self_.onmessage=null; self_.onerror=null;"
          " w.onmessage=function(e){ setTimeout(function(){ if(self_.onmessage) self_.onmessage(e); }, 2000); }; w.onerror=function(e){ if(self_.onerror) self_.onerror(e); };"
          " self_.postMessage=function(m,t){ w.postMessage(m,t); }; self_.terminate=function(){ w.terminate(); }; }; }catch(e){}",
}
SONDE = r"""(()=>{ window.__S=[]; let T=null;
  function arme(v){ if(!v||v.__s) return; v.__s=1; const tr=v.trace; v.trace=function(c, ct, o){ if(o && o.preparer) return tr.apply(this,arguments);   /* une préparation d'avance ne montre rien : ce n'est pas un texte affiché */
    const c0=(c.style.getPropertyValue('clip-path')||'none').replace(/\s+/g,''), t0=performance.now(), ctl=tr.apply(this,arguments);   /* la découpe d'avant le tracé (l'onboarding en pose une) : le module la rend à la fin */
    const tx=String(c.textContent||'').replace(/\s+/g,' ').trim(), r={tx:tx, t0:t0, im:0, part:0, vis:null, prem:null, deb:null, ctl:ctl, i0:v.mesures.image.length, img:[]}; __S.push(r); let tp=0;
    function vu(){ const cp=c.style.getPropertyValue('clip-path')||c.style.getPropertyValue('-webkit-clip-path')||'none';
      const cvL=!!(ctl.canevas && ctl.canevas.parentNode); const k=cp.replace(/\s+/g,''); return (k==='none'||k===''||(ctl.fini&&k===c0)) && !cvL && c.style.visibility!=='hidden'; }   /* le canevas de CE tracé (les textes d'une page sont frères : le canevas du suivant n'est pas le sien) */
    function vide(){ const cp=(c.style.getPropertyValue('clip-path')||'').replace(/\s+/g,''); return cp.indexOf('0px0px,0px0px')>=0 || cp.indexOf('M-9999')>=0; }
    (function f(){ const n=performance.now(), vv=vu(); if(r.prem===null) r.prem=vv; r.im++; if(r.deb===null && !vv && !vide()) r.deb=n-t0; if(r.deb!==null && r.vis===null && tp) r.img.push(n-tp); tp=n;
      if(!vv) r.part++; else if(r.vis===null){ r.vis=Math.round(n-t0); r.i1=v.mesures.image.length; }
      if(r.vis===null && performance.now()-t0<20000) requestAnimationFrame(f); })();
    return ctl; }; }
  Object.defineProperty(window,'TraceLettres',{configurable:true,get(){return T;},set(v){T=v; arme(v);}}); })();"""
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
def attendu(tx):
    n = len([c for c in tx if not c.isspace()]); s = len([c for c in tx if c.isspace()])
    return max(0, (n - 1) + ESPACE * s) * (1000.0 / CPS) + DMIN

def lis(pg): return pg.evaluate("()=>__S.map(r=>({tx:r.tx, vis:r.vis, prem:r.prem, part:r.part, im:r.im, age:Math.round(performance.now()-r.t0), deb:r.deb, duree:r.ctl&&r.ctl.duree, mod:r.ctl&&r.ctl.mesure, travail:(r.i1!=null?TraceLettres.mesures.image.slice(r.i0,r.i1):[]).reduce((a,x)=>Math.max(a,x),0), pire:r.img.reduce((a,x)=>Math.max(a,x),0)}))")
def attends_fin(pg, n0, lim=22000):
    for _ in range(lim // 200):
        S = lis(pg)
        if len(S) > n0 and all(r['vis'] is not None or r['age'] > 20000 for r in S[n0:]): return S
        pg.wait_for_timeout(200)
    return lis(pg)

def verifie(T, S, deja):
    for r in S:
        if r['tx'] in deja or not r['tx']: continue
        deja.add(r['tx']); A = attendu(r['tx']); v = r['vis']
        juge('[%s] « %s » : pas entier à la première image, dévoilé sur ≥ 3 images' % (T, r['tx'][:34]), r['prem'] is False and r['part'] >= 3, 'première image %s · %d images partielles' % ('ENTIER' if r['prem'] else 'découpé', r['part']))
        ok = v is not None and 0.7 * A <= v <= 2.5 * A + 1500; ch = B.charge()
        if not ok and v is not None and v > 2.5 * A + 1500 and ch > 8 and v < 3000 + 4 * A:
            # C-137 : un dépassement modéré sous une forte charge n'est pas jugé (il se rejoue au calme) — un texte qui ne paraît JAMAIS, lui, rougit toujours
            print('  ⚠ [%s] « %s » : %s ms pour %d ms attendus — NON JUGÉ (charge %.0f)' % (T, r['tx'][:34], v, A, ch), flush=True); continue
        juge('[%s] « %s » : paraît en entier entre 0,7 et 2,5 × le tracé à 40 car/s (+1,5 s)' % (T, r['tx'][:34]), ok, '%s ms pour %d ms attendus' % (v, A))
        # ⚑ v170d (Tom, C-125) : le DÉVOILEMENT (du premier trait au texte entier) dure la durée prévue à ± 10 % ; aucune image du tracé au-delà de 20 ms, aucun calcul
        #   de tracé pendant le dévoilement (le travail du module par image ≤ 8 ms). Au calme seulement (C-137) ; sinon NON JUGÉ. Le mode `normal` seul.
        if T.split(' ')[0] == 'normal' and v is not None and r['duree'] and r.get('mod') and r['mod'].get('attente') is not None:
            # le départ de la plume : l'instant que le module déclare (un POINTEUR) ; la fin : le texte entier À L'ÉCRAN (la découpe retirée, le canevas parti)
            reel = v - r['mod']['attente']; D = r['duree']
            juge('[%s] « %s » : la durée prévue suit la décision (40 car/s : de %d à %d ms)' % (T, r['tx'][:34], A, A + 25), A - 1 <= D <= A + 25, '%d ms' % D)
            if ch > 4: print('  ⚠ [%s] « %s » : dévoilement %d ms pour %d prévus, pire image %d ms, travail du tracé %.1f ms — NON JUGÉ (charge %.0f)' % (T, r['tx'][:34], reel, D, r['pire'], r['travail'], ch), flush=True)
            else:
                juge('[%s] « %s » : le dévoilement dure la durée prévue ± 10 %%' % (T, r['tx'][:34]), abs(reel - D) <= 0.10 * D + 17, '%d ms pour %d ms' % (reel, D))
                juge('[%s] « %s » : aucune image du tracé au-delà de 20 ms, travail du tracé ≤ 8 ms par image' % (T, r['tx'][:34]), r['pire'] <= 20 and r['travail'] <= 8, 'pire image %d ms · travail %.1f ms' % (r['pire'], r['travail']))

with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MODES:
        T = m; deja = set()
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
        ctx.add_init_script("try{ if(!sessionStorage.getItem('__i')){ sessionStorage.setItem('__i','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}")
        if INIT[m]: ctx.add_init_script(INIT[m])
        ctx.add_init_script(SONDE)
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        print('\n── %s · charge %.1f' % (m, B.charge()), flush=True)
        pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(6500)
        # 1 · l'onboarding : la page du prénom, puis celle de la parole
        S = attends_fin(pg, 0); verifie(T + ' · prénom', S, deja); n0 = len(S)
        c = B.tap_sel(pg, '#onbPh') if hasattr(B, 'tap_sel') else None
        pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(200); pg.keyboard.press('Enter'); pg.wait_for_timeout(2500)
        S = attends_fin(pg, n0); verifie(T + ' · parole', S, deja); n0 = len(S)
        if not pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.id==='onbIn'); }"):
            B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(400)
        pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(2500)
        S = attends_fin(pg, n0); verifie(T + ' · trait', S, deja); n0 = len(S)
        juge('[%s] l\'onboarding a tracé au moins quatre textes' % T, n0 >= 4, '%d textes : %s' % (n0, [r['tx'][:18] for r in S]))
        # 2 · le guide, ses quatre phrases
        pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
        for q in ('studio', 'plus', 'partage', 'reste'):
            pg.evaluate("q=>{ try{ _guide.finir&&_guide.finir(); }catch(e){} _guide.montre(q); }", q)
            if q == 'studio':
                for _ in range(60):
                    if len(lis(pg)) > n0: break
                    pg.wait_for_timeout(50)
                S = lis(pg)
                if len(S) > n0:
                    r = S[n0]; A = attendu(r['tx']); pg.wait_for_timeout(max(0, int(0.35 * A) - r['age']))
                    box = pg.evaluate("()=>{const e=document.getElementById('guidePhrase'); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.left-4,y:r.top-4,width:r.width+8,height:r.height+8};}")
                    mi = Image.open(io.BytesIO(pg.screenshot(clip=box))).convert('L') if box else None
            S = attends_fin(pg, n0)
            if q == 'studio' and len(S) > n0 and box and mi is not None:
                pg.wait_for_timeout(300); fi = Image.open(io.BytesIO(pg.screenshot(clip=box))).convert('L')
                df = ImageChops.difference(mi, fi).point(lambda v: 255 if v > 40 else 0); part = sum(df.histogram()[255:]) / float(fi.size[0] * fi.size[1])
                juge('[%s] À L\'IMAGE : à 35 %% du tracé, la phrase du Studio n\'est pas encore entière' % T, part > 0.02, '%.1f %% des pixels diffèrent de la phrase finie' % (part * 100))
            verifie(T + ' · guide ' + q, S[n0:], deja); n0 = len(S); pg.wait_for_timeout(300)
        juge('[%s] le guide a tracé ses quatre phrases' % T, len([x for x in deja]) >= 8, '%d textes tracés en tout' % len(deja))
        etat = pg.evaluate("()=>window.TraceLettres?(TraceLettres.ouvrierEtat||'—'):'module absent'")
        print('     ouvrier : %s' % etat, flush=True)
        juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
