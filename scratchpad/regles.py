# Les règles qui ÉCRIVENT réellement une propriété sur un nœud (CDP) : python3 regles.py "<ouvrir>" "<sélecteur>" prop1,prop2
import sys
from playwright.sync_api import sync_playwright
OUV, SEL, PROPS = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(400)
    pg.evaluate(OUV); pg.wait_for_timeout(2800)
    pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].find(x=>x.getBoundingClientRect().height>0); if(e) e.setAttribute('data-sonde','1');}", SEL)
    cdp=ctx.new_cdp_session(pg); cdp.send('DOM.enable'); cdp.send('CSS.enable'); doc=cdp.send('DOM.getDocument',{'depth':-1})
    nid=cdp.send('DOM.querySelector',{'nodeId':doc['root']['nodeId'],'selector':'[data-sonde]'})['nodeId']
    m=cdp.send('CSS.getMatchedStylesForNode',{'nodeId':nid})
    inl=m.get('inlineStyle',{}).get('cssProperties',[])
    for pp in inl:
        if pp['name'] in PROPS: print('  EN LIGNE', pp['name'], pp['value'])
    for r in m['matchedCSSRules']:
        props=[pp for pp in r['rule']['style']['cssProperties'] if pp['name'] in PROPS and pp.get('value')]
        if props: print('  ', r['rule']['selectorList']['text'][:110], '|', '; '.join('%s:%s'%(pp['name'],pp['value']) for pp in props))
    print('  CALCULÉ', pg.evaluate("(pr)=>{const e=document.querySelector('[data-sonde]'); const c=getComputedStyle(e); return pr.map(x=>x+'='+c.getPropertyValue(x));}", PROPS))
    b.close()
