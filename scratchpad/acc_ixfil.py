import json
from playwright.sync_api import sync_playwright
INV=r"""(root)=>{const R=document.querySelector(root);const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;const o=[];
R.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);if(r.width<3||r.height<3||c.display==='none'||c.visibility==='hidden'||+c.opacity<.05)return;
const y=(r.top-D.top)/k;if(y>330||y<0)return;const own=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
if(!own&&!e.id&&!['INPUT','BUTTON','CANVAS'].includes(e.tagName))return;
const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
o.push([e.tagName,e.id,(e.className+'').slice(0,24),own.slice(0,30),+((r.left-D.left)/k).toFixed(0),+y.toFixed(0),+(r.width/k).toFixed(0),+(r.height/k).toFixed(0),c.fontFamily.split(',')[0]+' '+c.fontSize+'/'+c.fontWeight,c.borderTopWidth+' r'+c.borderTopLeftRadius,!!t&&(t===e||e.contains(t))]);});return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    pg=ctx.new_page(); pg.goto("http://127.0.0.1:8752/app.html"); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
    clip={'x':D[0],'y':D[1],'width':390*D[2],'height':844*D[2]}
    out={}
    for th in ['light','dark']:
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(800)
        pg.locator('#viewSwitch button[data-view=index]').tap(); pg.wait_for_timeout(1800)
        out['index_'+th]=pg.evaluate(INV,'#indexSheet'); pg.screenshot(path='scratchpad/acc_index_%s.png'%th,clip=clip)
        out['index_n_'+th]=pg.evaluate("()=>document.querySelectorAll('#indexSheet .s4-carte').length")
        pg.evaluate("()=>quitteVues()"); pg.wait_for_timeout(900)
        pg.locator('#filBtn').tap(); pg.wait_for_timeout(1800)
        out['fil_'+th]=pg.evaluate(INV,'#feedView'); pg.screenshot(path='scratchpad/acc_fil_%s.png'%th,clip=clip)
        out['fil_n_'+th]=pg.evaluate("()=>[...document.querySelectorAll('#feedList > *')].filter(e=>e.offsetHeight>20).length")
        pg.evaluate("()=>{setView('toile');quitteVues();}"); pg.wait_for_timeout(900)
    out['liens']=pg.evaluate("()=>['fdIdxBtn','filIdxRow','ixToFeed','ixSortChev','feedScreen'].map(i=>{const e=document.getElementById(i);return [i,!!e,e?(e.offsetWidth>0):null]})")
    json.dump(out,open('scratchpad/acc_ixfil.json','w'),ensure_ascii=False,indent=0)
    for k,v in out.items():
        print('==',k)
        if isinstance(v,list):
            for r in v: print('  ',r)
        else: print('  ',v)
    b.close()
