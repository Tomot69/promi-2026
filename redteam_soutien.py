#!/usr/bin/env python3
"""redteam_soutien.py — ⚑ v174 (Tom, 31 oct. 2026, C-217) : « SOUTENIR PROMI ».

« Une rangée dans les Réglages, après “Ma Parole !”. Elle ouvre un écran simple, un texte provisoire, trois montants, un merci après le geste. Aucun paiement réel. La rangée
n'est proposée NULLE PART ailleurs, ne revient jamais d'elle-même, sans compteur ni relance. »

Banc comme Tom (WebKit, doigt), deux thèmes, échelles 1 et 0,79 :
  A · la rangée est aux Réglages, sous « Ma Parole ! », joignable au doigt, sans recouvrement
  B · l'écran : trois montants 2 · 5 · 10 €, rien ne déborde ; le merci absent, puis présent après un toucher
  C · aucun paiement, rien d'écrit au stockage ; rouvert, le merci n'y est plus
  D · X rend les Réglages
  E · absente partout ailleurs : le mot n'est sur aucun autre écran (dix écrans, plus 30 s d'accueil) ; source : un seul nœud, un seul ouvreur
Rouge sur v173 (`--fichier=zz-v173.html`).
"""
import sys, io, re; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:200]), flush=True)
VU = """(id)=>{ const e=document.getElementById(id); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {x:(r.left-D.left)/k,y:(r.top-D.top)/k,w:r.width/k,h:r.height/k,dessus:(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)||{}).id||''}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    print('fichier :', F, '· charge %.1f' % B.charge())
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            T = '[%s · %s]' % ('sombre' if sombre else 'clair', nom)
            ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#settingsBtn') if pg.evaluate("()=>!!document.getElementById('settingsBtn')&&document.getElementById('settingsBtn').getBoundingClientRect().width>0") else pg.evaluate("()=>document.getElementById('settingsBtn').click()")
            pg.wait_for_timeout(1400)
            a = pg.evaluate(VU, 'soutienCard'); m = pg.evaluate(VU, 'openPlusTop')
            ordre = pg.evaluate("()=>{ const s=document.getElementById('soutienCard'), m=document.getElementById('openPlusTop'), r=document.getElementById('replayOnb'); return s&&m&&r? [s.getBoundingClientRect().top>=m.getBoundingClientRect().bottom-1, s.getBoundingClientRect().bottom<=r.getBoundingClientRect().top+1] : null; }")
            juge(T + ' A · la rangée, sous « Ma Parole ! », avant la suite, joignable', a and ordre and all(ordre), (a, ordre))
            if not a: ctx.close(); continue
            ls0 = pg.evaluate("()=>JSON.stringify(Object.keys(localStorage).sort())")
            pg.evaluate("()=>document.getElementById('soutienCard').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
            B.tap_sel(pg, '#soutienCard'); pg.wait_for_timeout(1100)
            s = pg.evaluate("""()=>{ const S=document.getElementById('soutienScreen'); if(!S||!S.classList.contains('show')) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
               const bt=[...S.querySelectorAll('.so-m')].map(x=>{ const r=x.getBoundingClientRect(); return [x.textContent,(r.left-D.left)/k,(r.right-D.left)/k,r.height/k]; }); const m=S.querySelector('.so-merci'), t=S.querySelector('.scr-t');
               return {bt:bt, tx:S.querySelector('.so-tx').textContent, merci:getComputedStyle(m).visibility, titre:t.textContent, fs:parseFloat(getComputedStyle(t).fontSize), tr:t.getBoundingClientRect().right<=D.right}; }""")
            mt = [x[0].replace(' ', ' ') for x in s['bt']] if s else None
            juge(T + ' B · l\'écran : trois montants, dans l\'appareil (24 pt de marge), le merci absent', s and mt == ['2 €', '5 €', '10 €'] and min(x[1] for x in s['bt']) >= 23.5 and max(x[2] for x in s['bt']) <= 366.5 and all(abs(x[3] - 62) < 1 for x in s['bt']) and s['merci'] == 'hidden', s)
            juge(T + ' B · le texte dit que le don ne débloque rien', s and 'ne débloque rien' in s['tx'], s and s['tx'])
            B.tap_sel(pg, '#soutienScreen .so-m:nth-child(2)'); pg.wait_for_timeout(1000)
            mc = pg.evaluate("()=>{ const m=document.querySelector('#soutienScreen .so-merci'); return getComputedStyle(m).visibility; }")
            juge(T + ' B · le geste : le merci paraît', mc == 'visible', mc)
            ls1 = pg.evaluate("()=>JSON.stringify(Object.keys(localStorage).sort())")
            juge(T + ' C · aucun paiement, rien d\'écrit au stockage', ls0 == ls1, '' if ls0 == ls1 else (ls0, ls1))
            B.tap_sel(pg, '#soutienScreen .closeb'); pg.wait_for_timeout(1000)
            juge(T + ' D · X rend les Réglages', pg.evaluate("()=>document.getElementById('settingsScreen').classList.contains('show') && !document.getElementById('soutienScreen').classList.contains('show')"))
            B.tap_sel(pg, '#soutienCard'); pg.wait_for_timeout(900)
            juge(T + ' C · rouvert, le merci n\'y est plus (rien ne se garde)', pg.evaluate("()=>getComputedStyle(document.querySelector('#soutienScreen .so-merci')).visibility") == 'hidden')
            pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(700)
            ctx.close()
    # E · absente ailleurs
    ctx = B.contexte(b, False, vw=430, vh=932); pg = B.ouvre(ctx, F); ailleurs = []
    def vu(nom):
        t = pg.evaluate("()=>{ const D=document.getElementById('device'); const r=[]; const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); while(w.nextNode()){ const n=w.currentNode; if(!/soutenir promi|soutien/i.test(n.nodeValue||'')) continue; const e=n.parentElement; if(!e||e.closest('script,style')) continue; const c=getComputedStyle(e), q=e.getBoundingClientRect(); if(c.visibility==='visible'&&c.display!=='none'&&q.width>0&&q.height>0) r.push([e.id||e.className,Math.round(q.left),Math.round(q.top)]); } return r; }")
        d = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(); return [D.left,D.top,D.right,D.bottom]; }")
        t = [x for x in t if d[0] <= x[1] < d[2] and d[1] <= x[2] < d[3]]
        if t: ailleurs.append((nom, t))
    vu('accueil'); pg.wait_for_timeout(1500)
    for nom, js in (('Index', "document.getElementById('indexBtn')&&document.getElementById('indexBtn').click()"), ('Fil', "document.getElementById('filBtn')&&document.getElementById('filBtn').click()"), ('Aura', "document.getElementById('auraBtn')&&document.getElementById('auraBtn').click()"), ('Studio', "document.getElementById('studioBtn')&&document.getElementById('studioBtn').click()"), ('Partager', "document.getElementById('shareBtn')&&document.getElementById('shareBtn').click()")):
        pg.evaluate("()=>{ %s }" % js); pg.wait_for_timeout(1500); vu(nom); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2400); vu('page +'); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ if(promises[0]) openDetail(promises[0].id); }"); pg.wait_for_timeout(2200); vu('fiche'); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ if(window.ouvreCercle) ouvreCercle(); document.getElementById('plusScreen').classList.add('show'); }"); pg.wait_for_timeout(1500); vu('Ma Parole !')
    juge('E · absente de l\'accueil, l\'Index, le Fil, l\'Aura, le Studio, Partager, la page +, une fiche, l\'offre', not ailleurs, ailleurs)
    ctx.close(); b.close()
S = io.open(F, encoding='utf-8').read()
n = len(re.findall(r'_soutienPage\(', S)); q = len(re.findall(r'id="soutienCard"', S))
juge('E · source : une seule rangée, un seul appel de l\'écran ; aucune clé de stockage', q == 1 and n == 1 and not re.search(r"promi_soutien|soutien_", S), (q, n))
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
