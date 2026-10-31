#!/usr/bin/env python3
"""redteam_deux_etats.py — ⚑ v173b (Tom, C-210) : DEUX ÉTATS AU LIEU DE TROIS, UN SEUL ORANGE.

« L'état « à tenir » est supprimé ; il ne reste que « en cours » et « tenu ». Tous les oranges de l'app reprennent EXACTEMENT #FB4C0D ; aucune variante dérivée ne reste.
La légende : ses pastilles deviennent des rectangles d'aperçu, de la hauteur d'une majuscule des mots de la légende. » Décisions sur l'étude (ETUDE-DEUX-ETATS.md) : D1 « Ma Parole ! »
en crème sur le Peaufiner d'un Promi seulement · D2 « À RELEVER » reste sur un Chiche reçu · D5 la date passée s'affiche comme une date, « 12 OCT. », sans « c'était », sans couleur.

Banc comme Tom (WebKit, 390 × 844 ×3, doigt) ; un état enregistré « comme sur un téléphone d'avant » : une parole `rate`, un Fil « … est à tenir », une date passée (`?jour=+30`).
  A · la migration : aucune parole `rate`, l'échéance gardée ; le Fil reformulé ; aucun écrivain (`rate` absent de l'état après un `?jour=+30`)
  B · date passée : la parole reste « en cours » ; la carte d'Index et la fiche disent « EN COURS · <jour> <MOIS>. » ; aucun « À TENIR », aucun « C'ÉTAIT » ; la couleur = celle d'une carte en cours
  C · Fil : TRACER · REPORTER sur la parole à date passée ; REPORTER remet la date, l'état ne bouge pas
  D · Index et Fil : plus de filtre « À tenir », ni de tri « À tenir en premier »
  E · les disques : deux arcs au plus (Noyaux, anneau du +) ; légende de l'Aura à deux entrées, deux chiffres ; l'aide dit deux états
  F · la légende : un rectangle de la hauteur d'une capitale de ses mots (± 0,6 pt, lue sur la mise en page ET l'encre mesurée), Aura, personne, aide ; deux thèmes
  G · un Chiche reçu dit « À RELEVER » (D2), un Chiche lancé « LANCÉ »
  H · les oranges : aucune valeur retirée dans le code exécuté (hexadécimal, triplet, rgb()), hors la rampe de la Pelote (D4) ; aucun style calculé sur 8 écrans
Preuve : `--fichier=zz-v172.html` rougit.
"""
import sys, re, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
MOIS = ['JANV.', 'FÉVR.', 'MARS', 'AVR.', 'MAI', 'JUIN', 'JUIL.', 'AOÛT', 'SEPT.', 'OCT.', 'NOV.', 'DÉC.']
AMORCE = """(()=>{ if(sessionStorage.getItem('__mig')){ try{ window.__ids=JSON.parse(sessionStorage.getItem('__mig')); }catch(e){} return; } const S=JSON.parse(localStorage.getItem('promi_state')); const P=S.promises.filter(p=>!p.draft);
  const a=P.find(p=>p.status==='encours'&&!p.chiche&&!p.req&&(!p.from||p.from==='moi')&&!p.nuee); a.title='arroser la serre'; a.status='rate'; a.due=-2; a.enLair=false; delete a.ech; delete a.dueISO;
  const c=P.find(p=>p!==a&&p.status==='encours'&&!p.nuee&&!p.req); c.title='sauter du plongeoir'; c.chiche=true; c.from='Marion'; c.who='moi'; delete c.chicheEtat; c.due=4; delete c.ech;
  S.FEED=S.FEED||[]; S.FEED.unshift({id:99001, type:'missed', text:'« arroser la serre » est à tenir', pid:a.id, t:'hier'});
  localStorage.setItem('promi_state', JSON.stringify(S)); window.__ids=[a.id, c.id]; sessionStorage.setItem('__mig', JSON.stringify(window.__ids)); })()"""
ROUGES = ['rgb(221, 77, 35)', 'rgb(255, 122, 85)', 'rgb(254, 208, 195)']
SCAN = """(R)=>{ const out=[]; document.querySelectorAll('#device *').forEach(e=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return; const c=getComputedStyle(e); if(c.visibility==='hidden'||c.display==='none') return;
    ['color','backgroundColor','borderTopColor','webkitTextFillColor'].forEach(k=>{ if(R.includes(c[k])) out.push((e.id||e.className||e.tagName)+' '+k); }); }); return out.slice(0,6); }"""
def carte(pg, titre):
    return pg.evaluate("""(t)=>{ const c=[...document.querySelectorAll('#indexList .s4-carte')].find(x=>(x.textContent||'').includes(t)); if(!c) return null; const e=c.querySelector('.s4-et'), s=getComputedStyle(e); return {et:e.textContent, col:s.color, etat:c.getAttribute('data-etat')}; }""", titre)
