#!/usr/bin/env python3
"""redteam_depart_orange.py — ⚑ v155 (Tom, C-169 ; chef de chantier §4.5, Q561) : LE DÉPART DU TRAIT, ORANGE — ET CLIGNOTANT DANS L'ONBOARDING.

« Partout (onboarding, pages +, fiches), en clair et en sombre : tout le départ de la flèche, la pointe ET le trait de départ, est orange #FB4C0D. Fiches
à moitié tracées : le départ de la seconde moitié, au milieu du trait (pointe ET trait de départ), orange aussi. Pages + : « TRACE POUR … » en orange sur les
trois natures, plus la pointe et le trait de départ. Onboarding : « trace pour planter » et la flèche paraissent 1 s APRÈS la validation du prénom ; la
pointe et le trait de départ clignotent au même rythme que le I de PROMI (même code), jusqu'au premier toucher sur le trait, puis orange fixe. Le
clignotement n'existe que dans l'onboarding. Juge : couleur du départ (pointe et trait) sur l'onboarding, les pages + et les fiches à moitié tracées,
pour les trois natures et les deux thèmes ; clignotement dans l'onboarding seulement ; apparition à 1 s ± 50 ms après la validation. »
Banc comme Tom (WebKit 390 × 844 ×3). La couleur se LIT SUR L'IMAGE : là où le peintre déclare la pointe (`data-depart`), deux fenêtres — la pointe
(−8 → +5 pt) et le trait de départ (−40 → −14 pt), ± 14 pt autour de l'onde ; au moins 60 pixels (@3x) à moins de 40 de #FB4C0D dans CHACUNE.
  F · fiches à moitié tracées : Promi à soi, Promi à Rachel, Promi à tenir (échéance passée), Chiche lancé ; clair et sombre
  P · pages + au repos : Promi, Chiche, Cercle ; clair et sombre ; « TRACE POUR … » en #FB4C0D
  O · onboarding (stockage vierge, le vrai parcours) : apparition 1 000 ± 50 ms après Retour ; la couche du départ porte `promiBlink` (1,15 s, la
      même animation que le I), calée sur lui ; lu à la phase pleine : orange ; touché : plus d'animation, orange fixe ; « Réduire les animations » :
      aucune animation (ni le départ ni le I)
  N · le clignotement n'existe que dans l'onboarding : sur une fiche et une page +, aucune animation `promiBlink` hors du I de PROMI
Preuve : `--fichier=zz-av154.html` rougit (F, P, O).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ORG = (251, 76, 13); res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-108s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
def lit(pg, sel):
    """les pixels orange autour de la pointe déclarée par le canevas `sel` : (pointe, trait) en pixels @3x"""
    z = pg.evaluate("""(s)=>{ const c=document.querySelector(s); if(!c) return null; const dep=c.getAttribute('data-depart'); if(!dep) return null; const r=c.getBoundingClientRect(),
        D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, sx=r.width/k/(c.width/(window.devicePixelRatio||1))*0 || (r.width/k)/390;
      const p=dep.split(',').map(Number); return {x:(r.left-D.left)/k + p[0]*(r.width/k)/390, y:(r.top-D.top)/k + p[1]*(r.width/k)/390}; }""", sel)
    if not z: return None
    im = B.image(pg); px = im.load(); W, H = im.size; s = W / 390.0
    def compte(x0, x1, y0, y1):
        n = 0
        for X in range(max(0, int(x0 * s)), min(W, int(x1 * s))):
            for Y in range(max(0, int(y0 * s)), min(H, int(y1 * s))):
                c = px[X, Y][:3]
                if sum((c[i] - ORG[i]) ** 2 for i in range(3)) < 1600: n += 1
        return n
    return compte(z['x'] - 8, z['x'] + 5, z['y'] - 12, z['y'] + 12), compte(z['x'] - 40, z['x'] - 14, z['y'] - 16, z['y'] + 16), z
def blink_hors_i(pg):
    return pg.evaluate("()=>document.getAnimations().filter(a=>a.animationName==='promiBlink' && a.playState==='running').map(a=>{ const t=a.effect&&a.effect.target; return t?(t.id||t.className||t.tagName):'?'; }).filter(n=>!/(^|\\s)(hi|ii|blink|ti-x|uvi)(\\s|$)|^I$/.test(String(n)))")
with sync_playwright() as p:
    b = p.webkit.launch()
    # ── F · fiches
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'
        ctx = B.contexte(b, sombre=sombre); ctx.add_init_script('window.__INVITE_BANC=1;'); pg = B.ouvre(ctx, F)   # ⚑ v172 (C-209) : l'invite de la page + (départ, flèche, « trace pour … ») posée d'emblée comme avant — son apparition est jugée par redteam_invite_page_plus
        B.plante(pg, 'rendre le livre'); B.plante(pg, 'appeler mamie', qui='Rachel'); B.plante(pg, 'courir dimanche', nature=1, qui='Rachel'); B.plante(pg, 'ranger la cave')
        pg.evaluate("()=>{ const p=promises.find(x=>x.title==='ranger la cave'); p.status='rate'; try{ saveState(); syncAll(); }catch(e){} }")
        for titre, nom in (('rendre le livre', 'Promi à soi'), ('appeler mamie', 'Promi à Rachel'), ('ranger la cave', 'Promi à tenir'), ('courir dimanche', 'Chiche lancé')):
            pg.evaluate("t=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); const p=promises.find(x=>x.title===t); openDetail(p.id); }", titre); pg.wait_for_timeout(2600)
            r = lit(pg, '#dpTrameCv')
            juge('[%s] F · fiche %s : la pointe ET le trait de départ (au milieu) sont orange' % (T, nom), r and r[0] >= 60 and r[1] >= 60, r and 'pointe %d px · trait %d px · départ à %.0f, %.0f pt' % (r[0], r[1], r[2]['x'], r[2]['y']))
        n = blink_hors_i(pg); juge('[%s] N · sur une fiche, rien ne clignote hors du I' % T, not n, n)
        # ── P · pages +
        for nat, i in (('Promi', 0), ('Chiche', 1), ('Cercle', 2)):
            pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(800)
            pg.evaluate("n=>{ const x=[...document.querySelectorAll('#createSheet .tile')][n]; x&&x.click(); }", i); pg.wait_for_timeout(2600)
            r = lit(pg, '#csTrameCv')
            lab = pg.evaluate("()=>{ const e=document.querySelector('#createSheet .pp-trace'); if(!e) return null; const c=getComputedStyle(e); return [e.textContent, c.color, c.webkitTextFillColor]; }")
            juge('[%s] P · page + %s au repos : la pointe ET le trait de départ sont orange' % (T, nat), r and r[0] >= 60 and r[1] >= 60, r and 'pointe %d px · trait %d px' % (r[0], r[1]))
            juge('[%s] P · page + %s : « %s » en #FB4C0D' % (T, nat, lab and lab[0]), lab and lab[1] == 'rgb(251, 76, 13)' and lab[2] == 'rgb(251, 76, 13)', lab)
        n = blink_hors_i(pg); juge('[%s] N · sur une page +, rien ne clignote hors du I' % T, not n, n)
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    # ── O · onboarding
    for sombre, reduit in ((False, False), (True, False), (False, True)):
        T = ('sombre' if sombre else 'clair') + (', réduire les animations' if reduit else '')
        ctx = B.contexte(b, sombre=sombre, onb=False, guide=False); pg = B.ouvre(ctx, F, attente=7000)
        if reduit: pg.emulate_media(reduced_motion='reduce')
        B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(400)
        # ⚑ v173 (C-211) : le trait ne paraît plus 1,5 s après le prénom (v156) mais la promesse complétée, le clavier refermé — jugé par `redteam_onb_ordre`
        pg.keyboard.press('Enter'); B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
        st = pg.evaluate("""()=>{ const d=document.getElementById('onbDepart'), i=document.querySelector('#onbV .onbv-mm i'); const A=d?d.getAnimations():[], AI=i?i.getAnimations():[];
          const a=A.find(x=>x.animationName==='promiBlink'), ai=AI.find(x=>x.animationName==='promiBlink');
          return {vis:d?getComputedStyle(d).display:null, anim:!!a, dur:a?a.effect.getTiming().duration:null, iAnim:!!ai, phase:(a&&ai)?Math.round(((a.effect.getComputedTiming().progress-ai.effect.getComputedTiming().progress)*1150%1150+1150)%1150):null}; }""")
        if reduit:
            juge('[%s] O · rien ne clignote : ni le départ, ni le I de PROMI' % T, st['vis'] == 'block' and not st['anim'] and not st['iAnim'], st)
        else:
            juge('[%s] O · le départ clignote avec l\'animation du I (promiBlink, 1,15 s), en phase avec lui' % T, st['anim'] and st['dur'] == 1150 and st['iAnim'] and st['phase'] is not None and (st['phase'] <= 40 or st['phase'] >= 1110), st)
        for _ in range(40):
            if pg.evaluate("()=>{ const d=document.getElementById('onbDepart'); return d && getComputedStyle(d).opacity==='1'; }"): break
            pg.wait_for_timeout(50)
        r = lit(pg, '#onbTrait')
        juge('[%s] O · à la phase pleine, la pointe ET le trait de départ sont orange' % T, r and r[0] >= 60 and r[1] >= 60, r and 'pointe %d px · trait %d px' % (r[0], r[1]))
        if not reduit:
            z = r[2] if r else {'x': 43, 'y': 700}
            B.tap(pg, z['x'] - 4, z['y']); pg.wait_for_timeout(600)
            st2 = pg.evaluate("()=>{ const d=document.getElementById('onbDepart'); return {anim:d.getAnimations().some(x=>x.animationName==='promiBlink'), op:getComputedStyle(d).opacity, cls:d.className}; }")
            r2 = lit(pg, '#onbTrait')
            juge('[%s] O · touché une fois, le départ ne clignote plus : orange fixe' % T, not st2['anim'] and st2['op'] == '1' and r2 and r2[0] >= 60 and r2[1] >= 60, '%s · pointe %s px · trait %s px' % (st2, r2 and r2[0], r2 and r2[1]))
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
