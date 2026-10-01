#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_dalle_figee.py — UNE DALLE GARDE SA COULEUR COMME ELLE GARDE SON MONDE (Q213, 13 sept. 2026).

Avant ce lot, la couleur d'une dalle était tirée au hasard À CHAQUE CHARGEMENT (`cc()`, `Math.random`) :
« planter un arbre » sortait bleue, puis lilas. Et les peintres des cartes (Index, Fil) n'avaient pas le monde
de la plantation. Contrats :

  A · MÊME COULEUR À CHAQUE OUVERTURE   — 3 pages neuves × 2 thèmes : pour chaque Promi planté,
                                           `Toile.colorOf(id)` est la même partout
  B · UNE DALLE PLANTÉE GARDE SA COULEUR — on plante par le chemin de l'app (`Toile.addPromi`), on relit sa
                                           couleur, on sauve, on RECHARGE : la même
  C · LA TOILE NE LA RETIRE PAS          — après `Toile.sync` (qui refait toutes les dalles), la même
  D · LES CARTES SUIVENT LE STUDIO (v34) — chaque dalle peinte par l'Index et le Fil l'est dans le monde courant,
                                           même celle d'un Promi planté dans un autre monde (on en plante un en pixel · terre)

Preuve (§7) : `APP_DALLE=http://127.0.0.1:8752/sauvegardes/app-avant-lot-dalle-figee.html` doit ROUGIR.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_DALLE', "http://127.0.0.1:8752/app.html")
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-58s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-58s KO  %s' % (nom, detail))


# ⚠ PAR TITRE ET PERSONNE, JAMAIS PAR ID : les ids du jeu de démonstration changent d'un chargement à l'autre
#   (chantier 71). Le premier passage comparait l'id 129 d'une page à l'id 129 d'une autre — deux Promi différents.
COULEURS = "()=>{const o={};promises.filter(p=>!p.draft&&!p.req).forEach(p=>{o[p.title+'|'+p.who]=Toile.colorOf(p.id);});return o;}"


def ouvre(ctx, th):
    pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(900)
    try: pg.evaluate("()=>{if(window.assureLiaisonDalles)assureLiaisonDalles();}")
    except Exception: pass
    pg.wait_for_timeout(600)
    return pg


with sync_playwright() as p:
    b = p.chromium.launch()
    # A
    releves = []
    for th in ['light', 'dark']:
        for k in range(3):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            pg = ouvre(ctx, th); releves.append((th, k, pg.evaluate(COULEURS))); ctx.close()
    ref = releves[0][2]
    diff = []
    for th, k, r in releves[1:]:
        for pid, c in r.items():
            if ref.get(pid) != c: diff.append('%s·%d id %s %s≠%s' % (th, k, pid, ref.get(pid), c))
    nuls = [pid for pid, c in ref.items() if c is None]
    t('A · même couleur à chaque ouverture (3 × 2 thèmes)', not diff and not nuls and len(ref) >= 10,
      '%d dalles · %d écarts %s' % (len(ref), len(diff), ('— ' + ' | '.join(diff[:3])) if diff else ''))

    # B, C, D — une page qu'on garde, localStorage compris
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ouvre(ctx, 'light')
    np_ = pg.evaluate("""()=>{const q=P('juge dalle figée','moi',5,2,'encours',null); promises.push(q);
        Toile.addPromi(q.id); return {id:q.id};}""")
    pg.wait_for_timeout(1200)
    c1 = pg.evaluate("(id)=>Toile.colorOf(id)", np_['id'])
    pg.evaluate("()=>{Toile.sync(promises.filter(p=>!p.draft&&!p.req).map(p=>p.id));}"); pg.wait_for_timeout(1500)
    c2 = pg.evaluate("(id)=>Toile.colorOf(id)", np_['id'])
    avant = pg.evaluate(COULEURS)
    t('C · après sync, la Toile rend la même couleur', c1 is not None and c1 == c2 and all(avant[k] == ref[k] for k in avant if k in ref),
      'plantée %s → %s' % (c1, c2))
    # ⚠ L'app reconstruit le jeu de démonstration à chaque chargement : on ne peut pas recharger pour relire.
    #   On transporte donc le Promi SAUVÉ (sa forme JSON, comme saveState l'écrit) dans une page NEUVE.
    sauve = pg.evaluate("(id)=>JSON.stringify(promises.find(x=>x.id===id))", np_['id'])
    pg.close()
    pg = ouvre(ctx, 'light')
    c3 = pg.evaluate("""(s)=>{const q=JSON.parse(s); q.id=nid++; promises.push(q);
        Toile.sync(promises.filter(p=>!p.draft&&!p.req).map(p=>p.id)); return new Promise(r=>setTimeout(()=>r(Toile.colorOf(q.id)),1200));}""", sauve)
    t('B · une dalle plantée garde sa couleur, sauvée puis rechargée', c1 is not None and c3 == c1, '%s → %s · dalle sauvée %s' % (c1, c3, json.loads(sauve).get('dalle')))

    # D — ⚑ v34 (Tom, 23 sept.) : « tout suit le Studio — le Fil, l'Index… ; seule exception, l'Aura ». Réécrit au niveau
    #     de la décision (§7) : même intention — le monde des cartes est TENU —, règle inverse. Un Promi planté dans un AUTRE
    #     monde (pixel · terre) doit être peint dans le monde du STUDIO. (Original : sauvegardes/redteam_dalle_figee-avant-v34.py)
    pg.evaluate("""()=>{const q=promises.find(p=>!p.draft&&!p.req&&!p.nuee); q.monde={m:'pixel',p:'terre',h:0}; window._jugeId=q.id;
        Toile.setTheme('encre');
        window._appels=[]; const o=Toile.dalleTrame; Toile.dalleTrame=function(cv,id,k,monde){ const C=Toile.mondeCourant(); const r=o.apply(this,arguments);
          window._appels.push({id:id, peint:(cv&&cv.__dalleInfo&&cv.__dalleInfo.monde)||null, studio:C, pile:(new Error().stack||'')}); return r; };}""")
    pg.evaluate("()=>{closeAll();window.ouvrirIndex()}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{closeAll();setView('fil')}"); pg.wait_for_timeout(2500)
    r = pg.evaluate("""()=>{const A=window._appels.filter(a=>/peintCarte|peintBandeau/.test(a.pile)&&a.peint);
        const eg=(a,b)=>a&&b&&a.m===b.m&&a.p===b.p&&(+a.h||0)===(+b.h||0);
        const faux=A.filter(a=>!eg(a.peint,a.studio)).length;
        const juge=A.filter(a=>a.id===window._jugeId);
        const bon=juge.length>0 && juge.every(a=>a.peint.m==='encre' && a.peint.m!=='pixel');
        return {n:A.length,juge:juge.length,bon,faux};}""")
    t('D · les peintres des cartes suivent le Studio (v34)', r['n'] > 0 and r['bon'] and r['faux'] == 0,
      '%d appels · %d pour le Promi planté en « pixel · terre », peint dans le Studio (encre) : %s · %d hors du Studio' % (r['n'], r['juge'], r['bon'], r['faux']))
    ctx.close(); b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
