#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_aura_latence.py — L'AURA : LA PELOTE EST LÀ DÈS L'OUVERTURE (v146, Tom, 14 oct. 2026 — C-135).

« Quand on ouvre l'Aura, la place reste vide une à deux secondes avant que la Pelote paraisse. C'est un bug : il faut qu'elle soit là dès
l'ouverture. Cible : la première image de la Pelote se dessine dans l'image même où l'Aura s'ouvre. À la première ouverture comme aux
suivantes. Juge : délai entre le toucher et la première image de Pelote ; 1re, 2e et 5e ouverture. »

Par banc_tom (WebKit, 390 × 844 @3x), sur une Toile de 25 paroles relue de la sauvegarde, dont 6 tenues (elles font les îles). Le toucher est
un vrai toucher sur AURA ; l'Aura se referme par son ✕ FERMER. Le délai est lu DANS la page, à l'image près, par une boucle d'images
indépendante de l'app : l'heure du `touchstart`, l'image où l'écran paraît, l'image où le canevas de la Pelote porte une image NEUVE
(le compteur de peintures a avancé ET des pixels opaques sont lus au centre du canevas de la carte graphique).

  1 · avant la première ouverture, l'app au repos a préparé la Pelote (le juge attend le repos, 12 s au plus)
  2 · 1re, 2e, 3e, 4e, 5e ouverture : la Pelote est peinte dans le geste (avant la première image qui montre l'écran) ; EN DUR : au plus
      120 ms entre le clic et la première image qui porte la Pelote, et c'est l'image même où l'écran paraît
  3 · à chaque ouverture le ton est neuf (la décision « un ton neuf à chaque ouverture » tient)
  4 · la préparation au repos ne tourne pas sous le doigt : un toucher pendant qu'elle court l'arrête avant l'étape suivante
  5 · sans préparation (ouverture immédiate après un changement), la Pelote paraît quand même, sans erreur
Preuve (§7) : `python3 redteam_aura_latence.py sauvegardes/app-avant-v146.html` — il rougit (1,9 à 2,3 s, puis 0,8 à 0,9 s).
Usage : python3 redteam_aura_latence.py [fichier.html] [--port=8752]
"""
import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); PORT = arg('port', '8752')
MAX_MS = 120          # du CLIC (l'instant où l'app reçoit le geste ; le navigateur met 20 à 65 ms à faire un clic d'un toucher) à la première image
                      #   qui porte la Pelote — EN DUR
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:330]), flush=True)
VU = """()=>{ window.__V={t0:0,vu:null,img:0,ecran:null,sol:null};
  function peinte(){ try{ const c=document.getElementById('auBouleGL'); if(c && c.width){ const g=document.createElement('canvas'); g.width=g.height=8; const x=g.getContext('2d'); x.drawImage(c, c.width/2-40, c.height/2-40, 80, 80, 0, 0, 8, 8); const d=x.getImageData(0,0,8,8).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>200) n++; return n>=48; }
      const b=document.getElementById('auBoule'); if(!b||!b.width) return false; const d=b.getContext('2d').getImageData(b.width/2-4,b.height/2-4,8,8).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>200) n++; return n>=48; }catch(e){ return false; } }
  document.getElementById('souffleBtn').addEventListener('click', e=>{ if(window.__V.clic==null) window.__V.clic=+(performance.now()-window.__V.t0).toFixed(1); }, true);
  document.getElementById('souffleBtn').addEventListener('touchstart', e=>{ const V=window.__V; V.t0=performance.now(); V.vu=null; V.img=0; V.ecran=null; V.clic=null; let p0=0; try{ p0=_aura.etat().peints; }catch(e){}
    (function f(){ const t=performance.now()-V.t0; V.img++; let p=0; try{ p=_aura.etat().peints; }catch(e){} const s=document.getElementById('auraScreen');
      if(V.ecran==null && s.classList.contains('show')) V.ecran=[+t.toFixed(1), V.img];
      if(V.vu==null && p>p0 && s.classList.contains('show') && peinte()){ V.vu=[+t.toFixed(1), V.img]; try{ V.sol=_aura.sol().idx+'|'+_aura.corps().idx; }catch(e){} }
      if(t<6000 && V.vu==null) requestAnimationFrame(f); })(); }, true); }"""
def ferme(pg):
    r = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#auraScreen [data-close], #auraScreen .closeb')].find(x=>x.getBoundingClientRect().width>4); if(!e) return null; const q=e.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }")
    if r: pg.touchscreen.tap(r[0], r[1])
    pg.wait_for_timeout(700); return not pg.evaluate("()=>document.getElementById('auraScreen').classList.contains('show')")
def repos(pg, max_s=14):
    """attend que l'app, laissée tranquille, ait préparé la Pelote ; rend (prête, secondes attendues, état)"""
    t = 0.0
    while t < max_s:
        e = pg.evaluate("()=>{ try{ return (window._aura&&_aura.pre)?_aura.pre():null; }catch(e){ return null; } }")
        if e is None: return None, t, None
        if e['pret']: return True, t, e
        pg.wait_for_timeout(400); t += 0.4
    return False, t, e
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b)
    # l'état de Tom : une Toile de 25 paroles DONT 6 TENUES, relue de la sauvegarde à l'ouverture (les tenues font les îles de la Pelote)
    import io as _io
    st = json.load(_io.open('banc-etats/etat-25.json', encoding='utf-8')); st.pop('promi_theme', None); e = json.loads(st['promi_state'])
    for q in e['promises'][:6]: q['status'] = 'tenu'; q['keptAt'] = 1760000000000
    st['promi_state'] = json.dumps(e, ensure_ascii=False)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
    pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500)
    tenues = pg.evaluate("()=>promises.filter(p=>p.status==='tenu').length"); pg.evaluate(VU)
    juge('la Toile relue porte des paroles tenues (au moins 6 : elles font les îles)', tenues >= 6, tenues)
    pret, att, e = repos(pg)
    juge('1 · au repos après le démarrage, l\'app a préparé la Pelote', pret is True, 'après %.1f s · étapes (ms) %s' % (att, (e or {}).get('ms')) if pret is not None else 'pas de préparation au repos dans cette version')
    if e and e.get('ms'):
        pire = max([v for k, v in e['ms'].items() if k != 'total'] or [0])
        print('     la plus longue étape de la préparation : %.0f ms · total %s ms' % (pire, e['ms'].get('total')))
    sols = []
    for k in range(1, 6):
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(3400)
        V = pg.evaluate("()=>window.__V"); pre = pg.evaluate("()=>{ try{ return _aura.pre(); }catch(e){ return null; } }") or {}
        vu, ec = V.get('vu'), V.get('ecran')
        cl = V.get('clic') or 0
        ok = bool(vu and ec) and (vu[0] - cl) <= MAX_MS and vu[1] <= ec[1]
        if k in (1, 2, 5) or not ok:
            juge('2 · ouverture n° %d : la Pelote est dans l\'image même où l\'Aura paraît, ≤ %d ms après le clic' % (k, MAX_MS), ok,
                 'toucher 0 · clic %s ms · écran à %s ms (image %s) · Pelote à %s ms (image %s) · peinte dans le geste : %s · préparée d\'avance : %s' % (cl, ec and ec[0], ec and ec[1], vu and vu[0], vu and vu[1], pre.get('dansGeste'), pre.get('chaude')))
        sols.append(V.get('sol'))
        if not ferme(pg): juge('ouverture n° %d : l\'Aura se referme par son ✕' % k, False); break
        repos(pg)
    juge('3 · un ton neuf à chaque ouverture (sol ou corps change d\'une ouverture à la suivante)', len(sols) == 5 and all(sols[i] != sols[i + 1] for i in range(4)), sols)
    # 4 · la préparation s'efface devant le doigt
    if pret is not None:
        pg.evaluate("()=>{ try{ Toile.setPalette && 0; window.onPaletteChange && window.onPaletteChange(); }catch(e){} }")      # invalide : il faut re-préparer
        pg.wait_for_timeout(300)
        r = pg.evaluate("""async ()=>{ const att=ms=>new Promise(r=>setTimeout(r,ms)); let t=0; while(t<9000 && !_aura.pre().enCours){ await att(60); t+=60; }
            const a=_aura.pre(); if(!a.enCours) return {vu:false, a:a};
            document.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true})); const m0=JSON.stringify(_aura.pre().ms); await att(900); const b=_aura.pre();
            return {vu:true, enCoursApres:b.enCours, pretApres:b.pret, etapesAvant:m0, etapesApres:JSON.stringify(b.ms)}; }""")
        juge('4 · un toucher pendant la préparation l\'arrête (elle reprendra au repos suivant)', r.get('vu') and not r.get('enCoursApres') and not r.get('pretApres'), r)
        pret2, att2, _ = repos(pg, 16)
        juge('4 · puis, au repos, elle reprend et finit', pret2 is True, 'après %.1f s' % att2)
        # 5 · une ouverture AVANT que le repos ait préparé : la Pelote paraît quand même
        pg.evaluate("()=>{ try{ window.onPaletteChange && window.onPaletteChange(); }catch(e){} }"); pg.wait_for_timeout(120)
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(4200); V = pg.evaluate("()=>window.__V")
        juge('5 · ouverte avant d\'avoir pu se préparer, la Pelote paraît quand même', bool(V.get('vu')), 'Pelote à %s ms' % (V.get('vu') and V['vu'][0]))
    # 6 · on vient de tenir une parole (les îles changent), on ferme, on ouvre l'Aura 1,6 s plus tard : elle a eu le temps de se re-préparer
    if pret is not None:
        ferme(pg); repos(pg)
        pg.evaluate("()=>{ const p=promises.find(p=>p.status!=='tenu'); p.status='tenu'; p.keptAt=Date.now(); try{ syncAll(); }catch(e){} }"); pg.wait_for_timeout(1600)
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(3400); V = pg.evaluate("()=>window.__V"); pre = pg.evaluate("()=>_aura.pre()") or {}
        vu, ec = V.get('vu'), V.get('ecran')
        juge('6 · une parole vient d\'être tenue, l\'Aura ouverte 1,6 s après : la Pelote est dans l\'image même où l\'écran paraît', bool(vu and ec) and vu[1] <= ec[1] and (vu[0] - (V.get('clic') or 0)) <= MAX_MS,
             'écran à %s ms · Pelote à %s ms · peinte dans le geste : %s · préparée : %s' % (ec and ec[0], vu and vu[0], pre.get('dansGeste'), pre.get('chaude')))
    juge('aucune erreur de page, aucune erreur de l\'Aura', not pg.erreurs and not pg.evaluate("()=>window._auraErreur||null"), (pg.erreurs[:2], pg.evaluate("()=>window._auraErreur||null")))
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1200])
sys.exit(0 if ok == len(res) else 1)
