# Le « clic fantôme » : après un toucher, que reçoit la page, et qui appelle closeAll ?
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True)
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{ window.__log=[]; const t0=performance.now(); const L=(s)=>__log.push(Math.round(performance.now()-t0)+' '+s);
      const nom=e=>{ const x=e.target; return x ? (x.id?'#'+x.id:'')+'.'+String(x.className&&x.className.baseVal!==undefined?x.className.baseVal:x.className||'').split(' ')[0] : '?'; };
      ['pointerdown','pointerup','pointercancel','touchstart','touchend','mousedown','mouseup','click'].forEach(k=>document.addEventListener(k,e=>L(k+' → '+nom(e)),true));
      const c0=window.closeAll; window.closeAll=function(){ L('closeAll ← '+(new Error().stack.split('\\n')[2]||'').trim().slice(0,90)); return c0.apply(this,arguments); };
      const o0=window.openDetail; window.openDetail=function(id){ L('openDetail('+id+')'); return o0.apply(this,arguments); };
      const p0=window.openPerson; window.openPerson=function(n){ L('openPerson('+n+')'); return p0.apply(this,arguments); }; }""")
    def aura():
        pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(250)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret)"): break
        pg.wait_for_timeout(800)
    def tape(sel):
        c=pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].find(e=>e.getBoundingClientRect().height>0); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}", sel)
        pg.evaluate("()=>{__log.length=0;}")
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':c[0],'y':c[1]}]}); pg.wait_for_timeout(60)
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(1400)
        st=pg.evaluate("()=>({detail:document.getElementById('detailPoster').classList.contains('show'), personne:document.getElementById('personSheet').classList.contains('show'), aura:document.getElementById('auraScreen').classList.contains('show')})")
        print('\n== toucher', sel, st); [print('   ',l) for l in pg.evaluate("()=>__log")]
    aura(); tape('#auraScreen .au-c')
    aura(); tape('#auraScreen .au-gp .au-n .au-nb')
    b.close()
