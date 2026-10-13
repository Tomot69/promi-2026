"""v145 — les captures « comme Tom » des parts (C-115) et de la ligne « Un mot… » (C-116), et la marque de version (C-117)."""
import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import banc_tom as B
D = 'planche-v145/'
def ouvre_fiche(pg, pid):
    # une vraie pause entre la fermeture et l'ouverture (CLAUDE.md v139 : dans la même tâche, la phrase complète n'est pas posée)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2800)
def scene(sombre):
    S = []
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx)
        # 1 · une promesse à trois personnes, que l'on DEMANDE (ce sont elles qui tiennent) : aucune part, puis une, puis deux
        B.plante_doigt(pg, 'venir au concert', 'moi', 0)
        pid = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.who='Rachel, Marion, Nico'; p.req=true; p.status='encours'; delete p.parts; try{save()}catch(e){} return p.id; }")
        ouvre_fiche(pg, pid); S.append(('3 personnes · aucune part', B.capture(pg)))
        pg.evaluate("id=>{ var p=promises.find(x=>x.id===id); p.parts={'Marion':'2026-10-11T10:00:00.000Z'}; try{save()}catch(e){} }", pid)
        ouvre_fiche(pg, pid); S.append(('3 personnes · une part tracée', B.capture(pg)))
        # la liste des noms, au toucher du trait (seconde moitié)
        z = pg.evaluate("()=>{ var c=document.getElementById('dpTrameCv'); var d=c&&c.getAttribute('data-parts'); return d; }")
        t = pg.evaluate("()=>{ var c=document.getElementById('dpTrameCv'); var a=(c.getAttribute('data-trait')||'').split(','); return a.map(Number); }")
        yy = t[0] - 0.34 * t[1] * (290 / 390.0) if len(t) >= 2 and t[0] == t[0] else 280
        B.tap(pg, 290, yy); pg.wait_for_timeout(900); S.append(('toucher le trait · qui a tracé', B.capture(pg)))
        pg.evaluate("()=>{ try{ window._parts.ferme(); }catch(e){} }"); pg.wait_for_timeout(300)
        # 2 · six personnes : le compte « k SUR n »
        B.plante_doigt(pg, 'ranger le local', 'moi', 0)
        pid2 = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.who='Rachel, Marion, Nico, Adrien, Lou, Sam'; p.req=true; p.status='encours'; p.parts={'Rachel':'2026-10-10T10:00:00.000Z','Nico':'2026-10-11T10:00:00.000Z','Lou':'2026-10-12T10:00:00.000Z'}; try{save()}catch(e){} return p.id; }")
        ouvre_fiche(pg, pid2); S.append(('6 personnes · « 3 SUR 6 »', B.capture(pg)))
        # 3 · une parole REÇUE : la ligne « Un mot… », fermée, ouverte, puis un mot posé
        B.plante_doigt(pg, 'te rendre ton vélo', 'moi', 0)
        pid3 = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.from='Marion'; p.who='moi'; p.status='encours'; try{save()}catch(e){} return p.id; }")
        ouvre_fiche(pg, pid3); S.append(('reçue · la ligne « Un mot… »', B.capture(pg)))
        B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900); S.append(('reçue · la saisie ouverte', B.capture(pg)))
        pg.evaluate("()=>{ var i=document.querySelector('#cm5Ligne .cm5-saisie'); if(i){ i.value='Merci, samedi me va.'; i.dispatchEvent(new Event('input',{bubbles:true})); } }"); pg.wait_for_timeout(200)
        B.tap_sel(pg, '#cm5Ligne .cm5-va'); pg.wait_for_timeout(1200); S.append(('reçue · un mot posé', B.capture(pg)))
        print('erreurs', pg.__dict__['erreurs'][:3], '· parts déclarées', z); b.close()
    return S
def planche(nom, S):
    ims = [Image.open(io.BytesIO(x[1])).convert('RGB') for x in S]; w, h = ims[0].size; E = 60; T = 120
    P = Image.new('RGB', (len(ims) * (w + E) + E, h + T + E), (236, 232, 222)); d = ImageDraw.Draw(P)
    try: f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 44)
    except Exception: f = None
    for i, im in enumerate(ims): P.paste(im, (E + i * (w + E), T)); d.text((E + i * (w + E), 36), S[i][0], fill=(32, 25, 8), font=f)
    P.save(D + nom); print(nom, P.size)
if '--marque' in sys.argv:
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, q='?mesure=1'); pg.wait_for_timeout(1500)
        io.open(D + 'marque-version.png', 'wb').write(B.capture(pg)); print('marque lue :', pg.evaluate("()=>{ var e=document.getElementById('versionMarque'); return e&&e.textContent; }")); b.close()
else:
    for sombre in (False, True):
        S = scene(sombre); planche('PLANCHE-parts-%s.png' % ('sombre' if sombre else 'clair'), S[:4]); planche('PLANCHE-un-mot-%s.png' % ('sombre' if sombre else 'clair'), S[4:])
