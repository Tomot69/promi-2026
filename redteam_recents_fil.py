#!/usr/bin/env python3
"""redteam_recents_fil.py — ⚑ v182b (Tom, 6 nov. 2026, C-245 suite) : « Dans l'Index, c'est bon. Dans le Fil, la dernière action ne remonte pas en tête. Même règle
que l'Index. Juge : une action sur une parole ancienne la fait passer en tête du Fil. »

Banc WebKit ×3, au doigt, le vrai chemin : le Fil ouvert par sa porte, une carte touchée (sa fiche s'ouvre), l'action faite dans la fiche, la fiche refermée par
son X — on revient sur le Fil (C-193), qui n'est PAS rouvert. L'état exporté de Tom, puis la Toile du banc :
  A · un MOT (« Un mot… », la saisie, Entrée) sur la parole la plus basse du Fil : revenu sur le Fil, ses bandeaux sont en tête ;
  B · une MODIFICATION (l'échéance, écrite dans la parole et enregistrée) sur une autre : revenu sur le Fil, en tête ;
  C · rien ne bouge quand on ouvre et referme une fiche sans rien faire ;
  D · aucune erreur de page.
Rouge sur v181b (`--fichier=zz-v181b.html`) : A, B.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
ORDRE = "()=>[...document.querySelectorAll('#feedList .s4-carte')].sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top).map(c=>c.getAttribute('data-pid')).filter(Boolean)"
def ordre(pg): return [int(x) for x in pg.evaluate(ORDRE)]
def touche_carte(pg, pid):
    c = pg.evaluate("id=>{ const e=document.querySelector('#feedList .s4-carte[data-pid=\"'+id+'\"]'); if(!e) return null; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return [r.left+r.width*0.7, r.top+r.height/2]; }", pid)
    if c: pg.wait_for_timeout(400); c = pg.evaluate("id=>{ const e=document.querySelector('#feedList .s4-carte[data-pid=\"'+id+'\"]'); const r=e.getBoundingClientRect(); return [r.left+r.width*0.7, r.top+r.height/2]; }", pid); pg.mouse.click(c[0], c[1])   # la souris porte des évènements de pointeur : la pile de C-193 (l'origine lue à `pointerdown`) les lit — un toucher du banc WebKit n'en porte pas
    pg.wait_for_timeout(2600); return pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show') && typeof cur!=='undefined' && cur ? cur.id : null")
def ferme(pg):
    for _ in range(3):   # « Un mot… » encore ouvert : le premier toucher du X le referme
        c = pg.evaluate("()=>{ const e=document.querySelector('#detailPoster .closeb'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }"); pg.mouse.click(c[0], c[1]); pg.wait_for_timeout(1800)
        if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"): break
for nom in ('tom', 'banc'):
    with sync_playwright() as p:
        b = p.webkit.launch()
        if nom == 'tom': ctx, d = B.contexte_tom(b, echelle=1)
        else: ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10)
        pg = B.ouvre(ctx, F, 8000); pg.wait_for_timeout(1500); T = '[%s]' % nom
        B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600); o0 = ordre(pg)
        print('  %s Fil au départ' % T, o0, flush=True)
        if len(set(o0)) < 3: juge(T + ' le Fil porte au moins trois paroles', False, o0); b.close(); continue
        q = o0[-1]; ouv = touche_carte(pg, q); ferme(pg); oC = ordre(pg)
        juge(T + ' C · ouvrir puis refermer une fiche ne change rien', ouv == q and oC == o0, (ouv, oC[:5]))
        ouv = touche_carte(pg, q)
        B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900); pg.keyboard.type('je m\'y mets', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        ferme(pg); pg.wait_for_timeout(1800); oA = ordre(pg); vu = pg.evaluate("()=>document.getElementById('feedView').classList.contains('in')")
        juge(T + ' A · un mot sur la parole la plus basse : revenu sur le Fil, elle est en tête', ouv == q and vu and oA and oA[0] == q, (q, ouv, oA[:5]))
        q2 = next(x for x in reversed(oA) if x != q); ouv = touche_carte(pg, q2)
        pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); p.dueISO='2026-12-24'; p.due=40; saveState(true); }", q2); pg.wait_for_timeout(300)
        ferme(pg); pg.wait_for_timeout(1800); oB = ordre(pg)
        juge(T + ' B · une modification (l\'échéance) : revenu sur le Fil, elle est en tête', ouv == q2 and oB and oB[0] == q2, (q2, ouv, oB[:5]))
        juge(T + ' D · aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
