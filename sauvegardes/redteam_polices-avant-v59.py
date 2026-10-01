#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_polices.py — AUCUNE GRAISSE HORS DES FACES EMBARQUÉES.

En navigateur, une graisse absente se substitue **en silence** : la plus proche, ou une
oblique synthétique. **En Swift, elle casse.** Le prototype étant la spécification du
portage, tout couple `police | graisse | style` demandé doit exister en `@font-face`.

Les faces réellement embarquées, relevées dans `app.html` à chaque passage — jamais
recopiées ici :

    Fraunces 600 normal · Fraunces 600 italique
    Bricolage 600 · Bricolage 700
    Apfel 400 · ApfelMid 500              (aucune italique)

Le contrôle parcourt les écrans, lit le style CALCULÉ de chaque élément qui porte du texte,
et échoue sur tout couple hors liste. Il donne le compte, l'écran, et un exemple de nœud —
de quoi aller corriger à la source.

Usage :  python3 redteam_polices.py [--verbose] [--tout]
         --tout : liste chaque élément fautif, pas seulement un exemple par couple
"""
import io
import re
import sys
from collections import defaultdict
from playwright.sync_api import sync_playwright

RACINE = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
TOUT = '--tout' in sys.argv


def faces_embarquees():
    """Les `@font-face` du fichier. La liste ne vit QUE là : si on embarque une graisse,
    le contrôle la connaît au passage suivant, sans qu'on touche au test."""
    S = io.open(RACINE + '/app.html', encoding='utf-8').read()
    ok = set()
    for m in re.finditer(r"@font-face\{([^}]*)\}", S):
        d = m.group(1)
        fam = re.search(r"font-family:\s*['\"]?([A-Za-z][A-Za-z ]*?)['\"]?\s*;", d)
        wt = re.search(r"font-weight:\s*(\d+)", d)
        st = re.search(r"font-style:\s*(italic|normal)", d)
        if not fam:
            continue
        ok.add((fam.group(1).strip().lower(),
                int(wt.group(1)) if wt else 400,
                (st.group(1) if st else 'normal')))
    return ok


# ── LES ÉCRANS. On ouvre, on laisse peindre, on relève. ─────────────────────────────────
SCENES = [
    ('Toile',      "()=>{if(window.closeAll)closeAll(); setView('toile');}"),
    ('Fil',        "()=>{if(window.closeAll)closeAll(); setView('fil');}"),
    ('Index',      "()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex();}"),
    ('fiche',      "()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&!q.req)[0]; if(p)openDetail(p.id);}"),
    ('fiche · Peaufiner', "()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t)t.click();}"),
    ('Nuée',       "()=>{if(window.closeAll)closeAll(); const k=Object.keys(NUE)[0]; if(k)openEssaim(k);}"),
    ('Nuée · Peaufiner', "()=>{const t=document.querySelector('#dpDetails .dpd-tog'); if(t)t.click();}"),
    ('page +',     "()=>{if(window.closeAll)closeAll(); document.getElementById('createBtn').click();}"),
    ('Aura',       "()=>{if(window.closeAll)closeAll(); if(window.openAura)openAura(); else {const b=document.querySelector('[onclick*=Aura],#auraBtn'); if(b)b.click();}}"),
    ('Studio',     "()=>{if(window.closeAll)closeAll(); if(window.openStudio)openStudio();}"),
    ('Réglages',   "()=>{if(window.closeAll)closeAll(); if(window.openSettings)openSettings(); else if(window.openReglages)openReglages();}"),
    ('Partager',   "()=>{if(window.closeAll)closeAll(); const s=document.getElementById('shareScreen'); if(s){s.classList.add('show'); if(window.shareRender)shareRender();}}"),
]

