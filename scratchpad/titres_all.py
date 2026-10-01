# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
ECR=[('accueil',"()=>{closeAll();}"),('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}"),
     ('index',"()=>{closeAll(); document.getElementById('indexBtn').click();}"),
     ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('aide-aura',"()=>{closeAll(); document.getElementById('souffleBtn').click(); setTimeout(()=>{const b=document.getElementById('auraInfoBtn'); b&&b.click();},900);}"),
     ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}"),
     ('reglages',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}"),
     ('langue',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click(); setTimeout(()=>{const l=document.getElementById('openLang')||document.querySelector('[data-go=lang]'); l&&l.click();},900);}"),
     ('partage',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click();}"),
     ('nuee',"()=>{closeAll(); const k=Object.keys(NUE||{})[0]; window.openNueeDetail(k);}"),
     ('fiche',"()=>{closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee)[0].id);}")]
JS=r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const fr=document.querySelector('.frame').getBoundingClientRect();
  const out=[], vus=new Set();
  document.querySelectorAll('h1,h2,.scr-t,.scr-ti,.enh-t,.acc-mm').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<10||r.height<8) return;
    const y=(r.top-fr.top)/s; if(y<5||y>160) return;
    const cs=getComputedStyle(e); const t=(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,18);
    if(!t||vus.has(t)) return; vus.add(t);
    out.push({t:t, fs:cs.fontSize, ff:cs.fontFamily.split(',')[0].replace(/["']/g,''),
      cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ').join('.')).slice(0,34)});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR:
        try: pg.evaluate(js)
        except Exception: continue
        pg.wait_for_timeout(2400)
        for o in pg.evaluate(JS):
            mark='' if o['ff']=='PromiLate' and o['fs']=='27px' else '   <<<<'
            print('%-10s %-20s %-7s %-11s %s%s' % (nom, o['t'], o['fs'], o['ff'], o['cl'], mark))
    b.close()
