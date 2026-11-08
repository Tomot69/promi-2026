#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_mots_neufs.py — v184b (Tom, 7 nov. 2026) : C-253 (une pastille, pas du texte) et C-254 (le + des membres d'un Promi et d'un Chiche).

C-253 « Un nouveau commentaire est signalé par du texte écrit dans le Fil et dans la fiche. Remplace ce texte par la pastille qui existe déjà : même composant, même
taille, même couleur. Fil et Index : sur la ligne ou la carte de la parole qui a du nouveau. Fiche : sur chaque commentaire nouveau ; repliés sous « + X
commentaires », sur cette ligne. Elle disparaît une fois le commentaire vu. »
C-254 « Le + identique à celui du Cercle ; un membre ajouté a accès à tout l'historique ; la nature ne change pas. Juge : on ajoute un membre à un Promi qui a déjà
5 commentaires, et il voit les 5. »

Banc WebKit (390 × 844 et 330 × 714), l'état banc-etats/etat-cercle.json (une parole passée « reçue de Nico ») ; cinq mots d'autres personnes arrivent sur une parole (`_comm.arrive`, le chemin d'un mot reçu).
  A · la fiche : trois rangées avec la pastille, « + 2 commentaires » avec la pastille ; aucun « N mots » ; la pastille = `.s4-att` du Fil (taille, couleur, filet)
  B · l'Index et le Fil : la carte de la parole porte la pastille
  C · X puis réouverture : les trois vus n'ont plus de pastille ; « + 2 » la garde ; déplié puis fermé : plus aucune ; l'Index ne la porte plus
  D · le Cercle : sa ligne d'état ne compte plus les mots
  E · le + d'un Promi : 26 pt après la phrase, haut d'une capitale, orange, zone de 44 ; au doigt il ouvre Peaufiner sur À QUI, déplié
  F · un membre ajouté au doigt (la saisie, Retour) : la parole le porte, sa nature ne change pas, il voit les 5 mots (`_historique`), la fiche les montre
  G · un Chiche à moi a son + ; une parole reçue n'en a pas
Rouge sur v184a (`--fichier=zz-v184a.html`).
"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
ATT = "(sel)=>[...document.querySelectorAll(sel)].map(e=>{ const c=getComputedStyle(e); return [Math.round(e.getBoundingClientRect().width*10)/10, c.backgroundColor, c.boxShadow]; })"
FICHE = """()=>{ const L=document.getElementById('cm5Liste'); if(!L) return null; const r=[...L.querySelectorAll('.cm5-vus .cm5-un')].map(x=>!!x.querySelector('.s4-att'));
  const pl=L.querySelector('.cm5-plus'); const nb=document.querySelector('#cm5Ligne .cm5-nb');
  return {rangees:r, plus:pl?{txt:pl.textContent.trim(), att:!!pl.querySelector('.s4-att'), h:pl.getBoundingClientRect().height}:null, reste:[...L.querySelectorAll('.cm5-reste .cm5-un')].map(x=>!!x.querySelector('.s4-att')),
    nb:nb?[getComputedStyle(nb).display, nb.textContent]:null, ligneTx:(document.getElementById('cm5Ligne')||{}).textContent||''}; }"""
def fiche(pg):
    """la liste des mots, attendue jusqu'à 6 s (sous charge la pose de la fiche passe au-delà de 2,6 s)"""
    for _ in range(30):
        f = pg.evaluate(FICHE)
        if f: return f
        pg.wait_for_timeout(200)
    return None
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in ((390, 844, '0,93'), (330, 714, '0,79')):
        T = '[×%s]' % nom
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 8000)
        pid = pg.evaluate("""()=>{ const aFil=new Set((window.FEED||[]).map(f=>f.pid)); const p=promises.filter(q=>!q.draft && !q.chiche && !q.nuee && (!q.who||/^moi$/i.test(q.who)) && (!q.from||/^moi$/i.test(q.from)) && !q.pending && aFil.has(q.id))[0]; const rc=promises.find(q=>!q.draft && !q.nuee && q!==p && !q.chiche && q.who && !/^moi$/i.test(q.who)); if(rc){ rc.from='Nico'; rc.who='moi'; } p.comments=[]; saveState(true);
          ['Rachel','Marion','Nico','Rachel','Léa'].forEach((n,i)=>window._comm.arrive(p,{t:'mot '+(i+1)+' de '+n, by:n, d:new Date(Date.now()-(5-i)*60000).toISOString()}));
          return p.id; }""")
        pg.wait_for_timeout(600)
        # B · Index et Fil
        pg.evaluate("()=>{ closeAll(); setView('toile'); }"); B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2400)
        ix = pg.evaluate("id=>{ const c=document.querySelector('#indexList .s4-carte[data-pid=\"'+id+'\"]'); return c ? !!c.querySelector(':scope > .s4-att') : null; }", pid)
        juge(T + ' B · l\'Index : la carte de la parole porte la pastille', ix is True, ix)
        ref = pg.evaluate(ATT, '#indexList .s4-carte > .s4-att')
        pg.evaluate("()=>{ closeAll(); try{ setView('toile'); }catch(e){} }"); pg.wait_for_timeout(900); B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
        fl = pg.evaluate("id=>{ const L=[...document.querySelectorAll('#feedView .s4-carte[data-pid=\"'+id+'\"]')]; return L.map(c=>!!c.querySelector(':scope > .s4-att')); }", pid)
        juge(T + ' B · le Fil : la ligne la plus récente de la parole porte la pastille', bool(fl) and fl[0], fl)
        pg.evaluate("()=>{ closeAll(); setView('toile'); }"); pg.wait_for_timeout(500)
        # A · la fiche
        pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
        f = fiche(pg); a = pg.evaluate(ATT, '#cm5Liste .s4-att')
        juge(T + ' A · trois rangées à pastille, « + 2 commentaires » à pastille', f and f['rangees'] == [True, True, True] and f['plus'] and f['plus']['att'] and f['plus']['txt'].startswith('+ 2'), f)
        juge(T + ' A · aucun « N mots » écrit sur la fiche', f and (not f['nb'] or f['nb'][0] == 'none') and ' mots' not in f['ligneTx'] and ' mot' not in f['ligneTx'].replace('Un mot', ''), (f or {}).get('nb'))
        juge(T + ' A · la pastille de la fiche est celle du Fil (taille, couleur, filet)', ref and a and all(x == ref[0] for x in a), (ref[:1], a[:2]))
        # C · vus
        B.tap_sel(pg, '#detailPoster > .enh .closeb'); pg.wait_for_timeout(1200); pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(400)
        pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); f = fiche(pg)
        juge(T + ' C · rouverte : les trois vus sans pastille, « + 2 » la garde', f and f['rangees'] == [False, False, False] and f['plus'] and f['plus']['att'], f)
        pg.evaluate("()=>window._commDeplie()"); pg.wait_for_timeout(900)
        f2 = fiche(pg)
        pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(500); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); f3 = fiche(pg)
        juge(T + ' C · dépliée (les deux repliés à pastille), puis rouverte : plus aucune pastille', f2 and f2['reste'] == [True, True] and f3 and not any(f3['rangees']) and not any(f3['reste']) and not (f3['plus'] and f3['plus']['att']), (f2 and f2['reste'], f3))
        pg.evaluate("()=>{ closeAll(); }"); B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2400)
        ix2 = pg.evaluate("id=>{ const c=document.querySelector('#indexList .s4-carte[data-pid=\"'+id+'\"]'); return c ? !!c.querySelector(':scope > .s4-att') : null; }", pid)
        juge(T + ' C · tout vu : la carte de l\'Index n\'a plus de pastille', ix2 is False, ix2)
        pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(400)
        # D · le Cercle
        pg.evaluate("()=>{ const k=Object.keys(NUE)[0]; window._cercleMots.de(k).comments.push({t:'un mot', by:'Rachel', d:new Date().toISOString()}); window._cercleMots.garde(); openEssaim(k); }"); pg.wait_for_timeout(2600)
        et = pg.evaluate("()=>(document.getElementById('dptQuand')||{}).textContent||''")
        juge(T + ' D · la ligne d\'état d\'un Cercle ne compte plus les mots', ' mot' not in et, et)
        pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(500)
        # E · le + d'un Promi
        pg.evaluate("id=>{ window.__t0=performance.now(); openDetail(id); window.__tPlus=null; (function f(){ const b=document.getElementById('cerclePlusMembres'); if(b && b.style.display==='flex'){ window.__tPlus=Math.round(performance.now()-window.__t0); return; } if(performance.now()-window.__t0<6000) requestAnimationFrame(f); })(); }", pid); pg.wait_for_timeout(2600)
        for _ in range(20):
            if pg.evaluate("()=>window.__tPlus!=null"): break
            pg.wait_for_timeout(200)
        tplus = pg.evaluate("()=>window.__tPlus"); print('  … le + paraît %s ms après l\'ouverture' % tplus, flush=True)
        g = pg.evaluate("""()=>{ const b=document.getElementById('cerclePlusMembres'), q=document.getElementById('dptQui'); if(!b || getComputedStyle(b).display==='none') return null; const k=window._echDp(document.getElementById('detailPoster'));
          const rg=document.createRange(); rg.selectNodeContents(q); const L=[...rg.getClientRects()].filter(r=>r.width>1); const der=L[L.length-1], s=b.querySelector('svg').getBoundingClientRect(), z=b.getBoundingClientRect();
          return {ecart:Math.round((s.left-der.right)/k*10)/10, h:Math.round(s.height/k*10)/10, zone:Math.round(z.width/k), coul:b.querySelector('path').getAttribute('stroke'), vis:getComputedStyle(b).visibility}; }""")
        juge(T + ' E · le + d\'un Promi : 26 pt après la phrase, orange, zone de 44 pt', g and abs(g['ecart'] - 26) <= 1 and g['coul'].upper() == '#FB4C0D' and g['zone'] == 44 and g['vis'] == 'visible', g)
        B.tap_sel(pg, '#cerclePlusMembres'); pg.wait_for_timeout(1600)
        o = pg.evaluate("""()=>{ const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(x=>/^(À QUI|QUI OSE \\?)$/.test(((x.querySelector('.s2-lab')||{}).textContent||'').trim())); return {s2:document.getElementById('detailPoster').classList.contains('s2-ouv'), ligne:!!r, ouverte:!!(r&&r.classList.contains('s2-ouv'))}; }""")
        juge(T + ' E · au doigt : Peaufiner ouvert sur À QUI, déplié', o['s2'] and o['ligne'] and o['ouverte'], o)
        # F · un membre de plus, par la vraie saisie
        r = B.tap_sel(pg, '#dpdCorps .s2-reg.s2-ouv .gn > .ph-add'); pg.wait_for_timeout(600)   # la zone en pointillés EST le champ (C-122)
        foc = pg.evaluate("()=>document.activeElement && document.activeElement.id")
        if foc != 'gnSaisie': pg.evaluate("()=>{ const s=document.getElementById('gnSaisie'); if(s) s.focus(); }"); pg.wait_for_timeout(300)
        pg.keyboard.type('Adrien', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        w = pg.evaluate("id=>{ const p=promises.find(q=>q.id===id); const h=window._historique(p,'Adrien'); return {who:p.who, chiche:!!p.chiche, nuee:!!p.nuee, mots:h?h.mots.length:null}; }", pid)
        juge(T + ' F · Adrien ajouté : la parole le porte, toujours un Promi, il voit les 5 mots', w['who'] and 'Adrien' in w['who'] and not w['chiche'] and not w['nuee'] and w['mots'] == 5, (w, foc))
        pg.evaluate("()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(500); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); f = fiche(pg)
        juge(T + ' F · la fiche montre les 5 mots (3 + « + 2 »)', f and len(f['rangees']) == 3 and f['plus'] and f['plus']['txt'].startswith('+ 2'), f)
        pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(400)
        # G · Chiche à moi, parole reçue
        g2 = pg.evaluate("""async ()=>{ const vis=()=>{ const b=document.getElementById('cerclePlusMembres'); return !!(b && getComputedStyle(b).display!=='none'); };
          const ch=promises.find(q=>!q.draft && q.chiche && (!q.from || /^moi$/i.test(q.from))); const rc=promises.find(q=>!q.draft && !q.nuee && q.from && !/^moi$/i.test(q.from));
          const r={}; if(ch){ openDetail(ch.id); await new Promise(z=>setTimeout(z,2600)); r.chiche=vis(); closeAll(); await new Promise(z=>setTimeout(z,500)); }
          if(rc){ openDetail(rc.id); await new Promise(z=>setTimeout(z,2600)); r.recue=vis(); closeAll(); } return r; }""")
        juge(T + ' G · un Chiche à moi a son + ; une parole reçue n\'en a pas', g2.get('chiche') is True and g2.get('recue') is False, g2)
        if pg.erreurs: juge(T + ' aucune erreur de page', False, pg.erreurs[:3])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
