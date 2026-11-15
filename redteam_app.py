"""⚑ v202a (Tom, C-276) — LA RED TEAM DE TOUTE L'APP, SANS INDULGENCE. Un relevé, pas un verdict : il parcourt chaque écran (l'accueil, la page + des trois
natures, les fiches des trois natures et leur Peaufiner, l'Index, le Fil, l'Aura, les Réglages, Soutenir, Partager, le Studio sous six mondes), dans les deux
thèmes, à l'échelle 1 (430 × 932), à 0,79 (330 × 714) et dans la fenêtre de Tom (390 × 651, l'état exporté), et relève :
  E · les erreurs JavaScript (pageerror) et celles de la boîte noire (`_boiteNoire.lire()`) ;
  D · un texte visible qui sort de l'appareil (au-delà de 1 pt) ;
  C · un texte coupé : son contenu est plus large ou plus haut que sa boîte qui rogne (overflow hidden), sans « … » voulu ;
  R · deux textes visibles qui se recouvrent (plus de 30 % de la plus petite boîte d'encre), hors d'un même mot.
Chaque relevé est ensuite JUGÉ à l'œil (RED-TEAM.md) : un recouvrement voulu (une pastille sur sa carte) n'est pas un défaut.
--fichier= · --vues=1,079,tom · --themes=clair,sombre · --vite (sans le Studio)"""
import sys, os, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
VUES = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--vues=')), ['1', '079', 'tom'])
THEMES = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--themes=')), ['clair', 'sombre'])
VITE = '--vite' in A
SORTIE = 'scratchpad/v202/redteam-app-%s-%s.json' % (F.replace('.html', ''), '-'.join(VUES))

RELEVE = r"""()=>{ const dv=document.getElementById('device'); if(!dv) return null; const D=dv.getBoundingClientRect(), k=D.width/390, out={D:[],C:[],R:[]};
  const vis=e=>{ for(let x=e;x&&x.nodeType===1;x=x.parentElement){ const s=getComputedStyle(x); if(s.display==='none'||s.visibility==='hidden'||+s.opacity<0.05) return false; } return true; };
  const nom=e=>{ let s=e.tagName.toLowerCase(); if(e.id) s+='#'+e.id; else if(e.className&&typeof e.className==='string') s+='.'+e.className.trim().split(/\s+/).slice(0,2).join('.'); const p=e.closest('[id]'); return (p&&p!==e?p.id+' › ':'')+s; };
  const T=[]; const w=document.createTreeWalker(document.querySelector('.frame')||document.body, NodeFilter.SHOW_TEXT); let t, n=0;
  while((t=w.nextNode()) && n<2500){ const v=t.nodeValue.trim(); if(!v) continue; const e=t.parentElement; if(!e) continue;
    const rg=document.createRange(); rg.selectNodeContents(t); const rs=[...rg.getClientRects()].filter(q=>q.width>1&&q.height>1); if(!rs.length) continue;
    const r=rg.getBoundingClientRect(); if(r.bottom<D.top||r.top>D.bottom||r.right<D.left||r.left>D.right) continue;
    { const hit=document.elementFromPoint(Math.min(D.right-1,Math.max(D.left+1,r.left+r.width/2)), Math.min(D.bottom-1,Math.max(D.top+1,r.top+r.height/2)));
      if(!hit || !(hit===e || e.contains(hit) || hit.contains(e))) continue; }   /* recouvert par un écran : pas à l'écran */
    if(!vis(e)) continue; n++;
    const it={e:e, v:v.slice(0,40), r:r, rs:rs};
    T.push(it);
    if(r.left<D.left-k||r.right>D.right+k||r.top<D.top-k||r.bottom>D.bottom+k) out.D.push([nom(e), it.v, Math.round((r.left-D.left)/k), Math.round((r.right-D.left)/k), Math.round((r.top-D.top)/k)]);
    for(let x=e;x&&x!==dv;x=x.parentElement){ const s=getComputedStyle(x); if((s.overflow+s.overflowX+s.overflowY).indexOf('hidden')<0) continue; const xr=x.getBoundingClientRect();
      if(r.right>xr.right+2*k||r.left<xr.left-2*k||r.bottom>xr.bottom+2*k||r.top<xr.top-2*k){ if(!/…$/.test(v) && s.textOverflow!=='ellipsis' && x.scrollHeight<=x.clientHeight+2 && x.scrollWidth<=x.clientWidth+2) out.C.push([nom(e), it.v, nom(x)]); }
      break; } }
  for(let i=0;i<T.length;i++) for(let j=i+1;j<T.length;j++){ const a=T[i], b=T[j]; if(a.e===b.e||a.e.contains(b.e)||b.e.contains(a.e)) continue;
    let inter=0; for(const p of a.rs) for(const q of b.rs){ const w2=Math.min(p.right,q.right)-Math.max(p.left,q.left), h2=Math.min(p.bottom,q.bottom)-Math.max(p.top,q.top); if(w2>0&&h2>0) inter+=w2*h2; }
    if(!inter) continue; const sa=a.rs.reduce((s,q)=>s+q.width*q.height,0), sb=b.rs.reduce((s,q)=>s+q.width*q.height,0);
    if(inter>0.30*Math.min(sa,sb)) out.R.push([nom(a.e), a.v, nom(b.e), b.v, Math.round(100*inter/Math.min(sa,sb))]); }
  let bn=[]; try{ bn=(window._boiteNoire?_boiteNoire.lire():[]).filter(x=>/err|rej/i.test(JSON.stringify(x).slice(0,60))).map(x=>JSON.stringify(x).slice(0,200)); }catch(_){ }
  out.E=bn; return out; }"""

