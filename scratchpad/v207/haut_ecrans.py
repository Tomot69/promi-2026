# C-299 : sur chaque écran, ce qui PEINT un contenu (texte, filet, fond d'encart, image) dans les 66 premiers points de l'appareil (390 × 844), à fit 1
import sys, os, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html'); LIM=float(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--lim=')), '66'))
src = open('redteam_app.py', encoding='utf-8').read()
ns = {'VITE': False}; exec(re.search(r'(def ecrans\(pg\):.*?return L\n)', src, re.S).group(1), ns); ecrans = ns['ecrans']
INS=next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ins=')), '47,0,34,0')
PLEIN="window.__zsInsets=["+INS+"]; document.addEventListener('DOMContentLoaded',function(){ var st=document.createElement('style'); st.textContent='.frame{padding:0!important;--fit:1!important}#device{border-radius:0!important;box-shadow:none!important}'; document.head.appendChild(st); document.documentElement.style.setProperty('--zs-haut','47px'); });"
SONDE="""(lim)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, out=[];
  for(const e of document.querySelectorAll('#device *, .frame > *:not(#device) *, body > *')){ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) continue; const y0=(r.top-D.top)/k, y1=(r.bottom-D.top)/k, x0=(r.left-D.left)/k, x1=(r.right-D.left)/k;
    if(y0>=lim || y1<=0 || x1<=0 || x0>=390) continue; const c=getComputedStyle(e); if(c.visibility==='hidden'||c.display==='none') continue; let op=1,a=e; while(a&&a!==document.body){ op*=parseFloat(getComputedStyle(a).opacity); a=a.parentElement; } if(op<0.05) continue;
    const texte=[...e.childNodes].some(n=>n.nodeType===3&&n.data.trim()); const bord=parseFloat(c.borderTopWidth)>0&&c.borderTopStyle!=='none'; const bg=c.backgroundColor!=='rgba(0, 0, 0, 0)'&&c.backgroundColor!=='transparent';
    const grand=(x1-x0)>370&&(y1-y0)>300;   /* un fond plein écran : pas un contenu */
    if(grand) continue; if(!(texte||bord||e.tagName==='svg'||e.tagName==='IMG'||(bg&&(y1-y0)<200)||e.tagName==='CANVAS')) continue;
    out.push((e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className).trim().split(/\\s+/).slice(0,2).join('.'))+' '+Math.round(y0)+'→'+Math.round(y1)+(texte?' « '+e.textContent.trim().slice(0,18)+' »':'')); }
  return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=390, vh=844); B.toile_pleine(ctx, 10); ctx.add_init_script(PLEIN); pg = B.ouvre(ctx, F)
    for nom, js in ecrans(pg):
        pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ closeAll(); }catch(e){} document.querySelectorAll('#auraScreen.show .closeb, #studioScreen.show .closeb').forEach(x=>{ try{x.click()}catch(e){} }); }"); pg.wait_for_timeout(700)
        try: pg.evaluate(js)
        except Exception as e: print('  !', nom, str(e)[:100])
        pg.wait_for_timeout(2400)
        L=pg.evaluate(SONDE, LIM); L=[x for x in L if 'v187Bande' not in x]; print('==', nom, len(L), 'zs-dy', pg.evaluate("()=>getComputedStyle(document.documentElement).getPropertyValue('--zs-dy')")); [print('    ', x) for x in L[:8]]
    b.close()
