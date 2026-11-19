# ⚑ v207 (C-296, Tom, 17 nov. 2026) — « un rectangle parasite paraît et disparaît sur le « Je » ». Page + d'un Promi, image par image : trois tours de la bascule
# du sens (« Je me promets » → « Je promets à qui ? » → « qui ?, promets-moi » → « Je me promets »), puis la frappe d'un titre, son effacement, sa validation.
# À chaque image, chaque élément qui PEINT (fond, filet, contour, ombre ; pas un canevas de tracé) et dont la boîte coupe le « Je » ; un élément qui quitte la
# page (retiré, caché) alors que son filet ou son fond se voit encore a disparu d'un coup : rouge. Rouge sur v205 (la pastille « qui ? » qui part, à la bascule 3).
# Usage : python3 redteam_je.py [--fichier=zz-v205b.html] [--tours=3]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]; F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html'); TOURS = int(next((a.split('=', 1)[1] for a in A_ if a.startswith('--tours=')), '3'))
REC = r"""()=>{ window.__R=[]; const sc=document.getElementById('createSheet'), U=new WeakMap(); let n=0; const uid=e=>{ if(!U.has(e)) U.set(e,++n); return U.get(e); };
 function jeRect(){ const b=document.querySelector('#csPhrase [data-ph=sens]'); if(!b) return null; const w=document.createTreeWalker(b,NodeFilter.SHOW_TEXT); let x; while((x=w.nextNode())&&!x.data.trim()); if(!x) return null;
   const i=x.data.search(/\S/); const r=document.createRange(); r.setStart(x,i); r.setEnd(x,Math.min(x.data.length,i+2)); const q=r.getBoundingClientRect(); return [q.left,q.top,q.right,q.bottom]; }
 function poids(cs){ let p=0; const bg=cs.backgroundColor, m=bg&&bg.match(/rgba?\(([^)]+)\)/); if(m){ const v=m[1].split(',').map(parseFloat); if(v.length<4||v[3]>0.05) p=Math.max(p,1); }
   if(cs.borderTopStyle!=='none') p=Math.max(p, parseFloat(cs.borderTopWidth)||0); if(cs.outlineStyle!=='none') p=Math.max(p, parseFloat(cs.outlineWidth)||0); if(cs.boxShadow&&cs.boxShadow!=='none') p=Math.max(p,1); return p; }
 const vus=new Map();
 (function f(t){ const J=jeRect();
   const partis=[]; for(const [e,o] of vus){ let parti=!e.isConnected; if(!parti){ const cs=getComputedStyle(e); parti=cs.display==='none'||cs.visibility==='hidden'; } if(parti){ partis.push(o); vus.delete(e); } }
   if(J) for(const e of sc.querySelectorAll('*')){ if(e.tagName==='CANVAS') continue; const r=e.getBoundingClientRect(); if(!r.width||r.right<=J[0]||r.left>=J[2]||r.bottom<=J[1]||r.top>=J[3]){ vus.delete(e); continue; }
     const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'){ continue; } let op=1, a=e; while(a&&a!==document.body){ op*=parseFloat(getComputedStyle(a).opacity); a=a.parentElement; }
     const p=poids(cs); if(p>0.5&&op>0.05) vus.set(e,{nom:e.tagName.toLowerCase()+'.'+String(e.className).trim().split(/\s+/).join('.')+(e.dataset.ph?'[ph='+e.dataset.ph+']':''), cls:e.tagName+'|'+(e.dataset.ph||''), r:[r.left,r.top,r.width,r.height], poids:p, op:op}); else vus.delete(e); }
   /* un nœud rebâti à l'identique (la phrase se recompose : même place, même rôle, à 2 pt près) n'est pas un départ */
   for(const o of partis){ let remplace=false; const ph=o.cls.split('|')[1]; if(ph){ const e3=sc.querySelector('[data-ph="'+ph+'"]'); if(e3&&e3.getBoundingClientRect().width) remplace=true; }   /* la même place de la phrase, rebâtie (sa transition est jugée ailleurs) */
     if(!remplace) for(const [e2,o2] of vus){ if(o2.cls===o.cls && o2.r.every((v,i)=>Math.abs(v-o.r[i])<=2)){ remplace=true; break; } } if(!remplace) window.__R.push({t:Math.round(t), quoi:o.nom, poids:o.poids, op:o.op}); }
   if(window.__on!==false) requestAnimationFrame(f); })(performance.now()); }"""
R = []; ok_n = 0; tot = 0
def juge(nom, ok, d=''):
    global ok_n, tot
    tot += 1; ok_n += bool(ok); print(('✅ ' if ok else '❌ ') + nom + ('' if ok else '  ' + str(d)[:300]))
def releve(pg): return pg.evaluate("()=>{ const r=window.__R; window.__R=[]; return r; }")
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_je — %s · charge %.1f' % (F, B.charge()))
    for ech, (vw, vh) in (('1', (390, 844)), ('0,79', (330, 714))):
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, attente=7000)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(3500)
        pg.evaluate(REC); pg.wait_for_timeout(600); releve(pg)
        for i in range(TOURS * 3):
            B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(2400); r = releve(pg)
            juge('[%s] bascule %d : rien ne quitte le « Je » d’un coup' % (ech, i + 1), not r, r[:3])
        for i in range(2):
            B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500); pg.keyboard.type('marcher', delay=60); pg.wait_for_timeout(1500)
            for _ in range(9): pg.keyboard.press('Backspace'); pg.wait_for_timeout(50)
            pg.wait_for_timeout(2500); pg.keyboard.press('Enter'); pg.wait_for_timeout(2200); r = releve(pg)
            juge('[%s] frappe, effacement, validation %d : rien ne quitte le « Je » d’un coup' % (ech, i + 1), not r, r[:3])
        ctx.close()
    b.close()
print('\nredteam_je : %d/%d' % (ok_n, tot))
sys.exit(0 if ok_n == tot else 1)
