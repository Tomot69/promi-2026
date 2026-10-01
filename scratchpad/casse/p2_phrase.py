# -*- coding: utf-8 -*-
"""PASSE 2 — le vrai chemin : je touche un mot de la phrase, un panneau s'ouvre,
   j'écris. Est-ce que ça marche ?"""
import sys
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from lib import *
from playwright.sync_api import sync_playwright

ETAT = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const b=e=>{if(!e)return null;const r=e.getBoundingClientRect();
    return Math.round((r.left-dev.left)/sc)+','+Math.round((r.top-dev.top)/sc)+' '
          +Math.round(r.width/sc)+'x'+Math.round(r.height/sc);};
  const v=e=>{if(!e)return 'ABSENT';const c=getComputedStyle(e);
    return (c.display==='none'?'display:none':(c.visibility==='hidden'?'hidden':'visible'))+' '+b(e);};
  return {
    csChoix: v(document.getElementById('csChoix')),
    csChoixCls: (document.getElementById('csChoix')||{}).className,
    saisie: [...document.querySelectorAll('#csChoix input,#csChoix textarea,#createSheet input:not([type=file])')]
      .map(e=>'#'+(e.id||e.name||'?')+' '+v(e)+' val="'+(e.value||'')+'"'),
    phrase: (document.querySelector('.pp-phrase')||{textContent:''}).textContent.trim().replace(/\s+/g,' '),
    _phrase: JSON.stringify(window._phrase||null),
    fTitle: v(document.getElementById('fTitle')),
    fWho:   v(document.getElementById('fWho')),
  };}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto(URL); pg.wait_for_timeout(6800); pg.evaluate(PREP)
    pg.click('#createBtn'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0]; if(t)t.click();}")
    pg.wait_for_timeout(1000)

    print('les mots de la phrase, et ce qu\'ils ouvrent :')
    mots=pg.evaluate("""()=>[...document.querySelectorAll('#csPhrase [data-ph],.pp-phrase [data-ph]')]
      .map(e=>e.getAttribute('data-ph')+' « '+(e.textContent||'').trim()+' »')""")
    for m in mots: print('   ', m)

    for cle in ('titre','qui','quand'):
        print('\n════ je touche le mot « %s » ════'%cle)
        pg.evaluate("""(k)=>{const e=document.querySelector('#csPhrase [data-ph='+k+'],.pp-phrase [data-ph='+k+']');
          if(e)e.click();}""", cle)
        pg.wait_for_timeout(1000)
        e=pg.evaluate(ETAT)
        print('   #csChoix        :', e['csChoix'], '|', e['csChoixCls'])
        print('   champs de saisie:', e['saisie'] if e['saisie'] else 'AUCUN')
        # j'essaie d'écrire, comme un utilisateur
        ok=pg.evaluate("""()=>{const e=[...document.querySelectorAll('#csChoix input,#csChoix textarea')]
            .filter(x=>getComputedStyle(x).display!=='none' && x.getBoundingClientRect().width>4)[0];
          if(!e) return 'AUCUN CHAMP ATTEIGNABLE';
          e.focus(); e.value='la Bretagne';
          e.dispatchEvent(new Event('input',{bubbles:true}));
          e.dispatchEvent(new Event('change',{bubbles:true}));
          return 'écrit dans #'+(e.id||'?');}""")
        print('   écriture        :', ok)
        pg.wait_for_timeout(700)
        e2=pg.evaluate(ETAT)
        print('   la phrase dit   :', e2['phrase'][:90])
        print('   _phrase         :', (e2['_phrase'] or '')[:120])
        print('   #fTitle / #fWho :', e2['fTitle'], '/', e2['fWho'])
        r=pg.evaluate(CHEVAUCHE,'#createSheet')
        for s in r['sup'][:6]: print('   SUPERPOSE  ', s)
        for d in r['deb'][:4]: print('   DEBORDE    ', d)
    print('\nERREURS JS :', er[:4])
    b.close()
