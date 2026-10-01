# Le Peaufiner d'une Nuée, ouvert N fois de suite : quel constructeur, et la carte « LE TRAIT » porte-t-elle son rail ?
import sys
from playwright.sync_api import sync_playwright
APP=sys.argv[1] if len(sys.argv)>1 else 'app.html'
ETAT=r"""()=>{ const dp=document.getElementById('detailPoster'); const c=document.getElementById('npTrait');
  const l=dp.querySelector('.dpd-corps .s2-liste'); const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
  return {nuee:dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'), ouvert:!!(document.getElementById('dpDetails')||{}).classList&&document.getElementById('dpDetails').classList.contains('ouvert'),
    carte:vis(c), pastilles:c?c.querySelectorAll('.pc-t').length:-1, sig:c?c.getAttribute('data-sig'):null,
    liste:vis(l), rangee:!!document.getElementById('dpTraitReg')&&vis(document.getElementById('dpTraitReg')), rangeePast:document.querySelectorAll('#dpTraitReg .pc-t').length,
    peintes: c?[...c.querySelectorAll('.pc-t')].filter(t=>{const r=t.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); const e=t.querySelector('.pc-e'); return r.width>10&&r.height>10&&r.right>d.left&&r.left<d.right&&r.top<d.bottom&&r.bottom>d.top&&e&&e.innerHTML.length>20&&getComputedStyle(e).opacity!=='0';}).length:-1,
    carteBoite: c?(r=>[Math.round(r.top),Math.round(r.height)])(c.getBoundingClientRect()):null,
    vues: [...document.querySelectorAll('#dpdCorps > *')].filter(e=>getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>2).map(e=>e.id||e.className).slice(0,12)}; }"""
with sync_playwright() as p:
    for moteur in ('webkit',):
        b=getattr(p,moteur).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
        cdp=ctx.new_cdp_session(pg) if moteur=='chromium' else None
        pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for k in range(4):
            pg.evaluate("()=>{closeAll(); var k=null; for(var q in NUE){k=q;break;} openNueeDetail(k);}"); pg.wait_for_timeout(1500)
            xy=pg.evaluate("()=>{const b=document.querySelector('#dpDetails .dpd-tog'); if(!b) return null; const r=b.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}")
            if xy: pg.touchscreen.tap(*xy)
            pg.wait_for_timeout(1600)
            print(moteur, 'ouverture', k+1, pg.evaluate(ETAT), flush=True)
        b.close()
