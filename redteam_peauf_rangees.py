#!/usr/bin/env python3
"""redteam_peauf_rangees.py — ⚑ v163b (Tom, C-192 ; AUDIT-BOUTONS 5, 8, 10, point 4) : LES RANGÉES DE PEAUFINER FONT CE QU'ELLES DISENT.

« Branche DISSOUDRE LE CERCLE (avec la feuille de confirmation, au masculin) et PIÈCES JOINTES du Promi (le + dans la rangée) et du Cercle. Supprime :
COMMENTAIRES (Promi, Chiche, Cercle) ; LES PROMI DU CERCLE et INVITER dans le Peaufiner de la page + d'un Cercle ; À QUI et AVEC dans le Peaufiner de la
page +. Sur un Chiche reçu, « À QUI JE LANCE » disparaît. »
Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles ; chaque Peaufiner ouvert par sa barre, au doigt :
  A · fiche d'un Promi : aucune rangée COMMENTAIRES ; PIÈCES JOINTES ouverte porte un + de 44 pt qui ouvre le choix de fichiers ;
  B · fiche d'un Chiche reçu : pas de « À QUI JE LANCE » ; fiche d'un Chiche lancé : il est là, sous son mot de §16, « QUI OSE ? » ;
  C · fiche d'un Cercle : pas de COMMENTAIRES ; aucune carte n'en recouvre une autre, « + Planter » sous PIÈCES JOINTES ; PIÈCES JOINTES ouvre le choix de
      fichiers ; DISSOUDRE ouvre la feuille « Dissoudre … ? », « Dissoudre » dissout (le Cercle n'existe plus, ses Promi restent), le bandeau dit « dissous » ;
  D · page + : ni À QUI ni AVEC (Promi, Chiche) ; page + d'un Cercle : ni INVITER ni LES PROMI DU CERCLE.
Preuve : `--fichier=zz-v162.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
PIEGE = "(()=>{ window.__choix=0; const c=HTMLInputElement.prototype.click; HTMLInputElement.prototype.click=function(){ if(this.type==='file'){ window.__choix++; return; } return c.apply(this, arguments); }; })();"
LABS = "()=>[...document.querySelectorAll('#detailPoster .s2-lab, #detailPoster .np-lab, #createSheet .s2-lab')].filter(e=>e.getBoundingClientRect().height>0 && getComputedStyle(e).visibility!=='hidden').map(e=>e.textContent.trim())"
def centre(pg, sel):
    return pg.evaluate("s=>{ const e=typeof s==='string'?document.querySelector(s):null; if(!e) return null; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", sel)
def peauf(pg):
    B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1400)
def ferme(pg):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, F)
    # A · un Promi
    pid = pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && !q.chiche && !q.nuee && q.status!=='tenu'); return p.id; }")
    pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2400); peauf(pg); L = pg.evaluate(LABS)
    juge('A · Promi : aucune rangée COMMENTAIRES', L and 'COMMENTAIRES' not in L, L)
    c = pg.evaluate("()=>{ const r=[...document.querySelectorAll('#detailPoster .s2-reg')].find(x=>/PIÈCES JOINTES/.test(x.textContent)); if(!r) return null; r.scrollIntoView({block:'center'}); const q=r.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(q.left+40-D.left)/k, (q.top+20-D.top)/k]; }")
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(700)
    pl = pg.evaluate("()=>{ const b=document.querySelector('#detailPoster .s2-pj-plus'); if(!b) return null; b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k, r.width/k, r.height/k]; }")
    if pl: n0 = pg.evaluate("()=>window.__choix"); B.tap(pg, pl[0], pl[1]); pg.wait_for_timeout(500); n1 = pg.evaluate("()=>window.__choix")
    juge('A · PIÈCES JOINTES ouverte : un + de 44 pt qui ouvre le choix de fichiers', pl and abs(pl[2] - 44) < 1 and abs(pl[3] - 44) < 1 and n1 == n0 + 1, pl and (pl[2:], n0, n1))
    ferme(pg)
    # B · un Chiche reçu, un Chiche lancé
    ids = pg.evaluate("()=>{ const L=promises.filter(q=>!q.draft && q.chiche && !q.nuee); if(L.length<2){ const p=promises.find(q=>!q.draft && !q.chiche && !q.nuee && q.status!=='tenu' && q.id!==L[0]?.id); p.chiche=true; L.push(p); } L[0].from='Marion'; L[0].who='moi'; L[1].from='moi'; L[1].who='Rachel'; saveState(); syncAll(); return [L[0].id, L[1].id]; }")
    pg.evaluate("i=>openDetail(i)", ids[0]); pg.wait_for_timeout(2400); peauf(pg); L = pg.evaluate(LABS)
    juge('B · Chiche reçu : pas de « À QUI JE LANCE » (devenu « QUI OSE ? », C-197)', L and 'À QUI JE LANCE' not in L and 'QUI OSE ?' not in L, L)
    ferme(pg); pg.evaluate("i=>openDetail(i)", ids[1]); pg.wait_for_timeout(2400); peauf(pg); L = pg.evaluate(LABS)
    juge('B · Chiche lancé : la rangée de la personne défiée est là, nommée « QUI OSE ? » (§16, C-197)', 'QUI OSE ?' in L and 'À QUI JE LANCE' not in L, L)
    ferme(pg)
    # C · un Cercle
    nk = pg.evaluate("()=>{ const k='jardin'; NUE[k]='Les jardiniers'; NUEEMEM[k]=['Marion','Rachel']; NUECREATOR[k]='moi'; promises.filter(q=>!q.draft && !q.chiche).slice(0,2).forEach(q=>{ q.nuee=k; }); saveState(); syncAll(); return k; }"); pg.wait_for_timeout(800)
    nP = pg.evaluate("k=>promises.filter(q=>q.nuee===k).length", nk)
    pg.evaluate("k=>openNueeDetail(k)", nk); pg.wait_for_timeout(2600); peauf(pg); pg.wait_for_timeout(600)
    L = pg.evaluate(LABS)
    juge('C · Cercle : aucune carte COMMENTAIRES', L and 'COMMENTAIRES' not in L, L)
    R = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [...document.querySelectorAll('#npTrait,#npDesc,#npMemb,#npFich,#nfAdd')].filter(e=>e.getBoundingClientRect().height>0).map(e=>{ const r=e.getBoundingClientRect(); return [e.id, Math.round((r.top-D.top)/k), Math.round((r.bottom-D.top)/k)]; }); }")
    chev = [(a[0], b_[0]) for i, a in enumerate(R) for b_ in R[i + 1:] if min(a[2], b_[2]) - max(a[1], b_[1]) > 0.5]
    ordre = [x[0] for x in sorted(R, key=lambda x: x[1])]
    juge('C · Cercle : aucune carte n\'en recouvre une autre, « + Planter » sous PIÈCES JOINTES', not chev and ordre[-2:] == ['npFich', 'nfAdd'], {'cartes': R, 'chevauche': chev})
    c = centre(pg, '#npFich'); n0 = pg.evaluate("()=>window.__choix")
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(600)
    juge('C · PIÈCES JOINTES du Cercle ouvre le choix de fichiers', pg.evaluate("()=>window.__choix") == n0 + 1, (n0, pg.evaluate("()=>window.__choix")))
    c = centre(pg, '#npDiss')
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(700)
    f = pg.evaluate("()=>{ const v=document.getElementById('v16Conf'); return v ? [v.querySelector('.v16-conf-t').textContent, v.querySelector('.v16-oui').textContent] : null; }")
    juge('C · DISSOUDRE ouvre la feuille « Dissoudre … ? »', f and f[0].startswith('Dissoudre') and f[1] == 'Dissoudre', f)
    if f:
        pg.wait_for_timeout(300)
        o = pg.evaluate("()=>{ const e=document.querySelector('#v16Conf .v16-oui'); const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }")
        B.tap(pg, o[0], o[1]); pg.wait_for_timeout(500)
        r = pg.evaluate("k=>({nue:(k in NUE), promi:promises.length, feuille:!!document.getElementById('v16Conf'), ban:(document.body.innerText.match(/«[^»]*» dissou[a-z]*/)||[''])[0]})", nk)
        juge('C · « Dissoudre » : le Cercle n\'existe plus, ses Promi restent, « dissous » au masculin', not r['nue'] and r['ban'].endswith('dissous'), r)
    ferme(pg)
    # D · les pages +
    for nat, interdits in (('promi', ['À QUI', 'AVEC']), ('chiche', ['À QUI JE LANCE', 'QUI OSE ?', 'AVEC']), ('nuee', ['INVITER', 'LES PROMI DU CERCLE'])):
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2400)
        if nat != 'nuee': pg.evaluate("()=>{ window._phrase.qui='Rachel'; window.newWhoSel=['Rachel']; if(window._phraseRendu) _phraseRendu(); if(window._ppTout) _ppTout(); }"); pg.wait_for_timeout(600)
        B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1400); L = pg.evaluate(LABS)
        juge('D · page + %s : ni %s' % (nat, ' ni '.join(interdits)), L and not any(x in L for x in interdits), L)
        ferme(pg)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
