# Latences des transitions d'écran — un VRAI clic (souris Playwright, isTrusted), puis :
#   pret  : ms entre le pointerdown et la première image où l'écran visé est posé (sa condition)
#   img   : l'image la plus longue dans les 1,5 s qui suivent · lentes : images > 50 ms · bloque : Σ(image − 16,7) au-delà de 50
# En Chromium, le profileur du CDP nomme les fonctions qui coûtent (temps propre, ms).
# python3 latences.py [--webkit] [--profil] [--seul=nom]
import sys, json, collections
from playwright.sync_api import sync_playwright
WK='--webkit' in sys.argv; PROF='--profil' in sys.argv and not WK
SEUL=next((a.split('=')[1] for a in sys.argv if a.startswith('--seul=')),None)
INSTALLE=r"""()=>{ window.__F=[]; window.__T0=null; window.__PRET=null; window.__cond=null;
  if(!window.__arme){ window.__arme=1; window.addEventListener('pointerdown',e=>{ if(window.__T0==null&&!window.__surLeve) window.__T0=performance.now(); },true);
    window.addEventListener('pointerup',e=>{ if(window.__surLeve&&window.__T0==null) window.__T0=performance.now(); },true);
    (function boucle(t){ if(window.__F) window.__F.push(t); if(window.__cond&&window.__PRET==null&&window.__T0!=null){ try{ if(window.__cond()) window.__PRET=t; }catch(_){} } requestAnimationFrame(boucle); })(performance.now()); } }"""
LIT=r"""()=>{ const F=window.__F.filter(t=>t>=window.__T0-1), d=[]; for(let i=1;i<F.length;i++) d.push(F[i]-F[i-1]);
  const mx=d.length?Math.max(...d):0, lentes=d.filter(x=>x>50).length, bl=d.reduce((s,x)=>s+(x>50?x-16.7:0),0);
  return {pret: window.__PRET!=null? Math.round(window.__PRET-window.__T0):null, img:Math.round(mx), lentes:lentes, bloque:Math.round(bl)}; }"""
def centre(pg, sel):
    return pg.evaluate("s=>{const e=typeof s==='string'?document.querySelector(s):null; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}", sel)
def ferme(pg):
    pg.evaluate("()=>{ try{ document.querySelectorAll('.screen.show').forEach(s=>{ const r=s.getBoundingClientRect(); if(r.top<200&&r.bottom>300){ const c=s.querySelector('.closeb'); if(c) c.click(); } }); }catch(_){} }"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ try{ closeAll(); document.querySelectorAll('.screen.show').forEach(e=>{ if(e.id!=='studioScreen'&&e.id!=='auraScreen') e.classList.remove('show'); }); setView&&setView('toile'); var c=document.getElementById('accChoix'); if(c) c.classList.remove('ouvert'); }catch(_){} }")
    pg.wait_for_timeout(900)
ACTIONS=[
 ('+ (les natures)',        None, '#createBtn', "()=>document.getElementById('accChoix').classList.contains('ouvert')"),
 ('Un Promi → page +',      'plus', '#accChoix .acc-pil[data-k=promi]', "()=>{const s=document.getElementById('createSheet'); return s.classList.contains('show')&&s.classList.contains('pp-promi')&&!s.classList.contains('acc-passe')&&!s.classList.contains('pp-choix');}"),
 ('planter → dalle',        'pageplus', 'GESTE', "()=>Toile.count()>window.__n0"),
 ('fiche (toucher la dalle)', None, 'DALLE', "()=>document.getElementById('detailPoster').classList.contains('show')"),
 ('disque de fiche',        'fiche', 'DISQUE', "()=>!!document.querySelector('#personSheet.show, .sheet.show:not(#detailPoster)')"),
 ('retour à la Toile',      'fiche', '#detailPoster .closeb', "()=>!document.getElementById('detailPoster').classList.contains('show')"),
 ('Index',                  None, '#indexBtn', "()=>!!document.querySelector('#indexSheet.show, #indexList')&&document.querySelectorAll('#indexList .s4-carte').length>3&&document.querySelector('#indexList').getBoundingClientRect().top<500"),
 ('Fil',                    None, '#filBtn', "()=>{const f=document.getElementById('feedView'); return f&&f.classList.contains('in');}"),
 ('Studio',                 None, '#studioBtn', "()=>{const s=document.getElementById('studioScreen'); return s&&s.classList.contains('show')&&s.getBoundingClientRect().top<60;}"),
 ('Aura',                   None, '#souffleBtn', "()=>{const s=document.getElementById('auraScreen'); return s&&s.classList.contains('show')&&s.getBoundingClientRect().top<60;}"),
 ('Partager',               None, '#shareBtn', "()=>{const s=document.getElementById('shareScreen'); return s&&s.classList.contains('show')&&s.getBoundingClientRect().top<60;}"),
 ('Réglages',               None, '#settingsBtn', "()=>{const s=document.getElementById('settingsScreen'); return s&&s.classList.contains('show')&&s.getBoundingClientRect().top<60;}"),
 ('Cercle',                 'reglages', '#openPlusTop', "()=>{const s=document.getElementById('plusScreen'); return s&&s.classList.contains('show')&&s.getBoundingClientRect().top<60;}"),
]
def prepare(pg, etat):
    if etat=='plus':
        pg.mouse.click(*centre(pg,'#createBtn')); pg.wait_for_timeout(700)
    elif etat=='pageplus':
        pg.mouse.click(*centre(pg,'#createBtn')); pg.wait_for_timeout(600)
        pg.mouse.click(*centre(pg,'#accChoix .acc-pil[data-k=promi]')); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const t=document.getElementById('fTitle'); t.value='essai de latence'; t.dispatchEvent(new Event('input',{bubbles:true})); window.__n0=Toile.count(); }")
    elif etat=='reglages':
        pg.mouse.click(*centre(pg,'#settingsBtn')); pg.wait_for_timeout(1500)
    elif etat=='fiche':
        pg.evaluate("()=>{ const p=promises.find(p=>p.chiche&&!p.draft); openDetail(p.id); }"); pg.wait_for_timeout(1800)
