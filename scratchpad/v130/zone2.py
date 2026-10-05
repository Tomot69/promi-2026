import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; PERTE='--perte' in sys.argv
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:120])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    N="()=>({gl:document.querySelectorAll('#auBouleGL').length, canv:[...document.querySelectorAll('.au-bo canvas')].map(c=>c.id+':'+c.width).join(' '), etat:JSON.stringify(window._peloteGLEtat&&_peloteGLEtat()).slice(0,90), err:(window._peloteGLErreur||'').slice(0,80)})"
    def aura(n):
        pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(3500); print(n, pg.evaluate(N))
    def studio():
        pg.evaluate("()=>{closeAll(); const x=document.querySelector('#auraScreen .closeb'); if(x&&document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click();}"); pg.wait_for_timeout(600); pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
        if PERTE: print('  perte :', pg.evaluate("()=>{ const c=document.getElementById('auBouleGL'); if(!c) return 'pas de canevas'; const g=c.getContext('webgl2'); const e=g&&g.getExtension('WEBGL_lose_context'); if(e){ e.loseContext(); return 'contexte perdu'; } return 'extension absente'; }"))
        pg.evaluate("()=>{const x=document.querySelector('#studioScreen .closeb')||document.querySelector('#stcCadre .closeb'); if(x) x.click(); else closeAll();}"); pg.wait_for_timeout(1200)
    aura('Aura 1'); studio(); studio(); aura('Aura 2')
    b.close()
