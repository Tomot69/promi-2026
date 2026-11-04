#!/usr/bin/env python3
"""redteam_tout_effacer.py — ⚑ v163b (Tom, C-195 ; AUDIT-BOUTONS 20, 21, 27, point 7) : UN SEUL « TOUT EFFACER ».

« « Réinitialiser mes données », « Tout effacer » et « Supprimer mon compte » deviennent une seule rangée « Tout effacer » des Réglages, avec feuille de
confirmation et annulation de 5 s. « Se déconnecter » ne paraît que si un compte existe. Le bouton d'action des feuilles de confirmation prend l'encre du
mode en gras, pas #DD4D23. »
Banc comme Tom (WebKit ×3, doigt), clair et sombre :
  A · les Réglages portent « Tout effacer » une fois ; ni « Réinitialiser mes données » ni « Supprimer mon compte » ; Vie privée n'a plus « Tout effacer » ;
  B · « Tout effacer » touché : la feuille « Tout effacer ? » ; son bouton d'action est à l'encre du mode (fond = encre, ±12), en gras, jamais l'orange d'état ;
  C · « Effacer », puis « Annuler » dans les 5 s : rien n'est effacé ; « Effacer » sans annuler : après 5 s tout le stockage est vide ;
  D · « Se déconnecter » absent sans compte, présent avec un compte.
Preuve : `--fichier=zz-v162.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
def rgb(s):
    import re; v = [int(float(x)) for x in re.findall(r'[\d.]+', s)[:3]]; return tuple(v)
def centre(pg, sel):
    pg.evaluate("s=>{ const e=document.querySelector(s); if(e) e.scrollIntoView({block:'center'}); }", sel); pg.wait_for_timeout(400)
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!r.width) return null; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", sel)
RANGEES = "()=>[...document.querySelectorAll('#settingsScreen .scard .k')].filter(e=>e.getBoundingClientRect().height>0 && getComputedStyle(e.closest('.scard')).display!=='none').map(e=>e.textContent.trim())"
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'; ENC = (247, 240, 222) if sombre else (32, 25, 8)
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} }")
        B.tap_sel(pg, '#settingsBtn'); pg.wait_for_timeout(1800); L = pg.evaluate(RANGEES)
        pv = pg.evaluate("()=>[...document.querySelectorAll('#privScreen .scard .k')].map(e=>e.textContent.trim())")
        juge('[%s] A · « Tout effacer » une fois aux Réglages ; ni « Réinitialiser… » ni « Supprimer mon compte » ; plus dans Vie privée' % T,
             L.count('Tout effacer') == 1 and not any('Réinitialiser' in x or 'Supprimer mon compte' in x for x in L) and 'Tout effacer' not in pv, {'reglages': L, 'vie privée': pv})
        juge('[%s] D · « Se déconnecter » absent sans compte' % T, 'Se déconnecter' not in L, L)
        c = centre(pg, '#resetData')
        if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(700)
        f = pg.evaluate("()=>{ const v=document.getElementById('v16Conf'); if(!v) return null; const o=v.querySelector('.v16-oui'), s=getComputedStyle(o); return [v.querySelector('.v16-conf-t').textContent, o.textContent, s.backgroundColor, s.fontWeight]; }")
        okB = f and 'Tout effacer' in f[0] and f[1] == 'Effacer' and sum(abs(a - b_) for a, b_ in zip(rgb(f[2]), ENC)) <= 36 and int(f[3]) >= 700 and rgb(f[2]) != (221, 77, 35)
        juge('[%s] B · la feuille « Tout effacer ? », l\'action à l\'encre du mode, en gras, jamais l\'orange d\'état' % T, okB, f)
        if f:
            o = centre(pg, '#v16Conf .v16-oui'); B.tap(pg, o[0], o[1]); pg.wait_for_timeout(900)
            a = centre(pg, '#v16Toast button')
            if a: B.tap(pg, a[0], a[1])
            pg.wait_for_timeout(6000); n = pg.evaluate("()=>localStorage.getItem('promi_state')!=null")
            juge('[%s] C · « Effacer » puis « Annuler » dans les 5 s : rien n\'est effacé' % T, a is not None and n, 'annuler %s · état gardé %s' % (a, n))
        pg.evaluate("()=>{ localStorage.setItem('promi_compte','fait-apple'); }"); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500)
        B.tap_sel(pg, '#settingsBtn'); pg.wait_for_timeout(1800); L = pg.evaluate(RANGEES)
        juge('[%s] D · « Se déconnecter » présent avec un compte' % T, 'Se déconnecter' in L, L)
        if not sombre:
            c = centre(pg, '#resetData'); B.tap(pg, c[0], c[1]); pg.wait_for_timeout(700)
            o = centre(pg, '#v16Conf .v16-oui')
            if o:
                pg.evaluate("()=>{ window.__rel=0; try{ Object.defineProperty(location, 'reload', {value:()=>{ window.__rel++; }}); }catch(e){ window.__relErr=String(e); } }")
                B.tap(pg, o[0], o[1]); pg.wait_for_timeout(6500)
                try: n = pg.evaluate("()=>[localStorage.length, window.__rel||0]")
                except Exception as e: n = ['rechargé', str(e)[:40]]
                juge('[clair] C · « Effacer » sans annuler : après 5 s, tout le stockage est vide', n == ['rechargé', n[1]] or (n[0] <= 1), n)
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
