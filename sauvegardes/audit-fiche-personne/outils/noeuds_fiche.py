# L'INVENTAIRE COMPLET, nœud par nœud — tous les descendants de #personSheet, VISIBLES OU NON, avec leur valeur :
# quatre personnes (Marion, Rachel, moi, une personne sans Promi), en gratuit puis en Cercle FORCÉ (le mode perdu :
# on pose `premium` sur #device ET `device premium` sur .frame, le temps d'une page jetée, pour voir ce qu'il porterait).
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
INV = r"""()=>{ const sh=document.getElementById('personSheet'), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, out=[];
  const chemin=(e)=>{ const p=[]; for(let x=e; x&&x!==sh; x=x.parentElement) p.unshift(x.id?'#'+x.id:x.tagName.toLowerCase()+(x.classList.length?'.'+[...x.classList].slice(0,2).join('.'):'')); return p.join('>'); };
  for(const e of sh.querySelectorAll('*')){ const c=getComputedStyle(e), r=e.getBoundingClientRect();
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
    const vu=c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.01&&r.width>1&&r.height>1;
    let cache='' ; if(!vu){ for(let x=e; x&&x!==sh.parentElement; x=x.parentElement){ const cx=getComputedStyle(x); if(cx.display==='none'){cache='display:none sur '+(x.id||x.className); break;} if(cx.visibility==='hidden'){cache='visibility sur '+(x.id||x.className); break;} } if(!cache) cache=(r.width<=1||r.height<=1)?'0×0':'opacité'; }
    const clic=!!(e.onclick||e.getAttribute('onclick')||e.hasAttribute('data-close')||e.hasAttribute('data-id')||e.hasAttribute('data-p')||c.cursor==='pointer');
    out.push({n:chemin(e), txt:txt.slice(0,90), vu:vu, cache:cache, prem:!!e.closest('.prem-only')||e.classList.contains('kr-eux'), clic:clic, cls:String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).slice(0,40),
      box:vu?[Math.round((r.left-dv.left)/s),Math.round((r.top-dv.top)/s),Math.round(r.width/s),Math.round(r.height/s)]:null}); }
  return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    R = {}
    for mode in ('gratuit', 'cercle'):
        for nom in ('Marion', 'Rachel', 'moi', 'Zoé'):
            pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            pg.goto(URL); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            if mode == 'cercle':
                pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} document.getElementById('device').classList.add('premium'); const f=document.querySelector('.frame'); if(f){ f.classList.add('device'); f.classList.add('premium'); } }")
            pg.evaluate("(n)=>{closeAll(); openPerson(n);}", nom); pg.wait_for_timeout(1500)
            inv = pg.evaluate(INV); R['%s-%s' % (mode, nom)] = inv
            if nom in ('Marion', 'moi'):
                dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
                pg.screenshot(path=os.path.join(OUT, 'noeuds-%s-%s.png' % (mode, nom)), clip={'x': dev[0], 'y': dev[1], 'width': dev[2], 'height': dev[3]})
            vis = [x for x in inv if x['vu'] and (x['txt'] or x['clic'])]
            print('\n=== %s · %s : %d nœuds, %d visibles' % (mode, nom, len(inv), sum(1 for x in inv if x['vu'])))
            for x in inv:
                if x['txt'] or x['clic'] or x['prem'] or x['n'].endswith(('canvas.kr-c', 'svg')):
                    print('  %s %s%s %-58s %s%s' % ('●' if x['vu'] else '○', 'C' if x['prem'] else '·', 'T' if x['clic'] else '·', x['n'][-58:], ('« %s »' % x['txt']) if x['txt'] else '', '' if x['vu'] else '   [caché : %s]' % x['cache']))
            pg.close()
    json.dump(R, open(os.path.join(OUT, 'noeuds.json'), 'w'), ensure_ascii=False, indent=1)
    b.close()
