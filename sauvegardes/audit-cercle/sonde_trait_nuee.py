# Où vit le TRAIT sur une fiche de Nuée (le mode complet du §2.6) ? Tous les canevas visibles et leurs cotes.
from playwright.sync_api import sync_playwright
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
J = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const L=[...document.querySelectorAll('#detailPoster canvas, #detailPoster [id*=tenir], #detailPoster [class*=trait], #detailPoster [class*=geste]')].map(e=>{ const r=e.getBoundingClientRect();
    return {el:(e.id?'#'+e.id:'')+'.'+String(e.className).split(' ').slice(0,2).join('.'), tag:e.tagName, vis:e.checkVisibility(),
            r:[Math.round((r.left-dv.left)/s), Math.round((r.top-dv.top)/s), Math.round(r.width/s), Math.round(r.height/s)]}; });
  return L.filter(x=>x.r[2]>2 && x.r[3]>2); }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('dark')")
    pg.evaluate(BASE); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1800)
    print('FICHE Promi :'); [print('   ', x) for x in pg.evaluate(J)]
    pg.evaluate(BASE); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(2000)
    print('FICHE Nuée :'); [print('   ', x) for x in pg.evaluate(J)]
    br.close()
