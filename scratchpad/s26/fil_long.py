# -*- coding: utf-8 -*-
"""Le titre long du bandeau du Fil : il doit REMONTER, puis retrecir. Se passe sur les
   DEUX versions — la fautive doit rougir (titre tronque)."""
import json,sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
LONGS=["rapporter le livre de la bibliotheque avant vendredi",
       "reprendre l'arrosage du potager tous les matins"]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(L)=>{ var ids=[129,125]; ids.forEach(function(id,k){ var q=promises.filter(function(x){return x.id===id;})[0]; if(q) q.title=L[k]; }); }", LONGS)
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3600)
    r=pg.evaluate(r"""()=>{ var o=[];
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d){
        var t=d.querySelector('.s4-ti'), v=d.querySelector('.s4-ev'), e=d.querySelector('.s4-et');
        var rt=t.getBoundingClientRect(), rd=d.getBoundingClientRect(), rv=v.getBoundingClientRect(), re=e.getBoundingClientRect();
        var sc=rd.width/358;
        o.push({titre:t.textContent.slice(0,34), fs:getComputedStyle(t).fontSize,
                tronque:(t.scrollHeight>t.clientHeight+1),
                scroll:t.scrollHeight, client:t.clientHeight,
                tiTop:+t.style.top.replace('px',''), evTop:v.style.top,
                airEvTi:+(((rt.top-rv.bottom)/sc)).toFixed(1),
                airTiEt:+(((re.top-rt.bottom)/sc)).toFixed(1),
                hautEv:+(((rv.top-rd.top)/sc)).toFixed(1)});
      }); return o; }""")
    print(json.dumps(r,indent=1,ensure_ascii=False))
    open('scratchpad/s26/FIL-long-%s.png'%('apres' if 'app.html' in URL else 'avant'),'wb').write(pg.query_selector('#device').screenshot())
    b.close()
