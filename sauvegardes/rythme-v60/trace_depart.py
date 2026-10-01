# Trace (devtools.timeline) du vrai départ : ce que le moteur de rendu fait pendant les 300 ms qui suivent le « Oui ».
import json, sys, collections
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'gravure'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ openDetail(97001); }"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{ window._v16SupprimerPromi(cur); }"); pg.wait_for_timeout(800)
    xy=pg.evaluate("()=>{ const r=document.querySelector('#v16Conf .v16-oui').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]; }")
    b.start_tracing(page=pg, categories=['devtools.timeline','disabled-by-default-devtools.timeline','v8','blink','cc','gpu','disabled-by-default-devtools.timeline.frame','toplevel'])
    pg.mouse.click(*xy); pg.wait_for_timeout(400)
    tr=json.loads(b.stop_tracing())
    noms={(e['pid'],e['tid']):e['args']['name'] for e in tr['traceEvents'] if e.get('name')=='thread_name'}
    main=[k for k,v in noms.items() if v=='CrRendererMain']
    ev=[e for e in tr['traceEvents'] if e.get('ph')=='X' and e.get('dur',0)>1500 and (e['pid'],e['tid']) in main]
    t0=min(e['ts'] for e in ev)
    big=[e for e in ev if e['name']=='RunTask' and e['dur']>60000]
    if big:
        B=big[0]; tout=[e for e in tr['traceEvents'] if (e.get('pid'),e.get('tid')) in main and e.get('ts',0)>=B['ts'] and e.get('ts',0)<=B['ts']+B['dur'] and e.get('ph') in ('X','B','I','i')]
        c=collections.Counter(); 
        for e in tout: c[e['name']]+=e.get('dur',0)/1000
        print('DANS LA GRANDE TÂCHE', round(B['dur']/1000), c.most_common(25))
        for e in sorted(tout,key=lambda e:e['ts'])[:40]: print('   %6.1f %6.2f %s %s'%((e['ts']-B['ts'])/1000, e.get('dur',0)/1000, e['name'], str(e.get('args',{}))[:120]))
    for e in sorted(ev,key=lambda e:e['ts'])[:0]:
        a=e.get('args',{}).get('data',{}) or {}
        info=a.get('functionName') or a.get('type') or a.get('url','')[-20:] or ''
        if e['name']=='FunctionCall': info=str(a.get('functionName'))+' l.'+str(a.get('lineNumber'))
        if e['name']=='UpdateLayoutTree': info='éléments %s'%(e.get('args',{}).get('elementCount'))
        print('%6.1f %6.1f  %-22s %s'%((e['ts']-t0)/1000, e['dur']/1000, e['name'], info))
    b.close()
