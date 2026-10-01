from playwright.sync_api import sync_playwright
import json
ECR=[('accueil',"()=>{}"),('Index',"()=>document.getElementById('indexBtn').click()"),('Fil',"()=>document.getElementById('filBtn').click()"),
 ('Réglages',"()=>document.getElementById('settingsBtn').click()"),('Aura',"()=>document.getElementById('souffleBtn').click()"),
 ('Studio',"()=>document.getElementById('studioBtn').click()"),('Partager',"()=>document.getElementById('shareBtn').click()"),
 ('offre',"()=>ouvreCercle()"),('fiche Promi',"()=>openDetail(promises.find(p=>p.status==='encours'&&!p.chiche&&!p.draft).id)"),
 ('page +',"()=>{document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()},400)}")]
Q="""()=>{const dv=document.getElementById('device').getBoundingClientRect();const m={};
 document.querySelectorAll('#device *, .frame .screen.show, .frame .screen.show *').forEach(e=>{const s=getComputedStyle(e);const c=s.backgroundColor;if(!c||c==='rgba(0, 0, 0, 0)')return;
  const r=e.getBoundingClientRect();if(r.width<30||r.height<20||r.bottom<dv.top||r.top>dv.bottom||r.right<dv.left||r.left>dv.right)return;if(s.visibility==='hidden'||+s.opacity<0.05)return;
  const a=r.width*r.height; const k=c; if(!m[k])m[k]={aire:0,ex:[]}; m[k].aire+=a; if(m[k].ex.length<3)m[k].ex.push((e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,26));});
 return Object.entries(m).sort((x,y)=>y[1].aire-x[1].aire).slice(0,6).map(([c,v])=>[c,Math.round(v.aire/1000),v.ex.join(' ')]);}"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}"); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>setTheme('dark')")
    for nom,js in ECR:
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'))}"); pg.wait_for_timeout(500)
        pg.evaluate(js); pg.wait_for_timeout(1800)
        print('==',nom); [print('   ',x) for x in pg.evaluate(Q)]