RELEVE = r"""()=>{
  const out=[];
  /* ⚠ ON NE RELÈVE QUE CE QUI EST DANS LE CADRE. Les feuilles fermées ne sont pas en
     `display:none` — elles sont TRANSLATÉES hors champ. Sans ce filtre, chaque écran
     comptait aussi tous les autres : 3160 éléments là où il y en a le dixième, et une
     attribution par écran qui ne voulait rien dire (140 fautes « sur tous les écrans »). */
  const dev=document.getElementById('device').getBoundingClientRect();
  const sc=dev.width/390;
  document.querySelectorAll('*').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return;
    const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return;
    const x=(r.left-dev.left)/sc, y=(r.top-dev.top)/sc;
    const lw=r.width/sc, lh=r.height/sc;
    if(x+lw<2 || x>388 || y+lh<2 || y>842) return;
    /* on ne juge QUE ce qui porte du texte : une boîte vide n'affiche aucune police */
    let t='';
    e.childNodes.forEach(n=>{ if(n.nodeType===3) t+=n.nodeValue; });
    if(!t.trim()) return;
    const fam=(c.fontFamily||'').split(',')[0].replace(/["']/g,'').trim();
    const w=parseInt(c.fontWeight,10)||400;
    const st=(c.fontStyle||'normal').indexOf('italic')>=0?'italic':'normal';
    const cle=fam+'|'+w+'|'+st;
    const noeud=(e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean).slice(0,2).join('.'));
    out.push({fam:fam, w:w, st:st, noeud:noeud.slice(0,30), mot:t.trim().slice(0,18)});
  });
  return out;}"""

# les familles qui ne sont PAS du produit (system-ui d'un nœud sans police propre) :
# on ne juge pas ce qu'on n'a pas demandé
NOTRE = {'fraunces', 'bricolage', 'apfel', 'apfelmid'}


def main():
    ok = faces_embarquees()
    print('══ FACES EMBARQUÉES (lues dans app.html) ══')
    for f in sorted(ok):
        print('   %-10s %-4d %s' % f)
    print()

    fautes = defaultdict(list)
    bons = defaultdict(int)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.goto(APP)
        pg.wait_for_timeout(6800)
        pg.evaluate("""async()=>{try{await document.fonts.ready;}catch(e){}}""")
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for theme in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", theme)
            pg.wait_for_timeout(400)
            for nom, js in SCENES:
                try:
                    pg.evaluate(js)
                except Exception:
                    continue
                pg.wait_for_timeout(1100)
                for el in pg.evaluate(RELEVE):
                    fam = el['fam'].lower()
                    if fam not in NOTRE:
                        continue
                    cle = (fam, el['w'], el['st'])
                    if cle in ok:
                        bons[cle] += 1
                    else:
                        fautes[cle].append((nom, el['noeud'], el['mot']))
        b.close()

    print('══ COUPLES DEMANDÉS ET EMBARQUÉS ══')
    for cle in sorted(bons, key=lambda k: -bons[k]):
        print('   %-10s %-4d %-8s %d élément(s)' % (cle[0], cle[1], cle[2], bons[cle]))

    total = sum(len(v) for v in fautes.values())
    print('\n══ COUPLES DEMANDÉS MAIS ABSENTS — casseraient en Swift ══')
    if not fautes:
        print('   aucun.')
    for cle in sorted(fautes, key=lambda k: -len(fautes[k])):
        v = fautes[cle]
        ecrans = defaultdict(int)
        for e in v:
            ecrans[e[0]] += 1
        detail = ' · '.join('%s(%d)' % (k, n) for k, n in sorted(ecrans.items(), key=lambda x: -x[1]))
        print('   %-10s %-4d %-8s %3d élément(s)   %s' % (cle[0], cle[1], cle[2], len(v), detail))
        if VERBOSE or TOUT:
            for e in (v if TOUT else v[:3]):
                print('        %-22s « %s »   [%s]' % (e[1], e[2], e[0]))

    print('\n%d couple(s) absent(s) · %d élément(s)' % (len(fautes), total))
    sys.exit(0 if not fautes else 1)


main()
