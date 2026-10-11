# qui tourne au lever de « tenir » — banc_tom (WebKit), vrai doigt. Chaque rappel (minuteur, image, observateur, écouteur, message) est chronométré.
import sys, json; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
OU=open('redteam_deplace.py',encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; N=int(sys.argv[2]) if len(sys.argv)>2 else 4
PROF = r"""(function(){ var R=window.__P=[], on=false; window.__Pon=function(v){ on=v; if(v) R.length=0; };
  function nom(f,typ){ var s=''; try{ s=(f.name||'')+' · '+(''+f).replace(/\s+/g,' ').slice(0,150); }catch(e){} return typ+' | '+s; }
  function env(f,typ){ if(typeof f!=='function') return f; var w=function(){ if(!on) return f.apply(this,arguments); var t=performance.now(); try{ return f.apply(this,arguments); } finally { var d=performance.now()-t; if(d>=1.5) R.push([Math.round(t),Math.round(d*10)/10,nom(f,typ)]); } }; return w; }
  var st=window.setTimeout; window.setTimeout=function(f,ms){ var a=[].slice.call(arguments); a[0]=env(f,'minuteur '+(ms|0)); return st.apply(window,a); };
  var si=window.setInterval; window.setInterval=function(f,ms){ var a=[].slice.call(arguments); a[0]=env(f,'intervalle '+(ms|0)); return si.apply(window,a); };
  var rf=window.requestAnimationFrame; window.requestAnimationFrame=function(f){ return rf.call(window, env(f,'image')); };
  var MO=window.MutationObserver; window.MutationObserver=function(f){ return new MO(env(f,'observateur')); }; window.MutationObserver.prototype=MO.prototype;
  var ael=EventTarget.prototype.addEventListener; EventTarget.prototype.addEventListener=function(t,f,o){ if(typeof f==='function' && /^(touch|pointer|click|mouse|transitionend)/.test(t)){ var w=f.__w||(f.__w=env(f,'écouteur '+t)); return ael.call(this,t,w,o); } return ael.call(this,t,f,o); };
  window.__F=[]; (function b(t){ window.__F.push(Math.round(performance.now()*10)/10); if(window.__F.length>4000) window.__F.shift(); rf.call(window,b); })();
})();"""
with sync_playwright() as p:
    b=p.webkit.launch(); tous=[]
    for k in range(N):
        ctx=B.contexte(b); ctx.add_init_script(PROF); pg=B.ouvre(ctx,F)
        B.plante(pg,'rendre le livre'); B.plante(pg,'écrire à Lou'); pg.wait_for_timeout(1500)
        G=pg.evaluate(OU); a=list(G)[0]; B.tap(pg,G[a][0],G[a][1]); pg.wait_for_timeout(2500)
        z=pg.evaluate("()=>{const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]}")
        y=z[1]+z[3]*0.45
        pg.evaluate("()=>{ window.__Pon(true); window.__lever=0; document.addEventListener('touchend',()=>{ if(!window.__lever) window.__lever=performance.now(); },true); }")
        B.glisse(pg,[[200+130*i/12,y] for i in range(13)],pas=22,tenue=380); pg.wait_for_timeout(2200)
        r=pg.evaluate("()=>({lever:window.__lever, P:window.__P.slice(), F:window.__F.slice(), tenu:promises[0].status})")
        t0=r['lever']; L=[(e[0]-t0,e[1],e[2]) for e in r['P'] if -30<=e[0]-t0<=1800]
        Fr=[f for f in r['F'] if -50<=f-t0<=1800]; gaps=[(round(Fr[i]-t0),round(Fr[i+1]-Fr[i],1)) for i in range(len(Fr)-1) if Fr[i+1]-Fr[i]>20]
        tous.append((L,gaps)); print('passe',k,'statut',r['tenu'],'· images de plus de 20 ms :',gaps[:12],'· travail compté %.0f ms'%sum(e[1] for e in L),flush=True)
        ctx.close()
    b.close()
# le tableau : par rappel, le temps cumulé médian, le nombre, le pire, et quand
import collections; A=collections.defaultdict(list)
for L,_ in tous:
    loc=collections.defaultdict(lambda:[0,0,0,[]])
    for t,d,n in L: x=loc[n]; x[0]+=d; x[1]+=1; x[2]=max(x[2],d); x[3].append(round(t))
    for n,x in loc.items(): A[n].append(x)
rows=sorted(A.items(), key=lambda kv:-sum(x[0] for x in kv[1])/len(tous))
print('\n%-9s %-6s %-7s %-22s %s'%('ms/passe','appels','pire','quand (ms après lever)','rappel'))
for n,X in rows[:28]:
    print('%-9.1f %-6.1f %-7.1f %-22s %s'%(sum(x[0] for x in X)/len(tous), sum(x[1] for x in X)/len(tous), max(x[2] for x in X), str(sorted(X[0][3])[:5]), n[:170]))
json.dump([[L,g] for L,g in tous], open('scratchpad/v143/profil-%s.json'%F.replace('.html',''),'w'))
