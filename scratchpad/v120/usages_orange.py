# tous les usages RENDUS de #DD4D23 (rgb 221,77,35), écran par écran, deux thèmes — nœuds (styles calculés) et canevas (couleur dominante)
import re, io, json
from playwright.sync_api import sync_playwright
J=io.open('redteam_couleurs_ref.py',encoding='utf-8').read()
COLLECTE=re.search(r'COLLECTE = r"""(.*?)"""',J,re.S).group(1)
src=io.open('redteam_air.py',encoding='utf-8').read()
ECRANS=[(m.group(1),m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$",src,re.M)]
vu={}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t)}",th); pg.wait_for_timeout(600)
        for nom,js in ECRANS:
            try:
                pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(350)
                pg.evaluate(js); pg.wait_for_timeout(3000); R=pg.evaluate(COLLECTE)
            except Exception as ex: continue
            for k,o in R['n'].items():
                for pr,v in o.items():
                    if pr!='mot' and isinstance(v,str) and re.search(r'221, 77, 35',v):
                        cle=(re.sub(r' \[\d+\]$','',k),pr); vu.setdefault(cle,{'ecrans':set(),'mot':o.get('mot','')})['ecrans'].add('%s[%s]'%(nom,th[0]))
            for k,c in R['c'].items():
                for col in c['dom']:
                    if abs(col[0]-221)<=2 and abs(col[1]-77)<=2 and abs(col[2]-35)<=2:
                        vu.setdefault((k,'canevas %.0f %%'%(100*col[3])),{'ecrans':set(),'mot':''})['ecrans'].add('%s[%s]'%(nom,th[0]))
    b.close()
out=[]
for (k,pr),d in sorted(vu.items()):
    out.append('%-74s %-14s %-22s %s'%(k[:74],pr,repr(d['mot'])[:22],', '.join(sorted(d['ecrans']))[:150]))
io.open('planche-v120/usages-DD4D23-rendus.txt','w',encoding='utf-8').write('\n'.join(out)); print('\n'.join(out)); print(len(out))
