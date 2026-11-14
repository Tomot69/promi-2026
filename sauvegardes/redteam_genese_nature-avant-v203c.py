"""⚑ v203 (Tom, C-278) — PAGE + : CHANGER DE SENS OU DE NATURE PENDANT LA GENÈSE DU TRAIT.
« La genèse en cours s'interrompt proprement et la nouvelle se fait entière, sans dalle en double ni saut. Ajoute au juge les changements de nature à tous les instants
de la genèse. » WebKit, 390 × 844 ×3, au doigt (banc_tom), Toile de 10 paroles. La parole « lire » validée par Retour, puis à t ∈ {0, 150, 400, 700, 1000, 1400, 2500} ms :
  S · le sens basculé (« Je me promets » ⇄ « Je promets à ») ;  N · la page fermée (✕) et rouverte en Chiche, puis en Cercle.
Une sonde relève CHAQUE IMAGE dans la page (rien n'est lu en différé) :
  A · aucune lettre tracée hors de sa place : chaque canevas d'un tracé (`canvas[data-trace]`) recoupe la boîte de son texte (± 8 pt)
  B · le rail du pinceau, visible, n'est jamais sur l'encre de la phrase, et ne saute jamais (≤ 14 pt d'une image à l'autre) une fois visible
  C · une seule naissance du trait (au plus une invite qui paraît sans retrait entre) ; à la fin, l'invite est là
  D · S : la taille finale de la phrase, la même à chaque instant (et ≥ 30 : la v203 d'avant ce juge tombait à 16) ; « moi » à la place de « qui ? » le trait né
  E · les images de plus de 33 ms : relevées, jugées seulement au calme (charge < 4)
--quoi=S,N · --t=0,700 · --fichier="""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
QUOI = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--quoi=')), ['S', 'N'])
TS = next(([int(x) for x in a.split('=', 1)[1].split(',')] for a in A if a.startswith('--t=')), [80, 250, 450, 700, 1000, 1400, 2500])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
SONDE = r"""()=>{ window.__G={im:[], A:[], B:[], inv:[]}; const R=window.requestAnimationFrame.bind(window); const t0=performance.now(); let av=t0, railAv=null, invAv=false;
  const D=()=>document.getElementById('device').getBoundingClientRect();
  const op=e=>{ let o=1; for(let x=e;x&&x.nodeType===1;x=x.parentElement){ const c=getComputedStyle(x); o*=+c.opacity; if(c.visibility==='hidden'||c.display==='none') return 0; } return o; };
  (function f(t){ try{ const d=D(), k=d.width/390, now=performance.now(); window.__G.im.push(Math.round(now-av)); av=now;
    const cs=document.getElementById('createSheet'), vis=cs&&cs.classList.contains('show')&&op(cs)>0.5;
    if(vis){
      document.querySelectorAll('#createSheet canvas[data-trace]').forEach(cv=>{ const c=cv.previousElementSibling; if(!c) return; const a=cv.getBoundingClientRect(), b=c.getBoundingClientRect(), m=8*k;
        if(a.width<2||b.width<1) return; if(a.right<b.left-m||a.left>b.right+m||a.bottom<b.top-m||a.top>b.bottom+m) window.__G.A.push([Math.round(now-t0), (c.textContent||'').slice(0,20), Math.round((a.left-d.left)/k), Math.round((a.top-d.top)/k), Math.round((b.left-d.left)/k), Math.round((b.top-d.top)/k)]); });
      const rail=document.getElementById('csPinceau'), ph=document.querySelector('#csPhrase .ph-txt, #nueePhrase .ph-txt'), phv=ph&&ph.offsetParent;
      if(rail && op(rail)>0.5 && !cs.classList.contains('pp-ouvert') && !cs.classList.contains('pp-choix')){ const ry=(rail.getBoundingClientRect().top-d.top)/k; let enc=0;
        if(phv){ const w=document.createTreeWalker(ph, NodeFilter.SHOW_TEXT); let tn;   /* l'encre VISIBLE : ni une copie cachée (la préparation d'un tracé), ni un mot découpé à vide (un détracé fini) */
          while((tn=w.nextNode())){ const pe=tn.parentElement; if(!pe || !tn.nodeValue.trim()) continue; let cache=false; for(let x=pe;x&&x!==ph.parentElement;x=x.parentElement){ const c=getComputedStyle(x); if(c.visibility==='hidden'||+c.opacity<0.05||/polygon\(0px 0px, ?0px 0px, ?0px 0px\)/.test(c.clipPath||'')){ cache=true; break; } } if(cache) continue;
            const rg=document.createRange(); rg.selectNodeContents(tn); [].forEach.call(rg.getClientRects(), q=>{ if(q.width>1&&q.height>1) enc=Math.max(enc,(q.bottom-d.top)/k); }); } }
        if(enc && ry<enc-2) window.__G.B.push([Math.round(now-t0),'sur la phrase',Math.round(ry),Math.round(enc)]);
        /* ⚠ v203 : sans encre visible (toute la phrase découpée), la place relative n'existe pas — le juge lisait une variable absente (`pt`) et comparait ensuite à une valeur périmée */
        const rel=enc?ry-enc:null; if(rel!=null && railAv!=null && Math.abs(rel-railAv)>14) window.__G.B.push([Math.round(now-t0),'saut',Math.round(railAv),Math.round(rel)]);   /* relatif au bas VISIBLE de la phrase : « la suite glisse avec elle » ; le mouvement du clavier (Q598) les emporte ensemble */
        railAv=(rel!=null?rel:railAv); } else railAv=null;
      const iv=!!(window._ppInvite&&_ppInvite.etat().visible); if(iv!==invAv){ window.__G.inv.push([Math.round(now-t0), iv]); invAv=iv; } }
  }catch(e){ window.__G.err=String(e); } if(performance.now()-t0<9000) R(f); })(performance.now()); }"""
