# Audit : toute surface VISIBLE dans l'appareil qui porte une couleur d'état (texte, fond, bord, remplissage ou trait SVG).
# On ne juge pas ici : on liste, avec le contexte, pour trier à l'œil ce qui est un état et ce qui ne l'est pas.
import json, sys
from playwright.sync_api import sync_playwright
ETATS = {'#DD4D23': 'à tenir', '#291547': 'en cours (plein) / violet Nuée', '#A77CF7': 'en cours (clair)',
         '#00341A': 'tenu (plein)', '#33BA6C': 'tenu (clair)', '#8FE08F': 'amande (célébration seule)'}
PORTES = [
 ('accueil', "()=>{closeAll();}"),
 ('Index', "()=>{closeAll(); setView('toile'); ouvrirIndex();}"),
 ('Fil', "()=>{closeAll(); setView('fil');}"),
 ('fiche tenue', "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours', "()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche', "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('Peaufiner', "()=>{closeAll(); const p=promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('Nuée', "()=>{closeAll(); openEssaim('potager');}"),
 ('page +', "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Studio', "()=>{closeAll(); document.getElementById('studioBtn').click();}"),
 ('Aura', "()=>{closeAll(); document.getElementById('auraBtn')&&document.getElementById('auraBtn').click();}"),
 ('Réglages', "()=>{closeAll(); document.getElementById('settingsBtn').click();}"),
 ('Partager', "()=>{closeAll(); document.getElementById('shareScreen').classList.add('show'); shareRender();}"),
]
J = r"""(E)=>{ const dv=document.getElementById('device').getBoundingClientRect(); const out=[];
 const hex=c=>{ const m=(c||'').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/); if(!m) return null; if(m[4]!==undefined&&parseFloat(m[4])<0.05) return null;
   return '#'+[m[1],m[2],m[3]].map(x=>(+x).toString(16).padStart(2,'0')).join('').toUpperCase(); };
 const vu=e=>{ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return false; if(r.bottom<dv.top||r.top>dv.bottom||r.right<dv.left||r.left>dv.right) return false;
   let x=e; while(x&&x!==document.body){ const c=getComputedStyle(x); if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false; x=x.parentElement; }
   const cx=Math.min(Math.max(r.left+r.width/2,dv.left+1),dv.right-1), cy=Math.min(Math.max(r.top+r.height/2,dv.top+1),dv.bottom-1);
   const t=document.elementFromPoint(cx,cy); return !!t && (t===e||e.contains(t)||t.contains(e)); };
 for(const e of document.querySelectorAll('#device *, .frame *')){
   if(e.tagName==='CANVAS'||e.tagName==='SCRIPT'||e.tagName==='STYLE') continue;
   const c=getComputedStyle(e); const props={};
   const txt=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
   if(txt) props.texte=hex(c.color);
   props.fond=hex(c.backgroundColor);
   if(parseFloat(c.borderTopWidth)>0) props.bord=hex(c.borderTopColor);
   if(e instanceof SVGElement){ props.fill=hex(c.fill); props.stroke=(c.stroke&&c.stroke!=='none')?hex(c.stroke):null; }
   if(c.boxShadow&&c.boxShadow!=='none'){ const m=c.boxShadow.match(/rgba?\([^)]*\)/g); if(m) props.ombre=m.map(hex).filter(Boolean).join(','); }
   if(c.outlineStyle!=='none'&&parseFloat(c.outlineWidth)>0) props.outline=hex(c.outlineColor);
   const hit=Object.entries(props).filter(([k,v])=>v&&E.some(h=>v.indexOf(h)>=0));
   if(!hit.length||!vu(e)) continue;
   let id='',h=e; while(h&&!id){id=h.id;h=h.parentElement;}
   out.push({ou:id, el:e.tagName.toLowerCase()+'.'+String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).slice(0,40), txt:(e.textContent||'').trim().slice(0,30), hit:hit.map(([k,v])=>k+' '+v).join(' ; ')}); }
 return out; }"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        for nom, porte in PORTES:
            pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
            pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th)
            try: pg.evaluate(porte)
            except Exception as e: print(th, nom, 'PORTE KO', str(e)[:80]); pg.close(); continue
            pg.wait_for_timeout(2200)
            for r in pg.evaluate(J, list(ETATS)):
                k = (r['ou'], r['el'], r['hit'])
                res.setdefault(k, []).append(th + ':' + nom)
                if len(res[k]) == 1: print(th, nom, '|', r['ou'], r['el'], '«' + r['txt'] + '»', '|', r['hit'])
            pg.close()
    b.close()
json.dump({' | '.join(k): v for k, v in res.items()}, open('scratchpad/perf/etats_audit.json', 'w'), ensure_ascii=False, indent=1)
print('TOTAL distincts', len(res))
