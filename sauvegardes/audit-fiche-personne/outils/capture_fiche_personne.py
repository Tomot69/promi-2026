# AUDIT de la fiche de la personne — l'état ACTUEL, rien n'est modifié. Deux thèmes, atteinte comme un doigt l'atteint
# (toucher « Marion » dans la rangée de l'Aura). Captures de l'appareil (430 × 932 → #device 390 × 844 exact), défilée
# pas à pas jusqu'au bout, et l'INVENTAIRE mesuré de chaque élément visible de la fiche (cotes en écran 390).
#   python3 capture_fiche_personne.py URL DOSSIER
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
INVENT = r"""()=>{ const dv=document.getElementById('device'), dr=dv.getBoundingClientRect(), s=dr.width/390;
  const sh=document.getElementById('personSheet'); if(!sh) return {erreur:'pas de #personSheet'};
  const cs=(e)=>getComputedStyle(e), op=(e)=>{ let o=1; for(let x=e;x&&x!==document.body;x=x.parentElement) o*=+cs(x).opacity; return +o.toFixed(2); };
  const R=(e)=>{ const r=e.getBoundingClientRect(); return [+((r.left-dr.left)/s).toFixed(1), +((r.top-dr.top)/s).toFixed(1), +(r.width/s).toFixed(1), +(r.height/s).toFixed(1)]; };
  const out=[]; const tous=[sh, ...sh.querySelectorAll('*')];
  for(const e of tous){ const c=cs(e), r=e.getBoundingClientRect(); if(c.display==='none'||c.visibility==='hidden'||r.width<1||r.height<1) continue;
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
    const bw=parseFloat(c.borderTopWidth)||0, bg=c.backgroundColor, bgi=c.backgroundImage;
    const marque = txt || bw>0 || (bg && bg!=='rgba(0, 0, 0, 0)') || (bgi && bgi!=='none') || ['CANVAS','IMG','SVG','svg','BUTTON','INPUT'].includes(e.tagName);
    if(!marque) continue;
    out.push({tag:e.tagName.toLowerCase(), id:e.id||'', cls:(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'').toString().slice(0,60),
      txt:txt.slice(0,80), box:R(e), ff:c.fontFamily.split(',')[0].replace(/"/g,''), fs:+parseFloat(c.fontSize).toFixed(1), fw:c.fontWeight,
      col:c.color, fill:c.webkitTextFillColor, op:op(e), bg:bg, bgi:bgi&&bgi!=='none'?bgi.slice(0,60):'', bw:bw, bc:c.borderTopColor, rad:c.borderTopLeftRadius,
      pos:c.position, z:c.zIndex}); }
  const st={cls:sh.className, show:sh.classList.contains('show')||sh.classList.contains('open'), scrollH:sh.scrollHeight, clientH:sh.clientHeight, box:R(sh)};
  return {etat:st, elements:out}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
        # le disque de « Marion » : celui dont le centre est le plus près du libellé « Marion »
        pt = pg.evaluate("""()=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()==='Marion'); if(!lb) return null;
            const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
            for(const n of document.querySelectorAll('#auraScreen .au-nb')){ const r=n.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} }
            return best; }""")
        if not pt: print(th, '❌ pas de disque « Marion » dans l\'Aura'); continue
        pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1800)
        inv = pg.evaluate(INVENT)
        if inv.get('erreur'): print(th, '❌', inv['erreur']); continue
        json.dump(inv, open(os.path.join(OUT, th + '-inventaire.json'), 'w'), ensure_ascii=False, indent=1)
        dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
        clip = {'x': dev[0], 'y': dev[1], 'width': dev[2], 'height': dev[3]}
        H, h = inv['etat']['scrollH'], inv['etat']['clientH']; pas = max(1, int(h * 0.8)); y = 0; i = 0
        while True:
            pg.evaluate("(y)=>{document.getElementById('personSheet').scrollTop=y;}", y); pg.wait_for_timeout(500)
            pg.screenshot(path=os.path.join(OUT, '%s-%02d.png' % (th, i)), clip=clip); i += 1
            if y + h >= H or i > 12: break
            y += pas
        pg.evaluate("()=>{document.getElementById('personSheet').scrollTop=0;}")
        print('%-5s fiche ouverte (%s) · %d éléments visibles · défile %d/%d · %d capture(s) · device %.1f×%.1f' % (th, inv['etat']['cls'], len(inv['elements']), H, h, i, dev[2], dev[3]))
        pg.close()
    b.close()
