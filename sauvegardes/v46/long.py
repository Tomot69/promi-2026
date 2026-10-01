# Un titre long : la page + après validation (les trois natures), et la fiche. Mesure : rien ne sort de #device.
import sys
from playwright.sync_api import sync_playwright
T=([a for a in sys.argv[1:] if not a.startswith('--')] or ["réparer enfin le vieux vélo bleu de grand-père avant les vacances d'été prochaines"])[0]
SORT=r"""(sel)=>{ const d=document.getElementById('device').getBoundingClientRect(); const out=[];
  document.querySelectorAll(sel).forEach(e=>{ const r=e.getBoundingClientRect(); if(r.width<1) return; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none') return;
    if(r.right>d.right+0.5||r.left<d.left-0.5) out.push((e.id||e.className).toString().slice(0,30)+' '+Math.round(r.left-d.left)+'→'+Math.round(r.right-d.left)+' / '+Math.round(d.width)); });
  return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nat in ['promi','chiche']:
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click();}"); pg.wait_for_timeout(1200)
        pg.locator('[data-kind=%s]'%nat).first.tap(); pg.wait_for_timeout(1500)
        pg.locator('#csPhrase [data-ph=titre]').first.tap(); pg.wait_for_timeout(600)
        pg.keyboard.type(T, delay=5); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
        print(nat, 'page + : hors écran', pg.evaluate(SORT, '#createSheet *'))
        pg.locator('#device').screenshot(path='sauvegardes/v46/long_%s.png'%nat)
    # la fiche : un Promi du jeu, titre remplacé
    pg.evaluate("(t)=>{ closeAll(); const p=promises.filter(q=>!q.draft&&!q.nuee)[0]; p.title=t; openDetail(p.id); }", T); pg.wait_for_timeout(1800)
    print('fiche : hors écran', pg.evaluate(SORT, '#detailPoster *'))
    pg.locator('#device').screenshot(path='sauvegardes/v46/long_fiche.png')
    b.close()
