"""collisions.py — LES TEXTES QUI SE TOUCHENT, SUR TOUS LES ÉCRANS, DANS LES DEUX THÈMES.

C'est la dernière liste de CASSE.md : « les textes qui se touchent dans l'Index », « les
commentaires qui sortent de leur ligne ». On ne mesure pas des cotes : on demande au
navigateur si deux textes se recouvrent, et de combien.
"""
import sys
from playwright.sync_api import sync_playwright
APP = "http://127.0.0.1:8752/app.html"

SUP = r"""(racine)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  /* ⚠ ON CHERCHE D'ABORD L'ÉCRAN QUI EST DEVANT, ET ON NE REGARDE QUE LUI.
     Le dock, la barre d'état et les écrans fermés gardent leurs nœuds en `display:block` :
     ils sont RECOUVERTS, pas cachés. Les compter donnait 269 « collisions » dont aucune ne
     se voit. Et écarter un à un ce qui n'est pas au-dessus ne marche pas non plus : dans une
     VRAIE collision, c'est justement le texte du dessous qu'on écarterait — la collision
     disparaîtrait de la mesure. On prend donc la feuille la plus haute qui couvre l'écran,
     et on compare ses textes ENTRE EUX : ils sont tous dans le même plan. */
  const pile=document.elementsFromPoint(dev.left+dev.width/2, dev.top+dev.height*0.55);
  let h=null;
  for(const e of pile){ const r=e.getBoundingClientRect();
    if(r.width*r.height >= dev.width*dev.height*0.55){ h=e; break; } }
  if(!h) h=document.getElementById('device');
  const vis=e=>{const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return false;
    const r=e.getBoundingClientRect();
    if(r.width<6||r.height<6) return false;
    if(r.bottom<dev.top+2||r.top>dev.bottom-2||r.right<dev.left+2||r.left>dev.right-2) return false;
    return true;};
  const f=[...h.querySelectorAll('*')].filter(e=>{ if(!vis(e)) return false;
    if(['CANVAS','IMG','SVG','INPUT','TEXTAREA'].includes(e.tagName)) return false;
    const t=(e.textContent||'').trim(); if(!t) return false;
    return [...e.children].every(c=>['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(c.tagName));});
  const box=e=>{const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc,y:(r.top-dev.top)/sc,w:r.width/sc,h:r.height/sc};};
  const out=[];
  for(let i=0;i<f.length;i++) for(let j=i+1;j<f.length;j++){
    const a=f[i],b=f[j]; if(a.contains(b)||b.contains(a)) continue;
    const A=box(a),B=box(b);
    const ix=Math.max(0,Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x));
    const iy=Math.max(0,Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y));
    if(ix<3||iy<3) continue;
    const part=ix*iy/Math.min(A.w*A.h,B.w*B.h);
    if(part<0.30) continue;
    out.push('['+h.id+'.'+(''+h.className).split(' ')[0]+'] '+Math.round(part*100)
             +'% · «'+((a.textContent||'').trim().slice(0,22))
             +'» ⨯ «'+((b.textContent||'').trim().slice(0,22))+'»');}
  return [...new Set(out)].slice(0,8);}"""

ECRANS = [
 ('toile',        "()=>{closeAll(); setView('toile');}"),
 ('fiche tenue',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',"()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche', "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('fiche + commentaires',"()=>{closeAll(); const p=promises.filter(q=>q.comments&&q.comments.length)[0]||promises.filter(q=>!q.draft)[0]; if(p)openDetail(p.id);}"),
 ('Peaufiner',    "()=>{closeAll(); const p=promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('page +',       "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Index 2',      "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('Index 3',      "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
 ('Index tri',    "()=>{closeAll(); setView('toile'); ouvrirIndex(); setTimeout(()=>{const b=document.getElementById('ixTriBtn'); if(b)b.click();},700);}"),
 ('Fil',          "()=>{closeAll(); setView('fil');}"),
 ('Nuée',         "()=>{closeAll(); openEssaim('potager');}"),
 ('Nuée vide',    "()=>{closeAll(); openEssaim('atelier');}"),
 ('Nuée Peaufiner',"()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('Studio',       "()=>{closeAll(); if(window.ouvrirStudio)ouvrirStudio(); else {const b=document.getElementById('studioBtn'); if(b)b.click();}}"),
 ('Aura',         "()=>{closeAll(); const b=document.getElementById('souffleBtn'); if(b)b.click();}"),
 ('Partager',     "()=>{closeAll(); const b=document.getElementById('shareBtn')||document.querySelector('[data-nav=\"share\"]'); if(b)b.click();}"),
 ('Réglages',     "()=>{closeAll(); const b=document.getElementById('setBtn')||document.getElementById('settingsBtn'); if(b)b.click();}"),
]

n = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        for nom, js in ECRANS:
            pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
            try: pg.evaluate(js)
            except Exception as e: print('  ⚠ %s : %s' % (nom, e)); continue
            pg.wait_for_timeout(2400)
            s = pg.evaluate(SUP, None)
            if s:
                n += len(s)
                print('%-18s [%s]' % (nom, th))
                for x in s: print('     ', x)
    print('\nerreurs JS :', er[:3])
    b.close()
print('\n%d collision(s)' % n)
sys.exit(0 if n == 0 else 1)
