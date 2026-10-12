import sys, json; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
def longues(tr, marque):
    ev=tr.get('traceEvents',tr); m=[e for e in ev if e.get('name')==marque and 'ts' in e]
    if not m: return 'pas de marque'
    pid,tid,t0=m[0]['pid'],m[0]['tid'],m[0]['ts']; out=[]
    for e in ev:
        if e.get('pid')==pid and e.get('tid')==tid and e.get('ph')=='X' and e.get('dur',0)>14000 and -100000<e['ts']-t0<2300000 and e.get('name') in ('FunctionCall','Layout','UpdateLayoutTree','Paint','PrePaint','Layerize','EvaluateScript','TimerFire','FireAnimationFrame','EventDispatch','Commit','RunTask','v8.callFunction','UpdateLayerTree','RasterTask','MinorGC','MajorGC','V8.GC_SCAVENGER','ParseHTML'):
            d=e.get('args',{}).get('data',{}); out.append((round((e['ts']-t0)/1000), round(e['dur']/1000,1), e['name'], ((d.get('functionName') or '')+'@'+str(d.get('url','')).split('/')[-1][:22]+':'+str(d.get('lineNumber',''))+':'+str(d.get('columnNumber',''))) if d else ''))
    return sorted(out)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); ctx=B.contexte(b, sombre=True); pg=B.ouvre(ctx)
    for marque,js,att in (('m1',"()=>{ performance.mark('m1'); _guide.montre('studio'); }",2300),('m2',"()=>{ performance.mark('m2'); _guide.glisse(); }",1700)):
        b.start_tracing(page=pg, categories=['toplevel','devtools.timeline','disabled-by-default-devtools.timeline','blink.user_timing','v8'])
        pg.evaluate(js); pg.wait_for_timeout(att); tr=json.loads(b.stop_tracing().decode('utf-8'))
        print(marque); [print('   ',x) for x in longues(tr,marque)]
    b.close()
