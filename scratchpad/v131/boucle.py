import re, io, base64
from playwright.sync_api import sync_playwright
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
PIEGE=re.search(r'G2_PIEGE = r"""(.*?)"""', S, re.S).group(1).replace("window.__g2.push({", "window.__g2.push({url:(100*au/n>0.3?dcv.toDataURL():null), ")
ns={}; exec(re.search(r'(G2_ECRANS = \[.*?\]\n)', S, re.S).group(1), ns); ECR=ns['G2_ECRANS']
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch()
    for essai in range(50):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','light')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/zz-v130.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{Toile.setPalette&&Toile.setPalette('signal')}catch(e){}}")
        pg.evaluate(PIEGE)
        for m in ('pixel','braille','mosaique','gravure','sillons'):
            pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m); window.__g2m=m; window.__g2.length=0;}", m); pg.wait_for_timeout(2500)
            for nom,js in ECR:
                pg.evaluate("(n)=>{window.__g2e=n}", nom); pg.evaluate(js); pg.wait_for_timeout(2600)
            R=[r for r in pg.evaluate("()=>window.__g2.filter(r=>r.monde===Toile.getTheme())") if r['autres']>0.3]
            for i,r in enumerate(R):
                print('essai',essai,m,r['ecran'],r['autres'],r.get('qui'),flush=True)
                if r.get('url'): open('scratchpad/v131/pris-%d-%s-%d.png'%(essai,m,i),'wb').write(base64.b64decode(r['url'].split(',')[1]))
        print('essai',essai,'fini',flush=True); ctx.close()
    b.close()
