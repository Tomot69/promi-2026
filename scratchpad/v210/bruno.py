"""v210 (C-305) — l'exemple « Bruno-Stanislas, promets-moi de … » : la page + d'un Promi en « promets-moi », échelles 1 et 0,79, deux thèmes :
le prénom sur UNE ligne (aucune coupure au trait d'union), la phrase dans la marge (24 → 366), au-dessus du rail du pinceau et de « garder de côté », aucun
chevauchement entre ses lignes ; rien de coupé (« … »). python3 scratchpad/v210/bruno.py [--fichier=]"""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ok = tot = 0
def juge(c, m, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + m + ('   ' + d if d else ''))
M = r"""()=>{ const dev=document.getElementById('device').getBoundingClientRect(), k=dev.width/390, P=document.getElementById('csPhrase');
 const q=P.querySelector('[data-ph=qui]'); const rg=document.createRange(); rg.selectNodeContents(q); const R=[...rg.getClientRects()].filter(r=>r.width>1);
 const tops=R.map(r=>r.top+r.height/2).sort((a,b)=>a-b); let lignes=tops.length?1:0; for(let i=1;i<tops.length;i++) if(tops[i]-tops[i-1]>6*k) lignes++;
 const t=P.innerText; const pr=P.getBoundingClientRect();
 const txt=[]; const w=document.createTreeWalker(P,NodeFilter.SHOW_TEXT); let n; while(n=w.nextNode()){ if(!n.data.trim()) continue; const r2=document.createRange(); r2.selectNodeContents(n); for(const r of r2.getClientRects()) if(r.width>1) txt.push([(r.left-dev.left)/k,(r.top-dev.top)/k,(r.right-dev.left)/k,(r.bottom-dev.top)/k]); }
 let bas=Math.max(...txt.map(r=>r[3])), g=Math.min(...txt.map(r=>r[0])), d=Math.max(...txt.map(r=>r[2]));
 const rail=document.querySelector('#createSheet .pc-rail, #createSheet #csPinceau, #createSheet .pinceau-rail'); const gd=document.querySelector('#createSheet .cs-garder, #createSheet #addDraft, #createSheet [data-garder]');
 const RR=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return r.width? (r.top-dev.top)/k : null; };
 return {texte:t, quiTexte:q.innerText, lignesQui:lignes, bas:bas, gauche:g, droite:d, rail:RR(rail), garder:RR(gd), coupe:/…/.test(t)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ((390, 844), (330, 714)):
        for sombre in (False, True):
            ctx = B.contexte(b, sombre=sombre, vw=vw, vh=vh); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, attente=7000)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(3500)
            for i in range(2): B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(2600)
            r = pg.evaluate(M); nom = '%dx%d %s' % (vw, vh, 'sombre' if sombre else 'clair')
            juge('Bruno' in r['quiTexte'] and r['lignesQui'] == 1, '%s : « %s » sur une ligne' % (nom, r['quiTexte'].replace('\n', ' ')), '%d ligne(s)' % r['lignesQui'])
            juge(r['gauche'] >= 23.5 and r['droite'] <= 366.5 and not r['coupe'], '%s : la phrase dans la marge, rien de coupé' % nom, '%.1f → %.1f' % (r['gauche'], r['droite']))
            lim = min([v for v in (r['rail'], r['garder']) if v] or [999])
            juge(r['bas'] <= lim - 6, '%s : la phrase au-dessus du rail et de « garder de côté »' % nom, 'bas %.1f, dessous %.1f' % (r['bas'], lim))
            if vw == 390 and not sombre: B.capture(pg, 'scratchpad/v210/bruno-390.png')
            if vw == 330 and not sombre: B.capture(pg, 'scratchpad/v210/bruno-330.png')
            ctx.close()
    b.close()
print('\n  %s  %d / %d' % ('✅' if ok == tot else '❌', ok, tot))
