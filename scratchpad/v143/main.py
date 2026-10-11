import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
OU=open('redteam_deplace.py',encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
FL="()=>{const o={}; for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i); if(/^geste_vu_|promi_guide|promi_onb/.test(k)) o[k.replace('geste_vu_','g:')]=localStorage.getItem(k);} return JSON.stringify(o)}"
MAIN="()=>{ const g=document.getElementById('gesteFantome'); const m=g&&g.querySelector('svg > g'); const e=window.GesteFantome&&GesteFantome.etat&&GesteFantome.etat(); return {noeud:!!(m), etat:e, guide:(document.getElementById('guide')||{getAttribute:()=>null}).getAttribute('data-guide')} }"
def premier(b, chemin):
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True,is_mobile=True,user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000)
    B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Tom',delay=40); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
    pg.keyboard.type('marcher une heure',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
    z=pg.evaluate("()=>{const c=document.getElementById('onbTrait'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return {l:(r.left-d.left)/k,t:(r.top-d.top)/k,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    a=[float(v) for v in z['dep'].split(',')]; e=[float(v) for v in z['arr'].split(',')]
    B.glisse(pg,[[z['l']+a[0]+(e[0]+6-a[0])*i/24, z['t']+a[1]+(e[1]-a[1])*i/24-14*(1-abs(2*i/24-1))] for i in range(25)],pas=22); pg.wait_for_timeout(6800)
    B.tap(pg,195,300); pg.wait_for_timeout(1200); B.tap_sel(pg,'.onbv-compte .tard'); pg.wait_for_timeout(3500)
    print(chemin,'· sur l\'accueil :',pg.evaluate(MAIN),pg.evaluate(FL))
    if chemin=='plus tard': B.tap_sel(pg,'#guideTard'); pg.wait_for_timeout(1500)
    elif chemin=='ailleurs': B.tap(pg,195,250); pg.wait_for_timeout(1500)
    elif chemin=='studio':
        t=pg.evaluate("()=>_guide.etat().trou"); B.tap(pg,t['x'],t['y']); pg.wait_for_timeout(2500); B.tap_sel(pg,'#studioScreen .closeb'); pg.wait_for_timeout(1500)
    print('  après le guide :',pg.evaluate(MAIN))
    for essai in range(3):
        g=pg.evaluate("()=>(document.getElementById('guide')||{getAttribute:()=>null}).getAttribute('data-guide')")
        if not g: break
        B.tap_sel(pg,'#guideTard'); pg.wait_for_timeout(1500)
    G=pg.evaluate(OU); 
    if not G: print('  aucune dalle trouvée'); ctx.close(); return
    a_=list(G)[0]; B.tap(pg,G[a_][0],G[a_][1]); vus=[]
    for i in range(30):
        pg.wait_for_timeout(150); m=pg.evaluate(MAIN); vus.append(m['noeud'])
    fiche=pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
    print('  fiche ouverte',fiche,'· main vue',any(vus),'à partir de',(vus.index(True)*150 if any(vus) else None),'ms ·',pg.evaluate(MAIN),pg.evaluate(FL)); ctx.close()
with sync_playwright() as p:
    b=p.webkit.launch()
    for c in ('plus tard','ailleurs','studio'): premier(b,c)
    b.close()
