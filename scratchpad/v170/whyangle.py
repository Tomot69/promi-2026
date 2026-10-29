import sys, os; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]
src=src.replace("            if min(sf - a, b2 - sf) < 2.5 * Rk: break\n","            if min(sf - a, b2 - sf) < 2.5 * Rk: WHY.append(('bout',k,round(sf-a),round(b2-sf),round(2.5*Rk))); break\n",1)
src=src.replace("            if len(xx) < max(6, 0.8 * Rk): break\n","            if len(xx) < max(6, 0.8 * Rk): WHY.append(('bord',k,len(xx),int((rev & vu & (np.abs(S_ - sf) <= tol) & (K == k)).sum()))); break\n",1)
src=src.replace("            if min(sc - a, b2 - sc) < 2.5 * Rk: break\n","            if min(sc - a, b2 - sc) < 2.5 * Rk: WHY.append(('sc',k)); break\n",1)
src=src.replace("            out['angles'].append(round(90 - math.degrees(math.acos(min(1, abs(d[0] * tx + d[1] * ty)))), 1)); break\n","            out['angles'].append(round(90 - math.degrees(math.acos(min(1, abs(d[0] * tx + d[1] * ty)))), 1)); WHY.append(('ANG',i,k,round(sc,1),out['angles'][-1],(round(tx,2),round(ty,2)),(round(d[0],2),round(d[1],2)),len(xx), (int(xx.mean()),int(yy.mean())))); break\n",1)
src=src.replace("        for k, (a, b2) in enumerate(bornes):\n","        WHY.append(('sf',round(sf),[(round(a),round(b2)) for a,b2 in bornes]))\n        for k, (a, b2) in enumerate(bornes):\n",1)
WHY=[]; exec(src)
c=os.environ.get('C','S'); fz=float(os.environ.get('FZ','29'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    for m in [x for x in os.environ.get('ADD','').split(',') if x]: pg.add_script_tag(url='http://127.0.0.1:8752/'+m); pg.wait_for_timeout(300)
    o=geo_ecran(pg,c,fz,0.7466); print(o['angles'])
    for w in WHY: print(w)
    b.close()
