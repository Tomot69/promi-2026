# Les deux pièces manquantes : le TRAIT ENTIER (une parole tenue — les deux moitiés jointes), rogné AU-DESSUS des mots ;
# et la RANGÉE D'ANNEAUX en entier (le tien et ceux des personnes). On note tout chiffre visible.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ANNEAUX = r"""()=>{ const z=document.getElementById('dAura'); if(!z) return null; const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, r=z.getBoundingClientRect();
  const K=[...z.querySelectorAll('.kring')].map(k=>{ const q=k.getBoundingClientRect(); return {p:k.getAttribute('data-p'), vis:k.checkVisibility(), r:[Math.round((q.left-dv.left)/s), Math.round((q.top-dv.top)/s), Math.round(q.width/s), Math.round(q.height/s)]}; });
  const txt=[]; const w=document.createTreeWalker(z,NodeFilter.SHOW_TEXT); let n; while((n=w.nextNode())){ const t=n.textContent.trim(); if(t && n.parentElement.checkVisibility()) txt.push(t.slice(0,20)); }
  return {boite:[Math.round((r.left-dv.left)/s), Math.round((r.top-dv.top)/s), Math.round(r.width/s), Math.round(r.height/s)], anneaux:K, textes:txt, chiffres:txt.filter(t=>/[0-9]/.test(t))}; }"""
TRAIT = r"""()=>{ const z=document.getElementById('tenirZone'); if(!z) return null; const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, r=z.getBoundingClientRect();
  let basMots=null; const w=document.createTreeWalker(z,NodeFilter.SHOW_TEXT); let n;
  while((n=w.nextNode())){ const t=n.textContent.trim(); if(!t || !n.parentElement.checkVisibility()) continue; const g=document.createRange(); g.selectNodeContents(n); const q=g.getBoundingClientRect(); if(q.height>1) basMots = basMots===null ? q.top : Math.min(basMots, q.top); }
  return {x:r.left, y:r.top, w:r.width, h:r.height, hautMots:basMots, w390:+(r.width/s).toFixed(1), h390:+(r.height/s).toFixed(1), motsA:basMots?+((basMots-r.top)/s).toFixed(1):null}; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        for cas, choix in (('tenu', "promises.find(q=>!q.draft && q.status==='tenu' && q.who && q.who!=='moi' && !q.nuee)"),
                           ('encours', "promises.find(q=>!q.draft && q.status==='encours' && q.who && q.who!=='moi' && !q.nuee)")):
            pg.evaluate(BASE); pg.evaluate("(c)=>{ const p=eval(c); if(p) openDetail(p.id); }", choix); pg.wait_for_timeout(1900)
            t = pg.evaluate(TRAIT); a = pg.evaluate(ANNEAUX)
            R['%s · %s' % (th, cas)] = {'trait': t and {k: t[k] for k in ('w390', 'h390', 'motsA')}, 'anneaux': a}
            print('%-5s %-8s trait %sx%s (mots à %s) · anneaux %s · chiffres %s' % (th, cas, t and t['w390'], t and t['h390'], t and t['motsA'], a and [k['p'] for k in a['anneaux'] if k['vis']], a and a['chiffres']))
            if t and t['w'] > 4:
                h = (t['hautMots'] - t['y'] - 6) if t['hautMots'] else t['h']
                pg.screenshot(path=os.path.join(OUT, '%s_trait_%s.png' % (th, cas)), clip={'x': t['x'], 'y': t['y'], 'width': t['w'], 'height': max(40, h)})
            if a and a['boite'][2] > 4:
                dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390];}")
                pg.screenshot(path=os.path.join(OUT, '%s_anneaux_%s.png' % (th, cas)),
                              clip={'x': dv[0] + a['boite'][0] * dv[2], 'y': dv[1] + a['boite'][1] * dv[2], 'width': a['boite'][2] * dv[2], 'height': a['boite'][3] * dv[2]})
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'pieces2.json'), 'w'), ensure_ascii=False, indent=1)
