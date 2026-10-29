import sys, os; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
ech=float(os.environ.get('ECH','0.7466')); seul=os.environ.get('SEUL','')
tailles={}
for t,fz in TEXTES_PL:
    for c in t.replace(' ',''): tailles.setdefault(c,set()).add(round(fz))
cas=[(c,fz) for c in sorted(tailles) for fz in sorted(tailles[c])]+[('À',29),('É',42),('Deuxio',25)]
if seul: cas=[q for q in cas if q[0] in seul.split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    for m in [x for x in os.environ.get('ADD','').split(',') if x]: pg.add_script_tag(url='http://127.0.0.1:8752/'+m); pg.wait_for_timeout(300)
    A=[]
    for c,fz in cas:
        h={'À':GRAVE,'É':AIGU,'Deuxio':PENCHE}.get(c,c)
        o=geo_ecran(pg,h,fz,ech); A+=o['angles']
        bad = o['hors'] or o['ilots'] or o['creux'] or o['loin']>3 or o['pas']<12 or o['fin'] or (c!='Deuxio' and (o['trous']>30 or o['avance']>30))
        print(o.get('coudes'), end=' '); print('%s %s %g hors %d trous %d avance %d ilots %d(%d) creux %d loin %d fin %d pas %d angles %s' % ('KO' if bad else 'ok', c,fz,o['hors'],o['trous'],o['avance'],o['ilots'],o['ilotMax'],o['creux'],o['loin'],o['fin'],o['pas'],o['angles']), flush=True)
    print('ANGLES', len(A), max(A) if A else None)
    b.close()
