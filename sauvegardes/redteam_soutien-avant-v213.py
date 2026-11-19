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

⚑ v175 (Tom, C-217 §5) — contrat remis au niveau (original : sauvegardes/redteam_soutien-avant-v175.py) : la rangée en gras, `#82AEF8`, d'une autre couleur que « Ma Parole ! » ;
le texte de Tom, mot pour mot, rien de « ne débloque rien » ; cinq montants 5 · 10 · 25 · 50 · 100 €, deux rangées de trois, sans défilement, aux deux échelles ;
T · sur l'état de Tom, la Toile de l'écran est la Toile de l'écran « Ma Parole ! », jouée par sa boucle : mêmes cotes, mêmes pixels que son pavage, le pavage de Ma Parole ! retrouvé ensuite. Rouge sur v174 (`--fichier=zz-v174b.html`).
"""
import sys, io, re; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:200]), flush=True)
TEXTE = 'Promi est fait à la main, par une seule personne. Si l’app t’est chère, tu peux l’aider à grandir.'   # le texte de Tom, mot pour mot (v175)
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
            st = pg.evaluate("""()=>{ const c=q=>{ const e=document.querySelector(q); if(!e) return null; const s=getComputedStyle(e); return [s.color, s.fontWeight, s.fontFamily.split(',')[0]]; }; return [c('#soutienCard .k'), c('#openPlusTop .k')||c('#openPlusTop')]; }""")
            juge(T + ' A · la rangée : Atkinson gras, #82AEF8, une autre couleur que « Ma Parole ! »', st[0] and st[0][0] == 'rgb(130, 174, 248)' and int(st[0][1]) >= 700 and 'Atkinson' in st[0][2] and st[1] and st[1][0] != st[0][0], st)
            if not a: ctx.close(); continue
            ls0 = pg.evaluate("()=>JSON.stringify(Object.keys(localStorage).sort())")
            pg.evaluate("()=>document.getElementById('soutienCard').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
            B.tap_sel(pg, '#soutienCard'); pg.wait_for_timeout(1100)
            s = pg.evaluate("""()=>{ const S=document.getElementById('soutienScreen'); if(!S||!S.classList.contains('show')) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
               const bt=[...S.querySelectorAll('.so-m')].map(x=>{ const r=x.getBoundingClientRect(); return [x.textContent,(r.left-D.left)/k,(r.right-D.left)/k,r.height/k]; }); const m=S.querySelector('.so-merci'), t=S.querySelector('.scr-t');
               return {bt:bt, tx:S.querySelector('.so-tx').textContent, merci:getComputedStyle(m).visibility, titre:t.textContent, fs:parseFloat(getComputedStyle(t).fontSize), tr:t.getBoundingClientRect().right<=D.right}; }""")
            mt = [x[0].replace(' ', ' ') for x in s['bt']] if s else None
            juge(T + ' B · l\'écran : cinq montants, dans l\'appareil (24 pt de marge), le merci absent', s and mt == ['5 €', '10 €', '25 €', '50 €', '100 €'] and min(x[1] for x in s['bt']) >= 23.5 and max(x[2] for x in s['bt']) <= 366.5 and all(abs(x[3] - 62) < 1 for x in s['bt']) and s['merci'] == 'hidden', s)
            juge(T + ' B · le texte de Tom, mot pour mot, et rien d\'autre', s and s['tx'] == TEXTE and 'débloque' not in s['tx'], s and s['tx'])
            g = pg.evaluate("""()=>{ const S=document.getElementById('soutienScreen'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const b=[...S.querySelectorAll('.so-m')].map(x=>x.getBoundingClientRect()); const m=S.querySelector('.so-merci').getBoundingClientRect(); return {rangs:[...new Set(b.map(r=>Math.round((r.top-D.top)/k)))], col:[b.slice(0,3).length, b[3]?b.filter(r=>Math.abs(r.top-b[3].top)<2).length:0], m:(m.bottom-D.top)/k, dep:S.scrollHeight-S.clientHeight, W:Math.max(...b.map(r=>r.width))/k, ph:!!b[4]&&b[4].bottom<=D.bottom}; }""")
            juge(T + ' B · deux rangées (trois puis deux), rien à défiler, le merci dans l\'écran', len(g['rangs']) == 2 and g['col'] == [3, 2] and g['dep'] <= 0 and g['m'] <= 790 and g['ph'], g)
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
    # T · la Toile de l'écran « Ma Parole ! », sur l'état de Tom
    for sombre_t, nomt in ((False, 'clair'), (True, 'sombre')):
        ctx, et = B.contexte_tom(b, 'etats/tom-20261023-125022.json', sombre=sombre_t)
        pg = B.ouvre(ctx, F)
        pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>document.getElementById('soutienCard').click()"); pg.wait_for_timeout(2400)
        r = pg.evaluate("""()=>{ const c=document.querySelector('#soutienScreen .so-toile'); if(!c||!c.width||getComputedStyle(c).display==='none') return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, R=c.getBoundingClientRect();
          const s=window._vendToileOff&&_vendToileOff(); if(!s) return {pas:1}; const A=c.getContext('2d').getImageData(0,0,c.width,c.height).data, B=s.getContext('2d').getImageData(0,0,s.width,s.height).data; let dif=0, teintes=new Set();
          for(let i=0;i<A.length;i+=4){ if(A[i]!==B[i]||A[i+1]!==B[i+1]||A[i+2]!==B[i+2]) dif++; if(i%4000===0) teintes.add((A[i]>>4)+','+(A[i+1]>>4)+','+(A[i+2]>>4)); }
          return {box:[(R.left-D.left)/k,(R.top-D.top)/k,R.width/k,R.height/k], dim:[c.width,c.height,s.width,s.height], dif:dif, teintes:teintes.size}; }""")
        print('   Toile :', r, flush=True)
        pg.evaluate("()=>document.querySelector('#soutienScreen .closeb').click()"); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} if(window.ouvreCercle) ouvreCercle(); }"); pg.wait_for_timeout(2600)
        mp = pg.evaluate("()=>{ const c=document.querySelector('#plusScreen .pc-toile canvas'); if(!c||!c.width) return null; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=4000) if(d[i]>10) n++; return n; }")
        juge('[%s] T · l\'écran « Ma Parole ! » garde sa Toile après celui-ci' % nomt, mp, mp)
        juge('[%s] T · la Toile : les cotes de l\'écran « Ma Parole ! » (22 · 116 · 346 × 188)' % nomt, r and r.get('box') and abs(r['box'][0] - 22) < 1 and abs(r['box'][1] - 116) < 1 and abs(r['box'][2] - 346) < 1 and abs(r['box'][3] - 188) < 1, r and r.get('box'))
        juge('[%s] T · la même Toile, au pixel, en couleur (≥ 8 teintes)' % nomt, r and r.get('dif') == 0 and r['dim'][:2] == r['dim'][2:] and r['teintes'] >= 8, r)
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
