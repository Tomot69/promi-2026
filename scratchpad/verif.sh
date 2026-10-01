python3 -c "
import re,io,os; S=io.open('app.html',encoding='utf-8').read()
[os.remove('scratchpad/chk/'+f) for f in os.listdir('scratchpad/chk')]
for i,m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>',S,re.S)): io.open('scratchpad/chk/%03d.js'%i,'w',encoding='utf-8').write(m.group(1))
"
for f in scratchpad/chk/*.js; do node --check "$f" 2>&1 | head -3; done
[ -f promi-moteur.js ] && node --check promi-moteur.js
python3 - <<'P'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for eng in (p.webkit,p.chromium):
        b=eng.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        print(eng.name,'erreurs',errs[:4],'toile',pg.evaluate("()=>[Toile.count(),Toile.getTheme(),typeof render]"))
        b.close()
P
