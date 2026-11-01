#!/usr/bin/env python3
"""redteam_peauf_x.py — v176 (C-220) : APRÈS LE X DE PEAUFINER, AUCUN TEXTE DU TIROIR À L'ÉCRAN, sur la page +.

Trouvé en vérifiant v175a dans Safari iOS : la page + ouverte, Peaufiner ouvert puis fermé par son X, le texte brut du tiroir (AVANT, NOTE, PIÈCES JOINTES, les pastilles) restait affiché,
sans style. LA CAUSE : la règle « fermée : rien » portait `.pp-peauf`, la règle suivante la battait toujours ; une fois bâti, `.dpd-corps` restait donc dans le flux, à z-index de page.
Trois natures × deux thèmes × échelles 1 et 0,79, au doigt (banc comme Tom, WebKit) :
  A · ouvert par la barre : le tiroir est là, ses rangées lisibles.
  B · fermé par son X : aucun texte de `.dpd-corps` n'est rendu (boîte nulle ou cachée) ; le texte de la page est celui d'avant, à ses cotes (± 1 pt).
  C · rouvert : les rangées reviennent (les contrôles empruntés sont rendus, rien ne se perd).
Rouge sur v175b (`--fichier=zz-v175b.html`).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
TIROIR = """()=>{ const c=document.querySelector('#createSheet > .dpd-corps'); if(!c) return []; const o=[], w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT); let n;
  while(n=w.nextNode()){ const t=n.textContent.trim(); if(!t) continue; const s=getComputedStyle(n.parentElement); if(s.visibility!=='visible') continue; const R=document.createRange(); R.selectNodeContents(n); const r=R.getBoundingClientRect(); if(r.width>=1&&r.height>=1) o.push(t.slice(0,24)); } return o; }"""
PAGE = """()=>{ const c=document.getElementById('createSheet'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, o={}, w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT); let n;
  while(n=w.nextNode()){ const t=n.textContent.trim(); if(!t||n.parentElement.closest('.dpd-corps')) continue; const s=getComputedStyle(n.parentElement); if(s.visibility!=='visible') continue; const R=document.createRange(); R.selectNodeContents(n); const r=R.getBoundingClientRect(); if(r.width>=1&&r.height>=1&&r.top<D.bottom&&r.bottom>D.top) o[t.slice(0,24)+'@'+Math.round((r.left-D.left)/k)]=+((r.top-D.top)/k).toFixed(1); } return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_peauf_x — %s, charge %.1f' % (F, B.charge()))
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            for nat in ('promi', 'chiche', 'nuee'):
                T = '[%s · %s · %s]' % (nat, 'sombre' if sombre else 'clair', nom)
                ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
                B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(3000)
                av = pg.evaluate(PAGE); B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1500); t1 = pg.evaluate(TIROIR)
                juge(T + ' A · Peaufiner ouvert : ses rangées sont là', len(t1) >= 6, len(t1))
                x = pg.evaluate("()=>{ const e=document.querySelector('#createSheet .s2-fermer'), r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
                pg.touchscreen.tap(x[0], x[1]); pg.wait_for_timeout(1500)
                fe = pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('pp-peauf')"); t2 = pg.evaluate(TIROIR); ap = pg.evaluate(PAGE)
                juge(T + ' B · fermé par son X : aucun texte du tiroir à l\'écran', fe and not t2, '%s · %s' % (fe, t2[:5]))
                ec = [k for k in av if k not in ap or abs(av[k] - ap[k]) > 1]
                juge(T + ' B · la page est celle d\'avant, texte et cotes (± 1 pt)', not ec, ec[:5])
                B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1500); t3 = pg.evaluate(TIROIR)
                juge(T + ' C · rouvert : les rangées reviennent', len(t3) >= 6, len(t3))
                if pg.__dict__['erreurs']: juge(T + ' aucune erreur de page', False, pg.__dict__['erreurs'][:2])
                ctx.close()
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
sys.exit(0 if all(res) else 1)
