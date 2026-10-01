#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_titres_longs.py — UN TITRE LONG NE SORT JAMAIS DE L'ÉCRAN (Tom, 24 sept. 2026, v46), AU DOIGT.
« La phrase garde sa taille ; seule la partie à partir du de / d’ — le mot et la pastille noire — rapetisse et s'étale sur
deux lignes, trois au maximum, puis points de suite. Même marge à droite que le reste. » Et la fiche : deux lignes, trois au
plus, puis points de suite, jamais sous sa ligne d'état. Et l'élision « de » / « d’ » suit la frappe, à chaque caractère.
Valeurs en dur (§7) : marge 24 (bord droit ≤ 366 sur 390) · 3 lignes au plus.
  1 · page + (Promi, Chiche) : rien de la phrase au-delà de 366 ; la pastille ≤ 3 lignes ; « Je me promets » / « Chiche » gardent
      la taille qu'ils ont avec un titre court
  2 · fiche : titre ≤ 3 lignes, et son bas au-dessus de la ligne d'état
  3 · l'élision suit chaque touche : « a » → d’, puis effacé + « b » → de
"""
import sys
from playwright.sync_api import sync_playwright
LONGS = ["réparer enfin le vieux vélo bleu de grand-père avant les vacances d'été prochaines puis le repeindre en vert pomme",
         "anticonstitutionnellementetsurtoutsansespaceanticonstitutionnellement"]
ok = [0]; ko = []
def t(n, c, d=''):
    if c: ok[0] += 1; print('%-64s OK  %s' % (n, d))
    else: ko.append(n); print('%-64s KO  %s' % (n, d))
MES = r"""()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, txt=document.querySelector('#csPhrase .ph-txt');
  let droite=0; txt.querySelectorAll('.ph-m,.ph-b,.ph-li').forEach(x=>{ [...x.getClientRects()].forEach(q=>{ droite=Math.max(droite,(q.right-d.left)/k); }); });
  const pt=txt.querySelector('.ph-m[data-ph=titre]'); const rg=document.createRange(); rg.selectNodeContents(pt); const L=[];
  [...rg.getClientRects()].forEach(r=>{ if(r.width<1) return; const c=(r.top+r.bottom)/2; if(!L.some(b=>c>b[0]&&c<b[1])) L.push([r.top,r.bottom]); });
  const verbe=txt.querySelector('.ph-m[data-ph=sens], .ph-b'); return {droite:Math.round(droite), lignes:L.length, fsVerbe:verbe?parseFloat(getComputedStyle(verbe).fontSize):0, fsTxt:parseFloat(getComputedStyle(txt).fontSize)}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['light', 'dark']:
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
        pg.goto(__import__('os').environ.get('APP_TITRES','http://127.0.0.1:8752/app.html')); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);}", th); pg.wait_for_timeout(800)
        for nat in ['promi', 'chiche']:
            pg.evaluate("()=>{closeAll(); window._phrase&&(window._phrase.titre=''); document.getElementById('createBtn').click();}"); pg.wait_for_timeout(1100)
            pg.locator('[data-kind=%s]' % nat).first.tap(); pg.wait_for_timeout(1300)
            pg.locator('#csPhrase [data-ph=titre]').first.tap(); pg.wait_for_timeout(500)
            pg.keyboard.type('nager', delay=5); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
            court = pg.evaluate(MES)
            for L in LONGS:
                pg.locator('#csPhrase [data-ph=titre]').first.tap(); pg.wait_for_timeout(400)
                pg.keyboard.press('Meta+a'); pg.keyboard.press('Control+a'); pg.keyboard.press('Backspace')
                pg.keyboard.type(L, delay=2); pg.keyboard.press('Enter'); pg.wait_for_timeout(1000)
                m = pg.evaluate(MES)
                t('[%s] 1 · %s « %s… » : dans l\'écran, ≤ 3 lignes, verbe intact' % (T, nat, L[:14]),
                  m['droite'] <= 366 and m['lignes'] <= 3 and abs(m['fsVerbe'] - court['fsVerbe']) < 0.5,
                  'bord %d · %d lignes · verbe %.0f (court %.0f)' % (m['droite'], m['lignes'], m['fsVerbe'], court['fsVerbe']))
        # 2 · la fiche
        for L in LONGS:
            pg.evaluate("(t)=>{ closeAll(); const p=promises.filter(q=>!q.draft&&!q.nuee)[0]; p.title=t; openDetail(p.id); }", L); pg.wait_for_timeout(1600)
            f = pg.evaluate("""()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, ti=document.getElementById('dptTitre'), qd=document.getElementById('dptQuand');
              const lh=parseFloat(getComputedStyle(ti).lineHeight), r=ti.getBoundingClientRect(); return {lignes:Math.round(r.height/k/lh), bas:Math.round((r.bottom-d.top)/k), etat:qd?Math.round((qd.getBoundingClientRect().top-d.top)/k):9999, droite:Math.round((r.right-d.left)/k)}; }""")
            t('[%s] 2 · fiche « %s… » : ≤ 3 lignes, au-dessus de son état' % (T, L[:14]), f['lignes'] <= 3 and f['bas'] <= f['etat'] and f['droite'] <= 366, str(f))
        # 3 · l'élision
        pg.evaluate("()=>{closeAll(); window._phrase&&(window._phrase.titre=''); document.getElementById('createBtn').click();}"); pg.wait_for_timeout(1100)
        pg.locator('[data-kind=promi]').first.tap(); pg.wait_for_timeout(1300)
        pg.locator('#csPhrase [data-ph=titre]').first.tap(); pg.wait_for_timeout(500)
        pg.keyboard.press('Meta+a'); pg.keyboard.press('Control+a'); pg.keyboard.press('Backspace'); pg.wait_for_timeout(150)
        pg.keyboard.type('a'); pg.wait_for_timeout(120); e1 = pg.evaluate("()=>document.querySelector('#csPhrase .ph-li').textContent")
        pg.keyboard.press('Backspace'); pg.keyboard.type('b'); pg.wait_for_timeout(120); e2 = pg.evaluate("()=>document.querySelector('#csPhrase .ph-li').textContent")
        t('[%s] 3 · l\'élision suit la frappe' % T, e1 == 'd’' and e2 == 'de', '« a » → %s · « b » → %s' % (e1, e2))
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko))); sys.exit(1 if ko else 0)
