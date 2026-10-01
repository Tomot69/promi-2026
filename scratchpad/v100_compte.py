# 1re ouverture d'une Nuée : chaque appel à _rendDalle et à dalleTrame (id, taille demandée, taille rendue, durée).
import sys
from playwright.sync_api import sync_playwright
APP=sys.argv[1] if len(sys.argv)>1 else 'app.html'; WK='--webkit' in sys.argv
POSE=r"""()=>{ window.__L=[]; const r=window._rendDalle; window._rendDalle=function(id,w,h,o,f){ const t=performance.now(); const c=r.apply(this,arguments);
   const st=(new Error().stack||'').split('\n').slice(2,7).map(s=>{const m=s.match(/(\w[\w$.]*)?@?.*?:(\d+):\d+/)||s.match(/at (\S+) .*?:(\d+):\d+/); return m?((m[1]||'?')+':'+m[2]):'';}).join(' < '); window.__L.push(['rend',Math.round(performance.now()-(window.__t0||0)),id,Math.round(w),Math.round(h),c?c.width+'x'+c.height:'-',Math.round(performance.now()-t),!!f,st]); return c; };
 const d=Toile.dalleTrame; Toile.dalleTrame=function(cv,id,k){ const t=performance.now(); const x=d.apply(this,arguments);
   const st2=(new Error().stack||'').split('\n').slice(2,5).map(s=>{const m=s.match(/at (\S+) .*?:(\d+):\d+/)||s.match(/(\w[\w$.]*)?@.*?:(\d+):\d+/); return m?((m[1]||'?')+':'+m[2]):'';}).join(' < ');
   window.__L.push(['trame',id,+(+k).toFixed(2),cv.width+'x'+cv.height,Math.round(performance.now()-t),st2,Math.round(t-(window.__t0||0))]); return x; }; }"""
with sync_playwright() as p:
    b=p.webkit.launch() if WK else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(1500)
    pg.evaluate(POSE)
    pg.evaluate("()=>{window.__t0=performance.now(); var k=null; for(var q in NUE){k=q;break;} closeAll(); openNueeDetail(k); window.__t1=performance.now()-window.__t0;}")
    pg.wait_for_timeout(4000)
    L=pg.evaluate("()=>window.__L"); print('openNueeDetail synchrone :', round(pg.evaluate("()=>window.__t1")),'ms')
    import collections
    rend=[x for x in L if x[0]=='rend']; tr=[x for x in L if x[0]=='trame']
    print('appels _rendDalle', len(rend), 'total', sum(x[6] for x in rend),'ms · dalleTrame', len(tr), 'total', sum(x[4] for x in tr), 'ms')
    for x in sorted(tr,key=lambda x:-x[4])[:3]: print('  ', x)
    c=collections.Counter(x[8][:150] for x in rend); print('appelants de _rendDalle :')
    for k,v in c.most_common(8): print('  ',v,k)
    c2=collections.Counter(x[5][:160] for x in tr); print('appelants de dalleTrame :')
    for k,v in c2.most_common(8): print('  ',v,k,' — ',sum(y[4] for y in tr if y[5][:160]==k),'ms')
    print('CHRONOLOGIE (début ms, durée ms, appelant) :')
    for x in sorted(tr,key=lambda x:x[6]):
        if x[6]<800: print('   %5d %4d id %s k %s %s  %s' % (x[6], x[4], x[1], x[2], x[3], x[5]))
    import itertools
    dd=[x for x in rend if '22960' in x[8] or '22961' in x[8]]
    for id_,g in itertools.groupby(sorted(dd,key=lambda x:(x[2],x[1])),key=lambda x:x[2]):
        g=list(g); print('  dalleDe id',id_, [(x[1],x[3],x[4],x[6]) for x in g][:10])
    print('couples (id, taille) distincts :', len(set((x[2],x[3],x[4]) for x in rend)), 'sur', len(rend))
    b.close()
