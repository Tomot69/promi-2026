from playwright.sync_api import sync_playwright
CH=r"""(id)=>{const e=document.getElementById(id);
  if(!e) return 'ABSENT';
  let p=e.parentElement, ch=[];
  while(p && p!==document.body){ ch.push(p.id?('#'+p.id):('.'+(p.className+'').split(' ').filter(Boolean)[0])); p=p.parentElement; }
  return {chaine:ch.join(' < '), sousDevice: !!document.querySelector('#device #'+id),
          combien: document.querySelectorAll('#'+id).length};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('AU REPOS        detailPoster :', pg.evaluate(CH,'detailPoster'))
    print('AU REPOS        indexSheet   :', pg.evaluate(CH,'indexSheet'))
    pg.evaluate("()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}")
    pg.wait_for_timeout(1600)
    print('FICHE OUVERTE   detailPoster :', pg.evaluate(CH,'detailPoster'))
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1400)
    print('PEAUFINER OUVERT detailPoster:', pg.evaluate(CH,'detailPoster'))
    print('   .s2-cercle .s2-reg flou   :', pg.evaluate("""()=>{const e=document.querySelector('.s2-cercle .s2-reg');
      return e?getComputedStyle(e).filter:'ABSENT';}"""))
    print('   le sélecteur #device #detailPoster .s2-cercle .s2-reg touche :',
      pg.evaluate("()=>document.querySelectorAll('#device #detailPoster .s2-cercle .s2-reg').length"))
    pg.evaluate("()=>{if(window.closeAll)closeAll();ouvrirIndex();}"); pg.wait_for_timeout(1600)
    print('INDEX OUVERT    indexSheet   :', pg.evaluate(CH,'indexSheet'))
    b.close()
