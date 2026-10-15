#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_partage_toile.py — L'IMAGE PARTAGÉE DE LA TOILE EST LA TOILE AFFICHÉE (v143, Tom, 12 oct. 2026 — C-105).

« Sous Ritournelle, l'image de “Partager ma Toile” n'est pas cohérente avec la Toile qu'on voit. Vérifie les vingt mondes : l'image partagée
reprend les mêmes dalles, aux mêmes places, mêmes formes, mêmes couleurs, même cadrage que l'écran. »

LA CAUSE NOMMÉE : l'image était rendue « Toile entière, sans cadrage », sur un autre fond, alors que l'écran cadre les paroles.

Comme Tom (banc_tom : WebKit, 390 × 844 ×3, Toile vide, trois paroles plantées par l'app), sous les VINGT mondes. L'image partagée est celle que
le VRAI bouton produit (« Enregistrer » du plateau, puis « Partager ») : on garde le canevas que le moteur rend à cet instant. Elle est comparée
à la Toile affichée (le canevas de l'accueil), les deux ramenées à 78 × 169 (un cinquième : la respiration d'une matière ne compte pas, la
place, la forme, la couleur et le cadrage d'une dalle, si) :
  · écart moyen ≤ 9 niveaux (sur 255, par canal) ;  · moins de 6 % de cases à plus de 40 niveaux d'écart.
Planche des écarts : planche-v143/partage-<fichier>.png (écran | image partagée, par monde).
Preuve : rouge sur v142 (python3 redteam_partage_toile.py zz-av143.html).     --mondes=a,b pour une passe courte.

⚑ v146 (Tom, 14 oct. 2026, C-119) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_partage_toile-avant-v146.py).
« Supprime de l'encart du haut de l'accueil le bouton [Enregistrer] […]. On enregistre sa Toile depuis la page Partager : on va jusqu'au bout,
et là il y a le choix des réseaux sociaux, enregistrer en fichier, en photo, etc. Vérifie que ce chemin enregistre bien (photo et fichier). »
  · le bouton « Enregistrer » n'est plus sur le plateau de l'accueil (plus de `#enrToile`) ;
  · l'image comparée à l'écran est celle de la page Partager (le rendu du moteur à l'ouverture) — même règle, mêmes seuils ;
  · LE CHEMIN ENREGISTRE : le bouton « Partager » de la page (`#shShareBtn`) remet un FICHIER image (mon-promi.png, PNG, grand côté 3840) à la
    feuille de partage du téléphone — c'est elle qui porte « Enregistrer l'image » (la photo) et « Enregistrer dans Fichiers » (le fichier),
    simulée ici par `navigator.share` ; et, quand le navigateur n'a pas de feuille de partage, un téléchargement du même fichier part.
"""
import sys, io, base64
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageDraw
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
SEL = next((a.split('=')[1].split(',') for a in sys.argv[1:] if a.startswith('--mondes=')), None)
MOY_MAX, FORT_MAX = 9.0, 0.06
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:230]), flush=True)
def img(u): return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGB')
def compare(a, b):
    a = a.resize((78, 169), Image.BOX); b = b.resize((78, 169), Image.BOX); d = ImageChops.difference(a, b); px = list(d.getdata())
    moy = sum(sum(p) for p in px) / (3.0 * len(px)); fort = sum(1 for p in px if max(p) > 40) / float(len(px)); return moy, fort
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    for t in ('arroser le figuier', 'écrire à Lou', 'réparer le vélo'): plante(pg, t)
    # la feuille de partage du téléphone, simulée : elle reçoit ce que l'app lui remet
    pg.evaluate("()=>{ try{ Object.defineProperty(navigator,'canShare',{value:function(){ return true; },configurable:true}); Object.defineProperty(navigator,'share',{value:function(d){ window.__part=d; return Promise.resolve(); },configurable:true}); }catch(e){} }")
    pg.evaluate("()=>{ try{setPremium(true)}catch(e){} const f=Toile.renderTo; window.__rt=null; Toile.renderTo=function(cv){ const r=f.apply(this,arguments); try{ window.__rt=cv.toDataURL('image/png'); }catch(e){} return r; }; }")
    mondes = pg.evaluate("()=>{ const m=/order=\\[([^\\]]+)\\]/.exec([...document.scripts].map(x=>x.textContent).join('\\n')); return m ? m[1].replace(/['\"\\s]/g,'').split(',') : []; }")
    if SEL: mondes = [m for m in mondes if m in SEL]
    juge('les mondes sont trouvés (%d)' % len(mondes), len(mondes) == (len(SEL) if SEL else 20), mondes)
    planche = []
    for m in mondes:
        pg.evaluate("(m)=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(4200)
        ecran = img(pg.evaluate("()=>document.getElementById('toileCv').toDataURL('image/png')"))
        pg.evaluate("()=>{ window.__rt=null; window.__part=null; }")
        if m == mondes[0]: juge('le bouton « Enregistrer » n\'est plus sur le plateau de l\'accueil', not pg.evaluate("()=>!!document.getElementById('enrToile')"))
        tap_sel(pg, '#shareBtn'); pg.wait_for_timeout(2600); u = pg.evaluate("()=>window.__rt")
        if not u: juge('%s · « Partager » rend la Toile par le moteur' % m, False, 'aucun rendu vu'); continue
        part = img(u); moy, fort = compare(ecran, part)
        juge('%s · l\'image de la page Partager est la Toile affichée (écart moyen ≤ %.0f, cases très différentes ≤ %.0f %%)' % (m, MOY_MAX, 100 * FORT_MAX), moy <= MOY_MAX and fort <= FORT_MAX, 'écart moyen %.1f · %.1f %% de cases très différentes · image %d × %d' % (moy, 100 * fort, part.width, part.height))
        # le chemin ENREGISTRE : le bouton de la page remet un fichier image à la feuille de partage du téléphone
        if m in mondes[:3]:
            r = tap_sel(pg, '#shShareBtn'); pg.wait_for_timeout(2600)
            f = pg.evaluate("""async ()=>{ const d=window.__part; if(!d||!d.files||!d.files.length) return null; const f=d.files[0]; let w=0,h=0; try{ const b=await createImageBitmap(f); w=b.width; h=b.height; }catch(e){}
                const a=new Uint8Array(await f.slice(0,8).arrayBuffer()); return {nom:f.name, type:f.type, octets:f.size, w:w, h:h, png:(a[0]===0x89&&a[1]===0x50&&a[2]===0x4E&&a[3]===0x47)}; }""")
            juge('%s · le bouton « Partager » de la page remet un fichier image à la feuille de partage (photo et fichier s\'y enregistrent)' % m,
                 bool(f) and f['png'] and f['type'] == 'image/png' and f['nom'] == 'mon-promi.png' and f['octets'] > 60000 and max(f['w'], f['h']) == 3840, f if f else 'bouton %s · rien remis' % (r,))
        pg.evaluate("()=>{ try{ const s=document.getElementById('shareScreen'); const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        planche.append((m, ecran.resize((195, 422)), part.resize((195, 422)), moy))
    # sans feuille de partage (un navigateur de bureau) : le même fichier part en téléchargement
    try:
        pg.evaluate("()=>{ try{closeAll()}catch(e){} try{ Object.defineProperty(navigator,'canShare',{value:undefined,configurable:true}); }catch(e){} }"); pg.wait_for_timeout(400)
        tap_sel(pg, '#shareBtn'); pg.wait_for_timeout(2600)
        with pg.expect_download(timeout=9000) as dl: tap_sel(pg, '#shShareBtn')
        d = dl.value; chemin = d.path(); import os
        juge('sans feuille de partage, le fichier mon-promi.png se télécharge', d.suggested_filename == 'mon-promi.png' and chemin and os.path.getsize(chemin) > 60000, '%s · %s octets' % (d.suggested_filename, chemin and os.path.getsize(chemin)))
    except Exception as ex:
        juge('sans feuille de partage, le fichier mon-promi.png se télécharge', False, str(ex)[:160])
    juge('aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    ctx.close(); b.close()
if planche:
    n = len(planche); cols = 5; rows = (n + cols - 1) // cols; W = Image.new('RGB', (cols * 410, rows * 460), 'white'); g = ImageDraw.Draw(W)
    for i, (m, a, c, moy) in enumerate(planche):
        x = (i % cols) * 410; y = (i // cols) * 460; W.paste(a, (x, y + 30)); W.paste(c, (x + 200, y + 30)); g.text((x + 4, y + 8), '%s — écran | partagé — écart %.1f' % (m, moy), fill=(221, 77, 35) if moy > MOY_MAX else (32, 25, 8))
    W.save('planche-v146/partage-%s.png' % F.replace('.html', '').replace('/', '-'))
n = sum(1 for _, c in res if c); print('\n%d/%d' % (n, len(res)))
if n < len(res): sys.exit(1)