def ouvre_nat(pg, nat):
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
def passe(b, quoi, T):
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    ouvre_nat(pg, 'promi')
    for _ in range(4):
        B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(900)
        if pg.evaluate("()=>{const a=document.activeElement;return !!a&&a.id==='phIn';}"): break
    pg.keyboard.type('lire', delay=40); pg.wait_for_timeout(300)
    pg.evaluate(SONDE); pg.keyboard.press('Enter'); pg.wait_for_timeout(T)
    if quoi == 'S': B.tap_sel(pg, '#csPhrase [data-ph=sens]')
    else:
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(500); ouvre_nat(pg, 'chiche' if T % 2 == 0 else 'nuee')
    pg.wait_for_timeout(5000)
    G = pg.evaluate("()=>window.__G"); fin = pg.evaluate("""()=>{ const t=document.querySelector('#csPhrase .ph-txt, #nueePhrase .ph-txt'), q=document.querySelector('#csPhrase .ph-m[data-ph="qui"]'), i=window._ppInvite?_ppInvite.etat():{};
      return {fs:t?t.style.fontSize:null, qui:q?(q.textContent||'').replace(/\\s+/g,' ').trim():null, inv:!!i.visible, nat:document.getElementById('createSheet').getAttribute('data-kind'), pass:document.querySelectorAll('#createSheet canvas.passage-flaques').length}; }""")
    ch = pg.evaluate("()=>{ const c=document.getElementById('createSheet'); return c.classList.contains('show'); }")
    long_ = sorted(G['im'])[-5:]; ctx.close()
    return G, fin, long_
with sync_playwright() as p:
    b = p.webkit.launch(); charge = B.charge(); print('redteam_genese_nature — %s · charge %.1f' % (F, charge))
    for quoi in QUOI:
        tailles = []
        for T in TS:
            G, fin, lg = passe(b, quoi, T); L = '[%s · t=%d]' % ('sens' if quoi == 'S' else 'nature', T)
            juge(L + ' A · aucune lettre tracée hors de sa place', not G['A'], G['A'][:3])
            juge(L + ' B · le rail jamais sur la phrase, jamais un saut', not G['B'], G['B'][:3])
            # C — S : la genèse interrompue se retire puis renaît à sa nouvelle place (« s'interrompt proprement, la nouvelle se fait entière ») : à la fin, l'invite là, aucun calque de
            #     passage resté ; N : une page neuve, la parole pas encore validée — aucun trait, rien de la genèse d'avant (ni invite, ni passage, ni départ)
            juge(L + ' C · ' + ('la genèse se fait entière : l\'invite là, aucun passage resté' if quoi == 'S' else 'page neuve : rien de la genèse d\'avant (invite, passage, départ)'),
                 (fin['inv'] if quoi == 'S' else not fin['inv']) and fin['pass'] == 0, '%s · passages %d · %s' % (fin['nat'], fin['pass'], G['inv']))
            if quoi == 'S':
                tailles.append(fin['fs']); juge(L + ' D · « moi » à la place, le trait né ; la taille ≥ 30', fin['qui'] == 'moi' and fin['fs'] and float(fin['fs'][:-2]) >= 30, '%s · %s' % (fin['qui'], fin['fs']))
            print('      images les plus longues %s ms' % lg, flush=True)
        if quoi == 'S': juge('[sens] D · la même taille finale à chaque instant', len(set(tailles)) == 1, tailles)
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
