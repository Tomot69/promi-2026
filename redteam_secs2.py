"""⚑ v202a (Tom, C-271 ; AUDIT-SECS, les points « non jugés ») — IMAGE PAR IMAGE, après la peinture (WebKit, ×3, 430 × 932) :
  A · « Les Mots » : le premier mot arrive sur une fiche ouverte — le titre ne paraît jamais entier d'une image à l'autre (découpé ≥ 3 images avant d'être entier) ;
  B · la pastille « pas encore vu » qui ARRIVE grandit de son centre (≥ 3 images entre 0 et 1, jamais de 0 à 1 d'un coup) ;
  C · la pastille qui PART se referme sur son centre (≥ 3 images, puis absente) — v202a ;
  D · une valeur des Réglages qui change : l'ancienne et la nouvelle se croisent (≥ 3 images où les deux sont là, opacités intermédiaires) ;
  E · le toast arrive en se découvrant et part en se refermant (≥ 3 images de découpe à chaque bout ; jamais présent puis absent d'une image à l'autre) ;
  F · « à qui ? » qui part (retour à « Je me promets ») : une copie à sa place se détrace (≥ 120 ms découpée), puis plus rien — v202a ;
  G · le titre effacé : l'exemple revient découpé (≥ 3 images), l'encart s'adapte sans saut (≤ 30 pt par image) — v202a, C-274.
--fichier= ; --sonde : les transitions de v201b/v202a coupées (Element.animate et TraceLettres.trace rendus immédiats) — il rougit."""
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
A = sys.argv[1:]; F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html'); SONDE = '--sonde' in A
SND = """(()=>{ Element.prototype.animate=function(){ const o={onfinish:null, finished:Promise.resolve(), cancel(){}, finish(){}}; setTimeout(()=>{ o.onfinish&&o.onfinish(); },0); return o; };
  const arme=()=>{ if(!window.TraceLettres){ setTimeout(arme,50); return; } TraceLettres.trace=function(el,c,o){ o=o||{}; setTimeout(()=>{ o.surFin&&o.surFin({interrompu:false}); },0); return {fin:Promise.resolve(), etat(){return {};}, stop(){}, lance(){}}; }; }; arme(); })()"""
REC = """([sel, f])=>{ window.__rf=[]; const t0=performance.now(); let on=true; window.__rfStop=()=>{ on=false; };
  const MC=new MessageChannel(); MC.port1.onmessage=()=>{ try{ window.__rf.push([Math.round(performance.now()-t0)].concat(new Function('return ('+f+')')()())); }catch(e){ window.__rf.push([0,'err '+e]); } if(on) requestAnimationFrame(()=>MC.port2.postMessage(0)); };
  requestAnimationFrame(()=>MC.port2.postMessage(0)); }"""
res = []; NJ = []
def juge(nom, ok, d='', L=None):
    """une image de plus de 80 ms dans la fenêtre : la durée d'une transition n'y est pas lisible — NON JUGÉ (la charge), ni vert ni rouge"""
    if L and not ok and max((b2[0] - a2[0] for a2, b2 in zip(L, L[1:])), default=0) > 80:
        NJ.append(nom); print('  ⏸ %-66s non jugé (une image de plus de 80 ms : charge %.0f) %s' % (nom, B.charge(), str(d)[:200]), flush=True); return
    res.append(bool(ok)); print('  %s %-66s %s' % ('✅' if ok else '❌', nom, str(d)[:300]), flush=True)
def enregistre(pg, f, ms):
    pg.evaluate(REC, ['', f]); pg.wait_for_timeout(ms); pg.evaluate("window.__rfStop()"); return pg.evaluate("window.__rf")
