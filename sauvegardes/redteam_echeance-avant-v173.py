"""redteam_echeance.py — ⚑ v151 (Tom, C-160, Q544) : L'ÉCHÉANCE COMPTE ENFIN LES JOURS.

« L'échéance est une date comparée à aujourd'hui, dans Swift ET dès maintenant dans le prototype : une parole dont l'échéance est dépassée et qui
n'est pas tenue passe « à tenir ». Recalcul au lancement et à chaque retour au premier plan. Paramètre de test ?jour=+N. Juge : planter, ?jour=+30,
la parole est « à tenir » ; REPORTER la remet « en cours » ; tracer la rend « tenue ». »

Banc comme Tom (WebKit, 390 × 844, échelle 3, doigt, Toile vide, webdriver masqué) :
  A · planter « 1 sem. » par la page + : l'échéance est une DATE, aujourd'hui + 7 (AAAA-MM-JJ), la parole « en cours » (v163b, C-197 : « demain · 1 sem. · 1 mois »)
  B · ?jour=+30, rechargement : la parole est « à tenir » (statut, mot, carte de l'Index), 23 jours dépassés
  C · le Fil : l'appui maintenu sur son bandeau fait paraître REPORTER ; REPORTER « 1 sem. » → « en cours », échéance au 7e jour après aujourd'hui
  D · rechargé encore à ?jour=+30 : toujours « en cours », la date gardée
  E · tracer sur sa fiche la rend « tenue »
  F · le retour au premier plan recompte : une échéance passée pendant que l'app dormait la fait « à tenir » (visibilitychange)
  G · une parole sans date (« un jour ») ne passe jamais « à tenir », même à ?jour=+400
  H · ?jour n'est jamais mémorisé
Valeurs en dur (la décision, pas ce que l'app déclare). Preuve : `--fichier=zz-av150.html` rougit (A, B, C, F).
"""
import sys, datetime; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
URL = 'http://127.0.0.1:8752/' + F
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, d))
ETAT = """t=>{ const p=promises.find(x=>x.title===t); if(!p) return null;
  return {id:p.id, status:p.status, due:p.due, iso:(p.ech&&p.ech.iso)||null, mot:(window.motDuTemps?motDuTemps(p).mot:'')}; }"""
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }"
def jour(n): return (datetime.date.today() + datetime.timedelta(days=n)).isoformat()
def plante(pg, titre, d):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
    pg.evaluate("a=>{ document.getElementById('fTitle').value=a[0]; if(a[1]!=null){ const c=document.querySelector('#dueChips .chip[data-d=\"'+a[1]+'\"]'); c&&c.click(); } else { window._csEnLair=false; } }", [titre, d])
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2800)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)

