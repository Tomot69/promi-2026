#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_cercle_couleur.py — LA COULEUR, CINQUIÈME RÉGLAGE DU CERCLE (Tom, 13 sept. 2026).

  « En mode Cercle, on doit pouvoir choisir la couleur de sa dalle — à la page + et dans Peaufiner de chaque Promi, Chiche
    et Nuée. Code couleur libre, ou une couleur de la palette du Studio. C'est un cinquième réglage du Cercle : il rejoint
    récurrence, rappel, importance et mémoire dans le bloc verrouillé. Vérifie que le bloc tient à cinq. »

  1 · LE BLOC TIENT À CINQ — fiche, page +, Réglages : cinq rangées dans l'ordre, LA COULEUR en dernier, bloc 384
      (5 × 64 + 4 × 16), encart à 147 (centré), rien ne se superpose entre rangées.
  2 · VERROUILLÉ SANS LE CERCLE — LA COULEUR floutée et inerte comme les quatre autres.
  3 · UNE COULEUR DE LA PALETTE — au Cercle payé, un ton choisi dans la fiche : la dalle de la Toile prend CE ton.
  4 · UN CODE LIBRE — « #12AB34 » : la dalle de la Toile est rgb(18,171,52), la valeur l'affiche.
  5 · LE CHOIX TIENT — une plantation plus tard (le moteur recalcule ses tons), la dalle garde le code.
  6 · À LA PAGE + — un code choisi dans son Peaufiner est celui de la dalle plantée ; rouvrir la page + l'efface.
  7 · OUVERT, IL NE RECOUVRE RIEN — la rangée ouverte pousse ce qui suit.

