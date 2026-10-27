#!/usr/bin/env python3
"""redteam_veille_depart.py — ⚑ v167 (Tom, C-181 §3) : LA VEILLE PART À 60 s, PARTOUT.

« Au bout de 2 minutes, la veille n'arrive pas. Le délai repasse à 60 s. Reproduis sur mon état exporté, dans Safari WebKit, sur le vrai chemin. Juge : départ à
60 s ± 1 s sur 5 écrans différents, sur mon état, en WebKit. »

LA CAUSE (écrite dans `lot-V167-DOIGTS`) : le mur de Ma Parole ! arrête le `pointerup` d'un toucher sur un mur (window, capture), avant la veille : son compte de
doigts restait à 1 pour toujours. Les touchers de banc_tom ne fabriquent AUCUN évènement de pointeur — ce juge touche donc par de VRAIS évènements de pointeur
(`PointerEvent` pointerdown / pointerup, type « touch », puis le clic), comme le doigt de l'iPhone.
Sur l'état de Tom (`etats/tom-*.json`, sa fenêtre), la veille rallumée (sans `?veille`), cinq écrans — l'accueil, une fiche (son Peaufiner ouvert, un toucher
sur une rangée réservée : un mur), l'Index, le Fil, l'Aura — : après le dernier toucher, la veille part entre 59 et 61 s, pas avant.
Preuve : `--fichier=zz-v166.html` rougit (120 s ; et la fiche au mur ne part jamais).
"""
import sys, json, glob, io, time; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
DOIGT = """(sel)=>new Promise(ok=>{ const D=document.getElementById('device').getBoundingClientRect(); let x, y, e;
  if(sel){ const q=[...document.querySelectorAll(sel)].map(n=>n.getBoundingClientRect()).filter(r=>r.width>10 && r.top<D.bottom-20)[0]; if(!q) return ok(null); x=q.left+q.width/2; y=Math.min(q.top+30, D.bottom-30); }
  else { x=D.left+D.width/2; y=D.top+D.height*0.08; }
  e=document.elementFromPoint(x,y); const o={pointerId:11, pointerType:'touch', isPrimary:true, clientX:x, clientY:y, bubbles:true, cancelable:true, composed:true};
  e.dispatchEvent(new PointerEvent('pointerdown', Object.assign({buttons:1}, o)));
  setTimeout(()=>{ const t=performance.now(); e.dispatchEvent(new PointerEvent('pointerup', Object.assign({buttons:0}, o))); e.dispatchEvent(new MouseEvent('click', {clientX:x, clientY:y, bubbles:true, cancelable:true})); ok({t:t, cible:(e.id||e.className||e.tagName)+''}); }, 80); })"""
ECRANS = (
    ('accueil', "()=>{ try{ closeAll(); }catch(e){} }", None),
    ('fiche · un mur du Peaufiner', "()=>{ const p=promises.find(q=>!q.draft); openDetail(p.id); setTimeout(()=>{ try{ window._s2Ouvre(true); }catch(e){} }, 1500); }", '#detailPoster .s2-cercle:not(.v16-seul)'),
    ('Index', "()=>{ try{ closeAll(); }catch(e){} document.getElementById('indexBtn').click(); }", None),
    ('Fil', "()=>{ try{ closeAll(); }catch(e){} document.getElementById('filBtn').click(); }", None),
    ('Aura', "()=>{ try{ closeAll(); }catch(e){} document.getElementById('souffleBtn').click(); }", None),
)
with sync_playwright() as p:
    b = p.webkit.launch()
    L = [f for f in sorted(glob.glob('etats/tom-*.json')) if json.loads(json.load(io.open(f, encoding='utf-8')).get('ls', {}).get('promi_state', '{}') or '{}').get('promises')]
    if not L: juge("l'état exporté de Tom existe", False, 'aucun')
    for nom, ouvre, mur in (ECRANS if L else ()):
        ctx, d = B.contexte_tom(b, L[-1]); ctx.add_init_script("try{ localStorage.removeItem('promi_veille_off'); }catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(4500)
        pg.evaluate(ouvre); pg.wait_for_timeout(3500)
        r = pg.evaluate(DOIGT, mur)
        if not r: juge('[%s] le dernier toucher (un mur)' % nom, False, 'introuvable'); ctx.close(); continue
        dep = None; tf = time.time() + 75
        while time.time() < tf:
            v = pg.evaluate("()=>{ const v=_veille(); return [v.active, performance.now()-v.depuis, v.doigts]; }")
            if v[0]: dep = (v[1] - r['t']) / 1000.0; break
            pg.wait_for_timeout(500)
        juge('[%s] la veille part 60 s (± 1) après le dernier toucher (%s)' % (nom, r['cible'][:24]), dep is not None and 59 <= dep <= 61,
             ('part à %.2f s' % dep) if dep is not None else ('ne part pas en 75 s · doigts %s' % v[2]))
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
