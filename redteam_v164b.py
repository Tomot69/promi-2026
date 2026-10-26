#!/usr/bin/env python3
"""redteam_v164b.py — ⚑ v164b (Tom, réponse au lot v163) : TRIER (Q582) ET LES HUIT POINTS DE L'AUDIT (C-200), AU DOIGT.

  T · TRIER (Index et Fil) : le mot « TRIER » seul, en capitales (Gilbert, la police des libellés), à l'encre du mode, sans contour ni fond, ouvert ou
      fermé ; sa zone de toucher ≥ 44 pt, invisible, prise à son centre ; un toucher ouvre le menu.
  ① le bandeau « Garder ta Toile » : un premier « Plus tard », il revient plus loin ; un deuxième, il ne revient plus ; la rangée des Réglages reste.
  ② « RELANCER [nom] » n'est plus dans le Peaufiner d'une fiche reçue ; `#actRelance` n'existe plus.
  ③ Notifications : « de temps en temps, un mot », plus « une douce relance ».
  ④ le mot « Promi » de l'accueil, touché au doigt, n'ouvre pas Ma Parole !.
  ⑤ l'écran de Ma Parole ! ne montre plus « 5,99 ».
  ⑥ la Toile vide ne porte plus « touche le + ».
  ⑦ « Mention sur un dessin partagé » n'est plus aux Réglages ; elle est dans le panneau du Partage, et un toucher la change (mémorisé).
  ⑧ l'écran « La langue » et son code n'existent plus.
Banc comme Tom (WebKit, 390 × 844 ×3, doigt), clair et sombre pour T. Preuve : `--fichier=zz-v164a.html` rougit.
"""
import sys
sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
VU = """(sel)=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; const o=[];
  document.querySelectorAll(sel).forEach(e=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e); if(r.width<1||r.height<1||c.visibility==='hidden'||c.display==='none'||+c.opacity<0.05) return;
    if(r.bottom<d.top||r.top>d.bottom||r.right<d.left||r.left>d.right) return; const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').trim(); if(t) o.push(t); }); return o.join(' | '); }"""
