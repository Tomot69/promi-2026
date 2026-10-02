# Harnais de capture pour le simulateur iPhone (aucun outil de toucher) : une copie zz-sim.html de l'app qui passe l'onboarding et joue un scénario lu dans l'adresse.
# usage : sim.py <nom> <thème> <scénario> [query]   scénarios : studio | palettes | fiche | aura | plus | index
import sys, io, subprocess, time
UD='7936018E-692C-496E-B482-92047C1A0227'
nom, th, sc = sys.argv[1], sys.argv[2], sys.argv[3]; q = sys.argv[4] if len(sys.argv)>4 else ''
S=io.open(__import__('os').environ.get('SRC','app.html'),encoding='utf-8').read()
H="""<script>try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}
window.addEventListener('load',function(){ setTimeout(function(){ var P=new URLSearchParams(location.search), sc=P.get('sc'), th=P.get('th');
  var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}
  try{ setTheme(th); }catch(e){}
  function barre(mot){ var b=[].slice.call(document.querySelectorAll('#device *')).find(function(e){return e.children.length<4&&new RegExp('^\\\\s*'+mot+'\\\\s*$','i').test(e.textContent)&&e.getBoundingClientRect().height>0}); if(b)(b.closest('button,[role=button],.acc-b,a')||b).click(); }
  setTimeout(function(){
    if(sc==='studio'||sc==='palettes'){ barre('STUDIO'); if(sc==='palettes') setTimeout(function(){ var t=document.querySelector('#studioScreen .stp-ton'); if(t) t.click(); },2500); }
    if(sc==='aura') barre('AURA');
    if(sc==='index') barre('INDEX');
    if(sc==='plus'){ try{ document.getElementById('createBtn').click(); }catch(e){} }
    if(sc==='fiche'){ try{ var p=promises.find(function(q){return /cr.pes/i.test(q.title||'')}); openDetail(p.id); }catch(e){} }
  },700); },6500); });</script>"""
assert S.count('</head>')>=1
io.open('zz-sim.html','w',encoding='utf-8').write(S.replace('</head>',H+'</head>',1))
url='http://127.0.0.1:8752/zz-sim.html?sc=%s&th=%s&t=%d%s'%(sc,th,int(time.time()),('&'+q) if q else '')
subprocess.run(['xcrun','simctl','openurl',UD,url]); time.sleep(float(sys.argv[5]) if len(sys.argv)>5 else 16)
subprocess.run(['xcrun','simctl','io',UD,'screenshot','planche-v120/sim-%s.png'%nom],capture_output=True)
print('planche-v120/sim-%s.png'%nom)
