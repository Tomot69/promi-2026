# node --check sur chaque <script>, puis chargement de la page et lecture de pageerror (WebKit)
import re,io,subprocess,sys,os
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'
S=io.open(f,encoding='utf-8').read(); ko=0
for i,m in enumerate(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>',S,re.S)):
    io.open('/tmp/_chk.js','w',encoding='utf-8').write(m.group(1))
    r=subprocess.run(['node','--check','/tmp/_chk.js'],capture_output=True,text=True)
    if r.returncode: ko+=1; print('script',i,r.stderr[:300])
print('node --check :', 'OK' if not ko else '%d KO'%ko)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(6000)
    print('pageerror :', er or 'aucune', '| auraErreur :', pg.evaluate("()=>window._auraErreur||null"), '|', pg.evaluate("()=>JSON.stringify(_aura.corps())"), pg.evaluate("()=>_aura.etat?JSON.stringify({p:_aura.etat().palier}):''"))
    b.close()
