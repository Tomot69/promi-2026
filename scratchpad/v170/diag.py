import sys, io, json; sys.path.insert(0,'.')
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]
sys.argv=['x']; exec(src)
CARS=sys.argv_cars if hasattr(sys,'argv_cars') else None
import os
cars=os.environ.get('CARS','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}")
    for c in cars:
        r=pg.evaluate(GEO, ['PromiLate','400',c,NGEO,float(os.environ.get('FZ','150'))])
        if not r: print(c,'AUCUN'); continue
        o=geo_analyse(r); A=o['angles']
        print('%s hors %d trous %d avance %d ilots %d(max %d) loin %d bout %s angles %s coudes %s pas %d' % (c,o['hors'],o['trous'],o['avance'],o['ilots'],o['ilotMax'],o['loin'],o.get('bout'), (max(map(abs,A)) if A else None), o.get('coudes',0), o['pas']), flush=True)
    b.close()