Les cotes et le code sont EN DUR (§7 : un juge ne lit pas la valeur qu'il vérifie).
Preuve (§7) : `APP_CC=http://127.0.0.1:8752/sauvegardes/app-avant-lot-cercle-couleur.html` doit ROUGIR.
"""
import os, sys
from importlib.machinery import SourceFileLoader
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_CC', "http://127.0.0.1:8752/app.html")
R = os.path.dirname(os.path.abspath(__file__))
J = SourceFileLoader("j", R + "/releve-S3-page-plus.py").load_module()
ORDRE = ['RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE', 'LA COULEUR']
BLOC, ENCART = 384, 147          # 5 × 64 + 4 × 16 ; (384 − 90) ÷ 2
CODE, RGB = '#12AB34', 'rgb(18,171,52)'
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-64s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-64s KO  %s' % (nom, detail))


BLOCJS = """(h)=>{const c=document.querySelector(h+' .s2-cercle'); if(!c) return null; const k=document.getElementById('device').getBoundingClientRect().width/390;
  const R=e=>{const r=e.getBoundingClientRect();return {y:r.top/k,h:r.height/k,b:r.bottom/k}}; const b=R(c);
  const regs=[...c.querySelectorAll(':scope > .s2-reg')]; const enc=c.querySelector('.s2-encart,.set-cercle');
  let sup=0; for(let i=1;i<regs.length;i++){ if(R(regs[i]).y < R(regs[i-1]).b-0.5) sup++; }
  const last=regs[regs.length-1];
  return {n:regs.length, mots:regs.map(r=>(r.querySelector('.s2-lab')||{}).textContent), h:b.h, enc: enc&&getComputedStyle(enc).display!=='none' ? R(enc).y-b.y : null,
          sup, dernierDedans: last ? R(last).b <= b.b+0.5 : false,
          flou: last ? getComputedStyle(last).filter : '', pe: last ? getComputedStyle(last).pointerEvents : ''};}"""


def bloc(pg, hote, T, ou, attendEncart=True):
    g = pg.evaluate(BLOCJS, hote)
    t('[%s] 1 · %s : cinq réglages, LA COULEUR en dernier' % (T, ou), bool(g) and g['mots'] == ORDRE, str(g and g['mots']))
    t('[%s] 1 · %s : bloc de 384, tout dedans, rien ne se superpose' % (T, ou), bool(g) and abs(g['h'] - BLOC) < 1 and g['dernierDedans'] and g['sup'] == 0,
      g and 'h %.1f · sup %d' % (g['h'], g['sup']))
    if attendEncart:
        t('[%s] 1 · %s : encart centré à 147' % (T, ou), bool(g) and g['enc'] is not None and abs(g['enc'] - ENCART) < 1, g and 'encart %s' % g['enc'])
    return g


with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['dark', 'light']:
        T = 'sombre' if th == 'dark' else 'clair'
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        er = []; pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);setPremium(false);}", th)
        pg.wait_for_timeout(600)
        # ── fiche, non payé ──
        pid = pg.evaluate("()=>{closeAll();const p=promises.filter(p=>!p.draft&&!p.req)[0];openDetail(p.id);return p.id;}"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        g = bloc(pg, '#detailPoster', T, 'fiche')
        t('[%s] 2 · sans le Cercle, LA COULEUR est floutée et inerte' % T, bool(g) and g['n'] == 5 and 'blur' in (g['flou'] or '') and g['pe'] == 'none', g and '%s · %s' % (g['flou'], g['pe']))
        # ── Réglages ──
        pg.evaluate("()=>{closeAll();const s=document.getElementById('settingsBtn');if(s)s.click();else document.getElementById('settingsScreen').classList.add('show');}"); pg.wait_for_timeout(1300)
        # ⚑ v42 — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7 ; Tom, 24 sept. : « la décision est bonne, c'est le juge qui
        #   décrit l'état d'avant »). Décision v16 n° 4 : « les réglages du Cercle quittent les Réglages — ils appartiennent à
        #   un Promi (§5), ils restent dans Peaufiner. L'encart ✦ Le Cercle reste seul. » Les cinq réglages restent vérifiés
        #   dans Peaufiner (la fiche, plus haut) et à la page + (plus bas). Ici : AUCUN réglage, l'encart seul et visible,
        #   et il ouvre Le Cercle. Version d'avant : sauvegardes/redteam_cercle_couleur-avant-v42.py
        r = pg.evaluate("""()=>{const c=document.querySelector('#settingsScreen .s2-cercle'); if(!c) return null;
          const e=document.getElementById('openPlusTop'), r=e?e.getBoundingClientRect():null;
          const vu=!!(e && r.width>40 && r.height>40 && getComputedStyle(e).visibility!=='hidden' && getComputedStyle(e).display!=='none');
          return {regs:c.querySelectorAll('.s2-reg').length, encDedans:!!(e&&c.contains(e)), vu:vu,
                  mot:e?(e.querySelector('.sc-t')||{}).textContent:''};}""")
        t('[%s] 1 · Réglages : aucun réglage du Cercle (v16)' % T, bool(r) and r['regs'] == 0, r and '%d rangée(s)' % r['regs'])
        t('[%s] 1 · Réglages : l\'encart « ✦ Le Cercle » seul, visible' % T, bool(r) and r['encDedans'] and r['vu'] and 'Le Cercle' in (r['mot'] or ''), str(r))
        pg.evaluate("()=>document.getElementById('openPlusTop').click()"); pg.wait_for_timeout(1200)
        t('[%s] 1 · Réglages : l\'encart ouvre Le Cercle' % T, pg.evaluate("()=>document.getElementById('plusScreen').classList.contains('show')"))
        # ── page +, non payé ──
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)
        pg.evaluate(J.SCENE, 'pp_promi_rachel'); pg.wait_for_timeout(1400)
        pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1600)
        bloc(pg, '#createSheet', T, 'page +')
        # ── fiche, payé ──
        pg.evaluate("()=>{closeAll();setPremium(true);}"); pg.wait_for_timeout(600)
        pg.evaluate("(i)=>openDetail(i)", pid); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const r=document.querySelector('#detailPoster .s2-couleur');if(r)r.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(400)
        a = pg.evaluate("""()=>{const r=document.querySelector('#detailPoster .s2-couleur'); if(!r) return null; const s=getComputedStyle(r); return [s.filter, s.pointerEvents];}""")
        try:
            pg.locator('#detailPoster .s2-couleur .s2-lab').click(timeout=3000); pg.wait_for_timeout(600)
        except Exception as e:
            pass
        ton = pg.evaluate("()=>{const m=Toile.mondeCourant(); const c=(Toile.tonsDe?Toile.tonsDe(m.p,m.h):null); return c?c[2]:null;}")
        if ton is None:  # version fautive : la palette du Studio lue à la source
            ton = pg.evaluate("()=>{const m=Toile.mondeCourant(); return Toile.palettes()[m.p].cols[2];}")
        cible = pg.evaluate("(i)=>{const p=promises.find(q=>q.id===i); return p.dalle?p.dalle.ci:null;}", pid)
        ci = 2 if cible != 2 else 3
        if ci == 3:
            ton = pg.evaluate("()=>{const m=Toile.mondeCourant(); return Toile.tonsDe?Toile.tonsDe(m.p,m.h)[3]:Toile.palettes()[m.p].cols[3];}")
        try:
            pg.locator('#detailPoster .s2-couleur .cc-ton[data-ton="%d"]' % ci).click(timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(1300)
        c3 = pg.evaluate("(i)=>Toile.colorOf(i)", pid)
        att3 = 'rgb(%d,%d,%d)' % tuple(int(round(v)) for v in ton)
        t('[%s] 3 · un ton de la palette : la dalle de la Toile le prend' % T, c3 == att3 and pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"),
          '%s attendu %s · flou %s' % (c3, att3, a))
        try:
            pg.locator('#detailPoster .s2-couleur .cc-code').fill(CODE, timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(1300)
        c4 = pg.evaluate("(i)=>Toile.colorOf(i)", pid)
        val = pg.evaluate("()=>{const v=document.querySelector('#detailPoster .s2-couleur .s2-val');return v?v.textContent.trim():null;}")
        t('[%s] 4 · un code libre : la dalle est %s et la valeur l\'affiche' % (T, CODE), c4 == RGB and val == CODE, '%s · « %s »' % (c4, val))
        # 7 · ouvert, rien n'est recouvert
        o = pg.evaluate("""()=>{const r=document.querySelector('#detailPoster .s2-couleur.s2-ouv'); if(!r) return null; const c=r.closest('.s2-cercle');
          const nx=c.nextElementSibling; let n=nx; while(n && (getComputedStyle(n).display==='none'||n.getBoundingClientRect().height<2)) n=n.nextElementSibling;
          const rb=r.getBoundingClientRect().bottom, cb=c.getBoundingClientRect().bottom; return {dedans: rb<=cb+0.5, suivant: n ? n.getBoundingClientRect().top >= cb-0.5 : true, h:r.getBoundingClientRect().height};}""")
        t('[%s] 7 · LA COULEUR ouverte ne recouvre rien' % T, bool(o) and o['dedans'] and o['suivant'], str(o))
        # 5 · le choix tient après une plantation
        pg.evaluate("()=>{closeAll(); const q=P('juge couleur','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);}"); pg.wait_for_timeout(2200)
        c5 = pg.evaluate("(i)=>Toile.colorOf(i)", pid)
        t('[%s] 5 · le code tient après une plantation' % T, c5 == RGB, c5)
        # 6 · la page +
        pg.evaluate(J.SCENE, 'pp_promi_rachel'); pg.wait_for_timeout(1400)
        pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1600)
        pg.evaluate("()=>{const r=document.querySelector('#createSheet .s2-couleur');if(r)r.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(400)
        try:
            pg.locator('#createSheet .s2-couleur .s2-lab').click(timeout=3000); pg.wait_for_timeout(500)
            pg.locator('#createSheet .s2-couleur .cc-code').fill('#C0FFEE', timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(500)
        att6 = 'rgb(192,255,238)'   # #C0FFEE, en dur — un tirage au hasard ne peut pas tomber dessus
        c6 = pg.evaluate("()=>{closeAll(); const q=P('juge page plus','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id); return q.id;}")
        pg.wait_for_timeout(2000)
        col6 = pg.evaluate("(i)=>Toile.colorOf(i)", c6)
        t('[%s] 6 · un code choisi à la page + est celui de la dalle plantée' % T, col6 == att6, '%s attendu %s' % (col6, att6))
        pg.evaluate("()=>{ window._couleurAPlanter={ci:3,lit:0}; }")
        pg.evaluate(J.SCENE, 'pp_promi_vide'); pg.wait_for_timeout(1400)
        t('[%s] 6 · rouvrir la page + efface le choix en attente' % T, pg.evaluate("()=>window._couleurAPlanter==null"), '')
        t('[%s] aucune erreur JS' % T, not er, str(er[:2]))
        pg.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
