"""v211 C-307 — relevé des titres d'encart : taille, largeur, place avant le X ; la taille max de chacun. python3 scratchpad/v211_titres.py [--vue=1|079] [--fichier=]"""
import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
V = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--vue=')), '1')
exec(open('scratchpad/v210/encart.py', encoding='utf-8').read().split('REL = ')[0].split('PAGES = ')[1].join(['PAGES = ', '']) if False else '')
src = open('scratchpad/v210/encart.py', encoding='utf-8').read()
PAGES = eval(src.split('PAGES = ')[1].split('\nREL')[0])
FERME = src.split("pg.evaluate(\"()=>{ try{ if(window._peaufSortie)")[1].split('\n')[0]
FERME = "()=>{ try{ if(window._peaufSortie)" + FERME.rsplit('")', 1)[0]
PAGES = [('accueil', "()=>{}")] + PAGES + [('fiche promi', "()=>{ const p=promises.find(x=>!x.draft&&!x.nuee&&!x.chiche); openDetail(p.id); }"), ('page +', "()=>{ document.getElementById('createBtn').click(); setTimeout(()=>document.querySelector('#accChoix .acc-pil[data-k=promi]').click(),600); }")]
MES = r"""()=>{ const dev=document.getElementById('device').getBoundingClientRect(), k=dev.width/390;
 const top=document.elementFromPoint(dev.left+195*k, dev.top+70*k);
 let enh=top && (top.closest('.enh')||top.closest('#stpHaut')||top.closest('.acc-plat')||top.closest('#detailPoster')||top.closest('#createSheet'));
 let t=null, x=null;
 if(enh && enh.classList.contains('acc-plat')){ t=enh.querySelector('.acc-mm'); x=document.getElementById('shareBtn'); }
 else if(enh && enh.id==='detailPoster'){ t=document.getElementById('dptNat'); x=enh.querySelector('.closeb'); }
 else if(enh && enh.id==='createSheet'){ t=enh.querySelector('.cs-mark'); x=enh.querySelector('.closeb'); }
 else if(enh){ t=enh.querySelector('.enh-t,.stp-t'); x=enh.querySelector('.closeb'); }
 if(!t) return {enh:enh&&(enh.id||enh.className)};
 const c=getComputedStyle(t), g=document.createRange(); g.selectNodeContents(t); const ri=g.getBoundingClientRect(), rx=x?x.getBoundingClientRect():null;
 const fs=parseFloat(c.fontSize), w=ri.width/k, zl=rx?(rx.left-dev.left)/k:null, tl=(ri.left-dev.left)/k;
 return {page:(t.closest('[id]')||{}).id, texte:t.textContent.trim(), fs:fs, fam:c.fontFamily.split(',')[0], w:+w.toFixed(2), tl:+tl.toFixed(2), zl:zl&&+zl.toFixed(2), dispo:zl&&+(zl-tl-4).toFixed(2), max:zl&&+(fs*(zl-tl-4)/w).toFixed(2), lignes:Math.round(ri.height/k/(parseFloat(c.lineHeight)||fs*1.06))}; }"""
res = {}
with sync_playwright() as p:
    b = p.webkit.launch(); vw, vh = (430, 932) if V == '1' else (330, 714)
    ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    for nom, js in PAGES:
        pg.evaluate(FERME); pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(2600)
        res[nom] = pg.evaluate(MES); print('%-16s %s' % (nom, res[nom]), flush=True)
    b.close()
json.dump(res, open('scratchpad/v211_titres-%s.json' % V, 'w'), ensure_ascii=False, indent=1)
