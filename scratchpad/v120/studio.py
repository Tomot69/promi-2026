# Le Studio au doigt : chaque élément interactif visible est-il sous le doigt, répond-il ? + capture.  usage: studio.py <fichier> <etiquette> [query]
import sys, json
from playwright.sync_api import sync_playwright
F=sys.argv[1]; TAG=sys.argv[2]; Q=sys.argv[3] if len(sys.argv)>3 else ''
INV = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const S=document.getElementById('studioScreen'); const out=[];
  const els=[...S.querySelectorAll('button,[role=button],[role=switch],.stp-d,.stp-ton,.orb,[data-pal],[data-tx],[data-th],[onclick],.stp-fl,.stp-dot')];
  for(const e of els){ const r=e.getBoundingClientRect(); if(r.width<6||r.height<6) continue; const cx=r.left+r.width/2, cy=r.top+r.height/2;
    if(cx<dv.left||cx>dv.right||cy<dv.top||cy>dv.bottom) continue; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<.05) continue;
    const t=document.elementFromPoint(cx,cy); out.push({id:e.id||'', cls:(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'').toString().slice(0,40), tx:(e.textContent||'').trim().slice(0,18), x:Math.round(cx-dv.left), y:Math.round(cy-dv.top), w:Math.round(r.width), h:Math.round(r.height),
      joint: !!t && (t===e||e.contains(t)||t.contains(e)), dessus: t? (t.id||t.className||t.tagName).toString().slice(0,40):'rien', bg:cs.backgroundColor, bgi:(cs.backgroundImage||'').slice(0,60)}); }
  return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}")
        pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/'+F+Q); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setTheme(t)}catch(e){}}",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*STUDIO\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}")
        pg.wait_for_timeout(3500)
        inv=pg.evaluate(INV); nj=[e for e in inv if not e['joint']]
        print('== %s %s%s [%s] : %d éléments, %d NON joignables, erreurs %s, thème rendu %s' % (TAG,F,Q,th,len(inv),len(nj),er[:2], pg.evaluate("()=>document.documentElement.className+' | zzz='+(window._zzz&&_zzz.etat?JSON.stringify(_zzz.etat()):'?')")))
        for e in nj: print('   ✗', e['id'] or e['cls'], repr(e['tx']), (e['x'],e['y']), 'dessus:', e['dessus'])
        pal=[e for e in inv if 'ton' in e['cls'] or 'orb' in e['cls'] or 'pal' in e['cls']]
        print('   palettes:', len(pal), 'fonds vides:', sum(1 for e in pal if e['bg'] in ('rgba(0, 0, 0, 0)','transparent') and e['bgi'] in ('none','')))
        pg.screenshot(path='scratchpad/v120/studio-%s-%s.png'%(TAG,th), clip={'x':20,'y':44,'width':390,'height':844})
        json.dump(inv, open('scratchpad/v120/studio-%s-%s.json'%(TAG,th),'w'), ensure_ascii=False)
        ctx.close()
    b.close()
