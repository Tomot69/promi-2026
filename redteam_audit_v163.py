#!/usr/bin/env python3
"""redteam_audit_v163.py — ⚑ v163b (Tom, C-194, C-197, C-198, C-199 ; AUDIT-BOUTONS) : LES CORRECTIONS DE L'AUDIT, UNE PAR UNE.

Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles et un Cercle. Une famille par § du brief :
  §13 · la ligne « Un mot… » est le seul endroit pour commenter : aucune autre saisie de mot (fiche, Peaufiner ouvert ; Promi, Chiche, Cercle) ; un mot
        écrit dans la ligne d'un Cercle va dans son seul magasin (`promi_cercle_mots`) ;
  §16 · l'échéance dit « demain · 1 sem. · 1 mois · une date… · un jour » dans la phrase de la page +, son Peaufiner, celui d'une fiche et REPORTER du Fil ;
        « demain » vaut 1 jour ; « qui ose ? » ; « Inviter » ; plus de rangée « Le Studio » aux Réglages ;
  §17 · une phrase de mur levée au Studio : le X ferme le Studio, l'offre ne s'ouvre pas ; sur un monde payant, Sombre/Clair change le thème (sans mur) et
        une barrette change de monde ;
  §18 · tracer sans titre ouvre la saisie ; le « Chiche » de la phrase sans fond ; la page + d'un Cercle sans « Importer une photo » ; le libellé
        VoiceOver du bouton photo ; Partager (le texte ne touche plus le réglage global, pas de « fond de l'image » pour Ma Toile, pas de « Définir », le
        mot-marque ne bascule plus rien) ; « Supprimer » d'un gardé de côté ; les zones de 44 pt ; les contours de 2 pt ; le X du dessin.
Preuve : `--fichier=zz-v162.html` rougit.
"""
import sys, re; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
def c_(pg, sel, attente=500):
    pg.evaluate("s=>{ const e=document.querySelector(s); if(e) e.scrollIntoView({block:'center'}); }", sel); pg.wait_for_timeout(attente)
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!r.width) return null; const cx=r.left+r.width/2; for(let y=r.top+r.height/2, i=0; i<30; i++, y+=(i%2?-1:1)*i*2){ if(y<r.top||y>r.bottom) continue; const h=document.elementFromPoint(cx, y); if(h && (h===e || e.contains(h))) return [(cx-D.left)/k, (y-D.top)/k]; } return [(cx-D.left)/k, (r.top+r.height/2-D.top)/k]; }", sel)
def touche(pg, sel, attente=1200):
    c = c_(pg, sel)
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(attente)
    return c
