#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES FONCTIONS DE PEAUFINER SONT-ELLES INTACTES ?
   Un écran qui se superpose au moodboard mais qui ne fait plus rien est un faux vert.
   On vérifie au doigt : la barre ouvre et referme, chaque réglage déplie SON contrôle
   d'app (celui d'avant, déplacé — pas un neuf), la note s'écrit et se garde, les
   pastilles d'échéance répondent, et aucun nœud n'est perdu entre deux ouvertures."""
from playwright.sync_api import sync_playwright
R = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OK, KO = [], []


def t(nom, cond, det=''):
    (OK if cond else KO).append('%-52s %s' % (nom, det))


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []
    pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('file://' + R + '/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pid = pg.evaluate("""()=>{var p=promises.filter(q=>!q.draft&&q.status==='encours')[0];
        delete p.chiche; p.who='Rachel'; p.note=''; openDetail(p.id); return p.id;}""")
    pg.wait_for_timeout(1500)

    # 1 · la barre ouvre la page
    pg.evaluate("()=>{document.querySelector('#dpDetails .dpd-tog').click();}")
    pg.wait_for_timeout(800)
    t('la barre ouvre la page', pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('s2-ouv')"))
    t('la liste est bâtie', pg.evaluate("()=>!!document.querySelector('#dpdCorps .s2-liste')"))

    # 2 · chaque contrôle de l'app est DANS un réglage, pas perdu
    for cid in ('dWhoInput', 'mgDueChips', 'dNueeChips', 'dNote', 'dpFilesPromi', 'dCommentInput'):
        t('le contrôle #%s vit dans un réglage' % cid,
          pg.evaluate("(i)=>{var e=document.getElementById(i);return !!(e&&e.closest('.s2-reg'));}", cid))

    # 3 · un réglage se déplie et montre son contrôle
    pg.evaluate("""()=>{var e=[...document.querySelectorAll('.s2-reg')]
        .filter(x=>x.querySelector('#mgDueChips'))[0]; if(e) e.click();}""")
    pg.wait_for_timeout(400)
    t('le réglage AVANT déplie ses pastilles',
      pg.evaluate("()=>{var e=document.getElementById('mgDueChips');if(!e)return false;"
                  "var r=e.getBoundingClientRect();return r.height>4&&r.width>4;}"))

    # 4 · la note s'écrit et se garde dans la donnée
    pg.evaluate("()=>{var n=document.getElementById('dNote'); n.value='essai de note'; "
                "n.dispatchEvent(new Event('input',{bubbles:true})); n.dispatchEvent(new Event('change',{bubbles:true})); n.blur();}")
    pg.wait_for_timeout(600)
    t('la note atteint la donnée',
      pg.evaluate("(i)=>{var p=promises.filter(q=>q.id===i)[0];return p&&(p.note||'').indexOf('essai')>=0;}", pid),
      str(pg.evaluate("(i)=>{var p=promises.filter(q=>q.id===i)[0];return p?p.note:null;}", pid)))

    # 5 · l'échéance répond
    av = pg.evaluate("()=>{var v=[...document.querySelectorAll('.s2-reg')].filter(x=>x.querySelector('.s2-lab')&&x.querySelector('.s2-lab').textContent.trim()==='AVANT')[0];return v?v.querySelector('.s2-val').textContent.trim():null;}")
    # LA LISTE UNIQUE (S3/Q28) : « +1 sem. » n'existe plus — on choisit « 2 semaines »,
    # par sa prise data-d, jamais par son libellé.
    pg.evaluate("()=>{var b=document.querySelector('#mgDueChips [data-d=\"14\"]'); if(b) b.click();}")
    pg.wait_for_timeout(900)
    av2 = pg.evaluate("()=>{var v=[...document.querySelectorAll('.s2-reg')].filter(x=>x.querySelector('.s2-lab')&&x.querySelector('.s2-lab').textContent.trim()==='AVANT')[0];return v?v.querySelector('.s2-val').textContent.trim():null;}")
    t('la pastille « 2 semaines » change la valeur AVANT', av != av2, '%s -> %s' % (av, av2))

    # 6 · on referme, on rouvre : rien n'est perdu
    pg.evaluate("()=>{document.querySelector('#dpDetails .dpd-tog').click();}"); pg.wait_for_timeout(600)
    t('la barre referme la page', not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('s2-ouv')"))
    pg.evaluate("()=>{document.querySelector('#dpDetails .dpd-tog').click();}"); pg.wait_for_timeout(800)
    for cid in ('dWhoInput', 'mgDueChips', 'dNote', 'dCommentInput', 'dpFilesPromi', 'dNueeChips'):
        t('après un aller-retour, #%s existe encore' % cid,
          pg.evaluate("(i)=>!!document.getElementById(i)", cid))
    t('la note écrite est toujours dans le champ',
      pg.evaluate("()=>{var n=document.getElementById('dNote');return n&&(n.value||'').indexOf('essai')>=0;}"))

    # 7 · le rond Partager garde sa fonction (il n'ouvre pas la page)
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(false);}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{var s=document.querySelector('#dpDetails .dpd-part'); if(s) s.click();}")
    pg.wait_for_timeout(900)
    t('le rond Partager n\'ouvre pas Peaufiner',
      not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('s2-ouv')"))

    # 8 · la Nuée : bouton et dissolution branchés
    pg.evaluate("()=>{var c=document.querySelector('#detailPoster>.closeb'); if(c) c.click();}")
    pg.wait_for_timeout(700)
    pg.evaluate("()=>{var k=null; for(var q in NUE){k=q;break;} openNueeDetail(k);}")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{if(window._s2Ouvre) window._s2Ouvre(true);}"); pg.wait_for_timeout(700)
    t('la Nuée montre le bouton de plantation',
      pg.evaluate("()=>{var b=document.querySelector('#dpdCorps .s2-bouton');return !!b&&b.textContent.indexOf('Planter')>=0;}"))
    t('la Nuée garde son contrôle de dissolution',
      pg.evaluate("()=>!!document.getElementById('nqDissolve')"))
    t('la description de Nuée vit dans un réglage',
      pg.evaluate("()=>{var e=document.getElementById('nqNote');return !!(e&&e.closest('.s2-reg'));}"))

    # 9 · les Réglages généraux : le bloc du Cercle est bâti, l'encart reste cliquable
    pg.evaluate("()=>{var c=document.querySelector('#detailPoster>.closeb'); if(c) c.click();}")
    pg.wait_for_timeout(600)
    pg.evaluate("()=>{document.getElementById('settingsScreen').classList.add('show');}")
    pg.wait_for_timeout(900)
    t('Réglages : le bloc du Cercle est bâti',
      pg.evaluate("()=>{var c=document.querySelector('#settingsScreen .s2-cercle');"
                  "return !!c && c.querySelectorAll('.s2-reg').length===4;}"))
    t('Réglages : l\'encart du Cercle est dedans, net',
      pg.evaluate("()=>{var e=document.getElementById('openPlusTop');"
                  "return !!(e&&e.parentNode.classList.contains('s2-cercle')&&getComputedStyle(e).filter==='none');}"))

    if er:
        KO.append('ERREURS JS : ' + ' | '.join(er[:3]))
    b.close()

for x in OK:
    print('  OK  ' + x)
for x in KO:
    print('  KO  ' + x)
print('\n%d/%d' % (len(OK), len(OK) + len(KO)))
