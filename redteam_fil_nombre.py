#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_fil_nombre.py — LE « 1 » PARASITE DU FIL (v183c, Tom, 7 nov. 2026 — C-251).
« Dans le Fil, deux cartes portent un « 1 » après « Tu as commenté » ou « Tu as planté ». Trouve la cause et supprime-le. Juge : aucun texte de carte ne se
termine par un nombre isolé. »
Banc WebKit 390 × 844 : l'état des paroles avec des mots (banc-etats/etat-comm.json) — un mot envoyé par la vraie saisie d'une fiche, puis le Fil et l'Index
ouverts par la barre ; puis l'état exporté de Tom, un mot envoyé de même. Chaque ligne de texte de chaque carte (Fil, Index) : aucune ne finit par un nombre
isolé (« … 1 », « …1 » après une lettre). Rouge sur v183b (`--fichier=`).
"""
import sys, re; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %s  %s' % ('OK' if ok else 'KO', nom, str(d)[:240]), flush=True)
LIS = r"""(sel)=>{ const out=[]; document.querySelectorAll(sel).forEach(c=>{ const W=document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let n; const L=[];
   while((n=W.nextNode())){ const t=(n.textContent||'').replace(/\s+/g,' ').trim(); if(t) L.push(t); } out.push(L.join(' ⏐ ')); }); return out; }"""
FIN = re.compile(r'(^|[^\d\s.,:/h])\s*\d+$|\s\d+$')
def mot(pg, titre):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(900)
    pg.evaluate("t=>openDetail(promises.find(x=>x.title===t).id)", titre); pg.wait_for_timeout(2600)
    B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(700); pg.keyboard.type('Je viens aussi'); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ try{ window._comm.ferme() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(1200)
def cartes(pg, tag):
    for nom, btn, sel in (('Fil', '#filBtn', '#feedList .s4-carte, #feedList .s4-bandeau, #feedList .s4-grille > div'), ('Index', '#indexBtn', '#indexList .s4-carte')):
        pg.evaluate("()=>{ try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(600); B.tap_sel(pg, btn); pg.wait_for_timeout(2500)
        T = pg.evaluate(LIS, sel)
        mal = [t for t in T for l in t.split(' ⏐ ') if FIN.search(l) and not re.search(r'\d+ (paroles?|mots?|Promi|tenus?)$', l) and not re.search(r'\+\d+$', l)]   # « avec +2 » : le compte des membres d'un Cercle, un vrai texte
        juge('[%s · %s] %d cartes : aucun texte ne finit par un nombre isolé' % (tag, nom, len(T)), T and not mal, mal[:3])
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 'comm'); pg = B.ouvre(ctx, F)
    mot(pg, 'faire les crêpes'); cartes(pg, 'banc')
    ctx.close()
    ctx, d = B.contexte_tom(b)
    if ctx:
        pg = B.ouvre(ctx, F); t = pg.evaluate("()=>promises.filter(p=>!p.draft)[0].title"); mot(pg, t); cartes(pg, 'Tom')
        ctx.close()
    b.close()
print('\n%d / %d' % (sum(res), len(res)))
