import sys, random; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; N=int(sys.argv[2]) if len(sys.argv)>2 else 10; GRAINE=int(sys.argv[3]) if len(sys.argv)>3 else 1; PAS=int(sys.argv[4]) if len(sys.argv)>4 else 25
random.seed(GRAINE)
NEUFS={'esquille','bobinette','ritournelle','madrure','halin','brouillamini','chamade','volubilis','guingois','chantourne','mascaret','ramage'}
INV = """()=>{ var th=Toile.getTheme(), c=Toile_cellules(), col=c.c.filter(s=>s.kind!=='gray'), gris=c.c.length-col.length, n=col.length;
  var md=1e9, paire=null; for(var i=0;i<col.length;i++) for(var j=i+1;j<col.length;j++){ var d=Math.hypot(col[i].x-col[j].x, col[i].y-col[j].y); if(d<md){ md=d; paire=[col[i].pid,col[j].pid]; } }
  var pr=Toile_probe(), mp=0; pr.forEach(d=>{ mp=Math.max(mp,Math.abs(d[0]),Math.abs(d[1])); });
  return {th:th, n:n, gris:gris, total:c.c.length, neuf:Toile.semisNeuf(), md:Math.round(md*10)/10, paire:paire, vue:[+c.view.s.toFixed(3),+c.view.ox.toFixed(1),+c.view.oy.toFixed(1)], mp:mp, cv:document.getElementById('toileCv').width}; }"""
def ferme(pg):
    for _ in range(3):
        pg.evaluate("""()=>{ try{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); const s=h&&h.closest('.screen, #feedView, #indexSheet, .sheet, .poster'); const x=s&&s.querySelector('.closeb'); if(x) x.click(); }catch(e){} try{closeAll()}catch(e){} }""")
        pg.wait_for_timeout(500)
        if pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.42); return !h || h.id==='toileCv'; }"): return
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 692}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_monde','terrazzo');}}catch(e){}")
    if N in (1,5,10,25,50): toile_pleine(ctx, N)
    pg = ouvre(ctx, F); pg.evaluate("()=>{try{setPremium(true)}catch(e){}}")
    pg.wait_for_timeout(1500); base = pg.evaluate(INV); print('départ', base, flush=True)
    for i in range(PAS):
        act = random.choice(['studio','studio','studio','studio','page','fiche','attente'])
        if act=='studio':
            trace=[]; tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(1800)
            sd = random.choice([1,-1])
            for _ in range(random.randint(1,9)):
                s = sd; x0,x1 = (300,90) if s>0 else (90,300)
                rr=glisse(pg, droite([x0,420],[x1,420],10), pas=16); pg.wait_for_timeout(random.choice([150,600,1500])); trace.append((rr, pg.evaluate('()=>Toile.getTheme()')))
            tap_sel(pg,'#studioScreen .closeb'); pg.wait_for_timeout(random.choice([200,1200,2500])); print('   studio', trace)
        elif act=='page':
            tap_sel(pg, random.choice(['#souffleBtn','#indexBtn','#filBtn','#createBtn'])); pg.wait_for_timeout(random.choice([300,1500])); ferme(pg); pg.wait_for_timeout(random.choice([200,1500]))
        elif act=='fiche':
            pg.evaluate("()=>{var p=promises.filter(p=>!p.draft); if(p.length) openDetail(p[Math.floor(Math.random()*p.length)].id);}"); pg.wait_for_timeout(1200); ferme(pg); pg.wait_for_timeout(800)
        else: pg.wait_for_timeout(random.choice([3000,8000]))
        pg.wait_for_timeout(1500)
        r = pg.evaluate(INV)
        attendu_neuf = r['th'] in NEUFS and (r['th']=='ritournelle' or r['n']>=9)
        mal = []
        if r['neuf']!=attendu_neuf: mal.append('famille')
        if (not attendu_neuf) and r['gris']==0: mal.append('aucune cellule vide')
        if attendu_neuf and r['gris']>0: mal.append('cellules vides en semis neuf')
        if r['md']<8: mal.append('dalles empilées')
        if r['n']!=base['n']: mal.append('nombre')
        print(i, act, r['th'], 'n', r['n'], 'gris', r['gris'], 'neuf', r['neuf'], 'md', r['md'], 'vue', r['vue'], 'mp', round(r['mp'],1), ('❌ '+','.join(mal)) if mal else '', flush=True)
    print(pg.erreurs[:3]); b.close()
