import sys, json
from playwright.sync_api import sync_playwright
MOT = sys.argv[1] if len(sys.argv)>1 else 'webkit'
JS = r"""async ()=>{ const A=window._aura, M=window.PeloteMoteur, cv=document.getElementById('auBoule'); A.fige(true);
  await new Promise(r=>setTimeout(r,800));
  const med=a=>{a.sort((x,y)=>x-y); return +a[a.length>>1].toFixed(2)};
  // l'option courante : on la capture en enveloppant peintGL une fois
  let O=null; const pg0=M.peintGL; M.peintGL=function(c,o){ O=o; return pg0(c,o); }; A.pelote(); M.peintGL=pg0;
  const t={etat:[], gl:[], tout:[], cpu:[], lecture:[]};
  const o2=Object.assign({},O,{seulementEtat:true});
  for(let i=0;i<25;i++){ O.lac+=0.01; o2.lac=O.lac;
    let a=performance.now(); M.peint(cv,o2); t.etat.push(performance.now()-a);
    a=performance.now(); M.peintGL(cv,O); t.tout.push(performance.now()-a);
    a=performance.now(); cv.getContext('2d').getImageData(10,10,1,1); t.lecture.push(performance.now()-a); }
  for(let i=0;i<5;i++){ let a=performance.now(); M.peint(cv,O); t.cpu.push(performance.now()-a); }
  const d=document.createElement('canvas').getContext('webgl2'); const ext=d&&d.getExtension('WEBGL_debug_renderer_info');
  return {etat:med(t.etat), peintGL:med(t.tout), lecturePixel:med(t.lecture), cpu:med(t.cpu), n:O&&O.n, W:cv.width, rendu: ext?d.getParameter(ext.UNMASKED_RENDERER_WEBGL):d&&d.getParameter(d.RENDERER)}; }"""
with sync_playwright() as p:
    b = (p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4500)
    print(MOT, json.dumps(pg.evaluate(JS), ensure_ascii=False))
    b.close()
