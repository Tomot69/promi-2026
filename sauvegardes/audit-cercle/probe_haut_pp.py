# CHANTIER 64 — ce qui est peint dans le HAUT du Peaufiner : page + contre fiche (qui n'a pas le défaut), nœud par nœud.
from playwright.sync_api import sync_playwright
J = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, H=document.querySelector(hote); const out=[];
  H.querySelectorAll('*').forEach(e=>{ if(!e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return; const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return;
    const y=(r.top-dv.top)/s; if(y>150 || y+r.height/s<0) return;
    const own=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()); const k=getComputedStyle(e);
    const bord=parseFloat(k.borderTopWidth)>0&&k.borderTopStyle!=='none'; const fond=k.backgroundColor!=='rgba(0, 0, 0, 0)';
    if(!own && !bord && e.tagName!=='CANVAS' && !e.matches('.enh,.closeb,.ph-photo-btn,.s2-tete')) return;
    out.push({el:(e.id?'#'+e.id:'')+'.'+String(e.className).split(' ').slice(0,3).join('.'), tag:e.tagName, txt:own?e.textContent.trim().slice(0,30):'', r:[Math.round((r.left-dv.left)/s),Math.round(y),Math.round(r.width/s),Math.round(r.height/s)], bord, fond, z:k.zIndex, parent:(e.parentElement.id||String(e.parentElement.className).split(' ')[0])}); });
  return out; }"""
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('dark')")
    pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
    print('== page + AU REPOS (avant Peaufiner)'); [print('  ', x) for x in pg.evaluate(J, '#createSheet')]
    pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1800)
    print('== page + · PEAUFINER'); [print('  ', x) for x in pg.evaluate(J, '#createSheet')]
    pg.locator('#device').screenshot(path='bandeau/pp_peauf_haut_avant64.png')
    pg.evaluate(BASE); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1400)
    pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
    print('== fiche · PEAUFINER (la référence)'); [print('  ', x) for x in pg.evaluate(J, '#detailPoster')]
    pg.locator('#device').screenshot(path='bandeau/fiche_peauf_haut.png')
    br.close()
