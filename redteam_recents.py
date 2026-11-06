#!/usr/bin/env python3
"""redteam_recents.py — ⚑ v181b (Tom, 6 nov. 2026, C-245) : « Dans l'Index et dans le Fil, la parole ou la fiche qui a eu la dernière action (création,
trait, commentaire, modification, membre ajouté) remonte en tête de liste, et ainsi de suite. C'est l'ordre par défaut (« Récents »). Les autres tris ne
changent pas. Juge : une action sur une parole ancienne la fait passer en tête, dans l'Index et dans le Fil. »

Banc WebKit ×3, la Toile « cercle » (six paroles dans « Le potager », d'autres seules), 430 × 932. L'Index s'ouvre par `openSheet`, le Fil par `#filBtn`.
  A · un MOT (au doigt : « Un mot… », la saisie, Entrée) sur la parole la plus ancienne de l'Index → elle passe en tête de l'Index ; dans le Fil, ses
      bandeaux passent en tête ;
  B · un TRAIT (la parole tenue par son sélecteur d'état, comme le fait le trait) sur une autre parole ancienne → en tête ;
  C · une MODIFICATION (son échéance, par Peaufiner) → en tête ;
  D · un MEMBRE AJOUTÉ à un Cercle → le Cercle en tête de l'Index ;
  E · une PLANTATION → la parole neuve en tête ;
  F · ouvrir puis fermer une fiche, ou recharger l'app, ne change rien à l'ordre ;
  G · les autres tris (Par personne, Par Cercle ; Index et Fil) donnent le même ordre que v180b servie à côté, sur le même état ;
  H · aucune erreur de page.
Rouge sur v180b (`--fichier=zz-v180b.html`) : A à E.
"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
IX = """(tri)=>{ closeAll(); window.ixFiltre='tous'; window.ixTri=tri||'recent'; openSheet(document.getElementById('indexSheet')); buildIndex();
  return (window._s4Entrees||[]).map(e=>e.nuee?('n:'+e.nuee):('p:'+e.id)); }"""
FIL = """(tri)=>{ closeAll(); window.fdFiltre='tous'; try{ fdSortMode=tri||'recent'; }catch(e){} setView('fil'); buildFeed(); if(window._s4Fil) _s4Fil();
  return (window._filComp||[]).map(c=>c.pid!=null?('p:'+c.pid):(c.nk?('n:'+c.nk):'?')); }"""
FERME = "()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); try{ setView('toile'); }catch(e){} }"
def ix(pg, tri=None):
    o = pg.evaluate(IX, tri); pg.wait_for_timeout(500); pg.evaluate(FERME); pg.wait_for_timeout(400); return o
def fil(pg, tri=None):
    o = pg.evaluate(FIL, tri); pg.wait_for_timeout(500); pg.evaluate(FERME); pg.wait_for_timeout(500); return o
def ancienne(o, exclure=()):
    """la parole seule (hors Cercle, hors gardé de côté) la plus basse de l'Index"""
    for c in reversed(o):
        if c.startswith('p:') and c not in exclure: return int(c[2:])
def ouvre_fiche(pg, pid):
    pg.evaluate("id=>{ closeAll(); openDetail(id); }", pid); pg.wait_for_timeout(2400)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)
    pg.wait_for_timeout(1500)
    o0 = ix(pg); f0 = fil(pg); print('  Index au départ', o0, '\n  Fil au départ', f0, flush=True)
    # F · ouvrir, fermer
    q = ancienne(o0); ouvre_fiche(pg, q); pg.evaluate(FERME); pg.wait_for_timeout(600); pg.evaluate("()=>saveState(true)")
    o1 = ix(pg); juge('F · ouvrir puis fermer une fiche ne change rien à l\'ordre', o1 == o0, o1)
    # A · un mot au doigt
    pg.wait_for_timeout(50); ouvre_fiche(pg, q); B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900)
    pg.keyboard.type('Je m\'y mets demain', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    n = pg.evaluate("id=>((promises.find(x=>x.id===id)||{}).comments||[]).length", q)
    pg.evaluate(FERME); pg.wait_for_timeout(600)
    oA = ix(pg); fA = fil(pg)
    juge('A · un mot sur la parole la plus ancienne : en tête de l\'Index', n > 0 and oA and oA[0] == 'p:%d' % q, (q, n, oA[:4]))
    tete = [c for c in fA if c == 'p:%d' % q]
    juge('A · … et ses bandeaux en tête du Fil (s\'il en a)', (not tete) or fA[:len(tete)] == tete, (len(tete), fA[:4]))
    # B · un trait (le sélecteur d'état, le seul chemin du trait)
    q2 = ancienne(oA, exclure=('p:%d' % q,)); pg.wait_for_timeout(50)
    pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); p.status='tenu'; saveState(true); }", q2)
    oB = ix(pg); juge('B · un trait sur une autre parole ancienne : en tête de l\'Index', oB and oB[0] == 'p:%d' % q2, (q2, oB[:4]))
    # C · une modification (l'échéance)
    q3 = ancienne(oB, exclure=('p:%d' % q, 'p:%d' % q2)); pg.wait_for_timeout(50)
    pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); p.dueISO='2026-12-24'; p.due=40; saveState(true); }", q3)
    oC = ix(pg); juge('C · une modification (l\'échéance) : en tête de l\'Index', oC and oC[0] == 'p:%d' % q3, (q3, oC[:4]))
    # D · un membre ajouté à un Cercle
    k = next((c[2:] for c in oC if c.startswith('n:')), None); pg.wait_for_timeout(50)
    if k:
        pg.evaluate("k=>{ (NUEEMEM[k]=NUEEMEM[k]||[]).push('Lou'); saveState(true); }", k)
        oD = ix(pg); juge('D · un membre ajouté : le Cercle en tête de l\'Index', oD and oD[0] == 'n:%s' % k, (k, oD[:4]))
    else: juge('D · un membre ajouté (aucun Cercle sur cette Toile)', False, oC)
    # E · une plantation
    B.plante(pg, 'ranger le grenier'); pg.wait_for_timeout(1200)
    nid = pg.evaluate("()=>{ const l=promises.filter(p=>p.title==='ranger le grenier'); return l.length?l[l.length-1].id:null; }")
    oE = ix(pg); juge('E · une plantation : la parole neuve en tête de l\'Index', nid and oE and oE[0] == 'p:%d' % nid, (nid, oE[:4]))
    # F bis · recharger
    pg.evaluate("()=>saveState(true)"); pg.wait_for_timeout(300); pg.reload(); pg.wait_for_timeout(8000)
    oR = ix(pg); juge('F · recharger l\'app ne change rien à l\'ordre', oR == oE, (oR[:5], oE[:5]))
    juge('H · aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
    ctx.close()
    # G · les autres tris, contre v180b, sur le même état de départ
    if F == 'app.html':
        ordres = {}
        for f in ('app.html', 'zz-v180b.html'):
            c2 = B.contexte(b, vw=430, vh=932); B.toile_pleine(c2, 'cercle'); g = B.ouvre(c2, f, 7000); g.wait_for_timeout(1500)
            ordres[f] = {t: ix(g, t) for t in ('personne', 'nuee')}; ordres[f].update({'fil-' + t: fil(g, t) for t in ('personne', 'nuee')}); c2.close()
        for t in ordres['app.html']:
            juge('G · « %s » : le même ordre que v180b' % t, ordres['app.html'][t] == ordres['zz-v180b.html'][t], (ordres['app.html'][t][:5], ordres['zz-v180b.html'][t][:5]))
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