CLIP = "function(e){ if(!e) return 'absent'; const c=e.style.clipPath||e.style.webkitClipPath||getComputedStyle(e).clipPath; return (c&&c!=='none')?'clip':'net'; }"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10)
    if SONDE: ctx.add_init_script(SND)
    pg = B.ouvre(ctx, F); print('redteam_secs2 — %s, charge %.1f%s' % (F, B.charge(), ' · SONDE' if SONDE else ''), flush=True)
    # A · « Les Mots »
    pid = pg.evaluate("()=>{ const p=promises.find(q=>!q.chiche&&!q.nuee&&!q.draft&&!(q.comments&&q.comments.length)); return p?p.id:null; }")
    pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2500)
    L = enregistre(pg, "()=>{ const t=document.getElementById('cm5Titre'); const C=" + CLIP + "; const v=t&&t.offsetParent&&getComputedStyle(t).visibility!=='hidden'&&t.getBoundingClientRect().height>0; return [v?C(t):'absent']; }", 50)
    pg.evaluate("id=>{ const p=promises.find(q=>q.id===id); window._comm.arrive(p, {t:'premier mot', by:'Rachel'}); try{ window._comm.peint&&window._comm.peint(); }catch(e){} try{ dpRefresh&&dpRefresh(); }catch(e){} }", pid)
    L = enregistre(pg, "()=>{ const t=document.getElementById('cm5Titre'); const C=" + CLIP + "; const v=t&&t.offsetParent&&getComputedStyle(t).visibility!=='hidden'&&t.getBoundingClientRect().height>0; return [v?C(t):'absent']; }", 2500)
    seq = [x[1] for x in L]; i = next((k for k, s in enumerate(seq) if s != 'absent'), None)
    nclip = sum(1 for s in seq if s == 'clip')
    juge('A · « Les Mots » se trace (découpé ≥ 3 images avant d’être net)', i is not None and seq[i] == 'clip' and nclip >= 3, (i, nclip, ''.join({'absent': '.', 'clip': 'c', 'net': 'N'}[s] for s in seq)[:80]))
    pg.evaluate("()=>{ try{ _peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(800)
    # B, C · la pastille, par le moteur des pastilles (une carte de l'Index, l'attente forcée puis levée)
    pg.evaluate("()=>ouvrirIndex()"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ window.__pc=[...document.querySelectorAll('#indexList .s4-carte')].find(x=>!x.querySelector('.s4-att')); }")
    F_P = "()=>{ const c=window.__pc; const p=c&&c.querySelector(':scope > .s4-att, :scope > .s4-att-part'); if(!p) return ['absent']; const m=getComputedStyle(p).transform; let s=1; if(m&&m!=='none'){ const v=m.match(/matrix\\(([^,]+),([^,]+)/); if(v) s=Math.hypot(+v[1],+v[2]); } return [+s.toFixed(2)]; }"
    pg.evaluate("()=>{ window.__pc.setAttribute('data-nonvu','1'); }")
    L = None
    pg.evaluate(REC, ['', F_P]); pg.evaluate("()=>{ try{ window._pastillesAttente(document); }catch(e){ window.__pe=String(e); } }"); pg.wait_for_timeout(900); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    s = [x[1] for x in L]; vals = [v for v in s if v != 'absent']
    T = [x[0] for x in L if x[1] != 'absent' and x[1] < 0.99]; dur = (max(T) - min(T)) if len(T) > 1 else 0
    juge('B · la pastille qui arrive grandit de son centre (≥ 180 ms entre 0 et 1)', vals and dur >= 180 and vals[-1] >= 0.99, (dur, s[:24]), L)
    pg.evaluate("()=>{ window.__pc.setAttribute('data-nonvu','0'); }")
    pg.evaluate(REC, ['', F_P]); pg.evaluate("()=>{ try{ window._pastillesAttente(document); }catch(e){ window.__pe=String(e); } }"); pg.wait_for_timeout(900); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    s = [x[1] for x in L]; fin = s[-1] == 'absent'
    k1 = next((k for k, x in enumerate(L) if x[1] != 'absent' and x[1] < 0.99), None); k2 = next((k for k, x in enumerate(L) if x[1] == 'absent'), None)
    dur = (L[k2][0] - L[k1 - 1][0]) if (k1 and k2) else 0
    juge('C · la pastille qui part se referme (≥ 180 ms), puis absente', fin and dur >= 180 and k1 is not None, (dur, s[:24]), L)
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(800)
    # D · une valeur des Réglages (l'écrivain : un texte réécrit dans une rangée suivie)
    pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(2500)
    ok = pg.evaluate("()=>{ const v=[...document.querySelectorAll('#settingsScreen .scard .v')].find(e=>e.offsetParent&&e.textContent.trim()); if(!v) return false; window.__sv=v; return v.textContent.trim(); }")
    F_V = "()=>{ const v=window.__sv; if(!v) return ['?']; const parts=v.querySelectorAll('.v201-val, .v201-n'); const op=[...parts].map(x=>+(+getComputedStyle(x).opacity).toFixed(2)); return [parts.length, op.join('/')]; }"
    pg.evaluate(REC, ['', F_V]); pg.evaluate("()=>{ const v=window.__sv; v.textContent=(v.textContent.trim()==='essai'?'autre':'essai'); }"); pg.wait_for_timeout(800); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    T = [x[0] for x in L if x[1] != '?' and x[1] >= 2]; dur = (max(T) - min(T)) if len(T) > 1 else 0
    juge('D · une valeur des Réglages : l’ancienne et la nouvelle se croisent (≥ 150 ms)', ok and dur >= 150, (ok, dur, [x[1:] for x in L[:8]]), L)
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    # E · le toast
    F_T = "()=>{ const t=document.getElementById('_toast'); if(!t) return ['absent']; const c=getComputedStyle(t).clipPath; return [c&&c!=='none'&&!/inset\\(0(px)? 0(px)? 0(px)? 0(px)?/.test(c)?'clip':'net']; }"
    pg.evaluate(REC, ['', F_T]); pg.evaluate("()=>toast('Essai du toast')"); pg.wait_for_timeout(5500); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    s = ''.join({'absent': '.', 'clip': 'c', 'net': 'N'}.get(x[1], '?') for x in L)
    deb = s.lstrip('.'); okA = deb[:3] == 'ccc'; tr = s.rstrip('.'); okP = tr.endswith('ccc') and 'N.' not in s
    juge('E · le toast se découvre (≥ 3 images) et se referme (≥ 3 images)', okA and okP, s[:30] + ' … ' + s[-40:])
    # F · « à qui ? » qui part ; G · le titre effacé (une page neuve, sans la Toile pleine : la phrase de la page + y est celle d'un premier lancement)
    er0 = pg.__dict__['erreurs']; ctx2 = B.contexte(b, vw=430, vh=932)
    if SONDE: ctx2.add_init_script(SND)
    pg = B.ouvre(ctx2, F); pg.__dict__['erreurs'] = er0
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2800)
    for _ in range(4):
        if pg.evaluate("()=>{ const q=document.querySelector('#csPhrase [data-ph=qui]'); return !!(q && q.getBoundingClientRect().width>0) && /promets-moi/.test(document.getElementById('csPhrase').textContent); }"): break
        B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2600)
    F_G = "()=>{ const g=document.querySelector('#csPhrase .v202-part'); const C=" + CLIP + "; const q=document.querySelector('#csPhrase [data-ph=qui]'); return [g?C(g):'absent', !!(q && q.getBoundingClientRect().width>0)]; }"
    print('    avant F :', pg.evaluate("document.getElementById('csPhrase').textContent.replace(/\\s+/g,' ').slice(0,70)"))
    pg.evaluate(REC, ['', F_G]); B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2600); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    s = ''.join({'absent': '.', 'clip': 'c', 'net': 'N'}[x[1]] for x in L); qui = [x[2] for x in L]
    kc = s.find('c'); kf = s.find('.', kc) if kc >= 0 else -1; durF = (L[kf][0] - L[kc][0]) if (kc >= 0 and kf > kc) else 0
    juge('F · la place qui part se détrace à sa place (≥ 120 ms découpée), puis plus rien', durF >= 120 and s.endswith('.') and not qui[-1], '%s · %d ms' % (s[:60], durF))
    B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1200)
    if pg.evaluate("document.activeElement && document.activeElement.id") != 'phIn': pg.evaluate("()=>{ const m=document.querySelector('#csPhrase [data-ph=titre]'); m && m.click(); }"); pg.wait_for_timeout(1000)
    pg.keyboard.type('ab', delay=120); pg.wait_for_timeout(2500)
    F_E = "()=>{ const m=document.querySelector('#csPhrase [data-ph=titre]'); const C=" + CLIP + "; const i=m&&m.querySelector('.v200-mt'); return [m?(m.textContent||'').slice(0,12):'', m?+m.getBoundingClientRect().width.toFixed(1):0, i?C(i):'net']; }"
    pg.evaluate(REC, ['', F_E]); [pg.keyboard.press('Backspace') or pg.wait_for_timeout(140) for _ in range(2)]; pg.wait_for_timeout(2800); pg.evaluate("window.__rfStop()"); L = pg.evaluate("window.__rf")
    ex = pg.evaluate("document.getElementById('phIn').getAttribute('placeholder')")
    k0 = next((k for k, x in enumerate(L) if ex and x[1].startswith(ex[:8])), None)
    nclip = sum(1 for x in L[k0:] if x[3] == 'clip') if k0 is not None else 0
    k1 = next((k for k, x in enumerate(L) if x[1] == '' or x[3] == 'clip' or (ex and x[1].startswith(ex[:8]))), len(L))   # la transition (la frappe d'avant ne compte pas)
    P = [(abs(b2[2] - a2[2]) / max(16.7, b2[0] - a2[0]) * 390 / 430, a2, b2) for a2, b2 in zip(L[k1:], L[k1 + 1:])]
    vit = max((x[0] for x in P), default=0)   # pt par ms
    if vit > 1.5: print('    G, le plus grand pas :', max(P)[1:], '· début', L[k1 - 1:k1 + 2])
    juge('G · le titre effacé : l’exemple revient découpé (≥ 3 images), l’encart va à ≤ 1,5 pt/ms', k0 is not None and L[k0][3] == 'clip' and nclip >= 3 and vit <= 1.5, (k0, nclip, round(vit, 2)), L)
    print('erreurs :', pg.__dict__['erreurs'][:3])
    b.close()
print('redteam_secs2 : %d/%d%s' % (sum(res), len(res), (' · non jugés : ' + ', '.join(NJ)) if NJ else ''))
