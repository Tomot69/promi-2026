# -*- coding: utf-8 -*-
"""LE FIL APRÈS UNE PAROLE TENUE — au vrai chemin de l'app (`#segStatus`, la fiche)."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
SUF = sys.argv[2] if len(sys.argv)>2 else ''
Q=r"""()=>{var dv=document.getElementById('device').getBoundingClientRect(),sc=dv.width/390;
 var c=document.querySelector('#feedView .s4-carte'); if(!c) return null;
 var o={};
 ['.s4-natlab','.s4-ev','.s4-ti','.s4-et'].forEach(function(s){
   var e=c.querySelector(s); if(!e){o[s]='(absent)';return;}
   var r=e.getBoundingClientRect();
   o[s]={t:(e.textContent||'').trim(), y:+((r.top-dv.top)/sc).toFixed(0), b:+((r.bottom-dv.top)/sc).toFixed(0)};});
 var cv=c.querySelector('canvas');
 if(cv){try{var g=cv.getContext('2d'),d=g.getImageData(0,0,cv.width,cv.height).data,n=0;
   for(var k=3;k<d.length;k+=200) if(d[k]>10) n++;
   o.dalle=n;}catch(e){o.dalle='KO';}} else o.dalle=null;
 var rc=c.getBoundingClientRect(); o.carte={y:+((rc.top-dv.top)/sc).toFixed(0), h:+(rc.height/sc).toFixed(0)};
 return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    # on tient une parole PAR LE CHEMIN DE L'APP : on ouvre une fiche et on passe l'état à « tenu »
    r=pg.evaluate("""()=>{for(var i=1;i<=220;i++){try{var q=promises.filter(function(z){return z.id===i;})[0];
      if(q&&!q.draft&&q.status!=='tenu'&&!q.nuee&&(q.title||'').length>18){ openDetail(i); return {id:q.id,t:q.title}; }
    }catch(e){}} return null;}""")
    pg.wait_for_timeout(1800)
    pg.evaluate("()=>{var b=document.querySelector('#segStatus button[data-st=tenu]'); if(b) b.click();}")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3000)
    o=pg.evaluate(Q)
    print('parole tenue :', r)
    if not o: print('pas de carte'); raise SystemExit
    print('carte 1 · %s'%o['carte'])
    for k in ('.s4-natlab','.s4-ev','.s4-ti','.s4-et'):
        v=o[k]
        print('   %-12s %s'%(k, ('« %s » · y %s→%s'%(v['t'][:40],v['y'],v['b'])) if isinstance(v,dict) else v))
    print('   dalle        %s échantillons peints'%o['dalle'])
    # les contrats
    ev,ti,et = o['.s4-ev'],o['.s4-ti'],o['.s4-et']
    ok=[]
    ok.append(('la ligne 2 porte LE TITRE, pas un id ni une phrase', isinstance(ti,dict) and ti['t'] and not ti['t'].isdigit() and 'Tu as tenu' not in ti['t']))
    ok.append(('la ligne 1 porte l\'événement, sans le titre entre guillemets', isinstance(ev,dict) and ev['t'] and '«' not in ev['t']))
    ok.append(('les trois lignes ne se chevauchent pas', isinstance(ev,dict) and isinstance(ti,dict) and isinstance(et,dict) and ev['b']<=ti['y']+0.5 and ti['b']<=et['y']+0.5))
    ok.append(('la carte garde ses 128 de haut', o['carte']['h']==128))
    ok.append(('la dalle est peinte', isinstance(o['dalle'],int) and o['dalle']>200))
    print()
    for n,v in ok: print('   %-58s %s'%(n,'OK ' if v else 'KO'))
    print('\n%d/%d'%(sum(1 for _,v in ok if v), len(ok)))
    pg.locator('#device').screenshot(path='cap/fil-tenu%s.png'%SUF)
    b.close()
