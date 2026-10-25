#!/usr/bin/env python3
"""
⚑ v163b (C-197) : les pastilles de l'échéance sont « demain · 1 sem. · 1 mois · une date… · un jour » partout ; le juge choisit dans ces mots
(original : sauvegardes/redteam_peaufiner-avant-v163b.py) — même intention, même sévérité.
redteam_peaufiner.py — PEAUFINER RESTE OUVERT (v146, Tom, 14 oct. 2026 — C-134).
« Un choix dans Peaufiner s'applique sur place. Peaufiner reste ouvert […]. On en sort par un glissement du haut vers le bas de l'écran.
  Peaufiner redescend dans son bandeau normal en bas, et on revient à la fiche (ou à la page +). Plus JAMAIS de retour à la Toile depuis Peaufiner. »
Banc comme Tom (banc_tom : WebKit, 390 × 844 ×3, doigt), une Toile de 25 paroles relue de la sauvegarde. La fiche est ouverte par script (le sujet
est Peaufiner, pas le chemin jusqu'à la fiche) ; tout ce qui se passe DANS Peaufiner se fait au doigt.
  A  fiche : plusieurs choix d'affilée (échéance ×2, le trait, l'à-qui) — chacun appliqué (lu dans la parole), Peaufiner reste ouvert, la fiche reste
     la même, jamais la Toile ;
  B  page + : plusieurs choix d'affilée (échéance ×2, la couleur avec Ma Parole !) — idem ;
  C  la sortie : un glissement de 220 pt vers le bas referme Peaufiner et rend LA MÊME fiche (ou la page + avec sa phrase) ; un glissement de 60 pt
     ne referme rien ; un glissement quand Peaufiner est défilé ne referme rien ; un glissé horizontal sur le rail du trait ne referme rien ;
  D  la sonde du chemin inconnu : un choix dont le geste mène à une fermeture générale (sur le coup, ou 1 s après) — Peaufiner reste ouvert, le refus est
     gardé avec sa pile (et envoyé au Mac avec ?mesure=1) ;
  E  les sorties voulues restent possibles : « Supprimer ce Promi » ; l'offre Ma Parole ! ouverte d'un mur s'ouvre PAR-DESSUS et, refermée, rend Peaufiner.
Preuve (§7) : `--fichier=zz-avant-v146.html` — C et D rougissent (aucune sortie par le bas ; la fermeture générale ramène à la Toile).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-112s %s' % ('✅' if c else '❌', nom, str(d)[:240]), flush=True)
ET = """()=>{ const dp=document.getElementById('detailPoster'), cs=document.getElementById('createSheet'); const vus=[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show')].map(e=>e.id);
  return {fiche:dp.classList.contains('show'), peauf:dp.classList.contains('s2-ouv'), plus:cs.classList.contains('show'), ppeauf:cs.classList.contains('pp-peauf'), cur:(typeof cur!=='undefined'&&cur)?cur.title:null,
    toile:!vus.filter(i=>!/^(studioScreen|auraScreen|shareScreen)$/.test(i)).length, vus:vus.join(' '), offre:!!(document.getElementById('plusScreen')&&document.getElementById('plusScreen').classList.contains('show'))}; }"""
RANG = """([rac, lab])=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=[...document.querySelectorAll(rac+' .s2-reg')].find(x=>{const l=x.querySelector('.s2-lab'); return l&&l.textContent.trim()===lab;}); if(!r) return null;
  const sc=r.closest('.dpd-corps'); if(sc){ const q=r.getBoundingClientRect(), s=sc.getBoundingClientRect(); sc.scrollTop+= (q.top-s.top)-90; } const q=r.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k, (q.top+24-D.top)/k, r.classList.contains('s2-ouv')]; }"""
OPT = """([rac, lab, t])=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=[...document.querySelectorAll(rac+' .s2-reg')].find(x=>{const l=x.querySelector('.s2-lab'); return l&&l.textContent.trim()===lab;}); if(!r) return null;
  const e=[...r.querySelectorAll('button, .chip, .s2-ech, .pc-n, .cc-ton, .ph-o')].find(x=>(x.getAttribute('aria-label')||x.textContent||'').trim()===t); if(!e) return null; e.scrollIntoView({block:'nearest', inline:'center'}); const q=e.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k, (q.top+q.height/2-D.top)/k]; }"""
def choisit(pg, rac, lab, t):
    r = pg.evaluate(RANG, [rac, lab]); pg.wait_for_timeout(250); r = pg.evaluate(RANG, [rac, lab])
    if not r: return False
    if not r[2]: B.tap(pg, r[0], r[1]); pg.wait_for_timeout(700)
    o = pg.evaluate(OPT, [rac, lab, t]); pg.wait_for_timeout(250); o = pg.evaluate(OPT, [rac, lab, t])
    if not o: return False
    B.tap(pg, o[0], o[1]); pg.wait_for_timeout(1300); return True
def fiche(pg, titre):
    pg.evaluate("(t)=>{ closeAll(); const q=promises.filter(q=>q.title===t)[0]; openDetail(q.id); }", titre); pg.wait_for_timeout(2600)
    B.tap_sel(pg, '#dpDetails .dpd-tog'); pg.wait_for_timeout(1100)
def page(pg):
    pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); var n=0; (function e(){ var x=[...document.querySelectorAll('#createSheet .tile')][0]; var cs=document.getElementById('createSheet'); if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(e,350); })(); }"); pg.wait_for_timeout(2800)
    pg.evaluate("()=>{ const z=document.querySelector('#csPhrase [data-ph=quoi], #csPhrase .ph-quoi'); }")
    B.tap_sel(pg, '#csBotBar'); pg.wait_for_timeout(1100)
P = "(t)=>{ const q=promises.filter(q=>q.title===t)[0]; return q?{due:q.due, enLair:!!q.enLair, pinceau:q.pinceau||q.trait||null, who:q.who}:null; }"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    T = pg.evaluate("()=>{ const q=promises.filter(q=>!q.done&&q.who&&q.who!=='moi'&&!q.nuee&&q.kind!=='chiche')[0]; return q&&q.title; }")
    print('── A · la fiche « %s », plusieurs choix d\'affilée, au doigt' % T); fiche(pg, T); e0 = pg.evaluate(ET)
    juge('A · Peaufiner s\'ouvre sur la fiche', e0['fiche'] and e0['peauf'], e0)
    for lab, t, lit in (('AVANT', 'demain', lambda v: v['due'] == 1), ('AVANT', '1 sem.', lambda v: v['due'] == 7), ('AVANT', '1 mois', lambda v: v['due'] == 30)):
        ok = choisit(pg, '#detailPoster', lab, t); e = pg.evaluate(ET); v = pg.evaluate(P, T)
        juge('A · « %s » → « %s » : appliqué sur place, Peaufiner reste ouvert sur la même fiche, pas la Toile' % (lab, t), ok and lit(v) and e['peauf'] and e['fiche'] and e['cur'] == T and not e['toile'], '%s · %s' % (v, e['vus']))
    pc0 = pg.evaluate("()=>{ const a=[...document.querySelectorAll('#detailPoster .pc-n')]; return a.map(x=>x.textContent.trim()); }")
    t2 = next((x for x in pc0 if x not in ('Plein',)), None); ok = choisit(pg, '#detailPoster', 'LE TRAIT', t2) if t2 else False; e = pg.evaluate(ET)
    lu = pg.evaluate("()=>{ const v=[...document.querySelectorAll('#detailPoster .s2-reg')].find(x=>x.querySelector('.s2-lab').textContent.trim()==='LE TRAIT'); return v?v.querySelector('.s2-val').textContent.trim():null; }")
    juge('A · LE TRAIT → « %s » : appliqué (la valeur du réglage le dit), Peaufiner reste ouvert' % t2, ok and lu == t2 and e['peauf'] and e['fiche'] and not e['toile'], 'valeur %s · %s' % (lu, e['vus']))
    # C · la sortie
    print('── C · la sortie par le bas')
    pg.evaluate("()=>{ const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=0; }"); pg.wait_for_timeout(300)
    B.glisse(pg, B.droite([195, 200], [195, 260], 6), pas=16); pg.wait_for_timeout(700); e = pg.evaluate(ET)
    juge('C · un glissement de 60 pt vers le bas ne referme rien (Peaufiner remonte à sa place)', e['peauf'] and e['fiche'], e['vus'])
    pg.evaluate("()=>{ const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=300; }"); pg.wait_for_timeout(300)
    B.glisse(pg, B.droite([195, 250], [195, 470], 14), pas=16); pg.wait_for_timeout(900); e = pg.evaluate(ET)
    juge('C · Peaufiner défilé : un glissement vers le bas le fait défiler, il ne le referme pas', e['peauf'] and e['fiche'], '%s · défilement %s' % (e['vus'], pg.evaluate("()=>document.getElementById('dpdCorps').scrollTop")))
    pg.evaluate("()=>{ const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=0; }"); pg.wait_for_timeout(300)
    rail = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const e=document.querySelector('#detailPoster .pc-n'); if(!e) return null; const q=e.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k, (q.top+q.height/2-D.top)/k]; }")
    if rail and 120 < rail[1] < 700:
        B.glisse(pg, B.droite(rail, [rail[0] - 150, rail[1] + 12], 12), pas=16); pg.wait_for_timeout(800); e = pg.evaluate(ET)
        juge('C · un glissé horizontal sur le rail du trait ne referme rien', e['peauf'] and e['fiche'], e['vus'])
    pg.wait_for_timeout(300); pg.evaluate("()=>{ const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=0; }"); pg.wait_for_timeout(300)
    B.glisse(pg, B.droite([195, 180], [195, 400], 14), pas=16); pg.wait_for_timeout(1000); e = pg.evaluate(ET)
    juge('C · un glissement de 220 pt vers le bas referme Peaufiner et rend LA MÊME fiche — jamais la Toile', not e['peauf'] and e['fiche'] and e['cur'] == T and not e['toile'], e)
    B.capture(pg, 'planche-v146/peaufiner-sortie-fiche.png')
    # D · la sonde : un choix qui mène à une fermeture générale (sur le coup, puis 1 s après)
    print('── D · la sonde du chemin inconnu')
    B.tap_sel(pg, '#dpDetails .dpd-tog'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{ document.addEventListener('click', e=>{ if(e.target.closest && e.target.closest('#detailPoster .s2-ech')){ closeAll(); setTimeout(()=>closeAll(), 1000); } }, true); }")
    ok = choisit(pg, '#detailPoster', 'AVANT', '1 sem.'); pg.wait_for_timeout(1200); e = pg.evaluate(ET); R = pg.evaluate("()=>window._peaufRefus||[]")
    juge('D · un choix dont le geste mène à une fermeture générale (sur le coup et 1 s après) : Peaufiner reste ouvert sur la fiche', ok and e['peauf'] and e['fiche'] and not e['toile'], e['vus'])
    juge('D · chaque refus est gardé avec sa pile (et part au Mac avec ?mesure=1)', len(R) >= 2 and all(r.get('pile') for r in R[-2:]), '%d refus · %s' % (len(R), (R[-1]['pile'][:120] if R else '')))
    # F · le bandeau n'est pas un mur : une rangée réservée qui passe SOUS le bandeau ne répond pas au doigt qui touche le bandeau
    #   (le test du mur acceptait tout ce qui est dans la même fiche : toucher le bandeau, Peaufiner ouvert, faisait monter « Eh non. Mais avec
    #   Ma Parole !, oui. » et, la toute première fois, l'offre s'ouvrait seule — pris par redteam_fiches_theme)
    print('── F · le bandeau n\'est pas un mur')
    sous = pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, c=document.getElementById('dpdCorps'), y=D.top+802*k;
      for(const m of document.querySelectorAll('#detailPoster .s2-cercle:not(.v16-seul)')){ const q=m.getBoundingClientRect(); if(!q.height) continue; c.scrollTop+=(q.top+q.height/2)-y;
        const r=m.getBoundingClientRect(); if(r.top<=y-4 && r.bottom>=y+4){ const h=document.elementFromPoint(D.left+195*k, y); return {mur:(m.querySelector('.s2-lab')||m).textContent.trim().slice(0,30), sous:h?(h.id||h.className):null}; } }
      return null; }"""); pg.wait_for_timeout(400)
    m0 = pg.evaluate("()=>localStorage.getItem('promi_murs')")
    B.tap(pg, 195, 802); pg.wait_for_timeout(1200)
    f = pg.evaluate("()=>{ const m=document.getElementById('murPhrase'); const c=m?getComputedStyle(m):null; return {phrase:(m&&c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.1)?(m.textContent||'').slice(0,40):null, murs:localStorage.getItem('promi_murs')}; }")
    juge('F · Peaufiner ouvert, une rangée réservée sous le bandeau : toucher le bandeau ne fait monter aucune phrase de mur', bool(sous) and not f['phrase'] and f['murs'] == m0, 'mur sous le bandeau : %s · phrase %s · compteur %s → %s' % (sous, f['phrase'], m0, f['murs']))
    pg.wait_for_timeout(5500); e = pg.evaluate(ET)
    juge('F · … et l\'offre ne s\'ouvre pas d\'elle-même', not e['offre'], e['vus'])
    if not e['peauf']: B.tap_sel(pg, '#dpDetails .dpd-tog'); pg.wait_for_timeout(1100)
    # E · les sorties voulues : l'offre par-dessus, puis supprimer
    print('── E · les sorties voulues')
    m = pg.evaluate(RANG, ['#detailPoster', 'RÉCURRENCE'])
    if m:
        B.tap(pg, m[0], m[1]); pg.wait_for_timeout(900); B.tap(pg, 195, 420); pg.wait_for_timeout(1500); e1 = pg.evaluate(ET)
        c = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const x=document.querySelector('#plusScreen.show [data-close], #plusScreen.show .closeb'); if(!x) return null; const q=x.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k, (q.top+q.height/2-D.top)/k]; }")
        if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(1300)
        e2 = pg.evaluate(ET)
        juge('E · un mur de Peaufiner : l\'offre s\'ouvre PAR-DESSUS ; refermée, Peaufiner est là, sur la même fiche', e1['offre'] and e2['peauf'] and e2['fiche'] and e2['cur'] == T and not e2['offre'], 'offre %s → %s' % (e1['offre'], e2['vus']))
    pg.evaluate("()=>{ const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(400)
    n0 = pg.evaluate("()=>promises.length"); B.tap_sel(pg, '#detailPoster .s2-reg.v16-danger'); pg.wait_for_timeout(900)
    cf = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const x=document.querySelector('#v16Conf .v16-oui'); if(!x) return null; const q=x.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k, (q.top+q.height/2-D.top)/k, x.textContent.trim().slice(0,30)]; }")
    if cf: B.tap(pg, cf[0], cf[1]); pg.wait_for_timeout(1500)
    e = pg.evaluate(ET); n1 = pg.evaluate("()=>promises.length")
    juge('E · « Supprimer ce Promi » reste une sortie : la parole est retirée, la fiche se referme', n1 == n0 - 1 and not e['fiche'], '%d → %d paroles · confirmation %s · %s' % (n0, n1, cf and cf[2], e['vus']))
    juge('A–E · aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close()
    # B · la page +
    print('── B · la page +, plusieurs choix d\'affilée, avec Ma Parole !')
    ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F); pg.evaluate("()=>setPremium(true)"); page(pg); e0 = pg.evaluate(ET)
    juge('B · Peaufiner s\'ouvre sur la page +', e0['plus'] and e0['ppeauf'], e0['vus'])
    for lab, t in (('AVANT', '1 sem.'), ('AVANT', '1 mois'), ('LA COULEUR', 'couleur 2')):
        ok = choisit(pg, '#createSheet', lab, t); e = pg.evaluate(ET)
        lu = pg.evaluate("(t)=>{ const e=[...document.querySelectorAll('#createSheet .s2-reg .chip, #createSheet .s2-reg .cc-ton')].find(x=>(x.getAttribute('aria-label')||x.textContent||'').trim()===t); return e?(e.classList.contains('on')||e.getAttribute('aria-pressed')==='true'||e.classList.contains('choisi')||e.classList.contains('sel')):null; }", t)
        juge('B · « %s » → « %s » : appliqué (le choix est marqué), Peaufiner reste ouvert sur la page +, pas la Toile' % (lab, t), ok and lu and e['plus'] and e['ppeauf'] and not e['toile'], 'marqué %s · %s' % (lu, e['vus']))
    pg.evaluate("()=>{ const c=document.querySelector('#createSheet > .dpd-corps'); if(c) c.scrollTop=0; }"); pg.wait_for_timeout(300)
    B.glisse(pg, B.droite([195, 180], [195, 400], 14), pas=16); pg.wait_for_timeout(1000); e = pg.evaluate(ET)
    juge('C · page + : un glissement de 220 pt vers le bas referme Peaufiner et rend la page + — jamais la Toile', not e['ppeauf'] and e['plus'] and not e['toile'], e['vus'])
    B.capture(pg, 'planche-v146/peaufiner-sortie-plus.png')
    juge('B · aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close(); b.close()
print('\n  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
