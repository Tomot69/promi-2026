# -*- coding: utf-8 -*-
"""PASSE 7 — les GESTES qui comptent : planter, tenir. Et les écrans non portés."""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

def trace(pg, sel, y=None):
    """je trace au doigt, comme un utilisateur"""
    r=pg.evaluate("""(s)=>{const e=document.querySelector(s);if(!e)return null;
      const b=e.getBoundingClientRect();return {x:b.left,y:b.top,w:b.width,h:b.height};}""", sel)
    if not r: return 'ZONE ABSENTE'
    yy = r['y']+r['h']/2 if y is None else y
    pg.mouse.move(r['x']+12, yy); pg.mouse.down()
    for i in range(1,26):
        pg.mouse.move(r['x']+12+(r['w']-24)*i/25, yy+(6 if i%2 else -6)); pg.wait_for_timeout(12)
    pg.mouse.up(); pg.wait_for_timeout(1200)
    return 'tracé'

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)

    print('═══ TENIR UNE PAROLE AU GESTE, sur une fiche à tenir ═══')
    pid=pg.evaluate("()=>(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0]||{}).id")
    pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}",pid); pg.wait_for_timeout(1600)
    avant=pg.evaluate("(i)=>promises.find(p=>p.id===i).status",pid)
    print('   zone du geste :', pg.evaluate("""()=>{const z=document.getElementById('tenirZone');
      if(!z)return 'ABSENTE';const c=getComputedStyle(z);const b=z.getBoundingClientRect();
      const dev=document.getElementById('device').getBoundingClientRect();const sc=dev.width/390;
      return c.display+'/'+c.pointerEvents+' @'+Math.round((b.left-dev.left)/sc)+','
        +Math.round((b.top-dev.top)/sc)+' '+Math.round(b.width/sc)+'x'+Math.round(b.height/sc);}"""))
    print('   je trace      :', trace(pg,'#tenirCv'))
    apres=pg.evaluate("(i)=>promises.find(p=>p.id===i).status",pid)
    print('   statut : %s → %s   %s'%(avant,apres,'✓ tenue' if apres=='tenu' else '✗ RIEN NE SE PASSE'))

    print('\n═══ PLANTER UN PROMI depuis la page + ═══')
    n0=pg.evaluate("()=>promises.length")
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
    pg.click('#createBtn'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1000)
    pg.evaluate("""()=>{const e=document.querySelector('[data-ph=titre]');if(e)e.click();}"""); pg.wait_for_timeout(800)
    pg.evaluate("""()=>{const e=[...document.querySelectorAll('#csChoix input,#csChoix textarea')]
        .filter(x=>x.getBoundingClientRect().width>4)[0];
      if(e){e.focus();e.value='aller voir la mer';e.dispatchEvent(new Event('input',{bubbles:true}));}}""")
    pg.wait_for_timeout(900)
    print('   la phrase montre-t-elle « aller voir la mer » ?',
      pg.evaluate("""()=>((document.querySelector('.pp-phrase')||{textContent:''}).textContent||'')
        .includes('aller voir la mer')"""))
    print('   je trace pour planter :', trace(pg,'#planterCv') if pg.evaluate("()=>!!document.getElementById('planterCv')") else 'PAS DE #planterCv')
    n1=pg.evaluate("()=>promises.length")
    print('   Promi : %d → %d   %s'%(n0,n1,'✓ planté' if n1>n0 else '✗ RIEN N\'EST PLANTÉ'))
    print('   #addPromi atteignable ?', pg.evaluate("""()=>{const b=document.getElementById('addPromi');
      if(!b)return 'ABSENT';const c=getComputedStyle(b);const r=b.getBoundingClientRect();
      return c.display+' '+Math.round(r.width)+'x'+Math.round(r.height);}"""))

    print('\n═══ LES ÉCRANS NON PORTÉS — sont-ils intacts ? ═══')
    for nom,js,sel in (('AURA',"()=>{if(window.closeAll)closeAll();document.getElementById('souffleBtn').click();}",'#auraScreen'),
                       ('STUDIO',"()=>{if(window.closeAll)closeAll();document.getElementById('studioBtn').click();}",'#studioScreen'),
                       ('PARTAGE',"()=>{if(window.closeAll)closeAll();document.getElementById('shareBtn').click();}",'#shareScreen')):
        pg.evaluate(js); pg.wait_for_timeout(1600)
        vu=pg.evaluate("(s)=>{const e=document.querySelector(s);return e?getComputedStyle(e).display+'/'+(e.className||''):'ABSENT';}",sel)
        r=pg.evaluate(CHEVAUCHE,sel)
        print('   %-8s %s   superpositions=%d débordements=%d'%(nom,vu[:46],len(r['sup']),len(r['deb'])))
        for s in r['sup'][:4]: print('        SUPERPOSE ',s)
        for d in r['deb'][:3]: print('        DEBORDE   ',d)
    print('\nERREURS JS :', er[:6])
    b.close()