def ouvre_index(pg): pg.evaluate("()=>{ closeAll(); document.getElementById('indexBtn').click(); }"); pg.wait_for_timeout(1600)
def ouvre_fiche(pg, pid): pg.evaluate("(i)=>{ closeAll(); openDetail(i); }", pid); pg.wait_for_timeout(1500)
with sync_playwright() as p:
    b = p.webkit.launch()
    print('fichier :', F, '· charge %.1f' % B.charge())
    # ── les données d'un téléphone d'avant
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(AMORCE); pg = B.ouvre(ctx, F, attente=6500, q='?jour=+1')
    ids = pg.evaluate("()=>window.__ids")
    st = pg.evaluate("(i)=>{ const p=promises.find(x=>x.id===i); return {status:p.status, due:p.due, n:promises.filter(q=>q.status==='rate').length, f:(FEED.find(x=>x.id===99001)||{})}; }", ids[0])
    juge('A · migration : plus aucune parole `rate`, la date gardée', st['n'] == 0 and st['status'] == 'encours' and (st['due'] is not None and st['due'] < 0), st)
    t = st['f'].get('text', ''); juge('A · le Fil reformulé, sans « à tenir », avec la date', 'à tenir' not in t and bool(re.search(r'« arroser la serre » : \d+ [a-zéû.]+', t)) and st['f'].get('type') != 'missed', t)
    pg.evaluate("()=>{ if(window.saveState) saveState(); }")
    # date passée
    ouvre_index(pg); c = carte(pg, 'arroser la serre'); r = carte(pg, 'courir') or carte(pg, 'nager')
    m = re.fullmatch(r'EN COURS · \d+ (%s)' % '|'.join(re.escape(x) for x in MOIS), (c or {}).get('et', ''))
    juge('B · carte : « EN COURS · <date> », à la couleur d\'une carte en cours, sans « À TENIR » ni « C\'ÉTAIT »', bool(m) and c['etat'] == 'encours', c)
    tx = pg.evaluate("()=>document.getElementById('indexList').textContent")
    juge('B · aucun « À TENIR » dans l\'Index', 'À TENIR' not in tx.upper() or 'à tenir' not in tx.lower(), tx[:80])
    menus = pg.evaluate("()=>[...document.querySelectorAll('#ixMenu .ix-mi, #fdMenu .ix-mi')].map(e=>e.textContent)")
    juge('D · plus de filtre ni de tri « À tenir »', menus and not [x for x in menus if 'tenir' in x.lower() and 'tenue' not in x.lower()], [x for x in menus if 'tenir' in x.lower()])
    ouvre_fiche(pg, ids[0]); q = pg.evaluate("()=>{ const e=document.getElementById('dptQuand'), c=getComputedStyle(e); return {t:e.textContent, col:c.color}; }")
    juge('B · fiche : « EN COURS · <date> »', bool(re.fullmatch(r'EN COURS · \d+ (%s)' % '|'.join(re.escape(x) for x in MOIS), q['t'])) and q['col'] not in ROUGES, q)
    ouvre_fiche(pg, ids[1]); q2 = pg.evaluate("()=>document.getElementById('dptQuand').textContent")
    juge('G · un Chiche reçu dit « À RELEVER » (D2)', q2.startswith('À RELEVER'), q2)
    # Fil
    pg.evaluate("()=>{ closeAll(); document.getElementById('filBtn').click(); }"); pg.wait_for_timeout(1600)
    acts = pg.evaluate("(i)=>{ const f=FEED.find(x=>x.pid===i), c=(window._filComp||[]).filter(x=>x.pid===i).map(x=>JSON.stringify(x)).join(' '); return {c:c, fid:f.id}; }", ids[0])
    juge('C · Fil : TRACER · REPORTER sur la parole à date passée', 'TRACER' in acts['c'] and 'REPORTER' in acts['c'], acts)
    d = pg.evaluate("(a)=>{ _fpost(a[0], 3); const p=promises.find(x=>x.id===a[1]); return {status:p.status, due:p.due}; }", [acts['fid'], ids[0]])
    juge('C · REPORTER remet la date, l\'état ne bouge pas', d['status'] == 'encours' and d['due'] >= 0, d)
    # Aura
    pg.evaluate("()=>{ closeAll(); document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(2600)
    A = pg.evaluate("""()=>{ const S=document.getElementById('auraScreen'), arcs=[...S.querySelectorAll('.au-nb')].map(n=>new Set([...n.querySelectorAll('path.au-arc')].map(p=>p.getAttribute('stroke'))).size);
      const k=document.getElementById('device').getBoundingClientRect(), ech=k.width/390; const i=S.querySelector('.au-lg i'), s=S.querySelector('.au-lg span'), c=getComputedStyle(s), R=i.getBoundingClientRect(); const cv=document.createElement('canvas').getContext('2d'); cv.font=c.fontWeight+' '+c.fontSize+' '+c.fontFamily; const m=cv.measureText('H');
      return {arcs:arcs, lg:S.querySelectorAll('.au-lg span').length, cpt:S.querySelectorAll('.au-cpt span').length, tx:S.querySelector('.au-lg').textContent, h:R.height/ech, w:R.width/ech, cap:m.actualBoundingBoxAscent, ray:parseFloat(getComputedStyle(i).borderTopLeftRadius)}; }""")
    juge('E · Noyaux : deux couleurs d\'arc au plus ; légende et chiffres à deux entrées', A['arcs'] and max(A['arcs']) <= 2 and min(A['arcs']) >= 1 and A['lg'] == 2 and A['cpt'] == 2 and 'tenir' not in A['tx'].lower(), A)
    juge('F · légende de l\'Aura : un rectangle, hauteur d\'une capitale ± 0,6 pt', abs(A['h'] - A['cap']) <= 0.6 and A['w'] > A['h'] * 1.3 and A['ray'] < A['h'] / 2, 'rectangle %.1f × %.1f · capitale %.1f · rayon %.1f' % (A['w'], A['h'], A['cap'], A['ray']))
    ring = pg.evaluate("()=>{ closeAll(); const v=document.getElementById('createBtn').style.getPropertyValue('--kr-svg'); return decodeURIComponent(v); }")
    juge('E · l\'anneau du + : plus de troisième couleur', 'DD4D23' not in ring.upper(), len(ring))
    H = pg.evaluate("""()=>{ const h=document.getElementById('auraHelp'), l=h&&h.querySelector('.ah-legend'); if(!l) return null; h.classList.add('show'); const i=l.querySelector('i'), s=l.querySelector('span'), c=getComputedStyle(s), R=i.getBoundingClientRect(), k=document.getElementById('device').getBoundingClientRect().width/390, cv=document.createElement('canvas').getContext('2d'); cv.font=c.fontWeight+' '+c.fontSize+' '+c.fontFamily; const m=cv.measureText('H'); const o={n:l.querySelectorAll('span').length, h:R.height/k, cap:m.actualBoundingBoxAscent, txt:h.textContent.includes('à tenir')}; h.classList.remove('show'); return o; }""")
    juge('F · légende de l\'aide : deux entrées, un rectangle à la capitale ; l\'aide ne dit plus « à tenir »', H and H['n'] == 2 and abs(H['h'] - H['cap']) <= 0.6 and not H['txt'], H)
    # couleurs calculées sur quelques écrans
    bad = {}
    for nom, js in (('accueil', "closeAll()"), ('fiche', "openDetail(%d)" % ids[0]), ('peaufiner', "1"), ('index', "1")):
        if nom == 'index': ouvre_index(pg)
        else: pg.evaluate("()=>{ closeAll(); %s; }" % js); pg.wait_for_timeout(1000)
        x = pg.evaluate(SCAN, ROUGES)
        if x: bad[nom] = x
    juge('H · aucun style calculé aux valeurs retirées', not bad, bad)
    er = [e for e in pg.erreurs if 'version.json' not in e]; juge('aucune erreur de page', not er, er[:2]); ctx.close()
    # personne
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, attente=5000)
    Pp = pg.evaluate("""()=>{ closeAll(); openPerson('Marion'); return 1; }"""); pg.wait_for_timeout(1400)
    L = pg.evaluate("""()=>{ const l=document.querySelector('#psCadre .ps-lg'); if(!l) return null; const i=l.querySelector('i'), s=l.querySelector('span'), c=getComputedStyle(s), R=i.getBoundingClientRect(), k=l.closest('#device,.frame')?1:1, cv=document.createElement('canvas').getContext('2d'); cv.font=c.fontWeight+' '+c.fontSize+' '+c.fontFamily; const m=cv.measureText('H'); const r=document.getElementById('device').getBoundingClientRect().width/390; return {n:l.querySelectorAll('span').length, h:i.offsetHeight||R.height/r, cap:m.actualBoundingBoxAscent}; }""")
    juge('F · légende d\'une personne : deux entrées, un rectangle à la capitale', L and L['n'] == 2 and abs(L['h'] - L['cap']) <= 0.7, L)
    ctx.close(); b.close()
# ── la source
S = io.open(F, encoding='utf-8').read()
S2 = re.sub(r'/\*.*?\*/', '', S, flags=re.S)
reste = [m.group(0) for m in re.finditer(r'#DD4D23|#FF7A55|#FED0C3|#FF8664|#B8362D|\b221, ?77, ?35\b|\b255, ?122, ?85\b|\b254, ?208, ?195\b|orange53|orange-maparole-corps|orange-maparole-cobalt', S2, re.I)]
hors = [x for x in reste if x not in ('221,77,35',)]
ligne_d4 = S2.count('var ETATS=[[143,224,143],[221,77,35]]')
juge('H · la source : plus aucune valeur retirée dans le code, hors la rampe de la Pelote (D4)', not hors and len(reste) <= ligne_d4, 'trouvées %d (%s) · D4 %d' % (len(reste), sorted(set(reste))[:6], ligne_d4))
juge('A · plus aucun écrivain de `rate`', not re.search(r"status\s*=\s*'rate'|,\s*'rate'\s*[,)]", S2.replace("if(p && p.status==='rate') p.status='encours'", '')), '')
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
