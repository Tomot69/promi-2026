import sys, os; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
ech=float(os.environ.get('ECH','0.7466'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    for fz in (19,25,29,32,42,52):
        pg.evaluate(GEO_ECRAN,['U',fz,ech,'pose'])
        r=pg.evaluate("""fz=>{ const el=document.getElementById('gEl'), er=el.getBoundingClientRect(), k=er.width/el.offsetWidth, d=devicePixelRatio; const rg=document.createRange(); rg.setStart(el.firstChild,0); rg.setEnd(el.firstChild,1); const rc=rg.getClientRects()[0];
          const bac=document.createElement('div'); bac.style.cssText='position:absolute;left:-9999px;top:0;white-space:nowrap;line-height:normal'; document.body.appendChild(bac); const sp=document.createElement('span'); sp.style.cssText='font:400 '+fz+'px PromiLate;line-height:normal'; sp.appendChild(document.createTextNode('Hx')); const s0=document.createElement('span'); s0.style.cssText='display:inline-block;width:0;height:0;vertical-align:baseline'; sp.appendChild(s0); bac.appendChild(sp); const r2=document.createRange(); r2.setStart(sp.firstChild,0); r2.setEnd(sp.firstChild,1); const asc=s0.getBoundingClientRect().bottom-r2.getBoundingClientRect().top; const rh=r2.getBoundingClientRect().height; bac.remove();
          const m=document.createElement('canvas').getContext('2d'); m.font='400 '+fz+'px PromiLate'; const tm=m.measureText('H');
          return {k, asc, rh, fba: tm.fontBoundingBoxAscent, fbd: tm.fontBoundingBoxDescent, top:(rc.top-er.top)/k, h: rc.height/k, base:(rc.top-er.top)/k+asc, dev:(rc.top+asc*k)*d}; }""", fz)
        print(fz, {kk:round(v,3) for kk,v in r.items()})
    b.close()
