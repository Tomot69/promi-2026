# -*- coding: utf-8 -*-
"""LA LISTE UNIQUE DE L'ÉCHÉANCE (S3/Q28) — elle est branchée, pas recréée, et elle obéit
   aux trois règles : « repousser » a disparu · « un jour » et « en l'air » restent deux
   valeurs distinctes · sans choix explicite, aucune pastille active."""
from playwright.sync_api import sync_playwright
R = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OK, KO = [], []
def t(n, c, d=''): (OK if c else KO).append('%-58s %s' % (n, d))

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('file://'+R+'/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pid = pg.evaluate("""()=>{var p=promises.filter(q=>!q.draft&&q.status==='encours')[0];
        delete p.chiche; p.who='Rachel'; delete p.enLair; delete p.dueChoisi; p.due=3;
        openDetail(p.id); return p.id;}""")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(true);}"); pg.wait_for_timeout(800)
    mots = pg.evaluate("()=>[...document.querySelectorAll('#mgDueChips button')].map(b=>b.textContent.trim())")
    t('la liste unique est posée', mots == ['un jour','en l’air','demain','5 jours','2 semaines','ce mois-ci','une date précise…'], str(mots))
    t("le mot « repousser » a disparu", not any('repouss' in m for m in mots), str([m for m in mots if 'repouss' in m]))
    t('chaque pastille a une prise (data-q ou data-d ou datepick)',
      pg.evaluate("""()=>[...document.querySelectorAll('#mgDueChips button')]
        .every(b=>b.hasAttribute('data-q')||b.hasAttribute('data-d')||b.hasAttribute('data-datepick'))"""))
    t('sans choix explicite, aucune pastille active',
      pg.evaluate("()=>[...document.querySelectorAll('#mgDueChips button.on')].length")==0,
      str(pg.evaluate("()=>[...document.querySelectorAll('#mgDueChips button.on')].map(b=>b.textContent.trim())")))
    # choisir « en l'air »
    pg.evaluate("()=>{var b=document.querySelector('#mgDueChips [data-q=lair]'); if(b) b.click();}")
    pg.wait_for_timeout(700)
    d1 = pg.evaluate("(i)=>{var p=promises.filter(q=>q.id===i)[0];return {due:p.due, enLair:!!p.enLair};}", pid)
    t("« en l'air » : due null ET le drapeau enLair", d1=={'due':None,'enLair':True}, str(d1))
    # choisir « un jour »
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(true);}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{var b=document.querySelector('#mgDueChips [data-q=jour]'); if(b) b.click();}")
    pg.wait_for_timeout(700)
    d2 = pg.evaluate("(i)=>{var p=promises.filter(q=>q.id===i)[0];return {due:p.due, enLair:!!p.enLair};}", pid)
    t("« un jour » : due null SANS le drapeau — les deux ne fusionnent pas",
      d2=={'due':None,'enLair':False} and d1!=d2, '%s vs %s' % (d1, d2))
    # une date en jours
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(true);}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{var b=document.querySelector('#mgDueChips [data-d=\"14\"]'); if(b) b.click();}")
    pg.wait_for_timeout(700)
    d3 = pg.evaluate("(i)=>{var p=promises.filter(q=>q.id===i)[0];return {due:p.due, enLair:!!p.enLair};}", pid)
    t('« 2 semaines » : due = 14, drapeau retombé', d3=={'due':14,'enLair':False}, str(d3))
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(true);}"); pg.wait_for_timeout(600)
    t('le choix courant est marqué',
      pg.evaluate("()=>{var b=document.querySelector('#mgDueChips button.on');return b?b.textContent.trim():null;}")=='2 semaines',
      str(pg.evaluate("()=>{var b=document.querySelector('#mgDueChips button.on');return b?b.textContent.trim():null;}")))
    if er: KO.append('ERREURS JS : '+' | '.join(er[:3]))
    b.close()
for x in OK: print('  OK  '+x)
for x in KO: print('  KO  '+x)
print('\n%d/%d' % (len(OK), len(OK)+len(KO)))