res={}
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    cdp=None
    if PROF: cdp=ctx.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':200})
    APP=next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')),'app.html'); pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(9000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(1500)
    PASSES=2 if '--deux' in sys.argv else 1
    for passe_n in range(PASSES):
     if passe_n: pg.wait_for_timeout(6000)
     for nom,etat,cible,cond in ACTIONS:
         if SEUL and SEUL not in nom: continue
         ferme(pg); prepare(pg, etat)
         if cible=='DALLE':
             xy=pg.evaluate("()=>{ const P=promises.filter(p=>!p.draft); for(const q of P){ const D=Toile.dalleAbs(q.id), V=Toile.vue(), cv=document.getElementById('toileCv').getBoundingClientRect(); if(!D) continue; const x=cv.left+(D.minx+D.w/2)*V.s+V.ox, y=cv.top+(D.miny+D.h/2)*V.s+V.oy; if(y>250&&y<650&&x>60&&x<370){ const h=Toile.hit(x-cv.left,y-cv.top); if(h&&h.pid===q.id) return [x,y]; } } return null; }")
         elif cible=='GESTE':
             xy=pg.evaluate("()=>{ const z=document.getElementById('planterZone'); const r=z.getBoundingClientRect(); return r.width>10?[r.left, r.top+r.height/2, r.width]:null; }")
         elif cible=='DISQUE':
             xy=pg.evaluate("()=>{ const k=document.querySelectorAll('#detailPoster .kring:not(.kring-moi)')[0]; if(!k) return null; const r=k.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
         else: xy=centre(pg,cible)
         if not xy: res[nom]={'erreur':'cible absente'}; print(nom,'cible absente'); continue
         pg.evaluate(INSTALLE); pg.evaluate("c=>{ window.__cond=eval(c); }", cond)
         if PROF: cdp.send('Profiler.start')
         if cible=='GESTE':
             pg.evaluate("()=>{window.__surLeve=1;}")
             x0,y0,w=xy; pg.mouse.move(x0+12,y0); pg.mouse.down()
             for i in range(1,26): pg.mouse.move(x0+12+(w-24)*i/25, y0); pg.wait_for_timeout(12)
             pg.mouse.up(); pg.wait_for_timeout(1800); pg.evaluate("()=>{window.__surLeve=0;}")
         else:
             pg.mouse.click(*xy); pg.wait_for_timeout(1600)
         r=pg.evaluate(LIT)
         if PROF:
             prof=cdp.send('Profiler.stop')['profile']; nodes={n['id']:n for n in prof['nodes']}; self=collections.Counter()
             dt=prof['timeDeltas']; 
             for sid,d in zip(prof['samples'],dt):
                 n=nodes[sid]['callFrame']; key=(n['functionName'] or '(anon)')+' l.'+str(n['lineNumber']+1) if 'app.html' in n['url'] else (n['functionName'] or n['url'][-20:] or '(prog)')
                 self[key]+=d/1000
             r['top']=[(k,round(v)) for k,v in self.most_common(8) if k not in ('(idle)','(program)','(garbage collector)') or v>40][:7]
         res[('2e · ' if passe_n else '')+nom]=r; print(('2e · ' if passe_n else '')+nom, json.dumps(r, ensure_ascii=False))
    b.close()
APP=next((a.split('=')[1] for a in sys.argv if a.startswith('--app=')),'app.html'); json.dump(res, open('/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/sauvegardes/latences-v59/'+('webkit' if WK else 'chromium')+'-'+APP.replace('.html','')+'.json','w'), ensure_ascii=False, indent=1)
