import sys, os; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
cars=os.environ.get('CARS','R'); fzs=[float(x) for x in os.environ.get('FZS','29').split(',')]; ech=float(os.environ.get('ECH','0.7466'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    for m in [x for x in os.environ.get('ADD','').split(',') if x]: pg.add_script_tag(url='http://127.0.0.1:8752/'+m); pg.wait_for_timeout(300)
    for c in cars:
        for fz in fzs:
            h={'À':GRAVE,'É':AIGU,'D':None}.get(c) if c in 'ÀÉ' else c
            o=geo_ecran(pg, h, fz, ech); print('%s %g hors %d trous %d avance %d ilots %d(%d) creux %d loin %d fin %d pas %d angles %s reso %s' % (c,fz,o['hors'],o['trous'],o['avance'],o['ilots'],o['ilotMax'],o['creux'],o['loin'],o['fin'],o['pas'], o['angles'][:3], o['reso']['ok']), flush=True)
    b.close()
