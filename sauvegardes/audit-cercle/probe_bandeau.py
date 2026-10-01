# LE BANDEAU ✕ FERMER DU PEAUFINER — qu'est-ce qui est au PRODUIT, qu'est-ce qui vient de MA maquette ? (Tom, 11 sept.)
# Chemin UTILISATEUR seulement : des touchers au point (souris), AUCUNE retouche de page, aucun _phrase posé à la main
# pour la variante « pure ». Une seconde variante pose la phrase comme le fait releve-S3 (convention des juges), pour
# voir si la longueur du titre change le défaut. Pour chaque écran : les nœuds texte visibles dans le haut (y < 300),
# les paires qui se recouvrent CONFIRMÉES AU DOIGT (elementsFromPoint au centre de l'intersection), et le rond photo.
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'bandeau'); os.makedirs(OUT, exist_ok=True)
HAUT = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, H=document.querySelector(hote);
  const nom=(e)=>e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).trim().split(/\s+/).join('.');
  const T=[]; H.querySelectorAll('*').forEach(e=>{ if(!e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return;
    let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent; own=own.replace(/\s+/g,' ').trim();
    const r=e.getBoundingClientRect(); const y=(r.top-dv.top)/s; if(y>300||r.width<1) return;
    const cs=getComputedStyle(e);
    const deco=parseFloat(cs.borderTopWidth)>0||cs.backgroundColor!=='rgba(0, 0, 0, 0)';
    if(!own && !deco && e.tagName!=='BUTTON') return;
    T.push({n:nom(e).slice(0,70), t:own.slice(0,40), x:+((r.left-dv.left)/s).toFixed(1), y:+y.toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1),
            bd:cs.borderTopWidth, bg:cs.backgroundColor, pos:cs.position, _r:[r.left,r.top,r.right,r.bottom], _e:e}); });
  const rec=[]; const txt=T.filter(a=>a.t);
  for(let i=0;i<txt.length;i++) for(let j=i+1;j<txt.length;j++){ const a=txt[i]._r,b=txt[j]._r;
    const x0=Math.max(a[0],b[0]), y0=Math.max(a[1],b[1]), x1=Math.min(a[2],b[2]), y1=Math.min(a[3],b[3]);
    if(x1-x0>1&&y1-y0>1){ if(txt[i]._e.contains(txt[j]._e)||txt[j]._e.contains(txt[i]._e)) continue;
      const pile=document.elementsFromPoint((x0+x1)/2,(y0+y1)/2);
      const ai=pile.some(p=>p===txt[i]._e||txt[i]._e.contains(p)), bj=pile.some(p=>p===txt[j]._e||txt[j]._e.contains(p));
      rec.push({a:txt[i].n+' « '+txt[i].t+' »', b:txt[j].n+' « '+txt[j].t+' »', au_doigt: ai&&bj}); } }
  // le rond photo : ce qui est sous le doigt là où les captures le montraient (x 349, y 247)
  const px=dv.left+349*s, py=dv.top+247*s; const sous=document.elementsFromPoint(px,py).slice(0,4).map(nom);
  return {noeuds:T.map(({_r,_e,...o})=>o), recouvrements:rec, sous_349_247:sous}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def clic(sel):
        b = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}", sel)
        if b: pg.mouse.click(b[0], b[1])
        return b
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        for variante in ('pure', 'phrase'):
            pg.evaluate("()=>{ try{closeAll();}catch(e){} }"); pg.wait_for_timeout(300)
            clic('#createBtn'); pg.wait_for_timeout(700)
            clic('#createSheet .tile'); pg.wait_for_timeout(1000)
            if variante == 'phrase':
                pg.evaluate("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu();}"); pg.wait_for_timeout(600)
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s_pageplus.png' % (th, variante)))
            clic('#csBotBar'); pg.wait_for_timeout(1600)
            r = pg.evaluate(HAUT, '#createSheet'); pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s_pageplus_peauf.png' % (th, variante)))
            R['%s_%s_pageplus_peauf' % (th, variante)] = r
            print('\n== %s · %s · Peaufiner de la page +\n   recouvrements : %s\n   sous (349,247) : %s' % (th, variante,
                  [x['a'] + ' ↔ ' + x['b'] + (' [AU DOIGT]' if x['au_doigt'] else '') for x in r['recouvrements']], r['sous_349_247']))
            for n in r['noeuds']:
                if n['t'] or n['bd'] != '0px': print('     %-58s %-28s x %6.1f y %6.1f  %5.1f×%-5.1f bd %s pos %s' % (n['n'], n['t'], n['x'], n['y'], n['w'], n['h'], n['bd'], n['pos']))
        # la fiche, pour comparer : son Peaufiner, en haut
        pg.evaluate("()=>{ try{closeAll();}catch(e){} openDetail(126); }"); pg.wait_for_timeout(1500)
        clic('#dpDetails .dpd-tog'); pg.wait_for_timeout(1600)
        pg.evaluate("()=>{const c=document.querySelector('#detailPoster .dpd-corps'); if(c) c.scrollTop=0;}"); pg.wait_for_timeout(400)
        r = pg.evaluate(HAUT, '#detailPoster'); pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_fiche_peauf.png' % th))
        R['%s_fiche_peauf' % th] = r
        print('\n== %s · Peaufiner d’une fiche (126), en haut\n   recouvrements : %s' % (th, [x['a'] + ' ↔ ' + x['b'] + (' [AU DOIGT]' if x['au_doigt'] else '') for x in r['recouvrements']]))
    br.close()
json.dump(R, open(os.path.join(OUT, 'bandeau.json'), 'w'), ensure_ascii=False, indent=1)
