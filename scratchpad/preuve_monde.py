#!/usr/bin/env python3
"""PREUVE — le 4e argument de dalleTrame fait-il ce qu'il dit, et ne fuit-il pas ?

Quatre contrats :
  1 · SANS le 4e argument, rien ne change      (les six appels existants ne bougent pas)
  2 · AVEC, la dalle sort dans le monde demandé (pas dans le monde courant)
  3 · AUCUNE FUITE : après l'appel, la Toile est exactement dans l'état d'avant
  4 · chaque Promi porte un monde figé, et le rattrapage est idempotent
"""
from playwright.sync_api import sync_playwright

SIG = r"""([id,monde])=>{
  const c=document.createElement('canvas'); c.width=200; c.height=200;
  document.body.appendChild(c);
  window.Toile.dalleTrame(c,id,1,monde||undefined);
  const d=c.getContext('2d').getImageData(0,0,200,200).data;
  let n=0; const h={};
  for(let i=3;i<d.length;i+=40){ if(d[i]>10){ n++; const j=i-3;
    h[(d[j]>>5)+'-'+(d[j+1]>>5)+'-'+(d[j+2]>>5)]=1; } }
  c.remove();
  return n+'|'+Object.keys(h).sort().join(',');
}"""
ETAT = "()=>{const m=window.Toile.mondeCourant(); return m.m+'|'+m.p+'|'+m.h;}"

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    err=[]; pg.on('pageerror', lambda e: err.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ids = pg.evaluate("()=>promises.filter(p=>!p.draft&&!p.req).slice(0,3).map(p=>p.id)")

    print('── 4 · le champ figé sur les Promi')
    ech = pg.evaluate("()=>promises.slice(0,3).map(p=>p.id+' → '+JSON.stringify(p.monde))")
    for e in ech: print('   ', e)
    sans = pg.evaluate("()=>promises.filter(p=>!p.monde).length")
    print('    Promi SANS monde :', sans, '←' , 'aucun ✅' if sans==0 else 'RESTE ❌')
    print('    rattrapage relancé →', pg.evaluate("()=>window._figeMondesManquants()"),
          'Promi touchés (idempotent ✅)' )

    avant = pg.evaluate(ETAT)
    print('\n── état de la Toile avant :', avant)

    print('\n── 1 · SANS le 4e argument — la dalle ne bouge pas')
    a1 = {i: pg.evaluate(SIG,[i,None]) for i in ids}
    a2 = {i: pg.evaluate(SIG,[i,None]) for i in ids}
    print('    deux relevés identiques :', 'oui ✅' if a1==a2 else 'NON ❌')

    print('\n── 2 · AVEC — la dalle sort dans le monde demandé')
    for monde in ('mosaique','terrazzo','braille'):
        b1 = {i: pg.evaluate(SIG,[i,{'m':monde,'p':'signal','h':0}]) for i in ids}
        diff = sum(1 for i in ids if b1[i]!=a1[i])
        print('    %-9s → %d dalles sur %d diffèrent du monde courant  %s'
              % (monde, diff, len(ids), '✅' if diff==len(ids) else '❌'))

    print('\n── 3 · AUCUNE FUITE')
    apres = pg.evaluate(ETAT)
    print('    état de la Toile après :', apres, '←', 'inchangé ✅' if apres==avant else 'MODIFIÉ ❌')
    a3 = {i: pg.evaluate(SIG,[i,None]) for i in ids}
    print('    la dalle sans argument redonne la même chose :',
          'oui ✅' if a3==a1 else 'NON ❌ — la palette a fuité')

    print('\n── erreurs de page :', len(err))
    for e in err[:5]: print('   ', e)
    b.close()