BOUTON = """(s)=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, c=getComputedStyle(e);
  const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
  return {txt:(e.innerText||'').trim(), w:r.width/k, h:r.height/k, col:c.color, bg:c.backgroundColor, bd:parseFloat(c.borderTopWidth)+parseFloat(c.borderLeftWidth), sh:c.boxShadow, f:c.fontFamily.split(',')[0].replace(/["']/g,''), hit:h===e||e.contains(h)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    # ── T · TRIER ──
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'; ink = 'rgb(247, 240, 222)' if sombre else 'rgb(32, 25, 8)'
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
        for ecr, porte, btn, menu in (('Index', "document.getElementById('indexBtn').click()", '#ixTriBtn', '#ixMenu'), ('Fil', "openFeed()", '#fdTriBtn', '#fdMenu')):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} try{ %s }catch(e){} }" % porte); pg.wait_for_timeout(2600)
            r = pg.evaluate(BOUTON, btn) or {}
            juge('[%s · %s] T · le mot « TRIER » seul, Gilbert, à l\'encre du mode' % (T, ecr), r.get('txt') == 'TRIER' and r.get('f') == 'Gilbert' and r.get('col') == ink, r)
            juge('[%s · %s] T · ni contour, ni fond, ni ombre' % (T, ecr), r.get('bd') == 0 and r.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent') and r.get('sh') in ('none', ''), r)
            juge('[%s · %s] T · zone de toucher ≥ 44 pt, prise à son centre' % (T, ecr), r.get('w', 0) >= 44 - 0.5 and r.get('h', 0) >= 44 - 0.5 and r.get('hit'), r)
            B.tap_sel(pg, btn); pg.wait_for_timeout(900)
            ouv = pg.evaluate("(m)=>{ const e=document.querySelector(m); if(!e) return false; const c=getComputedStyle(e); return c.display!=='none' && c.visibility!=='hidden' && (e.classList.contains('on')||e.classList.contains('ouvert')||e.classList.contains('show')||+c.opacity>0.5); }", menu)
            r2 = pg.evaluate(BOUTON, btn) or {}
            juge('[%s · %s] T · un toucher ouvre le menu ; ouvert, toujours ni fond ni contour' % (T, ecr), ouv and r2.get('bd') == 0 and r2.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent'), {'menu': ouv, 'bg': r2.get('bg'), 'bd': r2.get('bd')})
        ctx.close()
    # ── ④ le mot « Promi » (sur un accueil frais : rien d'ouvert par-dessus) ──
    ctx4 = B.contexte(b); B.toile_pleine(ctx4, 10); pg4 = B.ouvre(ctx4, F)
    pg4.evaluate("()=>{ try{closeAll()}catch(e){} window.__oc=0; const o=window.ouvreCercle; window.ouvreCercle=function(){ window.__oc++; return o.apply(this,arguments); }; }"); pg4.wait_for_timeout(2000)
    sous = pg4.evaluate("()=>{ const m=document.querySelector('.acc-plat .acc-mm'); if(!m) return null; const r=m.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!h && (h===m || m.contains(h)); }")
    B.tap_sel(pg4, '.acc-plat .acc-mm'); pg4.wait_for_timeout(1500)
    o4 = pg4.evaluate("()=>[window.__oc, document.getElementById('plusScreen').classList.contains('show')]")
    juge('④ le mot « Promi » de l\'accueil, touché au doigt (le doigt tombe sur lui), n\'ouvre pas Ma Parole !', sous is True and o4 == [0, False], {'sous le doigt': sous, 'ouvreCercle, montré': o4})
    ctx4.close()
    # ── ① le bandeau ──
    ctx = B.contexte(b, stockage={'promi_rappel_n': '0', 'promi_debut': '1'}); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.setItem('promi_rappel_n','0'); localStorage.removeItem('promi_rappel_non'); localStorage.removeItem('promi_rappel_fin'); localStorage.removeItem('promi_compte'); closeAll(); }catch(e){} }")
    VUB = "()=>{ const e=document.getElementById('accRappel'); return !!(e && e.classList.contains('vu') && !e.classList.contains('rap-cache')); }"
    def attend(n=10):
        for _ in range(n):
            if pg.evaluate(VUB): return True
            pg.wait_for_timeout(700)
        return False
    v1 = attend(); juge('① le bandeau « Garder ta Toile » paraît', v1)
    if v1: B.tap_sel(pg, '#accRappel [data-r=non]'); pg.wait_for_timeout(700)
    pg.evaluate("()=>localStorage.setItem('promi_rappel_t', String(Date.now()-30*864e5))")
    v2 = attend(); juge('① après un « Plus tard », il revient plus loin', v1 and v2, pg.evaluate("()=>({n:localStorage.getItem('promi_rappel_n'), non:localStorage.getItem('promi_rappel_non')})"))
    if v2: B.tap_sel(pg, '#accRappel [data-r=non]'); pg.wait_for_timeout(700)
    pg.evaluate("()=>localStorage.setItem('promi_rappel_t', String(Date.now()-60*864e5))"); pg.wait_for_timeout(7500)
    juge('① après le deuxième « Plus tard », il ne revient plus', v2 and not pg.evaluate(VUB), pg.evaluate("()=>({non:localStorage.getItem('promi_rappel_non'), fin:localStorage.getItem('promi_rappel_fin')})"))
    juge('① « Garder ta Toile » reste aux Réglages', pg.evaluate("()=>!!document.getElementById('compteCard') && /Garder ta Toile/.test(document.getElementById('compteCard').textContent)"))
    # ── ② RELANCER ──
    pg.evaluate("()=>{ const p=promises.find(q=>!q.draft&&q.status==='encours'&&q.from&&q.from!=='moi') || promises.find(q=>!q.draft&&q.status==='encours'); window.__pid=p.id; if(!p.from||p.from==='moi'){ p.from='Marion'; } closeAll(); openDetail(p.id); }")
    pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ try{ if(window._s2Ouvre) _s2Ouvre(true); else if(window.peaufOuvre) peaufOuvre(true); else { const b=document.querySelector('#dpDetails .dpd-bar, #dpDetails .s2-barre'); if(b) b.click(); } }catch(e){} }"); pg.wait_for_timeout(1800)
    txt = pg.evaluate("()=>document.getElementById('detailPoster').innerText")
    juge('② « RELANCER » n\'est plus dans le Peaufiner d\'une fiche reçue', 'RELANCER' not in txt.upper().replace('RELANCÉ', ''), [l for l in txt.split('\n') if 'ELANC' in l.upper()][:3])
    juge('② #actRelance n\'existe plus', not pg.evaluate("()=>!!document.getElementById('actRelance')"))
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(900)
    # ── ③ les notifications ──
    pg.evaluate("()=>{ closeAll(); const s=document.getElementById('settingsBtn'); if(s) s.click(); }"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const c=document.getElementById('notifCard'); if(c) c.click(); }"); pg.wait_for_timeout(1800)
    tn = pg.evaluate("()=>document.body.innerText")
    juge('③ Notifications : « de temps en temps, un mot », plus « une douce relance »', 'de temps en temps, un mot' in tn and 'douce relance' not in tn, [l for l in tn.split('\n') if 'temps en temps' in l][:2])
    # ── ⑦ (Réglages) ──
    pg.evaluate("()=>{ closeAll(); const s=document.getElementById('settingsBtn'); if(s) s.click(); }"); pg.wait_for_timeout(1500)
    juge('⑦ « Mention sur un dessin partagé » n\'est plus aux Réglages', not pg.evaluate("()=>!!document.getElementById('setMention')") and 'Mention sur un dessin' not in pg.evaluate("()=>document.getElementById('settingsScreen').innerText"))
    # ── ⑧ la langue ──
    juge('⑧ l\'écran « La langue » et son code n\'existent plus', pg.evaluate("()=>!document.getElementById('langScreen') && !document.getElementById('langCard') && typeof window.buildLang==='undefined' && typeof LANGS==='undefined'"))
    # ── ⑤ 5,99 ──
    pg.evaluate("()=>{ closeAll(); window.ouvreCercle(); document.getElementById('plusScreen').classList.add('show'); }"); pg.wait_for_timeout(2500)
    vu = pg.evaluate(VU, '#plusScreen *')
    juge('⑤ l\'écran de Ma Parole ! ne montre plus « 5,99 »', '5,99' not in vu and 'par mois' not in vu, [x for x in vu.split(' | ') if '€' in x][:4])
    # ── ⑥ la Toile vide ──
    juge('⑥ la Toile vide ne porte plus « touche le + »', 'touche le' not in pg.evaluate("()=>(document.getElementById('toileEmpty')||{}).textContent||''"))
    # ── ⑦ (Partage) ──
    pg.evaluate("()=>{ closeAll(); const s=document.getElementById('shareBtn'); if(s) s.click(); }"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ const f=document.getElementById('shcPeaufiner'); if(f) f.click(); }"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const e=document.getElementById('shMentionRow'); if(e) e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(700)
    row = pg.evaluate("()=>{ const r=document.getElementById('shMentionRow'); if(!r) return null; const l=r.parentNode.querySelector('.l'); const bt=document.getElementById('shMentionOff').getBoundingClientRect(); const h=document.elementFromPoint(bt.left+bt.width/2, bt.top+bt.height/2); return {lab:l&&l.textContent, on:document.getElementById('shMentionOn').classList.contains('on'), hit:h&&h.id==='shMentionOff'}; }")
    juge('⑦ la rangée est dans le panneau du Partage, joignable, « Affichée » par défaut', bool(row and row['lab'] == 'MENTION SUR UN DESSIN PARTAGÉ' and row['on'] and row['hit']), row)
    if row: B.tap_sel(pg, '#shMentionOff'); pg.wait_for_timeout(700)
    k1 = pg.evaluate("()=>localStorage.getItem('promi_dessin_mention')")
    if row: B.tap_sel(pg, '#shMentionOn'); pg.wait_for_timeout(700)
    k2 = pg.evaluate("()=>localStorage.getItem('promi_dessin_mention')")
    juge('⑦ au doigt : « Masquée » la masque, « Affichée » la rend, c\'est mémorisé', k1 == '0' and k2 == '1', (k1, k2))
    er = [x for x in pg.erreurs if 'version.json' not in x]
    juge('aucune erreur de page', not er, er[:2])
    ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