with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    plante(pg, 'rendre le livre', 7); plante(pg, 'apprendre le piano', None)
    e = pg.evaluate(ETAT, 'rendre le livre')
    juge('A · planter « 1 sem. » : l\'échéance est une date, aujourd\'hui + 7, la parole « en cours »',
         e and e['status'] == 'encours' and e['iso'] == jour(7) and e['due'] == 7, str(e))

    pg.goto(URL + '?jour=+30'); pg.wait_for_timeout(6800)
    e = pg.evaluate(ETAT, 'rendre le livre')
    juge('B · ?jour=+30 : la parole est « à tenir » (statut et mot), 23 jours dépassés',
         e and e['status'] == 'rate' and e['mot'] == 'à tenir' and e['due'] == -23, str(e))
    pg.evaluate("()=>{ try{closeAll()}catch(e){} try{ ouvrirIndex(); }catch(e){} }"); pg.wait_for_timeout(2200)
    carte = pg.evaluate("t=>{ const c=[...document.querySelectorAll('#indexList .s4-carte')].find(c=>(c.textContent||'').indexOf(t)>=0); return c ? (c.textContent||'').replace(/\\s+/g,' ').trim() : null; }", 'rendre le livre')
    juge('B · la carte de l\'Index dit « À TENIR »', carte and 'tenir' in carte.lower(), (carte or '—')[:90])

    # C · le Fil, au doigt : l'appui maintenu, REPORTER, « 1 sem. »
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2200)
    rang = pg.evaluate("i=>{ const C=window._filComp||[]; const F=C.find(F=>F.pid===i); return F ? F.rang : null; }", e['id'] if e else -1)
    r = pg.evaluate("i=>{ const c=[...document.querySelectorAll('#feedList .s4-carte')][i]; if(!c) return null; c.scrollIntoView({block:'center'}); const b=c.getBoundingClientRect(); return [b.left+40, b.top+b.height/2]; }", rang) if rang is not None else None
    vu = 0
    if r:
        pg.wait_for_timeout(500)
        r = pg.evaluate("i=>{ const c=[...document.querySelectorAll('#feedList .s4-carte')][i]; const b=c.getBoundingClientRect(); return [b.left+40, b.top+b.height/2]; }", rang)
        B.glisse(pg, [r, [r[0] + 1, r[1]]], pas=20, tenue=760, appareil=False); pg.wait_for_timeout(900)
        vu = pg.evaluate("()=>[...document.querySelectorAll('#feedList [data-post],#feedList .fd-dec,#feedList .s4-acte:not(.fort)')].filter(e=>e.getBoundingClientRect().width>4 && /REPORTER/i.test(e.textContent||'')).length")
    juge('C · l\'appui maintenu sur son bandeau du Fil fait paraître REPORTER', vu > 0, 'rang %s · %d' % (rang, vu))
    if vu:
        q = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#feedList [data-post],#feedList .fd-dec,#feedList .s4-acte:not(.fort)')].find(e=>e.getBoundingClientRect().width>4 && /REPORTER/i.test(e.textContent||'')); const b=e.getBoundingClientRect(); return [b.left+b.width/2, b.top+b.height/2]; }")
        pg.touchscreen.tap(q[0], q[1]); pg.wait_for_timeout(700)
        q = pg.evaluate("()=>{ const t=document.getElementById('_toast'); if(!t) return null; const e=[...t.querySelectorAll('*')].find(x=>(x.textContent||'').trim()==='1 sem.' && x.children.length===0); if(!e) return null; const b=e.getBoundingClientRect(); return [b.left+b.width/2, b.top+b.height/2]; }")
        if q: pg.touchscreen.tap(q[0], q[1]); pg.wait_for_timeout(900)
        else: print('     (pas de « 1 sem. » dans le toast)')
    e = pg.evaluate(ETAT, 'rendre le livre')
    juge('C · REPORTER « 1 sem. » la remet « en cours », échéance au 7e jour après aujourd\'hui (+30)',
         e and e['status'] == 'encours' and e['due'] == 7 and e['iso'] == jour(37), str(e))

    pg.goto(URL + '?jour=+30'); pg.wait_for_timeout(6800)
    e = pg.evaluate(ETAT, 'rendre le livre')
    juge('D · rechargée à ?jour=+30 : toujours « en cours », la date gardée', e and e['status'] == 'encours' and e['iso'] == jour(37) and e['due'] == 7, str(e))

    # E · tracer sur sa fiche
    pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    if e: pg.evaluate("i=>openDetail(i)", e['id']); pg.wait_for_timeout(2800)
    z = pg.evaluate(ZONE, 'tenirZone')
    if z:
        y = z[1] + z[3] * 0.45
        B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(3200)
    e = pg.evaluate(ETAT, 'rendre le livre')
    juge('E · tracer sur sa fiche la rend « tenue »', e and e['status'] == 'tenu', str(e))

    # F · le retour au premier plan recompte (une échéance passée pendant que l'app dormait)
    pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    plante(pg, 'arroser les tomates', 1)
    av = pg.evaluate(ETAT, 'arroser les tomates')
    pg.evaluate("""()=>{ const p=promises.find(x=>x.title==='arroser les tomates'); if(!p||!p.ech) return;
      const d=new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate()+30-3); p.ech.iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
      Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'}); document.dispatchEvent(new Event('visibilitychange'));
      Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'visible'}); document.dispatchEvent(new Event('visibilitychange')); }""")
    pg.wait_for_timeout(600)
    ap = pg.evaluate(ETAT, 'arroser les tomates')
    juge('F · au retour au premier plan, une échéance passée entre-temps fait la parole « à tenir »',
         av and av['status'] == 'encours' and ap and ap['status'] == 'rate' and ap['due'] == -3, '%s → %s' % (av, ap))

    pg.goto(URL + '?jour=+400'); pg.wait_for_timeout(6800)
    e = pg.evaluate(ETAT, 'apprendre le piano')
    juge('G · une parole sans date (« un jour ») ne passe jamais « à tenir », même à ?jour=+400', e and e['status'] == 'encours' and e['due'] is None, str(e))
    k = pg.evaluate("()=>Object.keys(localStorage).filter(k=>/jour|decal/i.test(k)||/jour=/.test(localStorage.getItem(k)||''))")
    juge('H · ?jour n\'est jamais mémorisé', not k, str(k))
    # la vérification de version (v145) recharge, au retour au premier plan, une page dont le commit diffère de celui du serveur (arbre de travail
    # modifié pendant un lot) : sa requête annulée par ce rechargement n'est pas une faute de la page.
    err = [x for x in pg.erreurs if 'version.json' not in x]
    juge('aucune erreur de page', not err, str(err[:2]))
    b.close()

ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
