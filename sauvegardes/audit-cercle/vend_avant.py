# L'ÉCRAN QUI VEND, TEL QU'IL EST (avant le lot) : captures haut / bas, deux thèmes, et le contraste du prix et des boutons
# (rapport WCAG, et écart de luminosité du §3) — mesuré sur les couleurs CALCULÉES, fond effectif compris.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'vend')
CONTR = r"""()=>{ const lum=(c)=>{ const m=c.match(/[\d.]+/g).map(Number); const f=v=>{v/=255; return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);}; return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]); };
  const fond=(e)=>{ let x=e; while(x){ const b=getComputedStyle(x).backgroundColor; const a=(b.match(/[\d.]+/g)||[]).map(Number); if(a.length>=3 && (a.length<4 || a[3]>0.5)) return b; x=x.parentElement; } return 'rgb(255,255,255)'; };
  const out=[]; ['#buyMonth','#buyYear','#buyYear span','.pl-sub','.pl-sub b','.pl-h','.pl-note'].forEach(s=>{ document.querySelectorAll('#plusScreen '+s).forEach((e,i)=>{
    const k=getComputedStyle(e); const c=k.webkitTextFillColor&&k.webkitTextFillColor!=='rgba(0, 0, 0, 0)'?k.webkitTextFillColor:k.color; const f=fond(e);
    const L1=lum(c), L2=lum(f); const r=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05); const rc=e.getBoundingClientRect();
    out.push({sel:s+(i?'#'+i:''), texte:e.textContent.trim().slice(0,50), couleur:c, fond:f, rapport:+r.toFixed(2), op:k.opacity, x:Math.round(rc.left), y:Math.round(rc.top), w:Math.round(rc.width)}); }); });
  return out; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{ closeAll(); document.getElementById('cercleTopBtn').click(); }"); pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(OUT, 'avant_%s_haut.png' % th), clip=pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}"))
        R[th] = pg.evaluate(CONTR)
        pg.evaluate("()=>{const s=document.getElementById('plusScreen'); s.scrollTop=s.scrollHeight;}"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, 'avant_%s_bas.png' % th), clip=pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}"))
        print('==', th)
        for m in R[th]: print('   %-14s %-50s %5.2f  op %s  %s sur %s' % (m['sel'], m['texte'], m['rapport'], m['op'], m['couleur'], m['fond']))
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'contrastes_avant.json'), 'w'), ensure_ascii=False, indent=1)
