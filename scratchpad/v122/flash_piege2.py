from playwright.sync_api import sync_playwright
INIT="""try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');
 window.__j=[]; const sp=CSSStyleDeclaration.prototype.setProperty;
 CSSStyleDeclaration.prototype.setProperty=function(k,v,p){ try{ if(/color|fill/.test(k) && this.__el && /^(dptQui|dptQuand|dptTrace)$/.test(this.__el.id)) window.__j.push([performance.now()|0,this.__el.id,k,v,(new Error().stack||'').split('\\n').slice(1,4).join(' | ').slice(0,300)]); }catch(_){} return sp.call(this,k,v,p); };
 const ct=Object.getOwnPropertyDescriptor(CSSStyleDeclaration.prototype,'cssText'); Object.defineProperty(CSSStyleDeclaration.prototype,'cssText',{get(){return ct.get.call(this)}, set(v){ try{ if(this.__el && /^(dptQui|dptQuand|dptTrace)$/.test(this.__el.id)) window.__j.push([performance.now()|0,this.__el.id,'cssText',String(v).slice(0,90),(new Error().stack||'').split('\n').slice(1,4).join(' | ').slice(0,300)]); }catch(_){} return ct.set.call(this,v); }, configurable:true});
 const sa=Element.prototype.setAttribute; Element.prototype.setAttribute=function(k,v){ try{ if(k==='style' && /^(dptQui|dptQuand|dptTrace)$/.test(this.id)) window.__j.push([performance.now()|0,this.id,'attr style',String(v).slice(0,90),(new Error().stack||'').split('\n').slice(1,4).join(' | ').slice(0,300)]); }catch(_){} return sa.call(this,k,v); };
 ['color','webkitTextFillColor'].forEach(function(pp){ const dd=Object.getOwnPropertyDescriptor(CSSStyleDeclaration.prototype,pp); if(dd&&dd.set) Object.defineProperty(CSSStyleDeclaration.prototype,pp,{get(){return dd.get.call(this)}, set(v){ try{ if(this.__el && /^(dptQui|dptQuand|dptTrace)$/.test(this.__el.id)) window.__j.push([performance.now()|0,this.__el.id,pp,v,(new Error().stack||'').split('\n').slice(1,4).join(' | ').slice(0,300)]); }catch(_){} return dd.set.call(this,v); }, configurable:true}); });
 const d=Object.getOwnPropertyDescriptor(HTMLElement.prototype,'style'); Object.defineProperty(HTMLElement.prototype,'style',{get(){ const s=d.get.call(this); try{ s.__el=this; }catch(_){} return s; }, configurable:true});
}catch(e){}"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for i in range(1):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); ctx.add_init_script(INIT)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(700)
        r=pg.evaluate("""()=>new Promise(res=>{ window.__j=[]; const seq=[]; const t0=performance.now();
          const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);
          function f(){ const e=document.getElementById('dptQui'); const dp=document.getElementById('detailPoster');
            if(e) seq.push([(performance.now()-t0)|0, getComputedStyle(e).color, dp.className.slice(0,80), e.style.cssText.slice(0,80)]);
            if(performance.now()-t0<2500) requestAnimationFrame(f); else res({seq:seq, j:window.__j.map(x=>[x[0]-t0|0].concat(x.slice(1)))}); }
          requestAnimationFrame(f); })""")
        ch=[]; prev=None
        for s in r['seq']:
            if s[1]!=prev: ch.append(s); prev=s[1]
        print('== essai',i); [print('  ',c) for c in ch]
        for x in r['j'][:20]: print('   écrit',x)
        ctx.close()
    b.close()