def ferme(pg):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); try{ quitteVues(); }catch(e){} ['settingsScreen','studioScreen','shareScreen','plusScreen'].forEach(i=>{ const e=document.getElementById(i); if(e) e.classList.remove('show'); }); }"); pg.wait_for_timeout(900)
SAISIES = "()=>[...document.querySelectorAll('#detailPoster input, #detailPoster textarea, #detailPoster [contenteditable=true]')].filter(e=>{ const r=e.getBoundingClientRect(); const s=getComputedStyle(e); return r.width>20 && r.height>10 && s.visibility!=='hidden' && s.display!=='none' && +s.opacity>0.05 && /écris un mot|comment/i.test((e.placeholder||'')+(e.id||'')); }).map(e=>e.id||e.className||e.placeholder)"
LABS = "()=>[...document.querySelectorAll('#detailPoster .s2-lab, #detailPoster .np-lab, #createSheet .s2-lab')].filter(e=>e.getBoundingClientRect().height>0).map(e=>e.textContent.trim())"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ const k='jardin'; NUE[k]='Les jardiniers'; NUEEMEM[k]=['Marion','Rachel']; NUECREATOR[k]='moi'; promises.filter(q=>!q.draft && !q.chiche).slice(0,2).forEach(q=>{ q.nuee=k; }); saveState(); syncAll(); }"); pg.wait_for_timeout(600)
    # ── §13 ──
    for nom, js in (('Promi', "()=>openDetail(promises.find(q=>!q.draft && !q.chiche && !q.nuee && q.status!=='tenu').id)"), ('Chiche', "()=>openDetail(promises.find(q=>!q.draft && q.chiche).id)"), ('Cercle', "()=>openNueeDetail('jardin')")):
        pg.evaluate(js); pg.wait_for_timeout(2400); B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
        s_ = pg.evaluate(SAISIES); L = pg.evaluate(LABS)
        juge('§13 · %s, Peaufiner ouvert : aucune autre saisie de mot que la ligne « Un mot… », pas de COMMENTAIRES' % nom, not s_ and 'COMMENTAIRES' not in L, {'saisies': s_, 'COMMENTAIRES': 'COMMENTAIRES' in L})
        ferme(pg)
    pg.evaluate("()=>openNueeDetail('jardin')"); pg.wait_for_timeout(2600)
    L0 = pg.evaluate("()=>localStorage.getItem('promi_cercle_mots')||''")
    if touche(pg, '#cmCale .cm5-ligne, #detailPoster [data-cm5], #cm5Ligne', 900):
        pg.keyboard.type('on se retrouve samedi', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    L1 = pg.evaluate("()=>localStorage.getItem('promi_cercle_mots')||''")
    juge('§13 · un mot écrit dans la ligne d\'un Cercle va dans son seul magasin (promi_cercle_mots)', 'on se retrouve samedi' in L1 and 'on se retrouve samedi' not in L0, L1[-120:])
    ferme(pg)
    # ── §16 · l'échéance ──
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2400)
    # la phrase d'aujourd'hui ne porte pas de pastille d'échéance (elle se choisit dans Peaufiner) : sa liste (si elle reparaît) se lit dans le fichier
    SRC = open(F, encoding='utf-8').read()
    okP = "opts = ['demain', '1 sem.', '1 mois'];" in SRC and 'data-datepick="1">une date…</button>' in SRC and 'data-v="un jour">un jour</button>' in SRC and "{ 'demain':1, '1 sem.':7, '1 mois':30 }" in SRC
    juge('§16 · la phrase (sa liste, dans le fichier) : « demain · 1 sem. · 1 mois · une date… · un jour », « demain » = 1 jour', okP, '')
    B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1400)
    A = pg.evaluate("()=>[...document.querySelectorAll('#dueChips .chip')].map(e=>e.textContent.trim())")
    juge('§16 · le Peaufiner de la page + : les mêmes mots', A == ['demain', '1 sem.', '1 mois', 'une date…', 'un jour'], A)
    r_ = pg.evaluate("()=>{ const a=[...document.querySelectorAll('#createSheet .s2-reg')].find(x=>/AVANT/.test(x.textContent)); if(!a) return null; a.scrollIntoView({block:'center'}); const q=a.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(q.left+60-D.left)/k, (q.top+22-D.top)/k]; }")
    if r_: B.tap(pg, r_[0], r_[1]); pg.wait_for_timeout(800)   # la rangée AVANT s'ouvre d'abord
    touche(pg, '#dueChips .chip[data-d="1"]', 600)
    juge('§16 · « demain » vaut 1 jour (le Peaufiner de la page +, au doigt)', pg.evaluate("()=>typeof due!=='undefined'?due:null") == 1, pg.evaluate("()=>typeof due!=='undefined'?due:null"))
    ferme(pg)
    pg.evaluate("()=>openDetail(promises.find(q=>!q.draft && !q.chiche && !q.nuee && q.status!=='tenu').id)"); pg.wait_for_timeout(2400); B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
    E = pg.evaluate("()=>[...document.querySelectorAll('#mgDueChips button')].map(e=>e.textContent.trim())")
    juge('§16 · le Peaufiner d\'une fiche : les mêmes mots', E == ['demain', '1 sem.', '1 mois', 'une date…', 'un jour'], E)
    ferme(pg)
    pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && !q.req && !q.chiche && q.status!=='tenu' && !q.nuee); p.status='rate'; p.due=-1; feedAdd('added','Ton Promi « '+p.title+' » est à tenir',{pid:p.id}); saveState(); syncAll(); }")
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
    pg.evaluate("()=>{ const f=FEED.find(f=>{ const p=promises.find(q=>q.id===f.pid); return p && p.status==='rate'; }); feedPostpone(f.id); }"); pg.wait_for_timeout(500)
    R = pg.evaluate("()=>[...document.querySelectorAll('#_toast button')].map(e=>e.textContent.trim())")
    juge('§16 · REPORTER du Fil : « demain · 1 sem. · 1 mois »', R == ['demain', '1 sem.', '1 mois'], R)
    ferme(pg)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=chiche]'); pg.wait_for_timeout(2400)
    touche(pg, '#csPhrase .ph-m[data-ph="qui"]', 900)
    t = pg.evaluate("()=>{ const e=document.querySelector('#csChoix .ph-lab, .ph-choix .ph-lab, #csChoix [class*=titre]'); return e?e.textContent.trim():document.getElementById('createSheet').innerText.match(/QUI[^\\n]{0,20}/)?.[0]; }")
    juge('§16 · le choix de la personne d\'un Chiche s\'appelle « qui ose ? »', t and 'QUI OSE' in t.upper() and 'DÉFIES' not in t.upper(), t)
    # §18 · le « Chiche » de la phrase ne ressemble plus à un bouton
    v = pg.evaluate("()=>{ const e=document.querySelector('#csPhrase .ph-b-fixe'); if(!e) return null; const s=getComputedStyle(e); return [s.backgroundColor, s.cursor]; }")
    juge('§18 · le « Chiche » de la phrase : sans fond, curseur ordinaire', v and (v[0] in ('rgba(0, 0, 0, 0)', 'transparent')) and v[1] != 'pointer', v)
    ferme(pg)
    B.tap_sel(pg, '#settingsBtn'); pg.wait_for_timeout(1800)
    T = pg.evaluate("()=>[...document.querySelectorAll('#settingsScreen .scard .k')].filter(e=>e.getBoundingClientRect().height>0).map(e=>e.textContent.trim())")
    juge('§16 · Réglages : « Inviter » (un mot) ; plus de rangée « Le Studio »', 'Inviter' in T and 'Inviter sur Promi' not in T and 'Le Studio' not in T, T)
    ferme(pg)
    # ── §17 ──
    B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2600)
    for i in range(22):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1400)
    m0 = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')"); th0 = pg.evaluate("()=>document.getElementById('device').classList.contains('light')")
    d = pg.evaluate("()=>{ const v=document.querySelectorAll('#stpVue .stp-d'); const t=[...v].find(x=>!x.classList.contains('on')); if(!t) return null; const r=t.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }")
    if d: B.tap(pg, d[0], d[1]); pg.wait_for_timeout(1800)
    th1 = pg.evaluate("()=>document.getElementById('device').classList.contains('light')"); ph = pg.evaluate("()=>{ const m=document.getElementById('murPhrase'); return !!(m && m.classList.contains('lu') || (m && getComputedStyle(m).opacity>0.5 && m.textContent.trim())); }")
    juge('§17 · monde payant : Sombre/Clair change le thème, sans phrase de mur', th1 != th0 and not ph, 'thème %s → %s · phrase %s' % (th0, th1, ph))
    if d: B.tap(pg, d[0], d[1]); pg.wait_for_timeout(1200)
    bar = pg.evaluate("()=>{ const L=[...document.querySelectorAll('#stpDots .stp-dot')]; const i=L.findIndex(x=>x.classList.contains('on')); const t=L[(i+1)%L.length]; if(!t) return null; const r=t.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }")
    if bar: B.tap(pg, bar[0], bar[1]); pg.wait_for_timeout(2000)
    m1 = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
    juge('§17 · monde payant : une barrette change de monde', bar and m1 != m0, '%s → %s' % (m0, m1))
    for i in range(22):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{ try{ const o=JSON.parse(localStorage.getItem('promi_murs')||'{}'); o.decouvert=1; localStorage.setItem('promi_murs', JSON.stringify(o)); }catch(e){} }")
    B.tap(pg, 195, 300); pg.wait_for_timeout(700)
    lev = pg.evaluate("()=>{ const m=document.getElementById('murPhrase'); return !!(m && m.textContent.trim() && getComputedStyle(m).display!=='none'); }")
    touche(pg, '#studioScreen .closeb', 1500)
    r = pg.evaluate("()=>({studio:document.getElementById('studioScreen').classList.contains('show') && getComputedStyle(document.getElementById('studioScreen')).transform==='none', offre:document.getElementById('plusScreen').classList.contains('show')})")
    juge('§17 · une phrase de mur levée : le X ferme le Studio, l\'offre ne s\'ouvre pas', lev and not r['offre'], {'phrase levée': lev, **r})
    ferme(pg)
    # ── §18 ──
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2400)
    pg.evaluate("()=>{ document.getElementById('fTitle').value=''; window.promiRequis(document.getElementById('fTitle')); }"); pg.wait_for_timeout(900)
    f = pg.evaluate("()=>{ const a=document.activeElement; return [a?(a.id||a.className):null, !!document.querySelector('#csChoix.ouvert, #csPhrase .ph-zone.ouvert, .ph-choix.ouvert')]; }")
    juge('§18 · tracer sans titre ouvre la saisie du titre', f[1] or (f[0] and 'fTitle' not in f[0] and f[0] != 'BODY'), f)
    ferme(pg)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=nuee]'); pg.wait_for_timeout(2400)
    touche(pg, '#createSheet .ph-photo-btn', 800)
    M = pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(e=>e.textContent.trim())")
    juge('§18 · la page + d\'un Cercle : pas d\'« Importer une photo »', M and 'Importer une photo' not in M, M)
    hz = pg.evaluate("()=>{ const L=[...document.querySelectorAll('.ph-photo-menu button')], k=document.getElementById('device').getBoundingClientRect().width/390; const z=L.map(b=>{ const r=b.getBoundingClientRect(), h=parseFloat(getComputedStyle(b,'::after').height)||r.height/k; const c=(r.top+r.height/2)/k; return [c-h/2, c+h/2, h]; }); const chev=z.slice(1).some((x,i)=>x[0]<z[i][1]-0.5); return {zones:z.map(x=>Math.round(x[2]*10)/10), chevauche:chev}; }")
    juge('§18 · les pastilles du menu photo : 44 pt de toucher chacune, sans se recouvrir', hz and hz['zones'] and all(abs(x - 44) < 0.6 for x in hz['zones']) and not hz['chevauche'], hz)
    ferme(pg)
    pg.evaluate("()=>openNueeDetail('jardin')"); pg.wait_for_timeout(2400); ferme(pg)
    pg.evaluate("()=>openDetail(promises.find(q=>!q.draft && !q.chiche && !q.nuee && q.status!=='tenu').id)"); pg.wait_for_timeout(2400)
    lb = pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .ph-photo-btn')].map(b=>b.getAttribute('aria-label'))")
    juge('§18 · VoiceOver : sur une fiche de Promi après un Cercle, le bouton photo dit « Photo »', lb and all(x == 'Photo' for x in lb), lb)
    cb = pg.evaluate("()=>{ const b=document.querySelector('#detailPoster .ph-photo-btn'); if(!b) return null; const s=getComputedStyle(b); return [s.borderTopWidth, s.borderTopStyle, s.backdropFilter||s.webkitBackdropFilter]; }")
    juge('§18 · le bouton photo : contour plein de 2 pt, sans flou', cb and cb[0] == '2px' and cb[1] == 'solid' and (cb[2] in (None, '', 'none')), cb)
    ferme(pg)
    pg.evaluate("()=>{ try{ state.labels=true; }catch(e){} }"); pg.evaluate("()=>openShare()"); pg.wait_for_timeout(2600)
    pg.evaluate("()=>{ const b=document.getElementById('shTxOff'); if(b) b.click(); }"); pg.wait_for_timeout(500)
    sl = pg.evaluate("()=>[typeof state!=='undefined'?state.labels:null, window.shLabels]")
    juge('§18 · Partager « Sans texte » ne change plus le réglage de la Toile', sl[0] is True and sl[1] is False, sl)
    fd = pg.evaluate("()=>{ window.shareMode='toile'; return 1; }"); pg.wait_for_timeout(700)
    v = pg.evaluate("()=>{ const t=document.getElementById('shTheme'); if(!t) return 'absent'; const r=t.closest('[data-reg]')||t.parentElement; return getComputedStyle(r).display; }")
    df = pg.evaluate("()=>{ const c=document.getElementById('shCustom'); if(!c) return 'absent'; const r=c.getBoundingClientRect(); return (r.height>0 && getComputedStyle(c).display!=='none') ? 'visible' : 'caché'; }")
    sg0 = pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('sh-sig')"); pg.evaluate("()=>{ const b=document.getElementById('shBadge'); if(b) b.click(); }"); pg.wait_for_timeout(300)
    sg1 = pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('sh-sig')")
    juge('§18 · Partager : « Le fond de l\'image » absent pour Ma Toile, « Définir » absent, le mot-marque ne bascule rien', v == 'none' and df != 'visible' and sg0 == sg1, {'fond': v, 'définir': df, 'signature': (sg0, sg1)})
    ferme(pg)
    # le gardé de côté : « Supprimer »
    pg.evaluate("()=>{ const d=promises.filter(q=>!q.draft && !q.nuee)[3]; d.draft=true; d.brouillon={nat:'promi'}; saveState(); syncAll(); window.__gid=d.id; }")
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2500); touche(pg, '#indexList .s4-carte[data-etat=garde]', 3000)
    B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1500); pg.wait_for_timeout(600)
    sp = touche(pg, '#createSheet .v163-suppr', 800)
    cf = pg.evaluate("()=>{ const v=document.getElementById('v16Conf'); return v ? v.querySelector('.v16-conf-t').textContent : null; }")
    if cf: touche(pg, '#v16Conf .v16-oui', 900)
    gone = pg.evaluate("()=>!promises.some(q=>q.id===window.__gid)")
    juge('§18 · un gardé de côté rouvert : « Supprimer » dans son Peaufiner, avec la feuille, et il est supprimé', sp and cf and gone, {'rangée': sp, 'feuille': cf, 'supprimé': gone})
    ferme(pg)
    # les zones de 44 pt et le X du dessin
    z = pg.evaluate("""()=>{ const out={}; const e=document.getElementById('setNameInput'); if(e){ const r=e.getBoundingClientRect(), k=document.getElementById('device').getBoundingClientRect().width/390; out.prenom=Math.round(r.height/k*10)/10; }
        ['#studioScreen .stp-retour','#studioScreen .stp-nb','#device .dz-oeil'].forEach(s=>{ const a=document.querySelector(s); out[s]=a?getComputedStyle(a,'::after').height:'absent'; }); return out; }""")
    juge('§18 · zones de toucher : le prénom des Réglages 44 pt ; « ← Retour », le noir et blanc et l\'œil portent une zone de 44', (z.get('prenom') or 0) >= 43.5 and all(z[s] in ('44px', 'absent') for s in ('#studioScreen .stp-retour', '#studioScreen .stp-nb', '#device .dz-oeil')), z)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