def ecrans(pg):
    """(nom, ouverture) — chaque ouverture part de l'accueil (closeAll), par le chemin de l'app"""
    L = [('accueil', "()=>{}")]
    for k in ('promi', 'chiche', 'nuee'):
        L.append(('page+ ' + k, "async ()=>{ document.getElementById('createBtn').click(); await new Promise(r=>setTimeout(r,700)); const x=document.querySelector('.acc-pil[data-k=%s]'); if(x) x.click(); }" % k))
    L += [('fiche promi', "()=>{ const p=promises.find(q=>!q.chiche&&!q.nuee&&!q.draft); if(p) openDetail(p.id); }"),
          ('fiche chiche', "()=>{ const p=promises.find(q=>q.chiche&&!q.draft); if(p) openDetail(p.id); }"),
          ('fiche cercle', "()=>{ const k=Object.keys(NUE).find(x=>x!=='soi'); if(k) openNueeDetail(k); }"),
          ('peaufiner promi', "async ()=>{ const p=promises.find(q=>!q.chiche&&!q.nuee&&!q.draft); if(p) openDetail(p.id); await new Promise(r=>setTimeout(r,1500)); const b=document.getElementById('dpDetails'); if(b) b.click(); }"),
          ('index', "()=>{ ouvrirIndex(); }"),
          ('fil', "()=>{ document.getElementById('filBtn').click(); }"),
          ('aura', "()=>{ document.getElementById('souffleBtn').click(); }"),
          ('reglages', "()=>{ document.getElementById('settingsBtn').click(); }"),
          ('partager', "()=>{ document.getElementById('shareBtn').click(); }")]
    if not VITE:
        for m in ('encre', 'touffe', 'mascaret', 'ramage', 'esquille', 'houle'):
            L.append(('studio ' + m, "async ()=>{ try{ Toile.setTheme('%s'); }catch(e){} document.getElementById('studioBtn').click(); }" % m))
    return L

res = []
with sync_playwright() as p:
    b = p.webkit.launch()
    for vue in VUES:
        for th in THEMES:
            if vue == 'tom':
                ctx, _d = B.contexte_tom(b, sombre=(th == "sombre"))
            else:
                vw, vh = (430, 932) if vue == '1' else (330, 714)
                ctx = B.contexte(b, sombre=(th == 'sombre'), vw=vw, vh=vh); B.toile_pleine(ctx, 10)
            ctx.add_init_script("(()=>{let a=777; Math.random=function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};})()")   # le même hasard pour deux versions
            pg = B.ouvre(ctx, F)
            for nom, js in ecrans(pg):
                try:
                    pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ closeAll(); }catch(e){} document.querySelectorAll('#auraScreen.show .closeb, #studioScreen.show .closeb').forEach(x=>{ if(x.getBoundingClientRect().top<300) x.click(); }); }")
                    pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(2600)
                    r = pg.evaluate(RELEVE)
                except Exception as e:
                    r = {'D': [], 'C': [], 'R': [], 'E': ['juge : ' + str(e)[:160]]}
                r = r or {'D': [], 'C': [], 'R': [], 'E': []}
                r['E'] = list(r['E']) + pg.__dict__['erreurs']; pg.__dict__['erreurs'] = []
                n = sum(len(r[x]) for x in 'DCRE')
                print('%-4s %-6s %-16s E%d D%d C%d R%d' % (vue, th, nom, len(r['E']), len(r['D']), len(r['C']), len(r['R'])), flush=True)
                for x in 'EDCR':
                    for it in r[x][:6]: print('      ', x, it, flush=True)
                res.append({'vue': vue, 'theme': th, 'ecran': nom, **r})
            ctx.close()
    b.close()
json.dump(res, open(SORTIE, 'w'), ensure_ascii=False, indent=0)
print('relevé :', SORTIE, '·', sum(len(r['E']) for r in res), 'erreurs,', sum(len(r['D']) for r in res), 'débordements,', sum(len(r['C']) for r in res), 'coupes,', sum(len(r['R']) for r in res), 'recouvrements')
